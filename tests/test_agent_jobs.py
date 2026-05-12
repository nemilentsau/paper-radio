import json
import tempfile
import unittest
from pathlib import Path

from paper_radio.agent_jobs import (
    REVIEW_RECORD_SCHEMA,
    SOURCE_DOSSIER_SCHEMA,
    TRIAGE_RECORD_SCHEMA,
    build_job_prompt,
    build_source_dossier_prompt,
    write_agent_job_artifacts,
)


class AgentJobsTest(unittest.TestCase):
    def test_schemas_define_standalone_paper_radio_records(self):
        self.assertIn("paper_id", TRIAGE_RECORD_SCHEMA["required"])
        self.assertEqual(
            TRIAGE_RECORD_SCHEMA["properties"]["decision"]["enum"],
            ["advance_to_review", "queue_for_review", "skip"],
        )
        self.assertIn("research_score", REVIEW_RECORD_SCHEMA["properties"])
        self.assertIn("podcast_score", REVIEW_RECORD_SCHEMA["properties"])
        self.assertIn("research_dossier_markdown", SOURCE_DOSSIER_SCHEMA["required"])

    def test_write_agent_job_artifacts_creates_schema_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            write_agent_job_artifacts(root)

            self.assertTrue((root / "schemas" / "triage-record.schema.json").exists())
            self.assertTrue((root / "schemas" / "review-record.schema.json").exists())
            self.assertTrue((root / "schemas" / "source-dossier.schema.json").exists())
            self.assertTrue((root / "jobs" / "README.md").exists())

            source_schema = json.loads((root / "schemas" / "source-dossier.schema.json").read_text())
            self.assertIn("research_dossier_markdown", source_schema["required"])

    def test_source_dossier_prompt_keeps_notebooklm_as_renderer_not_script_writer(self):
        job = {
            "job_id": "episode-2026-05-12-01-dossier",
            "episode_id": "episode-2026-05-12-01",
            "title": "PEFT papers with stale baselines",
            "episode_type": "comparison",
            "paper_ids": ["arxiv-2604.01694", "arxiv-2604.09999"],
            "review_paths": ["data/reviews/arxiv-2604.01694.json", "data/reviews/arxiv-2604.09999.json"],
            "bundle_output_path": "episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md",
            "schema_path": "schemas/source-dossier.schema.json",
        }

        prompt = build_source_dossier_prompt(job)

        self.assertIn("NotebookLM will generate the conversational audio", prompt)
        self.assertIn("Do not write dialogue", prompt)
        self.assertIn("research_dossier_markdown", prompt)
        self.assertIn("PEFT papers with stale baselines", prompt)

    def test_triage_prompt_includes_candidate_input_paths(self):
        job = {
            "job_id": "triage-arxiv-2604.01694",
            "kind": "triage",
            "paper_id": "arxiv-2604.01694",
            "candidate": {
                "paper_id": "arxiv-2604.01694",
                "title": "MiCA Learns More Knowledge Than LoRA and Full Fine-Tuning",
                "abstract": "A compact PEFT method is evaluated on knowledge injection tasks.",
                "categories": ["cs.LG"],
            },
            "input_paths": ["data/candidates/2026-05-12/arxiv.json"],
            "output_path": "data/triage/arxiv-2604.01694.json",
            "schema_path": "schemas/triage-record.schema.json",
        }

        prompt = build_job_prompt(job)

        self.assertIn("Use only the embedded candidate JSON below", prompt)
        self.assertIn("Do not browse the web", prompt)
        self.assertIn("Do not inspect repository files", prompt)
        self.assertIn("MiCA Learns More Knowledge Than LoRA", prompt)
        self.assertIn("decision must be exactly one of", prompt)
        self.assertIn("Score both research quality and podcast value", prompt)


if __name__ == "__main__":
    unittest.main()
