import json
import re
from collections.abc import Mapping
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from paper_radio.memory.cards import memory_cards_dir, parse_card_frontmatter, slugify_tag

MAX_MEMORY_CONTEXT_CHARS = 8000
RECENT_DOSSIER_LIMIT = 2
RECENT_DOSSIER_DAYS = 14


def _resolve_project_path(root: Path, path: object) -> Path:
    candidate = Path(str(path))
    if candidate.is_absolute():
        return candidate
    return root / candidate


def _safe_read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _normalize_terms(text: str) -> set[str]:
    words = {slugify_tag(word) for word in re.findall(r"[A-Za-z][A-Za-z0-9-]{2,}", text)}
    return {word for word in words if len(word) >= 3}


def _json_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return path.read_text(encoding="utf-8")
    return json.dumps(data, ensure_ascii=False)


def _object_list(value: object) -> list[object]:
    if not isinstance(value, list | tuple):
        return []
    return list(value)


def _query_terms(root: Path, job: Mapping[str, object]) -> set[str]:
    chunks: list[str] = []
    chunks.extend(str(item) for item in _object_list(job.get("paper_ids", [])) if str(item))
    chunks.append(str(job.get("title", "")))
    chunks.append(str(job.get("episode_type", "")))
    for review_path in _object_list(job.get("review_paths", [])):
        chunks.append(_json_text(_resolve_project_path(root, review_path)))
    return _normalize_terms(" ".join(chunks))


def _body_without_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return text.strip()


def _matching_cards(root: Path, terms: set[str]) -> list[tuple[dict[str, Any], Path, str]]:
    cards_root = memory_cards_dir(root)
    if not cards_root.exists():
        return []
    matches: list[tuple[dict[str, Any], Path, str]] = []
    for path in sorted(cards_root.glob("*/*.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter = parse_card_frontmatter(text)
        searchable = {slugify_tag(str(item)) for key in ("tags", "aliases") for item in frontmatter.get(key, [])}
        has_match = bool(terms & searchable)
        if not has_match:
            has_match = any(all(part in terms for part in token.split("-") if part) for token in searchable)
        if has_match:
            matches.append((frontmatter, path, _body_without_frontmatter(text)))
    matches.sort(key=lambda item: str(item[0].get("updated_at", "")), reverse=True)
    return matches[:5]


def _extract_section(markdown: str, heading: str, max_chars: int = 900) -> str:
    pattern = re.compile(rf"^{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", markdown[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(markdown)
    return markdown[start:end].strip()[:max_chars].strip()


def _episode_date_from_path(path: Path) -> date | None:
    parts = path.parts
    for part in parts:
        try:
            return date.fromisoformat(part)
        except ValueError:
            continue
    return None


def _current_episode_date(job: Mapping[str, object]) -> date | None:
    for key in ("bundle_output_path", "episode_manifest_path", "output_path"):
        value = job.get(key)
        if value:
            parsed = _episode_date_from_path(Path(str(value)))
            if parsed:
                return parsed
    return None


def _recent_dossiers(root: Path, job: Mapping[str, object]) -> list[str]:
    current_bundle = _resolve_project_path(root, job.get("bundle_output_path", ""))
    current_date = _current_episode_date(job)
    if current_date is None:
        current_date = date.today()
    earliest = current_date - timedelta(days=RECENT_DOSSIER_DAYS)
    blocks: list[tuple[date, str]] = []
    for path in sorted((root / "episodes").glob("*/*/notebooklm_bundle/research_dossier.md")):
        if path.resolve() == current_bundle.resolve():
            continue
        episode_date = _episode_date_from_path(path)
        if episode_date is None or episode_date < earliest or episode_date > current_date:
            continue
        markdown = _safe_read(path)
        thesis = _extract_section(markdown, "## Concise Thesis")
        verdict = _extract_section(markdown, "## Verdict For The Listener")
        if not thesis and not verdict:
            continue
        rel = path.relative_to(root).as_posix()
        blocks.append((episode_date, f"### {rel}\n\nConcise Thesis:\n{thesis}\n\nVerdict:\n{verdict}".strip()))
    blocks.sort(key=lambda item: item[0], reverse=True)
    return [block for _, block in blocks[:RECENT_DOSSIER_LIMIT]]


def build_memory_context(
    root: Path | None,
    job: Mapping[str, object],
    max_chars: int = MAX_MEMORY_CONTEXT_CHARS,
) -> str:
    if root is None:
        return "No project root was provided, so no prior memory was retrieved."
    terms = _query_terms(root, job)
    card_matches = _matching_cards(root, terms)
    lines: list[str] = [
        "Memory is framing guidance, not evidence. Current paper sources and review records remain controlling.",
        "",
        "## Durable Cards",
    ]
    if not card_matches:
        lines.append("No prior memory cards matched this episode's tags, aliases, title, or review text.")
    else:
        for frontmatter, path, body in card_matches:
            tags = ", ".join(str(tag) for tag in frontmatter.get("tags", []))
            updated_at = str(frontmatter.get("updated_at", "unknown"))
            relative_path = path.relative_to(root).as_posix()
            lines.append(f"### {relative_path} ({frontmatter.get('type', 'unknown')}; {updated_at}; tags: {tags})")
            lines.append(body[:1600].strip())
    lines.extend(["", "## Recent Working Memory"])
    recent_blocks = _recent_dossiers(root, job)
    if not recent_blocks:
        lines.append("No recent prior episode dossiers were found in the last 14 days.")
    else:
        lines.extend(recent_blocks)
    context = "\n\n".join(lines).strip()
    if len(context) > max_chars:
        return context[:max_chars].rsplit("\n", 1)[0].strip() + "\n\n[Memory context truncated to budget.]"
    return context
