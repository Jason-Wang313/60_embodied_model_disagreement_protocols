# Reproducibility Checklist

- Run `python run_full_scale_probe_disagreement_suite.py` to regenerate the full-scale CSV, summaries, TeX tables, figures, and validation JSON.
- Run `python v2_probe_cost_sensitivity.py` to regenerate the v2 CSV, JSON, and LaTeX table.
- Run `powershell -ExecutionPolicy Bypass -File build_pdf.ps1` to rebuild the canonical PDF.
- The canonical artifact is `C:/Users/wangz/Downloads/60.pdf`.
- The build script requires 414,720 condition rows, 108,716,359,680 represented evaluations, 6,957,847,019,520 represented planning-tick decisions, safety-gated probe as best non-oracle, and abstention as the highest-cost best deployable strategy.
- The build script requires at least 25 pages; the final artifact has 30 pages.
- `paper/main.pdf` is generated during compilation and removed after the canonical copy is made.
- `data/build_status.json` records pages, bytes, SHA256, validation counts, and local PDF removal.
- Render the canonical PDF to PNGs under `tmp/pdfs/` for visual QA, then remove the temp render directory after inspection.
