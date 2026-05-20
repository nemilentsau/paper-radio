# Applied Domain LLM Plan

## Goal

Add an applied-domain lane for papers where LLMs or foundation models are used inside practical domain workflows.

This is not a general "more papers" expansion. The goal is to find papers where the interesting question is:

**Does the model help with a real domain task, under validation that would matter to domain experts?**

The first version should stay arXiv-only and reuse the existing Paper Radio pipeline after candidate selection.

## Why This Comes Next

The memory-aware daily run now works. Before adding Hugging Face trends, lab blogs, PubMed, OpenAlex, or other source systems, we should test whether Paper Radio can evaluate applied LLM use cases with better domain-specific judgment.

This gives us broader coverage without increasing deep-review cost or building a multi-source discovery platform too early.

## First Episode Type

Use a new episode type:

```text
applied_domain_llm_roundup
```

The first applied episode should probably focus on one broad domain family:

```text
bio / medicine / scientific workflows
```

Reasons:

- lots of current LLM activity
- concrete stakes and failure modes
- natural link to the existing `active-evidence-acquisition` memory card
- useful distinction between benchmark gains and workflow usefulness

## Core Selection Question

For each candidate, ask:

```text
Is the LLM or foundation model part of a real domain workflow, or is this just a generic benchmark with domain vocabulary?
```

Good applied-domain candidates usually involve at least one of:

- retrieval or search over domain evidence
- extraction from domain documents or records
- multimodal perception in a domain setting
- decision support
- planning or protocol generation
- simulation, analysis, or workflow control
- hypothesis generation or literature synthesis
- human expert collaboration

Weak candidates often look like:

- "we prompted GPT on a benchmark"
- no domain expert baseline
- no realistic deployment point
- no leakage analysis
- no safety/error analysis
- domain labels but generic ML validation

## Initial Domain Buckets

Start with one or two buckets, not all of them.

### Bio, Medicine, Clinical

Candidate categories:

- `q-bio.*`
- `cs.CL`
- `cs.AI`
- `cs.CV`
- `stat.ML`

Useful keywords:

- `large language model`
- `LLM`
- `clinical`
- `EHR`
- `medical`
- `radiology`
- `biomedical`
- `agent`
- `RAG`
- `retrieval`
- `foundation model`
- `multimodal`

### Chemistry And Materials

Candidate categories:

- `physics.chem-ph`
- `cond-mat.mtrl-sci`
- `cs.LG`
- `stat.ML`

Useful keywords:

- `large language model`
- `LLM`
- `molecule`
- `materials`
- `chemistry`
- `reaction`
- `synthesis`
- `lab`
- `agent`
- `foundation model`

### Finance And Economic Modeling

Candidate categories:

- `q-fin.*`
- `econ.*`
- `cs.AI`
- `stat.ML`

Useful keywords:

- `large language model`
- `LLM`
- `financial`
- `finance`
- `forecasting`
- `portfolio`
- `risk`
- `market`
- `backtesting`
- `economic`
- `econometric`
- `agent`

### Scientific Literature And Discovery

Candidate categories:

- `cs.CL`
- `cs.AI`
- `cs.IR`
- `stat.ML`
- `q-bio.QM`

Useful keywords:

- `large language model`
- `LLM`
- `scientific discovery`
- `literature review`
- `hypothesis generation`
- `evidence synthesis`
- `knowledge discovery`
- `research agent`
- `retrieval`
- `RAG`

## V1 Discovery Strategy

Keep discovery simple.

1. Pull a larger arXiv candidate batch from selected domain categories.
2. Apply LLM/foundation-model keyword scoring.
3. Keep the top candidate pool for triage.
4. Triage cheaply from title, abstract, category, source signals, and memory overlap.
5. Promote around 10 papers into one episode.
6. Run the existing production pipeline unchanged:
   - fetch sources
   - review records
   - dossier
   - NotebookLM bundle
   - memory note
   - promote-memory

Do not fetch and parse every candidate PDF.

## Candidate Scoring Signals

Triage should score applied candidates on:

- domain workflow concreteness
- domain validation quality
- relevance to current Paper Radio memory cards
- practical stakes
- quality of baselines
- evidence of real users, experts, or deployment setting
- likely critique value
- podcast value

Negative signals:

- only prompt engineering
- only synthetic tasks
- no expert baseline
- no uncertainty/error analysis
- no domain-specific validation
- possible data leakage
- benchmark-only framing
- broad deployment claims from narrow evidence

## Review Prompt Additions

Applied-domain review records should still use the existing review schema, but the prompt should ask the reviewer to address:

- What is the domain workflow?
- Who is the implied user?
- What decision, action, or scientific step does the model affect?
- Is the model doing retrieval, extraction, planning, perception, generation, or decision support?
- What is the domain baseline?
- Is there an expert or prior-system comparison?
- Is validation prospective, retrospective, simulated, benchmark-only, or human-adjudicated?
- Could the model be using privileged evidence, leakage, or benchmark artifacts?
- What would a domain expert find missing?
- What failure would matter in the real workflow?

## Episode Shape

The first applied-domain episode should not try to be a complete field survey.

Good first episode structure:

1. One anchor paper with a concrete workflow.
2. Two to four comparison papers around similar workflows.
3. One flawed-but-interesting paper that exposes a recurring applied-domain problem.
4. One meta segment about validation standards.

Possible episode thesis:

```text
LLMs look most useful in applied domains when they improve evidence access, workflow control, or expert productivity, but the evidence often collapses if validation is only retrospective, benchmark-style, or tool-privileged.
```

## Memory Promotion Opportunities

Applied-domain runs should create durable memory only when the lesson is reusable.

Likely durable card themes:

- `clinical-evidence-access`
- `domain-validation`
- `privileged-evidence`
- `retrospective-leakage`
- `expert-baselines`
- `llm-as-workflow-interface`
- `scientific-agent-evaluation`

Do not promote one-off domain facts unless they change how future papers should be evaluated.

## V1 Implementation Tasks

Status: first slice implemented.

1. Add a documented applied-domain preset. Done: four presets are available.
2. Add or reuse CLI flags for domain categories and keyword filters. Done via `candidate-applied-domain`.
3. Add applied-domain triage prompt guidance. Done.
4. Add applied-domain review prompt guidance. Done.
5. Add tests for candidate filtering/scoring if new code is introduced. Done.

Next implementation step:

- wire this candidate lane into a higher-level applied-domain daily run, or
  teach `daily-run` to accept a source mode without complicating the core
  frontier-ML path.
6. Run one explicit applied-domain episode.
7. Inspect whether the selected papers are actually domain-useful.
8. Adjust categories, keywords, and prompts before adding new sources.

## Deferred

Do not build these yet:

- PubMed / Europe PMC connector
- OpenAlex or Semantic Scholar connector
- ChemRxiv connector
- HF trend merger
- lab blog ingestion
- portfolio selector across source types
- embeddings or full RAG for candidate discovery

These become useful after the arXiv applied-domain lane shows what kinds of papers we actually want.

## Success Criteria

The first applied-domain run is successful if:

- it finds papers that are not just core ML benchmarks
- the dossier identifies concrete workflows
- review records separate ML novelty from domain usefulness
- weak papers fail for domain-specific reasons, not vague quality reasons
- the episode can explain why validation matters in the domain
- memory either updates a reusable card or explicitly no-ops

The run does not need perfect coverage. It only needs to prove that Paper Radio can evaluate applied LLM use cases without losing its claim-versus-evidence discipline.
