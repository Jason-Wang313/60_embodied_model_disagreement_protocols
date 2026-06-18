# Plan

1. Preserve the v2 probe-cost sensitivity stress as a negative control: executable probes are useful only when physical cost and risk are justified by value of information.
2. Add a RAM-light deterministic full-scale benchmark over ambiguity class, world-model family, decision strategy, probe cost weight, safety risk weight, observation regime, perturbation severity, and probe-library quality.
3. Stream compact condition rows and online aggregates to `results/full_scale/` without loading the full condition CSV into memory.
4. Generate full-scale tables, figures, validation JSON, and strategy/cost/risk/ambiguity/model/observation/probe-library summaries.
5. Rewrite the manuscript around the final bounded claim: cost-aware, safety-gated physical probes improve disagreement resolution and reduce unsafe false accepts when cheap safe probes exist, while latent disagreement or abstention can be rational at higher cost or risk.
6. Expand to at least 25 pages before final export.
7. Update `build_pdf.ps1` to enforce the full-scale validation and page threshold, record size/hash/page count in ASCII JSON, copy only the final artifact to `C:/Users/wangz/Downloads/60.pdf`, and remove `paper/main.pdf`.
8. Render the Downloads PDF for visual QA, update all status docs, run stale scans and validation checks, then commit and push only after the repo is clean.
