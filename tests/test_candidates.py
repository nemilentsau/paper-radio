import json
import tempfile
import unittest
from pathlib import Path

from paper_radio.candidates import write_candidate_batch
from paper_radio.papers import PaperRecord


def make_paper(paper_id: str = "arxiv-2604.01694") -> PaperRecord:
    return PaperRecord(
        paper_id=paper_id,
        source="arxiv",
        source_id=paper_id.removeprefix("arxiv-").replace("-", "/"),
        title="MiCA Learns More Knowledge Than LoRA and Full Fine-Tuning",
        authors=("Sten Rüdiger",),
        author_affiliations=("Research Institute for Machine Learning",),
        abstract="A compact PEFT method is evaluated on knowledge injection tasks.",
        published_at="2026-04-03T00:00:00Z",
        updated_at="2026-04-04T00:00:00Z",
        categories=("cs.LG",),
        pdf_url="https://arxiv.org/pdf/2604.01694",
        abs_url="https://arxiv.org/abs/2604.01694",
        source_types=("arxiv_recent",),
        status="candidate",
        trusted_orgs=("Research Institute for Machine Learning",),
    )


class CandidateTest(unittest.TestCase):
    def test_write_candidate_batch_writes_json_and_markdown_for_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            paths = write_candidate_batch(root, run_date="2026-05-12", source="arxiv", papers=[make_paper()])

            self.assertEqual(paths.json_path, root / "data" / "candidates" / "2026-05-12" / "arxiv.json")
            self.assertEqual(paths.markdown_path, root / "data" / "candidates" / "2026-05-12" / "arxiv.md")
            candidates = json.loads(paths.json_path.read_text(encoding="utf-8"))
            markdown = paths.markdown_path.read_text(encoding="utf-8")
            self.assertEqual(candidates[0]["paper_id"], "arxiv-2604.01694")
            self.assertEqual(candidates[0]["author_affiliations"], ["Research Institute for Machine Learning"])
            self.assertEqual(candidates[0]["trusted_orgs"], ["Research Institute for Machine Learning"])
            self.assertIsNone(candidates[0]["candidate_score"])
            self.assertEqual(candidates[0]["decision"], "untriaged")
            self.assertIn("arxiv-2604.01694", markdown)
            self.assertIn("MiCA Learns More Knowledge", markdown)
            self.assertIn("Research Institute for Machine Learning", markdown)


if __name__ == "__main__":
    unittest.main()
