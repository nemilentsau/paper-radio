import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from paper_radio.agent_jobs import find_job
from paper_radio.agent_runner import run_job
from paper_radio.arxiv import fetch_recent_candidates
from paper_radio.config import PROJECT_ROOT
from paper_radio.episode_manifest import create_episode_manifest
from paper_radio.episode_planning import write_episode_job_manifests
from paper_radio.episode_runner import run_episode
from paper_radio.papers import load_paper_record
from paper_radio.source_fetch import SourceFetchError, fetch_paper_source, validate_full_text_source
from paper_radio.triage_planning import write_triage_job_manifest
from paper_radio.triage_promotion import promote_triage_results

DEFAULT_DAILY_CATEGORIES = ("cs.LG", "cs.CL", "cs.AI")
DEFAULT_DAILY_MAX_RESULTS = 10
DEFAULT_EPISODE_SLUG = "01_frontier_ml_roundup"
DEFAULT_EPISODE_TYPE = "frontier_ml_roundup"


@dataclass(frozen=True)
class DailyRunReport:
    run_date: str
    candidate_path: Path
    triage_job_ids: list[str]
    triage_job_ids_run: list[str]
    promoted_paper_ids: list[str]
    skipped_paper_ids: list[str]
    unrecognized_paper_ids: list[str]
    fetched_source_paper_ids: list[str]
    episode_path: Path
    review_job_ids: list[str]
    source_dossier_job_id: str
    promote_memory_job_id: str | None
    episode_commands_run: int
    script_path: Path
    notebooklm_bundle_path: Path

    def to_dict(self) -> dict[str, object]:
        return {
            "run_date": self.run_date,
            "candidate_path": self.candidate_path.as_posix(),
            "triage_job_ids": self.triage_job_ids,
            "triage_job_ids_run": self.triage_job_ids_run,
            "promoted_paper_ids": self.promoted_paper_ids,
            "skipped_paper_ids": self.skipped_paper_ids,
            "unrecognized_paper_ids": self.unrecognized_paper_ids,
            "fetched_source_paper_ids": self.fetched_source_paper_ids,
            "episode_path": self.episode_path.as_posix(),
            "review_job_ids": self.review_job_ids,
            "source_dossier_job_id": self.source_dossier_job_id,
            "promote_memory_job_id": self.promote_memory_job_id,
            "episode_commands_run": self.episode_commands_run,
            "script_path": self.script_path.as_posix(),
            "notebooklm_bundle_path": self.notebooklm_bundle_path.as_posix(),
        }


def default_daily_title(run_date: str) -> str:
    return f"Frontier ML roundup for {run_date}"


def _resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def _remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def _candidate_json_path(root: Path, run_date: str) -> Path:
    return root / "data" / "candidates" / run_date / "arxiv.json"


def _candidate_paper_ids(candidate_path: Path) -> list[str]:
    candidates = json.loads(candidate_path.read_text(encoding="utf-8"))
    return [str(candidate["paper_id"]) for candidate in candidates]


def _remove_candidate_artifacts(root: Path, paper_ids: list[str]) -> None:
    for paper_id in paper_ids:
        for path in (
            root / "data" / "triage" / f"{paper_id}.json",
            root / "data" / "papers" / f"{paper_id}.json",
            root / "data" / "papers" / f"{paper_id}.md",
            root / "data" / "papers" / "pdfs" / f"{paper_id}.pdf",
            root / "data" / "papers" / "fulltext" / f"{paper_id}.txt",
            root / "data" / "reviews" / f"{paper_id}.json",
        ):
            _remove_path(path)


def _triage_output_exists(root: Path, job_id: str) -> bool:
    job = find_job(root / "jobs" / "triage.jsonl", job_id)
    return _resolve(root, Path(str(job["output_path"]))).exists()


def _ensure_candidate_batch(root: Path, run_date: str, categories: list[str], max_results: int, fresh: bool) -> Path:
    candidate_path = _candidate_json_path(root, run_date)
    if candidate_path.exists() and not fresh:
        return candidate_path
    return fetch_recent_candidates(root, categories=categories, max_results=max_results, run_date=run_date).json_path


def _ensure_sources(root: Path, paper_ids: list[str]) -> list[str]:
    fetched_paper_ids: list[str] = []
    for paper_id in paper_ids:
        paper = load_paper_record(root, paper_id)
        try:
            validate_full_text_source(root, paper)
        except (RuntimeError, SourceFetchError):
            fetch_paper_source(root, paper_id)
            fetched_paper_ids.append(paper_id)
    return fetched_paper_ids


def run_daily(
    root: Path = PROJECT_ROOT,
    run_date: str = "",
    categories: list[str] | None = None,
    max_results: int = DEFAULT_DAILY_MAX_RESULTS,
    episode_slug: str = DEFAULT_EPISODE_SLUG,
    title: str | None = None,
    episode_type: str = DEFAULT_EPISODE_TYPE,
    agent: str = "codex",
    fresh: bool = False,
) -> DailyRunReport:
    if not run_date:
        raise ValueError("run_date is required")
    selected_categories = list(categories or DEFAULT_DAILY_CATEGORIES)
    episode_path = Path("episodes") / run_date / episode_slug

    if fresh:
        _remove_path(root / "data" / "candidates" / run_date)
        _remove_path(root / episode_path)

    candidate_path = _ensure_candidate_batch(root, run_date, selected_categories, max_results, fresh)
    paper_ids = _candidate_paper_ids(candidate_path)
    if fresh:
        _remove_candidate_artifacts(root, paper_ids)

    triage_plan = write_triage_job_manifest(root, candidate_path)
    triage_job_ids_run: list[str] = []
    for job_id in triage_plan.job_ids:
        if _triage_output_exists(root, job_id):
            continue
        run_job(root / "jobs" / "triage.jsonl", job_id, agent, root=root)
        triage_job_ids_run.append(job_id)

    promotion = promote_triage_results(root, paper_ids=paper_ids)
    if not promotion.promoted_paper_ids:
        raise RuntimeError(f"No papers were promoted for daily run {run_date}")

    fetched_source_paper_ids = _ensure_sources(root, promotion.promoted_paper_ids)
    create_episode_manifest(
        root=root,
        episode_path=episode_path.as_posix(),
        title=title or default_daily_title(run_date),
        episode_type=episode_type,
        paper_ids=promotion.promoted_paper_ids,
    )
    episode_plan = write_episode_job_manifests(root, episode_path.as_posix())
    episode_commands = run_episode(episode_path.as_posix(), agent, root=root)

    return DailyRunReport(
        run_date=run_date,
        candidate_path=candidate_path,
        triage_job_ids=triage_plan.job_ids,
        triage_job_ids_run=triage_job_ids_run,
        promoted_paper_ids=promotion.promoted_paper_ids,
        skipped_paper_ids=promotion.skipped_paper_ids,
        unrecognized_paper_ids=promotion.unrecognized_paper_ids,
        fetched_source_paper_ids=fetched_source_paper_ids,
        episode_path=episode_path,
        review_job_ids=episode_plan.review_job_ids,
        source_dossier_job_id=episode_plan.source_dossier_job_id,
        promote_memory_job_id=episode_plan.promote_memory_job_id,
        episode_commands_run=len(episode_commands),
        script_path=episode_path / "script.json",
        notebooklm_bundle_path=episode_path / "notebooklm_bundle" / "research_dossier.md",
    )
