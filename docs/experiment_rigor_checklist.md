# Experiment Rigor Checklist

- [x] Original deterministic protocol diagnostic is present.
- [x] V2 cost-sensitivity utility stress is present.
- [x] Abstention baseline is included in v2 stress.
- [x] Claims are narrowed away from cost-insensitive probe dominance.
- [x] Full-scale deterministic benchmark is present.
- [x] Full-scale benchmark streams 414,720 compact rows without dense RAM allocation.
- [x] Summary tables and figures are generated from `results/full_scale/`.
- [x] Safety-gated probe policy is the best non-oracle strategy.
- [x] Highest-cost best deployable strategy is abstention.
- [x] Final build enforces full-scale validation and a 25-page minimum.
- [x] Canonical PDF has 30 pages and was visually inspected from rendered PNGs.
- [ ] Real robot validation.
- [ ] Learned probe library.
- [ ] Safety-gate validation.
- [ ] Hardware disruption/recovery analysis.

Decision impact: the paper is a full-scale deterministic submission candidate, but it remains a benchmark/reporting contribution rather than a hardware safety claim.
