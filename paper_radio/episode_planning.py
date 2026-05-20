from dataclasses import dataclass
from pathlib import Path
from typing import Any

from paper_radio.io import read_json, upsert_jsonl_by_key
from paper_radio.memory.cards import ensure_memory_scaffold, memory_cards_dir
from paper_radio.papers import load_paper_record
from paper_radio.paths import project_relative
from paper_radio.source_fetch import validate_full_text_source


@dataclass(frozen=True)
class EpisodeJobPlan:
    review_job_ids: list[str]
    source_dossier_job_id: str
    promote_memory_job_id: str | None = None


def _relative_episode_path(root: Path, episode_path: str) -> str:
    return project_relative(root, Path(episode_path))


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


def _review_job(root: Path, paper_id: str, paper_paths: dict[str, str]) -> dict[str, Any]:
    paper = load_paper_record(root, paper_id)
    full_text_path = validate_full_text_source(root, paper)
    input_paths = [paper_paths[paper_id]] if paper_id in paper_paths else []
    input_paths.append(full_text_path)
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
        "memory_note_path": f"{episode_path}/memory_note.md",
    }


def _candidate_card_paths(root: Path) -> list[str]:
    cards_dir = memory_cards_dir(root)
    if not cards_dir.exists():
        return []
    return [path.relative_to(root).as_posix() for path in sorted(cards_dir.glob("*/*.md"))[:50]]


def _promote_memory_job(root: Path, manifest: dict[str, Any], episode_path: str) -> dict[str, Any]:
    episode_id = str(manifest["episode_id"])
    return {
        "job_id": f"{episode_id}-promote-memory",
        "kind": "promote_memory",
        "episode_id": episode_id,
        "title": str(manifest["title"]),
        "episode_type": str(manifest["episode_type"]),
        "paper_ids": _paper_ids(manifest),
        "episode_manifest_path": f"{episode_path}/manifest.json",
        "bundle_output_path": f"{episode_path}/notebooklm_bundle/research_dossier.md",
        "memory_note_path": f"{episode_path}/memory_note.md",
        "vocab_path": "data/memory/vocab.json",
        "cards_dir": "data/memory/cards",
        "candidate_card_paths": _candidate_card_paths(root),
        "input_paths": [
            f"{episode_path}/manifest.json",
            f"{episode_path}/script.json",
            f"{episode_path}/notebooklm_bundle/research_dossier.md",
            f"{episode_path}/memory_note.md",
            "data/memory/vocab.json",
        ],
        "output_path": f"{episode_path}/memory_update.json",
        "schema_path": "schemas/memory-update.schema.json",
    }


def write_episode_job_manifests(root: Path, episode_path: str) -> EpisodeJobPlan:
    ensure_memory_scaffold(root)
    relative_episode_path = _relative_episode_path(root, episode_path)
    manifest = read_json(_manifest_path(root, episode_path))
    if not isinstance(manifest, dict):
        raise ValueError(f"Expected episode manifest object at {_manifest_path(root, episode_path)}")
    paper_paths = _paper_paths(manifest)
    review_jobs = [_review_job(root, paper_id, paper_paths) for paper_id in _paper_ids(manifest)]
    source_dossier_job = _source_dossier_job(manifest, relative_episode_path)
    promote_memory_job = _promote_memory_job(root, manifest, relative_episode_path)

    upsert_jsonl_by_key(root / "jobs" / "reviews.jsonl", review_jobs)
    upsert_jsonl_by_key(root / "jobs" / "source-dossiers.jsonl", [source_dossier_job])
    upsert_jsonl_by_key(root / "jobs" / "memory-updates.jsonl", [promote_memory_job])

    return EpisodeJobPlan(
        review_job_ids=[str(job["job_id"]) for job in review_jobs],
        source_dossier_job_id=str(source_dossier_job["job_id"]),
        promote_memory_job_id=str(promote_memory_job["job_id"]),
    )
