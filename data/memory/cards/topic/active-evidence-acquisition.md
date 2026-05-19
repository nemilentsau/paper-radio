---
id: active-evidence-acquisition
type: topic
tags: ["active-evidence-acquisition", "agent-evaluation", "belief-revision"]
aliases: ["active evidence acquisition", "evidence-seeking agents", "knowing what to inspect"]
evidence: ["episode-2026-05-19-01-frontier-ml-roundup"]
updated_at: 2026-05-19
---

## Reusable Framing

Evaluate agentic and multimodal systems by whether they acquire the evidence needed to answer, not only by whether they can answer when the evidence is already present. Passive perception benchmarks can hide the central failure mode: a model may recognize the right evidence from an oracle view or crop but fail to choose actions, viewpoints, tools, retrieval steps, or follow-up checks that would obtain that evidence in the first place.

## Current Evidence

In episode-2026-05-19-01-frontier-ml-roundup, ESI-Bench supplied the clearest current evidence. Its passive single-view, passive random multi-view, active exploration, and ground-truth trajectory conditions separate raw visual understanding from action selection and evidence acquisition. The review signal was that current MLLMs often can answer from the right evidence but do not know how to go get it: they commit early, move redundantly, seek confirmation, and weakly revise beliefs. Vision-OPD added a narrower single-image analogue: models can perform better when a small region is cropped, and the method tries to distill that crop-conditioned behavior back into full-image inference.

## Prior Framing And Future Use

Before this episode, the durable framing was mostly implicit: benchmark gains should be checked for whether the model saw the right information. This update sharpens that into a reusable evaluation question for future papers: did the experiment isolate evidence acquisition, or did it provide privileged evidence through crops, oracle trajectories, synthetic boxes, retrieval, labels, or task generators? Strong future work should include random, scripted, oracle, and information-gain baselines; measure belief revision and premature stopping; and report whether failures come from perception, memory, planning, tool choice, or confidence calibration. The caveat from the current evidence is that synthetic simulators and high-level actions can make evidence acquisition easier to instrument than it would be in real deployment, so this card should guide critique rather than certify any one benchmark as definitive.

## Changelog
Created from episode-2026-05-19-01-frontier-ml-roundup to preserve the reusable evaluation frame that agent capability depends on active evidence acquisition, not just passive perception.
