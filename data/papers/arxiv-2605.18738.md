# What Does the AI Doctor Value? Auditing Pluralism in the Clinical Ethics of Language Models

## Metadata
- Paper ID: arxiv-2605.18738
- Source: arxiv
- Source ID: 2605.18738
- Authors: Payal Chandak, Victoria Alkin, David Wu, Maya Dagan, Taposh Dutta Roy, Maria Clara Saad Menezes, Ayush Noori, Nirali Somia, John S. Brownstein, Ran Balicer, Rebecca W. Brendel, Noa Dagan, Isaac S. Kohane, Gabriel A. Brat
- Published: 2026-05-18T17:56:13Z
- Updated: 2026-05-18T17:56:13Z
- Categories: cs.AI
- Source signals: arxiv_recent
- Triage decision: advance_to_review
- Triage rationale: This is a timely cs.AI paper with a concrete benchmark and an auditable clinical-ethics framing, which makes it likely to yield a substantive review. The abstract suggests a real empirical finding rather than generic safety claims, and the topic has both research and discussion value.
- Research score estimate: 7.6
- Podcast score estimate: 8.3
- Local PDF path: data/papers/pdfs/arxiv-2605.18738.pdf
- Full text path: data/papers/fulltext/arxiv-2605.18738.txt
- Abstract URL: https://arxiv.org/abs/2605.18738
- PDF URL: https://arxiv.org/pdf/2605.18738

## Abstract
Medicine is inherently pluralistic. Principles such as autonomy, beneficence, nonmaleficence, and justice routinely conflict, and such ethical dilemmas often sharply divide reasonable physicians. Good clinical practice navigates these tensions in concert with each patient's values rather than imposing a single ethical stance. The ethical values that large language models bring to medical advice, however, have not been systematically examined. We present a framework for auditing value pluralism in medical AI, comprising a benchmark of clinician-verified dilemmas and an attribution method that recovers value priorities directly from decisions. The ecosystem of frontier models spans physician-level value heterogeneity, and models discuss competing values in their reasoning (Overton pluralism) before committing to a decision. However, individual model decisions are near-deterministic across repeated sampling and semantic variations, failing to reproduce the distributional pluralism of the physician panel. Across benchmark cases, these consistent decisions reflect committed, systematic value preferences. While most model priorities fall within the natural range of inter-physician variation, some significantly underweight patient autonomy. A single LLM deployed without regard for its value priorities could amplify those priorities at scale to every patient it serves. Without explicit efforts to balance ethical perspectives with one or multiple models, these tools risk replacing clinical pluralism with a deployment monoculture.
