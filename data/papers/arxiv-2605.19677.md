# Agentic Discovery of Cryomicroneedle Formulations

## Metadata
- Paper ID: arxiv-2605.19677
- Source: arxiv
- Source ID: 2605.19677
- Authors: Hao Li, Lifu Du, Nurul Hameed, Shemonti Saha Authai, Zlata Stefanovic, Chenjie Xu
- Published: 2026-05-19T11:09:46Z
- Updated: 2026-05-19T11:09:46Z
- Categories: cs.LG, q-bio.QM
- Source signals: arxiv_applied_domain, applied_domain:chemistry_materials
- Triage decision: advance_to_review
- Triage rationale: This is a concrete domain workflow paper, not a benchmark-only study: it includes iterative wet-lab validation, measurable gains over rounds, and an explicit materials/formulation discovery loop. The evidence in the abstract is strong enough to merit full review because the claims are tied to experimental outcomes, though the multi-objective limitation suggests some caution.
- Research score estimate: 7.6
- Podcast score estimate: 6.8
- Local PDF path: data/papers/pdfs/arxiv-2605.19677.pdf
- Full text path: data/papers/fulltext/arxiv-2605.19677.txt
- Abstract URL: https://arxiv.org/abs/2605.19677
- PDF URL: https://arxiv.org/pdf/2605.19677

## Abstract
Cryomicroneedles offer a route to minimally invasive intradermal delivery of living cells, but their cryogenic formulations must reconcile cell protection with constraints on toxicity and device fabrication. Here we report an AI-assisted, closed-loop workflow for cryomicroneedle cryoprotectant discovery that combines literature curation, Gaussian-process surrogate modelling, Bayesian optimization, and sequential wet-lab validation. A curated dataset of 198 mesenchymal stem-cell cryopreservation formulations from 42 studies was converted into 21 ingredient features and used to train an uncertainty-aware literature prior. This model captured moderate structure in the literature data but failed prospectively, motivating iterative wet-lab correction. Across ten validation iterations and 106 wet-lab observations, the model progressively adapted to cryomicroneedle-specific outcomes: batch RMSE decreased from 41.21 to 6.86 percentage points, later-stage rank correlations became consistently positive, and the cumulative wet-lab predicted-versus-measured summary reached $R^2 = 0.942$. The best validated formulation achieved 95.15\% post-thaw viability with low DMSO, ectoin, ethylene glycol, and fetal bovine serum. However, high viability alone did not ensure intact cryomicroneedle formation, highlighting the need for future multi-objective optimization. These results demonstrate that agent-assisted computational infrastructure can make data-efficient formulation discovery more accessible to labs with minimal data expertise in-house. Project code is available at https://github.com/baitmeister/ML-for-CryoMN.
