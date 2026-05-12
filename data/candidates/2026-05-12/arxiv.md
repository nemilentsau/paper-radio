# arxiv Candidates For 2026-05-12

## arxiv-2605.10938: ELF: Embedded Language Flows

- Categories: cs.CL, cs.AI, cs.LG
- Authors: Keya Hu, Linlu Qiu, Yiyang Lu, Hanhong Zhao, Tianhong Li, Yoon Kim, Jacob Andreas, Kaiming He
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.10938
- PDF URL: https://arxiv.org/pdf/2605.10938

Diffusion and flow-based models have become the de facto approaches for generating continuous data, e.g., in domains such as images and videos. Their success has attracted growing interest in applying them to language modeling. Unlike their image-domain counterparts, today's leading diffusion language models (DLMs) primarily operate over discrete tokens. In this paper, we show that continuous DLMs can be made effective with minimal adaptation to the discrete domain. We propose Embedded Language Flows (ELF), a class of diffusion models in continuous embedding space based on continuous-time Flow Matching. Unlike existing DLMs, ELF predominantly stays within the continuous embedding space until the final time step, where it maps to discrete tokens using a shared-weight network. This formulation makes it straightforward to adapt established techniques from image-domain diffusion models, e.g., classifier-free guidance (CFG). Experiments show that ELF substantially outperforms leading discrete and continuous DLMs, achieving better generation quality with fewer sampling steps. These results suggest that ELF offers a promising path toward effective continuous DLMs.

## arxiv-2605.10934: Variational Inference for Lévy Process-Driven SDEs via Neural Tilting

- Categories: cs.LG, cs.AI, cs.CV, cs.RO, stat.ML
- Authors: Yaman Kindap, Manfred Opper, Benjamin Dupuis, Umut Simsekli, Tolga Birdal
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.10934
- PDF URL: https://arxiv.org/pdf/2605.10934

Modelling extreme events and heavy-tailed phenomena is central to building reliable predictive systems in domains such as finance, climate science, and safety-critical AI. While Lévy processes provide a natural mathematical framework for capturing jumps and heavy tails, Bayesian inference for Lévy-driven stochastic differential equations (SDEs) remains intractable with existing methods: Monte Carlo approaches are rigorous but lack scalability, whereas neural variational inference methods are efficient but rely on Gaussian assumptions that fail to capture discontinuities. We address this tension by introducing a neural exponential tilting framework for variational inference in Lévy-driven SDEs. Our approach constructs a flexible variational family by exponentially reweighting the Lévy measure using neural networks. This parametrization preserves the jump structure of the underlying process while remaining computationally tractable. To enable efficient inference, we develop a quadratic neural parametrization that yields closed-form normalization of the tilted measure, a conditional Gaussian representation for stable processes that facilitates simulation, and symmetry-aware Monte Carlo estimators for scalable optimization. Empirically, we demonstrate that the method accurately captures jump dynamics and yields reliable posterior inference in regimes where Gaussian-based variational approaches fail, on both synthetic and real-world datasets.

## arxiv-2605.10933: DECO: Sparse Mixture-of-Experts with Dense-Comparable Performance on End-Side Devices

- Categories: cs.LG, cs.CL
- Authors: Chenyang Song, Weilin Zhao, Xu Han, Chaojun Xiao, Yingfa Chen, Zhiyuan Liu
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.10933
- PDF URL: https://arxiv.org/pdf/2605.10933

While Mixture-of-Experts (MoE) scales model capacity without proportionally increasing computation, its massive total parameter footprint creates significant storage and memory-access bottlenecks, which hinder efficient end-side deployment that simultaneously requires high performance, low computational cost, and small storage overhead. To achieve these properties, we present DECO, a sparse MoE architecture designed to match the performance of dense Transformers under identical total parameter budgets and training tokens. DECO utilizes the differentiable and flexible ReLU-based routing enhanced by learnable expert-wise scaling, which adaptively balances the contributions of routed and shared experts. Furthermore, we introduce NormSiLU, an activation function that normalizes inputs prior to SiLU operators, producing a more stable trend of routed-expert activation ratio and a higher intrinsic sparsity level. We also identify an empirical advantage in using non-gated MLP experts with ReLU-based routing, indicating the possibility of MoE architecture simplification. Experiments demonstrate that DECO, activating only 20% of experts, matches dense performance and outperforms established MoE baselines. Our specialized acceleration kernel delivers a 3.00$\times$ speedup on real hardware compared with dense inference. Codes and checkpoints will be released.

## arxiv-2605.10931: Quantifying Concentration Phenomena of Mean-Field Transformers in the Low-Temperature Regime

- Categories: math.AP, cs.LG, math.DS
- Authors: Albert Alcalde, Leon Bungert, Konstantin Riedl, Tim Roith
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.10931
- PDF URL: https://arxiv.org/pdf/2605.10931

Transformers with self-attention modules as their core components have become an integral architecture in modern large language and foundation models. In this paper, we study the evolution of tokens in deep encoder-only transformers at inference time which is described in the large-token limit by a mean-field continuity equation. Leveraging ideas from the convergence analysis of interacting multi-particle systems, with particles corresponding to tokens, we prove that the token distribution rapidly concentrates onto the push-forward of the initial distribution under a projection map induced by the key, query, and value matrices, and remains metastable for moderate times. Specifically, we show that the Wasserstein distance of the two distributions scales like $\sqrt{{\log(β+1)}/β}\exp(Ct)+\exp(-ct)$ in terms of the temperature parameter $β^{-1}\to 0$ and inference time $t\geq 0$. For the proof, we establish Lyapunov-type estimates for the zero-temperature equation, identify its limit as $t\to\infty$, and employ a stability estimate in Wasserstein space together with a quantitative Laplace principle to couple the two equations. Our result implies that for time scales of order $\logβ$ the token distribution concentrates at the identified limiting distribution. Numerical experiments confirm this and, beyond that, complement our theory by showing that for finite $β$ and large $t$ the dynamics enter a different terminal phase, dominated by the spectrum of the value matrix.

## arxiv-2605.10923: Dynamic Skill Lifecycle Management for Agentic Reinforcement Learning

- Categories: cs.LG, cs.CL
- Authors: Junhao Shen, Teng Zhang, Xiaoyan Zhao, Hong Cheng
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.10923
- PDF URL: https://arxiv.org/pdf/2605.10923

Large language model agents increasingly rely on external skills to solve complex tasks, where skills act as modular units that extend their capabilities beyond what parametric memory alone supports. Existing methods assume external skills either accumulate as persistent guidance or internalized into the policy, eventually leading to zero-skill inference. We argue this assumption is overly restrictive, since with limited parametric capacity and uneven marginal contribution across skills, the optimal active skill set is non-monotonic, task- and stage-dependent. In this work, we propose SLIM, a framework of dynamic Skill LIfecycle Management for agentic reinforcement learning (RL), which treats the active external skill set as a dynamic optimization variable jointly updated with policy learning. Specifically, SLIM estimates each active skill's marginal external contribution through leave-one-skill-out validation, then applies three lifecycle operations: retaining high-value skills, retiring skills whose contribution becomes negligible after sufficient exposure, and expanding the skill bank when persistent failures reveal missing capability coverage. Experiments show that SLIM outperforms the best baselines by an average of 7.1% points across ALFWorld and SearchQA. Results further indicate that policy learning and external skill retention are not mutually exclusive: some skills are absorbed into the policy, while others continue to provide external value, supporting SLIM as a more general paradigm for skill-based agentic RL.

## arxiv-2605.10917: Optimal and Scalable MAPF via Multi-Marginal Optimal Transport and Schrödinger Bridges

- Categories: cs.LG, cs.MA, cs.RO
- Authors: Usman A. Khan, Joseph W. Durham
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.10917
- PDF URL: https://arxiv.org/pdf/2605.10917

We consider anonymous multi-agent path finding (MAPF) where a set of robots is tasked to travel to a set of targets on a finite, connected graph. We show that MAPF can be cast as a special class of multi-marginal optimal transport (MMOT) problems with an underlying Markovian structure, under which the exponentially large MMOT collapses to a linear program (LP) polynomial in size. Focusing on the anonymous setting, we establish conditions under which the corresponding LP is feasible, totally unimodular, and consequently, yields min-cost, integral $(\{0,1\})$ transports that do not overlap in both space and time. To adapt the approach to large-scale problems, we cast the MAPF-MMOT in a probabilistic framework via Schrödinger bridges. Under standard assumptions, we show that the Schrödinger bridge formulation reduces to an entropic regularization of the corresponding MMOT that admits an iterative Sinkhorn-type solution. The Schrödinger bridge, being a probabilistic framework, provides a shadow (fractional) transport that we use as a template to solve a reduced LP and demonstrate that it results in near-optimal, integral transports at a significant reduction in complexity. Extensive experiments highlight the optimality and scalability of the proposed approaches.

## arxiv-2605.10916: Confidence-Guided Diffusion Augmentation for Enhanced Bangla Compound Character Recognition

- Categories: cs.CV, cs.AI
- Authors: Md. Sultan Al Rayhan, Maheen Islam
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.10916
- PDF URL: https://arxiv.org/pdf/2605.10916

Recognition of handwritten Bangla compound characters remains a challenging problem due to complex character structures, large intra-class variation, and limited availability of high-quality annotated data. Existing Bangla handwritten character recognition systems often struggle to generalize across diverse writing styles, particularly for compound characters containing intricate ligatures and diacritical variations. In this work, we propose a confidence-guided diffusion augmentation framework for low-resolution Bangla compound character recognition. Our framework combines class-conditional diffusion modeling with classifier guidance to synthesize high-quality handwritten compound character samples. To further improve generation quality, we introduce Squeeze-and-Excitation enhanced residual blocks within the diffusion model's U-Net backbone. We additionally propose a confidence-based filtering mechanism where pre-trained classifiers act as quality gates to retain only highly class-consistent synthetic samples. The filtered synthetic images are fused with the original training data and used to retrain multiple classification architectures. Experiments conducted on the AIBangla compound character dataset demonstrate consistent performance improvements across ResNet50, DenseNet121, VGG16, and Vision Transformer architectures. Our best-performing model achieves 89.2\% classification accuracy, surpassing the previously published AIBangla benchmark by a substantial margin. The results demonstrate that quality-aware diffusion augmentation can effectively enhance handwritten character recognition performance in low-resource script domains.

## arxiv-2605.10913: Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace

- Categories: cs.AI, cs.PL, cs.SE
- Authors: Simon Yu, Derek Chong, Ananjan Nandi, Dilara Soylu, Jiuding Sun, Christopher D Manning, Weiyan Shi
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.10913
- PDF URL: https://arxiv.org/pdf/2605.10913

We introduce Shepherd, a functional programming model that formalizes meta-agent operations on target agents as functions, with core operations mechanized in Lean. Shepherd records every agent-environment interaction as a typed event in a Git-like execution trace, enabling any past state to be forked and replayed. The system forks the agent process and its filesystem $5\times$ faster than Docker, achieving $>95\%$ prompt-cache reuse on replay. We demonstrate the model through three applications. First, in runtime intervention, a live supervisor increases pair coding pass rates from 28.8% to 54.7% on CooperBench. Second, in counterfactual meta-optimization, branching exploration outperforms baselines across four benchmarks by up to 11 points while reducing wall-clock time by up to 58%. Third, in Tree-RL training, forking rollouts at selected turns improves TerminalBench-2 performance from 34.2% to 39.4%. These results establish Shepherd as an efficient infrastructure for programming meta-agents. We open-source the system to support future research.

## arxiv-2605.10912: WildClawBench: A Benchmark for Real-World, Long-Horizon Agent Evaluation

- Categories: cs.CL
- Authors: Shuangrui Ding, Xuanlang Dai, Long Xing, Shengyuan Ding, Ziyu Liu, Yang JingYi, Penghui Yang, Zhixiong Zhang, Xilin Wei, Xinyu Fang, Yubo Ma, Haodong Duan, Jing Shao, Jiaqi Wang, Dahua Lin, Kai Chen, Yuhang Zang
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.10912
- PDF URL: https://arxiv.org/pdf/2605.10912

Large language and vision-language models increasingly power agents that act on a user's behalf through command-line interface (CLI) harnesses. However, most agent benchmarks still rely on synthetic sandboxes, short-horizon tasks, mock-service APIs, and final-answer checks, leaving open whether agents can complete realistic long-horizon work in the runtimes where they are deployed. This work presents WildClawBench, a native-runtime benchmark of 60 human-authored, bilingual, multimodal tasks spanning six thematic categories. Each task averages roughly 8 minutes of wall-clock time and over 20 tool calls, and runs inside a reproducible Docker container hosting an actual CLI agent harness (OpenClaw, Claude Code, Codex, or Hermes Agent) with access to real tools rather than mock services. Grading is hybrid, combining deterministic rule-based checks, environment-state auditing of side effects, and an LLM/VLM judge for semantic verification. Across 19 frontier models, the best, Claude Opus 4.7, reaches only 62.2% overall under OpenClaw, while every other model stays below 60%, and switching harness alone shifts a single model by up to 18 points. These results show that long-horizon, native-runtime agent evaluation remains a far-from-resolved task for current frontier models. We release the tasks, code, and containerized tooling to support reproducible evaluation.

## arxiv-2605.10910: Equivariant Reinforcement Learning for Clifford Quantum Circuit Synthesis

- Categories: quant-ph, cs.LG
- Authors: Richie Yeung, Aleks Kissinger, Rob Cornish
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.10910
- PDF URL: https://arxiv.org/pdf/2605.10910

We consider the problem of synthesizing Clifford quantum circuits for devices with all-to-all qubit connectivity. We approach this task as a reinforcement learning problem in which an agent learns to discover a sequence of elementary Clifford gates that reduces a given symplectic matrix representation of a Clifford circuit to the identity. This formulation permits a simple learning curriculum based on random walks from the identity. We introduce a novel neural network architecture that is equivariant to qubit relabelings of the symplectic matrix representation, and which is size-agnostic, allowing a single learned policy to be applied across different qubit counts without circuit splicing or network reparameterization. On six-qubit Clifford circuits, the largest regime for which optimal references are available, our agent finds circuits within one two-qubit gate of optimality in milliseconds per instance, and finds optimal circuits in 99.2% of instances within seconds per instance. After continued training on ten-qubit instances, the agent scales to unseen Clifford tableaus with up to thirty qubits, including targets generated from circuits with over a thousand Clifford gates, where it achieves lower average two-qubit gate counts than Qiskit's Aaronson-Gottesman and greedy Clifford synthesizers.
