from collections.abc import Mapping
from pathlib import Path
from typing import Any

HANDOFF_FILENAME = "HANDOFF.md"
NOTEBOOKLM_FORMAT = "Deep Dive"
NOTEBOOKLM_LENGTH = "Long"


def handoff_path_for_bundle(bundle_output_path: Path) -> Path:
    return bundle_output_path.parent / HANDOFF_FILENAME


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


def _string_items(value: object) -> list[str]:
    if not isinstance(value, list | tuple):
        return []
    return [str(item) for item in value if str(item)]


def _recommended_upload_sources(value: object) -> list[Mapping[str, Any]]:
    if not isinstance(value, list | tuple):
        return []
    sources: list[Mapping[str, Any]] = []
    for item in value:
        if isinstance(item, Mapping):
            sources.append(item)
    return sources[:2]


def render_notebooklm_handoff(job: Mapping[str, object], output: Mapping[str, Any]) -> str:
    bundle_output_path = str(job["bundle_output_path"])
    output_path = str(job["output_path"])
    paper_ids = _string_items(job.get("paper_ids", []))
    review_paths = _string_items(job.get("review_paths", []))
    citations = _string_items(output.get("citations", []))
    recommended_upload_sources = _recommended_upload_sources(output.get("recommended_upload_sources", []))
    provenance_paths = [output_path, *review_paths, *citations]
    deduped_provenance_paths = list(dict.fromkeys(provenance_paths))
    provenance_lines = "\n".join(f"- `{source}`" for source in deduped_provenance_paths)
    paper_lines = "\n".join(f"- `{paper_id}`" for paper_id in paper_ids)
    focus_paper_lines = "\n".join(
        f"- `{paper_id}`: `data/papers/pdfs/{paper_id}.pdf` or `data/papers/{paper_id}.md`" for paper_id in paper_ids
    )
    if recommended_upload_sources:
        recommended_upload_lines = "\n".join(
            f"- `{source.get('source_path', '')}` ({source.get('paper_id', '')}, {source.get('source_type', '')}): "
            f"{source.get('rationale', '')}"
            for source in recommended_upload_sources
        )
    else:
        recommended_upload_lines = "- No original paper sources recommended for this episode."
    upload_files = ["- `" + bundle_output_path + "`"]
    upload_files.extend(f"- `{source.get('source_path', '')}`" for source in recommended_upload_sources)
    upload_file_lines = "\n".join(upload_files)
    return f"""# NotebookLM Handoff

## NotebookLM Settings

- Format: {NOTEBOOKLM_FORMAT}
- Length: {NOTEBOOKLM_LENGTH}
- Do not choose Debate.

## Episode

- Episode ID: {job["episode_id"]}
- Title: {job["title"]}
- Episode type: {job.get("episode_type", "unknown")}

## Papers

{paper_lines}

## Recommended NotebookLM Upload Set

Upload exactly these files for the normal production run:

{upload_file_lines}

Keep `research_dossier.md` as the controlling source even when anchor papers are added.

## LLM Upload Decision

The source-dossier job chose these original paper sources:

{recommended_upload_lines}

## Optional Focus Papers

- The source-dossier job may recommend at most two original paper sources.
- Add only the recommended files from the upload set above.
- Prefer the PDF when NotebookLM imports it cleanly; use the paper markdown if the PDF import is slow, noisy, or fails.

Candidate original paper sources:

{focus_paper_lines}

## Local Provenance

Do not upload these provenance files by default. Use them to audit or debug the generated dossier.
Raw review JSONs contain detailed critique fields and citation pointers, but they are machine-oriented local
provenance. Important review details should be synthesized into `research_dossier.md`, not uploaded as raw JSON.

{provenance_lines}

## Custom Prompt

```text
Use the uploaded research dossier as the controlling factual source material for a NotebookLM Deep Dive.
Keep the tone analytical and concrete.
Preserve critique, uncertainty, and paper-to-paper comparisons.
Discuss both research quality and podcast value.
If one or two original paper sources are also uploaded, use them only to sharpen details about those anchor papers.
Do not invent paper details beyond the source dossier.
Do not turn the notes into a debate format.
Do not add stage directions, host banter, or scripted dialogue from outside the source material.
```

## Operator Checklist

- Upload exactly the files listed in Recommended NotebookLM Upload Set.
- Choose {NOTEBOOKLM_FORMAT}.
- Choose {NOTEBOOKLM_LENGTH}.
- Paste the custom prompt above.
- Confirm NotebookLM is generating conversation from source material, not from a performed script.
"""


def validate_notebooklm_handoff(root: Path, job: Mapping[str, object]) -> None:
    bundle_output_path = _resolve_project_path(root, job["bundle_output_path"])
    handoff_path = handoff_path_for_bundle(bundle_output_path)
    if not handoff_path.exists():
        raise RuntimeError(f"{_relative(handoff_path, root)} is missing")
    handoff = handoff_path.read_text(encoding="utf-8")
    required_snippets = (
        NOTEBOOKLM_FORMAT,
        NOTEBOOKLM_LENGTH,
        "Do not choose Debate",
        "research_dossier.md",
        "Recommended NotebookLM Upload Set",
        "LLM Upload Decision",
        "Optional Focus Papers",
        "may recommend at most two original paper sources",
        "Local Provenance",
        "Do not upload these provenance files by default",
        "not uploaded as raw JSON",
        "Custom Prompt",
        "Operator Checklist",
    )
    missing = [snippet for snippet in required_snippets if snippet not in handoff]
    for review_path in _string_items(job.get("review_paths", [])):
        if review_path not in handoff:
            missing.append(review_path)
    if missing:
        raise RuntimeError(f"{_relative(handoff_path, root)} is incomplete: {', '.join(missing)}")
