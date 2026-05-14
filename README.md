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

Run one daily episode end to end:

```bash
uv run python -m paper_radio.cli daily-run \
  --run-date 2026-05-13 \
  --category cs.LG \
  --category cs.CL \
  --category cs.AI \
  --max-results 10 \
  --episode-slug 01_frontier_ml_roundup \
  --title "Frontier ML roundup: agent memory, post-training, and multimodal generation" \
  --episode-type frontier_ml_roundup \
  --agent codex
```

Add `--fresh` to delete run-date candidates, the run-date episode directory, and candidate-derived triage/paper/source/review artifacts before rerunning.

Discover recent arXiv candidates:

```bash
uv run python -m paper_radio.cli candidate-arxiv \
  --category cs.LG \
  --category cs.CL \
  --category cs.AI \
  --max-results 100
```

arXiv affiliation metadata is opportunistic: the API can expose author-supplied
`arxiv:affiliation` values, but many papers omit them. When affiliations are
present, Paper Radio matches them against `config/trusted-orgs.json` and stores
the resulting `trusted_orgs` as weak triage signals. Edit that config to tune
which labs or universities get source-signal treatment.

Create triage jobs for a candidate batch:

```bash
uv run python -m paper_radio.cli plan-triage --candidate-path data/candidates/2026-05-12/arxiv.json
```

Promote selected triage outputs into stored paper records:

```bash
uv run python -m paper_radio.cli promote-triage
```

Ingest a known arXiv paper ID:

```bash
uv run python -m paper_radio.cli ingest-arxiv --id 2604.01694
```

Create an episode manifest from stored paper records:

```bash
uv run python -m paper_radio.cli create-episode \
  --episode-path episodes/2026-05-12/01_peft \
  --title "PEFT papers with stale baselines" \
  --episode-type comparison \
  --paper-id arxiv-2604.01694
```

Create or update the job manifests for an episode:

```bash
uv run python -m paper_radio.cli plan-episode --episode-path episodes/2026-05-12/01_peft
```

Production episode runs should use the ordered runner:

```bash
scripts/run_episode --episode-path episodes/2026-05-12/01_peft --agent codex
```

The runner executes paper review jobs first, validates that review records are substantive, then creates the source dossier for NotebookLM. The source-dossier job also decides whether zero, one, or two original paper sources should be uploaded as anchors. The final bundle contains `notebooklm_bundle/research_dossier.md` plus `notebooklm_bundle/HANDOFF.md` with the Deep Dive, Long, not-Debate settings, the exact recommended upload set, local provenance paths, the custom prompt, and the operator checklist. Raw review JSONs stay local provenance; important review details should be synthesized into the dossier instead of uploaded as machine-oriented JSON.
