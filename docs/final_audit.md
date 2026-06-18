# Final Audit

Paper: 60 embodied_model_disagreement_protocols

Status: terminal

Decision: final full-scale deterministic submission candidate

## Main reason

The final paper is a 30-page full-scale deterministic benchmark. It expands the v2 protocol note into a RAM-light suite over 414,720 compact condition rows, representing 108,716,359,680 evaluations and 6,957,847,019,520 planning-tick decisions. The strongest deployable result is the safety-gated probe policy, while abstention remains the best deployable strategy at the highest physical cost weight.

## V3 evidence

- Best non-oracle strategy: safety_gated_probe_policy, utility 0.373966.
- Oracle selector utility: 0.846562.
- Uncertainty-threshold unsafe false accept: 0.382443.
- Executable-probe unsafe false accept: 0.137995.
- Safety-gated unsafe false accept: 0.103445.
- Highest-cost best deployable strategy: abstain.
- Canonical PDF: `C:/Users/wangz/Downloads/60.pdf`.
- Canonical PDF pages: 30.
- Canonical PDF SHA256: 407C2F0EC72FCFFDB6EF81F509B85D7E6014F0D0082314613AA0CB4D657AC552.

## Boundary

The paper may claim that cost-aware, safety-gated physical probes improve the safety-resolution tradeoff when cheap safe observable signatures exist. It may not claim hardware validation, cost-insensitive dominance, safety certification, or universal superiority over latent disagreement and abstention.
