# SURGE: Approximation-free Training Free Particle Filter for Diffusion Surrogate

## Metadata
- Paper ID: arxiv-2605.18745
- Source: arxiv
- Source ID: 2605.18745
- Authors: Lifu Wei, Yinuo Ren, Naichen Shi, Yiping Lu
- Published: 2026-05-18T17:59:00Z
- Updated: 2026-05-18T17:59:00Z
- Categories: stat.ML, cs.LG, math.NA, math.PR, q-fin.MF, stat.CO
- Source signals: arxiv_recent
- Triage decision: queue_for_review
- Triage rationale: This looks like a technically substantive methods paper in a current ML area, with a clear algorithmic contribution and a plausible experimental payoff. It is worth review because the abstract makes a strong claim about an unbiased equivalence and simpler inference-time guidance, which is both research-relevant and potentially useful to critique on podcast.
- Research score estimate: 7.4
- Podcast score estimate: 6.8
- Local PDF path: data/papers/pdfs/arxiv-2605.18745.pdf
- Full text path: data/papers/fulltext/arxiv-2605.18745.txt
- Abstract URL: https://arxiv.org/abs/2605.18745
- PDF URL: https://arxiv.org/pdf/2605.18745

## Abstract
Diffusion-based generative models increasingly rely on inference-time guidance, adding a drift term or reweighting mixture of experts, to improve sample quality on task-specific objectives. However, most existing techniques require repeated score or gradient evaluations, introducing bias, high computational overhead, or both. We introduce \texttt{URGE}, Unbiased Resampling via Girsanov Estimation, a derivative-free inference-time scaling algorithm that performs path-wise importance reweighting via a Girsanov change of measure. Instead of computing gradient-based particle weights in previous work, \texttt{URGE} attaches a simple multiplicative weight to each simulated trajectory and periodically resamples. No score, no Hessian, and no PDE evaluation is required. We establish an equivalence between path-wise and particle-wise SMC: the Girsanov path weight admits a backward conditional expectation that recovers the previous particle-level weights, guaranteeing that both schemes produce the same unbiased terminal law. Empirically, \texttt{URGE} outperforms existing inference-time guidance baselines on synthetic tests and diffusion-model benchmarks, achieving better generation quality, while being significantly simpler to implement and fully gradient-free.
