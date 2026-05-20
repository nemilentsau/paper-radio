---
id: active-evidence-acquisition
type: topic
tags: ["active-evidence-acquisition", "agent-evaluation", "belief-revision"]
aliases: ["active evidence acquisition", "evidence-seeking agents", "knowing what to inspect"]
evidence: ["episode-2026-05-19-01-frontier-ml-roundup", "episode-2026-05-20-01-frontier-ml-roundup"]
updated_at: 2026-05-20
---

## Reusable Framing

Evaluate agentic and multimodal systems by whether they acquire the evidence needed to answer, not only by whether they can answer when the evidence is already present. Passive benchmarks can hide the central failure mode: a model may recognize the right evidence from an oracle context, crop, report, or retrieved bundle but fail to choose actions, tools, viewpoints, or follow-up checks that would obtain and verify that evidence in deployment.

## Current Evidence

The prior framing came from episode-2026-05-19-01-frontier-ml-roundup, where ESI-Bench separated passive views, active exploration, and ground-truth trajectories, and Vision-OPD showed a narrower crop-conditioned version of the same issue. The reusable lesson was that evidence acquisition must be isolated from raw perception or answer generation.

In episode-2026-05-20-01-frontier-ml-roundup, ClinSeekAgent extends this frame into clinical agents. Its paired design compares curated patient context against an automated evidence-seeking setting over raw EHR, web, and imaging evidence. That is a stronger systems question than ordinary clinical QA: can the agent decide what to retrieve, inspect, and trust? The result is not a clean victory for agentic retrieval, because the active condition often has a larger and more tool-rich evidence surface than the curated baseline, and decision-making tasks degrade in some settings. This makes the paper valuable as evidence for the evaluation frame, not as proof that clinical evidence-seeking agents are reliable.

The same episode adds adjacent evidence from staged VLM post-training: visual reasoning may improve when perception is trained before reasoning, suggesting that longer reasoning traces cannot compensate for missing or weakly grounded perceptual facts. KoRe provides a structured-knowledge analogue, where the question is whether graph facts should be made available as compact learned tokens rather than verbose textual triples.

## Prior Framing And Future Use

Before this episode, the card emphasized active exploration and privileged crops. The update broadens the reusable critique to clinical, multimodal, and structured-knowledge systems: when a paper reports better downstream accuracy, ask whether the model became better at reasoning or simply received a larger, cleaner, more specialized, or more judge-friendly evidence surface. Strong future evaluations should include curated-input, raw-retrieval, retrieval-only, oracle-evidence, no-browser/tool-ablated, and cost-normalized conditions; report tool calls and evidence provenance; and separate failures of perception, retrieval, tool choice, belief revision, and domain reasoning. In high-stakes domains, evidence access must also be judged for operational meaning, not only benchmark F1.

## Changelog
Created from episode-2026-05-19-01-frontier-ml-roundup to preserve the reusable evaluation frame that agent capability depends on active evidence acquisition, not just passive perception.
Updated from episode-2026-05-20-01-frontier-ml-roundup to extend the active-evidence-acquisition frame from exploration/crops to clinical agents, staged VLM perception, and structured evidence surfaces.
