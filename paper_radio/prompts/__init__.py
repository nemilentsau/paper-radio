from pathlib import Path
from typing import Any

from paper_radio.prompts.memory import build_promote_memory_prompt
from paper_radio.prompts.review import build_review_prompt
from paper_radio.prompts.source_dossier import build_source_dossier_prompt
from paper_radio.prompts.triage import build_triage_prompt


def build_job_prompt(job: dict[str, Any], root: Path | None = None) -> str:
    kind = str(job.get("kind", ""))
    if kind == "source_dossier":
        return build_source_dossier_prompt(job, root=root)
    if kind == "promote_memory":
        return build_promote_memory_prompt(job, root=root)
    if kind == "review":
        return build_review_prompt(job)
    if kind == "triage":
        return build_triage_prompt(job)
    raise ValueError(f"Unsupported job kind: {kind}")
