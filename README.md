# paper-radio

Standalone pipeline for turning daily research papers into NotebookLM-ready audio episode bundles.

The project follows the working `landscape_of_consciousness` pattern, but keeps its own code and domain model for now:

1. Ingest and triage papers.
2. Generate schema-shaped paper reviews with separate research and podcast scores.
3. Build episode-level factual source dossiers.
4. Hand `notebooklm_bundle/research_dossier.md` to NotebookLM as the final audio renderer.

## Setup

```bash
uv sync --extra dev
uv run python -m paper_radio.cli init
```

## Quality Gate

```bash
uv run ruff check .
uv run pyright
uv run python -m unittest discover -s tests -v
```

## Episode Runner

Create or update the job manifests for an episode:

```bash
uv run python -m paper_radio.cli plan-episode --episode-path episodes/2026-05-12/01_peft
```

Production episode runs should use the ordered runner:

```bash
scripts/run_episode --episode-path episodes/2026-05-12/01_peft --agent codex
```

The runner executes paper review jobs first, validates that review records are substantive, then creates the source dossier for NotebookLM.
