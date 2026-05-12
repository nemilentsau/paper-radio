import json
import tempfile
import unittest
from pathlib import Path

from paper_radio.papers import PaperRecord, normalize_arxiv_paper_id, write_paper_record


class PaperRecordTest(unittest.TestCase):
    def test_normalize_arxiv_paper_id_removes_version_and_uses_repo_safe_id(self):
        self.assertEqual(normalize_arxiv_paper_id("2604.01694v2"), "arxiv-2604.01694")
        self.assertEqual(normalize_arxiv_paper_id("cs/0607105v1"), "arxiv-cs-0607105")

    def test_write_paper_record_writes_json_and_markdown_inputs_for_review_jobs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paper = PaperRecord(
                paper_id="arxiv-2604.01694",
                source="arxiv",
                source_id="2604.01694",
                title="MiCA Learns More Knowledge Than LoRA and Full Fine-Tuning",
                authors=("Sten Rüdiger", "Sebastian Raschka"),
                author_affiliations=("Research Institute for Machine Learning",),
                abstract="A compact PEFT method is evaluated on knowledge injection tasks.",
                published_at="2026-04-03T00:00:00Z",
                updated_at="2026-04-04T00:00:00Z",
                categories=("cs.LG",),
                pdf_url="https://arxiv.org/pdf/2604.01694",
                abs_url="https://arxiv.org/abs/2604.01694",
                source_types=("arxiv",),
                status="ingested",
                trusted_orgs=("Research Institute for Machine Learning",),
                triage_decision="queue_for_review",
                triage_rationale="Strong audio value and concrete evaluation claim.",
                research_score_estimate=7.2,
                podcast_score_estimate=8.4,
            )

            paths = write_paper_record(root, paper)

            self.assertEqual(paths.json_path, root / "data" / "papers" / "arxiv-2604.01694.json")
            self.assertEqual(paths.markdown_path, root / "data" / "papers" / "arxiv-2604.01694.md")
            data = json.loads(paths.json_path.read_text(encoding="utf-8"))
            markdown = paths.markdown_path.read_text(encoding="utf-8")
            self.assertEqual(data["paper_id"], "arxiv-2604.01694")
            self.assertEqual(data["authors"], ["Sten Rüdiger", "Sebastian Raschka"])
            self.assertEqual(data["author_affiliations"], ["Research Institute for Machine Learning"])
            self.assertEqual(data["trusted_orgs"], ["Research Institute for Machine Learning"])
            self.assertEqual(data["triage_decision"], "queue_for_review")
            self.assertEqual(data["triage_rationale"], "Strong audio value and concrete evaluation claim.")
            self.assertEqual(data["research_score_estimate"], 7.2)
            self.assertEqual(data["podcast_score_estimate"], 8.4)
            self.assertIn("# MiCA Learns More Knowledge Than LoRA and Full Fine-Tuning", markdown)
            self.assertIn("Research Institute for Machine Learning", markdown)
            self.assertIn("Strong audio value and concrete evaluation claim.", markdown)
            self.assertIn("## Abstract", markdown)
            self.assertIn("https://arxiv.org/abs/2604.01694", markdown)

    def test_paper_record_defaults_optional_affiliation_and_triage_fields(self):
        paper = PaperRecord.from_dict(
            {
                "paper_id": "arxiv-2604.01694",
                "source": "arxiv",
                "source_id": "2604.01694",
                "title": "MiCA Learns More Knowledge Than LoRA and Full Fine-Tuning",
                "authors": ["Sten Rüdiger"],
                "abstract": "A compact PEFT method is evaluated on knowledge injection tasks.",
                "published_at": "2026-04-03T00:00:00Z",
                "updated_at": "2026-04-04T00:00:00Z",
                "categories": ["cs.LG"],
                "pdf_url": "https://arxiv.org/pdf/2604.01694",
                "abs_url": "https://arxiv.org/abs/2604.01694",
                "source_types": ["arxiv"],
                "status": "candidate",
            }
        )

        self.assertEqual(paper.author_affiliations, ())
        self.assertEqual(paper.trusted_orgs, ())
        self.assertIsNone(paper.triage_decision)
        self.assertIsNone(paper.triage_rationale)


if __name__ == "__main__":
    unittest.main()
