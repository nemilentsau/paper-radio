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
                "output_path": "episodes/2026-05-12/01_peft/script.json",
                "schema_path": "schemas/source-dossier.schema.json",
                "bundle_output_path": "episodes/2026-05-12/01_peft/notebooklm_bundle/research_dossier.md",
            }
            manifest_path.write_text(json.dumps(job) + "\n", encoding="utf-8")
            structured_output = {
                "episode_id": "episode-2026-05-12-01",
                "title": "PEFT papers with stale baselines",
                "research_dossier_markdown": "# Research dossier\n\nFactual material for NotebookLM.",
                "citations": ["arXiv:2604.01694"],
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
    def test_check_agent_available_reports_broken_cli_stderr(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=["codex", "--version"],
            returncode=1,
            stdout="",
            stderr="spawn missing vendored binary ENOENT",
        )

        with self.assertRaisesRegex(RuntimeError, "codex CLI is not usable"):
            check_agent_available("codex")


if __name__ == "__main__":
    unittest.main()
