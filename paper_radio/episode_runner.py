import argparse
import json
from pathlib import Path
from typing import Any

from paper_radio.agent_runner import run_job
from paper_radio.config import PROJECT_ROOT
from paper_radio.output_validation import OutputValidationError, validate_review_file


class ReviewReadinessError(OutputValidationError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest_path(root: Path, episode_path: str) -> Path:
    return root / episode_path / "manifest.json"


def _review_manifest_path(root: Path) -> Path:
    return root / "jobs" / "reviews.jsonl"


def _source_dossier_manifest_path(root: Path) -> Path:
    return root / "jobs" / "source-dossiers.jsonl"


def _memory_update_manifest_path(root: Path) -> Path:
    return root / "jobs" / "memory-updates.jsonl"


def _paper_ids(manifest: dict[str, Any]) -> list[str]:
    return [str(paper_id) for paper_id in manifest["paper_ids"]]


def _script_job_id(manifest: dict[str, Any]) -> str:
    return str(manifest.get("script_job_id", f"{manifest['episode_id']}-dossier"))


def _promote_memory_job_id(manifest: dict[str, Any]) -> str:
    return f"{manifest['episode_id']}-promote-memory"


def validate_reviews_ready(root: Path, paper_ids: list[str]) -> None:
    errors: list[str] = []
    for paper_id in paper_ids:
        try:
            validate_review_file(root, paper_id)
        except OutputValidationError as error:
            errors.append(str(error))
    if errors:
        detail = "\n- ".join(errors)
        raise ReviewReadinessError(f"Review records are not production-ready:\n- {detail}")


def plan_episode_jobs(episode_path: str, root: Path = PROJECT_ROOT) -> list[dict[str, str]]:
    manifest = _read_json(_manifest_path(root, episode_path))
    plan = [
        {"kind": "review", "manifest": str(_review_manifest_path(root)), "job_id": f"review-{paper_id}"}
        for paper_id in _paper_ids(manifest)
    ]
    plan.append(
        {
            "kind": "source_dossier",
            "manifest": str(_source_dossier_manifest_path(root)),
            "job_id": _script_job_id(manifest),
        }
    )
    plan.append(
        {
            "kind": "promote_memory",
            "manifest": str(_memory_update_manifest_path(root)),
            "job_id": _promote_memory_job_id(manifest),
        }
    )
    return plan


def run_episode(
    episode_path: str,
    agent: str,
    root: Path = PROJECT_ROOT,
    dry_run: bool = False,
) -> list[list[str]]:
    manifest = _read_json(_manifest_path(root, episode_path))
    paper_ids = _paper_ids(manifest)
    if dry_run:
        return [[step["manifest"], step["job_id"]] for step in plan_episode_jobs(episode_path, root)]

    commands: list[list[str]] = []
    review_manifest = _review_manifest_path(root)
    for paper_id in paper_ids:
        try:
            validate_review_file(root, paper_id)
            continue
        except OutputValidationError:
            pass
        commands.append(run_job(review_manifest, f"review-{paper_id}", agent, root=root))

    validate_reviews_ready(root, paper_ids)
    commands.append(run_job(_source_dossier_manifest_path(root), _script_job_id(manifest), agent, root=root))
    commands.append(run_job(_memory_update_manifest_path(root), _promote_memory_job_id(manifest), agent, root=root))
    return commands


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one Paper Radio episode through the required production order")
    parser.add_argument("--episode-path", required=True, help="Episode dir, e.g. episodes/2026-05-12/01_peft")
    parser.add_argument("--agent", required=True, choices=("codex", "claude"), help="Headless agent backend")
    parser.add_argument("--dry-run", action="store_true", help="Print the job order without executing jobs")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = run_episode(args.episode_path, args.agent, dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
