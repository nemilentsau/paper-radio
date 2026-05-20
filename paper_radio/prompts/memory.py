from pathlib import Path
from typing import Any

from paper_radio.prompts.common import embedded_file


def build_promote_memory_prompt(job: dict[str, Any], root: Path | None = None) -> str:
    memory_note = embedded_file(job["memory_note_path"], root)
    dossier = embedded_file(job["bundle_output_path"], root)
    vocab = embedded_file(job["vocab_path"], root)
    existing_cards = [embedded_file(card_path, root) for card_path in job.get("candidate_card_paths", [])]
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
