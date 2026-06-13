from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
PAPER = ROOT / "paper"

SUMMARY = DOCS / "protocol_summary.json"
COST_WEIGHTS = [0.0, 0.10, 0.25, 0.50, 1.25]
RISK_WEIGHT = 1.0

DISPLAY = {
    "uncertainty_threshold": "uncertainty",
    "latent_disagreement_score": "latent",
    "executable_probe_protocol": "probe",
    "abstain": "abstain",
}


def load_stats() -> dict[str, dict[str, float]]:
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    stats = payload["strategy_stats"]
    stats["abstain"] = {
        "resolved_rate": 0.0,
        "unsafe_false_accept_rate": 0.0,
        "physical_probe_cost": 0.0,
    }
    return stats


def utility(stats: dict[str, float], cost_weight: float) -> float:
    return (
        stats["resolved_rate"]
        - RISK_WEIGHT * stats["unsafe_false_accept_rate"]
        - cost_weight * stats["physical_probe_cost"]
    )


def summarize(stats: dict[str, dict[str, float]]) -> list[dict[str, object]]:
    rows = []
    for cost_weight in COST_WEIGHTS:
        utilities = {name: utility(values, cost_weight) for name, values in stats.items()}
        best = max(utilities.items(), key=lambda item: item[1])[0]
        rows.append(
            {
                "risk_weight": RISK_WEIGHT,
                "cost_weight": cost_weight,
                "best_strategy": best,
                "uncertainty_utility": utilities["uncertainty_threshold"],
                "latent_utility": utilities["latent_disagreement_score"],
                "probe_utility": utilities["executable_probe_protocol"],
                "abstain_utility": utilities["abstain"],
            }
        )
    return rows


def write_outputs(rows: list[dict[str, object]]) -> None:
    csv_path = DOCS / "v2_probe_cost_sensitivity.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "risk_weight",
                "cost_weight",
                "best_strategy",
                "uncertainty_utility",
                "latent_utility",
                "probe_utility",
                "abstain_utility",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    payload = {
        "risk_weight": RISK_WEIGHT,
        "cost_weights": COST_WEIGHTS,
        "rows": rows,
        "interpretation": (
            "Executable probes win when physical probe cost is cheap. Once cost weight reaches 0.25, "
            "the latent disagreement score has higher utility; at very high probe cost, abstention wins."
        ),
    }
    (DOCS / "v2_probe_cost_sensitivity.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    table_lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Cost w. & Best & Probe U & Latent U & Abstain U \\",
        r"\midrule",
    ]
    for row in rows:
        table_lines.append(
            f"{row['cost_weight']:.2f} & {DISPLAY[row['best_strategy']]} & "
            f"{row['probe_utility']:.3f} & {row['latent_utility']:.3f} & "
            f"{row['abstain_utility']:.3f} \\\\"
        )
    table_lines.extend([r"\bottomrule", r"\end{tabular}"])
    (PAPER / "v2_probe_cost_table.tex").write_text("\n".join(table_lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = summarize(load_stats())
    write_outputs(rows)
    tipping = next(row for row in rows if row["cost_weight"] == 0.25)
    high = next(row for row in rows if row["cost_weight"] == 1.25)
    print(
        "cost_0.25_best="
        f"{tipping['best_strategy']} "
        "cost_1.25_best="
        f"{high['best_strategy']}"
    )


if __name__ == "__main__":
    main()
