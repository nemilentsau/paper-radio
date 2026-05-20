# AutoResearchClaw: Self-Reinforcing Autonomous Research with Human-AI Collaboration

## Metadata
- Paper ID: arxiv-2605.20025
- Source: arxiv
- Source ID: 2605.20025
- Authors: Jiaqi Liu, Shi Qiu, Mairui Li, Bingzhou Li, Haonian Ji, Siwei Han, Xinyu Ye, Peng Xia, Zihan Dong, Congyu Zhang, Letian Zhang, Guiming Chen, Haoqin Tu, Xinyu Yang, Lu Feng, Xujiang Zhao, Haifeng Chen, Jiawei Zhou, Xiao Wang, Weitong Zhang, Hongtu Zhu, Yun Li, Jieru Mei, Hongliang Fei, Jiaheng Zhang, Linjie Li, Linjun Zhang, Yuyin Zhou, Sheng Wang, Caiming Xiong, James Zou, Zeyu Zheng, Cihang Xie, Mingyu Ding, Huaxiu Yao
- Published: 2026-05-19T15:49:51Z
- Updated: 2026-05-19T15:49:51Z
- Categories: cs.AI
- Source signals: arxiv_applied_domain, applied_domain:scientific_discovery
- Triage decision: queue_for_review
- Triage rationale: This is a concrete scientific-discovery workflow paper rather than a generic benchmark claim: the abstract names specific mechanisms, a human-in-the-loop ablation, and a cross-run learning loop. The main risk is that the evidence described in the abstract is still benchmark-centered and may overstate general scientific usefulness, so it deserves review but not automatic advancement.
- Research score estimate: 7.4
- Podcast score estimate: 7.8
- Local PDF path: data/papers/pdfs/arxiv-2605.20025.pdf
- Full text path: data/papers/fulltext/arxiv-2605.20025.txt
- Abstract URL: https://arxiv.org/abs/2605.20025
- PDF URL: https://arxiv.org/pdf/2605.20025

## Abstract
Automating scientific discovery requires more than generating papers from ideas. Real research is iterative: hypotheses are challenged from multiple perspectives, experiments fail and inform the next attempt, and lessons accumulate across cycles. Existing autonomous research systems often model this process as a linear pipeline: they rely on single-agent reasoning, stop when execution fails, and do not carry experience across runs. We present AutoResearchClaw, a multi-agent autonomous research pipeline built on five mechanisms: structured multi-agent debate for hypothesis generation and result analysis, a self-healing executor with a \textsc{Pivot}/\textsc{Refine} decision loop that transforms failures into information, verifiable result reporting that prevents fabricated numbers and hallucinated citations, human-in-the-loop collaboration with seven intervention modes spanning full autonomy to step-by-step oversight, and cross-run evolution that converts past mistakes into future safeguards. On ARC-Bench, a 25-topic experiment-stage benchmark, AutoResearchClaw outperforms AI Scientist v2 by 54.7%. A human-in-the-loop ablation across seven intervention modes reveals that precise, targeted collaboration at high-leverage decision points consistently outperforms both full autonomy and exhaustive step-by-step oversight. We position AutoResearchClaw as a research amplifier that augments rather than replaces human scientific judgment. Code is available at https://github.com/aiming-lab/AutoResearchClaw.
