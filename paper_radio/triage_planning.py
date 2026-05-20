from dataclasses import dataclass
from pathlib import Path
from typing import Any

from paper_radio.io import read_json, upsert_jsonl_by_key
from paper_radio.paths import project_relative, resolve_project_path


@dataclass(frozen=True)
class TriageJobPlan:
    job_ids: list[str]


def write_triage_job_manifest(root: Path, candidate_path: Path) -> TriageJobPlan:
    resolved_candidate_path = resolve_project_path(root, candidate_path)
    relative_candidate_path = project_relative(root, resolved_candidate_path)
    candidates = read_json(resolved_candidate_path)
    if not isinstance(candidates, list):
        raise ValueError(f"Expected candidate list in {resolved_candidate_path}")
    jobs: list[dict[str, Any]] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ValueError(f"Expected candidate object in {resolved_candidate_path}")
        jobs.append(
            {
                "job_id": f"triage-{candidate['paper_id']}",
                "kind": "triage",
                "paper_id": str(candidate["paper_id"]),
                "candidate": candidate,
                "input_paths": [relative_candidate_path],
                "output_path": f"data/triage/{candidate['paper_id']}.json",
                "schema_path": "schemas/triage-record.schema.json",
            }
        )
    upsert_jsonl_by_key(root / "jobs" / "triage.jsonl", jobs)
    return TriageJobPlan(job_ids=[str(job["job_id"]) for job in jobs])
