import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EpisodeJobPlan:
    review_job_ids: list[str]
    source_dossier_job_id: str


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
    path.write_text(f"{text}\n" if text else "", encoding="utf-8")


def _upsert_jobs(path: Path, jobs: list[dict[str, Any]]) -> None:
    existing = _load_jsonl(path)
    replacements = {str(job["job_id"]): job for job in jobs}
    seen: set[str] = set()
    updated: list[dict[str, Any]] = []
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


def _relative_episode_path(root: Path, episode_path: str) -> str:
    path = Path(episode_path)
    if path.is_absolute():
        return path.relative_to(root).as_posix()
    return path.as_posix()


def _manifest_path(root: Path, episode_path: str) -> Path:
    path = Path(episode_path)
    if path.is_absolute():
        return path / "manifest.json"
    return root / path / "manifest.json"


def _paper_ids(manifest: dict[str, Any]) -> list[str]:
    return [str(paper_id) for paper_id in manifest["paper_ids"]]


def _paper_paths(manifest: dict[str, Any]) -> dict[str, str]:
    value = manifest.get("paper_paths", {})
    if not isinstance(value, dict):
        return {}
    return {str(key): str(path) for key, path in value.items()}


def _review_job(paper_id: str, paper_paths: dict[str, str]) -> dict[str, Any]:
    input_paths = [paper_paths[paper_id]] if paper_id in paper_paths else []
    return {
        "job_id": f"review-{paper_id}",
        "kind": "review",
        "paper_id": paper_id,
        "input_paths": input_paths,
        "output_path": f"data/reviews/{paper_id}.json",
        "schema_path": "schemas/review-record.schema.json",
    }


def _source_dossier_job(manifest: dict[str, Any], episode_path: str) -> dict[str, Any]:
    paper_ids = _paper_ids(manifest)
    review_paths = [f"data/reviews/{paper_id}.json" for paper_id in paper_ids]
    episode_id = str(manifest["episode_id"])
    source_job_id = str(manifest.get("script_job_id", f"{episode_id}-dossier"))
    return {
        "job_id": source_job_id,
        "kind": "source_dossier",
        "episode_id": episode_id,
        "title": str(manifest["title"]),
        "episode_type": str(manifest["episode_type"]),
        "paper_ids": paper_ids,
        "review_paths": review_paths,
        "input_paths": [f"{episode_path}/manifest.json", *review_paths],
        "episode_manifest_path": f"{episode_path}/manifest.json",
        "output_path": f"{episode_path}/script.json",
        "schema_path": "schemas/source-dossier.schema.json",
        "notebooklm_bundle_dir": f"{episode_path}/notebooklm_bundle",
        "bundle_output_path": f"{episode_path}/notebooklm_bundle/research_dossier.md",
    }


def write_episode_job_manifests(root: Path, episode_path: str) -> EpisodeJobPlan:
    relative_episode_path = _relative_episode_path(root, episode_path)
    manifest = _read_json(_manifest_path(root, episode_path))
    paper_paths = _paper_paths(manifest)
    review_jobs = [_review_job(paper_id, paper_paths) for paper_id in _paper_ids(manifest)]
    source_dossier_job = _source_dossier_job(manifest, relative_episode_path)

    _upsert_jobs(root / "jobs" / "reviews.jsonl", review_jobs)
    _upsert_jobs(root / "jobs" / "source-dossiers.jsonl", [source_dossier_job])

    return EpisodeJobPlan(
        review_job_ids=[str(job["job_id"]) for job in review_jobs],
        source_dossier_job_id=str(source_dossier_job["job_id"]),
    )
