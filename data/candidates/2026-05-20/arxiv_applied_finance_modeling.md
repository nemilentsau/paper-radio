# arxiv_applied_finance_modeling Candidates For 2026-05-20

## arxiv-2605.19895: Streamlined Constraint Reasoning via CNN Pattern Recognition on Enumerated Solutions

- Categories: cs.AI
- Authors: Patrick Spracklen
- Author affiliations: unknown
- Trusted org matches: none
- Applied domain: Finance and economic modeling workflows
- Applied-domain score: 7
- Matched required domain terms: portfolio
- Matched model terms: large language model, llm
- Matched LLM/domain keywords: large language model, llm, portfolio
- Matched workflow terms: portfolio, risk
- Abstract URL: https://arxiv.org/abs/2605.19895
- PDF URL: https://arxiv.org/pdf/2605.19895

Constraint programming practitioners accelerate hard problems through a layered set of techniques applied in order of risk. Standard hardening (symmetry-breaking and implied constraints) is applied first and preserves satisfiability. Streamliner constraints, which restrict search to a structural sub-family of solutions, do not preserve satisfiability and are reserved as a final lever. Existing automated streamliner-synthesis approaches either search a constraint grammar or prompt a Large Language Model directly on the problem model. We propose a different approach: enumerate feasible solutions, train a Convolutional Neural Network contrastively against perturbed non-solutions to detect structural patterns, and translate the CNN's discriminative signal into candidate MiniZinc streamliners through LLM-driven synthesis. The CNN grounds the LLM's constraint generation in observed solution structure rather than model text alone. We evaluate on hardened benchmark models where streamliner discovery is the residual performance lever. Our pipeline achieves 98.8% portfolio time reduction on hardened Vessel Loading, 98.6% on hardened Social Golfers, and 89.4% on Black Hole, with best-single streamliners reaching geometric-mean speedups of 932x, 356x, and 1103x respectively. Discovered streamliners include class-based packing constraints on Vessel Loading, beyond-hardening canonicalisations on Social Golfers, and layout-coordinate bounds on Black Hole.

## arxiv-2605.20098: Neurosymbolic Learning for Inference-Time Argumentation

- Categories: cs.AI
- Authors: Gabriel Freedman, Adam Dejl, Adam Gould, Mansi, Lihu Chen, Jianqi Jiang, Francesca Toni
- Author affiliations: unknown
- Trusted org matches: none
- Applied domain: Finance and economic modeling workflows
- Applied-domain score: 3
- Matched required domain terms: finance
- Matched model terms: llm
- Matched LLM/domain keywords: llm, finance
- Matched workflow terms: none
- Abstract URL: https://arxiv.org/abs/2605.20098
- PDF URL: https://arxiv.org/pdf/2605.20098

Claim verification is an important problem in high-stakes settings, including health and finance. When information underpinning claims is incomplete or conflicting, uncertain answers may be more appropriate than binary true or false classifications. In all cases, faithful explanations of the considerations determining the final verdict are crucial. We introduce inference-time argumentation (ITA), a trainable neurosymbolic framework for ternary claim verification in which a formal argumentation semantics giving the strength of claims is used both (i) to guide LLM training as models learn to generate arguments and assign them base scores (representing intrinsic strengths) and (ii) to compute ternary (true/false/uncertain) predictions from generated, scored arguments. As a result, at training time, argument generation and scoring can be optimised according to the quality of the induced argumentative predictions. Moreover, at inference time, the final prediction is faithful, by construction, to the arguments and scores determining the verdict, rather than being justified by a potentially unfaithful post-hoc reasoning trace as in conventional reasoning models. We finally show that, on two datasets for ternary claim verification, ITA improves upon argumentative baselines and can perform competitively against non-argumentative direct-prediction baselines, while providing verdicts that are computed deterministically from explicit, inspectable argumentative structures.

## arxiv-2605.19674: Beyond Rational Illusion: Behaviorally Realistic Strategic Classification

- Categories: cs.AI
- Authors: Xinpeng Lv, Yunxin Mao, Renzhe Xu, Chunyuan Zheng, Yikai Chen, Haoxuan Li, Yang Shi, Jinxuan Yang, Zhouchen Lin, Yuanlong Chen, Yuanxing Zhang, Shaowu Yang, Wenjing Yang, Haotian Wang
- Author affiliations: unknown
- Trusted org matches: none
- Applied domain: Finance and economic modeling workflows
- Applied-domain score: 3
- Matched required domain terms: economic
- Matched model terms: agent
- Matched LLM/domain keywords: economic, agent
- Matched workflow terms: none
- Abstract URL: https://arxiv.org/abs/2605.19674
- PDF URL: https://arxiv.org/pdf/2605.19674

Strategic classification(SC) studies the interaction between decision models and agents who strategically manipulate their features for favorable outcomes. Existing SC frameworks typically rely on the idealized assumption that agents are strictly rational. However, evidence from behavioral economics and psychology consistently shows that real-world decision-making is often shaped by cognitive biases, deviating from pure rationality. To formalize this limitation, we identify and define a new problem setting, termed the behaviorally realistic strategic classification problem, where agents' strategic manipulations deviate from full rationality due to psychological biases. Motivated by the identified limitation, we propose the Prospect-Guided Strategic Framework (Pro-SF) to address the problem, a principled framework grounded in prospect theory to model and learn under behaviorally realistic strategic responses. Specifically, to capture behaviorally realistic strategic manipulations, our framework reformulates the Stackelberg-style interaction between agents and the decision-maker by incorporating three key mechanisms inspired by prospect theory, including the asymmetry between benefits and costs, different subjective reference points, and non-rational probability distortion. Experiments on synthetic and real-world datasets establish Pro-SF as a behaviorally grounded approach to strategic classification, bridging machine learning and behavioral economics for more reliable deployment in the real world.
