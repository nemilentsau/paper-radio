import json
import tempfile
import unittest
from pathlib import Path

from paper_radio.triage_planning import write_triage_job_manifest


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class TriagePlanningTest(unittest.TestCase):
    def test_write_triage_job_manifest_creates_idempotent_jobs_from_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate_path = root / "data" / "candidates" / "2026-05-12" / "arxiv.json"
            candidate_path.parent.mkdir(parents=True)
            candidate_path.write_text(
                json.dumps(
                    [
                        {
                            "paper_id": "arxiv-2604.01694",
                            "title": "MiCA Learns More Knowledge Than LoRA and Full Fine-Tuning",
                            "abstract": "A compact PEFT method is evaluated on knowledge injection tasks.",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            result = write_triage_job_manifest(root, candidate_path)
            write_triage_job_manifest(root, candidate_path)

            jobs = read_jsonl(root / "jobs" / "triage.jsonl")
            self.assertEqual(result.job_ids, ["triage-arxiv-2604.01694"])
            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs[0]["kind"], "triage")
            self.assertEqual(jobs[0]["paper_id"], "arxiv-2604.01694")
            self.assertEqual(jobs[0]["input_paths"], ["data/candidates/2026-05-12/arxiv.json"])
            self.assertEqual(jobs[0]["output_path"], "data/triage/arxiv-2604.01694.json")
            self.assertEqual(jobs[0]["schema_path"], "schemas/triage-record.schema.json")


if __name__ == "__main__":
    unittest.main()
