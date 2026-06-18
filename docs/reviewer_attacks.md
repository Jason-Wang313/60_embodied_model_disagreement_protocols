# Reviewer Attacks

## Fatal if unaddressed

- "This is just active learning with robot-themed language."
- "Physical probes can be too expensive or disruptive."
- "The diagnostic is synthetic and may not transfer to hardware."
- "The safety gate may be harder than the original planning problem."
- "The probe library is hand-specified."

## V3 response

- The manuscript now frames the contribution as the embodied compilation step from disagreement to safe probe, with predicted signatures, safety gates, aborts, cost accounting, and stopping rules.
- Retained the v2 utility stress over physical probe cost as a negative control.
- Added a full-scale deterministic benchmark over 414,720 compact condition rows.
- Reported that safety-gated probing is the best non-oracle strategy on average, while abstention is the best deployable strategy at the highest physical-cost weight.
- Final decision is a full-scale deterministic submission candidate, not a hardware safety claim.
