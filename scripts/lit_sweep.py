import csv
import json
import re
import sys
from collections import OrderedDict, defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen, Request

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

QUERIES = [
    "robot world model ensemble disagreement",
    "embodied uncertainty planning robot model disagreement",
    "robotic active probing model disagreement",
    "visual tactile world model ensemble robotics",
    "sim-to-real world model ensemble robot",
    "model predictive control ensemble disagreement robot",
    "contact-rich manipulation world model uncertainty",
    "robot foundation model uncertainty action planning",
    "active learning robotics uncertainty ensemble",
    "physics reasoning robot world models",
]

STOP = {"the", "and", "for", "with", "from", "into", "via", "using", "based", "robot", "robots", "robotic", "model", "models"}

def fetch_json(url: str):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

def norm_text(s):
    return re.sub(r"\s+", " ", (s or "")).strip()

def year_of(item):
    for key in ("published-print", "published-online", "created", "issued"):
        parts = item.get(key, {}).get("date-parts", [[]])
        if parts and parts[0]:
            return int(parts[0][0])
    return ""

def score(title, abstract):
    text = f"{title} {abstract}".lower()
    keys = ["world model", "uncertainty", "ensemble", "disagreement", "planning", "contact", "tactile", "sim-to-real", "active", "physics", "embodied", "manipulation", "control"]
    return sum(1 for k in keys if k in text)

def label(item, title, abstract):
    text = f"{title} {abstract}".lower()
    tags = []
    if "world model" in text or "predictive model" in text:
        tags.append("world-model")
    if "ensemble" in text or "disagreement" in text:
        tags.append("ensemble-disagreement")
    if "uncertainty" in text or "bayesian" in text:
        tags.append("uncertainty")
    if "planning" in text or "control" in text or "policy" in text:
        tags.append("planning-control")
    if "contact" in text or "tactile" in text or "grasp" in text or "manipulation" in text:
        tags.append("embodied-manipulation")
    if "sim-to-real" in text or "sim2real" in text or "transfer" in text:
        tags.append("sim2real")
    if "active" in text or "probe" in text or "query" in text or "exploration" in text:
        tags.append("active-probing")
    return "|".join(tags[:4])

def heuristic_fields(title, abstract):
    text = f"{title} {abstract}".lower()
    problem = "robot decision-making under uncertain dynamics"
    if "contact" in text:
        problem = "contact-rich embodied prediction"
    elif "planning" in text:
        problem = "planning with learned dynamics"
    elif "tactile" in text:
        problem = "multimodal tactile-visual inference"
    elif "sim-to-real" in text or "transfer" in text:
        problem = "sim-to-real transfer"
    mechanism = "learned predictive representation"
    if "ensemble" in text:
        mechanism = "ensemble prediction"
    elif "bayesian" in text:
        mechanism = "Bayesian inference"
    elif "active" in text:
        mechanism = "active data acquisition"
    assumptions = "stationary data and well-calibrated observations"
    if "contact" in text:
        assumptions = "smooth contact proxies and stable sensing"
    if "world model" in text:
        assumptions = "rollout error is manageable"
    fail = "distribution shift, compounding error, or sparse supervision"
    if "uncertainty" in text:
        fail = "miscalibrated uncertainty and epistemic leakage"
    if "active" in text:
        fail = "query cost and exploration bias"
    less_novel = "overlaps with standard learned-model pipelines"
    openq = "when does the method fail under embodied shift?"
    return problem, mechanism, assumptions, fail, less_novel, openq

def main():
    rows = OrderedDict()
    for q in QUERIES:
        cursor = "*"
        fetched = 0
        while fetched < 400 and len(rows) < 1400:
            url = f"https://api.crossref.org/works?query={quote(q)}&rows=100&cursor={quote(cursor)}&cursor-max=1000"
            data = fetch_json(url)
            msg = data.get("message", {})
            items = msg.get("items", [])
            cursor = msg.get("next-cursor", "")
            if not items:
                break
            for it in items:
                title = norm_text((it.get("title") or [""])[0])
                if not title:
                    continue
                doi = (it.get("DOI") or "").lower()
                key = doi or title.lower()
                if key in rows:
                    continue
                abstract = norm_text(it.get("abstract", ""))
                y = year_of(it)
                url = it.get("URL", "")
                sc = score(title, abstract)
                prob, mech, assump, fail, less, openq = heuristic_fields(title, abstract)
                rows[key] = {
                    "title": title,
                    "year": y,
                    "doi": doi,
                    "url": url,
                    "source_query": q,
                    "abstract": abstract,
                    "category": label(it, title, abstract),
                    "relevance_score": sc,
                    "problem_claimed": prob,
                    "mechanism_introduced": mech,
                    "hidden_assumptions": assump,
                    "failure_modes_ignored": fail,
                    "what_makes_less_novel": less,
                    "what_it_leaves_open": openq,
                }
            fetched += len(items)
            if not cursor:
                break
    sorted_rows = sorted(rows.values(), key=lambda r: (r["relevance_score"], r["year"]), reverse=True)
    out = DOCS / "related_work_matrix.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sorted_rows[0].keys()))
        w.writeheader()
        w.writerows(sorted_rows[:1200])
    meta = {
        "generated_at": datetime.now().isoformat(),
        "count": len(sorted_rows[:1200]),
        "queries": QUERIES,
    }
    (DOCS / "lit_sweep_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {out} with {len(sorted_rows[:1200])} rows")

if __name__ == "__main__":
    sys.exit(main())
