# arxiv_applied_chemistry_materials Candidates For 2026-05-20

## arxiv-2605.19747: Direct Simulation of LiNi0.8Mn0.1Co0.1O2 Transport Properties Using an Efficient and Accurate Machine Learning Potential

- Categories: cond-mat.mtrl-sci
- Authors: Jian He, Constantijn H. J. A. van de Wetering, Rolande W. Nolsen, Nongnuch Artrith
- Author affiliations: unknown
- Trusted org matches: none
- Applied domain: Chemistry and materials workflows
- Applied-domain score: 4
- Matched required domain terms: materials, cond-mat
- Matched model terms: foundation model
- Matched LLM/domain keywords: materials, foundation model
- Matched workflow terms: none
- Abstract URL: https://arxiv.org/abs/2605.19747
- PDF URL: https://arxiv.org/pdf/2605.19747

The rate capability of layered lithium nickel manganese cobalt oxide (NMC) cathode materials plays a decisive role in high-power applications such as fast charging, necessitating a detailed understanding of lithium-ion diffusion. However, the mechanisms governing lithium-ion transport in NMC remain insufficiently understood, both experimentally and computationally. In this study, we employ an advanced and efficient machine learning potential (MLP) to simulate lithium self-diffusion in LiNi0.8Mn0.1Co0.1O2 (NMC811), enabling direct large-scale molecular dynamics (MD) simulations. The workflow integrates a fine-tuned MACE (Message Passing Atomic Cluster Expansion) foundation model as a structural generator and leverages an active learning strategy applied to a near-ground-state dataset. This approach enables the construction of a reliable MLP for NMC811 in a data-efficient manner using a limited number of density functional theory (DFT) reference calculations. Based on this potential, we performed MD simulations to predict lithium diffusion coefficients. The MLP-based simulations preserve the accuracy of DFT while overcoming its time and length scale limitations, thereby allowing direct simulation of lithium self-diffusion in NMC811.

## arxiv-2605.19677: Agentic Discovery of Cryomicroneedle Formulations

- Categories: cs.LG, q-bio.QM
- Authors: Hao Li, Lifu Du, Nurul Hameed, Shemonti Saha Authai, Zlata Stefanovic, Chenjie Xu
- Author affiliations: unknown
- Trusted org matches: none
- Applied domain: Chemistry and materials workflows
- Applied-domain score: 4
- Matched required domain terms: lab
- Matched model terms: agent
- Matched LLM/domain keywords: lab, agent
- Matched workflow terms: optimization
- Abstract URL: https://arxiv.org/abs/2605.19677
- PDF URL: https://arxiv.org/pdf/2605.19677

Cryomicroneedles offer a route to minimally invasive intradermal delivery of living cells, but their cryogenic formulations must reconcile cell protection with constraints on toxicity and device fabrication. Here we report an AI-assisted, closed-loop workflow for cryomicroneedle cryoprotectant discovery that combines literature curation, Gaussian-process surrogate modelling, Bayesian optimization, and sequential wet-lab validation. A curated dataset of 198 mesenchymal stem-cell cryopreservation formulations from 42 studies was converted into 21 ingredient features and used to train an uncertainty-aware literature prior. This model captured moderate structure in the literature data but failed prospectively, motivating iterative wet-lab correction. Across ten validation iterations and 106 wet-lab observations, the model progressively adapted to cryomicroneedle-specific outcomes: batch RMSE decreased from 41.21 to 6.86 percentage points, later-stage rank correlations became consistently positive, and the cumulative wet-lab predicted-versus-measured summary reached $R^2 = 0.942$. The best validated formulation achieved 95.15\% post-thaw viability with low DMSO, ectoin, ethylene glycol, and fetal bovine serum. However, high viability alone did not ensure intact cryomicroneedle formation, highlighting the need for future multi-objective optimization. These results demonstrate that agent-assisted computational infrastructure can make data-efficient formulation discovery more accessible to labs with minimal data expertise in-house. Project code is available at https://github.com/baitmeister/ML-for-CryoMN.
