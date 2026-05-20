# Neurosymbolic Learning for Inference-Time Argumentation

## Metadata
- Paper ID: arxiv-2605.20098
- Source: arxiv
- Source ID: 2605.20098
- Authors: Gabriel Freedman, Adam Dejl, Adam Gould, Mansi, Lihu Chen, Jianqi Jiang, Francesca Toni
- Published: 2026-05-19T16:49:29Z
- Updated: 2026-05-19T16:49:29Z
- Categories: cs.AI
- Source signals: arxiv_applied_domain, applied_domain:finance_modeling
- Triage decision: queue_for_review
- Triage rationale: This looks methodologically interesting because it couples explicit argumentative structure with trainable LLM behavior and evaluates ternary verification rather than simple binary classification. I would not advance it directly from the abstract alone because the domain signal is still generic claim verification with only weak evidence of a concrete finance workflow or strong real-world validation.
- Research score estimate: 6.2
- Podcast score estimate: 7.4
- Local PDF path: data/papers/pdfs/arxiv-2605.20098.pdf
- Full text path: data/papers/fulltext/arxiv-2605.20098.txt
- Abstract URL: https://arxiv.org/abs/2605.20098
- PDF URL: https://arxiv.org/pdf/2605.20098

## Abstract
Claim verification is an important problem in high-stakes settings, including health and finance. When information underpinning claims is incomplete or conflicting, uncertain answers may be more appropriate than binary true or false classifications. In all cases, faithful explanations of the considerations determining the final verdict are crucial. We introduce inference-time argumentation (ITA), a trainable neurosymbolic framework for ternary claim verification in which a formal argumentation semantics giving the strength of claims is used both (i) to guide LLM training as models learn to generate arguments and assign them base scores (representing intrinsic strengths) and (ii) to compute ternary (true/false/uncertain) predictions from generated, scored arguments. As a result, at training time, argument generation and scoring can be optimised according to the quality of the induced argumentative predictions. Moreover, at inference time, the final prediction is faithful, by construction, to the arguments and scores determining the verdict, rather than being justified by a potentially unfaithful post-hoc reasoning trace as in conventional reasoning models. We finally show that, on two datasets for ternary claim verification, ITA improves upon argumentative baselines and can perform competitively against non-argumentative direct-prediction baselines, while providing verdicts that are computed deterministically from explicit, inspectable argumentative structures.
