import json
from pathlib import Path

from paper_radio.paths import resolve_project_path


def prompt_text(value: object) -> str:
    return str(value).replace("\x00", "")


def embedded_file(path_label: object, root: Path | None) -> str:
    label = prompt_text(path_label)
    if root is None:
        resolved = Path(label)
    else:
        resolved = resolve_project_path(root, path_label)
    if not resolved.exists():
        return f"### {label}\n\nMISSING: {label}"
    return f"### {label}\n\n{resolved.read_text(encoding='utf-8')}"


def embedded_review_inputs(job: dict[str, object], root: Path | None) -> str:
    blocks: list[str] = []
    review_paths = job.get("review_paths", [])
    if not isinstance(review_paths, list | tuple):
        return ""
    for review_path in review_paths:
        label = prompt_text(review_path)
        if root is None:
            resolved = Path(label)
        else:
            resolved = resolve_project_path(root, review_path)
        if not resolved.exists():
            blocks.append(f"### {label}\n\nMISSING: {label}")
            continue
        review_text = resolved.read_text(encoding="utf-8")
        try:
            review_record = json.loads(review_text)
        except json.JSONDecodeError:
            rendered_review = review_text
        else:
            if isinstance(review_record, dict):
                review_record.pop("citations", None)
            rendered_review = json.dumps(review_record, indent=2, ensure_ascii=False)
        blocks.append(f"### {label}\n\n```json\n{rendered_review}\n```")
    return "\n\n".join(blocks)
