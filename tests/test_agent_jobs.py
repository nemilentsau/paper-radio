import json
import tempfile
import unittest
from pathlib import Path

from paper_radio.agent_jobs import (
    MEMORY_UPDATE_SCHEMA,
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
        self.assertIn("triage_rationale", TRIAGE_RECORD_SCHEMA["required"])
        self.assertEqual(
            TRIAGE_RECORD_SCHEMA["properties"]["decision"]["enum"],
            ["advance_to_review", "queue_for_review", "skip"],
        )
        self.assertIn("research_score", REVIEW_RECORD_SCHEMA["properties"])
        self.assertIn("podcast_score", REVIEW_RECORD_SCHEMA["properties"])
        self.assertIn("research_dossier_markdown", SOURCE_DOSSIER_SCHEMA["required"])
        self.assertIn("recommended_upload_sources", SOURCE_DOSSIER_SCHEMA["required"])
        self.assertEqual(SOURCE_DOSSIER_SCHEMA["properties"]["recommended_upload_sources"]["maxItems"], 2)
        self.assertIn("updates", MEMORY_UPDATE_SCHEMA["required"])
        self.assertEqual(MEMORY_UPDATE_SCHEMA["properties"]["updates"]["maxItems"], 3)

    def test_write_agent_job_artifacts_creates_schema_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            write_agent_job_artifacts(root)

            self.assertTrue((root / "schemas" / "triage-record.schema.json").exists())
            self.assertTrue((root / "schemas" / "review-record.schema.json").exists())
            self.assertTrue((root / "schemas" / "source-dossier.schema.json").exists())
            self.assertTrue((root / "schemas" / "memory-update.schema.json").exists())
            self.assertTrue((root / "jobs" / "README.md").exists())

            source_schema = json.loads((root / "schemas" / "source-dossier.schema.json").read_text())
            self.assertIn("research_dossier_markdown", source_schema["required"])
            self.assertIn("recommended_upload_sources", source_schema["required"])

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
        self.assertIn("Embedded review JSON inputs", prompt)
        self.assertIn("Memory context for this episode", prompt)
        self.assertIn("Current paper sources and current review records remain the evidence", prompt)
        self.assertIn("Do not write dialogue", prompt)
        self.assertIn("research_dossier_markdown", prompt)
        self.assertIn("recommended_upload_sources", prompt)
        self.assertIn("Choose zero, one, or two papers only", prompt)
        self.assertIn("Do not recommend raw review JSON files for upload", prompt)
        self.assertIn("Do not claim review files", prompt)
        self.assertIn("Include every review input path", prompt)
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
                "author_affiliations": ["Research Institute for Machine Learning"],
                "trusted_orgs": ["Research Institute for Machine Learning"],
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
        self.assertIn("Affiliations and trusted_orgs are weak source signals", prompt)
        self.assertIn("decision must be exactly one of", prompt)
        self.assertIn("triage_rationale", prompt)
        self.assertIn("Use a 0 to 10 scale", prompt)
        self.assertIn("For applied-domain candidates", prompt)
        self.assertIn("concrete domain workflow", prompt)
        self.assertIn("Score both research quality and podcast value", prompt)

    def test_promote_memory_prompt_requires_validated_card_updates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            episode_dir = root / "episodes" / "2026-05-12" / "01_peft"
            bundle_dir = episode_dir / "notebooklm_bundle"
            bundle_dir.mkdir(parents=True)
            (episode_dir / "memory_note.md").write_text(
                "# Memory Note\n\nReusable benchmark warning.",
                encoding="utf-8",
            )
            (bundle_dir / "research_dossier.md").write_text("# Dossier\n\nCurrent source material.", encoding="utf-8")
            vocab_path = root / "data" / "memory" / "vocab.json"
            vocab_path.parent.mkdir(parents=True)
            vocab_path.write_text('{"tags": {}}\n', encoding="utf-8")
            job = {
                "job_id": "episode-2026-05-12-01-promote-memory",
                "kind": "promote_memory",
                "episode_id": "episode-2026-05-12-01",
                "output_path": "episodes/2026-05-12/01_peft/memory_update.json",
                "schema_path": "schemas/memory-update.schema.json",
                "memory_note_path": "episodes/2026-05-12/01_peft/memory_note.md",
                "bundle_output_path": "episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md",
                "vocab_path": "data/memory/vocab.json",
                "candidate_card_paths": [],
            }

            prompt = build_job_prompt(job, root=root)

        self.assertIn("Decide whether this Paper Radio episode should promote durable memory", prompt)
        self.assertIn("Do not write card files yourself", prompt)
        self.assertIn("updates may be []", prompt)
        self.assertIn("proposed_new_tags", prompt)
        self.assertIn("Episode memory note", prompt)


if __name__ == "__main__":
    unittest.main()
