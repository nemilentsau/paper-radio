# KoRe: Compact Knowledge Representations for Large Language Models

## Metadata
- Paper ID: arxiv-2605.20170
- Source: arxiv
- Source ID: 2605.20170
- Authors: Davide Cavicchini, Fausto Giunchiglia, Jacopo Staiano
- Published: 2026-05-19T17:53:29Z
- Updated: 2026-05-19T17:53:29Z
- Categories: cs.CL
- Source signals: arxiv_recent
- Triage decision: advance_to_review
- Triage rationale: This looks like a plausible and relevant LLM knowledge-injection paper with a concrete method and measurable efficiency claim, so it is worth review. The abstract is specific enough to suggest technical substance rather than pure hype, and the token-efficiency angle could make it useful for both research and discussion.
- Research score estimate: 7.2
- Podcast score estimate: 6.8
- Local PDF path: data/papers/pdfs/arxiv-2605.20170.pdf
- Full text path: data/papers/fulltext/arxiv-2605.20170.txt
- Abstract URL: https://arxiv.org/abs/2605.20170
- PDF URL: https://arxiv.org/pdf/2605.20170

## Abstract
Modern Large Language Models (LLMs) have shown impressive performances in user-facing tasks such as question answering, as well as consistent improvements in reasoning capabilities. Still, the way these models encode knowledge seems inherently flawed: by design, LLMs encode world-knowledge within their parameters. This way of representing knowledge is inherently opaque, difficult to debug and update, and prone to hallucinations. On the other hand, Knowledge Graphs can provide human-readable and easily editable world knowledge representations, and their application in knowledge-intensive tasks has consistently proven beneficial to downstream performance. Nonetheless, current integration techniques require extensive retraining or finetuning. To overcome this issue, we introduce KoRe, a methodology to encode 1-hop sub-graphs into compact discrete knowledge tokens and inject them into a LLM backbone. We test the proposed approach on three established benchmarks, and report competitive performances coupled with a significant reduction (up to 10x) in token usage. Our results show that compact discrete KG representations can efficiently and effectively be used to ground modern LLMs.
