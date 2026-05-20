# Paper Radio Implementation Plan

## Goal

Turn Paper Radio from a daily arXiv-to-NotebookLM pipeline into a memory-aware research audio system.

The plan is intentionally staged. The first compounding layer now exists: daily runs can write episode memory notes, retrieve durable cards, and update those cards after the dossier is produced. The next step is not to build every source connector or a complex database. The next step is to widen the *kind* of arXiv papers we ask for, starting with applied-domain LLM/foundation-model use cases.

## Current Status

Implemented and exercised:

1. Daily arXiv candidate discovery for core ML categories.
2. Cheap triage into a 10-paper episode set.
3. PDF and full-text fetching for selected papers.
4. Headless review jobs with schema-shaped review records.
5. Ordered production runner via `scripts/run_episode`.
6. Source-dossier generation for NotebookLM.
7. NotebookLM bundle generation with `research_dossier.md` and `HANDOFF.md`.
8. Per-episode `memory_note.md` artifacts.
9. Promoted durable memory cards under `data/memory/cards/`.
10. Prompt-time memory retrieval from durable cards plus recent dossiers.
11. Validation for reviews, source dossiers, NotebookLM handoffs, and memory updates.

The 2026-05-19 and 2026-05-20 runs proved the memory loop:

- 2026-05-19 created the initial `active-evidence-acquisition` durable card.
- 2026-05-20 retrieved that card while building the dossier.
- ClinSeekAgent extended the same memory frame from embodied/visual evidence acquisition into clinical evidence-seeking agents.
- The promote-memory job updated the card in place with the new evidence and preserved provenance.

Small production lesson from the 2026-05-20 run: validation should reject real scratch outputs without banning legitimate technical terms. The review placeholder guard was tightened after a false positive on a substantive review phrase.

## Phase 1: Stabilize The Current Daily Run

Keep the existing production path as the backbone:

1. Pull arXiv candidates.
2. Triage candidates.
3. Fetch full text for selected papers.
4. Generate review records.
5. Build the episode dossier.
6. Prepare NotebookLM handoff.

Near-term improvements:

- make reruns less fragile when headless review jobs hang
- keep generated artifacts organized under dated episode folders
- preserve the distinction between research score and podcast score
- keep NotebookLM as the renderer, not the research brain
- keep validator checks strict enough to catch scratch outputs, but narrow enough to avoid rejecting substantive critique

Status: mostly done. Continue hardening only when real runs expose failure modes.

## Phase 2: Add Promoted Memory

Add a small memory layer before expanding the funnel, but do not create a giant pile of notes.

Status: implemented as the current lightweight memory system. Future work here should be refinement, not a rewrite.

The useful pattern from `landscape_of_consciousness` is not its exact capsule system. That project is bounded and course-like; Paper Radio is open-ended. The transferable lesson is:

**memory should be curated compression, not an ever-growing context document.**

Memory lives in three layers, with explicit artifacts for each:

1. **Raw archive** — already exists. Paper records, review records, dossiers, full text, and PDFs under `data/` and `episodes/`. Plus a new per-episode `memory_note.md` written at the end of every run. Append-only. Never rewritten.

2. **Recent working memory** — a *view* over the archive, not a new artifact. The dossier job reads bounded sections from recent `research_dossier.md` files, such as `Concise Thesis`, `Verdict For The Listener`, and source notes from the last 14 days. No summarizer job, no separate file to maintain.

3. **Promoted durable memory** — typed cards under `data/memory/cards/<type>/<slug>.md`. Rewritten in place. Small enough to retrieve directly without RAG.

Most daily observations should stay in the archive. Only a few should be promoted.

Card types:

- topic cards
- benchmark cards
- recurring-red-flag cards
- lab/source cards
- domain cards
- model-family or method-family cards

Each card body stays short, probably 300-700 words. When new evidence arrives, rewrite the body in place rather than appending another unbounded note. Provenance is preserved via append-only frontmatter and changelog (see schema below).

### Card schema

Every card file has YAML frontmatter:

```
---
id: card-benchmark-mmlu
type: benchmark        # topic | benchmark | red-flag | lab | domain | method
tags: [mmlu, evals]
aliases: ["Massive Multitask Language Understanding"]
evidence: [ep-2026-05-19, ep-2026-05-21]   # append-only
updated_at: 2026-05-19
---

<body, 300-700 words, rewritten in place>

## Changelog
- 2026-05-19: initial card from ep-2026-05-19
- 2026-05-21: amended re: contamination concerns (ep-2026-05-21)
```

The body is allowed to drift as the LLM rewrites it. `evidence` and `Changelog` are append-only in intent so provenance survives rewrites; validation should check that existing evidence and changelog entries were preserved.

The frontmatter is also the upgrade path to embeddings: when tag retrieval stops being good enough, batch-embed card bodies and store vectors alongside. The schema does not change; only the index does.

### Tag vocabulary

A hand-curated `data/memory/vocab.json` lists canonical tags and aliases. The promote-memory job is required to map every new tag to an existing canonical tag or explicitly propose a new one. This keeps retrieval working without embeddings.

### Promotion is its own job

After every episode, run a `promote-memory` job (same headless-agent runner as review/dossier). It can: create a new card, amend an existing card in place, or no-op. Promotion criteria are in "Memory Guardrails" below.

The job should produce a structured proposed update first, then write the card only after validation. Durable memory is too important to let a bad model run smear a card silently.

Status: implemented. The runner creates and validates a structured memory-update record, then applies accepted card updates.

### Memory notes vs cards

Memory notes are per-episode artifacts in the raw archive, one per episode, never rewritten. Cards are topic-keyed and rewritten over time. They are not the same thing.

### Concurrency

Episodes run serially through `scripts/run_episode`. Cards are mutated in place under that assumption. Do not parallelize episode runs without revisiting this.

## Phase 3: Make Future Dossiers Memory-Aware

Before generating a new episode dossier, retrieve a small set of relevant durable cards and recent working-memory items.

Retrieve cards by `tag ∈ card.tags ∪ card.aliases`, ranked by `updated_at` desc. Working memory is the last 14 days of dossier headers, read directly off disk.

For a normal episode, include at most:

- 1-2 topic or method cards
- 0-1 benchmark card
- 0-1 red-flag card
- 0-1 lab/source card
- 0-2 recent episode capsules (working memory)

Hard token budget for the memory block: ~2k tokens. Drop oldest-amended cards first if over.

### When nothing matches

If no cards match, the dossier prompt must say so explicitly ("no prior cards matched this topic") rather than injecting the loosest available card. This is how we avoid self-confirming bias on new topics.

Important rule:

**memory is framing guidance, not evidence.**

Current paper sources and current review records remain the factual evidence for the episode. Memory can say "we have seen this pattern before" or "this benchmark has a prior warning," but it should not prove claims about the current paper.

Success criterion:

- today's dossier can say, "This resembles a prior pattern we saw before," without relying on the model's memory.
- the prompt stays small even after a month of daily runs.
- an empty memory block is valid and tested.

Status: implemented for tag/alias card retrieval and recent working memory. The next few runs should tell us whether the retrieval is too narrow, too eager, or about right.

## Phase 4: Add Applied-Domain LLM Use Cases

Before adding Hugging Face, lab blogs, or a multi-source portfolio selector, add one focused source lane for applied-domain LLM/foundation-model papers.

Reason:

- It expands the intellectual surface without changing the whole ingestion architecture.
- It tests the most interesting product direction: LLMs as instruments inside real domain workflows.
- It can reuse the current arXiv candidate, triage, fetch, review, dossier, and memory machinery.
- It avoids mixing popularity/lab-prestige signals into selection before we have domain criteria.

First version: arXiv-only, category plus keyword search.

Target episode type:

- `applied_domain_llm_roundup`

Target paper count:

- still 10 reviewed papers maximum
- discover more candidates shallowly, but only deeply review the selected episode set

Initial domain buckets:

- bio/medicine: `q-bio.*`, `cs.CL`, `cs.AI`, `stat.ML`
- chemistry/materials: `physics.chem-ph`, `cond-mat.mtrl-sci`, `cs.LG`, `stat.ML`
- physics/astronomy: `physics.*`, `astro-ph.*`, `hep-*`, `cs.LG`
- finance/econ: `q-fin.*`, `econ.*`, `stat.ML`, `cs.AI`
- climate/energy/infrastructure: `physics.ao-ph`, `eess.*`, `cs.CE`, `cs.AI`
- robotics/embodied: `cs.RO`, `cs.CV`, `cs.AI`
- software/security: `cs.SE`, `cs.CR`, `cs.AI`, `cs.CL`

Keyword families:

- `"large language model"`, `LLM`, `language model`
- `agent`, `RAG`, `retrieval augmented`
- `foundation model`, `multimodal model`
- `GPT`, `Claude`, `Gemini`, `Llama`, `Qwen`

The first implementation should not try every bucket daily. Start with one mode that can be run explicitly:

```bash
uv run python -m paper_radio.cli daily-run \
  --run-date 2026-05-21 \
  --episode-slug 01_applied_domain_llm_roundup \
  --episode-type applied_domain_llm_roundup \
  --agent codex \
  ...
```

The CLI flags are still to be designed, but the behavior should be:

1. Pull a larger arXiv metadata pool from selected domain categories.
2. Filter/rank by LLM/foundation-model keywords.
3. Triage candidates with domain-use-case criteria.
4. Select a 10-paper episode set.
5. Run the existing production pipeline unchanged after selection.

Review prompt additions for this lane:

- Identify the real domain workflow, not just the ML method.
- Separate ML novelty from domain value.
- Ask whether the domain validation is meaningful to domain experts.
- Watch for "we prompted GPT" demos with no operational validation.
- Track whether the LLM is acting as a search/retrieval assistant, planner, simulator interface, decision-support tool, extraction system, or multimodal perception component.
- Keep domain-specific failure modes visible: clinical safety, wet-lab validation, physical realism, market backtesting leakage, regulatory constraints, security threat models, etc.

Memory implications:

- Promote durable cards only when an applied-domain pattern is reusable.
- Likely new card types/tags will include domain workflows and recurring applied red flags.
- Do not let applied papers become token variety; domain evidence quality matters.

## Phase 5: Widen Candidate Discovery

Only after the applied-domain arXiv lane works, add more source lanes.

Priority order:

1. Hugging Face trending papers
2. major lab research blogs
3. broader non-arXiv domain indexes
4. later: PubMed, Europe PMC, OpenAlex, ChemRxiv, SSRN, or other domain indexes

Important rule:

- expand shallow discovery, not deep review
- parse many abstracts if useful
- fully review only a small shortlist

## Phase 6: Add Portfolio Selection

Once multiple source lanes exist, select candidates by portfolio rather than one global ranking.

Example daily mix:

- core ML arXiv
- HF or lab-salience item
- domain-application item
- memory-followup item
- wildcard

This reduces sampling bias without pretending the feed is unbiased.

## Phase 7: Improve Episode Planning

Move from one default episode to multiple candidate episode shapes.

Episode types:

- anchor
- flawed but interesting
- comparison cluster
- lab dispatch
- applied frontier
- recurring pathology

The system should suggest several episode candidates, then produce one by default unless asked for more.

## Phase 8: Weekly And Monthly Memory Products

Once the durable memory layer has enough history, generate higher-level episodes:

- weekly digest
- top credible papers
- top overclaimed papers
- recurring benchmark problems
- topic trajectory notes
- applied-domain watchlist

This is where Paper Radio becomes more than a daily feed.

## Memory Guardrails

Avoid these failure modes:

- dumping every paper note into future prompts
- treating early impressions as permanent truth
- letting memory turn into self-confirming bias
- overbuilding embeddings/vector search before we know the shape of the data
- promoting trivia that will never matter again

Promotion criteria:

- the point is likely reusable across future papers
- the point describes a claim family, benchmark, method, lab/source behavior, or domain workflow
- the point changes how we should evaluate future work
- the point is short enough to be carried forward without crowding out current evidence

### Pruning (deferred)

Depromotion is deferred until the card set exceeds ~50 cards. Below that threshold, hand-pruning is cheaper than a janitor job. Revisit when the threshold is crossed.

When pruning does come online, depromotion criteria:

- no related papers appear after several weeks
- the point was too paper-specific
- later evidence reverses it
- a broader card now covers it better

## Memory Quality Gates

Before a memory update is accepted, check:

- card frontmatter parses cleanly
- `type` is one of the allowed card types
- tags map to `data/memory/vocab.json`
- existing `evidence` entries are preserved
- existing changelog entries are preserved
- new evidence points to an existing episode or review artifact
- card body stays roughly within the target length
- card body distinguishes current evidence from prior framing
- no card is injected into a dossier when there is no tag/alias match
- the final memory block stays under the token budget

These checks can begin as ordinary Python validation, not a database or RAG system.

## Current Recommendation

Build in this order:

1. Done: per-episode `memory_note.md` writer.
2. Done: card schema + `data/memory/` directory + `vocab.json`.
3. Done: `promote-memory` headless job wired into the episode runner after dossier generation.
4. Done: memory retrieval helper with tag/alias lookup and recent working memory.
5. Done: retrieved cards + working memory injected into the source-dossier prompt, with memory as framing rather than evidence.
6. Next: applied-domain LLM arXiv lane.
7. Then: HF ingest, lab blogs, broader domain indexes, portfolio selection, weekly digest.

The next real milestone:

**A new applied-domain LLM episode runs through the existing production pipeline, still reviewing only about 10 papers, but sourcing candidates from domain categories plus LLM/foundation-model keyword filters.**

That is the smallest step that changes the system from "frontier ML recent papers" to "frontier ML plus practical domain use cases" without prematurely building a multi-source discovery platform.
