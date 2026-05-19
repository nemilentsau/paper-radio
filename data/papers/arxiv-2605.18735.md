# PIXLRelight: Controllable Relighting via Intrinsic Conditioning

## Metadata
- Paper ID: arxiv-2605.18735
- Source: arxiv
- Source ID: 2605.18735
- Authors: Miguel Farinha, Ronald Clark
- Published: 2026-05-18T17:55:03Z
- Updated: 2026-05-18T17:55:03Z
- Categories: cs.CV, cs.GR, cs.LG
- Source signals: arxiv_recent
- Triage decision: queue_for_review
- Triage rationale: The abstract describes a concrete method with a clear technical contribution at the intersection of CV, graphics, and generative rendering, and it claims both controllability and real-time speed. It looks strong enough to merit review, but the claims are still purely self-reported here and the contribution is specialized rather than broadly episode-defining.
- Research score estimate: 7.2
- Podcast score estimate: 6.8
- Local PDF path: data/papers/pdfs/arxiv-2605.18735.pdf
- Full text path: data/papers/fulltext/arxiv-2605.18735.txt
- Abstract URL: https://arxiv.org/abs/2605.18735
- PDF URL: https://arxiv.org/pdf/2605.18735

## Abstract
We present PIXLRelight, a feed-forward approach for physically controllable single-image relighting. Existing methods either provide limited lighting control (e.g. through text or environment maps), accumulate errors when chaining inverse and forward rendering, or require costly per-image optimization. Our key idea is to bridge physically based rendering (PBR) and learned image synthesis through a shared intrinsic conditioning that can be obtained from either real photographs or PBR renders. At training time, paired multi-illumination photographs are decomposed into albedo, diffuse shading, and non-diffuse residuals, which condition the model. At inference time, the same conditioning is computed from a path-traced render of a coarse 3D reconstruction of the input under user-specified PBR lights. A transformer-based neural renderer then applies the target illumination to the source photograph, preserving fine image detail through a per-pixel affine modulation. PIXLRelight enables arbitrary PBR-style lighting control, achieves state-of-the-art relighting quality, and runs in under a tenth of a second per image. Code and models are available at https://mlfarinha.github.io/pixl-relight/.
