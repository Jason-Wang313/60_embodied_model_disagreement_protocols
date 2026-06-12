# Embodied Model Disagreement Protocols

Paper 60 recovery artifact for the robotics 60-paper batch.

## Thesis

Robot world-model disagreement should be compiled into executable physical probes rather than treated only as a scalar uncertainty score.

## Artifacts

- `docs/related_work_matrix.csv`: 1200-row landscape matrix.
- `docs/serious_skim_300.csv`: serious skim subset.
- `docs/deep_read_225.csv`: deep-read subset.
- `docs/hostile_100.csv`: hostile prior subset.
- `docs/probe_protocol_trials.csv`: deterministic diagnostic trials.
- `paper/main.tex` and `paper/main.pdf`: ICLR-style paper.

## Key diagnostic

Executable probes resolve 0.795 of disagreements and reduce unsafe false accepts to 0.106, with mean physical probe cost 1.927.
