import unittest

from paper_radio.cli import build_parser


class CliTest(unittest.TestCase):
    def test_parser_accepts_plan_episode_command(self):
        parser = build_parser()

        args = parser.parse_args(["plan-episode", "--episode-path", "episodes/2026-05-12/01_peft"])

        self.assertEqual(args.command, "plan-episode")
        self.assertEqual(args.episode_path, "episodes/2026-05-12/01_peft")


if __name__ == "__main__":
    unittest.main()
