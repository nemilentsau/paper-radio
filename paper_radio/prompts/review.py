from typing import Any

from paper_radio.prompts.common import prompt_text


def build_review_prompt(job: dict[str, Any]) -> str:
    input_paths = "\n".join(f"- {prompt_text(path)}" for path in job.get("input_paths", []))
    return f"""Critically review one ML paper for Paper Radio.

Job ID: {job["job_id"]}
Paper ID: {job["paper_id"]}
Output path: {job["output_path"]}
Required schema: {job["schema_path"]}

Paper inputs to read:
{input_paths}

Return only JSON matching the schema. Be skeptical, concrete, and source-grounded.
"""
