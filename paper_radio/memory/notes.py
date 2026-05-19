import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

MEMORY_NOTE_FILENAME = "memory_note.md"


def _resolve_project_path(root: Path, path: object) -> Path:
    candidate = Path(str(path))
    if candidate.is_absolute():
        return candidate
    return root / candidate


def memory_note_path_for_job(root: Path, job: Mapping[str, object]) -> Path:
    explicit_path = job.get("memory_note_path")
    if explicit_path:
        return _resolve_project_path(root, explicit_path)
    output_path = _resolve_project_path(root, job["output_path"])
    return output_path.parent / MEMORY_NOTE_FILENAME


def _string_items(value: object) -> list[str]:
    if not isinstance(value, list | tuple):
        return []
    return [str(item) for item in value if str(item)]


def _extract_section(markdown: str, heading: str) -> str:
    match = re.search(rf"^{re.escape(heading)}\s*$", markdown, flags=re.MULTILINE)
    if not match:
        return "_Not found in dossier._"
    start = match.end()
    next_heading = re.search(r"^##\s+", markdown[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(markdown)
    return markdown[start:end].strip() or "_Section was present but empty._"


def _load_review_summary(root: Path, path: str) -> str:
    resolved = _resolve_project_path(root, path)
    if not resolved.exists():
        return f"- `{path}`: missing review record"
    try:
        review = json.loads(resolved.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return f"- `{path}`: review record was not valid JSON"
    if not isinstance(review, dict):
        return f"- `{path}`: review record was not an object"
    paper_id = str(review.get("paper_id", resolved.stem))
    research_score = review.get("research_score", "n/a")
    podcast_score = review.get("podcast_score", "n/a")
    verdict = str(review.get("verdict", "")).strip()
    claim = str(review.get("one_line_claim", "")).strip()
    return (
        f"- `{paper_id}`: research {research_score}, podcast {podcast_score}. "
        f"Claim: {claim} Verdict: {verdict}"
    )


def render_memory_note(root: Path, job: Mapping[str, object], output: Mapping[str, Any]) -> str:
    dossier = str(output.get("research_dossier_markdown", "")).strip()
    raw_review_paths = job.get("review_paths", [])
    review_paths = list(raw_review_paths) if isinstance(raw_review_paths, list | tuple) else []
    paper_lines = "\n".join(f"- `{paper_id}`" for paper_id in _string_items(job.get("paper_ids", [])))
    review_lines = "\n".join(_load_review_summary(root, path) for path in _string_items(review_paths))
    provenance_lines = "\n".join(
        f"- `{path}`"
        for path in _string_items(
            [
                job.get("output_path", ""),
                job.get("bundle_output_path", ""),
                *review_paths,
            ]
        )
    )
    return f"""# Memory Note

## Episode

- Episode ID: {job["episode_id"]}
- Title: {job["title"]}
- Episode type: {job.get("episode_type", "unknown")}

## Papers

{paper_lines}

## Concise Thesis

{_extract_section(dossier, "## Concise Thesis")}

## Verdict For The Listener

{_extract_section(dossier, "## Verdict For The Listener")}

## Review Signals

{review_lines}

## Promotion Hints

- Promote only reusable topic, benchmark, method, lab/source, domain, or recurring-red-flag observations.
- Do not promote paper-specific trivia.
- Treat this note as archive evidence for memory curation, not as evidence about future papers.

## Local Provenance

{provenance_lines}
"""


def write_memory_note(root: Path, job: Mapping[str, object], output: Mapping[str, Any]) -> Path:
    path = memory_note_path_for_job(root, job)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_memory_note(root, job, output), encoding="utf-8")
    return path
