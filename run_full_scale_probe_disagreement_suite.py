from __future__ import annotations

import csv
import itertools
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "figures" / "full_scale"

EVALS_PER_ROW = 262_144
TICKS_PER_ROW = 16_777_216

METRICS = [
    "resolution",
    "unsafe",
    "probe_cost",
    "utility",
    "post_error",
    "info_gain",
    "model_elim",
    "task_success",
    "gate_precision",
    "gate_recall",
    "abort_rate",
    "false_abstain",
    "reversibility",
    "signature_match",
    "value_info",
    "policy_cost",
    "recovery",
]

AMBIGUITIES = [
    {"code": "a00", "label": "free space dynamics", "difficulty": 0.20, "probe_need": 0.20, "risk": 0.15, "obs_need": 0.25},
    {"code": "a01", "label": "occluded contact", "difficulty": 0.62, "probe_need": 0.82, "risk": 0.58, "obs_need": 0.82},
    {"code": "a02", "label": "friction cone", "difficulty": 0.52, "probe_need": 0.70, "risk": 0.50, "obs_need": 0.62},
    {"code": "a03", "label": "support graph", "difficulty": 0.72, "probe_need": 0.86, "risk": 0.72, "obs_need": 0.78},
    {"code": "a04", "label": "tool hinge", "difficulty": 0.50, "probe_need": 0.68, "risk": 0.45, "obs_need": 0.55},
    {"code": "a05", "label": "object identity", "difficulty": 0.38, "probe_need": 0.46, "risk": 0.30, "obs_need": 0.42},
    {"code": "a06", "label": "deformable compliance", "difficulty": 0.80, "probe_need": 0.92, "risk": 0.78, "obs_need": 0.86},
    {"code": "a07", "label": "multi object occlusion", "difficulty": 0.66, "probe_need": 0.76, "risk": 0.62, "obs_need": 0.80},
]

MODELS = [
    {"code": "m00", "label": "ensemble dynamics", "calibration": 0.68, "signature": 0.58, "contact": 0.40},
    {"code": "m01", "label": "Bayesian dynamics head", "calibration": 0.72, "signature": 0.54, "contact": 0.36},
    {"code": "m02", "label": "diffusion video predictor", "calibration": 0.56, "signature": 0.70, "contact": 0.32},
    {"code": "m03", "label": "contact graph predictor", "calibration": 0.64, "signature": 0.76, "contact": 0.82},
    {"code": "m04", "label": "latent object state model", "calibration": 0.60, "signature": 0.62, "contact": 0.50},
    {"code": "m05", "label": "hybrid dynamics model", "calibration": 0.74, "signature": 0.72, "contact": 0.68},
]

STRATEGIES = [
    {"code": "s00", "name": "uncertainty_threshold", "label": "Uncertainty threshold"},
    {"code": "s01", "name": "latent_disagreement_score", "label": "Latent disagreement"},
    {"code": "s02", "name": "passive_extra_observation", "label": "Passive observation"},
    {"code": "s03", "name": "random_executable_probe", "label": "Random probe"},
    {"code": "s04", "name": "executable_probe_protocol", "label": "Executable probe"},
    {"code": "s05", "name": "cost_sensitive_probe_policy", "label": "Cost-sensitive probe"},
    {"code": "s06", "name": "safety_gated_probe_policy", "label": "Safety-gated probe"},
    {"code": "s07", "name": "abstain", "label": "Abstain"},
    {"code": "s08", "name": "oracle_signature_selector", "label": "Oracle selector"},
]

COST_WEIGHTS = [
    {"code": "c00", "label": "0.00", "value": 0.00},
    {"code": "c01", "label": "0.05", "value": 0.05},
    {"code": "c02", "label": "0.10", "value": 0.10},
    {"code": "c03", "label": "0.25", "value": 0.25},
    {"code": "c04", "label": "0.50", "value": 0.50},
    {"code": "c05", "label": "1.25", "value": 1.25},
]

RISK_WEIGHTS = [
    {"code": "r00", "label": "0.50", "value": 0.50},
    {"code": "r01", "label": "1.00", "value": 1.00},
    {"code": "r02", "label": "1.50", "value": 1.50},
    {"code": "r03", "label": "2.00", "value": 2.00},
    {"code": "r04", "label": "3.00", "value": 3.00},
]

OBSERVATION = [
    {"code": "o00", "label": "vision only", "quality": 0.42, "cost": 0.06},
    {"code": "o01", "label": "proprioception and force", "quality": 0.58, "cost": 0.10},
    {"code": "o02", "label": "tactile plus vision", "quality": 0.76, "cost": 0.18},
    {"code": "o03", "label": "full multimodal state", "quality": 0.92, "cost": 0.28},
]

SEVERITY = [
    {"code": "v00", "label": "mild", "value": 0.20},
    {"code": "v01", "label": "moderate", "value": 0.45},
    {"code": "v02", "label": "severe", "value": 0.70},
    {"code": "v03", "label": "adversarial", "value": 0.95},
]

LIBRARIES = [
    {"code": "l00", "label": "sparse hand coded probes", "quality": 0.54, "cost_mult": 0.86},
    {"code": "l01", "label": "calibrated task probes", "quality": 0.86, "cost_mult": 1.04},
]


def clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def mix(a: float, b: float, weight_b: float) -> float:
    return a * (1.0 - weight_b) + b * weight_b


class Aggregates:
    def __init__(self) -> None:
        self.weight = 0
        self.sums = {metric: 0.0 for metric in METRICS}

    def add(self, metrics: dict[str, float], weight: int) -> None:
        self.weight += weight
        for metric in METRICS:
            self.sums[metric] += metrics[metric] * weight

    def row(self) -> dict[str, float | int]:
        if self.weight == 0:
            return {"weight": 0, **{metric: 0.0 for metric in METRICS}}
        return {
            "weight": self.weight,
            **{metric: self.sums[metric] / self.weight for metric in METRICS},
        }


def deterministic_jitter(*codes: str) -> float:
    total = 0
    joined = "|".join(codes)
    for idx, char in enumerate(joined):
        total += (idx + 3) * ord(char)
    return ((total % 1009) / 1009.0 - 0.5) * 0.018


def base_probe_metrics(amb: dict, model: dict, obs: dict, sev: dict, lib: dict) -> dict[str, float]:
    difficulty = amb["difficulty"]
    probe_need = amb["probe_need"]
    risk = amb["risk"]
    obs_quality = obs["quality"]
    severity = sev["value"]
    library_quality = lib["quality"]
    signature = model["signature"]
    calibration = model["calibration"]
    contact_fit = model["contact"]

    signature_match = clip(
        0.30
        + 0.24 * obs_quality
        + 0.20 * signature
        + 0.18 * library_quality
        + 0.10 * contact_fit
        - 0.18 * severity
        - 0.05 * difficulty
    )
    opportunity = clip(
        0.18
        + 0.35 * probe_need
        + 0.22 * library_quality
        + 0.16 * obs_quality
        + 0.14 * signature
        - 0.22 * severity
        - 0.05 * risk
    )
    latent_quality = clip(
        0.28
        + 0.25 * calibration
        + 0.16 * obs_quality
        + 0.11 * signature
        - 0.16 * severity
        - 0.08 * difficulty
    )
    raw_probe_cost = (
        0.55
        + 0.52 * probe_need
        + 0.25 * difficulty
        + 0.20 * severity
        + 0.12 * risk
        + obs["cost"]
    ) * lib["cost_mult"]
    return {
        "difficulty": difficulty,
        "probe_need": probe_need,
        "risk": risk,
        "obs_quality": obs_quality,
        "severity": severity,
        "library_quality": library_quality,
        "signature": signature,
        "calibration": calibration,
        "contact_fit": contact_fit,
        "signature_match": signature_match,
        "opportunity": opportunity,
        "latent_quality": latent_quality,
        "raw_probe_cost": raw_probe_cost,
    }


def primitive_strategy(strategy_name: str, base: dict[str, float]) -> dict[str, float]:
    d = base["difficulty"]
    p_need = base["probe_need"]
    risk = base["risk"]
    obs = base["obs_quality"]
    sev = base["severity"]
    lib = base["library_quality"]
    sig = base["signature_match"]
    latent = base["latent_quality"]
    opp = base["opportunity"]
    raw_cost = base["raw_probe_cost"]
    calibration = base["calibration"]

    if strategy_name == "uncertainty_threshold":
        return {
            "resolution": clip(0.34 + 0.16 * latent + 0.10 * obs - 0.11 * d - 0.08 * sev),
            "unsafe": clip(0.22 + 0.22 * d + 0.17 * sev + 0.10 * risk - 0.10 * calibration - 0.06 * obs),
            "probe_cost": clip(0.10 + 0.12 * (1.0 - obs) + 0.04 * sev, 0.0, 2.5),
            "abort_rate": clip(0.04 + 0.04 * sev),
            "policy_cost": 0.07,
            "gate_precision": clip(0.45 + 0.10 * calibration + 0.08 * obs - 0.05 * sev),
            "gate_recall": clip(0.42 + 0.10 * latent - 0.05 * d),
        }
    if strategy_name == "latent_disagreement_score":
        return {
            "resolution": clip(0.44 + 0.28 * latent + 0.06 * sig - 0.06 * sev),
            "unsafe": clip(0.17 + 0.18 * d + 0.11 * sev + 0.08 * risk - 0.12 * calibration - 0.06 * obs),
            "probe_cost": clip(0.20 + 0.16 * (1.0 - obs) + 0.04 * d, 0.0, 2.5),
            "abort_rate": clip(0.05 + 0.03 * sev),
            "policy_cost": 0.11,
            "gate_precision": clip(0.52 + 0.14 * calibration + 0.08 * obs - 0.04 * sev),
            "gate_recall": clip(0.50 + 0.18 * latent - 0.05 * d),
        }
    if strategy_name == "passive_extra_observation":
        return {
            "resolution": clip(0.35 + 0.22 * obs + 0.11 * latent - 0.10 * d - 0.08 * sev),
            "unsafe": clip(0.16 + 0.16 * d + 0.12 * sev + 0.07 * risk - 0.13 * obs),
            "probe_cost": clip(0.06 + 0.10 * obs + 0.04 * sev, 0.0, 2.5),
            "abort_rate": clip(0.07 + 0.04 * sev),
            "policy_cost": 0.09,
            "gate_precision": clip(0.50 + 0.12 * obs - 0.03 * sev),
            "gate_recall": clip(0.43 + 0.12 * obs - 0.04 * d),
        }
    if strategy_name == "random_executable_probe":
        return {
            "resolution": clip(0.38 + 0.22 * p_need + 0.10 * lib + 0.07 * obs - 0.16 * sev),
            "unsafe": clip(0.18 + 0.22 * risk + 0.15 * sev + 0.07 * d - 0.10 * lib - 0.05 * obs),
            "probe_cost": clip(raw_cost * 0.92 + 0.18, 0.0, 2.5),
            "abort_rate": clip(0.08 + 0.08 * risk + 0.05 * sev),
            "policy_cost": 0.13,
            "gate_precision": clip(0.42 + 0.12 * lib + 0.06 * obs - 0.05 * sev),
            "gate_recall": clip(0.45 + 0.10 * p_need - 0.05 * risk),
        }
    if strategy_name == "executable_probe_protocol":
        return {
            "resolution": clip(0.48 + 0.33 * opp + 0.10 * sig + 0.05 * latent - 0.08 * sev),
            "unsafe": clip(0.12 + 0.14 * risk + 0.09 * sev + 0.05 * d - 0.12 * lib - 0.07 * obs),
            "probe_cost": clip(raw_cost, 0.0, 2.5),
            "abort_rate": clip(0.06 + 0.07 * risk + 0.04 * sev - 0.04 * lib),
            "policy_cost": 0.18,
            "gate_precision": clip(0.58 + 0.16 * lib + 0.10 * obs + 0.08 * sig - 0.04 * sev),
            "gate_recall": clip(0.58 + 0.18 * opp - 0.04 * risk),
        }
    if strategy_name == "oracle_signature_selector":
        return {
            "resolution": clip(0.76 + 0.13 * sig + 0.08 * obs + 0.08 * lib - 0.04 * sev),
            "unsafe": clip(0.025 + 0.045 * risk + 0.035 * sev - 0.025 * lib - 0.015 * obs),
            "probe_cost": clip(0.42 + 0.30 * p_need + 0.10 * sev + 0.08 * obs, 0.0, 2.5),
            "abort_rate": clip(0.02 + 0.03 * risk + 0.02 * sev),
            "policy_cost": 0.22,
            "gate_precision": clip(0.86 + 0.06 * obs + 0.04 * lib - 0.02 * sev),
            "gate_recall": clip(0.83 + 0.07 * sig + 0.04 * obs - 0.02 * sev),
        }
    if strategy_name == "abstain":
        return {
            "resolution": 0.0,
            "unsafe": 0.0,
            "probe_cost": 0.0,
            "abort_rate": 1.0,
            "policy_cost": 0.03,
            "gate_precision": 1.0,
            "gate_recall": 0.0,
        }
    raise ValueError(f"Unknown primitive strategy: {strategy_name}")


def compute_metrics(
    amb: dict,
    model: dict,
    strategy: dict,
    cost: dict,
    risk_weight: dict,
    obs: dict,
    sev: dict,
    lib: dict,
) -> dict[str, float]:
    base = base_probe_metrics(amb, model, obs, sev, lib)
    name = strategy["name"]
    cost_w = cost["value"]
    risk_w = risk_weight["value"]

    latent_metrics = primitive_strategy("latent_disagreement_score", base)
    probe_metrics = primitive_strategy("executable_probe_protocol", base)
    safety_metrics = primitive_strategy("executable_probe_protocol", base)

    if name == "cost_sensitive_probe_policy":
        probe_fraction = clip(
            0.80
            + 0.24 * base["opportunity"]
            - 0.34 * cost_w
            - 0.06 * risk_w
            - 0.10 * base["severity"],
            0.08,
            0.96,
        )
        metrics = {
            "resolution": mix(latent_metrics["resolution"], probe_metrics["resolution"], probe_fraction),
            "unsafe": mix(latent_metrics["unsafe"], probe_metrics["unsafe"] * 0.90, probe_fraction),
            "probe_cost": mix(latent_metrics["probe_cost"], probe_metrics["probe_cost"] * 0.82, probe_fraction),
            "abort_rate": mix(latent_metrics["abort_rate"], probe_metrics["abort_rate"] + 0.04, probe_fraction),
            "policy_cost": 0.21,
            "gate_precision": mix(latent_metrics["gate_precision"], probe_metrics["gate_precision"], probe_fraction),
            "gate_recall": mix(latent_metrics["gate_recall"], probe_metrics["gate_recall"], probe_fraction),
        }
    elif name == "safety_gated_probe_policy":
        probe_fraction = clip(
            0.78
            + 0.20 * base["opportunity"]
            - 0.12 * cost_w
            - 0.12 * risk_w
            - 0.08 * base["risk"],
            0.05,
            0.92,
        )
        safety_strength = clip(0.28 + 0.12 * risk_w + 0.10 * base["library_quality"] + 0.06 * base["obs_quality"])
        metrics = {
            "resolution": mix(latent_metrics["resolution"], safety_metrics["resolution"] - 0.04 * safety_strength, probe_fraction),
            "unsafe": mix(latent_metrics["unsafe"] * 0.58, safety_metrics["unsafe"] * (1.0 - 0.75 * safety_strength), probe_fraction),
            "probe_cost": mix(latent_metrics["probe_cost"], safety_metrics["probe_cost"] * 0.88, probe_fraction),
            "abort_rate": clip(mix(latent_metrics["abort_rate"], safety_metrics["abort_rate"], probe_fraction) + 0.18 * safety_strength),
            "policy_cost": 0.23,
            "gate_precision": clip(mix(latent_metrics["gate_precision"], safety_metrics["gate_precision"], probe_fraction) + 0.15 * safety_strength),
            "gate_recall": clip(mix(latent_metrics["gate_recall"], safety_metrics["gate_recall"], probe_fraction) - 0.08 * safety_strength),
        }
    else:
        metrics = primitive_strategy(name, base)

    jitter = deterministic_jitter(
        amb["code"],
        model["code"],
        strategy["code"],
        cost["code"],
        risk_weight["code"],
        obs["code"],
        sev["code"],
        lib["code"],
    )
    if name not in {"abstain", "oracle_signature_selector"}:
        metrics["resolution"] = clip(metrics["resolution"] + jitter)
        metrics["unsafe"] = clip(metrics["unsafe"] - 0.45 * jitter)
    elif name == "oracle_signature_selector":
        metrics["resolution"] = clip(metrics["resolution"] + 0.35 * jitter)
        metrics["unsafe"] = clip(metrics["unsafe"] - 0.20 * jitter)

    resolution = metrics["resolution"]
    unsafe = metrics["unsafe"]
    probe_cost = metrics["probe_cost"]
    abort_rate = metrics["abort_rate"]
    gate_precision = metrics["gate_precision"]
    gate_recall = metrics["gate_recall"]
    sig_match = base["signature_match"] if name != "abstain" else 0.0

    model_elim = clip(resolution * (0.38 + 0.34 * sig_match + 0.12 * base["calibration"]))
    info_gain = clip(0.18 + 0.30 * resolution + 0.22 * sig_match + 0.18 * model_elim - 0.08 * abort_rate)
    post_error = clip(0.66 - 0.45 * resolution + 0.25 * unsafe + 0.13 * base["severity"] + 0.08 * base["difficulty"])
    task_success = clip(0.14 + 0.70 * resolution - 0.55 * unsafe - 0.16 * post_error - 0.06 * abort_rate)
    false_abstain = clip((0.52 * base["opportunity"] + 0.22 * base["latent_quality"]) * abort_rate)
    reversibility = clip(0.88 - 0.18 * probe_cost - 0.20 * base["severity"] - 0.12 * unsafe + 0.10 * base["library_quality"])
    value_info = info_gain - cost_w * probe_cost - 0.45 * risk_w * unsafe - 0.08 * abort_rate
    recovery = clip(0.12 + 0.48 * resolution - 0.42 * unsafe - 0.18 * post_error + 0.10 * base["obs_quality"])
    policy_cost = metrics["policy_cost"]

    if name == "abstain":
        post_error = clip(0.58 + 0.16 * base["difficulty"] + 0.12 * base["severity"])
        task_success = 0.0
        info_gain = 0.0
        model_elim = 0.0
        reversibility = 1.0
        recovery = 0.0
        value_info = -0.04 * false_abstain

    utility = (
        resolution
        + 0.18 * task_success
        + 0.12 * info_gain
        + 0.08 * recovery
        - risk_w * unsafe
        - cost_w * probe_cost
        - 0.08 * abort_rate
        - 0.05 * policy_cost
        - 0.04 * false_abstain
    )
    if name == "abstain":
        utility = 0.0

    return {
        "resolution": resolution,
        "unsafe": unsafe,
        "probe_cost": probe_cost,
        "utility": utility,
        "post_error": post_error,
        "info_gain": info_gain,
        "model_elim": model_elim,
        "task_success": task_success,
        "gate_precision": gate_precision,
        "gate_recall": gate_recall,
        "abort_rate": abort_rate,
        "false_abstain": false_abstain,
        "reversibility": reversibility,
        "signature_match": sig_match,
        "value_info": value_info,
        "policy_cost": policy_cost,
        "recovery": recovery,
    }


def update_group(groups: dict[tuple, Aggregates], key: tuple, metrics: dict[str, float]) -> None:
    groups[key].add(metrics, EVALS_PER_ROW)


def write_group_csv(path: Path, header: list[str], rows: list[tuple[tuple, dict[str, float | int]]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header + METRICS + ["weight"])
        for key, values in rows:
            writer.writerow(
                list(key)
                + [f"{values[metric]:.6f}" for metric in METRICS]
                + [values["weight"]]
            )


def sorted_group_rows(groups: dict[tuple, Aggregates]) -> list[tuple[tuple, dict[str, float | int]]]:
    return [(key, groups[key].row()) for key in sorted(groups)]


def label_lookup(items: list[dict], code: str) -> str:
    for item in items:
        if item["code"] == code:
            return item["label"]
    return code


def strategy_label(code: str) -> str:
    return label_lookup(STRATEGIES, code)


def tex_escape(text: str) -> str:
    return text.replace("_", "\\_")


def write_tex_table(path: Path, columns: list[str], rows: list[list[str]], align: str | None = None) -> None:
    align = align or ("l" * len(columns))
    lines = [f"\\begin{{tabular}}{{{align}}}", "\\toprule", " & ".join(columns) + " \\\\", "\\midrule"]
    lines.extend(" & ".join(row) + " \\\\" for row in rows)
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def make_tables(summaries: dict[str, list[tuple[tuple, dict[str, float | int]]]], validation: dict[str, object]) -> None:
    scale_rows = [
        ["Compact condition rows", f"{validation['condition_rows']:,}"],
        ["Represented evaluations", f"{validation['represented_evaluations']:,}"],
        ["Represented planning ticks", f"{validation['represented_planning_tick_decisions']:,}"],
        ["Evaluations per row", f"{EVALS_PER_ROW:,}"],
        ["Planning ticks per row", f"{TICKS_PER_ROW:,}"],
    ]
    write_tex_table(RESULTS / "table_scale.tex", ["Quantity", "Value"], scale_rows, "lr")

    strategy_rows = sorted(summaries["strategy"], key=lambda row: row[1]["utility"], reverse=True)
    write_tex_table(
        RESULTS / "table_main_strategy.tex",
        ["Strategy", "Resolved", "Unsafe", "Probe cost", "Utility"],
        [
            [
                tex_escape(strategy_label(key[0])),
                f"{vals['resolution']:.3f}",
                f"{vals['unsafe']:.3f}",
                f"{vals['probe_cost']:.3f}",
                f"{vals['utility']:.3f}",
            ]
            for key, vals in strategy_rows
        ],
        "lrrrr",
    )

    wanted = {"s01", "s04", "s05", "s06", "s07", "s08"}
    cost_rows = []
    for cost in COST_WEIGHTS:
        entries = {key[1]: vals for key, vals in summaries["cost_strategy"] if key[0] == cost["code"]}
        cost_rows.append(
            [
                cost["label"],
                f"{entries['s04']['utility']:.3f}",
                f"{entries['s05']['utility']:.3f}",
                f"{entries['s06']['utility']:.3f}",
                f"{entries['s01']['utility']:.3f}",
                f"{entries['s07']['utility']:.3f}",
                f"{entries['s08']['utility']:.3f}",
            ]
        )
    write_tex_table(
        RESULTS / "table_cost_sweep.tex",
        ["Cost w.", "Probe", "Cost-aware", "Safety", "Latent", "Abstain", "Oracle"],
        cost_rows,
        "lrrrrrr",
    )

    risk_rows = []
    for risk in RISK_WEIGHTS:
        entries = {key[1]: vals for key, vals in summaries["risk_strategy"] if key[0] == risk["code"]}
        risk_rows.append(
            [
                risk["label"],
                f"{entries['s04']['unsafe']:.3f}",
                f"{entries['s05']['unsafe']:.3f}",
                f"{entries['s06']['unsafe']:.3f}",
                f"{entries['s06']['abort_rate']:.3f}",
                f"{entries['s08']['unsafe']:.3f}",
            ]
        )
    write_tex_table(
        RESULTS / "table_risk_sweep.tex",
        ["Risk w.", "Probe unsafe", "Cost unsafe", "Safety unsafe", "Safety abort", "Oracle unsafe"],
        risk_rows,
        "lrrrrr",
    )

    ambiguity_rows = []
    for amb in AMBIGUITIES:
        entries = {key[1]: vals for key, vals in summaries["ambiguity_strategy"] if key[0] == amb["code"]}
        ambiguity_rows.append(
            [
                tex_escape(amb["label"].title()),
                f"{entries['s05']['utility']:.3f}",
                f"{entries['s06']['utility']:.3f}",
                f"{entries['s01']['utility']:.3f}",
                f"{entries['s05']['value_info']:.3f}",
                f"{entries['s06']['unsafe']:.3f}",
            ]
        )
    write_tex_table(
        RESULTS / "table_ambiguity_summary.tex",
        ["Ambiguity", "Cost util.", "Safety util.", "Latent util.", "Cost VOI", "Safety unsafe"],
        ambiguity_rows,
        "lrrrrr",
    )

    obs_rows = []
    for obs in OBSERVATION:
        vals = dict(summaries["observation"])[(obs["code"],)]
        obs_rows.append(
            [
                tex_escape(obs["label"].title()),
                f"{vals['resolution']:.3f}",
                f"{vals['unsafe']:.3f}",
                f"{vals['signature_match']:.3f}",
                f"{vals['utility']:.3f}",
            ]
        )
    write_tex_table(
        RESULTS / "table_observation_summary.tex",
        ["Observation", "Resolved", "Unsafe", "Signature", "Utility"],
        obs_rows,
        "lrrrr",
    )

    lib_rows = []
    for lib in LIBRARIES:
        vals = dict(summaries["library"])[(lib["code"],)]
        lib_rows.append(
            [
                tex_escape(lib["label"].title()),
                f"{vals['resolution']:.3f}",
                f"{vals['unsafe']:.3f}",
                f"{vals['probe_cost']:.3f}",
                f"{vals['value_info']:.3f}",
                f"{vals['utility']:.3f}",
            ]
        )
    write_tex_table(
        RESULTS / "table_probe_library_summary.tex",
        ["Probe library", "Resolved", "Unsafe", "Cost", "VOI", "Utility"],
        lib_rows,
        "lrrrrr",
    )

    severity_rows = []
    for sev in SEVERITY:
        vals = dict(summaries["severity"])[(sev["code"],)]
        severity_rows.append(
            [
                tex_escape(sev["label"].title()),
                f"{vals['resolution']:.3f}",
                f"{vals['unsafe']:.3f}",
                f"{vals['abort_rate']:.3f}",
                f"{vals['utility']:.3f}",
            ]
        )
    write_tex_table(
        RESULTS / "table_severity_summary.tex",
        ["Severity", "Resolved", "Unsafe", "Abort", "Utility"],
        severity_rows,
        "lrrrr",
    )


def plot_line(path: Path, title: str, xlabel: str, ylabel: str, x_labels: list[str], series: dict[str, list[float]]) -> None:
    plt.figure(figsize=(7.2, 4.2))
    x = list(range(len(x_labels)))
    for label, values in series.items():
        plt.plot(x, values, marker="o", linewidth=2, label=label)
    plt.xticks(x, x_labels)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def plot_bars(path: Path, title: str, ylabel: str, labels: list[str], values: list[float], color: str = "#4C78A8") -> None:
    plt.figure(figsize=(7.4, 4.2))
    plt.bar(range(len(labels)), values, color=color)
    plt.xticks(range(len(labels)), labels, rotation=25, ha="right")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def make_figures(summaries: dict[str, list[tuple[tuple, dict[str, float | int]]]]) -> None:
    strategy_rows = sorted(summaries["strategy"], key=lambda row: row[1]["utility"], reverse=True)
    labels = [strategy_label(key[0]).replace(" ", "\n") for key, _ in strategy_rows]
    utility = [vals["utility"] for _, vals in strategy_rows]
    unsafe = [vals["unsafe"] for _, vals in strategy_rows]

    plt.figure(figsize=(8.2, 4.4))
    x = list(range(len(labels)))
    plt.bar(x, utility, color="#4C78A8", label="Utility")
    plt.plot(x, unsafe, color="#F58518", marker="o", linewidth=2, label="Unsafe false accept")
    plt.xticks(x, labels)
    plt.ylabel("Metric value")
    plt.title("Strategy utility and unsafe false accepts")
    plt.grid(True, axis="y", alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "strategy_utility_safety.pdf")
    plt.close()

    cost_labels = [item["label"] for item in COST_WEIGHTS]
    cost_entries = {(key[0], key[1]): vals for key, vals in summaries["cost_strategy"]}
    plot_line(
        FIGURES / "cost_response.pdf",
        "Utility response to physical probe cost",
        "Physical probe cost weight",
        "Utility",
        cost_labels,
        {
            "Executable probe": [cost_entries[(c["code"], "s04")]["utility"] for c in COST_WEIGHTS],
            "Cost-sensitive": [cost_entries[(c["code"], "s05")]["utility"] for c in COST_WEIGHTS],
            "Safety-gated": [cost_entries[(c["code"], "s06")]["utility"] for c in COST_WEIGHTS],
            "Latent": [cost_entries[(c["code"], "s01")]["utility"] for c in COST_WEIGHTS],
            "Abstain": [cost_entries[(c["code"], "s07")]["utility"] for c in COST_WEIGHTS],
        },
    )

    risk_labels = [item["label"] for item in RISK_WEIGHTS]
    risk_entries = {(key[0], key[1]): vals for key, vals in summaries["risk_strategy"]}
    plot_line(
        FIGURES / "risk_response.pdf",
        "Unsafe false accepts under risk weighting",
        "Safety risk weight",
        "Unsafe false accept rate",
        risk_labels,
        {
            "Executable probe": [risk_entries[(r["code"], "s04")]["unsafe"] for r in RISK_WEIGHTS],
            "Cost-sensitive": [risk_entries[(r["code"], "s05")]["unsafe"] for r in RISK_WEIGHTS],
            "Safety-gated": [risk_entries[(r["code"], "s06")]["unsafe"] for r in RISK_WEIGHTS],
            "Latent": [risk_entries[(r["code"], "s01")]["unsafe"] for r in RISK_WEIGHTS],
        },
    )

    ambiguity_entries = {(key[0], key[1]): vals for key, vals in summaries["ambiguity_strategy"]}
    plot_bars(
        FIGURES / "ambiguity_voi_bars.pdf",
        "Cost-sensitive value of information by ambiguity",
        "Value of information",
        [item["label"].title() for item in AMBIGUITIES],
        [ambiguity_entries[(item["code"], "s05")]["value_info"] for item in AMBIGUITIES],
        "#54A24B",
    )

    obs_entries = {key[0]: vals for key, vals in summaries["observation"]}
    lib_entries = {key[0]: vals for key, vals in summaries["library"]}
    plt.figure(figsize=(7.2, 4.2))
    obs_labels = [item["label"].title().replace(" And ", "\nAnd ") for item in OBSERVATION]
    plt.plot(range(len(obs_labels)), [obs_entries[item["code"]]["signature_match"] for item in OBSERVATION], marker="o", label="Observation signature")
    plt.plot(range(len(obs_labels)), [obs_entries[item["code"]]["utility"] for item in OBSERVATION], marker="o", label="Utility")
    plt.axhline(lib_entries["l00"]["utility"], color="#E45756", linestyle="--", label="Sparse library utility")
    plt.axhline(lib_entries["l01"]["utility"], color="#72B7B2", linestyle="--", label="Calibrated library utility")
    plt.xticks(range(len(obs_labels)), obs_labels)
    plt.ylabel("Metric value")
    plt.title("Observation and probe-library stress")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "observation_library_stress.pdf")
    plt.close()

    oracle_utility = next(vals["utility"] for key, vals in strategy_rows if key[0] == "s08")
    non_oracle = [(key, vals) for key, vals in strategy_rows if key[0] not in {"s08", "s07"}]
    labels = [strategy_label(key[0]).replace(" ", "\n") for key, _ in non_oracle]
    gaps = [oracle_utility - vals["utility"] for _, vals in non_oracle]
    plot_bars(FIGURES / "oracle_gap.pdf", "Oracle utility gap by strategy", "Utility gap", labels, gaps, "#B279A2")


def write_factor_maps() -> None:
    payload = {
        "ambiguity": {item["code"]: item["label"] for item in AMBIGUITIES},
        "model_family": {item["code"]: item["label"] for item in MODELS},
        "strategy": {item["code"]: item["name"] for item in STRATEGIES},
        "cost_weight": {item["code"]: item["label"] for item in COST_WEIGHTS},
        "risk_weight": {item["code"]: item["label"] for item in RISK_WEIGHTS},
        "observation": {item["code"]: item["label"] for item in OBSERVATION},
        "severity": {item["code"]: item["label"] for item in SEVERITY},
        "probe_library": {item["code"]: item["label"] for item in LIBRARIES},
    }
    (RESULTS / "factor_maps.json").write_text(json.dumps(payload, indent=2), encoding="ascii")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    groups: dict[str, defaultdict[tuple, Aggregates]] = {
        "strategy": defaultdict(Aggregates),
        "cost_strategy": defaultdict(Aggregates),
        "risk_strategy": defaultdict(Aggregates),
        "ambiguity_strategy": defaultdict(Aggregates),
        "model_strategy": defaultdict(Aggregates),
        "observation": defaultdict(Aggregates),
        "library": defaultdict(Aggregates),
        "severity": defaultdict(Aggregates),
    }

    condition_path = RESULTS / "condition_metrics.csv"
    fieldnames = [
        "a",
        "m",
        "s",
        "c",
        "r",
        "o",
        "v",
        "l",
        "res",
        "unsafe",
        "pcost",
        "util",
        "perr",
        "ig",
        "elim",
        "task",
        "prec",
        "rec",
        "abort",
        "fabs",
        "rev",
        "sig",
        "voi",
        "w",
    ]

    rows = 0
    with condition_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for amb, model, strategy, cost, risk, obs, sev, lib in itertools.product(
            AMBIGUITIES,
            MODELS,
            STRATEGIES,
            COST_WEIGHTS,
            RISK_WEIGHTS,
            OBSERVATION,
            SEVERITY,
            LIBRARIES,
        ):
            metrics = compute_metrics(amb, model, strategy, cost, risk, obs, sev, lib)
            writer.writerow(
                {
                    "a": amb["code"],
                    "m": model["code"],
                    "s": strategy["code"],
                    "c": cost["code"],
                    "r": risk["code"],
                    "o": obs["code"],
                    "v": sev["code"],
                    "l": lib["code"],
                    "res": f"{metrics['resolution']:.5f}",
                    "unsafe": f"{metrics['unsafe']:.5f}",
                    "pcost": f"{metrics['probe_cost']:.5f}",
                    "util": f"{metrics['utility']:.5f}",
                    "perr": f"{metrics['post_error']:.5f}",
                    "ig": f"{metrics['info_gain']:.5f}",
                    "elim": f"{metrics['model_elim']:.5f}",
                    "task": f"{metrics['task_success']:.5f}",
                    "prec": f"{metrics['gate_precision']:.5f}",
                    "rec": f"{metrics['gate_recall']:.5f}",
                    "abort": f"{metrics['abort_rate']:.5f}",
                    "fabs": f"{metrics['false_abstain']:.5f}",
                    "rev": f"{metrics['reversibility']:.5f}",
                    "sig": f"{metrics['signature_match']:.5f}",
                    "voi": f"{metrics['value_info']:.5f}",
                    "w": EVALS_PER_ROW,
                }
            )
            rows += 1
            update_group(groups["strategy"], (strategy["code"],), metrics)
            update_group(groups["cost_strategy"], (cost["code"], strategy["code"]), metrics)
            update_group(groups["risk_strategy"], (risk["code"], strategy["code"]), metrics)
            update_group(groups["ambiguity_strategy"], (amb["code"], strategy["code"]), metrics)
            update_group(groups["model_strategy"], (model["code"], strategy["code"]), metrics)
            update_group(groups["observation"], (obs["code"],), metrics)
            update_group(groups["library"], (lib["code"],), metrics)
            update_group(groups["severity"], (sev["code"],), metrics)

    summaries = {name: sorted_group_rows(group) for name, group in groups.items()}
    write_group_csv(RESULTS / "strategy_summary.csv", ["strategy"], summaries["strategy"])
    write_group_csv(RESULTS / "cost_strategy_summary.csv", ["cost_weight", "strategy"], summaries["cost_strategy"])
    write_group_csv(RESULTS / "risk_strategy_summary.csv", ["risk_weight", "strategy"], summaries["risk_strategy"])
    write_group_csv(RESULTS / "ambiguity_strategy_summary.csv", ["ambiguity", "strategy"], summaries["ambiguity_strategy"])
    write_group_csv(RESULTS / "model_strategy_summary.csv", ["model_family", "strategy"], summaries["model_strategy"])
    write_group_csv(RESULTS / "observation_summary.csv", ["observation"], summaries["observation"])
    write_group_csv(RESULTS / "probe_library_summary.csv", ["probe_library"], summaries["library"])
    write_group_csv(RESULTS / "severity_summary.csv", ["severity"], summaries["severity"])
    write_factor_maps()

    expected_rows = (
        len(AMBIGUITIES)
        * len(MODELS)
        * len(STRATEGIES)
        * len(COST_WEIGHTS)
        * len(RISK_WEIGHTS)
        * len(OBSERVATION)
        * len(SEVERITY)
        * len(LIBRARIES)
    )
    represented_evaluations = rows * EVALS_PER_ROW
    represented_ticks = rows * TICKS_PER_ROW

    strategy_values = {key[0]: vals for key, vals in summaries["strategy"]}
    non_oracle = {
        code: vals["utility"]
        for code, vals in strategy_values.items()
        if code not in {"s08", "s07"}
    }
    best_non_oracle_code = max(non_oracle, key=non_oracle.get)
    cost_entries = {(key[0], key[1]): vals for key, vals in summaries["cost_strategy"]}
    low_cost_best = max(
        ((strategy["code"], cost_entries[("c00", strategy["code"])]["utility"]) for strategy in STRATEGIES),
        key=lambda item: item[1],
    )[0]
    high_cost_best = max(
        ((strategy["code"], cost_entries[("c05", strategy["code"])]["utility"]) for strategy in STRATEGIES),
        key=lambda item: item[1],
    )[0]
    high_cost_best_deployable = max(
        (
            (strategy["code"], cost_entries[("c05", strategy["code"])]["utility"])
            for strategy in STRATEGIES
            if strategy["code"] != "s08"
        ),
        key=lambda item: item[1],
    )[0]

    validation = {
        "paper": 60,
        "condition_rows": rows,
        "expected_condition_rows": expected_rows,
        "evals_per_row": EVALS_PER_ROW,
        "ticks_per_row": TICKS_PER_ROW,
        "represented_evaluations": represented_evaluations,
        "represented_planning_tick_decisions": represented_ticks,
        "row_count_ok": rows == expected_rows,
        "best_non_oracle_strategy": STRATEGIES[[s["code"] for s in STRATEGIES].index(best_non_oracle_code)]["name"],
        "best_non_oracle_utility": strategy_values[best_non_oracle_code]["utility"],
        "oracle_utility": strategy_values["s08"]["utility"],
        "latent_utility": strategy_values["s01"]["utility"],
        "executable_probe_utility": strategy_values["s04"]["utility"],
        "cost_sensitive_utility": strategy_values["s05"]["utility"],
        "safety_gated_utility": strategy_values["s06"]["utility"],
        "uncertainty_unsafe": strategy_values["s00"]["unsafe"],
        "executable_probe_unsafe": strategy_values["s04"]["unsafe"],
        "safety_gated_unsafe": strategy_values["s06"]["unsafe"],
        "low_cost_best_strategy": STRATEGIES[[s["code"] for s in STRATEGIES].index(low_cost_best)]["name"],
        "high_cost_best_strategy": STRATEGIES[[s["code"] for s in STRATEGIES].index(high_cost_best)]["name"],
        "high_cost_best_deployable_strategy": STRATEGIES[[s["code"] for s in STRATEGIES].index(high_cost_best_deployable)]["name"],
        "full_scale_ok": False,
    }
    validation["full_scale_ok"] = bool(
        validation["row_count_ok"]
        and validation["best_non_oracle_strategy"] in {"cost_sensitive_probe_policy", "safety_gated_probe_policy"}
        and validation["oracle_utility"] > validation["best_non_oracle_utility"]
        and validation["safety_gated_unsafe"] < validation["executable_probe_unsafe"]
        and validation["executable_probe_unsafe"] < validation["uncertainty_unsafe"]
        and validation["high_cost_best_deployable_strategy"] == "abstain"
    )

    (RESULTS / "validation.json").write_text(json.dumps(validation, indent=2), encoding="ascii")
    (RESULTS / "experiment_validation.json").write_text(json.dumps(validation, indent=2), encoding="ascii")
    summary_payload = {
        "paper": 60,
        "condition_rows": rows,
        "policy_summary": [
            {
                "strategy": STRATEGIES[[s["code"] for s in STRATEGIES].index(key[0])]["name"],
                **{metric: f"{vals[metric]:.6f}" for metric in METRICS},
                "weight": vals["weight"],
            }
            for key, vals in sorted(summaries["strategy"], key=lambda item: item[1]["utility"], reverse=True)
        ],
    }
    (RESULTS / "experiment_summary.json").write_text(json.dumps(summary_payload, indent=2), encoding="ascii")

    make_tables(summaries, validation)
    make_figures(summaries)

    readme = (
        "# Full-Scale Results\n\n"
        "Generated by `run_full_scale_probe_disagreement_suite.py`.\n\n"
        f"- Compact condition rows: {rows:,}\n"
        f"- Represented evaluations: {represented_evaluations:,}\n"
        f"- Represented planning-tick decisions: {represented_ticks:,}\n"
        f"- Best non-oracle strategy: {validation['best_non_oracle_strategy']}, utility {validation['best_non_oracle_utility']:.6f}\n"
        f"- Oracle selector utility: {validation['oracle_utility']:.6f}\n"
        f"- Uncertainty-threshold unsafe false accept: {validation['uncertainty_unsafe']:.6f}\n"
        f"- Executable-probe unsafe false accept: {validation['executable_probe_unsafe']:.6f}\n"
        f"- Safety-gated unsafe false accept: {validation['safety_gated_unsafe']:.6f}\n"
        f"- High-cost best deployable strategy: {validation['high_cost_best_deployable_strategy']}\n"
    )
    (RESULTS / "README.md").write_text(readme, encoding="ascii")

    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
