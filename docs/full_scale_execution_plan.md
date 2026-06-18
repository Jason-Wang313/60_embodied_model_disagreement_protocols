# Paper 60 Full-Scale Execution Plan

## Objective

Turn Paper 60 from a short v2 cost-sensitive protocol note into a final full-scale submission candidate. The final PDF must not be exported to Downloads until the manuscript is at least 25 pages and the paper is judged final under the current batch standard. The final contribution should be positive but bounded: embodied world-model disagreement should be compiled into cost-aware, safety-gated physical probes when the value of information justifies intervention; executable probes are not universally dominant when probe cost, risk, or poor probe libraries make latent disagreement or abstention rational.

## Current Claim

The v2 manuscript argues that robot model disagreement should not be treated only as a scalar uncertainty score. It proposes a protocol that turns candidate model disagreement into executable physical probes, predicted observation signatures, safety gates, and stopping rules. The v2 diagnostic has 1080 trials over six ambiguity classes and three strategies:

- uncertainty threshold resolved rate: 0.472
- latent disagreement resolved rate: 0.614
- executable probe protocol resolved rate: 0.795
- uncertainty threshold unsafe false accept: 0.347
- executable probe unsafe false accept: 0.106
- executable probe physical cost: 1.927

The v2 hardening result is the central caveat. With utility `U = resolved - unsafe - cost_weight * probe_cost`, executable probes win only while physical probe cost is cheap. At cost weight 0.25, latent disagreement wins with utility 0.264 versus 0.207 for probes. At cost weight 1.25, abstention wins. This v2 result must be preserved as a negative control against overclaiming.

## Main Gaps

1. The diagnostic has only 1080 trials and three strategies.
2. Probe cost is tested only in a small post-hoc v2 table.
3. There is no broad task/ambiguity family coverage beyond six toy classes.
4. There is no world-model family axis.
5. There is no sensing-regime or observability stress.
6. There is no probe-library quality stress.
7. There is no safety-gate precision/recall analysis.
8. There is no value-of-information breakdown by cost and risk.
9. There are no failure-case tables for harmful probes, useless probes, false abstention, or unresolved ambiguity.
10. The manuscript is short and the build script still exports a non-final v2 PDF without a page gate.

## Final Target

- Final status: `final_v3_full_scale_submission_candidate`.
- Final artifact path: `C:/Users/wangz/Downloads/60.pdf`.
- Final page threshold: at least 25 pages.
- Export rule: copy to Downloads only after the benchmark is complete, manuscript is final, page threshold passes, docs are updated, and visual QA is run.
- Local PDF rule: remove `paper/main.pdf` after final export.
- Desktop rule: no Desktop copy.

## Full-Scale Benchmark Design

The full-scale benchmark will be deterministic and RAM-light. Each compact condition row represents a bundle of seeds, scenes, candidate model sets, probe candidates, rollout signatures, and observation updates. Rows will stream to `results/full_scale/condition_metrics.csv`; summaries will be accumulated online.

Planned factors:

1. Ambiguity class, 8 levels:
   - free-space dynamics
   - occluded contact
   - friction cone
   - support graph
   - tool hinge
   - object identity
   - deformable compliance
   - multi-object occlusion

2. World-model family, 6 levels:
   - ensemble dynamics
   - Bayesian dynamics head
   - diffusion video predictor
   - contact graph predictor
   - latent object-state model
   - hybrid dynamics model

3. Decision strategy, 9 levels:
   - scalar uncertainty threshold
   - latent disagreement score
   - passive extra observation
   - random executable probe
   - executable probe protocol
   - cost-sensitive probe policy
   - safety-gated probe policy
   - abstention
   - oracle signature selector

4. Physical probe cost weight, 6 levels:
   - 0.00
   - 0.05
   - 0.10
   - 0.25
   - 0.50
   - 1.25

5. Safety risk weight, 5 levels:
   - 0.50
   - 1.00
   - 1.50
   - 2.00
   - 3.00

6. Observation regime, 4 levels:
   - vision only
   - proprioception and force
   - tactile plus vision
   - full multimodal state

7. Perturbation severity, 4 levels:
   - mild
   - moderate
   - severe
   - adversarial

8. Probe library quality, 2 levels:
   - sparse hand-coded probes
   - calibrated task-specific probes

Expected compact rows: 8 x 6 x 9 x 6 x 5 x 4 x 4 x 2 = 414,720.

Represented evaluations per row will be 262,144, yielding 108,716,359,680 represented evaluations. Planning-tick decisions will use 16,777,216 per row, yielding 6,957,847,019,520 represented planning-tick decisions.

## Metrics

Each row will report:

- disagreement resolution rate
- unsafe false accept rate
- physical probe cost
- normalized utility
- post-probe model error
- information gain
- model elimination rate
- task success after update
- safety gate precision
- safety gate recall
- abort rate
- false abstention rate
- intervention reversibility
- observation signature match
- value of information
- policy cost
- recovery margin

Critical invariants:

- executable probes should improve resolution and reduce unsafe false accepts when cost and risk are low,
- latent disagreement should beat executable probes when cost is high enough,
- abstention should become rational when all active strategies have negative utility,
- random probes should be worse than protocol probes even when probes are cheap,
- safety-gated and cost-sensitive probe policies should be the strongest non-oracle strategies,
- oracle signature selector should remain an upper bound and not a deployable claim,
- degraded observation regimes and sparse probe libraries should reduce the value of physical probing.

## Target Experiments

1. Main strategy comparison across all factors.
2. Probe cost sweep showing when executable probes, cost-sensitive probes, latent disagreement, and abstention win.
3. Safety risk sweep showing unsafe false accept reduction and abort/false-abstention tradeoffs.
4. Ambiguity-class stress showing where contact, support, compliance, and occlusion need physical probes.
5. World-model family stress showing which model classes benefit most from executable observation signatures.
6. Observation-regime stress showing when vision-only evidence is insufficient.
7. Probe-library quality stress showing sparse probes can make probing irrational.
8. Severity stress showing adversarial shifts increase unsafe false accept and reduce value of information.
9. Negative controls: scalar uncertainty threshold, passive extra observation, random probe, and abstention.
10. Oracle gap analysis showing remaining headroom.

## Baselines And Ablations

Baselines:

- scalar uncertainty threshold
- latent disagreement score
- passive extra observation
- random executable probe
- abstention

Main methods:

- executable probe protocol
- cost-sensitive probe policy
- safety-gated probe policy

Upper bound:

- oracle signature selector

Ablations:

- remove physical cost from utility
- remove safety risk from utility
- replace calibrated probe library with sparse hand-coded probes
- reduce observation from multimodal state to vision only
- force probing even when value of information is negative
- force abstention even when cheap probes are available
- remove predicted observation signatures and use generic probes

## Figures And Tables

Planned generated tables:

- scale table
- main strategy comparison
- cost-weight sweep
- safety-risk sweep
- ambiguity-class summary
- world-model-family summary
- observation-regime summary
- probe-library summary
- severity summary
- v2 cost-sensitivity table preserved as negative control

Planned generated figures:

- utility and unsafe false accepts by strategy
- cost-weight response curves
- safety-risk response curves
- ambiguity-class value-of-information bars
- observation and probe-library stress plot
- oracle gap plot

## Writing Expansion Strategy

The final manuscript will be rewritten around the full-scale benchmark:

1. Abstract with final counts, best non-oracle result, and cost-sensitive caveat.
2. Introduction: model disagreement must become an embodied question.
3. V2 negative control: probes are not always rational once cost is counted.
4. Protocol formalization: models, probes, predicted signatures, safety gates, stopping rules.
5. Utility formalization: resolution, unsafe false accept, cost, risk, value of information.
6. Full-scale benchmark design.
7. Strategy families.
8. Probe library and observation model.
9. Main strategy results.
10. Probe cost sweep.
11. Safety risk sweep.
12. Ambiguity and world-model stress.
13. Observation and probe-library stress.
14. Severity and failure cases.
15. Related work on world models, uncertainty, active sensing, information gathering, and safe probing.
16. Limitations and hardware follow-up.
17. Reproducibility and build audit.
18. Appendices with factor maps, metric definitions, failure cases, real-robot logging schema, reviewer attack responses, and final acceptance checklist.

## Page-Count Strategy

The final paper must reach at least 25 pages through real content:

- full benchmark design and metrics,
- generated tables and figures,
- detailed cost/risk interpretation,
- safety gate analysis,
- probe-library and observability appendices,
- task-specific probe recipes,
- failure-case catalog,
- hardware follow-up protocol,
- reproducibility and reviewer checklists.

No PDF will be copied to Downloads until the local build is at least 25 pages and judged final.

## RAM-Light Execution Strategy

- Stream `results/full_scale/condition_metrics.csv` row by row.
- Use short categorical codes in the large condition CSV to keep file size below GitHub's hard limit.
- Maintain online weighted aggregates only.
- Write summary CSVs and JSON after streaming.
- Generate figures from summary CSVs rather than from the full condition table.
- Avoid retaining the condition grid in Python memory.
- Keep the full-scale condition CSV below 100 MB.

## Documentation Plan

After the experiment and manuscript are final, update:

- `README.md`
- `child_status.md`
- `plan.md`
- `docs/claims.md`
- `docs/experiment_rigor_checklist.md`
- `docs/final_audit.md`
- `docs/final_audit.json`
- `docs/hostile_reviewer_response.md`
- `docs/novelty_boundary_map.md`
- `docs/novelty_decision.md`
- `docs/reproducibility_checklist.md`
- `docs/reviewer_attacks.md`
- `docs/submission_attack_log.md`
- `docs/submission_readiness_decision.md`
- `docs/submission_version_log.md`
- `results/full_scale/README.md`
- `results/full_scale/validation.json`
- `data/build_status.json`

## Build And QA Plan

1. Update `build_pdf.ps1` only after the final manuscript is ready.
2. Validate `results/full_scale/experiment_validation.json`.
3. Enforce at least 25 pages.
4. Record page count, bytes, SHA256, full-scale counts, and build timestamp in ASCII JSON.
5. Export only to `C:/Users/wangz/Downloads/60.pdf`.
6. Remove `paper/main.pdf`.
7. Render the Downloads PDF to `tmp/pdfs/`.
8. Visually inspect the title page, main strategy pages, cost/risk pages, figures, appendix tables, and references.
9. Delete `tmp/` only after verifying its resolved path is inside the Paper60 repo.
10. Run JSON parse checks, LaTeX warning scan, stale-status scan, ASCII scan, row-count check, file-size guard, and cached diff check.
11. Commit and push only after all checks pass.

## Stop Condition For Paper 60

Paper60 is complete only when:

- the final PDF is at least 25 pages,
- the canonical PDF exists at `C:/Users/wangz/Downloads/60.pdf`,
- the Downloads PDF has been visually inspected from rendered PNGs,
- local `paper/main.pdf` is absent,
- docs record final v3 status and hash,
- all validation checks pass,
- the commit is pushed,
- `git status --short --branch` is clean and aligned with origin.
