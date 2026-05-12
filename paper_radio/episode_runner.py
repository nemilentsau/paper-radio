import argparse
import json
from pathlib import Path
from typing import Any

from paper_radio.agent_runner import run_job
from paper_radio.config import PROJECT_ROOT

READINESS_FIELDS = ("one_line_claim", "strongest_point", "weakest_point", "verdict")
PLACEHOLDER_MARKERS = ("review incomplete", "research incomplete")


class ReviewReadinessError(RuntimeError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest_path(root: Path, episode_path: str) -> Path:
    return root / episode_path / "manifest.json"


def _review_manifest_path(root: Path) -> Path:
    return root / "jobs" / "reviews.jsonl"


def _source_dossier_manifest_path(root: Path) -> Path:
    return root / "jobs" / "source-dossiers.jsonl"


def _paper_ids(manifest: dict[str, Any]) -> list[str]:
    return [str(paper_id) for paper_id in manifest["paper_ids"]]


def _script_job_id(manifest: dict[str, Any]) -> str:
    return str(manifest.get("script_job_id", f"{manifest['episode_id']}-dossier"))


def _is_placeholder(value: object) -> bool:
    return isinstance(value, str) and any(marker in value.casefold() for marker in PLACEHOLDER_MARKERS)


def validate_reviews_ready(root: Path, paper_ids: list[str]) -> None:
    errors: list[str] = []
    for paper_id in paper_ids:
        review_path = root / "data" / "reviews" / f"{paper_id}.json"
        if not review_path.exists():
            errors.append(f"{review_path.relative_to(root)} is missing")
            continue
        try:
            record = _read_json(review_path)
        except json.JSONDecodeError as error:
            errors.append(f"{review_path.relative_to(root)} is not valid JSON: {error}")
            continue
        for field in READINESS_FIELDS:
            value = record.get(field)
            if not isinstance(value, str) or not value.strip() or _is_placeholder(value):
                errors.append(f"{review_path.relative_to(root)} has incomplete field `{field}`")
        for field in ("research_score", "podcast_score"):
            if not isinstance(record.get(field), int | float):
                errors.append(f"{review_path.relative_to(root)} has invalid field `{field}`")
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
        commands.append(run_job(review_manifest, f"review-{paper_id}", agent, root=root))

    validate_reviews_ready(root, paper_ids)
    commands.append(run_job(_source_dossier_manifest_path(root), _script_job_id(manifest), agent, root=root))
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
