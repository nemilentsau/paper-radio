import unittest

from paper_radio.cli import build_parser


class CliTest(unittest.TestCase):
    def test_parser_accepts_plan_episode_command(self):
        parser = build_parser()

        args = parser.parse_args(["plan-episode", "--episode-path", "episodes/2026-05-12/01_peft"])

        self.assertEqual(args.command, "plan-episode")
        self.assertEqual(args.episode_path, "episodes/2026-05-12/01_peft")

    def test_parser_accepts_candidate_arxiv_command(self):
        parser = build_parser()

        args = parser.parse_args(
            [
                "candidate-arxiv",
                "--category",
                "cs.LG",
                "--category",
                "cs.CL",
                "--max-results",
                "50",
                "--run-date",
                "2026-05-12",
            ]
        )

        self.assertEqual(args.command, "candidate-arxiv")
        self.assertEqual(args.category, ["cs.LG", "cs.CL"])
        self.assertEqual(args.max_results, 50)
        self.assertEqual(args.run_date, "2026-05-12")

    def test_parser_accepts_candidate_applied_domain_command(self):
        parser = build_parser()

        args = parser.parse_args(
            [
                "candidate-applied-domain",
                "--preset",
                "bio_medicine",
                "--max-results",
                "100",
                "--keep-results",
                "10",
                "--min-score",
                "3",
                "--run-date",
                "2026-05-20",
            ]
        )

        self.assertEqual(args.command, "candidate-applied-domain")
        self.assertEqual(args.preset, "bio_medicine")
        self.assertEqual(args.max_results, 100)
        self.assertEqual(args.keep_results, 10)
        self.assertEqual(args.min_score, 3)
        self.assertEqual(args.run_date, "2026-05-20")

    def test_parser_accepts_ingest_arxiv_command(self):
        parser = build_parser()

        args = parser.parse_args(["ingest-arxiv", "--id", "2604.01694", "--id", "2604.09999"])

        self.assertEqual(args.command, "ingest-arxiv")
        self.assertEqual(args.id, ["2604.01694", "2604.09999"])

    def test_parser_accepts_fetch_sources_command(self):
        parser = build_parser()

        args = parser.parse_args(["fetch-sources", "--paper-id", "arxiv-2605.10933"])

        self.assertEqual(args.command, "fetch-sources")
        self.assertEqual(args.paper_id, ["arxiv-2605.10933"])

    def test_parser_accepts_plan_triage_command(self):
        parser = build_parser()

        args = parser.parse_args(["plan-triage", "--candidate-path", "data/candidates/2026-05-12/arxiv.json"])

        self.assertEqual(args.command, "plan-triage")
        self.assertEqual(args.candidate_path, "data/candidates/2026-05-12/arxiv.json")

    def test_parser_accepts_promote_triage_command(self):
        parser = build_parser()

        args = parser.parse_args(
            [
                "promote-triage",
                "--triage-dir",
                "data/triage",
                "--manifest",
                "jobs/triage.jsonl",
                "--paper-id",
                "arxiv-2605.20176",
            ]
        )

        self.assertEqual(args.command, "promote-triage")
        self.assertEqual(args.triage_dir, "data/triage")
        self.assertEqual(args.manifest, "jobs/triage.jsonl")
        self.assertEqual(args.paper_id, ["arxiv-2605.20176"])

    def test_parser_accepts_create_episode_command(self):
        parser = build_parser()

        args = parser.parse_args(
            [
                "create-episode",
                "--episode-path",
                "episodes/2026-05-12/01_peft",
                "--title",
                "PEFT papers with stale baselines",
                "--episode-type",
                "comparison",
                "--paper-id",
                "arxiv-2604.01694",
            ]
        )

        self.assertEqual(args.command, "create-episode")
        self.assertEqual(args.paper_id, ["arxiv-2604.01694"])

    def test_parser_accepts_daily_run_command(self):
        parser = build_parser()

        args = parser.parse_args(
            [
                "daily-run",
                "--run-date",
                "2026-05-13",
                "--category",
                "cs.LG",
                "--category",
                "cs.CL",
                "--max-results",
                "10",
                "--episode-slug",
                "01_frontier_ml_roundup",
                "--title",
                "Daily frontier ML",
                "--episode-type",
                "frontier_ml_roundup",
                "--agent",
                "codex",
                "--fresh",
            ]
        )

        self.assertEqual(args.command, "daily-run")
        self.assertEqual(args.run_date, "2026-05-13")
        self.assertEqual(args.category, ["cs.LG", "cs.CL"])
        self.assertEqual(args.max_results, 10)
        self.assertEqual(args.episode_slug, "01_frontier_ml_roundup")
        self.assertEqual(args.title, "Daily frontier ML")
        self.assertEqual(args.episode_type, "frontier_ml_roundup")
        self.assertEqual(args.agent, "codex")
        self.assertTrue(args.fresh)


if __name__ == "__main__":
    unittest.main()
