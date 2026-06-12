# Novelty Decision

Chosen thesis: model disagreement in robot world models should not be treated primarily as a scalar uncertainty score. It should be compiled into a small set of executable physical probes whose observations can distinguish the candidate embodied hypotheses.

Why this is strongest:

- It turns disagreement into an action protocol, not another calibration metric.
- It is embodied: the protocol must account for contact, occlusion, support, force, and safety cost.
- It is falsifiable: a probe either reduces the hypothesis set or it was the wrong probe.

Rejected alternatives:

- Bigger ensembles: too close to existing uncertainty work.
- Pure uncertainty calibration: useful but does not say which physical action to take.
- Passive disagreement heatmaps: descriptive rather than executable.
