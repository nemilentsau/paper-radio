import json
from typing import Any


def build_triage_prompt(job: dict[str, Any]) -> str:
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
