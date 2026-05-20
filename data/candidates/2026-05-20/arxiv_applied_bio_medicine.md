# arxiv_applied_bio_medicine Candidates For 2026-05-20

## arxiv-2605.20176: ClinSeekAgent: Automating Multimodal Evidence Seeking for Agentic Clinical Reasoning

- Categories: cs.CL
- Authors: Juncheng Wu, Letian Zhang, Yuhan Wang, Haoqin Tu, Hardy Chen, Zijun Wang, Cihang Xie, Yuyin Zhou
- Author affiliations: unknown
- Trusted org matches: none
- Applied domain: Bio, medicine, and clinical workflows
- Applied-domain score: 10
- Matched required domain terms: clinical, ehr, medical
- Matched model terms: llm, agent
- Matched LLM/domain keywords: llm, clinical, ehr, medical, multimodal
- Matched workflow terms: decision support, evidence, workflow
- Abstract URL: https://arxiv.org/abs/2605.20176
- PDF URL: https://arxiv.org/pdf/2605.20176

Large language models (LLMs) and agentic systems have shown promise for clinical decision support, but existing works largely assume that evidence has already been curated and handed to the model. Real-world clinical workflows instead require agents to actively seek, iteratively plan, and synthesize multimodal evidence from heterogeneous sources. In this paper, we introduce ClinSeekAgent, an automated agentic framework for dynamic multimodal evidence seeking that shifts the paradigm from passive evidence consumption to active evidence acquisition. Given only a clinical query and access to raw data sources, ClinSeekAgent gathers evidence by querying medical knowledge bases, navigating raw EHRs, and invoking medical imaging tools; refines its hypotheses as new information emerges; and integrates the collected evidence into grounded clinical decisions. ClinSeekAgent serves both as an inference-time agent for frontier LLMs and as a training-time pipeline for distilling high-quality agent trajectories into compact open-source models. To validate its inference-time effectiveness, we construct ClinSeek-Bench, which pairs Curated Input reasoning from fixed pre-selected evidence with Automated Evidence-Seeking over raw clinical data. On text-only EHR tasks, ClinSeekAgent improves Claude Opus 4.6 from 60.0 to 63.2 overall F1 and MiniMax M2.5 from 43.1 to 47.3, with positive risk-prediction gains in 7 out of 9 evaluated host models. On multimodal tasks, ClinSeekAgent improves Claude Opus 4.6 from 47.5 to 62.6 (+15.1); all evaluated models improve across the three CXR-related task groups. We further validate ClinSeekAgent as a training pipeline by distilling agentic evidence-seeking trajectories into ClinSeek-35B-A3B, which achieves 34.0 average F1 on existing AgentEHR-Bench, improving over its Qwen3.5-35B-A3B baseline by +11.9 points and approaching Claude Opus 4.6.

## arxiv-2605.20158: Rethinking Visual Attribution for Chest X-ray Reasoning in Large Vision Language Models

- Categories: cs.CV, cs.AI, cs.CL
- Authors: Guangzhi Xiong, Qiao Jin, Sanchit Sinha, Zhiyong Lu, Aidong Zhang
- Author affiliations: unknown
- Trusted org matches: none
- Applied domain: Bio, medicine, and clinical workflows
- Applied-domain score: 6
- Matched required domain terms: clinical, medical
- Matched model terms: lvlm
- Matched LLM/domain keywords: clinical, medical
- Matched workflow terms: evidence, expert
- Abstract URL: https://arxiv.org/abs/2605.20158
- PDF URL: https://arxiv.org/pdf/2605.20158

Large Vision Language Models (LVLMs) show promise in medical applications, but their inability to faithfully ground responses in visual evidence raises serious concerns about clinical trustworthiness. While visual attribution methods are widely used to explain LVLM predictions, whether these explanations actually reflect the visual evidence underlying the model's decision is largely unverified, since ground-truth annotations for internal model reasoning are typically unavailable. We address this question for chest X-ray (CXR) reasoning by developing a causal evaluation framework that retains only CXR-VQA samples for which the expert-annotated region is verified, via counterfactual editing, to be causally responsible for the model's prediction. Using this framework across 11 attribution methods, six open-source LVLMs, and two output modes (direct answer and step-by-step reasoning), we find that existing attribution methods often fail to identify the evidence used by LVLMs. To address this failure, we propose MedFocus, a concept-based attribution method that localizes clinically meaningful anatomical regions via unbalanced optimal transport and measures their causal effect on model outputs through targeted interventions. MedFocus produces spatial, concept-level, and token-level attributions and substantially outperforms prior methods, taking a step toward more trustworthy attribution for medical LVLMs. Our data and code are available at https://github.com/gzxiong/medfocus/.
