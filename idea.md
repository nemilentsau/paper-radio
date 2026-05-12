Yes. This is buildable, and the target should not be “find the best papers.” The target should be:

**produce 3 hours/day of high-yield audio from a ranked paper queue, with enough variety that even bad papers are entertaining because they get dismantled.**

That is a much better design problem.

A few constraints from the tooling side matter. NotebookLM’s Audio Overviews are designed exactly for “turn a source set into a conversational audio summary,” and Google has expanded them broadly, including support for many languages and a Studio workflow for generating/managing outputs. ([blog.google][1]) arXiv gives you official RSS and API-style intake, and its public announcement schedule is predictable enough that you can automate a morning ingest around it. ([arXiv Blog][2]) Hugging Face papers gives you daily, weekly, and monthly community-trending views, which is useful as one signal but should stay only one signal. ([Hugging Face][3])

Here is the system I would build.

## The real architecture

You want **four layers**:

1. **Ingest**
2. **Triage and scoring**
3. **Knowledge base + clustering**
4. **Audio packaging**

Do not send raw daily papers straight into NotebookLM. That creates random sludge. Instead, make NotebookLM the **last mile audio renderer**, not the brain of the pipeline.

## 1) Ingest: create a daily candidate pool

Each morning, auto-pull from:

* arXiv RSS/API for the categories you actually care about, probably a narrow slice like `cs.LG`, `cs.CL`, maybe `cs.AI` depending on tolerance for fluff. arXiv’s RSS and API are official and stable enough for this intake job. ([arXiv Blog][2])
* Hugging Face daily/weekly/monthly papers as a popularity signal, not a quality signal. ([Hugging Face][3])
* Optional: selected labs or authors you trust, as a whitelist stream.

The first key move: **do not ingest everything equally**. Tag each paper with source signals:

* appeared on arXiv only
* appeared on HF daily
* appeared on HF weekly/monthly
* from trusted lab / author
* has code
* has benchmark tables
* is a survey / methods / eval / systems / theory paper

That already helps later ranking.

## 2) Triage: score for “audio worthiness,” not just scientific quality

This is the part that changes everything.

You do **not** only want 9/10 papers. You want a mix:

* a few genuinely strong papers
* a few flawed-but-interesting papers
* maybe one complete trainwreck that is fun to destroy

That gives you better listening.

So each paper gets two scores:

### A. Research quality score

Things like:

* baseline recency
* ablations
* benchmark leakage risk
* claim/evidence match
* model choice sanity
* code / reproducibility
* breadth of validation

### B. Podcast value score

Things like:

* strong central idea
* high controversy / overclaim potential
* easy-to-explain failure modes
* relevance to your interests
* contrast with prior work
* likely to produce a good argument

This matters because a 4/10 paper can still be an 8/10 podcast.

So your pipeline should not discard everything weak. It should sort papers into buckets:

* **Keep: strong**
* **Keep: flawed but interesting**
* **Discard: boring and weak**
* **Discard: unreadable incremental sludge**

That is the key distinction.

## 3) Knowledge base: store the paper as structured objects, not just PDFs

Build a simple database. SQLite is enough to start.

For each paper store:

* title
* abstract
* authors
* date
* arXiv category
* links
* source signals
* paper family/topic
* summary
* critique
* red flags
* positive contributions
* scores
* “podcast angles”
* related prior papers
* verdict

Then add a **topic graph** on top:

* PEFT / finetuning
* inference-time compute
* multimodal OCR
* synthetic data
* evals / benchmarks
* retrieval / RAG
* RL / agents
* systems

Why this matters: once you store papers as structured objects, you can generate podcasts that are not just “one paper summary.” You can generate:

* **3-paper comparison episodes**
* **one good + one bad paper showdown**
* **theme episodes** like “Why so many PEFT papers have bullshit baselines”
* **weekly state of the field**
* **graveyard episodes** for papers that look exciting but collapse under inspection

That gives you far more audio than raw single-paper summaries.

## 4) Audio packaging: turn ranked clusters into daily episodes

This is where NotebookLM shines.

NotebookLM Audio Overviews are source-grounded audio conversations rather than generic TTS summaries, and that makes them useful for your workout use case. ([blog.google][1])

Instead of one notebook per paper, I would generate **three daily notebooks**:

### Episode 1: strongest paper of the day

One paper, plus maybe one related baseline/reference paper.

### Episode 2: flawed but interesting cluster

Two or three papers on the same topic, with your critique notes added as sources.

### Episode 3: theme/meta episode

A generated briefing doc based on that day’s papers:

* common failure modes
* what actually seems real
* what looks like benchmark theater

That should get you roughly:

* 30–45 min
* 30–45 min
* 30–45 min

Then add a fourth, lower-effort episode if needed:

### Episode 4: “garbage fire of the day”

One hilariously overclaimed paper plus a critique memo.

That gets you close to your 3-hour target.

## The important trick: inject your own critique as a first-class source

Do not rely on NotebookLM or Claude to infer your stance fresh every time.

For each paper, your pipeline should generate a short **review memo** like:

* what the paper claims
* what the evidence actually supports
* strongest point
* weakest point
* missing baseline
* overclaim rating
* final score

Then upload **both the paper and the memo** into the notebook.

That way the podcast is anchored not just in the paper’s self-description, but in your adversarial framing too. Since Google explicitly notes Audio Overviews reflect the provided sources rather than being comprehensive or objective, feeding in your critique memo is exactly how you bend the output toward something useful. ([blog.google][1])

## The daily content formula I would use

For 3 hours/day, I would not do “4 random papers.”

I would do:

* **1 anchor episode**: one of the best recent papers
* **1 adversarial episode**: one or two weak papers with sharp critique
* **1 cluster episode**: three papers on the same topic compared against each other
* **1 meta episode every few days**: “what this week says about the field”

That makes the listening feel cumulative instead of like isolated paper blurbs.

## How Claude should be used

Claude should not be your raw paper reader only. It should be the **critic + curator + scriptwriter**.

Morning pipeline:

1. Ingest papers
2. Claude does short triage
3. Claude writes a compact critique memo for survivors
4. Claude assigns topic tags and episode candidates
5. Claude generates notebook-ready source docs:

   * one-page summary
   * one-page critique
   * one-page comparison note if clustered

Then NotebookLM turns those source bundles into audio.

That way Claude is doing the judgment work, and NotebookLM is doing the listening-format conversion.

## Scoring rubric I would actually use

Make it dead simple.

For each paper, 1–5 on:

* idea novelty
* empirical rigor
* baseline quality
* ablation quality
* evaluation cleanliness
* relevance to your interests
* podcast value

Then compute:

* **research score**
* **podcast score**

Selection rule:

* high research + high podcast → anchor episode
* low research + high podcast → adversarial episode
* medium research + high topical overlap → cluster episode
* low research + low podcast → discard

This solves your real problem: you need content, not just excellence.

## What the knowledge base should accumulate over time

After a month, this becomes much more powerful.

You will not just have papers. You will have:

* recurring red flags by topic
* labs/authors that consistently oversell
* labs/authors worth prioritizing
* benchmark families that are chronically weak
* model families that papers abuse as stale baselines
* your own map of where the field is actually moving

At that point, you can generate episodes like:

* “Top 5 fake-looking PEFT improvements this month”
* “Three multimodal parsing papers that actually differ”
* “Why this benchmark is becoming useless”
* “What recent RL-for-agents papers get wrong”

That is much richer than daily HF trending.

## My blunt recommendation

Do **not** build a “paper ranking system.”

Build a **research radio station** with four queues:

* **best**
* **interesting but flawed**
* **same-topic comparison**
* **garbage fire**

That matches your workout use case far better.

Because you do not actually need 3 hours of pristine science every day. Nobody does. You need 3 hours of **intellectually stimulating material**. Bad papers with good criticism absolutely count.

## Minimal first version

Version 1 can be very small:

* arXiv + HF ingest every morning ([arXiv Blog][2])
* Claude triage into scores/tags
* generate one markdown memo per selected paper
* store in a local folder or SQLite
* create 3 NotebookLM notebooks/day from bundles of paper PDFs + memos
* listen during workout

That is enough to validate the workflow.

## Version 2

Once it works, add:

* topic clustering
* “compare against previous month” memory
* author/lab priors
* automatic episode planning
* skip papers too similar to ones already covered

That is where it turns from feed consumption into a real knowledge base.

The key insight is this:

**Your output unit is not a paper. It is an episode.**
Once you design around episodes, the whole pipeline becomes obvious.

I can sketch the exact schema and daily job flow next: tables, scoring fields, folder structure, and the prompts for Claude/Cowork.

[1]: https://blog.google/innovation-and-ai/products/notebooklm-audio-overviews/?utm_source=chatgpt.com "NotebookLM now lets you listen to a conversation about ..."
[2]: https://blog.arxiv.org/2024/01/31/attention-arxiv-users-re-implemented-rss/?utm_source=chatgpt.com "Attention arXiv users: Re-implemented RSS"
[3]: https://huggingface.co/papers/trending?utm_source=chatgpt.com "Trending Papers"



Here is a concrete version that is actually buildable.

## Goal

Every morning, automatically turn the paper firehose into:

* a ranked knowledge base
* a set of short critique memos
* 3–4 NotebookLM-ready source bundles
* about 2–3 hours of audio

The unit of production is **an episode**, not a paper.

---

# 1. System shape

Use five stages:

1. **Ingest**
   Pull candidate papers from arXiv + HF trending + optional whitelists.

2. **Normalize**
   Store metadata, dedupe, assign IDs, fetch PDFs.

3. **Triage**
   Claude/Cowork scores papers for research quality and podcast value.

4. **Package**
   Build source bundles for NotebookLM:

   * paper PDF
   * summary memo
   * critique memo
   * comparison memo if clustered

5. **Archive + Learn**
   Save everything into a structured KB so future episodes can compare against past papers.

---

# 2. What to store

Do not just store PDFs. Store **paper objects** plus **review objects** plus **episode objects**.

## Core entities

### Paper

This is the raw thing you ingest.

Suggested fields:

```json
{
  "paper_id": "2026-04-10-arxiv-2604.01694",
  "title": "MiCA Learns More Knowledge Than LoRA and Full Fine-Tuning",
  "authors": ["Sten Rüdiger", "Sebastian Raschka"],
  "abstract": "...",
  "pdf_url": "...",
  "arxiv_id": "2604.01694",
  "source_types": ["arxiv", "hf_daily"],
  "published_at": "2026-04-03",
  "categories": ["cs.LG"],
  "code_url": null,
  "model_families": ["Llama-2", "Qwen2.5"],
  "task_tags": ["peft", "finetuning", "knowledge-injection"],
  "status": "ingested"
}
```

### Review

This is Claude’s judgment.

```json
{
  "review_id": "review-2026-04-10-arxiv-2604.01694",
  "paper_id": "2026-04-10-arxiv-2604.01694",
  "one_line_claim": "Adapting minor singular directions beats LoRA for knowledge injection.",
  "what_they_tested": "7B models, synthetic MCQ evals, custom history corpus",
  "strongest_point": "Minor-vs-major-vs-random ablation",
  "weakest_point": "Narrow eval and stale model choices",
  "missing_baselines": ["Qwen3", "Gemma"],
  "red_flags": [
    "claim-evidence mismatch",
    "stale baselines",
    "synthetic benchmark loop"
  ],
  "positive_signals": [
    "clear central hypothesis",
    "some ablation effort"
  ],
  "research_score": 4.5,
  "podcast_score": 8.0,
  "overclaim_score": 8.5,
  "replication_interest": 6.0,
  "verdict": "flawed_but_interesting"
}
```

### Episode candidate

This is how papers become audio.

```json
{
  "episode_candidate_id": "epcand-2026-04-10-01",
  "episode_type": "flawed_but_interesting",
  "paper_ids": [
    "2026-04-10-arxiv-2604.01694",
    "2026-04-10-arxiv-xxxx.xxxxx"
  ],
  "theme": "PEFT papers with weak baseline selection",
  "hook": "Interesting idea, weak evidence, suspicious model choices",
  "estimated_audio_minutes": 40
}
```

### Episode

This tracks what actually got packaged and listened to.

```json
{
  "episode_id": "episode-2026-04-10-02",
  "episode_type": "comparison",
  "title": "Three PEFT papers and which one survives contact with reality",
  "paper_ids": [
    "2026-04-10-arxiv-2604.01694",
    "2026-04-09-arxiv-xxxx.xxxxx",
    "2026-04-08-arxiv-xxxx.xxxxx"
  ],
  "bundle_path": "episodes/2026-04-10/02_peft_comparison/",
  "notebooklm_status": "ready",
  "runtime_minutes": null,
  "listened": false
}
```

---

# 3. Scoring system

You need two scores, not one.

## A. Research score

How good is the paper?

Rate 1–10 on:

* novelty
* baseline quality
* ablation quality
* benchmark cleanliness
* breadth of validation
* reproducibility
* claim/evidence alignment

Then combine with weights like:

```text
research_score =
0.15 * novelty +
0.20 * baseline_quality +
0.15 * ablation_quality +
0.15 * benchmark_cleanliness +
0.10 * breadth +
0.10 * reproducibility +
0.15 * claim_evidence_alignment
```

## B. Podcast score

How good is it as listening material?

Rate 1–10 on:

* clarity of central idea
* amount of controversy
* ease of critique
* relevance to your interests
* compare/contrast potential
* likely entertainment value

Then:

```text
podcast_score =
0.15 * idea_clarity +
0.20 * controversy +
0.15 * critiqueability +
0.20 * relevance +
0.15 * comparison_value +
0.15 * entertainment_value
```

## C. Verdict buckets

Use simple thresholds:

* **8–10 research**: strong

* **5–8 research**: mixed

* **<5 research**: weak

* **8–10 podcast**: definitely keep

* **5–8 podcast**: maybe keep

* **<5 podcast**: discard

Then classify:

* high research + high podcast → `anchor`
* low/mid research + high podcast → `flawed_but_interesting`
* medium research + medium/high topical overlap → `comparison`
* low research + low podcast → `discard`

---

# 4. Folder structure

Keep it stupidly simple.

```text
paper_radio/
  data/
    raw/
      metadata/
      pdfs/
    processed/
      papers/
      reviews/
      episodes/
  prompts/
    triage_prompt.md
    full_review_prompt.md
    comparison_prompt.md
    weekly_digest_prompt.md
  notebooks/
    daily/
      2026-04-10/
        episode_01_anchor/
        episode_02_flawed/
        episode_03_comparison/
        episode_04_garbage_fire/
  exports/
    notebooklm_ready/
    podcast_scripts/
  db/
    papers.db
  scripts/
    ingest_arxiv.py
    ingest_hf.py
    dedupe.py
    triage.py
    cluster.py
    build_episode_bundles.py
    weekly_digest.py
```

---

# 5. Database schema

SQLite is enough.

## `papers`

```sql
CREATE TABLE papers (
    paper_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    abstract TEXT,
    authors_json TEXT,
    arxiv_id TEXT,
    pdf_url TEXT,
    code_url TEXT,
    published_at TEXT,
    categories_json TEXT,
    source_types_json TEXT,
    task_tags_json TEXT,
    model_families_json TEXT,
    status TEXT
);
```

## `reviews`

```sql
CREATE TABLE reviews (
    review_id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL,
    one_line_claim TEXT,
    what_they_tested TEXT,
    strongest_point TEXT,
    weakest_point TEXT,
    missing_baselines_json TEXT,
    red_flags_json TEXT,
    positive_signals_json TEXT,
    research_score REAL,
    podcast_score REAL,
    overclaim_score REAL,
    replication_interest REAL,
    verdict TEXT,
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
);
```

## `episodes`

```sql
CREATE TABLE episodes (
    episode_id TEXT PRIMARY KEY,
    episode_type TEXT,
    title TEXT,
    theme TEXT,
    paper_ids_json TEXT,
    bundle_path TEXT,
    notebooklm_status TEXT,
    runtime_minutes REAL,
    listened INTEGER DEFAULT 0
);
```

## `paper_links`

For similarity / lineage / follow-up relationships.

```sql
CREATE TABLE paper_links (
    src_paper_id TEXT,
    dst_paper_id TEXT,
    relation_type TEXT,
    strength REAL
);
```

Relation types:

* `same_topic`
* `same_claim_family`
* `baseline_for`
* `contradicts`
* `followup_to`

---

# 6. Daily flow

Here is the daily job sequence.

## 6:00 AM — ingest

Pull:

* recent arXiv papers from selected categories
* HF daily + weekly + monthly trending
* optionally whitelisted labs/authors

For each paper:

* dedupe by arXiv ID/title
* download PDF
* extract metadata
* assign coarse tags

## 6:15 AM — fast triage

Claude sees only:

* title
* abstract
* intro
* experiment tables if extracted
* maybe conclusion

Claude returns:

* topic
* likely red flags
* likely missing baselines
* estimated relevance
* keep/discard

This should be cheap and fast.

## 6:30 AM — full review on survivors

Run full critique only on:

* top relevance papers
* top controversy papers
* papers in themes you care about

Claude writes:

* summary memo
* critique memo
* red flags
* verdict
* episode type suggestions

## 7:00 AM — clustering

Group by:

* PEFT
* OCR/layout parsing
* agent evals
* RL
* retrieval
* synthetic data
* benchmark papers
* systems

Then make episode candidates.

## 7:15 AM — episode packaging

Generate 3–4 bundles:

* anchor
* flawed but interesting
* comparison
* garbage fire if available

Each bundle contains:

* PDF(s)
* summary memo(s)
* critique memo(s)
* episode briefing doc

## 7:30 AM — NotebookLM ingest

Either manual or semi-automated:

* create notebook
* upload bundle
* generate audio overview

If full automation into NotebookLM is awkward, that is fine. The valuable part is already done.

---

# 7. Bundle contents for NotebookLM

Each episode folder should contain a small set of files.

## Example: `episode_02_flawed/`

```text
episode_02_flawed/
  01_paper_main.pdf
  02_summary_main.md
  03_critique_main.md
  04_context_note.md
  05_episode_brief.md
```

## `02_summary_main.md`

Keep it short:

```markdown
# Summary

## Claim
The paper claims X.

## Method
They do Y.

## Evidence
They evaluate on Z.

## Why it matters
Could matter because ...
```

## `03_critique_main.md`

```markdown
# Critique

## Strongest point
...

## Weakest point
...

## Missing baselines
...

## Overclaim risk
...

## Final verdict
Interesting but weak evidence.
```

## `05_episode_brief.md`

This is the key file.

```markdown
# Episode Brief

This episode should focus on:
- what the paper is trying to do
- what is actually interesting
- why the evaluation is weaker than the title suggests
- what better baselines would have looked like
- whether the result is likely old-model-specific

Tone:
Critical, concrete, not polite.

Target:
~40 minutes of audio with back-and-forth discussion.

Do not just summarize the paper. Compare claim vs evidence.
```

That file strongly shapes the resulting audio.

---

# 8. Claude prompts

## A. Fast triage prompt

Use this on many papers.

```markdown
You are triaging a recent ML paper for whether it deserves a full critique and whether it would make a good podcast episode.

Read only enough to answer:

1. What is the core claim?
2. What did they actually test?
3. What are the 2 biggest red flags?
4. What is the most obvious missing baseline or ablation?
5. Is this:
   - strong
   - mixed but interesting
   - weak but entertaining
   - discard
6. Score:
   - research quality: 1-10
   - podcast value: 1-10

Be concise and skeptical. Prefer concrete methodological criticism over vague praise.
```

## B. Full review prompt

```markdown
Critically review this paper.

Return the following sections:

## One-sentence claim
## What they actually did
## Strongest point
## Weakest point
## Missing baselines
## Missing ablations
## Risk of benchmark leakage or synthetic overfitting
## Whether the title/abstract overclaim
## Final verdict
## Scores
- research_score: 1-10
- podcast_score: 1-10
- overclaim_score: 1-10
- replication_interest: 1-10

Be hostile-but-fair. Do not reward polish. Reward rigor.
```

## C. Comparison prompt

```markdown
Compare these papers as if deciding which one survives serious scrutiny.

For each paper:
- core claim
- strongest evidence
- biggest weakness
- whether the baselines are current
- whether the evaluation actually tests the claim

Then produce:
- ranking from most credible to least credible
- common pathology across the set
- what a serious follow-up paper would do differently
```

## D. Episode-planning prompt

```markdown
You are planning workout podcast episodes from reviewed ML papers.

Given these reviewed papers, create 4 episode candidates:
1. strongest paper
2. flawed but interesting
3. topic comparison
4. garbage fire

For each:
- title
- theme
- included papers
- why it will be good listening
- expected runtime (30-45 min)
```

---

# 9. Topic taxonomy

This matters more than people think. Without tags the KB becomes junk.

Use a controlled tag set.

## Method tags

* peft
* finetuning
* instruction-tuning
* rl
* inference-time-compute
* retrieval
* multimodal
* ocr
* synthetic-data
* benchmark
* systems
* agents
* memory
* quantization
* distillation

## Quality tags

* stale-baselines
* weak-ablation
* synthetic-eval-loop
* claim-evidence-mismatch
* benchmark-theater
* tiny-model-generalization
* hidden-extra-trick
* underpowered-comparison
* irreproducible
* good-negative-result

## Podcast tags

* fun-destruction
* serious-contender
* weird-idea
* replication-worthy
* overclaim-fest
* compare-this
* field-diagnostic

These tags are gold later.

---

# 10. Episode templates

You need consistent formats.

## Anchor episode

One strong paper.

Template:

* what problem it tackles
* why it matters
* what they did
* what evidence is convincing
* what still remains weak
* whether it is worth following

## Flawed but interesting

One paper with a real idea and weak evidence.

Template:

* idea is interesting
* experiments are weak
* exactly where it overclaims
* what a real test would look like

## Comparison episode

2–3 papers on one topic.

Template:

* common goal
* how methods differ
* who used honest baselines
* who did benchmark theater
* which one is most worth remembering

## Garbage fire

One paper that is mostly bad but revealing.

Template:

* why people found it exciting
* why it collapses under inspection
* what pathology it illustrates about the field

---

# 11. How to get 3 hours/day reliably

You do not need 5 amazing papers every day. You need enough episode material.

A good daily mix:

* 1 anchor episode = 35–45 min
* 1 flawed but interesting = 35–45 min
* 1 comparison = 40–50 min
* 1 garbage fire or meta = 30–40 min

That is 140–180 minutes.

If a day is weak, fill with:

* weekly roundup
* “recurring pathology” episode
* revisit older paper after related new paper appears
* one replication-design episode

So the KB should support not just new papers, but **meta content**.

---

# 12. Weekly layer

This is where the KB starts compounding.

Every Friday, generate:

## Weekly digest

* top 3 credible papers
* top 3 overclaimed papers
* one recurring failure mode
* one topic to watch next week

## Monthly field memo

By topic:

* where signal is real
* where hype is strongest
* which benchmarks are becoming useless
* which model families are being abused as stale baselines

This creates reusable audio on slow days.

---

# 13. Minimal v1 implementation

Do not overbuild.

## v1 stack

* Python scripts
* SQLite
* local markdown files
* Claude/Cowork for triage/review
* NotebookLM for audio

## v1 outputs

* `papers.db`
* downloaded PDFs
* one review markdown per kept paper
* 3 episode folders per day

That is enough.

---

# 14. v2 improvements

Only add these after v1 works:

* embedding-based topic clustering
* author/lab quality priors
* novelty detection against your existing KB
* skip-near-duplicates
* automatic episode length balancing
* “paper lineage” view
* “papers that looked good but aged badly” tracker

---

# 15. One practical warning

Do not let Claude write long generic summaries.

Force it to produce compact, structured memos. Otherwise your source bundles become bloated sludge and NotebookLM will drift into polite summarization instead of real critique.

Your memo files should be sharp, short, and opinionated.

Think:

* 300–700 words summary
* 400–900 words critique
* 300–700 words comparison note

Not essays.

---

# 16. Recommended daily operating rule

Use this exact selection logic:

* keep any paper with `research_score >= 7`
* keep any paper with `podcast_score >= 7`
* discard papers with both `< 5`
* cluster papers with shared topic tags
* guarantee at least:

  * one strong or mixed-serious paper
  * one flawed but interesting paper
  * one comparison/meta episode

That will keep the feed useful even on trash days.

---

# 17. What success looks like

After 30 days, your KB should let you ask things like:

* show me PEFT papers with stale baselines
* give me multimodal parsing papers worth replication
* which labs most often overclaim
* what topics produce the best workout episodes
* what papers looked good at first but failed comparison later

That is when it becomes a real system instead of a pile of summaries.

---

# 18. My recommendation for first build order

Build in this order:

1. SQLite schema
2. ingest scripts
3. triage prompt
4. review prompt
5. daily episode folder generator
6. manual NotebookLM upload
7. weekly digest

Do not start with clustering or embeddings. You do not need them yet.

---

If you want, next I can turn this into a very concrete **implementation spec** with:

* exact SQLite schema file
* Python dataclasses / Pydantic models
* folder/file naming conventions
* daily cron job sequence
* and the exact markdown templates for each memo type.
