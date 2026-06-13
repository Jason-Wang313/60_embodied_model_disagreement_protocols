# Final Audit

Paper: 60 embodied_model_disagreement_protocols

Status: terminal

Decision: workshop-only

## Main reason

The protocol is useful as a mechanism, but the evidence is deterministic and synthetic. V2 hardening shows that executable probes dominate only when physical probe cost is low enough. The paper cannot claim general superiority over latent disagreement or abstention.

## V2 evidence

- Original executable probe diagnostic: 0.795 resolved, 0.106 unsafe false accepts, 1.927 probe cost.
- Utility at cost weight 0.10: executable probes win, utility 0.497.
- Utility at cost weight 0.25: latent disagreement wins, utility 0.264 versus 0.207 for probes.
- Utility at cost weight 0.50: latent disagreement still wins, utility 0.180 versus -0.274 for probes.
- Utility at cost weight 1.25: abstention wins with utility 0.000.

## Boundary

The paper may claim that disagreement should be compiled into executable probes when cheap safe probes exist. It may not claim hardware validation, cost-insensitive dominance, or universal superiority over scalar or latent disagreement scores.
