import json
import re
from pathlib import Path
from typing import Any

from paper_radio.papers import load_paper_record, paper_markdown_path


def _resolve_episode_path(root: Path, episode_path: str) -> Path:
    path = Path(episode_path)
    if path.is_absolute():
        return path
    return root / path


def _relative_episode_path(root: Path, episode_path: str) -> str:
    path = Path(episode_path)
    if path.is_absolute():
        return path.relative_to(root).as_posix()
    return path.as_posix()


def _default_episode_id(episode_path: str) -> str:
    parts = Path(episode_path).parts
    if len(parts) >= 3 and parts[-3] == "episodes":
        date_part = parts[-2]
        slug_part = parts[-1]
    else:
        date_part = "episode"
        slug_part = Path(episode_path).name or "episode"
    normalized_slug = re.sub(r"[^a-zA-Z0-9]+", "-", slug_part).strip("-").lower()
    return f"episode-{date_part}-{normalized_slug}"


def create_episode_manifest(
    root: Path,
    episode_path: str,
    title: str,
    episode_type: str,
    paper_ids: list[str],
    episode_id: str | None = None,
) -> Path:
    manifest_path = _resolve_episode_path(root, episode_path) / "manifest.json"
    relative_episode_path = _relative_episode_path(root, episode_path)
    paper_records = [load_paper_record(root, paper_id) for paper_id in paper_ids]
    manifest: dict[str, Any] = {
        "episode_id": episode_id or _default_episode_id(relative_episode_path),
        "title": title,
        "episode_type": episode_type,
        "paper_ids": paper_ids,
        "paper_titles": {paper.paper_id: paper.title for paper in paper_records},
        "paper_paths": {
            paper.paper_id: paper_markdown_path(root, paper.paper_id).relative_to(root).as_posix()
            for paper in paper_records
        },
        "script_job_id": f"{episode_id or _default_episode_id(relative_episode_path)}-dossier",
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest_path
