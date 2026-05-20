# Direct Simulation of LiNi0.8Mn0.1Co0.1O2 Transport Properties Using an Efficient and Accurate Machine Learning Potential

## Metadata
- Paper ID: arxiv-2605.19747
- Source: arxiv
- Source ID: 2605.19747
- Authors: Jian He, Constantijn H. J. A. van de Wetering, Rolande W. Nolsen, Nongnuch Artrith
- Published: 2026-05-19T12:16:08Z
- Updated: 2026-05-19T12:16:08Z
- Categories: cond-mat.mtrl-sci
- Source signals: arxiv_applied_domain, applied_domain:chemistry_materials
- Triage decision: advance_to_review
- Triage rationale: This is a concrete materials workflow paper, not just a benchmark: it uses a foundation model, active learning, and direct MD simulation to answer a physically meaningful transport question in NMC811. The topic is narrow but methodologically substantive, with clear applied relevance and enough technical content to merit review.
- Research score estimate: 7.2
- Podcast score estimate: 5.8
- Local PDF path: data/papers/pdfs/arxiv-2605.19747.pdf
- Full text path: data/papers/fulltext/arxiv-2605.19747.txt
- Abstract URL: https://arxiv.org/abs/2605.19747
- PDF URL: https://arxiv.org/pdf/2605.19747

## Abstract
The rate capability of layered lithium nickel manganese cobalt oxide (NMC) cathode materials plays a decisive role in high-power applications such as fast charging, necessitating a detailed understanding of lithium-ion diffusion. However, the mechanisms governing lithium-ion transport in NMC remain insufficiently understood, both experimentally and computationally. In this study, we employ an advanced and efficient machine learning potential (MLP) to simulate lithium self-diffusion in LiNi0.8Mn0.1Co0.1O2 (NMC811), enabling direct large-scale molecular dynamics (MD) simulations. The workflow integrates a fine-tuned MACE (Message Passing Atomic Cluster Expansion) foundation model as a structural generator and leverages an active learning strategy applied to a near-ground-state dataset. This approach enables the construction of a reliable MLP for NMC811 in a data-efficient manner using a limited number of density functional theory (DFT) reference calculations. Based on this potential, we performed MD simulations to predict lithium diffusion coefficients. The MLP-based simulations preserve the accuracy of DFT while overcoming its time and length scale limitations, thereby allowing direct simulation of lithium self-diffusion in NMC811.
