# Vision-OPD: Learning to See Fine Details for Multimodal LLMs via On-Policy Self-Distillation

## Metadata
- Paper ID: arxiv-2605.18740
- Source: arxiv
- Source ID: 2605.18740
- Authors: Qianhao Yuan, Jie Lou, Xing Yu, Hongyu Lin, Le Sun, Xianpei Han, Yaojie Lu
- Published: 2026-05-18T17:57:04Z
- Updated: 2026-05-18T17:57:04Z
- Categories: cs.CV, cs.AI, cs.CL, cs.LG
- Source signals: arxiv_recent
- Triage decision: queue_for_review
- Triage rationale: The paper appears technically coherent and methodologically specific, with a clear self-supervised distillation setup and evaluation across multiple fine-grained vision benchmarks. It is a worthwhile review candidate because it targets a real failure mode in MLLMs and claims competitive results against stronger baselines, but the contribution is still relatively incremental and benchmark-driven rather than obviously field-defining.
- Research score estimate: 7.2
- Podcast score estimate: 6.8
- Local PDF path: data/papers/pdfs/arxiv-2605.18740.pdf
- Full text path: data/papers/fulltext/arxiv-2605.18740.txt
- Abstract URL: https://arxiv.org/abs/2605.18740
- PDF URL: https://arxiv.org/pdf/2605.18740

## Abstract
Multimodal Large Language Models (MLLMs) still struggle with fine-grained visual understanding, where answers often depend on small but decisive evidence in the full image. We observe a regional-to-global perception gap: the same MLLM answers fine-grained questions more accurately when conditioned on evidence-centered crops than on the corresponding full images, suggesting that many failures stem from difficulty to focus on relevant evidence rather than insufficient local recognition ability. Motivated by this observation, we propose Vision-OPD (Vision On-Policy Distillation), a regional-to-global self-distillation framework that transfers the model's own privileged regional perception to its full-image policy. Vision-OPD instantiates two conditional policies from the same MLLM: a crop-conditioned teacher and a full-image-conditioned student. The student generates on-policy rollouts, and Vision-OPD minimizes token-level divergence between the teacher and student next-token distributions along these rollouts. This enables the model to internalize the benefit of visual zooming without external teacher models, ground-truth labels, reward verifiers, or inference-time tool use. Experiments on multiple fine-grained visual understanding benchmarks show that Vision-OPD models achieve competitive or superior performance against much larger open-source, closed-source, and "Thinking-with-Images" agentic models.
