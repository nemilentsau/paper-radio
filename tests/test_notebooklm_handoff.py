import json
import tempfile
import unittest
from pathlib import Path

from paper_radio.notebooklm_handoff import render_notebooklm_handoff
from paper_radio.output_validation import OutputValidationError, validate_source_dossier_files

SUBSTANTIVE_DOSSIER = """## Episode Metadata

- Episode ID: episode-2026-05-12-01
- Papers: arxiv-2604.01694

## Why These Papers Are Grouped

The episode groups papers that share a concrete research and podcast comparison.

## Concise Thesis

The source dossier is factual and gives NotebookLM material rather than a performed script.

## Per-Paper Claim Versus Evidence

- arxiv-2604.01694: The paper makes a testable claim and the review highlights evidence.

## Strongest Contributions

- The dossier preserves critique notes and source-grounded comparisons for NotebookLM.

## Serious Weaknesses And Red Flags

- The papers require careful baseline checking and should not be treated as settled.

## Missing Baselines And Ablations

- The dossier names missing baselines and ablations from the local reviews.

## Comparison Axes

- Research quality.
- Podcast value.
- Replication interest.

## Verdict For The Listener

NotebookLM should generate a Deep Dive discussion from factual notes, not a staged script.

## Source Notes And Local Input Paths

- data/reviews/arxiv-2604.01694.json
""" + ("Additional factual dossier sentence. " * 40)


class NotebookLMHandoffTest(unittest.TestCase):
    def test_render_handoff_uses_llm_recommended_upload_sources(self):
        job = {
            "episode_id": "episode-2026-05-12-01",
            "title": "PEFT papers with stale baselines",
            "episode_type": "paper_roundup",
            "paper_ids": ["arxiv-2604.01694", "arxiv-2604.09999"],
            "review_paths": ["data/reviews/arxiv-2604.01694.json", "data/reviews/arxiv-2604.09999.json"],
            "output_path": "episodes/2026-05-12/01_peft/script.json",
            "bundle_output_path": "episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md",
        }
        output = {
            "recommended_upload_sources": [
                {
                    "paper_id": "arxiv-2604.01694",
                    "source_path": "data/papers/pdfs/arxiv-2604.01694.pdf",
                    "source_type": "paper_pdf",
                    "rationale": "This paper is the central mechanism anchor for the episode.",
                }
            ],
            "citations": ["data/reviews/arxiv-2604.01694.json", "data/reviews/arxiv-2604.09999.json"],
        }

        handoff = render_notebooklm_handoff(job, output)

        self.assertIn("## Recommended NotebookLM Upload Set", handoff)
        self.assertIn("episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md", handoff)
        self.assertIn("data/papers/pdfs/arxiv-2604.01694.pdf", handoff)
        self.assertIn("## LLM Upload Decision", handoff)
        self.assertIn("central mechanism anchor", handoff)
        self.assertIn("## Optional Focus Papers", handoff)
        self.assertIn("may recommend at most two original paper sources", handoff)
        self.assertIn("## Local Provenance", handoff)
        self.assertIn("Do not upload these provenance files by default.", handoff)
        self.assertIn("not uploaded as raw JSON", handoff)
        self.assertIn("data/reviews/arxiv-2604.01694.json", handoff)

    def test_validate_source_dossier_files_requires_handoff_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle_dir = root / "episodes" / "2026-05-12" / "01_peft" / "notebooklm_bundle"
            bundle_dir.mkdir(parents=True)
            output_path = root / "episodes" / "2026-05-12" / "01_peft" / "script.json"
            bundle_output_path = bundle_dir / "research_dossier.md"
            output = {
                "episode_id": "episode-2026-05-12-01",
                "title": "PEFT papers with stale baselines",
                "episode_type": "paper_roundup",
                "research_dossier_markdown": SUBSTANTIVE_DOSSIER,
                "recommended_upload_sources": [],
                "citations": ["data/reviews/arxiv-2604.01694.json"],
                "missing_inputs": [],
            }
            output_path.write_text(json.dumps(output), encoding="utf-8")
            bundle_output_path.write_text(SUBSTANTIVE_DOSSIER, encoding="utf-8")
            job = {
                "episode_id": "episode-2026-05-12-01",
                "title": "PEFT papers with stale baselines",
                "episode_type": "paper_roundup",
                "paper_ids": ["arxiv-2604.01694"],
                "review_paths": ["data/reviews/arxiv-2604.01694.json"],
                "output_path": "episodes/2026-05-12/01_peft/script.json",
                "bundle_output_path": "episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md",
            }

            with self.assertRaisesRegex(OutputValidationError, "HANDOFF.md is missing"):
                validate_source_dossier_files(root, job)


if __name__ == "__main__":
    unittest.main()
