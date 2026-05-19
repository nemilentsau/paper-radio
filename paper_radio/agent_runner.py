import argparse
import json
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from paper_radio.agent_jobs import build_job_prompt, find_job
from paper_radio.config import PROJECT_ROOT
from paper_radio.memory.cards import apply_memory_update_file
from paper_radio.memory.notes import write_memory_note
from paper_radio.notebooklm_handoff import handoff_path_for_bundle, render_notebooklm_handoff
from paper_radio.output_validation import (
    OutputValidationError,
    validate_job_output,
    validate_source_dossier_record,
)
from paper_radio.source_fetch import validate_review_job_sources


def check_agent_available(agent: str) -> None:
    if agent == "codex":
        command = ["codex", "--version"]
    elif agent == "claude":
        command = ["claude", "--version"]
    else:
        raise ValueError("agent must be 'codex' or 'claude'")

    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or f"exit code {result.returncode}").strip()
        raise RuntimeError(f"{agent} CLI is not usable: {detail}")


def build_codex_command(job: Mapping[str, object], prompt: str) -> list[str]:
    command = [
        "codex",
        "exec",
        "--sandbox",
        "workspace-write",
        "--output-schema",
        str(job["schema_path"]),
        "-o",
        str(job["output_path"]),
        prompt,
    ]
    if job.get("kind") == "triage":
        command[2:2] = [
            "--ignore-user-config",
            "--model",
            "gpt-5.4-mini",
            "-c",
            'model_reasoning_effort="low"',
        ]
    return command


def build_claude_command(job: Mapping[str, object], prompt: str, root: Path = PROJECT_ROOT) -> list[str]:
    schema = (root / str(job["schema_path"])).read_text(encoding="utf-8")
    return [
        "claude",
        "-p",
        prompt,
        "--output-format",
        "json",
        "--json-schema",
        schema,
    ]


def _resolve_project_path(root: Path, path: object) -> Path:
    candidate = Path(str(path))
    if candidate.is_absolute():
        return candidate
    return root / candidate


def _normalize_source_dossier_output(job: Mapping[str, object], output: Any) -> Any:
    if job.get("kind") != "source_dossier" or not isinstance(output, dict):
        return output
    normalized = dict(output)
    existing_citations = normalized.get("citations", [])
    if not isinstance(existing_citations, list):
        existing_citations = []
    citations = [str(citation) for citation in existing_citations if str(citation)]
    review_paths = job.get("review_paths", [])
    if not isinstance(review_paths, list | tuple):
        review_paths = []
    for review_path in review_paths:
        review_path_text = str(review_path)
        if review_path_text not in citations:
            citations.append(review_path_text)
    normalized["citations"] = citations
    return normalized


def _extract_claude_output(stdout: str) -> Any:
    payload: Any = json.loads(stdout)
    if isinstance(payload, dict) and "structured_output" in payload:
        output = payload["structured_output"]
    elif isinstance(payload, dict) and "result" in payload:
        output = payload["result"]
    else:
        output = payload
    if isinstance(output, str):
        stripped = output.strip()
        if stripped:
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError:
                return output
            if isinstance(parsed, dict | list):
                return parsed
    return output


def _write_source_dossier_bundle(job: Mapping[str, object], output: Any, root: Path) -> None:
    if str(job.get("kind", "")) != "source_dossier":
        return
    if not isinstance(output, dict):
        return
    dossier = output.get("research_dossier_markdown")
    bundle_output_path = job.get("bundle_output_path")
    if not isinstance(dossier, str) or not bundle_output_path:
        return
    dossier_path = _resolve_project_path(root, bundle_output_path)
    dossier_path.parent.mkdir(parents=True, exist_ok=True)
    dossier_path.write_text(dossier, encoding="utf-8")
    handoff_path = handoff_path_for_bundle(dossier_path)
    handoff_path.write_text(render_notebooklm_handoff(job, output), encoding="utf-8")


def _write_structured_output(job: Mapping[str, object], output: Any, root: Path) -> None:
    output = _normalize_source_dossier_output(job, output)
    output_path = _resolve_project_path(root, job["output_path"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(output, str):
        output_path.write_text(output, encoding="utf-8")
    else:
        output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _write_source_dossier_bundle(job, output, root)


def _write_codex_sidecar_outputs(job: Mapping[str, object], root: Path) -> None:
    output_path = _resolve_project_path(root, job["output_path"])
    if not output_path.exists():
        return
    try:
        output = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    output = _normalize_source_dossier_output(job, output)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _write_source_dossier_bundle(job, output, root)


def _remove_invalid_outputs(job: Mapping[str, object], root: Path) -> None:
    paths = [job.get("output_path")]
    if job.get("kind") == "source_dossier":
        paths.append(job.get("bundle_output_path"))
        bundle_output_path = job.get("bundle_output_path")
        if bundle_output_path:
            paths.append(handoff_path_for_bundle(_resolve_project_path(root, bundle_output_path)))
    for path in paths:
        if not path:
            continue
        output_path = _resolve_project_path(root, path)
        if output_path.exists():
            output_path.unlink()


def _validate_written_job_output(job: Mapping[str, object], root: Path) -> None:
    try:
        validate_job_output(root, job)
    except OutputValidationError:
        _remove_invalid_outputs(job, root)
        raise


def _apply_valid_job_side_effects(job: Mapping[str, object], root: Path) -> None:
    kind = str(job.get("kind", ""))
    if kind == "source_dossier":
        output_path = _resolve_project_path(root, job["output_path"])
        output = json.loads(output_path.read_text(encoding="utf-8"))
        if isinstance(output, Mapping):
            write_memory_note(root, job, output)
    elif kind == "promote_memory":
        apply_memory_update_file(root, job)


def run_job(
    manifest_path: Path,
    job_id: str,
    agent: str,
    root: Path = PROJECT_ROOT,
    dry_run: bool = False,
) -> list[str]:
    job = find_job(manifest_path, job_id)
    validate_review_job_sources(root, job)
    if not dry_run:
        check_agent_available(agent)
    prompt = build_job_prompt(job, root=root)
    if agent == "codex":
        command = build_codex_command(job, prompt)
    elif agent == "claude":
        command = build_claude_command(job, prompt, root)
    else:
        raise ValueError("agent must be 'codex' or 'claude'")

    if dry_run:
        return command

    _resolve_project_path(root, job["output_path"]).parent.mkdir(parents=True, exist_ok=True)

    if agent == "codex":
        subprocess.run(command, cwd=root, check=True)
        _write_codex_sidecar_outputs(job, root)
        _validate_written_job_output(job, root)
        _apply_valid_job_side_effects(job, root)
    else:
        result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=True)
        output = _extract_claude_output(result.stdout)
        output = _normalize_source_dossier_output(job, output)
        if job.get("kind") == "source_dossier" and isinstance(output, Mapping):
            validate_source_dossier_record(job, output, root=root)
        _write_structured_output(job, output, root)
        _validate_written_job_output(job, root)
        _apply_valid_job_side_effects(job, root)
    return command


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Codex CLI or Claude Code headless Paper Radio jobs")
    parser.add_argument("--manifest", required=True, type=Path, help="JSONL job manifest path")
    parser.add_argument("--job-id", required=True, help="Job id from the manifest")
    parser.add_argument("--agent", required=True, choices=("codex", "claude"), help="Headless agent backend")
    parser.add_argument("--dry-run", action="store_true", help="Print the command without executing it")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    manifest = args.manifest if args.manifest.is_absolute() else PROJECT_ROOT / args.manifest
    command = run_job(manifest, args.job_id, args.agent, dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(command, indent=2))


if __name__ == "__main__":
    main()
