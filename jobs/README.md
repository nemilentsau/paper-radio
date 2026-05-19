# Paper Radio Jobs

This directory holds JSONL job manifests for headless Codex or Claude Code runs.

- `triage.jsonl`: fast paper triage jobs
- `reviews.jsonl`: full paper review jobs
- `source-dossiers.jsonl`: episode-level NotebookLM source dossier jobs
- `memory-updates.jsonl`: post-dossier durable memory promotion jobs

Use `scripts/run_episode` for production episode runs so review readiness is checked before a source dossier is created.
