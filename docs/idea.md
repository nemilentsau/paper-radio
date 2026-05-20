# Paper Radio: Product And Architecture Note

## Working Goal

Paper Radio should be a daily research audio system, not a generic "best papers" ranker.

The target is:

**Produce 1-3 hours per day of high-yield, source-grounded research audio from a ranked and memory-aware paper queue.**

That means the output unit is an **episode**, not a paper. A good day is not necessarily ten excellent papers. A good day is a listenable mix of:

- one serious anchor paper
- one flawed-but-interesting paper
- one comparison cluster
- one short meta or recurring-pathology segment when the day is thin

The system should reward rigor, but it should also preserve papers that are useful because they are revealing, weird, overclaimed, or good foils for comparison.

## What We Have Proven So Far

The current local pipeline already proves the core shape:

1. Pull a daily arXiv candidate batch.
2. Triage into a small episode set.
3. Fetch PDFs and full text.
4. Generate compact review records with separate research and podcast scores.
5. Build an episode-level factual dossier.
6. Hand NotebookLM a dossier plus selected anchor sources.
7. Write per-episode memory notes.
8. Retrieve and update durable memory cards when a reusable pattern recurs.

The 2026-05-19 run showed the key lesson: the dossier is the product. NotebookLM should remain the final audio renderer, while Paper Radio owns the judgment, memory, source selection, and critique.

The 2026-05-20 run showed that the memory layer can actually compound: the active-evidence-acquisition card created from the prior episode was retrieved for ClinSeekAgent, used as framing in the new dossier, then updated with clinical evidence-seeking, staged VLM perception, and structured-knowledge examples.

## The Main Design Tension

We want broader coverage without parsing 100 full papers every morning.

So the pipeline needs two passes:

1. **Wide, shallow discovery**
   - Read metadata, abstracts, venue/source signals, blog metadata, trend signals, and maybe first-page/introduction snippets.
   - Score cheaply.
   - Do not download and parse everything.

2. **Narrow, deep review**
   - Fully fetch and review only the short list.
   - Usually 8-15 papers maximum.
   - Package only 1-4 episodes.

This is the central architecture. Widen the top of the funnel, but keep deep review scarce.

## Source Expansion

### 1. arXiv Recent

Keep arXiv as the backbone because it is predictable, easy to automate, and broad enough for frontier ML.

Default ML categories:

- `cs.LG`
- `cs.CL`
- `cs.AI`
- `cs.CV`
- `cs.RO`
- `cs.SE`
- `cs.DB`
- `stat.ML`

Do not treat all categories equally. Use category as a source signal and apply quotas. For example, do not let `cs.CV` flood the queue unless the episode target is multimodal or robotics.

### 2. Hugging Face Papers

Hugging Face should be a popularity and salience signal, not a quality signal.

Useful signals:

- appeared on daily trending
- appeared on weekly trending
- appeared on monthly trending
- high community discussion
- code/model/demo linked

Interpretation:

- HF trend upvotes can find papers people are talking about.
- They cannot tell whether a paper is rigorous.
- A paper that is both arXiv recent and HF trending should get priority for triage, not automatic promotion.

### 3. Research Blogs

Add a "lab dispatch" source stream for major research blogs and technical reports.

Initial watchlist:

- OpenAI research / announcements with technical substance
- Anthropic research
- Google DeepMind
- Meta AI
- Microsoft Research
- NVIDIA research / technical blogs
- Apple Machine Learning Research
- Cohere, Mistral, AI2, FAIR-adjacent sources

Blog posts should become source records with a different type from papers:

```json
{
  "source_id": "blog-openai-...",
  "source_kind": "research_blog",
  "organization": "OpenAI",
  "title": "...",
  "url": "...",
  "published_at": "...",
  "linked_papers": [],
  "linked_models": [],
  "claims": [],
  "status": "candidate"
}
```

The review question for blogs is different:

- What is the technical claim?
- Is there an associated paper, system card, benchmark, model release, or eval?
- Is this research evidence, product positioning, or safety/communication framing?
- Does it connect to papers already in the knowledge base?

Do not let lab blogs dominate. They are often important, but they are not neutral samples of the field.

### 4. Domain Application Papers

This is the most interesting expansion, and it should be handled as a separate "applied frontier" lane rather than mixed blindly into the ML feed.

This should be the next expansion before Hugging Face trends, lab blogs, or multi-source portfolio selection. The first version can stay arXiv-only and reuse the existing pipeline: pull domain-category candidates, filter for LLM/foundation-model use, triage cheaply, then review only the selected episode set.

Target domains:

- biology and medicine
- chemistry and materials
- physics and astronomy
- robotics and embodied systems
- finance and economics
- climate and energy
- law and governance
- education
- software engineering and security

The key query is not "LLM paper." The key query is:

**Where is an LLM or foundation model used as an instrument inside a real domain workflow?**

Examples of useful applied patterns:

- LLM as scientific literature agent
- LLM as lab planning assistant
- LLM for molecule/material proposal
- LLM for clinical triage or decision support
- LLM for coding or simulation workflows
- LLM for financial analysis, forecasting, or audit
- LLM for legal review or policy analysis
- multimodal model for microscopy, radiology, satellite, robotics, or industrial inspection

Potential intake sources:

- arXiv domain categories: `q-bio.*`, `physics.*`, `cond-mat.*`, `astro-ph.*`, `q-fin.*`, `econ.*`, `stat.AP`, `cs.CE`, `cs.RO`
- PubMed / Europe PMC for biomedical application papers
- bioRxiv and medRxiv for preprints
- ChemRxiv for chemistry and materials
- SSRN or working-paper feeds for finance/econ/legal applications
- Semantic Scholar or OpenAlex as cross-domain discovery indexes

The first version should not try to cover all domains daily. Start with explicit applied-domain runs, then later use rotating domain days:

- Monday: core ML systems/evals
- Tuesday: bio/medicine
- Wednesday: robotics/embodied/multimodal
- Thursday: chemistry/materials/physics
- Friday: finance/econ/software/security plus weekly digest

This keeps the system from becoming a random firehose.

## Avoiding Bias While Staying Cheap

The current "pull 10 recent arXiv papers" approach is fast, but biased:

- recency bias
- category bias
- arXiv-only bias
- title/abstract persuasion bias
- popularity bias if HF is added
- lab prestige bias if blog streams are added
- English/preprint bias

We should not pretend to remove bias. We should make it visible and useful.

Use a portfolio selection rule:

- 40% arXiv recent core ML
- 20% HF/lab/high-salience papers
- 20% domain application papers
- 10% memory-followup papers related to past episodes
- 10% wildcards or random exploration

Then triage each bucket separately. A domain paper should not have to compete directly with a flashy LLM systems paper.

## Knowledge Base: The Compounding Asset

The knowledge base is what turns daily summaries into a real research system.

It should answer:

- Have we seen this claim before?
- Which prior papers are the natural baselines?
- Is this paper using stale baselines?
- Is this benchmark becoming overused?
- Is this lab consistently overclaiming?
- Which topics are getting better versus noisier?
- What did we say about similar papers last week?

### Store Structured Records

Keep the current JSON/Markdown file model, but add a lightweight SQLite index later.

Core objects:

- `PaperRecord`
- `BlogRecord`
- `ReviewRecord`
- `EpisodeRecord`
- `TopicMemory`
- `ClaimMemory`
- `BenchmarkMemory`
- `LabMemory`

### Paper Memory Fields

Each reviewed paper should accumulate:

- topic tags
- method tags
- domain tags
- task tags
- model families
- benchmark names
- datasets
- claimed contribution type
- actual evidence type
- missing baselines
- recurring red flags
- related prior papers
- follow-up questions

### Memory Notes

Add compact memory notes after each episode:

```markdown
# Memory Note

## Topic
embodied spatial intelligence

## New Claim
Spatial intelligence benchmarks should evaluate evidence-seeking actions, not just passive perception.

## Related Prior Claims
- passive visual QA overstates spatial competence
- 3D grounding can help depth-sensitive tasks but can also distort relations if representation is poor

## Reusable Critique
Ask whether the agent can seek falsifying evidence and revise under contradiction.

## Future Watch
Look for real-world or robotics follow-ups that test active evidence acquisition outside simulation.
```

These memory notes are the bridge from "daily paper feed" to "grounded field map."

## Episode Types

### Anchor

One strong paper or lab report with enough evidence to deserve detailed attention.

Use when:

- research score is high
- podcast score is high
- mechanism is crisp
- paper changes how we should think about a topic

### Flawed But Interesting

One paper with a real idea and weak or incomplete evidence.

Use when:

- podcast score is high
- overclaim score is high
- critique is concrete and useful
- the paper illustrates a recurring pathology

### Comparison Cluster

Two to four papers around one topic.

Use when:

- papers share a benchmark, task, method, or claim family
- none is strong enough alone
- the contrast teaches more than a single summary

### Lab Dispatch

One research blog or technical report plus related paper context.

Use when:

- OpenAI/Anthropic/DeepMind/etc. publish something substantive
- the claim connects to ongoing KB threads
- the source is too important to wait for arXiv

### Applied Frontier

One or more domain papers using LLMs/foundation models in practical workflows.

Use when:

- the domain workflow is concrete
- the paper has domain-specific validation
- the ML contribution is not just "we prompted GPT"
- there is a genuine question about deployment, reliability, or scientific value

### Recurring Pathology

A meta episode grounded in the KB.

Examples:

- stale baselines in PEFT
- benchmark theater in agent evals
- crop-supervision disguised as visual reasoning
- simulation-only claims in embodied intelligence
- "we used GPT as a judge" without calibration

## Scoring

Keep separate scores.

### Research Score

How good is the work?

Inputs:

- novelty
- baseline quality
- ablation quality
- benchmark cleanliness
- breadth of validation
- reproducibility
- claim/evidence alignment
- domain validation, if applied

### Podcast Score

How valuable is it as audio?

Inputs:

- clear central idea
- tension or controversy
- critiqueability
- relevance to our interests
- comparison value
- entertainment value
- memory value: does it connect to prior episodes?

### Overclaim Score

How much does the paper outrun its evidence?

This is not always bad for the show. High overclaim plus a real idea can make excellent audio.

### Replication Interest

Would we want to see someone reproduce or stress-test this?

This helps identify papers worth following over time.

## Selection Logic

Use this as the default daily rule:

- keep any paper with `research_score >= 7.0`
- keep any paper with `podcast_score >= 7.5`
- keep any paper that strongly connects to a prior KB thread
- discard papers with both research and podcast scores below 5
- cap full reviews unless the day is unusually strong

Daily episode mix:

- one anchor or serious mixed paper
- one flawed-but-interesting paper
- one comparison or applied-frontier segment
- one meta/follow-up segment if needed

## Proposed Daily Pipeline

### Stage 1: Discovery

Pull a wider candidate pool:

- 50-100 arXiv metadata records
- HF trending records
- lab blog/RSS records
- 10-30 domain-source records, depending on rotating theme

Do not fetch every PDF.

### Stage 2: Cheap Triage

Use title, abstract, metadata, source signals, category, and memory overlap.

Return:

- provisional topic tags
- source signals
- novelty suspicion
- obvious red flags
- likely podcast value
- whether to fetch full text

### Stage 3: Full Fetch

Fetch full text only for:

- top research candidates
- top podcast candidates
- domain-application candidates selected by quota
- memory-followup candidates

Usually 8-15 items.

### Stage 4: Review

Run substantive review jobs only on the fetched shortlist.

Review outputs should remain compact:

- one-line claim
- what they tested
- strongest point
- weakest point
- missing baselines
- missing ablations
- red flags
- positive signals
- scores
- verdict

### Stage 5: Memory Grounding

Before dossier generation, retrieve 3-8 relevant memory notes:

- same topic
- same benchmark
- same lab
- same method family
- same domain workflow
- repeated red flag

The source dossier should say when a new paper matches a prior pattern.

### Stage 6: Episode Packaging

Build 1-4 episode folders.

Each episode should include:

- controlling dossier
- selected original sources
- relevant memory notes
- upload/handoff instructions

### Stage 7: NotebookLM Audio

NotebookLM receives the smallest sufficient source set:

- always the episode dossier
- one or two original papers/blogs when needed
- memory notes when they materially ground comparisons

Do not upload raw review JSON unless debugging. The dossier should synthesize the important critique.

## First Implementation Priorities

### Next Small Step

Memory-aware daily runs are now in place. The next small step is an applied-domain LLM lane that still uses the current production flow after candidate selection.

1. Define an `applied_domain_llm_roundup` episode type.
2. Add domain-category arXiv query presets.
3. Add LLM/foundation-model keyword filtering or scoring.
4. Add domain-use-case criteria to triage/review prompts.
5. Run one explicit applied-domain episode before adding more source systems.

This gives broader coverage while keeping the deep-review budget fixed.

### Then Add Source Expansion

1. Add HF papers as a candidate source.
2. Add lab blog records as a candidate source.
3. Add broader non-arXiv domain indexes when arXiv applied runs show the shape of the demand.
4. Add source quotas to daily selection.

### Then Add Better Planning

1. Generate multiple episode candidates.
2. Choose one production episode by default.
3. Keep the others as backlog.
4. Add weekly digest generation.

## Concrete Roadmap

### Milestone 1: Memory-Aware Daily Run

Goal: today's dossier can cite yesterday's conclusions.

Status: complete for the lightweight version.

Implemented:

- per-episode `memory_note.md`
- durable cards under `data/memory/cards/`
- `data/memory/vocab.json`
- promote-memory job after dossier generation
- tag/alias card retrieval plus recent working-memory context
- validation for memory updates and handoffs

### Milestone 2: Applied Domain Lane

Goal: find practical LLM/foundation-model applications outside core ML without adding a whole multi-source platform yet.

Work:

- define domain presets and tags
- implement arXiv domain category queries
- add LLM/foundation-model keyword filtering
- add applied-domain triage criteria
- test one domain run, probably bio/medicine or robotics first
- keep review count around 10 papers

### Milestone 3: Wider Candidate Funnel

Goal: stop relying only on recent arXiv pulls.

Work:

- add candidate source type field beyond arXiv
- implement HF trending ingest
- implement lab blog ingest
- merge/dedupe candidate batches
- add source-signal-aware triage prompt

### Milestone 4: Portfolio Selection

Goal: reduce sampling bias while staying cheap.

Work:

- add candidate quotas by source lane
- add rotating domain lane
- add wildcard sampling
- select full-review shortlist from the portfolio

### Milestone 5: Weekly Memory Products

Goal: make the KB itself produce episodes.

Work:

- weekly digest dossier
- recurring red flags report
- topic trajectory report
- "papers that changed our mind" tracker

## Opinionated Choices

### Do Not Parse 100 Full Papers

Parse 100 abstracts if useful. Fully parse 10-15 papers. Deep review maybe 8-10. Package 1-4 episodes.

### Do Not Chase Neutrality

The show should be fair, but it should have a point of view. The value is not neutral summarization. The value is claim-versus-evidence pressure.

### Do Not Let Popularity Decide

HF and lab blogs are salience streams. They are not quality filters.

### Do Not Let Domain Papers Become Token Variety

Applied papers need domain-grounded review criteria. A biology paper should be judged partly on biological validation, not only ML novelty.

### Keep NotebookLM As Renderer

NotebookLM is good at producing listenable conversation from sources. Paper Radio should decide what sources, what critique, what comparisons, and what memory context get uploaded.

## Near-Term Decision

The memory-first decision is now resolved. The next product decision is which expansion lane comes first.

Current recommendation: **applied-domain arXiv lane first, then HF/lab/multi-source expansion.**

Reason: applied-domain arXiv lets us test the new editorial direction while reusing the current machinery. HF and lab blogs add useful salience, but also add popularity and prestige bias. Domain-use-case papers force us to build better selection and review criteria without yet building a broad source-ingestion platform.

After applied-domain runs work, add HF and lab blogs. Then add broader domain indexes and portfolio quotas.

## Success Criteria

After 30 days, the system should answer:

- What topics keep recurring?
- Which claims are genuinely new versus recycled?
- Which benchmarks are getting stale?
- Which labs or authors are reliable?
- Which source lanes produce the best episodes?
- Which papers looked good in isolation but weak in comparison?
- Which applied domains are producing real LLM use, not just demos?

If we can answer those, Paper Radio becomes more than a feed. It becomes a personal research memory system that happens to produce a very good daily podcast.
