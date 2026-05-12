import argparse
import json
from pathlib import Path

from paper_radio.agent_jobs import write_agent_job_artifacts
from paper_radio.agent_runner import run_job
from paper_radio.config import PROJECT_ROOT
from paper_radio.episode_runner import run_episode


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


def cmd_run_episode(args: argparse.Namespace) -> None:
    result = run_episode(args.episode_path, args.agent, dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(result, indent=2))


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

    run_episode_parser = subparsers.add_parser("run-episode")
    run_episode_parser.add_argument("--episode-path", required=True, help="Episode dir")
    run_episode_parser.add_argument(
        "--agent", required=True, choices=("codex", "claude"), help="Headless agent backend"
    )
    run_episode_parser.add_argument("--dry-run", action="store_true", help="Print ordered jobs without executing them")
    run_episode_parser.set_defaults(func=cmd_run_episode)

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
