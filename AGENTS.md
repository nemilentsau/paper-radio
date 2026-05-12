# Agent Instructions

## Python Tooling

- Use `uv` for Python dependency management and command execution.
- Keep a dedicated `.venv` in this repo. Create or refresh it with `uv sync --extra dev`.
- Do not rely on a global Python environment for project commands.
- Run Python commands through `uv run`, for example:
  - `uv run python -m paper_radio.cli init`
  - `uv run python -m paper_radio.cli run-episode --episode-path episodes/2026-05-12/01_peft --agent codex`
  - `uv run python -m unittest discover -s tests -v`
  - `uv run ruff check .`
  - `uv run pyright`

## Quality Gate

All Python code must be checked with Ruff and Pyright.

Before claiming Python work is complete, run:

```bash
uv run ruff check .
uv run pyright
uv run python -m unittest discover -s tests -v
```

## Project Notes

- This is the `paper-radio` repo.
- This repo is standalone for now. Reuse proven patterns from `landscape_of_consciousness`, but do not add a runtime dependency on that project until a shared boundary is obvious.
- NotebookLM is only the final audio handoff target. Research, triage, review, scoring, and source-dossier generation should run through local Python plus headless Codex CLI or Claude Code jobs.
- For NotebookLM audio, use Deep Dive format with Long length. Do not choose Debate as the NotebookLM format; critique and adversarial framing belong in the custom prompt and factual source dossier.
- Keep generated paper, review, and episode records schema-shaped so they can be validated, resumed, and used as NotebookLM bundle inputs.
- `script.json` is a historical artifact name borrowed from the reference project. Its content must be factual NotebookLM source material, especially `research_dossier_markdown`; do not create dialogue, host banter, stage directions, or performed scripts.

## Production Pipeline Rules

- Do not run episode production through inline shell snippets or ad hoc one-off command sequences.
- Use `scripts/run_episode --episode-path <episode-dir> --agent codex|claude` for production episode runs.
- Run exactly one episode unless the user explicitly asks for a batch.
- The ordered runner must preserve this sequence:
  1. run every required `review-<paper-id>` job
  2. validate that review records are substantive and not placeholders
  3. run the single source-dossier job for the episode
  4. prepare the `notebooklm_bundle/research_dossier.md` handoff artifact
- `run-job` is low-level debugging/comparison only. Do not use it as the production path for a whole episode.

## Paper Radio Domain Rules

- The output unit is an episode, not a paper.
- Keep separate scores for research quality and podcast value.
- Weak papers are allowed into the queue only when they are analytically useful, entertaining to critique, or valuable for comparison.
- Hugging Face trends are popularity signals, not quality signals.
- Review memos should be compact, concrete, and source-grounded. Avoid long generic summaries.
- NotebookLM bundles should contain factual dossiers, critique notes, and source material. NotebookLM generates the conversation.

## Headless Agent Rules

- Use the locally installed/authenticated Codex CLI or Claude Code CLI.
- Do not tell the user to configure API keys for Claude Code headless unless an actual CLI error proves local auth is unavailable.
- Claude Code should run in normal print mode through the project runner; do not use `--bare` unless the user explicitly requests it.
