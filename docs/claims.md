# Claims

## Supported

1. Scalar uncertainty scores do not specify the physical observation that would disambiguate embodied models.
2. A useful protocol should emit a probe action, predicted observation signatures, a safety gate, and a stopping rule.
3. The full-scale benchmark contains 414,720 compact condition rows representing 108,716,359,680 evaluations.
4. The safety-gated probe policy is the best non-oracle strategy, with utility 0.373966 and unsafe false accept 0.103445.
5. The oracle selector reaches utility 0.846562, leaving substantial headroom for better signature prediction and safety-aware probe selection.
6. The v2 utility stress and full-scale cost sweep show that physical probes are rational only when their cost and risk are justified.
7. At the highest physical-cost weight, abstention is the best deployable strategy.

## Removed or narrowed

1. No claim of hardware validation.
2. No claim that physical probing is always worth its cost.
3. No claim that the safety gate is solved.
4. No claim of universal superiority over latent disagreement or abstention.
