# DECO: Sparse Mixture-of-Experts with Dense-Comparable Performance on End-Side Devices

## Metadata
- Paper ID: arxiv-2605.10933
- Source: arxiv
- Source ID: 2605.10933
- Authors: Chenyang Song, Weilin Zhao, Xu Han, Chaojun Xiao, Yingfa Chen, Zhiyuan Liu
- Published: 2026-05-11T17:58:28Z
- Updated: 2026-05-11T17:58:28Z
- Categories: cs.LG, cs.CL
- Source signals: arxiv_recent
- Triage decision: advance_to_review
- Research score estimate: 7.1
- Podcast score estimate: 7.4
- Abstract URL: https://arxiv.org/abs/2605.10933
- PDF URL: https://arxiv.org/pdf/2605.10933

## Abstract
While Mixture-of-Experts (MoE) scales model capacity without proportionally increasing computation, its massive total parameter footprint creates significant storage and memory-access bottlenecks, which hinder efficient end-side deployment that simultaneously requires high performance, low computational cost, and small storage overhead. To achieve these properties, we present DECO, a sparse MoE architecture designed to match the performance of dense Transformers under identical total parameter budgets and training tokens. DECO utilizes the differentiable and flexible ReLU-based routing enhanced by learnable expert-wise scaling, which adaptively balances the contributions of routed and shared experts. Furthermore, we introduce NormSiLU, an activation function that normalizes inputs prior to SiLU operators, producing a more stable trend of routed-expert activation ratio and a higher intrinsic sparsity level. We also identify an empirical advantage in using non-gated MLP experts with ReLU-based routing, indicating the possibility of MoE architecture simplification. Experiments demonstrate that DECO, activating only 20% of experts, matches dense performance and outperforms established MoE baselines. Our specialized acceleration kernel delivers a 3.00$\times$ speedup on real hardware compared with dense inference. Codes and checkpoints will be released.
