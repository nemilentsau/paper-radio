# Elastic Attention Cores for Scalable Vision Transformers

## Metadata
- Paper ID: arxiv-2605.12491
- Source: arxiv
- Source ID: 2605.12491
- Authors: Alan Z. Song, Yinjie Chen, Mu Nan, Rui Zhang, Jiahang Cao, Weijian Mai, Muquan Yu, Hossein Adeli, Deva Ramanan, Michael J. Tarr, Andrew F. Luo
- Published: 2026-05-12T17:59:26Z
- Updated: 2026-05-12T17:59:26Z
- Categories: cs.CV, cs.LG
- Source signals: arxiv_recent
- Triage decision: queue_for_review
- Triage rationale: This looks like a substantive architecture paper with a clear technical claim about reducing ViT attention complexity and an explicit tradeoff mechanism for compute versus accuracy. It is also likely useful for review because it targets a well-known bottleneck in vision transformers and could have both research and discussion value if the reported gains hold.
- Research score estimate: 7.6
- Podcast score estimate: 7.1
- Local PDF path: data/papers/pdfs/arxiv-2605.12491.pdf
- Full text path: data/papers/fulltext/arxiv-2605.12491.txt
- Abstract URL: https://arxiv.org/abs/2605.12491
- PDF URL: https://arxiv.org/pdf/2605.12491

## Abstract
Vision Transformers (ViTs) achieve strong data-driven scaling by leveraging all-to-all self-attention. However, this flexibility incurs a computational cost that scales quadratically with image resolution, limiting ViTs in high-resolution domains. Underlying this approach is the assumption that pairwise token interactions are necessary for learning rich visual-semantic representations. In this work, we challenge this assumption, demonstrating that effective visual representations can be learned without any direct patch-to-patch interaction. We propose VECA (Visual Elastic Core Attention), a vision transformer architecture that uses efficient linear-time core-periphery structured attention enabled by a small set of learned cores. In VECA, these cores act as a communication interface: patch tokens exchange information exclusively through the core tokens, which are initialized from scratch and propagated across layers. Because the $N$ image patches only directly interact with a resolution invariant set of $C$ learned "core" embeddings, this yields linear complexity $O(N)$ for predetermined $C$, which bypasses quadratic scaling. Compared to prior cross-attention architectures, VECA maintains and iteratively updates the full set of $N$ input tokens, avoiding a small $C$-way bottleneck. Combined with nested training along the core axis, our model can elastically trade off compute and accuracy during inference. Across classification and dense tasks, VECA achieves performance competitive with the latest vision foundation models while reducing computational cost. Our results establish elastic core-periphery attention as a scalable alternative building block for Vision Transformers.
