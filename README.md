# Embodied Model Disagreement Protocols

Submission-hardening v3 full-scale artifact for paper 60 in the robotics 60-paper batch.

## Decision

Final full-scale submission candidate.

The paper is now a 30-page deterministic benchmark submission candidate, not the earlier short v2 protocol note. The claim remains bounded: cost-aware, safety-gated physical probes improve disagreement resolution and reduce unsafe false accepts when cheap safe observable signatures exist; latent disagreement or abstention can still be rational at higher physical cost or risk.

## Full-scale result

- Compact condition rows: 414,720
- Represented evaluations: 108,716,359,680
- Represented planning-tick decisions: 6,957,847,019,520
- Best non-oracle strategy: `safety_gated_probe_policy`, utility 0.373966
- Oracle selector utility: 0.846562
- Uncertainty-threshold unsafe false accept: 0.382443
- Safety-gated unsafe false accept: 0.103445
- Highest-cost best deployable strategy: `abstain`
- Final PDF: `C:/Users/wangz/Downloads/60.pdf`
- Final PDF SHA256: `15868C37F4A2E75FB067DAFC6A5404FAE1AD78E9D5956E1F9DA1A462353341B5`
- Visual hardening: VLA-v4-style boxed links, with green citation/URL borders and red internal-reference borders, verified on pages 2, 5, 8, 9, 10, 12, 13, 14, 15, and 26.

## Reproducible artifacts

- `run_full_scale_probe_disagreement_suite.py`: RAM-light full-scale benchmark generator.
- `results/full_scale/condition_metrics.csv`: compact streamed condition table.
- `results/full_scale/experiment_validation.json`: full-scale validation gate.
- `results/full_scale/*.tex`: generated manuscript tables.
- `figures/full_scale/*.pdf`: generated manuscript figures.
- `v2_probe_cost_sensitivity.py`: v2 utility stress retained as the negative control.
- `paper/main.tex`: final manuscript source.
- `build_pdf.ps1`: validates the full-scale run, enforces at least 25 pages, rebuilds `C:/Users/wangz/Downloads/60.pdf`, records SHA256, and removes `paper/main.pdf`.
