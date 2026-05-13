# arxiv Candidates For 2026-05-13

## arxiv-2605.12495: AlphaGRPO: Unlocking Self-Reflective Multimodal Generation in UMMs via Decompositional Verifiable Reward

- Categories: cs.CV, cs.AI, cs.LG
- Authors: Runhui Huang, Jie Wu, Rui Yang, Zhe Liu, Hengshuang Zhao
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.12495
- PDF URL: https://arxiv.org/pdf/2605.12495

In this paper, we propose AlphaGRPO, a novel framework that applies Group Relative Policy Optimization (GRPO) to AR-Diffusion Unified Multimodal Models (UMMs) to enhance multimodal generation capabilities without an additional cold-start stage. Our approach unlocks the model's intrinsic potential to perform advanced reasoning tasks: Reasoning Text-to-Image Generation, where the model actively infers implicit user intents, and Self-Reflective Refinement, where it autonomously diagnoses and corrects misalignments in generated outputs. To address the challenge of providing stable supervision for real-world multimodal generation, we introduce the Decompositional Verifiable Reward (DVReward). Unlike holistic scalar rewards, DVReward utilizes an LLM to decompose complex user requests into atomic, verifiable semantic and quality questions, which are then evaluated by a general MLLM to provide reliable and interpretable feedback. Extensive experiments demonstrate that AlphaGRPO yields robust improvements across multimodal generation benchmarks, including GenEval, TIIF-Bench, DPG-Bench and WISE, while also achieving significant gains in editing tasks on GEdit without training on editing tasks. These results validate that our self-reflective reinforcement approach effectively leverages inherent understanding to guide high-fidelity generation. Project page: https://huangrh99.github.io/AlphaGRPO/

## arxiv-2605.12493: LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues

- Categories: cs.CL
- Authors: Di Wu, Zixiang Ji, Asmi Kawatkar, Bryan Kwan, Jia-Chen Gu, Nanyun Peng, Kai-Wei Chang
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.12493
- PDF URL: https://arxiv.org/pdf/2605.12493

Long-term memory is crucial for agents in specialized web environments, where success depends on recalling interface affordances, state dynamics, workflows, and recurring failure modes. However, existing memory benchmarks for agents mostly focus on user histories, short traces, or downstream task success, leaving open how to directly evaluate whether memory systems effectively internalize environment-specific experience. To address this gap, we introduce LongMemEval-V2 (LME-V2), a benchmark for evaluating whether memory systems can help agents acquire the experience needed to become knowledgeable colleagues in customized environments. LME-V2 contains 451 manually curated questions covering five core memory abilities for web agents: static state recall, dynamic state tracking, workflow knowledge, environment gotchas, and premise awareness. Questions are paired with history trajectories containing up to 500 trajectories and 115M tokens. We use a context gathering formulation: memory systems consume history trajectories and return compact evidence for downstream question answering. We propose a suite of two memory methods: AgentRunbook-R, an efficient RAG-based memory with knowledge pools for raw state observations, events, and strategy notes, and AgentRunbook-C, which stores trajectories as files and invokes a coding agent to gather evidence in an augmented sandbox. Experiments show that AgentRunbook-C achieves the best performance with 72.5% average accuracy, outperforming the strongest RAG baseline (48.5%) and the off-the-shelf coding agent baseline (69.3%). Despite the strong performance gains, coding agent based methods have high latency costs. While AgentRunbook-C advances the accuracy-latency Pareto frontier, substantial room for improvement remains. Together, these results establish LME-V2 as a challenging testbed for developing long-term memory systems for environment experience.

## arxiv-2605.12492: Pion: A Spectrum-Preserving Optimizer via Orthogonal Equivalence Transformation

- Categories: cs.LG, stat.ML
- Authors: Kexuan Shi, Hanxuan Li, Zeju Qiu, Yandong Wen, Simon Buchholz, Weiyang Liu
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.12492
- PDF URL: https://arxiv.org/pdf/2605.12492

We introduce Pion, a spectrum-preserving optimizer for large language model (LLM) training based on orthogonal equivalence transformation. Unlike additive optimizers such as Adam and Muon, Pion updates each weight matrix through left and right orthogonal transformations, preserving its singular values throughout training. This yields an optimization mechanism that modulates the geometry of weight matrices while keeping their spectral norm fixed. We derive the Pion update rule, systematically examine its design choices, and analyze its convergence behavior along with several key properties. Empirical results show that Pion offers a stable and competitive alternative to standard optimizers for both LLM pretraining and finetuning.

## arxiv-2605.12491: Elastic Attention Cores for Scalable Vision Transformers

- Categories: cs.CV, cs.LG
- Authors: Alan Z. Song, Yinjie Chen, Mu Nan, Rui Zhang, Jiahang Cao, Weijian Mai, Muquan Yu, Hossein Adeli, Deva Ramanan, Michael J. Tarr, Andrew F. Luo
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.12491
- PDF URL: https://arxiv.org/pdf/2605.12491

Vision Transformers (ViTs) achieve strong data-driven scaling by leveraging all-to-all self-attention. However, this flexibility incurs a computational cost that scales quadratically with image resolution, limiting ViTs in high-resolution domains. Underlying this approach is the assumption that pairwise token interactions are necessary for learning rich visual-semantic representations. In this work, we challenge this assumption, demonstrating that effective visual representations can be learned without any direct patch-to-patch interaction. We propose VECA (Visual Elastic Core Attention), a vision transformer architecture that uses efficient linear-time core-periphery structured attention enabled by a small set of learned cores. In VECA, these cores act as a communication interface: patch tokens exchange information exclusively through the core tokens, which are initialized from scratch and propagated across layers. Because the $N$ image patches only directly interact with a resolution invariant set of $C$ learned "core" embeddings, this yields linear complexity $O(N)$ for predetermined $C$, which bypasses quadratic scaling. Compared to prior cross-attention architectures, VECA maintains and iteratively updates the full set of $N$ input tokens, avoiding a small $C$-way bottleneck. Combined with nested training along the core axis, our model can elastically trade off compute and accuracy during inference. Across classification and dense tasks, VECA achieves performance competitive with the latest vision foundation models while reducing computational cost. Our results establish elastic core-periphery attention as a scalable alternative building block for Vision Transformers.

## arxiv-2605.12487: Task-Adaptive Embedding Refinement via Test-time LLM Guidance

- Categories: cs.CL, cs.IR, cs.LG
- Authors: Ariel Gera, Shir Ashury-Tahan, Gal Bloch, Ohad Eytan, Assaf Toledo
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.12487
- PDF URL: https://arxiv.org/pdf/2605.12487

We explore the effectiveness of an LLM-guided query refinement paradigm for extending the usability of embedding models to challenging zero-shot search and classification tasks. Our approach refines the embedding representation of a user query using feedback from a generative LLM on a small set of documents, enabling embeddings to adapt in real time to the target task. We conduct extensive experiments with state-of-the-art text embedding models across a diverse set of challenging search and classification benchmarks. Empirical results indicate that LLM-guided query refinement yields consistent gains across all models and datasets, with relative improvements of up to +25% in literature search, intent detection, key-point matching, and nuanced query-instruction following. The refined queries improve ranking quality and induce clearer binary separation across the corpus, enabling the embedding space to better reflect the nuanced, task-specific constraints of each ad-hoc user query. Importantly, this expands the range of practical settings in which embedding models can be effectively deployed, making them a compelling alternative when costly LLM pipelines are not viable at corpus-scale. We release our experimental code for reproducibility, at https://github.com/IBM/task-aware-embedding-refinement.

## arxiv-2605.12484: Learning, Fast and Slow: Towards LLMs That Adapt Continually

- Categories: cs.LG, cs.AI
- Authors: Rishabh Tiwari, Kusha Sareen, Lakshya A Agrawal, Joseph E. Gonzalez, Matei Zaharia, Kurt Keutzer, Inderjit S Dhillon, Rishabh Agarwal, Devvrit Khatri
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.12484
- PDF URL: https://arxiv.org/pdf/2605.12484

Large language models (LLMs) are trained for downstream tasks by updating their parameters (e.g., via RL). However, updating parameters forces them to absorb task-specific information, which can result in catastrophic forgetting and loss of plasticity. In contrast, in-context learning with fixed LLM parameters can cheaply and rapidly adapt to task-specific requirements (e.g., prompt optimization), but cannot by itself typically match the performance gains available through updating LLM parameters. There is no good reason for restricting learning to being in-context or in-weights. Moreover, humans also likely learn at different time scales (e.g., System 1 vs 2). To this end, we introduce a fast-slow learning framework for LLMs, with model parameters as "slow" weights and optimized context as "fast" weights. These fast "weights" can learn from textual feedback to absorb the task-specific information, while allowing slow weights to stay closer to the base model and persist general reasoning behaviors. Fast-Slow Training (FST) is up to 3x more sample-efficient than only slow learning (RL) across reasoning tasks, while consistently reaching a higher performance asymptote. Moreover, FST-trained models remain closer to the base LLM (up to 70% less KL divergence), resulting in less catastrophic forgetting than RL-training. This reduced drift also preserves plasticity: after training on one task, FST trained models adapt more effectively to a subsequent task than parameter-only trained models. In continual learning scenarios, where task domains change on the fly, FST continues to acquire each new task while parameter-only RL stalls.

## arxiv-2605.12483: Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training

- Categories: cs.LG, cs.AI
- Authors: Yuanda Xu, Hejian Sang, Zhengze Zhou, Ran He, Zhipeng Wang, Alborz Geramifard
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.12483
- PDF URL: https://arxiv.org/pdf/2605.12483

In settings where labeled verifiable training data is the binding constraint, each checked example should be allocated carefully. The standard practice is to use this data directly on the model that will be deployed, for example by running GRPO on the deployment student. We argue that this is often an inefficient allocation because it overlooks a reward-density principle: sparse sequence-level reward should train models where exploration is productive, while dense token-level teacher reward should be used where the aim is to compress behavior into a smaller model. In this view, GRPO-style sparse RL and OPD-style dense teacher supervision are not separate recipes; they are different reward-density regimes. The allocation rule is simple: use scarce labeled training data upstream on the strongest model that can turn it into reward-shaped behavior, then transfer that behavior downstream as dense supervision. We evaluate this rule on verifiable math with Qwen3 and Llama models. At fixed Qwen3-1.7B deployment-student size, an RL-improved 8B teacher distilled through the dense bridge outperforms direct GRPO on the same student, while transfer from the same teacher before RL underperforms. The bridge is important: a forward-KL warmup on teacher rollouts followed by OPD on student rollouts is consistently strongest on MATH before any post-bridge student-side sparse RL, and also gives the best pre-Stage~3 AIME endpoints for the canonical 8B/14B teachers. The bridge also makes later student-side sparse RL effective: GRPO that is weak on a cold student lifts MATH from $75.4\%$ to $78.5\%$ after the bridge and outperforms a matched replay control by $2.8$ points. The operational principal is to avoid using scarce labeled data on the least prepared policy: use sparse reward for teacher-side discovery, dense transfer for student compression, and student-side sparse reward only after the bridge.

## arxiv-2605.12481: ToolCUA: Towards Optimal GUI-Tool Path Orchestration for Computer Use Agents

- Categories: cs.AI
- Authors: Xuhao Hu, Xi Zhang, Haiyang Xu, Kyle Qiao, Jingyi Yang, Xuanjing Huang, Jing Shao, Ming Yan, Jieping Ye
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.12481
- PDF URL: https://arxiv.org/pdf/2605.12481

Computer Use Agents (CUAs) can act through both atomic GUI actions, such as click and type, and high-level tool calls, such as API-based file operations, but this hybrid action space often leaves them uncertain about when to continue with GUI actions or switch to tools, leading to suboptimal execution paths. This difficulty stems from the scarcity of high-quality interleaved GUI-Tool trajectories, the cost and brittleness of collecting real tool trajectories, and the lack of trajectory-level supervision for GUI-Tool path selection. In this paper, we propose ToolCUA, an end-to-end agent designed to learn optimal GUI-Tool path selection through a staged training paradigm. We first introduce an Interleaved GUI-Tool Trajectory Scaling Pipeline that repurposes abundant static GUI trajectories and synthesizes a grounded tool library, enabling diverse GUI-Tool trajectories without manual engineering or real tool-trajectory collection. We then perform Tool-Bootstrapped GUI RFT, combining warmup SFT with single-turn RL to improve decisions at critical GUI-Tool switching points. Finally, we optimize ToolCUA with Online Agentic RL in a high-fidelity GUI-Tool environment, guided by a Tool-Efficient Path Reward that encourages appropriate tool use and shorter execution paths. Experiments on OSWorld-MCP show that ToolCUA achieves 46.85% accuracy, a relative improvement of approximately 66% over the baseline, establishing a new state of the art among models of comparable scale. It also improves by 3.9% over GUI-only settings, demonstrating effective GUI-Tool orchestration. The results further suggest that training in a hybrid action space is a promising paradigm for real-world digital agents. Open-sourced here: https://x-plug.github.io/ToolCUA/

## arxiv-2605.12480: OmniNFT: Modality-wise Omni Diffusion Reinforcement for Joint Audio-Video Generation

- Categories: cs.CV, cs.AI
- Authors: Guohui Zhang, XiaoXiao Ma, Jie Huang, Hang Xu, Hu Yu, Siming Fu, Yuming Li, Zeyue Xue, Lin Song, Haoyang Huang, Nan Duan, Feng Zhao
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.12480
- PDF URL: https://arxiv.org/pdf/2605.12480

Recent advances in joint audio-video generation have been remarkable, yet real-world applications demand strong per-modality fidelity, cross-modal alignment, and fine-grained synchronization. Reinforcement Learning (RL) offers a promising paradigm, but its extension to multi-objective and multi-modal joint audio-video generation remains unexplored. Notably, our in-depth analysis first reveals that the primary obstacles to applying RL in this stem from: (i) multi-objective advantages inconsistency, where the advantages of multimodal outputs are not always consistent within a group; (ii) multi-modal gradients imbalance, where video-branch gradients leak into shallow audio layers responsible for intra-modal generation; (iii) uniform credit assignment, where fine-grained cross-modal alignment regions fail to get efficient exploration. These shortcomings suggest that vanilla RL fine-tuning strategy with a single global advantage often leads to suboptimal results. To address these challenges, we propose OmniNFT, a novel modality-aware online diffusion RL framework with three key innovations: (1) Modality-wise advantage routing, which routes independent per-reward advantages to their respective modality generation branches. (2) Layer-wise gradient surgery, which selectively detaches video-branch gradients on shallow audio layers while retaining those for cross-modal interaction layers. (3) Region-wise loss reweighting, which modulates policy optimization toward critical regions related to audio-video synchronization and fine-grained alignment. Extensive experiments on JavisBench and VBench with the LTX-2 backbone demonstrate that OmniNFT achieves comprehensive improvements in audio and video perceptual quality, cross-modal alignment, and audio-video synchronization.

## arxiv-2605.12477: MEME: Multi-entity & Evolving Memory Evaluation

- Categories: cs.LG, cs.CL
- Authors: Seokwon Jung, Alexander Rubinstein, Arnas Uselis, Sangdoo Yun, Seong Joon Oh
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.12477
- PDF URL: https://arxiv.org/pdf/2605.12477

LLM-based agents increasingly operate in persistent environments where they must store, update, and reason over information across many sessions. While prior benchmarks evaluate only single-entity updates, MEME defines six tasks spanning the full space defined by the multi-entity and evolving axes, including three not scored by prior work: Cascade and Absence (dependency reasoning) and Deletion (post-removal state). Evaluating six memory systems spanning three memory paradigms on 100 controlled episodes, we find that all systems collapse on dependency reasoning under the default configuration (Cascade: 3%, Absence: 1% in average accuracy) despite adequate static retrieval performance. Prompt optimization, deeper retrieval, reduced filler noise, and most stronger LLMs fail to close this gap. Only a file-based agent paired with Claude Opus 4.7 as its internal LLM partially closes the gap, but at ~70x the baseline cost, indicating closure currently depends on configurations that are not practical at scale. Code and data are available on the project page: https://seokwonjung-jay.github.io/meme-eval/.
