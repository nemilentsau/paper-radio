import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TriageJobPlan:
    job_ids: list[str]


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
    path.write_text(f"{text}\n" if text else "", encoding="utf-8")


def _project_relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix() if path.is_absolute() else path.as_posix()


def _upsert_jobs(path: Path, jobs: list[dict[str, Any]]) -> None:
    existing = _load_jsonl(path)
    replacements = {str(job["job_id"]): job for job in jobs}
    updated: list[dict[str, Any]] = []
    seen: set[str] = set()
    for job in existing:
        job_id = str(job.get("job_id", ""))
        if job_id in replacements:
            updated.append(replacements[job_id])
            seen.add(job_id)
        else:
            updated.append(job)
    for job in jobs:
        job_id = str(job["job_id"])
        if job_id not in seen:
            updated.append(job)
    _write_jsonl(path, updated)


def write_triage_job_manifest(root: Path, candidate_path: Path) -> TriageJobPlan:
    resolved_candidate_path = candidate_path if candidate_path.is_absolute() else root / candidate_path
    relative_candidate_path = _project_relative(root, resolved_candidate_path)
    candidates = json.loads(resolved_candidate_path.read_text(encoding="utf-8"))
    jobs = [
        {
            "job_id": f"triage-{candidate['paper_id']}",
            "kind": "triage",
            "paper_id": str(candidate["paper_id"]),
            "input_paths": [relative_candidate_path],
            "output_path": f"data/triage/{candidate['paper_id']}.json",
            "schema_path": "schemas/triage-record.schema.json",
        }
        for candidate in candidates
    ]
    _upsert_jobs(root / "jobs" / "triage.jsonl", jobs)
    return TriageJobPlan(job_ids=[str(job["job_id"]) for job in jobs])
