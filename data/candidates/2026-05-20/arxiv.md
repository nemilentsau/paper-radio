# arxiv Candidates For 2026-05-20

## arxiv-2605.20182: Atoms of Thought: Universal EEG Representation Learning with Microstates

- Categories: cs.LG, cs.AI
- Authors: Xinyang Tian, Ruitao Liu, Ziyi Ye, Siyang Xue, Xin Wang, Xuesong Chen
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.20182
- PDF URL: https://arxiv.org/pdf/2605.20182

Learning universal representations from electroencephalogram (EEG) signals is a cutting-edge approach in the field of neuroinformatics and brain-computer interfaces (BCIs). Conventionally, EEG is treated as a multivariate temporal signal, where time- or frequency-domain features are extracted for representation learning. This paper investigates a simple yet effective EEG representation, i.e., microstates. Microstates represent the building blocks of brain activity patterns at a microscopic time scale. We build a universal microstate tokenizer from a large medical EEG dataset by clustering continuous EEG signals into sequences of discrete microstates. The microstate tokenizer is then adopted universally across a series of downstream tasks, including sleep staging, emotion recognition, and motor imagery classification. Experimental results show that EEG representation learning with microstates outperforms traditional time-domain and frequency-domain features under different models and across different tasks. Further analysis shows that microstates offer greater interpretability and scalability, thereby opening up applications in both cognitive neuroscience and clinical research.

## arxiv-2605.20179: TIDE: Efficient and Lossless MoE Diffusion LLM Inference with I/O-aware Expert Offload

- Categories: cs.CL
- Authors: Zhiben Chen, Youpeng Zhao, Yang Sui, Jun Wang, Yuzhang Shang
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.20179
- PDF URL: https://arxiv.org/pdf/2605.20179

Diffusion Large Language Models (dLLMs) have emerged as a competitive alternative to autoregressive (AR) models, offering better hardware utilization and bidirectional context through parallel block-level decoding. However, as dLLMs continue to scale up with mixture-of-experts (MoE) architectures, their deployment on resource-constrained devices remains an open challenge. Existing AR-based methods often incur either prohibitive I/O overhead or significant compute bottlenecks. In this work, we propose TIDE, a novel resource-efficient inference system that leverages the temporal stability of expert activations during the diffusion process within the block. Specifically, we leverage the temporal stability of expert activations during the diffusion process within the block and introduce an interval-based expert refresh strategy that updates the expert placement in an I/O-aware fashion. To ensure optimal performance, we formulate the inference scheduling as a mathematical programming problem, solving for the optimal interval that minimizes I/O traffic and CPU computation. Most importantly, TIDE is a lossless optimization that requires no model training, providing a "free lunch" acceleration for dLLM inference. In a single GPU-CPU system, we demonstrate that TIDE achieves up to 1.4$\times$ and 1.5$\times$ throughput improvements over prior baselines on LLaDA2.0-mini and LLaDA2.0-flash models, respectively.

## arxiv-2605.20177: From Seeing to Thinking: Decoupling Perception and Reasoning Improves Post-Training of Vision-Language Models

- Categories: cs.CL, cs.CV
- Authors: Juncheng Wu, Hardy Chen, Haoqin Tu, Xianfeng Tang, Freda Shi, Hui Liu, Hanqing Lu, Cihang Xie, Yuyin Zhou
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.20177
- PDF URL: https://arxiv.org/pdf/2605.20177

Recent advances in vision-language models (VLMs) emphasize long chain-of-thought reasoning; yet, we find that their performance on visual tasks is primarily limited by a lack of visual perception as opposed to reasoning itself. In this work, we systematically study the interplay between perception and reasoning in VLM post-training by decomposing their capabilities into three separate training stages: visual perception, visual reasoning, and textual reasoning, incorporating specialized training data. We demonstrate that visual perception (a) requires targeted optimization with specialized data; (b) serves as a fundamental scaffold that should be solidified through staged training before refining visual reasoning; and (c) is more effectively learned via RL than caption-based SFT. Our experiments across multiple VLMs demonstrate that staged training consistently improves both visual perception and reasoning performance over merged training. Notably, models trained with our approach achieve 1.5% higher reasoning accuracy with 20.8% shorter reasoning traces, suggesting that superior perception reduces the need for excessive reasoning. Furthermore, we show that this capability-based staging represents a new curriculum dimension orthogonal to traditional difficulty-based curricula, and combining both yields further additive gains. Our staged-training models achieve superior performance among open-weight VLMs, establishing advanced results on several visual math and perception (e.g., +5.2% on WeMath and +3.7% on RealWorldQA) tasks compared with the base counterpart.

## arxiv-2605.20176: ClinSeekAgent: Automating Multimodal Evidence Seeking for Agentic Clinical Reasoning

- Categories: cs.CL
- Authors: Juncheng Wu, Letian Zhang, Yuhan Wang, Haoqin Tu, Hardy Chen, Zijun Wang, Cihang Xie, Yuyin Zhou
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.20176
- PDF URL: https://arxiv.org/pdf/2605.20176

Large language models (LLMs) and agentic systems have shown promise for clinical decision support, but existing works largely assume that evidence has already been curated and handed to the model. Real-world clinical workflows instead require agents to actively seek, iteratively plan, and synthesize multimodal evidence from heterogeneous sources. In this paper, we introduce ClinSeekAgent, an automated agentic framework for dynamic multimodal evidence seeking that shifts the paradigm from passive evidence consumption to active evidence acquisition. Given only a clinical query and access to raw data sources, ClinSeekAgent gathers evidence by querying medical knowledge bases, navigating raw EHRs, and invoking medical imaging tools; refines its hypotheses as new information emerges; and integrates the collected evidence into grounded clinical decisions. ClinSeekAgent serves both as an inference-time agent for frontier LLMs and as a training-time pipeline for distilling high-quality agent trajectories into compact open-source models. To validate its inference-time effectiveness, we construct ClinSeek-Bench, which pairs Curated Input reasoning from fixed pre-selected evidence with Automated Evidence-Seeking over raw clinical data. On text-only EHR tasks, ClinSeekAgent improves Claude Opus 4.6 from 60.0 to 63.2 overall F1 and MiniMax M2.5 from 43.1 to 47.3, with positive risk-prediction gains in 7 out of 9 evaluated host models. On multimodal tasks, ClinSeekAgent improves Claude Opus 4.6 from 47.5 to 62.6 (+15.1); all evaluated models improve across the three CXR-related task groups. We further validate ClinSeekAgent as a training pipeline by distilling agentic evidence-seeking trajectories into ClinSeek-35B-A3B, which achieves 34.0 average F1 on existing AgentEHR-Bench, improving over its Qwen3.5-35B-A3B baseline by +11.9 points and approaching Claude Opus 4.6.

## arxiv-2605.20174: Multi-axis Analysis of Image Manipulation Localization

- Categories: cs.CV, cs.LG
- Authors: Keanu Nichols, Divya Appapogu, Giscard Biamby, Dina Bashkirova, Anna Rohrbach, Bryan A. Plummer
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.20174
- PDF URL: https://arxiv.org/pdf/2605.20174

Advanced image editing software enables easy creation of highly convincing image manipulations, which has been made even more accessible in recent years due to advances in generative AI. Manipulated images, while often harmless, could spread misinformation, create false narratives, and influence people's opinions on important issues. Despite this growing threat, there is limited research on detecting advanced manipulations across different visual domains. Thus, we introduce Analysis Under Domain-shifts, qualIty, Type, and Size (AUDITS), a comprehensive benchmark designed for studying axes of analysis in image manipulation detection. AUDITS comprises over 530K images from two distinct sources (user and news photos). We curate our dataset to support analysis across multiple axes using recent diffusion-based inpaintings, spanning a diverse range of manipulation types and sizes. We conduct experiments under different types of domain shift to evaluate robustness of existing image manipulation detection methods. Our goal is to drive further research in this area by offering new insights that would help develop more reliable and generalizable image manipulation detection methods.

## arxiv-2605.20173: A Methodology for Selecting and Composing Runtime Architecture Patterns for Production LLM Agents

- Categories: cs.AI, cs.SE
- Authors: Vasundra Srinivasan
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.20173
- PDF URL: https://arxiv.org/pdf/2605.20173

Production LLM agents combine stochastic model outputs with deterministic software systems, yet the boundary between the two is rarely treated as a first-class architectural object. This paper names that boundary the stochastic-deterministic boundary (SDB): a four-part contract among a proposer, verifier, commit step, and reject signal that specifies how an LLM output becomes a system action. We argue that the SDB is the load-bearing primitive of production agent runtimes. Around this primitive, we organize agent runtime design into three concerns: Coordination, State, and Control. We present a catalog of six runtime patterns that compose the SDB differently across conversational, autonomous, and long-horizon agents: hierarchical delegation, scatter-gather plus saga, event-driven sequencing, shared state machine, supervisor plus gate, and human in the loop. For each pattern, we trace its lineage to distributed-systems concepts and identify what changes when the worker is stochastic. The paper contributes a five-step methodology for selecting runtime patterns, a diagnostic procedure that maps production failures to pattern weaknesses, and a failure mode called replay divergence, in which LLM-based consumers of a deterministic event log produce different downstream outputs under model-version or prompt changes. A stylized reliability decomposition separates per-call model variance from architectural momentum, motivating the claim that as model variance decreases, pattern choice and SDB strength become increasingly important levers for long-run reliability. We apply the methodology to five workloads and provide one runnable reference implementation for a 90-day contract-renewal agent.

## arxiv-2605.20172: Long-term Power Grid Planning via Answer Set Programming

- Categories: cs.LO, cs.AI
- Authors: Antonio Ielo, Francesco Doria, Sandra Castellanos-Paez, Marco Maratea, Francesco Percassi, Mauro Vallati
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.20172
- PDF URL: https://arxiv.org/pdf/2605.20172

The Power grid is a critical infrastructure underpinning all aspects of modern society and its services. Maintaining its effectiveness requires continuous adaptations. In particular, addressing sustainability targets, demand patterns, and urbanisation trends requires implementing changes to the network. Actual developments can potentially span over a decade, with supply continuity and service quality that must be preserved throughout by ensuring conformance to several topological and combinatorial invariants. Long-term power grid planning deals with the above process, and although planning languages could be a natural choice, the kind of properties and invariants needed are cumbersome to express in such languages; on the contrary, they can be elegantly and succinctly encoded in Answer Set Programming (ASP). In this paper, we propose the first approach to automate and optimise the long-term power grid planning process using ASP. Experimental evaluations conducted on synthetic and real-world grid data confirm the expressive power of the proposed ASP-based approach and demonstrate its effectiveness.

## arxiv-2605.20170: KoRe: Compact Knowledge Representations for Large Language Models

- Categories: cs.CL
- Authors: Davide Cavicchini, Fausto Giunchiglia, Jacopo Staiano
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.20170
- PDF URL: https://arxiv.org/pdf/2605.20170

Modern Large Language Models (LLMs) have shown impressive performances in user-facing tasks such as question answering, as well as consistent improvements in reasoning capabilities. Still, the way these models encode knowledge seems inherently flawed: by design, LLMs encode world-knowledge within their parameters. This way of representing knowledge is inherently opaque, difficult to debug and update, and prone to hallucinations. On the other hand, Knowledge Graphs can provide human-readable and easily editable world knowledge representations, and their application in knowledge-intensive tasks has consistently proven beneficial to downstream performance. Nonetheless, current integration techniques require extensive retraining or finetuning. To overcome this issue, we introduce KoRe, a methodology to encode 1-hop sub-graphs into compact discrete knowledge tokens and inject them into a LLM backbone. We test the proposed approach on three established benchmarks, and report competitive performances coupled with a significant reduction (up to 10x) in token usage. Our results show that compact discrete KG representations can efficiently and effectively be used to ground modern LLMs.

## arxiv-2605.20167: HaorFloodAlert: Deseasonalized ML Ensemble for 72-Hour Flood Prediction in Bangladesh Haor Wetlands

- Categories: cs.AI, cs.LG
- Authors: Salma Hoque Talukdar Koli, Fahima Haque Talukder Jely, Md. Samiul Alim, Md. Zakir Hossen
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.20167
- PDF URL: https://arxiv.org/pdf/2605.20167

Flash floods in Bangladesh's haor wetlands show up with almost no warning. They wreck the annual boro rice harvest. Current setups, built for riverine floods, miss backwater dynamics entirely. These basins are flat. Water does not behave like it does on the Brahmaputra. We built HaorFloodAlert, a deseasonalized machine learning ensemble that forecasts 72-hour flood probability for the Sunamganj Haor (approximately 8,000 km2). Temperature was acting as a seasonal cheat code - it inflated accuracy by 6.9 pp just because floods happen in warm months. We caught that. We also built an upstream Barak River Sentinel-1 SAR proxy from Silchar, Assam, giving about 36 hours of lead time. Otsu-thresholded SAR change detection validates at 84-91 percent spatial match. The operational ensemble (RF 0.5625 + XGBoost 0.4375) hits 89.6 percent LOOCV accuracy, 87.5 percent recall, and 0.943 AUC-ROC on 77 real Sentinel-1 events. A three-tier alert pipeline and a BRRI-calibrated boro rice damage estimator are included.

## arxiv-2605.20164: Not Every Rubric Teaches Equally: Policy-Aware Rubric Rewards for RLVR

- Categories: cs.AI
- Authors: Utkarsh Tyagi, Xingang Guo, MohammadHossein Rezaei, Daniel George, Anas Mahmoud, Jackson Lee, Bing Liu, Yunzhong He
- Author affiliations: unknown
- Trusted org matches: none
- Abstract URL: https://arxiv.org/abs/2605.20164
- PDF URL: https://arxiv.org/pdf/2605.20164

Reinforcement learning with verifiable rewards has made post-training highly effective when correctness can be checked automatically. However, many important model behaviors require satisfying several qualitative criteria at once. Rubric-based rewards address this setting by grading prompt-specific criteria and aggregating them into a scalar reward. Yet standard static aggregations conflate a criterion's human-assigned importance with its current usefulness as an optimization signal. We show that this assumption breaks down in rubric RL: many important criteria are already saturated or currently unreachable, while criteria that distinguish rollouts are not necessarily those with the largest human weights. We introduce POW3R, a policy-aware rubric reward framework that preserves human weights and category balance as the rubric objective while adapting criterion-level reward weights during training. POW3R uses rollout-level contrast to emphasize criteria that currently separate the policy's outputs, making the GRPO reward more informative without changing the underlying evaluation target. Across three base policies on two datasets spanning multimodal and text-only settings, POW3R wins $24$ of $30$ base-policy/metric comparisons, improving both mean rubric reward and strict completion (the fraction of prompts whose response satisfies every required rubric criterion) over vanilla GRPO with rubric rewards, and reaches the same plateau in $2.5$--$4\times$ fewer training steps. Rubric rewards should therefore distinguish what should matter in the final answer from what can teach the current policy.
