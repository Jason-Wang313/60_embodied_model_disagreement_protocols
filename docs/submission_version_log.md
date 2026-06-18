# Submission Version Log

## v1

Recovery build with deterministic protocol diagnostic, literature sweep, figure, and ICLR-style PDF.

## v2

- Added `v2_probe_cost_sensitivity.py`.
- Added `docs/v2_probe_cost_sensitivity.csv`.
- Added `docs/v2_probe_cost_sensitivity.json`.
- Added `paper/v2_probe_cost_table.tex`.
- Reframed physical probes as cost-sensitive.
- Added canonical build script and removed local generated PDF from version control.
- Final decision at v2: workshop-only.

## v3 full-scale

- Added `run_full_scale_probe_disagreement_suite.py`.
- Added RAM-light full-scale results under `results/full_scale/`.
- Added generated full-scale figures under `figures/full_scale/`.
- Expanded the manuscript to a 30-page final submission candidate.
- Added protocol design details, factor design, value-of-information metrics, strategy audit, probe recipes, safety-gate calibration notes, hardware logging schema, and reproducibility contract.
- Updated `build_pdf.ps1` to enforce full-scale validation, a 25-page minimum, canonical PDF export, SHA256 recording, and local PDF removal.
- Final v3 PDF: `C:/Users/wangz/Downloads/60.pdf`.
- Final v3 decision: full-scale deterministic submission candidate; not a hardware safety claim.
