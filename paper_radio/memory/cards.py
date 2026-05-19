import json
import re
from collections.abc import Mapping
from datetime import date
from pathlib import Path
from typing import Any

ALLOWED_CARD_TYPES = frozenset(("topic", "benchmark", "red-flag", "lab", "domain", "method"))
MEMORY_UPDATE_FIELDS = {"episode_id", "updates", "proposed_new_tags", "no_update_reason", "citations"}
MEMORY_UPDATE_ITEM_FIELDS = {
    "action",
    "card_path",
    "card_type",
    "tags",
    "aliases",
    "evidence",
    "updated_at",
    "body_markdown",
    "changelog_entry",
}
PROPOSED_TAG_FIELDS = {"tag", "aliases", "rationale"}
MIN_NO_UPDATE_REASON_CHARS = 24
MIN_CARD_BODY_WORDS = 75
MAX_CARD_BODY_WORDS = 900


class MemoryValidationError(RuntimeError):
    pass


def memory_vocab_path(root: Path) -> Path:
    return root / "data" / "memory" / "vocab.json"


def memory_cards_dir(root: Path) -> Path:
    return root / "data" / "memory" / "cards"


def ensure_memory_scaffold(root: Path) -> None:
    memory_cards_dir(root).mkdir(parents=True, exist_ok=True)
    vocab_path = memory_vocab_path(root)
    if not vocab_path.exists():
        vocab_path.parent.mkdir(parents=True, exist_ok=True)
        vocab_path.write_text(json.dumps({"tags": {}}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slugify_tag(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "untagged"


def _resolve_project_path(root: Path, path: object) -> Path:
    candidate = Path(str(path))
    if candidate.is_absolute():
        return candidate
    return root / candidate


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list | tuple):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_vocab(root: Path) -> dict[str, Any]:
    ensure_memory_scaffold(root)
    data = _read_json(memory_vocab_path(root))
    if not isinstance(data.get("tags"), dict):
        data["tags"] = {}
    return data


def _write_vocab(root: Path, vocab: Mapping[str, Any]) -> None:
    path = memory_vocab_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(vocab, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def _frontmatter_value(value: object) -> str:
    if isinstance(value, list | tuple):
        return json.dumps([str(item) for item in value], ensure_ascii=False)
    return str(value)


def _parse_inline_list(value: str) -> list[str]:
    text = value.strip()
    if not text.startswith("[") or not text.endswith("]"):
        return [text.strip("'\"")] if text else []
    inner = text[1:-1].strip()
    if not inner:
        return []
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return [part.strip().strip("'\"") for part in inner.split(",") if part.strip()]
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    return []


def parse_card_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    try:
        frontmatter = text.split("---\n", 2)[1]
    except IndexError:
        return {}
    parsed: dict[str, Any] = {}
    for raw_line in frontmatter.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        value = raw_value.strip()
        if value.startswith("["):
            parsed[key.strip()] = _parse_inline_list(value)
        else:
            parsed[key.strip()] = value.strip("'\"")
    return parsed


def _existing_changelog(text: str) -> list[str]:
    marker = "## Changelog"
    if marker not in text:
        return []
    changelog = text.split(marker, 1)[1]
    return [line.rstrip() for line in changelog.splitlines() if line.strip()]


def _render_card(update: Mapping[str, Any], existing_text: str | None = None) -> str:
    evidence = _string_list(update.get("evidence"))
    if existing_text:
        existing_frontmatter = parse_card_frontmatter(existing_text)
        evidence = list(dict.fromkeys([*_string_list(existing_frontmatter.get("evidence")), *evidence]))
    body = str(update["body_markdown"]).strip()
    changelog_lines: list[str] = []
    if existing_text:
        changelog_lines.extend(_existing_changelog(existing_text))
    changelog_entry = str(update["changelog_entry"]).strip()
    if changelog_entry and changelog_entry not in changelog_lines:
        changelog_lines.append(changelog_entry)
    changelog = "\n".join(changelog_lines)
    frontmatter = {
        "id": Path(str(update["card_path"])).stem,
        "type": str(update["card_type"]),
        "tags": [slugify_tag(tag) for tag in _string_list(update.get("tags"))],
        "aliases": _string_list(update.get("aliases")),
        "evidence": evidence,
        "updated_at": str(update["updated_at"]),
    }
    frontmatter_text = "\n".join(f"{key}: {_frontmatter_value(value)}" for key, value in frontmatter.items())
    return f"---\n{frontmatter_text}\n---\n\n{body}\n\n## Changelog\n{changelog}\n"


def _validate_update_shape(update: object, index: int) -> list[str]:
    errors: list[str] = []
    label = f"updates[{index}]"
    if not isinstance(update, Mapping):
        return [f"{label} must be an object"]
    missing = MEMORY_UPDATE_ITEM_FIELDS - set(update)
    extra = set(update) - MEMORY_UPDATE_ITEM_FIELDS
    if missing:
        errors.append(f"{label} is missing fields: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{label} has unexpected fields: {', '.join(sorted(extra))}")
    return errors


def _validate_proposed_tags(value: object) -> tuple[list[str], dict[str, set[str]]]:
    errors: list[str] = []
    proposed: dict[str, set[str]] = {}
    if not isinstance(value, list | tuple):
        return ["proposed_new_tags must be a list"], proposed
    for index, item in enumerate(value):
        label = f"proposed_new_tags[{index}]"
        if not isinstance(item, Mapping):
            errors.append(f"{label} must be an object")
            continue
        missing = PROPOSED_TAG_FIELDS - set(item)
        extra = set(item) - PROPOSED_TAG_FIELDS
        if missing:
            errors.append(f"{label} is missing fields: {', '.join(sorted(missing))}")
        if extra:
            errors.append(f"{label} has unexpected fields: {', '.join(sorted(extra))}")
        tag = slugify_tag(str(item.get("tag", "")))
        aliases = {alias for alias in _string_list(item.get("aliases"))}
        rationale = str(item.get("rationale", "")).strip()
        if not tag:
            errors.append(f"{label} tag is empty")
        if len(rationale) < MIN_NO_UPDATE_REASON_CHARS:
            errors.append(f"{label} rationale is too short")
        proposed[tag] = aliases
    return errors, proposed


def validate_memory_update_record(job: Mapping[str, object], output: Mapping[str, Any], root: Path) -> None:
    errors: list[str] = []
    missing = MEMORY_UPDATE_FIELDS - set(output)
    extra = set(output) - MEMORY_UPDATE_FIELDS
    if missing:
        errors.append(f"memory update output is missing fields: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"memory update output has unexpected fields: {', '.join(sorted(extra))}")
    expected_episode_id = str(job.get("episode_id", ""))
    if output.get("episode_id") != expected_episode_id:
        errors.append(
            f"memory update output has episode_id {output.get('episode_id')!r}, expected {expected_episode_id!r}"
        )
    tag_errors, proposed_tags = _validate_proposed_tags(output.get("proposed_new_tags", []))
    errors.extend(tag_errors)
    vocab = load_vocab(root)
    existing_tags = {slugify_tag(tag) for tag in vocab.get("tags", {})}
    allowed_tags = existing_tags | set(proposed_tags)
    citations = _string_list(output.get("citations"))
    for required_path in (job.get("memory_note_path"), job.get("bundle_output_path")):
        if required_path and str(required_path) not in citations:
            errors.append(f"memory update output does not cite {required_path}")
    updates = output.get("updates")
    if not isinstance(updates, list):
        errors.append("memory update output updates must be a list")
        updates = []
    elif len(updates) > 3:
        errors.append("memory update output may propose at most three card updates")
    if not updates and len(str(output.get("no_update_reason", "")).strip()) < MIN_NO_UPDATE_REASON_CHARS:
        errors.append("memory update output needs a substantive no_update_reason when there are no updates")
    for index, update in enumerate(updates):
        errors.extend(_validate_update_shape(update, index))
        if not isinstance(update, Mapping):
            continue
        label = f"updates[{index}]"
        action = update.get("action")
        if action not in ("create", "update"):
            errors.append(f"{label} action must be create or update")
        card_type = str(update.get("card_type", ""))
        if card_type not in ALLOWED_CARD_TYPES:
            errors.append(f"{label} card_type {card_type!r} is not allowed")
        card_path = str(update.get("card_path", ""))
        expected_prefix = f"data/memory/cards/{card_type}/"
        if not card_path.startswith(expected_prefix) or not card_path.endswith(".md"):
            errors.append(f"{label} card_path must live under {expected_prefix} and end in .md")
        resolved_card_path = _resolve_project_path(root, card_path)
        resolved_root = root.resolve()
        resolved_card = resolved_card_path.resolve()
        if resolved_card != resolved_root and resolved_root not in resolved_card.parents:
            errors.append(f"{label} card_path escapes the project: {card_path}")
        if action == "update" and not resolved_card_path.exists():
            errors.append(f"{label} update action targets a missing card: {card_path}")
        tags = [slugify_tag(tag) for tag in _string_list(update.get("tags"))]
        if not tags:
            errors.append(f"{label} tags must not be empty")
        unknown_tags = sorted(set(tags) - allowed_tags)
        if unknown_tags:
            errors.append(f"{label} tags are not in vocab or proposed_new_tags: {', '.join(unknown_tags)}")
        evidence = _string_list(update.get("evidence"))
        if expected_episode_id not in evidence:
            errors.append(f"{label} evidence must include {expected_episode_id}")
        try:
            date.fromisoformat(str(update.get("updated_at", "")))
        except ValueError:
            errors.append(f"{label} updated_at must be an ISO date")
        body = str(update.get("body_markdown", "")).strip()
        word_count = len(re.findall(r"\b\w+\b", body))
        if not MIN_CARD_BODY_WORDS <= word_count <= MAX_CARD_BODY_WORDS:
            errors.append(f"{label} body_markdown should be roughly {MIN_CARD_BODY_WORDS}-{MAX_CARD_BODY_WORDS} words")
        changelog_entry = str(update.get("changelog_entry", "")).strip()
        if expected_episode_id not in changelog_entry:
            errors.append(f"{label} changelog_entry must mention {expected_episode_id}")
    if errors:
        raise MemoryValidationError("Memory update output is not production-ready:\n- " + "\n- ".join(errors))


def apply_memory_update_record(job: Mapping[str, object], output: Mapping[str, Any], root: Path) -> list[Path]:
    validate_memory_update_record(job, output, root)
    ensure_memory_scaffold(root)
    vocab = load_vocab(root)
    tags = vocab.setdefault("tags", {})
    for proposed in output.get("proposed_new_tags", []):
        tag = slugify_tag(str(proposed["tag"]))
        existing = tags.setdefault(tag, {"aliases": []})
        aliases = list(dict.fromkeys([*existing.get("aliases", []), *_string_list(proposed.get("aliases"))]))
        existing["aliases"] = aliases
        existing["rationale"] = str(proposed.get("rationale", ""))
    _write_vocab(root, vocab)

    written: list[Path] = []
    for update in output.get("updates", []):
        card_path = _resolve_project_path(root, update["card_path"])
        existing_text = card_path.read_text(encoding="utf-8") if card_path.exists() else None
        card_text = _render_card(update, existing_text=existing_text)
        card_path.parent.mkdir(parents=True, exist_ok=True)
        card_path.write_text(card_text, encoding="utf-8")
        written.append(card_path)
    return written


def apply_memory_update_file(root: Path, job: Mapping[str, object]) -> list[Path]:
    output_path = _resolve_project_path(root, job["output_path"])
    output = _read_json(output_path)
    if not isinstance(output, Mapping):
        raise MemoryValidationError("Memory update output is not production-ready:\n- output must be an object")
    return apply_memory_update_record(job, output, root)
