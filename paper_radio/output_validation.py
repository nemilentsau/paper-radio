import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from paper_radio.memory.cards import MemoryValidationError, validate_memory_update_record
from paper_radio.notebooklm_handoff import validate_notebooklm_handoff

REVIEW_STRING_FIELDS = (
    "one_line_claim",
    "what_they_tested",
    "strongest_point",
    "weakest_point",
    "verdict",
)
REVIEW_LIST_FIELDS = (
    "missing_baselines",
    "missing_ablations",
    "red_flags",
    "positive_signals",
    "citations",
)
REVIEW_SCORE_FIELDS = (
    "research_score",
    "podcast_score",
    "overclaim_score",
    "replication_interest",
)
REVIEW_FIELDS = {"paper_id", *REVIEW_STRING_FIELDS, *REVIEW_LIST_FIELDS, *REVIEW_SCORE_FIELDS}

SOURCE_DOSSIER_SECTIONS = (
    "## Episode Metadata",
    "## Why These Papers Are Grouped",
    "## Concise Thesis",
    "## Per-Paper Claim Versus Evidence",
    "## Strongest Contributions",
    "## Serious Weaknesses And Red Flags",
    "## Missing Baselines And Ablations",
    "## Comparison Axes",
    "## Verdict For The Listener",
    "## Source Notes And Local Input Paths",
)
SOURCE_DOSSIER_FIELDS = {
    "episode_id",
    "title",
    "episode_type",
    "research_dossier_markdown",
    "recommended_upload_sources",
    "citations",
    "missing_inputs",
}
PLACEHOLDER_MARKERS = (
    "review incomplete",
    "research incomplete",
    "placeholder",
    "todo",
)
MIN_REVIEW_TEXT_CHARS = 24
MIN_REVIEW_LIST_ITEM_CHARS = 20
MIN_SOURCE_DOSSIER_CHARS = 1200
MIN_UPLOAD_RATIONALE_CHARS = 24


class OutputValidationError(RuntimeError):
    pass


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _is_placeholder(value: str) -> bool:
    folded = value.casefold()
    return any(marker in folded for marker in PLACEHOLDER_MARKERS)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_project_path(root: Path, path: object) -> Path:
    candidate = Path(str(path))
    if candidate.is_absolute():
        return candidate
    return root / candidate


def _job_items(job: Mapping[str, object], field: str) -> list[object]:
    value = job.get(field, [])
    if isinstance(value, list | tuple):
        return list(value)
    return []


def _string_errors(record: Mapping[str, Any], fields: Sequence[str], label: str) -> list[str]:
    errors: list[str] = []
    for field in fields:
        value = record.get(field)
        if not isinstance(value, str) or len(value.strip()) < MIN_REVIEW_TEXT_CHARS:
            errors.append(f"{label} has too-short field `{field}`")
            continue
        if _is_placeholder(value):
            errors.append(f"{label} has placeholder field `{field}`")
    return errors


def _list_errors(record: Mapping[str, Any], fields: Sequence[str], label: str) -> list[str]:
    errors: list[str] = []
    for field in fields:
        value = record.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"{label} has empty field `{field}`")
            continue
        for item in value:
            if not isinstance(item, str) or len(item.strip()) < MIN_REVIEW_LIST_ITEM_CHARS:
                errors.append(f"{label} has too-short item in `{field}`")
                break
            if _is_placeholder(item):
                errors.append(f"{label} has placeholder item in `{field}`")
                break
    return errors


def validate_review_record(record: Mapping[str, Any], expected_paper_id: str, label: str = "review output") -> None:
    errors: list[str] = []
    missing = REVIEW_FIELDS - set(record)
    extra = set(record) - REVIEW_FIELDS
    if missing:
        errors.append(f"{label} is missing fields: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{label} has unexpected fields: {', '.join(sorted(extra))}")
    if record.get("paper_id") != expected_paper_id:
        errors.append(f"{label} has paper_id {record.get('paper_id')!r}, expected {expected_paper_id!r}")
    errors.extend(_string_errors(record, REVIEW_STRING_FIELDS, label))
    errors.extend(_list_errors(record, REVIEW_LIST_FIELDS, label))
    for field in REVIEW_SCORE_FIELDS:
        value = record.get(field)
        if not isinstance(value, int | float) or not 0 <= value <= 10:
            errors.append(f"{label} has invalid 0-10 score `{field}`")
    if errors:
        raise OutputValidationError("Review output is not production-ready:\n- " + "\n- ".join(errors))


def validate_review_file(root: Path, paper_id: str) -> None:
    path = root / "data" / "reviews" / f"{paper_id}.json"
    label = _relative(path, root)
    if not path.exists():
        raise OutputValidationError(f"Review output is not production-ready:\n- {label} is missing")
    try:
        record = _read_json(path)
    except json.JSONDecodeError as error:
        raise OutputValidationError(
            f"Review output is not production-ready:\n- {label} is not valid JSON: {error}"
        ) from error
    validate_review_record(record, paper_id, label)


def validate_source_dossier_record(
    job: Mapping[str, object], output: Mapping[str, Any], root: Path | None = None
) -> None:
    project_root = root or Path.cwd()
    errors: list[str] = []
    missing = SOURCE_DOSSIER_FIELDS - set(output)
    extra = set(output) - SOURCE_DOSSIER_FIELDS
    if missing:
        errors.append(f"source dossier output is missing fields: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"source dossier output has unexpected fields: {', '.join(sorted(extra))}")
    for field in ("episode_id", "title", "episode_type"):
        expected = job.get(field)
        if expected is not None and output.get(field) != expected:
            errors.append(f"source dossier output has {field} {output.get(field)!r}, expected {expected!r}")
    missing_inputs = output.get("missing_inputs")
    if not isinstance(missing_inputs, list) or missing_inputs:
        errors.append("source dossier output must have missing_inputs == []")
    recommended_upload_sources = output.get("recommended_upload_sources")
    paper_ids = {str(paper_id) for paper_id in _job_items(job, "paper_ids")}
    if not isinstance(recommended_upload_sources, list):
        errors.append("source dossier output recommended_upload_sources must be a list")
    elif len(recommended_upload_sources) > 2:
        errors.append("source dossier output recommended_upload_sources must contain at most two sources")
    else:
        seen_upload_papers: set[str] = set()
        for index, source in enumerate(recommended_upload_sources):
            label = f"recommended_upload_sources[{index}]"
            if not isinstance(source, Mapping):
                errors.append(f"source dossier output {label} must be an object")
                continue
            allowed_fields = {"paper_id", "source_path", "source_type", "rationale"}
            missing_fields = allowed_fields - set(source)
            extra_fields = set(source) - allowed_fields
            if missing_fields:
                errors.append(f"source dossier output {label} is missing fields: {', '.join(sorted(missing_fields))}")
            if extra_fields:
                errors.append(f"source dossier output {label} has unexpected fields: {', '.join(sorted(extra_fields))}")
            paper_id = str(source.get("paper_id", ""))
            source_path = str(source.get("source_path", ""))
            source_type = source.get("source_type")
            rationale = source.get("rationale")
            if paper_id not in paper_ids:
                errors.append(f"source dossier output {label} has unknown paper_id {paper_id!r}")
            if paper_id in seen_upload_papers:
                errors.append(f"source dossier output {label} duplicates paper_id {paper_id!r}")
            seen_upload_papers.add(paper_id)
            expected_pdf_path = f"data/papers/pdfs/{paper_id}.pdf"
            expected_markdown_path = f"data/papers/{paper_id}.md"
            if source_type == "paper_pdf":
                expected_path = expected_pdf_path
            elif source_type == "paper_markdown":
                expected_path = expected_markdown_path
            else:
                expected_path = ""
                errors.append(f"source dossier output {label} has invalid source_type {source_type!r}")
            if expected_path and source_path != expected_path:
                errors.append(f"source dossier output {label} source_path must be {expected_path!r}")
            if expected_path and not _resolve_project_path(project_root, expected_path).exists():
                errors.append(f"source dossier output {label} source_path does not exist: {expected_path}")
            if not isinstance(rationale, str) or len(rationale.strip()) < MIN_UPLOAD_RATIONALE_CHARS:
                errors.append(f"source dossier output {label} rationale is too short")
            elif _is_placeholder(rationale):
                errors.append(f"source dossier output {label} rationale contains placeholder text")
    citations = output.get("citations")
    if not isinstance(citations, list) or not citations:
        errors.append("source dossier output must cite local review inputs")
    else:
        for review_path in _job_items(job, "review_paths"):
            if str(review_path) not in citations:
                errors.append(f"source dossier output does not cite {review_path}")
    dossier = output.get("research_dossier_markdown")
    if not isinstance(dossier, str) or len(dossier.strip()) < MIN_SOURCE_DOSSIER_CHARS:
        errors.append("source dossier output research_dossier_markdown is too short")
    elif _is_placeholder(dossier):
        errors.append("source dossier output research_dossier_markdown contains placeholder text")
    elif any(section not in dossier for section in SOURCE_DOSSIER_SECTIONS):
        errors.append("source dossier output is missing required NotebookLM dossier sections")
    if isinstance(dossier, str):
        for paper_id in _job_items(job, "paper_ids"):
            if str(paper_id) not in dossier:
                errors.append(f"source dossier output does not mention paper {paper_id}")
        folded_dossier = dossier.casefold()
        forbidden = ("speaker 1:", "speaker 2:", "\nhost:", "cold open:", "stage direction:")
        if folded_dossier.startswith("host:") or any(marker in folded_dossier for marker in forbidden):
            errors.append("source dossier output looks like narration or dialogue instead of source material")
    if errors:
        raise OutputValidationError("Source dossier output is not production-ready:\n- " + "\n- ".join(errors))


def validate_source_dossier_files(root: Path, job: Mapping[str, object]) -> None:
    output_path = _resolve_project_path(root, job["output_path"])
    bundle_output_path = _resolve_project_path(root, job["bundle_output_path"])
    if not output_path.exists():
        raise OutputValidationError(
            f"Source dossier output is not production-ready:\n- {_relative(output_path, root)} is missing"
        )
    if not bundle_output_path.exists():
        raise OutputValidationError(
            f"Source dossier output is not production-ready:\n- {_relative(bundle_output_path, root)} is missing"
        )
    try:
        output = _read_json(output_path)
    except json.JSONDecodeError as error:
        raise OutputValidationError(
            "Source dossier output is not production-ready:\n"
            f"- {_relative(output_path, root)} is not valid JSON: {error}"
        ) from error
    validate_source_dossier_record(job, output, root=root)
    dossier = output["research_dossier_markdown"]
    if bundle_output_path.read_text(encoding="utf-8") != dossier:
        raise OutputValidationError(
            "Source dossier output is not production-ready:\n"
            "- NotebookLM bundle does not match research_dossier_markdown"
        )
    try:
        validate_notebooklm_handoff(root, job)
    except RuntimeError as error:
        raise OutputValidationError(f"Source dossier output is not production-ready:\n- {error}") from error


def validate_job_output(root: Path, job: Mapping[str, object]) -> None:
    kind = str(job.get("kind", ""))
    if kind == "review":
        validate_review_file(root, str(job["paper_id"]))
    elif kind == "source_dossier":
        validate_source_dossier_files(root, job)
    elif kind == "promote_memory":
        output_path = _resolve_project_path(root, job["output_path"])
        if not output_path.exists():
            raise OutputValidationError(
                f"Memory update output is not production-ready:\n- {_relative(output_path, root)} is missing"
            )
        try:
            output = _read_json(output_path)
        except json.JSONDecodeError as error:
            raise OutputValidationError(
                "Memory update output is not production-ready:\n"
                f"- {_relative(output_path, root)} is not valid JSON: {error}"
            ) from error
        try:
            validate_memory_update_record(job, output, root=root)
        except MemoryValidationError as error:
            raise OutputValidationError(str(error)) from error
