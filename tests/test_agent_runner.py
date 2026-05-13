import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from paper_radio.agent_runner import (
    build_claude_command,
    build_codex_command,
    check_agent_available,
    run_job,
)

SUBSTANTIVE_DOSSIER = """## Episode Metadata

- Episode ID: episode-2026-05-12-01
- Papers: arxiv-2604.01694, arxiv-2604.09999

## Why These Papers Are Grouped

These papers are grouped because they test whether small adaptation changes can create useful gains.
The grouping is evidence-focused and highlights the common risk of overclaiming narrow experiments.

## Concise Thesis

The episode thesis is that PEFT claims need careful budget matching, stronger baselines, and direct ablations.

## Per-Paper Claim Versus Evidence

- arxiv-2604.01694: The claim is grounded in an ablation over singular directions and narrow task evidence.
- arxiv-2604.09999: The claim is useful but needs stronger comparisons before broad deployment claims.

## Strongest Contributions

- The reviews identify concrete experiments rather than relying on abstract-only summaries.
- The episode can compare evidence maturity across both papers.

## Serious Weaknesses And Red Flags

- The papers rely on narrow benchmarks and do not fully pin down variance.
- Some deployment claims require stronger baselines.

## Missing Baselines And Ablations

- Full fine-tuning and common PEFT baselines under matched compute.
- Seed variance and task-family sensitivity.

## Comparison Axes

- Evidence maturity.
- Budget matching.
- Replication value.

## Verdict For The Listener

These are useful but incomplete papers. The listener should ask which baseline was matched and what evidence
would change the conclusion.

## Source Notes And Local Input Paths

- data/reviews/arxiv-2604.01694.json
- data/reviews/arxiv-2604.09999.json
"""


class AgentRunnerTest(unittest.TestCase):
    def test_build_codex_command_uses_exec_schema_and_output_file(self):
        job = {
            "kind": "review",
            "output_path": "data/reviews/2604.01694.json",
            "schema_path": "schemas/review-record.schema.json",
        }
        prompt = "Review the paper and return JSON."

        command = build_codex_command(job, prompt)

        self.assertEqual(command[:2], ["codex", "exec"])
        self.assertIn("--sandbox", command)
        self.assertIn("workspace-write", command)
        self.assertIn("--output-schema", command)
        self.assertIn("schemas/review-record.schema.json", command)
        self.assertIn("-o", command)
        self.assertIn("data/reviews/2604.01694.json", command)
        self.assertEqual(command[-1], prompt)

    def test_build_codex_command_uses_low_cost_settings_for_fast_triage(self):
        job = {
            "kind": "triage",
            "output_path": "data/triage/arxiv-2604.01694.json",
            "schema_path": "schemas/triage-record.schema.json",
        }
        prompt = "Triage the embedded candidate."

        command = build_codex_command(job, prompt)

        self.assertIn("--ignore-user-config", command)
        self.assertIn("--model", command)
        self.assertIn("gpt-5.4-mini", command)
        self.assertIn("-c", command)
        self.assertIn('model_reasoning_effort="low"', command)
        self.assertIn("data/triage/arxiv-2604.01694.json", command)

    @patch("paper_radio.agent_runner.subprocess.run")
    def test_run_codex_job_creates_output_parent_before_running_agent(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = root / "jobs" / "triage.jsonl"
            manifest_path.parent.mkdir(parents=True)
            output_path = root / "data" / "triage" / "arxiv-2604.01694.json"
            job = {
                "job_id": "triage-arxiv-2604.01694",
                "kind": "triage",
                "paper_id": "arxiv-2604.01694",
                "candidate": {
                    "paper_id": "arxiv-2604.01694",
                    "title": "A Useful Paper",
                },
                "output_path": "data/triage/arxiv-2604.01694.json",
                "schema_path": "schemas/triage-record.schema.json",
            }
            manifest_path.write_text(json.dumps(job) + "\n", encoding="utf-8")

            def fake_run(command, **kwargs):
                if command == ["codex", "--version"]:
                    return subprocess.CompletedProcess(args=command, returncode=0, stdout="codex 0.130.0", stderr="")
                self.assertTrue(output_path.parent.exists())
                output_path.write_text(
                    json.dumps(
                        {
                            "paper_id": "arxiv-2604.01694",
                            "title": "A Useful Paper",
                            "core_claim": "The paper makes a concrete claim.",
                            "triage_rationale": "This candidate has enough signal for review.",
                            "topic_tags": ["agents"],
                            "likely_red_flags": ["Only abstract-level evidence is available."],
                            "research_score_estimate": 6.5,
                            "podcast_score_estimate": 6.0,
                            "decision": "queue_for_review",
                        }
                    )
                    + "\n",
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(args=command, returncode=0)

            run.side_effect = fake_run

            run_job(manifest_path, "triage-arxiv-2604.01694", "codex", root=root)

    def test_build_claude_command_uses_print_mode_and_json_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            schema_path = root / "schemas" / "source-dossier.schema.json"
            schema_path.parent.mkdir(parents=True)
            schema = {"type": "object", "properties": {"title": {"type": "string"}}, "required": ["title"]}
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            job = {"schema_path": "schemas/source-dossier.schema.json"}
            prompt = "Write a factual NotebookLM source dossier."

            command = build_claude_command(job, prompt, root)

            self.assertEqual(command[:2], ["claude", "-p"])
            self.assertIn(prompt, command)
            self.assertNotIn("--bare", command)
            self.assertIn("--output-format", command)
            self.assertIn("json", command)
            self.assertIn("--json-schema", command)
            self.assertIn(json.dumps(schema), command)

    @patch("paper_radio.agent_runner.subprocess.run")
    def test_run_claude_source_dossier_job_writes_json_and_notebooklm_bundle(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            schema_path = root / "schemas" / "source-dossier.schema.json"
            schema_path.parent.mkdir(parents=True)
            schema_path.write_text(
                json.dumps(
                    {
                        "type": "object",
                        "properties": {
                            "episode_id": {"type": "string"},
                            "title": {"type": "string"},
                            "research_dossier_markdown": {"type": "string"},
                            "citations": {"type": "array", "items": {"type": "string"}},
                            "missing_inputs": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": [
                            "episode_id",
                            "title",
                            "research_dossier_markdown",
                            "citations",
                            "missing_inputs",
                        ],
                    }
                ),
                encoding="utf-8",
            )
            manifest_path = root / "jobs" / "source-dossiers.jsonl"
            manifest_path.parent.mkdir(parents=True)
            job = {
                "job_id": "episode-2026-05-12-01-dossier",
                "kind": "source_dossier",
                "episode_id": "episode-2026-05-12-01",
                "title": "PEFT papers with stale baselines",
                "episode_type": "paper_roundup",
                "paper_ids": ["arxiv-2604.01694", "arxiv-2604.09999"],
                "review_paths": ["data/reviews/arxiv-2604.01694.json", "data/reviews/arxiv-2604.09999.json"],
                "output_path": "episodes/2026-05-12/01_peft/script.json",
                "schema_path": "schemas/source-dossier.schema.json",
                "bundle_output_path": "episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md",
            }
            manifest_path.write_text(json.dumps(job) + "\n", encoding="utf-8")
            structured_output = {
                "episode_id": "episode-2026-05-12-01",
                "title": "PEFT papers with stale baselines",
                "episode_type": "paper_roundup",
                "research_dossier_markdown": SUBSTANTIVE_DOSSIER,
                "citations": ["data/reviews/arxiv-2604.01694.json", "data/reviews/arxiv-2604.09999.json"],
                "missing_inputs": [],
            }
            run.side_effect = [
                subprocess.CompletedProcess(args=["claude", "--version"], returncode=0, stdout="2.1.138", stderr=""),
                subprocess.CompletedProcess(
                    args=["claude", "-p"],
                    returncode=0,
                    stdout=json.dumps({"result": structured_output}),
                    stderr="",
                ),
            ]

            run_job(manifest_path, "episode-2026-05-12-01-dossier", "claude", root=root)

            script_path = root / "episodes" / "2026-05-12" / "01_peft" / "script.json"
            dossier_path = (
                root
                / "episodes"
                / "2026-05-12"
                / "01_peft"
                / "notebooklm_bundle"
                / "research_dossier.md"
            )
            self.assertEqual(json.loads(script_path.read_text(encoding="utf-8")), structured_output)
            self.assertEqual(dossier_path.read_text(encoding="utf-8"), structured_output["research_dossier_markdown"])

    @patch("paper_radio.agent_runner.subprocess.run")
    def test_run_claude_source_dossier_job_rejects_thin_dossier(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            schema_path = root / "schemas" / "source-dossier.schema.json"
            schema_path.parent.mkdir(parents=True)
            schema_path.write_text(
                json.dumps(
                    {
                        "type": "object",
                        "properties": {
                            "episode_id": {"type": "string"},
                            "title": {"type": "string"},
                            "episode_type": {"type": "string"},
                            "research_dossier_markdown": {"type": "string"},
                            "citations": {"type": "array", "items": {"type": "string"}},
                            "missing_inputs": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": [
                            "episode_id",
                            "title",
                            "episode_type",
                            "research_dossier_markdown",
                            "citations",
                            "missing_inputs",
                        ],
                    }
                ),
                encoding="utf-8",
            )
            manifest_path = root / "jobs" / "source-dossiers.jsonl"
            manifest_path.parent.mkdir(parents=True)
            job = {
                "job_id": "episode-2026-05-12-01-dossier",
                "kind": "source_dossier",
                "episode_id": "episode-2026-05-12-01",
                "title": "PEFT papers with stale baselines",
                "episode_type": "paper_roundup",
                "paper_ids": ["arxiv-2604.01694"],
                "review_paths": ["data/reviews/arxiv-2604.01694.json"],
                "output_path": "episodes/2026-05-12/01_peft/script.json",
                "schema_path": "schemas/source-dossier.schema.json",
                "bundle_output_path": "episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md",
            }
            manifest_path.write_text(json.dumps(job) + "\n", encoding="utf-8")
            structured_output = {
                "episode_id": "episode-2026-05-12-01",
                "title": "PEFT papers with stale baselines",
                "episode_type": "paper_roundup",
                "research_dossier_markdown": "Too thin.",
                "citations": [],
                "missing_inputs": [],
            }
            run.side_effect = [
                subprocess.CompletedProcess(args=["claude", "--version"], returncode=0, stdout="2.1.138", stderr=""),
                subprocess.CompletedProcess(
                    args=["claude", "-p"],
                    returncode=0,
                    stdout=json.dumps({"result": structured_output}),
                    stderr="",
                ),
            ]

            with self.assertRaisesRegex(RuntimeError, "source dossier output"):
                run_job(manifest_path, "episode-2026-05-12-01-dossier", "claude", root=root)

    @patch("paper_radio.agent_runner.subprocess.run")
    def test_check_agent_available_reports_broken_cli_stderr(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=["codex", "--version"],
            returncode=1,
            stdout="",
            stderr="spawn missing vendored binary ENOENT",
        )

        with self.assertRaisesRegex(RuntimeError, "codex CLI is not usable"):
            check_agent_available("codex")

    @patch("paper_radio.agent_runner.subprocess.run")
    def test_run_review_job_rejects_manifest_without_full_text_source(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = root / "jobs" / "reviews.jsonl"
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(
                json.dumps(
                    {
                        "job_id": "review-arxiv-2605.10933",
                        "kind": "review",
                        "paper_id": "arxiv-2605.10933",
                        "input_paths": ["data/papers/arxiv-2605.10933.md"],
                        "output_path": "data/reviews/arxiv-2605.10933.json",
                        "schema_path": "schemas/review-record.schema.json",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(RuntimeError, "full-text source"):
                run_job(manifest_path, "review-arxiv-2605.10933", "codex", root=root)

            run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
