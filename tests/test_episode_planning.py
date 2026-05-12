import json
import tempfile
import unittest
from pathlib import Path

from paper_radio.episode_planning import write_episode_job_manifests


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class EpisodePlanningTest(unittest.TestCase):
    def test_write_episode_job_manifests_creates_review_and_source_dossier_jobs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            episode_dir = root / "episodes" / "2026-05-12" / "01_peft"
            episode_dir.mkdir(parents=True)
            (episode_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "episode_id": "episode-2026-05-12-01",
                        "title": "PEFT papers with stale baselines",
                        "episode_type": "comparison",
                        "paper_ids": ["arxiv-2604.01694", "arxiv-2604.09999"],
                        "paper_paths": {
                            "arxiv-2604.01694": "data/papers/arxiv-2604.01694.md",
                            "arxiv-2604.09999": "data/papers/arxiv-2604.09999.md",
                        },
                    }
                ),
                encoding="utf-8",
            )

            result = write_episode_job_manifests(root, "episodes/2026-05-12/01_peft")

            review_jobs = read_jsonl(root / "jobs" / "reviews.jsonl")
            source_jobs = read_jsonl(root / "jobs" / "source-dossiers.jsonl")

            self.assertEqual(result.review_job_ids, ["review-arxiv-2604.01694", "review-arxiv-2604.09999"])
            self.assertEqual(result.source_dossier_job_id, "episode-2026-05-12-01-dossier")
            self.assertEqual([job["job_id"] for job in review_jobs], result.review_job_ids)
            self.assertEqual(review_jobs[0]["kind"], "review")
            self.assertEqual(review_jobs[0]["paper_id"], "arxiv-2604.01694")
            self.assertEqual(review_jobs[0]["input_paths"], ["data/papers/arxiv-2604.01694.md"])
            self.assertEqual(review_jobs[0]["output_path"], "data/reviews/arxiv-2604.01694.json")
            self.assertEqual(review_jobs[0]["schema_path"], "schemas/review-record.schema.json")

            self.assertEqual(len(source_jobs), 1)
            self.assertEqual(source_jobs[0]["kind"], "source_dossier")
            self.assertEqual(source_jobs[0]["episode_id"], "episode-2026-05-12-01")
            self.assertEqual(source_jobs[0]["paper_ids"], ["arxiv-2604.01694", "arxiv-2604.09999"])
            self.assertEqual(
                source_jobs[0]["review_paths"],
                ["data/reviews/arxiv-2604.01694.json", "data/reviews/arxiv-2604.09999.json"],
            )
            self.assertEqual(
                source_jobs[0]["bundle_output_path"],
                "episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md",
            )

    def test_write_episode_job_manifests_upserts_existing_jobs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            episode_dir = root / "episodes" / "2026-05-12" / "01_peft"
            episode_dir.mkdir(parents=True)
            manifest_path = episode_dir / "manifest.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "episode_id": "episode-2026-05-12-01",
                        "title": "Old title",
                        "episode_type": "comparison",
                        "paper_ids": ["arxiv-2604.01694"],
                    }
                ),
                encoding="utf-8",
            )

            write_episode_job_manifests(root, "episodes/2026-05-12/01_peft")
            manifest_path.write_text(
                json.dumps(
                    {
                        "episode_id": "episode-2026-05-12-01",
                        "title": "Updated title",
                        "episode_type": "anchor",
                        "paper_ids": ["arxiv-2604.01694"],
                    }
                ),
                encoding="utf-8",
            )

            write_episode_job_manifests(root, "episodes/2026-05-12/01_peft")

            review_jobs = read_jsonl(root / "jobs" / "reviews.jsonl")
            source_jobs = read_jsonl(root / "jobs" / "source-dossiers.jsonl")

            self.assertEqual(len(review_jobs), 1)
            self.assertEqual(len(source_jobs), 1)
            self.assertEqual(source_jobs[0]["title"], "Updated title")
            self.assertEqual(source_jobs[0]["episode_type"], "anchor")


if __name__ == "__main__":
    unittest.main()
