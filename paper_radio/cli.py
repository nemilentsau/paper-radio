import argparse
import json
from datetime import date
from pathlib import Path

from paper_radio.agent_jobs import write_agent_job_artifacts
from paper_radio.agent_runner import run_job
from paper_radio.arxiv import fetch_recent_candidates, ingest_arxiv_ids
from paper_radio.config import PROJECT_ROOT
from paper_radio.daily_run import (
    DEFAULT_DAILY_MAX_RESULTS,
    DEFAULT_EPISODE_SLUG,
    DEFAULT_EPISODE_TYPE,
    default_daily_title,
    run_daily,
)
from paper_radio.episode_manifest import create_episode_manifest
from paper_radio.episode_planning import write_episode_job_manifests
from paper_radio.episode_runner import run_episode
from paper_radio.source_fetch import fetch_paper_source
from paper_radio.triage_planning import write_triage_job_manifest
from paper_radio.triage_promotion import promote_triage_results


def cmd_init(args: argparse.Namespace) -> None:
    write_agent_job_artifacts(PROJECT_ROOT)
    print("Wrote Paper Radio schema and job scaffolding")


def cmd_run_job(args: argparse.Namespace) -> None:
    manifest = Path(args.manifest)
    if not manifest.is_absolute():
        manifest = PROJECT_ROOT / manifest
    command = run_job(manifest, args.job_id, args.agent, dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(command, indent=2))


def cmd_candidate_arxiv(args: argparse.Namespace) -> None:
    paths = fetch_recent_candidates(
        PROJECT_ROOT,
        categories=args.category,
        max_results=args.max_results,
        run_date=args.run_date or date.today().isoformat(),
    )
    print(json.dumps({"json_path": str(paths.json_path), "markdown_path": str(paths.markdown_path)}, indent=2))


def cmd_ingest_arxiv(args: argparse.Namespace) -> None:
    papers = ingest_arxiv_ids(PROJECT_ROOT, args.id)
    print(json.dumps({"paper_ids": [paper.paper_id for paper in papers]}, indent=2))


def cmd_fetch_sources(args: argparse.Namespace) -> None:
    paths = [fetch_paper_source(PROJECT_ROOT, paper_id) for paper_id in args.paper_id]
    print(
        json.dumps(
            {
                "sources": [
                    {
                        "pdf_path": str(path.pdf_path),
                        "full_text_path": str(path.full_text_path),
                    }
                    for path in paths
                ]
            },
            indent=2,
        )
    )


def cmd_plan_triage(args: argparse.Namespace) -> None:
    candidate_path = Path(args.candidate_path)
    result = write_triage_job_manifest(PROJECT_ROOT, candidate_path)
    print(json.dumps({"triage_job_ids": result.job_ids}, indent=2))


def cmd_promote_triage(args: argparse.Namespace) -> None:
    result = promote_triage_results(
        PROJECT_ROOT,
        triage_dir=Path(args.triage_dir),
        manifest_path=Path(args.manifest),
    )
    print(
        json.dumps(
            {
                "promoted_paper_ids": result.promoted_paper_ids,
                "skipped_paper_ids": result.skipped_paper_ids,
                "unrecognized_paper_ids": result.unrecognized_paper_ids,
            },
            indent=2,
        )
    )


def cmd_create_episode(args: argparse.Namespace) -> None:
    manifest_path = create_episode_manifest(
        root=PROJECT_ROOT,
        episode_path=args.episode_path,
        title=args.title,
        episode_type=args.episode_type,
        paper_ids=args.paper_id,
        episode_id=args.episode_id,
    )
    print(json.dumps({"manifest_path": str(manifest_path)}, indent=2))


def cmd_plan_episode(args: argparse.Namespace) -> None:
    result = write_episode_job_manifests(PROJECT_ROOT, args.episode_path)
    print(
        json.dumps(
            {
                "review_job_ids": result.review_job_ids,
                "source_dossier_job_id": result.source_dossier_job_id,
                "promote_memory_job_id": result.promote_memory_job_id,
            },
            indent=2,
        )
    )


def cmd_run_episode(args: argparse.Namespace) -> None:
    result = run_episode(args.episode_path, args.agent, dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(result, indent=2))


def cmd_daily_run(args: argparse.Namespace) -> None:
    report = run_daily(
        root=PROJECT_ROOT,
        run_date=args.run_date or date.today().isoformat(),
        categories=args.category,
        max_results=args.max_results,
        episode_slug=args.episode_slug,
        title=args.title,
        episode_type=args.episode_type,
        agent=args.agent,
        fresh=args.fresh,
    )
    print(json.dumps(report.to_dict(), indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Paper Radio production pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.set_defaults(func=cmd_init)

    run_job_parser = subparsers.add_parser("run-job")
    run_job_parser.add_argument("--manifest", required=True, help="JSONL job manifest path")
    run_job_parser.add_argument("--job-id", required=True, help="Job id from the manifest")
    run_job_parser.add_argument("--agent", required=True, choices=("codex", "claude"), help="Headless agent backend")
    run_job_parser.add_argument("--dry-run", action="store_true", help="Print the command without executing it")
    run_job_parser.set_defaults(func=cmd_run_job)

    candidate_arxiv_parser = subparsers.add_parser("candidate-arxiv")
    candidate_arxiv_parser.add_argument(
        "--category",
        action="append",
        required=True,
        help="arXiv category, e.g. cs.LG. Repeat for multiple categories.",
    )
    candidate_arxiv_parser.add_argument("--max-results", type=int, default=100, help="Maximum arXiv results to fetch")
    candidate_arxiv_parser.add_argument("--run-date", help="Candidate batch date, defaults to today")
    candidate_arxiv_parser.set_defaults(func=cmd_candidate_arxiv)

    ingest_arxiv_parser = subparsers.add_parser("ingest-arxiv")
    ingest_arxiv_parser.add_argument("--id", action="append", required=True, help="arXiv ID. Repeat for multiple IDs.")
    ingest_arxiv_parser.set_defaults(func=cmd_ingest_arxiv)

    fetch_sources_parser = subparsers.add_parser("fetch-sources")
    fetch_sources_parser.add_argument(
        "--paper-id",
        action="append",
        required=True,
        help="Stored paper ID. Repeat for multiple papers.",
    )
    fetch_sources_parser.set_defaults(func=cmd_fetch_sources)

    plan_triage_parser = subparsers.add_parser("plan-triage")
    plan_triage_parser.add_argument("--candidate-path", required=True, help="Candidate JSON path")
    plan_triage_parser.set_defaults(func=cmd_plan_triage)

    promote_triage_parser = subparsers.add_parser("promote-triage")
    promote_triage_parser.add_argument("--triage-dir", default="data/triage", help="Directory of triage JSON records")
    promote_triage_parser.add_argument("--manifest", default="jobs/triage.jsonl", help="Triage job manifest path")
    promote_triage_parser.set_defaults(func=cmd_promote_triage)

    create_episode_parser = subparsers.add_parser("create-episode")
    create_episode_parser.add_argument("--episode-path", required=True, help="Episode dir")
    create_episode_parser.add_argument("--title", required=True, help="Episode title")
    create_episode_parser.add_argument("--episode-type", required=True, help="Episode type")
    create_episode_parser.add_argument(
        "--paper-id",
        action="append",
        required=True,
        help="Stored paper ID, e.g. arxiv-2604.01694. Repeat for multiple papers.",
    )
    create_episode_parser.add_argument("--episode-id", help="Optional explicit episode ID")
    create_episode_parser.set_defaults(func=cmd_create_episode)

    plan_episode_parser = subparsers.add_parser("plan-episode")
    plan_episode_parser.add_argument("--episode-path", required=True, help="Episode dir")
    plan_episode_parser.set_defaults(func=cmd_plan_episode)

    run_episode_parser = subparsers.add_parser("run-episode")
    run_episode_parser.add_argument("--episode-path", required=True, help="Episode dir")
    run_episode_parser.add_argument(
        "--agent", required=True, choices=("codex", "claude"), help="Headless agent backend"
    )
    run_episode_parser.add_argument("--dry-run", action="store_true", help="Print ordered jobs without executing them")
    run_episode_parser.set_defaults(func=cmd_run_episode)

    daily_run_parser = subparsers.add_parser("daily-run")
    daily_run_parser.add_argument("--run-date", help="Run date, defaults to today")
    daily_run_parser.add_argument(
        "--category",
        action="append",
        help="arXiv category, e.g. cs.LG. Repeat for multiple categories.",
    )
    daily_run_parser.add_argument(
        "--max-results",
        type=int,
        default=DEFAULT_DAILY_MAX_RESULTS,
        help="Maximum arXiv results to fetch",
    )
    daily_run_parser.add_argument("--episode-slug", default=DEFAULT_EPISODE_SLUG, help="Episode directory slug")
    daily_run_parser.add_argument(
        "--title",
        default=None,
        help=f"Episode title, defaults to '{default_daily_title('YYYY-MM-DD')}'",
    )
    daily_run_parser.add_argument("--episode-type", default=DEFAULT_EPISODE_TYPE, help="Episode type")
    daily_run_parser.add_argument("--agent", required=True, choices=("codex", "claude"), help="Headless agent backend")
    daily_run_parser.add_argument(
        "--fresh",
        action="store_true",
        help="Delete run-date candidates, episode folder, and candidate-derived artifacts before running",
    )
    daily_run_parser.set_defaults(func=cmd_daily_run)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except RuntimeError as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
