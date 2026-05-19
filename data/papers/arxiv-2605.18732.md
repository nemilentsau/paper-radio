# Predictable Confabulations: Factual Recall by LLMs Scales with Model Size and Topic Frequency

## Metadata
- Paper ID: arxiv-2605.18732
- Source: arxiv
- Source ID: 2605.18732
- Authors: Matthew L. Smith, Jonathan P. Shock, Samuel T. Segun, Iyiola E. Olatunji, Tegawendé F. Bissyandé
- Published: 2026-05-18T17:53:44Z
- Updated: 2026-05-18T17:53:44Z
- Categories: cs.CL, cs.AI, cs.LG
- Source signals: arxiv_recent
- Triage decision: advance_to_review
- Triage rationale: The abstract proposes a concrete scaling relationship for factual recall and reports evaluation across many models and references, which makes it methodologically interesting and potentially useful for comparison. It is also likely to be a good episode topic because the claim is simple, testable, and directly relevant to LLM behavior, even though the evidence is only from the abstract at this stage.
- Research score estimate: 7.8
- Podcast score estimate: 8.2
- Local PDF path: data/papers/pdfs/arxiv-2605.18732.pdf
- Full text path: data/papers/fulltext/arxiv-2605.18732.txt
- Abstract URL: https://arxiv.org/abs/2605.18732
- PDF URL: https://arxiv.org/pdf/2605.18732

## Abstract
While scaling laws govern aggregate large language model performance, no scaling law has linked factual recall to both model size and training-data composition. We evaluated 38 models on over 8,900 scholarly references evaluated by an automated reference verification system. Recall quality follows a sigmoid in the log-linear combination of model parameter count and topic representation in training data. These two variables alone explain 60% of the variance across 16 dense models from four families, rising to 74-94% within individual families. The form matches a superposition-inspired account in which recall is gated by a signal-to-noise ratio: signal strength scales with concept frequency and the noise floor with model capacity.
