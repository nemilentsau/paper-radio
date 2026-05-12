import json
import tempfile
import unittest
from pathlib import Path

from paper_radio.triage_promotion import normalize_triage_decision, promote_triage_results


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def candidate_record(paper_id: str, source_id: str, title: str) -> dict[str, object]:
    return {
        "paper_id": paper_id,
        "source": "arxiv",
        "source_id": source_id,
        "title": title,
        "authors": ["Ada Lovelace", "Grace Hopper"],
        "abstract": "A compact abstract for triage promotion.",
        "published_at": "2026-05-11T17:49:43Z",
        "updated_at": "2026-05-11T17:49:43Z",
        "categories": ["cs.LG"],
        "pdf_url": f"https://arxiv.org/pdf/{source_id}",
        "abs_url": f"https://arxiv.org/abs/{source_id}",
        "source_types": ["arxiv_recent"],
        "status": "candidate",
        "decision": "untriaged",
    }


class TriagePromotionTest(unittest.TestCase):
    def test_normalize_triage_decision_accepts_agent_variants(self):
        self.assertEqual(normalize_triage_decision("queue"), "queue_for_review")
        self.assertEqual(normalize_triage_decision("Queue for Review"), "queue_for_review")
        self.assertEqual(normalize_triage_decision("advance-to-review"), "advance_to_review")
        self.assertEqual(normalize_triage_decision("reject"), "skip")

    def test_promote_triage_results_writes_selected_candidates_as_triaged_papers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            selected = candidate_record(
                "arxiv-2605.10912",
                "2605.10912",
                "WildClawBench: A Benchmark for Real-World, Long-Horizon Agent Evaluation",
            )
            skipped = candidate_record(
                "arxiv-2605.10916",
                "2605.10916",
                "Confidence-Guided Diffusion Augmentation",
            )
            write_jsonl(
                root / "jobs" / "triage.jsonl",
                [
                    {
                        "job_id": "triage-arxiv-2605.10912",
                        "kind": "triage",
                        "paper_id": "arxiv-2605.10912",
                        "candidate": selected,
                    },
                    {
                        "job_id": "triage-arxiv-2605.10916",
                        "kind": "triage",
                        "paper_id": "arxiv-2605.10916",
                        "candidate": skipped,
                    },
                ],
            )
            write_json(
                root / "data" / "triage" / "arxiv-2605.10912.json",
                {
                    "paper_id": "arxiv-2605.10912",
                    "title": selected["title"],
                    "decision": "queue",
                },
            )
            write_json(
                root / "data" / "triage" / "arxiv-2605.10916.json",
                {
                    "paper_id": "arxiv-2605.10916",
                    "title": skipped["title"],
                    "decision": "skip",
                },
            )

            result = promote_triage_results(root)

            self.assertEqual(result.promoted_paper_ids, ["arxiv-2605.10912"])
            self.assertEqual(result.skipped_paper_ids, ["arxiv-2605.10916"])
            self.assertEqual(result.unrecognized_paper_ids, [])
            selected_json = root / "data" / "papers" / "arxiv-2605.10912.json"
            skipped_json = root / "data" / "papers" / "arxiv-2605.10916.json"
            data = json.loads(selected_json.read_text(encoding="utf-8"))
            markdown = (root / "data" / "papers" / "arxiv-2605.10912.md").read_text(encoding="utf-8")
            self.assertEqual(data["status"], "triaged")
            self.assertEqual(data["source_types"], ["arxiv_recent"])
            self.assertEqual(data["abs_url"], "https://arxiv.org/abs/2605.10912")
            self.assertIn("# WildClawBench", markdown)
            self.assertFalse(skipped_json.exists())

    def test_promote_triage_results_requires_candidate_for_selected_paper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_jsonl(root / "jobs" / "triage.jsonl", [])
            write_json(
                root / "data" / "triage" / "arxiv-2605.10912.json",
                {
                    "paper_id": "arxiv-2605.10912",
                    "title": "WildClawBench",
                    "decision": "advance_to_review",
                },
            )

            with self.assertRaisesRegex(RuntimeError, "No triage job candidate"):
                promote_triage_results(root)


if __name__ == "__main__":
    unittest.main()
