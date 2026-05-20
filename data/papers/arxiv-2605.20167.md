# HaorFloodAlert: Deseasonalized ML Ensemble for 72-Hour Flood Prediction in Bangladesh Haor Wetlands

## Metadata
- Paper ID: arxiv-2605.20167
- Source: arxiv
- Source ID: 2605.20167
- Authors: Salma Hoque Talukdar Koli, Fahima Haque Talukder Jely, Md. Samiul Alim, Md. Zakir Hossen
- Published: 2026-05-19T17:51:46Z
- Updated: 2026-05-19T17:51:46Z
- Categories: cs.AI, cs.LG
- Source signals: arxiv_recent
- Triage decision: queue_for_review
- Triage rationale: This looks application-focused but potentially useful: it claims a concrete operational setting, a nontrivial lead time, and an attempt to address seasonal leakage rather than just optimize accuracy. The abstract is still dominated by single-dataset performance claims and implementation details, so it is better queued for review than advanced immediately.
- Research score estimate: 6.0
- Podcast score estimate: 7.0
- Local PDF path: data/papers/pdfs/arxiv-2605.20167.pdf
- Full text path: data/papers/fulltext/arxiv-2605.20167.txt
- Abstract URL: https://arxiv.org/abs/2605.20167
- PDF URL: https://arxiv.org/pdf/2605.20167

## Abstract
Flash floods in Bangladesh's haor wetlands show up with almost no warning. They wreck the annual boro rice harvest. Current setups, built for riverine floods, miss backwater dynamics entirely. These basins are flat. Water does not behave like it does on the Brahmaputra. We built HaorFloodAlert, a deseasonalized machine learning ensemble that forecasts 72-hour flood probability for the Sunamganj Haor (approximately 8,000 km2). Temperature was acting as a seasonal cheat code - it inflated accuracy by 6.9 pp just because floods happen in warm months. We caught that. We also built an upstream Barak River Sentinel-1 SAR proxy from Silchar, Assam, giving about 36 hours of lead time. Otsu-thresholded SAR change detection validates at 84-91 percent spatial match. The operational ensemble (RF 0.5625 + XGBoost 0.4375) hits 89.6 percent LOOCV accuracy, 87.5 percent recall, and 0.943 AUC-ROC on 77 real Sentinel-1 events. A three-tier alert pipeline and a BRRI-calibrated boro rice damage estimator are included.
