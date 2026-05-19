# arxiv Candidates For 2026-05-19

## arxiv-2605.18753: DashAttention: Differentiable and Adaptive Sparse Hierarchical Attention

- Categories: cs.CL, cs.AI, cs.LG
- Authors: Yuxiang Huang, Nuno M. T. Gonçalves, Federico Alvetreti, Lei Li, Xu Han, Edoardo M. Ponti, André F. T. Martins, Marcos V. Treviso
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.18753
- PDF URL: https://arxiv.org/pdf/2605.18753

Current hierarchical attention methods, such as NSA and InfLLMv2, select the top-k relevant key-value (KV) blocks based on coarse attention scores and subsequently apply fine-grained softmax attention on the selected tokens. However, the top-k operation assumes the number of relevant tokens for any query is fixed and it precludes the gradient flow between the sparse and dense stages. In this work, we propose DashAttention (Differentiable and Adaptive Sparse Hierarchical Attention), which leverages the adaptively sparse $α$-entmax transformation to select a variable number of blocks according to the current query in the first stage. This in turn provides a prior for the second-stage softmax attention, keeping the entire hierarchy fully differentiable. Contrary to other hierarchical attention methods, we show that DashAttention is non-dispersive, translating to better long-context modeling ability. Experiments with large language models (LLMs) show that DashAttention achieves comparable accuracy as full attention with 75% sparsity and a better Pareto frontier than NSA and InfLLMv2, especially in high-sparsity regimes. We also provide an efficient, GPU-aware implementation of DashAttention in Triton, which achieves a speedup of up to over FlashAttention-3 at inference time. Overall, DashAttention offers a cost-effective strategy to model long contexts.

## arxiv-2605.18750: A Readiness-Driven Runtime for Pipeline-Parallel Training under Runtime Variability

- Categories: cs.DC, cs.LG
- Authors: Ruitao Liu, Xinyang Tian, Shuo Chen, Tingrui Zhang, Guang Yang, Alan Zhao, Wei Xu
- Author affiliations: Tsinghua University, Scitix AI
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.18750
- PDF URL: https://arxiv.org/pdf/2605.18750

Pipeline parallelism is a key technique for scaling large-model training, but modern workloads exhibit runtime variability in computation and communication. Existing pipeline systems typically consume static, profiled, or adaptively generated schedules as pre-committed execution orders. When realized task readiness diverges from the pre-committed order, stages may wait for not-yet-ready work even though other executable work is available, creating stage misalignment, idle bubbles, and reduced utilization. We present Runtime-Readiness-First Pipeline (RRFP), a readiness-driven runtime for pipeline-parallel training. RRFP changes how schedules are consumed at runtime: instead of treating a schedule as a sequence that stages must wait to follow, it treats the schedule as a non-binding hint order for ranking currently ready work. To support this model, RRFP combines message-driven asynchronous communication, lightweight tensor-parallel coordination for collective consistency, and ready-set arbitration for low-overhead dispatch. We implement RRFP in a Megatron-based training framework and evaluate it on language-only and multimodal workloads at up to 128 GPUs. RRFP improves over fixed-order pipeline baselines across all settings. Using the BFW hint, RRFP achieves up to 1.77$\times$ speedup on language-only workloads and up to 2.77$\times$ on multimodal workloads. In cross-framework comparisons, RRFP with the default BF hint outperforms the faster available external system by up to 1.84$\times$ while preserving training correctness.

## arxiv-2605.18747: Code as Agent Harness

- Categories: cs.CL, cs.AI
- Authors: Xuying Ning, Katherine Tieu, Dongqi Fu, Tianxin Wei, Zihao Li, Yuanchen Bei, Jiaru Zou, Mengting Ai, Zhining Liu, Ting-Wei Li, Lingjie Chen, Yanjun Zhao, Ke Yang, Bingxuan Li, Cheng Qian, Gaotang Li, Xiao Lin, Zhichen Zeng, Ruizhong Qiu, Sirui Chen, Yifan Sun, Xiyuan Yang, Ruida Wang, Rui Pan, Chenyuan Yang, Dylan Zhang, Liri Fang, Zikun Cui, Yang Cao, Pan Chen, Dorothy Sun, Ren Chen, Mahesh Srinivasan, Nipun Mathur, Yinglong Xia, Hong Li, Hong Yan, Pan Lu, Lingming Zhang, Tong Zhang, Hanghang Tong, Jingrui He
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.18747
- PDF URL: https://arxiv.org/pdf/2605.18747

Recent large language models (LLMs) have demonstrated strong capabilities in understanding and generating code, from competitive programming to repository-level software engineering. In emerging agentic systems, code is no longer only a target output. It increasingly serves as an operational substrate for agent reasoning, acting, environment modeling, and execution-based verification. We frame this shift through the lens of agent harnesses and introduce code as agent harness: a unified view that centers code as the basis for agent infrastructure. To systematically study this perspective, we organize the survey around three connected layers. First, we study the harness interface, where code connects agents to reasoning, action, and environment modeling. Second, we examine harness mechanisms: planning, memory, and tool use for long-horizon execution, together with feedback-driven control and optimization that make harness reliable and adaptive. Third, we discuss scaling the harness from single-agent systems to multi-agent settings, where shared code artifacts support multi-agent coordination, review, and verification. Across these layers, we summarize representative methods and practical applications of code as agent harness, spanning coding assistants, GUI/OS automation, embodied agents, scientific discovery, personalization and recommendation, DevOps, and enterprise workflows. We further outline open challenges for harness engineering, including evaluation beyond final task success, verification under incomplete feedback, regression-free harness improvement, consistent shared state across multiple agents, human oversight for safety-critical actions, and extensions to multimodal environments. By centering code as the harness of agentic AI, this survey provides a unified roadmap toward executable, verifiable, and stateful AI agent systems.

## arxiv-2605.18746: ESI-Bench: Towards Embodied Spatial Intelligence that Closes the Perception-Action Loop

- Categories: cs.CV, cs.AI, cs.CL, cs.LG, cs.RO
- Authors: Yining Hong, Jiageng Liu, Han Yin, Manling Li, Leonidas Guibas, Li Fei-Fei, Jiajun Wu, Yejin Choi
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.18746
- PDF URL: https://arxiv.org/pdf/2605.18746

Spatial intelligence unfolds through a perception-action loop: agents act to acquire observations, and reason about how observations vary as a function of action. Rather than passively processing what is seen, they actively uncover what is unseen - occluded structure, dynamics, containment, and functionality that cannot be resolved from passive sensing alone. We move beyond prior formulations of spatial intelligence that assume oracle observations by recasting the observer as an actor. We introduce ESI-BENCH, a comprehensive benchmark for embodied spatial intelligence spanning 10 task categories and 29 subcategories built on OmniGibson, grounded in Spelke's core knowledge systems. Agents must decide what abilities to deploy - perception, locomotion, and manipulation - and how to sequence them to actively accumulate task-relevant evidence. We conduct extensive experiments on state-of-the-art MLLMs and find that active exploration substantially outperforms passive counterparts, with agents spontaneously discovering emergent spatial strategies without explicit instructions, while random multi-view often adds noise rather than signal despite consuming far more images. Most failures stem not from weak perception but from action blindness: poor action choices lead to poor observations, which in turn drive cascading errors. While explicit 3D grounding stabilizes reasoning on depth-sensitive tasks, imperfect 3D representation proves more harmful than 2D baselines by distorting spatial relations. Human studies further reveal that unlike humans who seek falsifying viewpoints and revise beliefs under contradiction, models commit prematurely with high confidence regardless of evidence quality, exposing a metacognitive gap that neither better perception nor more embodied interaction alone can close.

## arxiv-2605.18745: SURGE: Approximation-free Training Free Particle Filter for Diffusion Surrogate

- Categories: stat.ML, cs.LG, math.NA, math.PR, q-fin.MF, stat.CO
- Authors: Lifu Wei, Yinuo Ren, Naichen Shi, Yiping Lu
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.18745
- PDF URL: https://arxiv.org/pdf/2605.18745

Diffusion-based generative models increasingly rely on inference-time guidance, adding a drift term or reweighting mixture of experts, to improve sample quality on task-specific objectives. However, most existing techniques require repeated score or gradient evaluations, introducing bias, high computational overhead, or both. We introduce \texttt{URGE}, Unbiased Resampling via Girsanov Estimation, a derivative-free inference-time scaling algorithm that performs path-wise importance reweighting via a Girsanov change of measure. Instead of computing gradient-based particle weights in previous work, \texttt{URGE} attaches a simple multiplicative weight to each simulated trajectory and periodically resamples. No score, no Hessian, and no PDE evaluation is required. We establish an equivalence between path-wise and particle-wise SMC: the Girsanov path weight admits a backward conditional expectation that recovers the previous particle-level weights, guaranteeing that both schemes produce the same unbiased terminal law. Empirically, \texttt{URGE} outperforms existing inference-time guidance baselines on synthetic tests and diffusion-model benchmarks, achieving better generation quality, while being significantly simpler to implement and fully gradient-free.

## arxiv-2605.18743: Actionable World Representation

- Categories: cs.AI
- Authors: Kunqi Xu, Jitao Li, Jianglong Ye, Tianshu Tang, Isabella Liu, Sifei Liu, Xueyan Zou
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.18743
- PDF URL: https://arxiv.org/pdf/2605.18743

Inspired by the emergent behaviors in large language models that generalized human intelligence, the research community is pursuing similar emergent capabilities within world models, with a emphasis on modeling the physical world. Within the scope of physical world model, objects are the fundamental primitives that constitute physical reality. From humans to computers, nearly everything we interact with is an object. These objects are rarely static; they are actionable entities with varying states determined by their intrinsic properties. While current methods approach object action states either via video generation or dynamic scene reconstruction, none explicitly model this basic element in a unified, principled way to build an actionable object representation. We propose WorldString, a neural architecture capable of modeling the state manifold of real-world objects by learning directly from point clouds or RGB-D video streams. Serving as a versatile digital twin, it acts as a foundational building block for physical world models; thus, we name it WorldString. Sweetly, its fully differentiable structure seamlessly enables future integration with policy learning and neural dynamics.

## arxiv-2605.18740: Vision-OPD: Learning to See Fine Details for Multimodal LLMs via On-Policy Self-Distillation

- Categories: cs.CV, cs.AI, cs.CL, cs.LG
- Authors: Qianhao Yuan, Jie Lou, Xing Yu, Hongyu Lin, Le Sun, Xianpei Han, Yaojie Lu
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.18740
- PDF URL: https://arxiv.org/pdf/2605.18740

Multimodal Large Language Models (MLLMs) still struggle with fine-grained visual understanding, where answers often depend on small but decisive evidence in the full image. We observe a regional-to-global perception gap: the same MLLM answers fine-grained questions more accurately when conditioned on evidence-centered crops than on the corresponding full images, suggesting that many failures stem from difficulty to focus on relevant evidence rather than insufficient local recognition ability. Motivated by this observation, we propose Vision-OPD (Vision On-Policy Distillation), a regional-to-global self-distillation framework that transfers the model's own privileged regional perception to its full-image policy. Vision-OPD instantiates two conditional policies from the same MLLM: a crop-conditioned teacher and a full-image-conditioned student. The student generates on-policy rollouts, and Vision-OPD minimizes token-level divergence between the teacher and student next-token distributions along these rollouts. This enables the model to internalize the benefit of visual zooming without external teacher models, ground-truth labels, reward verifiers, or inference-time tool use. Experiments on multiple fine-grained visual understanding benchmarks show that Vision-OPD models achieve competitive or superior performance against much larger open-source, closed-source, and "Thinking-with-Images" agentic models.

## arxiv-2605.18738: What Does the AI Doctor Value? Auditing Pluralism in the Clinical Ethics of Language Models

- Categories: cs.AI
- Authors: Payal Chandak, Victoria Alkin, David Wu, Maya Dagan, Taposh Dutta Roy, Maria Clara Saad Menezes, Ayush Noori, Nirali Somia, John S. Brownstein, Ran Balicer, Rebecca W. Brendel, Noa Dagan, Isaac S. Kohane, Gabriel A. Brat
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.18738
- PDF URL: https://arxiv.org/pdf/2605.18738

Medicine is inherently pluralistic. Principles such as autonomy, beneficence, nonmaleficence, and justice routinely conflict, and such ethical dilemmas often sharply divide reasonable physicians. Good clinical practice navigates these tensions in concert with each patient's values rather than imposing a single ethical stance. The ethical values that large language models bring to medical advice, however, have not been systematically examined. We present a framework for auditing value pluralism in medical AI, comprising a benchmark of clinician-verified dilemmas and an attribution method that recovers value priorities directly from decisions. The ecosystem of frontier models spans physician-level value heterogeneity, and models discuss competing values in their reasoning (Overton pluralism) before committing to a decision. However, individual model decisions are near-deterministic across repeated sampling and semantic variations, failing to reproduce the distributional pluralism of the physician panel. Across benchmark cases, these consistent decisions reflect committed, systematic value preferences. While most model priorities fall within the natural range of inter-physician variation, some significantly underweight patient autonomy. A single LLM deployed without regard for its value priorities could amplify those priorities at scale to every patient it serves. Without explicit efforts to balance ethical perspectives with one or multiple models, these tools risk replacing clinical pluralism with a deployment monoculture.

## arxiv-2605.18735: PIXLRelight: Controllable Relighting via Intrinsic Conditioning

- Categories: cs.CV, cs.GR, cs.LG
- Authors: Miguel Farinha, Ronald Clark
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.18735
- PDF URL: https://arxiv.org/pdf/2605.18735

We present PIXLRelight, a feed-forward approach for physically controllable single-image relighting. Existing methods either provide limited lighting control (e.g. through text or environment maps), accumulate errors when chaining inverse and forward rendering, or require costly per-image optimization. Our key idea is to bridge physically based rendering (PBR) and learned image synthesis through a shared intrinsic conditioning that can be obtained from either real photographs or PBR renders. At training time, paired multi-illumination photographs are decomposed into albedo, diffuse shading, and non-diffuse residuals, which condition the model. At inference time, the same conditioning is computed from a path-traced render of a coarse 3D reconstruction of the input under user-specified PBR lights. A transformer-based neural renderer then applies the target illumination to the source photograph, preserving fine image detail through a per-pixel affine modulation. PIXLRelight enables arbitrary PBR-style lighting control, achieves state-of-the-art relighting quality, and runs in under a tenth of a second per image. Code and models are available at https://mlfarinha.github.io/pixl-relight/.

## arxiv-2605.18732: Predictable Confabulations: Factual Recall by LLMs Scales with Model Size and Topic Frequency

- Categories: cs.CL, cs.AI, cs.LG
- Authors: Matthew L. Smith, Jonathan P. Shock, Samuel T. Segun, Iyiola E. Olatunji, Tegawendé F. Bissyandé
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.18732
- PDF URL: https://arxiv.org/pdf/2605.18732

While scaling laws govern aggregate large language model performance, no scaling law has linked factual recall to both model size and training-data composition. We evaluated 38 models on over 8,900 scholarly references evaluated by an automated reference verification system. Recall quality follows a sigmoid in the log-linear combination of model parameter count and topic representation in training data. These two variables alone explain 60% of the variance across 16 dense models from four families, rising to 74-94% within individual families. The form matches a superposition-inspired account in which recall is gated by a signal-to-noise ratio: signal strength scales with concept frequency and the noise floor with model capacity.
