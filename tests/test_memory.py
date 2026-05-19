import json
import tempfile
import unittest
from pathlib import Path

from paper_radio.memory.cards import (
    MemoryValidationError,
    apply_memory_update_record,
    ensure_memory_scaffold,
    parse_card_frontmatter,
    validate_memory_update_record,
)
from paper_radio.memory.context import build_memory_context
from paper_radio.memory.notes import write_memory_note

CARD_BODY = (
    "This card captures a reusable evaluation pattern rather than a single paper summary. "
    "The current episode shows that benchmark claims become more useful when the dossier separates the stated "
    "headline from the actual evidence, names the missing comparisons, and records whether the paper is valuable "
    "for critique even when the research score is modest. Future episodes should use this card as framing only: "
    "it can remind the reviewer to inspect baseline freshness, benchmark coverage, ablations, contamination risk, "
    "and whether a popular result is actually measuring the capability it claims to measure. It should not be used "
    "as evidence about any new paper unless the new paper's own sources and review record support the connection."
)


def memory_job() -> dict[str, object]:
    return {
        "job_id": "episode-2026-05-12-01-promote-memory",
        "kind": "promote_memory",
        "episode_id": "episode-2026-05-12-01",
        "memory_note_path": "episodes/2026-05-12/01_peft/memory_note.md",
        "bundle_output_path": "episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md",
        "output_path": "episodes/2026-05-12/01_peft/memory_update.json",
    }


def memory_update() -> dict[str, object]:
    return {
        "episode_id": "episode-2026-05-12-01",
        "updates": [
            {
                "action": "create",
                "card_path": "data/memory/cards/benchmark/baseline-freshness.md",
                "card_type": "benchmark",
                "tags": ["baseline-freshness"],
                "aliases": ["stale baselines"],
                "evidence": ["episode-2026-05-12-01"],
                "updated_at": "2026-05-12",
                "body_markdown": CARD_BODY,
                "changelog_entry": "- 2026-05-12: initial card from episode-2026-05-12-01",
            }
        ],
        "proposed_new_tags": [
            {
                "tag": "baseline-freshness",
                "aliases": ["stale baselines"],
                "rationale": "Reusable benchmark tag for episodes that critique stale or incomplete baselines.",
            }
        ],
        "no_update_reason": "",
        "citations": [
            "episodes/2026-05-12/01_peft/memory_note.md",
            "episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md",
        ],
    }


class MemoryTest(unittest.TestCase):
    def test_write_memory_note_extracts_dossier_sections_and_review_signals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            review_dir = root / "data" / "reviews"
            review_dir.mkdir(parents=True)
            (review_dir / "arxiv-2604.01694.json").write_text(
                json.dumps(
                    {
                        "paper_id": "arxiv-2604.01694",
                        "one_line_claim": "The paper claims better adaptation from minor directions.",
                        "research_score": 4.5,
                        "podcast_score": 8.0,
                        "verdict": "Useful as a critique of narrow PEFT evidence.",
                    }
                ),
                encoding="utf-8",
            )
            job = {
                "episode_id": "episode-2026-05-12-01",
                "title": "PEFT papers with stale baselines",
                "episode_type": "comparison",
                "paper_ids": ["arxiv-2604.01694"],
                "review_paths": ["data/reviews/arxiv-2604.01694.json"],
                "output_path": "episodes/2026-05-12/01_peft/script.json",
                "bundle_output_path": "episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md",
            }
            output = {
                "research_dossier_markdown": (
                    "## Episode Metadata\n\nmetadata\n\n"
                    "## Concise Thesis\n\nThe episode is about stale PEFT baselines.\n\n"
                    "## Verdict For The Listener\n\nListen for claim versus evidence gaps.\n\n"
                    "## Source Notes And Local Input Paths\n\npaths"
                )
            }

            path = write_memory_note(root, job, output)

            note = path.read_text(encoding="utf-8")
            self.assertIn("The episode is about stale PEFT baselines.", note)
            self.assertIn("Listen for claim versus evidence gaps.", note)
            self.assertIn("research 4.5, podcast 8.0", note)

    def test_apply_memory_update_writes_vocab_and_card(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_memory_scaffold(root)
            output = memory_update()

            written = apply_memory_update_record(memory_job(), output, root)

            self.assertEqual(written, [root / "data" / "memory" / "cards" / "benchmark" / "baseline-freshness.md"])
            vocab = json.loads((root / "data" / "memory" / "vocab.json").read_text(encoding="utf-8"))
            self.assertIn("baseline-freshness", vocab["tags"])
            card_text = written[0].read_text(encoding="utf-8")
            frontmatter = parse_card_frontmatter(card_text)
            self.assertEqual(frontmatter["type"], "benchmark")
            self.assertEqual(frontmatter["tags"], ["baseline-freshness"])
            self.assertEqual(frontmatter["evidence"], ["episode-2026-05-12-01"])
            self.assertIn("## Changelog", card_text)

    def test_validate_memory_update_rejects_unproposed_tags(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_memory_scaffold(root)
            output = memory_update()
            output["proposed_new_tags"] = []

            with self.assertRaisesRegex(MemoryValidationError, "not in vocab or proposed_new_tags"):
                validate_memory_update_record(memory_job(), output, root)

    def test_build_memory_context_matches_cards_and_recent_dossiers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            apply_memory_update_record(memory_job(), memory_update(), root)
            review_dir = root / "data" / "reviews"
            review_dir.mkdir(parents=True)
            (review_dir / "arxiv-2604.01694.json").write_text(
                json.dumps(
                    {
                        "paper_id": "arxiv-2604.01694",
                        "one_line_claim": "The key issue is stale baselines and baseline freshness.",
                    }
                ),
                encoding="utf-8",
            )
            prior_dossier = root / "episodes" / "2026-05-10" / "01_prior" / "notebooklm_bundle" / "research_dossier.md"
            prior_dossier.parent.mkdir(parents=True)
            prior_dossier.write_text(
                "## Concise Thesis\n\nPrior thesis about evaluation drift.\n\n"
                "## Verdict For The Listener\n\nPrior verdict about benchmark caution.\n",
                encoding="utf-8",
            )
            job = {
                "title": "Baseline freshness roundup",
                "episode_type": "comparison",
                "paper_ids": ["arxiv-2604.01694"],
                "review_paths": ["data/reviews/arxiv-2604.01694.json"],
                "bundle_output_path": "episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md",
            }

            context = build_memory_context(root, job)

            self.assertIn("baseline-freshness.md", context)
            self.assertIn("Prior thesis about evaluation drift.", context)
            self.assertIn("Memory is framing guidance, not evidence", context)


if __name__ == "__main__":
    unittest.main()
