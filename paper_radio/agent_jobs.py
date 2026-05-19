import json
from pathlib import Path
from typing import Any

from paper_radio.memory.cards import ALLOWED_CARD_TYPES
from paper_radio.memory.context import build_memory_context

TRIAGE_RECORD_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "paper_id": {"type": "string"},
        "title": {"type": "string"},
        "core_claim": {"type": "string"},
        "triage_rationale": {"type": "string"},
        "topic_tags": {"type": "array", "items": {"type": "string"}},
        "likely_red_flags": {"type": "array", "items": {"type": "string"}},
        "research_score_estimate": {"type": "number"},
        "podcast_score_estimate": {"type": "number"},
        "decision": {"type": "string", "enum": ["advance_to_review", "queue_for_review", "skip"]},
    },
    "required": [
        "paper_id",
        "title",
        "core_claim",
        "triage_rationale",
        "topic_tags",
        "likely_red_flags",
        "research_score_estimate",
        "podcast_score_estimate",
        "decision",
    ],
    "additionalProperties": False,
}

REVIEW_RECORD_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "paper_id": {"type": "string"},
        "one_line_claim": {"type": "string"},
        "what_they_tested": {"type": "string"},
        "strongest_point": {"type": "string"},
        "weakest_point": {"type": "string"},
        "missing_baselines": {"type": "array", "items": {"type": "string"}},
        "missing_ablations": {"type": "array", "items": {"type": "string"}},
        "red_flags": {"type": "array", "items": {"type": "string"}},
        "positive_signals": {"type": "array", "items": {"type": "string"}},
        "research_score": {"type": "number"},
        "podcast_score": {"type": "number"},
        "overclaim_score": {"type": "number"},
        "replication_interest": {"type": "number"},
        "verdict": {"type": "string"},
        "citations": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "paper_id",
        "one_line_claim",
        "what_they_tested",
        "strongest_point",
        "weakest_point",
        "missing_baselines",
        "missing_ablations",
        "red_flags",
        "positive_signals",
        "research_score",
        "podcast_score",
        "overclaim_score",
        "replication_interest",
        "verdict",
        "citations",
    ],
    "additionalProperties": False,
}

SOURCE_DOSSIER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "episode_id": {"type": "string"},
        "title": {"type": "string"},
        "episode_type": {"type": "string"},
        "research_dossier_markdown": {"type": "string"},
        "recommended_upload_sources": {
            "type": "array",
            "maxItems": 2,
            "items": {
                "type": "object",
                "properties": {
                    "paper_id": {"type": "string"},
                    "source_path": {"type": "string"},
                    "source_type": {"type": "string", "enum": ["paper_pdf", "paper_markdown"]},
                    "rationale": {"type": "string"},
                },
                "required": ["paper_id", "source_path", "source_type", "rationale"],
                "additionalProperties": False,
            },
        },
        "citations": {"type": "array", "items": {"type": "string"}},
        "missing_inputs": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "episode_id",
        "title",
        "episode_type",
        "research_dossier_markdown",
        "recommended_upload_sources",
        "citations",
        "missing_inputs",
    ],
    "additionalProperties": False,
}

MEMORY_UPDATE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "episode_id": {"type": "string"},
        "updates": {
            "type": "array",
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["create", "update"]},
                    "card_path": {"type": "string"},
                    "card_type": {"type": "string", "enum": sorted(ALLOWED_CARD_TYPES)},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "aliases": {"type": "array", "items": {"type": "string"}},
                    "evidence": {"type": "array", "items": {"type": "string"}},
                    "updated_at": {"type": "string"},
                    "body_markdown": {"type": "string"},
                    "changelog_entry": {"type": "string"},
                },
                "required": [
                    "action",
                    "card_path",
                    "card_type",
                    "tags",
                    "aliases",
                    "evidence",
                    "updated_at",
                    "body_markdown",
                    "changelog_entry",
                ],
                "additionalProperties": False,
            },
        },
        "proposed_new_tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "tag": {"type": "string"},
                    "aliases": {"type": "array", "items": {"type": "string"}},
                    "rationale": {"type": "string"},
                },
                "required": ["tag", "aliases", "rationale"],
                "additionalProperties": False,
            },
        },
        "no_update_reason": {"type": "string"},
        "citations": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["episode_id", "updates", "proposed_new_tags", "no_update_reason", "citations"],
    "additionalProperties": False,
}

JOBS_README = """# Paper Radio Jobs

This directory holds JSONL job manifests for headless Codex or Claude Code runs.

- `triage.jsonl`: fast paper triage jobs
- `reviews.jsonl`: full paper review jobs
- `source-dossiers.jsonl`: episode-level NotebookLM source dossier jobs
- `memory-updates.jsonl`: post-dossier durable memory promotion jobs

Use `scripts/run_episode` for production episode runs so review readiness is checked before a source dossier is created.
"""


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_agent_job_artifacts(root: Path) -> None:
    schemas_dir = root / "schemas"
    jobs_dir = root / "jobs"
    _write_json(schemas_dir / "triage-record.schema.json", TRIAGE_RECORD_SCHEMA)
    _write_json(schemas_dir / "review-record.schema.json", REVIEW_RECORD_SCHEMA)
    _write_json(schemas_dir / "source-dossier.schema.json", SOURCE_DOSSIER_SCHEMA)
    _write_json(schemas_dir / "memory-update.schema.json", MEMORY_UPDATE_SCHEMA)
    jobs_dir.mkdir(parents=True, exist_ok=True)
    (jobs_dir / "README.md").write_text(JOBS_README, encoding="utf-8")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def find_job(manifest_path: Path, job_id: str) -> dict[str, Any]:
    for job in load_jsonl(manifest_path):
        if job.get("job_id") == job_id:
            return job
    raise KeyError(f"No job_id {job_id!r} in {manifest_path}")


def _prompt_text(value: object) -> str:
    return str(value).replace("\x00", "")


def _resolve_prompt_path(root: Path | None, path: object) -> Path:
    candidate = Path(str(path))
    if candidate.is_absolute() or root is None:
        return candidate
    return root / candidate


def _embedded_review_inputs(job: dict[str, Any], root: Path | None) -> str:
    blocks: list[str] = []
    for review_path in job.get("review_paths", []):
        label = _prompt_text(review_path)
        resolved = _resolve_prompt_path(root, review_path)
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


def build_source_dossier_prompt(job: dict[str, Any], root: Path | None = None) -> str:
    paper_ids = "\n".join(f"- {_prompt_text(paper_id)}" for paper_id in job.get("paper_ids", []))
    review_paths = "\n".join(f"- {_prompt_text(path)}" for path in job.get("review_paths", []))
    embedded_reviews = _embedded_review_inputs(job, root)
    memory_context = build_memory_context(root, job)
    return f"""Write one factual NotebookLM source dossier for a Paper Radio episode.

Job ID: {job["job_id"]}
Episode ID: {job["episode_id"]}
Title: {job["title"]}
Episode type: {job.get("episode_type", "unknown")}
Required schema: {job["schema_path"]}
NotebookLM dossier markdown output: {job["bundle_output_path"]}

Papers:
{paper_ids}

Review inputs to read:
{review_paths}

Embedded review JSON inputs:

{embedded_reviews}

Memory context for this episode:

{memory_context}

Use the memory context only as framing guidance. Current paper sources and current review records remain the evidence.
If no durable card matched, do not force a weak analogy.

NotebookLM will generate the conversational audio. Do not write dialogue, speaker names, stage directions,
banter, cold opens, finished narration, or host patter.

The research_dossier_markdown should be factual, compact, and opinionated. Use these top-level Markdown
sections in this order:
- ## Episode Metadata
- ## Why These Papers Are Grouped
- ## Concise Thesis
- ## Per-Paper Claim Versus Evidence
- ## Strongest Contributions
- ## Serious Weaknesses And Red Flags
- ## Missing Baselines And Ablations
- ## Comparison Axes
- ## Verdict For The Listener
- ## Source Notes And Local Input Paths

Also decide what original paper sources, if any, NotebookLM should receive in addition to
research_dossier.md. Return this decision in recommended_upload_sources:
- Choose zero, one, or two papers only.
- Recommend an original paper only when it is an anchor for a specific mechanism, result, or critique that
  would benefit from NotebookLM seeing the paper directly.
- Use source_type `paper_pdf` with source_path `data/papers/pdfs/<paper_id>.pdf` when the PDF is likely to
  import cleanly; otherwise use source_type `paper_markdown` with source_path `data/papers/<paper_id>.md`.
- The rationale must explain why that paper deserves upload budget.
- Do not recommend raw review JSON files for upload. The review JSONs are local provenance and compression
  inputs; if they contain important details, synthesize those details into research_dossier_markdown.
- Set missing_inputs to [] when the embedded review JSON inputs above are present. Do not claim review files
  are unavailable after reading the embedded JSON.
- Include every review input path listed above in citations exactly as written.

Return only JSON matching the schema. The local runner writes research_dossier_markdown to the
NotebookLM dossier markdown output path for upload.
"""


def _embedded_file(path_label: object, root: Path | None) -> str:
    label = _prompt_text(path_label)
    resolved = _resolve_prompt_path(root, path_label)
    if not resolved.exists():
        return f"### {label}\n\nMISSING: {label}"
    return f"### {label}\n\n{resolved.read_text(encoding='utf-8')}"


def build_promote_memory_prompt(job: dict[str, Any], root: Path | None = None) -> str:
    memory_note = _embedded_file(job["memory_note_path"], root)
    dossier = _embedded_file(job["bundle_output_path"], root)
    vocab = _embedded_file(job["vocab_path"], root)
    existing_cards = []
    for card_path in job.get("candidate_card_paths", []):
        existing_cards.append(_embedded_file(card_path, root))
    existing_cards_text = (
        "\n\n".join(existing_cards) if existing_cards else "No candidate existing cards were provided."
    )
    return f"""Decide whether this Paper Radio episode should promote durable memory.

Job ID: {job["job_id"]}
Episode ID: {job["episode_id"]}
Output path: {job["output_path"]}
Required schema: {job["schema_path"]}

Durable memory cards are curated compression for future episodes. They are not episode summaries.
Most episodes should create zero or one updates. Use no updates when the observation is too paper-specific.

Allowed card types:
- topic
- benchmark
- red-flag
- lab
- domain
- method

Promotion criteria:
- The point is likely reusable across future papers.
- The point describes a claim family, benchmark, method, lab/source behavior, domain workflow, or recurring red flag.
- The point changes how future papers should be evaluated.
- The body can stay compact without crowding out current evidence.

Rules:
- Return only JSON matching the schema.
- Do not write card files yourself. The local runner applies validated updates.
- updates may be [].
- If updates is [], write a concrete no_update_reason and keep proposed_new_tags [].
- If you use a tag that is not already in vocab, include it in proposed_new_tags.
- Use canonical slug-style tags, for example `agent-memory`, `clinical-evals`, `stale-baselines`.
- evidence must include the current episode ID: {job["episode_id"]}.
- citations must include both `{job["memory_note_path"]}` and `{job["bundle_output_path"]}`.
- card_path must be `data/memory/cards/<card_type>/<slug>.md`.
- body_markdown should be 75-900 words and must distinguish current evidence from prior framing.
- changelog_entry must mention {job["episode_id"]}.

Current vocab:

{vocab}

Existing candidate cards:

{existing_cards_text}

Episode memory note:

{memory_note}

Current source dossier:

{dossier}
"""


def build_job_prompt(job: dict[str, Any], root: Path | None = None) -> str:
    kind = str(job.get("kind", ""))
    if kind == "source_dossier":
        return build_source_dossier_prompt(job, root=root)
    if kind == "promote_memory":
        return build_promote_memory_prompt(job, root=root)
    if kind == "review":
        input_paths = "\n".join(f"- {_prompt_text(path)}" for path in job.get("input_paths", []))
        return f"""Critically review one ML paper for Paper Radio.

Job ID: {job["job_id"]}
Paper ID: {job["paper_id"]}
Output path: {job["output_path"]}
Required schema: {job["schema_path"]}

Paper inputs to read:
{input_paths}

Return only JSON matching the schema. Be skeptical, concrete, and source-grounded.
"""
    if kind == "triage":
        candidate_json = json.dumps(job.get("candidate", {}), indent=2, ensure_ascii=False)
        return f"""Triage one ML paper for Paper Radio.

Job ID: {job["job_id"]}
Paper ID: {job["paper_id"]}
Output path: {job["output_path"]}
Required schema: {job["schema_path"]}

Use only the embedded candidate JSON below. Do not browse the web. Do not inspect repository files.
This is fast triage, not a full review. Infer from title, abstract, authors, categories, and source signals only.
Do not cite external evidence. Do not reward hype language without evidence in the abstract.
The decision must be exactly one of: advance_to_review, queue_for_review, skip.
Affiliations and trusted_orgs are weak source signals. They can affect review priority, but they are not evidence
that the paper's claims are correct.
Set triage_rationale to one or two concrete sentences explaining the decision.
Use a 0 to 10 scale for research_score_estimate and podcast_score_estimate, not a 0 to 1 scale.

Embedded candidate JSON:
{candidate_json}

Return only JSON matching the schema. Score both research quality and podcast value.
"""
    raise ValueError(f"Unsupported job kind: {kind}")
