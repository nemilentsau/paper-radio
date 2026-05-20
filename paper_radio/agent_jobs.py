from pathlib import Path
from typing import Any

from paper_radio.io import load_jsonl, write_json
from paper_radio.memory.cards import ALLOWED_CARD_TYPES
from paper_radio.prompts import (
    build_job_prompt,
    build_promote_memory_prompt,
    build_source_dossier_prompt,
)

__all__ = [
    "MEMORY_UPDATE_SCHEMA",
    "REVIEW_RECORD_SCHEMA",
    "SOURCE_DOSSIER_SCHEMA",
    "TRIAGE_RECORD_SCHEMA",
    "build_job_prompt",
    "build_promote_memory_prompt",
    "build_source_dossier_prompt",
    "find_job",
    "load_jsonl",
    "write_agent_job_artifacts",
]

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


def write_agent_job_artifacts(root: Path) -> None:
    schemas_dir = root / "schemas"
    jobs_dir = root / "jobs"
    write_json(schemas_dir / "triage-record.schema.json", TRIAGE_RECORD_SCHEMA)
    write_json(schemas_dir / "review-record.schema.json", REVIEW_RECORD_SCHEMA)
    write_json(schemas_dir / "source-dossier.schema.json", SOURCE_DOSSIER_SCHEMA)
    write_json(schemas_dir / "memory-update.schema.json", MEMORY_UPDATE_SCHEMA)
    jobs_dir.mkdir(parents=True, exist_ok=True)
    (jobs_dir / "README.md").write_text(JOBS_README, encoding="utf-8")


def find_job(manifest_path: Path, job_id: str) -> dict[str, Any]:
    for job in load_jsonl(manifest_path):
        if job.get("job_id") == job_id:
            return job
    raise KeyError(f"No job_id {job_id!r} in {manifest_path}")
