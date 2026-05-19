# Paper Radio

Paper Radio is a local pipeline for turning daily research papers into
NotebookLM-ready audio episode bundles.

The important idea: Paper Radio does the research judgment, source selection,
critique, and dossier writing. NotebookLM is only the final audio renderer.

The current system can:

1. Pull recent arXiv candidates.
2. Triage them into a small episode set.
3. Fetch PDFs and extracted full text.
4. Generate compact paper review records with separate research and podcast scores.
5. Build one episode-level factual source dossier.
6. Prepare a NotebookLM handoff bundle.

The next planned step is to add lightweight memory so future episodes can be
grounded in what previous runs already learned, without jumping straight to a
large RAG system.

## Project Status

Working today:

- arXiv candidate discovery
- headless Codex or Claude Code jobs for triage, review, and source dossiers
- ordered single-episode production runner
- NotebookLM handoff bundle with recommended sources and prompt
- quality gates for review and dossier outputs

Planned next:

- `memory_note.md` per episode
- curated durable memory cards under `data/memory/`
- memory retrieval for future source-dossier prompts
- broader discovery lanes: Hugging Face papers, research blogs, and applied domain papers

See:

- [Product and architecture note](docs/idea.md)
- [Implementation plan](docs/implementation-plan.md)

## Setup

Use `uv` and keep dependencies inside this repo's `.venv`.

```bash
uv sync --extra dev
uv run python -m paper_radio.cli init
```

## Quality Gate

Before claiming Python changes are complete, run:

```bash
uv run ruff check .
uv run pyright
uv run python -m unittest discover -s tests -v
```

## Daily Episode Run

The simplest production path is `daily-run`.

```bash
uv run python -m paper_radio.cli daily-run \
  --run-date 2026-05-19 \
  --category cs.LG \
  --category cs.CL \
  --category cs.AI \
  --max-results 10 \
  --episode-slug 01_frontier_ml_roundup \
  --title "Frontier ML roundup" \
  --episode-type frontier_ml_roundup \
  --agent codex
```

Add `--fresh` when you want to delete the run-date candidate batch, episode
folder, and candidate-derived artifacts before rerunning.

## Production Episode Runner

For an existing episode directory, use the ordered runner:

```bash
scripts/run_episode --episode-path episodes/2026-05-19/01_frontier_ml_roundup --agent codex
```

The runner deliberately executes exactly one episode:

1. Run every required `review-<paper-id>` job.
2. Validate that review records are substantive and not placeholders.
3. Run the source-dossier job.
4. Prepare `notebooklm_bundle/research_dossier.md` and `HANDOFF.md`.

Use `run-job` only for low-level debugging or comparison. Do not use it as the
normal production path for a whole episode.

## Manual Workflow

The pieces can also be run manually.

Discover recent arXiv candidates:

```bash
uv run python -m paper_radio.cli candidate-arxiv \
  --category cs.LG \
  --category cs.CL \
  --category cs.AI \
  --max-results 100
```

Create triage jobs:

```bash
uv run python -m paper_radio.cli plan-triage \
  --candidate-path data/candidates/2026-05-19/arxiv.json
```

Promote selected triage outputs into stored paper records:

```bash
uv run python -m paper_radio.cli promote-triage
```

Ingest known arXiv IDs:

```bash
uv run python -m paper_radio.cli ingest-arxiv --id 2604.01694
```

Fetch PDFs and full text:

```bash
uv run python -m paper_radio.cli fetch-sources --paper-id arxiv-2604.01694
```

Create an episode manifest:

```bash
uv run python -m paper_radio.cli create-episode \
  --episode-path episodes/2026-05-19/01_frontier_ml_roundup \
  --title "Frontier ML roundup" \
  --episode-type frontier_ml_roundup \
  --paper-id arxiv-2604.01694
```

Create or update episode job manifests:

```bash
uv run python -m paper_radio.cli plan-episode \
  --episode-path episodes/2026-05-19/01_frontier_ml_roundup
```

## NotebookLM Handoff

NotebookLM receives factual source material, not a performed script.

The final bundle lives under:

```text
episodes/<date>/<episode-slug>/notebooklm_bundle/
```

Key files:

- `research_dossier.md`: the main factual source for NotebookLM
- `HANDOFF.md`: upload instructions, recommended sources, custom prompt, and checklist

NotebookLM settings:

- format: Deep Dive
- length: Long
- do not use Debate

Critique and adversarial framing belong in the source dossier and custom prompt,
not in a separate debate-format audio mode.

## Repository Layout

```text
paper_radio/      Python package
scripts/          thin production command wrappers
jobs/             JSONL manifests for headless agent jobs
schemas/          JSON schemas for generated records
config/           source-signal configuration
data/             generated candidates, papers, reviews, and triage records
episodes/         dated episode manifests, dossiers, bundles, and artifacts
docs/             product notes and implementation planning
tests/            unit tests
```

Generated `data/` and `episodes/` artifacts are provenance. They should stay
schema-shaped so runs can be validated, resumed, and handed off cleanly.

## Design Principles

- The output unit is an episode, not a paper.
- Keep research quality and podcast value as separate scores.
- Weak papers can be useful when they are revealing, entertaining to critique,
  or valuable for comparison.
- Hugging Face trends should be treated as salience signals, not quality signals.
- Memory should be curated compression, not an ever-growing context dump.
- Current paper sources and review records remain the evidence; memory is only
  framing guidance.

## Current Refactor Direction

Before expanding memory and source lanes, the codebase should get a small
structure pass:

- extract shared JSONL helpers
- extract project and episode path helpers
- introduce `paper_radio/memory/` as a real package
- keep the production runner explicit and ordered

Avoid broad framework work for now. The system is still small enough that clear
files and stable data contracts matter more than deep abstraction.
