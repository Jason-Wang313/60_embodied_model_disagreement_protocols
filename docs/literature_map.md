# Literature Map

The recovery sweep collected 1200 rows for embodied model disagreement, robot world models, uncertainty, active probing, contact-rich prediction, and planning.

Top categories: planning-control: 498, uncertainty: 376, embodied-manipulation: 299, active-probing: 271, model-disagreement: 167, general-robot-learning: 133.

Main clusters:

1. World-model and predictive-control papers treat disagreement as a rollout quality signal.
2. Ensemble and Bayesian uncertainty papers estimate epistemic uncertainty but often leave the physical disambiguating observation implicit.
3. Active learning and exploration papers select queries, but many queries are information-gathering actions detached from contact safety.
4. Contact-rich manipulation papers show why visual uncertainty scores fail when the missing variable is tactile, geometric, or support-graph structure.

Gap: the field has uncertainty scores and active learning, but it lacks a compact protocol that converts model disagreement into executable, safety-gated physical probes.
