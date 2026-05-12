import json
import tempfile
import unittest
from pathlib import Path

from paper_radio.episode_runner import (
    ReviewReadinessError,
    plan_episode_jobs,
    validate_reviews_ready,
)


class EpisodeRunnerTest(unittest.TestCase):
    def test_plan_episode_jobs_runs_reviews_before_source_dossier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            episode_dir = root / "episodes" / "2026-05-12" / "01_peft"
            episode_dir.mkdir(parents=True)
            (episode_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "episode_id": "episode-2026-05-12-01",
                        "paper_ids": ["arxiv-2604.01694", "arxiv-2604.09999"],
                        "script_job_id": "episode-2026-05-12-01-dossier",
                    }
                ),
                encoding="utf-8",
            )

            plan = plan_episode_jobs("episodes/2026-05-12/01_peft", root=root)

            self.assertEqual(
                [step["job_id"] for step in plan],
                [
                    "review-arxiv-2604.01694",
                    "review-arxiv-2604.09999",
                    "episode-2026-05-12-01-dossier",
                ],
            )

    def test_validate_reviews_ready_rejects_placeholders_before_dossier_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            review_dir = root / "data" / "reviews"
            review_dir.mkdir(parents=True)
            (review_dir / "arxiv-2604.01694.json").write_text(
                json.dumps(
                    {
                        "paper_id": "arxiv-2604.01694",
                        "one_line_claim": "Review incomplete",
                        "strongest_point": "Review incomplete",
                        "weakest_point": "Review incomplete",
                        "research_score": 0,
                        "podcast_score": 0,
                        "verdict": "review_incomplete",
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ReviewReadinessError, "not production-ready"):
                validate_reviews_ready(root, ["arxiv-2604.01694"])

    def test_validate_reviews_ready_accepts_substantive_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            review_dir = root / "data" / "reviews"
            review_dir.mkdir(parents=True)
            (review_dir / "arxiv-2604.01694.json").write_text(
                json.dumps(
                    {
                        "paper_id": "arxiv-2604.01694",
                        "one_line_claim": "The paper claims minor singular directions improve PEFT.",
                        "strongest_point": "It directly ablates minor, major, and random directions.",
                        "weakest_point": "The evaluation is too narrow to support broad claims.",
                        "research_score": 4.5,
                        "podcast_score": 8.0,
                        "verdict": "flawed_but_interesting",
                    }
                ),
                encoding="utf-8",
            )

            validate_reviews_ready(root, ["arxiv-2604.01694"])


if __name__ == "__main__":
    unittest.main()
