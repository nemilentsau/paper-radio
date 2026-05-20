# A Methodology for Selecting and Composing Runtime Architecture Patterns for Production LLM Agents

## Metadata
- Paper ID: arxiv-2605.20173
- Source: arxiv
- Source ID: 2605.20173
- Authors: Vasundra Srinivasan
- Published: 2026-05-19T17:54:21Z
- Updated: 2026-05-19T17:54:21Z
- Categories: cs.AI, cs.SE
- Source signals: arxiv_recent
- Triage decision: advance_to_review
- Triage rationale: The paper is squarely about production LLM agent architecture and offers a concrete methodology, pattern catalog, and a runnable implementation, which makes it useful for both research and episode critique. It reads as more conceptual than empirically deep, but the runtime focus and failure-mode framing are strong enough to merit review.
- Research score estimate: 6.7
- Podcast score estimate: 8.3
- Local PDF path: data/papers/pdfs/arxiv-2605.20173.pdf
- Full text path: data/papers/fulltext/arxiv-2605.20173.txt
- Abstract URL: https://arxiv.org/abs/2605.20173
- PDF URL: https://arxiv.org/pdf/2605.20173

## Abstract
Production LLM agents combine stochastic model outputs with deterministic software systems, yet the boundary between the two is rarely treated as a first-class architectural object. This paper names that boundary the stochastic-deterministic boundary (SDB): a four-part contract among a proposer, verifier, commit step, and reject signal that specifies how an LLM output becomes a system action. We argue that the SDB is the load-bearing primitive of production agent runtimes. Around this primitive, we organize agent runtime design into three concerns: Coordination, State, and Control. We present a catalog of six runtime patterns that compose the SDB differently across conversational, autonomous, and long-horizon agents: hierarchical delegation, scatter-gather plus saga, event-driven sequencing, shared state machine, supervisor plus gate, and human in the loop. For each pattern, we trace its lineage to distributed-systems concepts and identify what changes when the worker is stochastic. The paper contributes a five-step methodology for selecting runtime patterns, a diagnostic procedure that maps production failures to pattern weaknesses, and a failure mode called replay divergence, in which LLM-based consumers of a deterministic event log produce different downstream outputs under model-version or prompt changes. A stylized reliability decomposition separates per-call model variance from architectural momentum, motivating the claim that as model variance decreases, pattern choice and SDB strength become increasingly important levers for long-run reliability. We apply the methodology to five workloads and provide one runnable reference implementation for a 90-day contract-renewal agent.
