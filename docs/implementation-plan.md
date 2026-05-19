# Paper Radio Implementation Plan

## Goal

Turn Paper Radio from a daily arXiv-to-NotebookLM pipeline into a memory-aware research audio system.

The plan is intentionally broad for now. The next step is not to build every source connector or a complex database. The next step is to make the current working pipeline compound over time.

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

## Phase 2: Add Promoted Memory

Add a small memory layer before expanding the funnel, but do not create a giant pile of notes.

The useful pattern from `landscape_of_consciousness` is not its exact capsule system. That project is bounded and course-like; Paper Radio is open-ended. The transferable lesson is:

**memory should be curated compression, not an ever-growing context document.**

Use three layers:

1. **Raw archive**
   - all paper records, review records, dossiers, full text, and PDFs
   - complete provenance
   - not meant to fit into prompt context

2. **Recent working memory**
   - last 7-14 days of episode summaries and review highlights
   - useful for trend detection and "what have we been seeing lately?"
   - allowed to age out

3. **Promoted durable memory**
   - only the few claims, red flags, benchmark warnings, lab priors, and topic summaries worth carrying forward
   - updated over time rather than appended forever
   - small enough to retrieve directly without full RAG

Most daily observations should stay in the archive. Only a few should be promoted.

Durable memory should be represented as living cards:

- topic cards
- benchmark cards
- recurring-red-flag cards
- lab/source cards
- domain cards
- model-family or method-family cards

Each card should stay short, probably 300-700 words. When new evidence arrives, rewrite or amend the card rather than adding another unbounded note.

## Phase 3: Make Future Dossiers Memory-Aware

Before generating a new episode dossier, retrieve a small set of relevant durable cards and recent working-memory items.

Use simple matching first:

- topic tags
- benchmark names
- method tags
- domain tags
- lab or author names
- recurring red flag tags

For a normal episode, include at most:

- 1-2 topic or method cards
- 0-1 benchmark card
- 0-1 red-flag card
- 0-1 lab/source card
- 0-2 recent episode capsules

This keeps context bounded without building full retrieval infrastructure.

Important rule:

**memory is framing guidance, not evidence.**

Current paper sources and current review records remain the factual evidence for the episode. Memory can say "we have seen this pattern before" or "this benchmark has a prior warning," but it should not prove claims about the current paper.

Success criterion:

- today's dossier can say, "This resembles a prior pattern we saw before," without relying on the model's memory.
- the prompt stays small even after a month of daily runs.

## Phase 4: Widen Candidate Discovery

Only after promoted memory exists, add more source lanes.

Priority order:

1. Hugging Face trending papers
2. major lab research blogs
3. rotating domain-application arXiv queries
4. later: PubMed, Europe PMC, OpenAlex, ChemRxiv, SSRN, or other domain indexes

Important rule:

- expand shallow discovery, not deep review
- parse many abstracts if useful
- fully review only a small shortlist

## Phase 5: Add Portfolio Selection

Once multiple source lanes exist, select candidates by portfolio rather than one global ranking.

Example daily mix:

- core ML arXiv
- HF or lab-salience item
- domain-application item
- memory-followup item
- wildcard

This reduces sampling bias without pretending the feed is unbiased.

## Phase 6: Improve Episode Planning

Move from one default episode to multiple candidate episode shapes.

Episode types:

- anchor
- flawed but interesting
- comparison cluster
- lab dispatch
- applied frontier
- recurring pathology

The system should suggest several episode candidates, then produce one by default unless asked for more.

## Phase 7: Weekly And Monthly Memory Products

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

Depromotion criteria:

- no related papers appear after several weeks
- the point was too paper-specific
- later evidence reverses it
- a broader card now covers it better

## Current Recommendation

Build in this order:

1. Promoted memory skeleton.
2. Recent working-memory summary.
3. Bounded memory retrieval for dossiers.
4. Hugging Face ingest.
5. Lab blog ingest.
6. Domain application lane.
7. Portfolio selection.
8. Weekly digest.

The first real milestone is:

**Run tomorrow's episode with one or two durable cards and a recent working-memory summary available to the source-dossier job.**

That is the smallest step that changes the character of the system from daily summarization to cumulative research memory without pretending we already need full RAG.
