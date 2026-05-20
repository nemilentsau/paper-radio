# Atoms of Thought: Universal EEG Representation Learning with Microstates

## Metadata
- Paper ID: arxiv-2605.20182
- Source: arxiv
- Source ID: 2605.20182
- Authors: Xinyang Tian, Ruitao Liu, Ziyi Ye, Siyang Xue, Xin Wang, Xuesong Chen
- Published: 2026-05-19T17:59:31Z
- Updated: 2026-05-19T17:59:31Z
- Categories: cs.LG, cs.AI
- Source signals: arxiv_recent
- Triage decision: queue_for_review
- Triage rationale: The paper has a concrete methodological idea with cross-task evaluation and a plausible interpretability angle, so it is worth a closer look. It is still a relatively specialized EEG representation paper with claims that need full-review scrutiny for dataset breadth, baseline strength, and generalization.
- Research score estimate: 6.4
- Podcast score estimate: 5.8
- Local PDF path: data/papers/pdfs/arxiv-2605.20182.pdf
- Full text path: data/papers/fulltext/arxiv-2605.20182.txt
- Abstract URL: https://arxiv.org/abs/2605.20182
- PDF URL: https://arxiv.org/pdf/2605.20182

## Abstract
Learning universal representations from electroencephalogram (EEG) signals is a cutting-edge approach in the field of neuroinformatics and brain-computer interfaces (BCIs). Conventionally, EEG is treated as a multivariate temporal signal, where time- or frequency-domain features are extracted for representation learning. This paper investigates a simple yet effective EEG representation, i.e., microstates. Microstates represent the building blocks of brain activity patterns at a microscopic time scale. We build a universal microstate tokenizer from a large medical EEG dataset by clustering continuous EEG signals into sequences of discrete microstates. The microstate tokenizer is then adopted universally across a series of downstream tasks, including sleep staging, emotion recognition, and motor imagery classification. Experimental results show that EEG representation learning with microstates outperforms traditional time-domain and frequency-domain features under different models and across different tasks. Further analysis shows that microstates offer greater interpretability and scalability, thereby opening up applications in both cognitive neuroscience and clinical research.
