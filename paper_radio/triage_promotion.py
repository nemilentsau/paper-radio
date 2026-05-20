import json
import re
from collections.abc import Iterable
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from paper_radio.io import load_jsonl
from paper_radio.papers import PaperRecord, write_paper_record

SELECTED_TRIAGE_DECISIONS = frozenset(("advance_to_review", "queue_for_review"))


@dataclass(frozen=True)
class TriagePromotionResult:
    promoted_paper_ids: list[str]
    skipped_paper_ids: list[str]
    unrecognized_paper_ids: list[str]


def normalize_triage_decision(decision: object) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", str(decision).strip().lower()).strip("_")
    aliases = {
        "advance": "advance_to_review",
        "advance_to_review": "advance_to_review",
        "promote": "advance_to_review",
        "review": "advance_to_review",
        "selected": "advance_to_review",
        "queue": "queue_for_review",
        "queued": "queue_for_review",
        "queue_review": "queue_for_review",
        "queue_for_review": "queue_for_review",
        "skip": "skip",
        "reject": "skip",
        "rejected": "skip",
        "not_relevant": "skip",
    }
    return aliases.get(normalized, normalized or "unknown")


def _resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def _load_candidates_by_paper_id(manifest_path: Path) -> dict[str, dict[str, Any]]:
    candidates: dict[str, dict[str, Any]] = {}
    for job in load_jsonl(manifest_path):
        paper_id = str(job.get("paper_id", ""))
        candidate = job.get("candidate")
        if paper_id and isinstance(candidate, dict):
            candidates[paper_id] = candidate
    return candidates


def _optional_float(value: object) -> float | None:
    if value is None:
        return None
    if isinstance(value, int | float | str):
        return float(value)
    raise TypeError(f"Expected a numeric triage score, got {type(value).__name__}")


def _candidate_to_triaged_paper(candidate: dict[str, Any], triage_record: dict[str, Any], decision: str) -> PaperRecord:
    paper = PaperRecord.from_dict(candidate)
    return replace(
        paper,
        status="triaged",
        triage_decision=decision,
        triage_rationale=str(triage_record["triage_rationale"])
        if triage_record.get("triage_rationale") is not None
        else None,
        research_score_estimate=_optional_float(triage_record.get("research_score_estimate")),
        podcast_score_estimate=_optional_float(triage_record.get("podcast_score_estimate")),
    )


def promote_triage_results(
    root: Path,
    triage_dir: Path = Path("data/triage"),
    manifest_path: Path = Path("jobs/triage.jsonl"),
    paper_ids: Iterable[str] | None = None,
) -> TriagePromotionResult:
    resolved_triage_dir = _resolve(root, triage_dir)
    resolved_manifest_path = _resolve(root, manifest_path)
    candidates_by_paper_id = _load_candidates_by_paper_id(resolved_manifest_path)
    allowed_paper_ids = set(paper_ids) if paper_ids is not None else None
    promoted_paper_ids: list[str] = []
    skipped_paper_ids: list[str] = []
    unrecognized_paper_ids: list[str] = []

    for triage_path in sorted(resolved_triage_dir.glob("*.json")):
        triage_record = json.loads(triage_path.read_text(encoding="utf-8"))
        paper_id = str(triage_record["paper_id"])
        if allowed_paper_ids is not None and paper_id not in allowed_paper_ids:
            continue
        decision = normalize_triage_decision(triage_record.get("decision", ""))

        if decision in SELECTED_TRIAGE_DECISIONS:
            candidate = candidates_by_paper_id.get(paper_id)
            if candidate is None:
                raise RuntimeError(f"No triage job candidate found for selected paper {paper_id}")
            write_paper_record(root, _candidate_to_triaged_paper(candidate, triage_record, decision))
            promoted_paper_ids.append(paper_id)
        elif decision == "skip":
            skipped_paper_ids.append(paper_id)
        else:
            unrecognized_paper_ids.append(paper_id)

    return TriagePromotionResult(
        promoted_paper_ids=promoted_paper_ids,
        skipped_paper_ids=skipped_paper_ids,
        unrecognized_paper_ids=unrecognized_paper_ids,
    )
