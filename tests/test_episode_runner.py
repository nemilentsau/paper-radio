import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from paper_radio.episode_runner import (
    ReviewReadinessError,
    plan_episode_jobs,
    run_episode,
    validate_reviews_ready,
)


class EpisodeRunnerTest(unittest.TestCase):
    def _write_substantive_review(self, root: Path, paper_id: str) -> None:
        review_dir = root / "data" / "reviews"
        review_dir.mkdir(parents=True, exist_ok=True)
        (review_dir / f"{paper_id}.json").write_text(
            json.dumps(
                {
                    "paper_id": paper_id,
                    "one_line_claim": "The paper claims minor singular directions improve PEFT.",
                    "what_they_tested": "It compares minor, major, and random singular-vector adaptations.",
                    "strongest_point": "It directly ablates minor, major, and random directions.",
                    "weakest_point": "The central empirical comparison is too thin for an optimizer paper.",
                    "missing_baselines": ["Full fine-tuning under a matched compute budget."],
                    "missing_ablations": ["Seed variance across all reported tasks."],
                    "red_flags": ["The benchmark mix is too narrow for the headline claim."],
                    "positive_signals": ["The central ablation directly targets the mechanism."],
                    "research_score": 4.5,
                    "podcast_score": 8.0,
                    "overclaim_score": 6.0,
                    "replication_interest": 7.0,
                    "verdict": "Flawed but interesting enough to discuss if the review foregrounds limits.",
                    "citations": ["Table 2 compares minor, major, and random directions."],
                }
            ),
            encoding="utf-8",
        )

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
                    "episode-2026-05-12-01-promote-memory",
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

    def test_validate_reviews_ready_rejects_schema_shaped_but_empty_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            review_dir = root / "data" / "reviews"
            review_dir.mkdir(parents=True)
            (review_dir / "arxiv-2604.01694.json").write_text(
                json.dumps(
                    {
                        "paper_id": "wrong-paper-id",
                        "one_line_claim": "Thin claim.",
                        "what_they_tested": "Thin methods.",
                        "strongest_point": "Thin strength.",
                        "weakest_point": "Thin weakness.",
                        "missing_baselines": [],
                        "missing_ablations": [],
                        "red_flags": [],
                        "positive_signals": [],
                        "research_score": 0,
                        "podcast_score": 0,
                        "overclaim_score": 0,
                        "replication_interest": 0,
                        "verdict": "Thin verdict.",
                        "citations": [],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ReviewReadinessError, "not production-ready"):
                validate_reviews_ready(root, ["arxiv-2604.01694"])

    def test_validate_reviews_ready_rejects_accidental_placeholder_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            review_dir = root / "data" / "reviews"
            review_dir.mkdir(parents=True)
            (review_dir / "arxiv-2604.01694.json").write_text(
                json.dumps(
                    {
                        "paper_id": "arxiv-2604.01694",
                        "one_line_claim": "The paper claims minor singular directions improve PEFT.",
                        "what_they_tested": "It compares minor, major, and random singular-vector adaptations.",
                        "strongest_point": "It directly ablates minor, major, and random directions.",
                        "weakest_point": "The central empirical comparison is too thin for an optimizer paper.",
                        "missing_baselines": ["Full fine-tuning under a matched compute budget."],
                        "missing_ablations": ["Seed variance across all reported tasks."],
                        "red_flags": [
                            "I have not yet read the paper inputs; this placeholder was emitted accidentally."
                        ],
                        "positive_signals": ["The central ablation directly targets the mechanism."],
                        "research_score": 4.5,
                        "podcast_score": 8.0,
                        "overclaim_score": 6.0,
                        "replication_interest": 7.0,
                        "verdict": "Flawed but interesting enough to discuss if the review foregrounds limits.",
                        "citations": ["Table 2 compares minor, major, and random directions."],
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
                        "what_they_tested": "It compares minor, major, and random singular-vector adaptations.",
                        "strongest_point": "It directly ablates minor, major, and random directions.",
                        "weakest_point": "The evaluation is too narrow to support broad claims.",
                        "missing_baselines": ["Full fine-tuning under a matched compute budget."],
                        "missing_ablations": ["Seed variance across all reported tasks."],
                        "red_flags": ["The benchmark mix is too narrow for the headline claim."],
                        "positive_signals": ["The central ablation directly targets the mechanism."],
                        "research_score": 4.5,
                        "podcast_score": 8.0,
                        "overclaim_score": 6.0,
                        "replication_interest": 7.0,
                        "verdict": "Flawed but interesting enough to discuss if the review foregrounds limits.",
                        "citations": ["Table 2 compares minor, major, and random directions."],
                    }
                ),
                encoding="utf-8",
            )

            validate_reviews_ready(root, ["arxiv-2604.01694"])

    def test_validate_reviews_ready_accepts_substantive_placeholder_critique(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            review_dir = root / "data" / "reviews"
            review_dir.mkdir(parents=True)
            (review_dir / "arxiv-2604.01694.json").write_text(
                json.dumps(
                    {
                        "paper_id": "arxiv-2604.01694",
                        "one_line_claim": "The paper claims minor singular directions improve PEFT.",
                        "what_they_tested": "It compares minor, major, and random singular-vector adaptations.",
                        "strongest_point": "It directly ablates minor, major, and random directions.",
                        "weakest_point": "The central empirical comparison is too thin for an optimizer paper.",
                        "missing_baselines": [
                            "A production placeholder replacement baseline that keeps token budget fixed."
                        ],
                        "missing_ablations": ["Seed variance across all reported tasks."],
                        "red_flags": ["The benchmark mix is too narrow for the headline claim."],
                        "positive_signals": ["The central ablation directly targets the mechanism."],
                        "research_score": 4.5,
                        "podcast_score": 8.0,
                        "overclaim_score": 6.0,
                        "replication_interest": 7.0,
                        "verdict": "Flawed but interesting enough to discuss if the review foregrounds limits.",
                        "citations": ["Table 2 compares minor, major, and random directions."],
                    }
                ),
                encoding="utf-8",
            )

            validate_reviews_ready(root, ["arxiv-2604.01694"])

    def test_validate_reviews_ready_accepts_too_thin_as_substantive_critique(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            review_dir = root / "data" / "reviews"
            review_dir.mkdir(parents=True)
            (review_dir / "arxiv-2604.01694.json").write_text(
                json.dumps(
                    {
                        "paper_id": "arxiv-2604.01694",
                        "one_line_claim": "The paper claims minor singular directions improve PEFT.",
                        "what_they_tested": "It compares minor, major, and random singular-vector adaptations.",
                        "strongest_point": "It directly ablates minor, major, and random directions.",
                        "weakest_point": "The central empirical comparison is too thin for an optimizer paper.",
                        "missing_baselines": ["Full fine-tuning under a matched compute budget."],
                        "missing_ablations": ["Seed variance across all reported tasks."],
                        "red_flags": ["The benchmark mix is too narrow for the headline claim."],
                        "positive_signals": ["The central ablation directly targets the mechanism."],
                        "research_score": 4.5,
                        "podcast_score": 8.0,
                        "overclaim_score": 6.0,
                        "replication_interest": 7.0,
                        "verdict": "Flawed but interesting enough to discuss if the review foregrounds limits.",
                        "citations": ["Table 2 compares minor, major, and random directions."],
                    }
                ),
                encoding="utf-8",
            )

            validate_reviews_ready(root, ["arxiv-2604.01694"])

    def test_run_episode_resumes_by_skipping_existing_valid_reviews(self):
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
            self._write_substantive_review(root, "arxiv-2604.01694")

            def fake_run_job(manifest: Path, job_id: str, agent: str, *, root: Path) -> list[str]:
                if job_id == "review-arxiv-2604.09999":
                    self._write_substantive_review(root, "arxiv-2604.09999")
                return [str(manifest), job_id, agent]

            with patch("paper_radio.episode_runner.run_job", side_effect=fake_run_job) as run_job_mock:
                commands = run_episode("episodes/2026-05-12/01_peft", "codex", root=root)

            self.assertEqual(
                [call.args[1] for call in run_job_mock.call_args_list],
                [
                    "review-arxiv-2604.09999",
                    "episode-2026-05-12-01-dossier",
                    "episode-2026-05-12-01-promote-memory",
                ],
            )
            self.assertEqual(
                [command[1] for command in commands],
                [
                    "review-arxiv-2604.09999",
                    "episode-2026-05-12-01-dossier",
                    "episode-2026-05-12-01-promote-memory",
                ],
            )


if __name__ == "__main__":
    unittest.main()
