from pathlib import Path
from typing import Any

from paper_radio.memory.context import build_memory_context
from paper_radio.prompts.common import embedded_review_inputs, prompt_text


def build_source_dossier_prompt(job: dict[str, Any], root: Path | None = None) -> str:
    paper_ids = "\n".join(f"- {prompt_text(paper_id)}" for paper_id in job.get("paper_ids", []))
    review_paths = "\n".join(f"- {prompt_text(path)}" for path in job.get("review_paths", []))
    embedded_reviews = embedded_review_inputs(job, root)
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
