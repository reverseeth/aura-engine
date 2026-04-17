"""
Creative DNA Registry — CRUD + análise + DNA extraction.

Uso:
    python registry.py init /workspace/<product-slug>
    python registry.py add /workspace/<product-slug> <creative-id> <features.json> --product <slug>
    python registry.py update /workspace/<product-slug> <creative-id> <performance.json>
    python registry.py stats /workspace/<product-slug> --product <slug>
    python registry.py dna /workspace/<product-slug> --product <slug>
    python registry.py show /workspace/<product-slug>
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import datetime
from pathlib import Path
from statistics import mean


SCHEMA_PATH = Path(__file__).parent / "schema.sql"
MIN_CREATIVES_FOR_DNA = 10


def connect(db_path: Path) -> sqlite3.Connection:
    """Open SQLite connection with WAL mode + timeout for concurrent writes."""
    conn = sqlite3.connect(db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init(workspace_product: Path):
    if not SCHEMA_PATH.exists():
        sys.stderr.write(
            f"ERROR: schema.sql not found at {SCHEMA_PATH}. "
            "Reinstall creative-dna lib from Aura repo.\n"
        )
        sys.exit(1)
    dna_dir = workspace_product / "creative-dna"
    dna_dir.mkdir(parents=True, exist_ok=True)
    db_path = dna_dir / "registry.db"
    conn = connect(db_path)
    conn.executescript(SCHEMA_PATH.read_text())
    conn.commit()
    print(f"Initialized: {db_path}")


def add_creative(db_path: Path, creative_id: str, features_file: Path, product_slug: str):
    features = json.loads(features_file.read_text())
    conn = connect(db_path)
    conn.execute("""
        INSERT OR REPLACE INTO creatives
        (id, product_slug, concept_id, source_file, features_json, produced_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        creative_id,
        product_slug,
        features.get("concept_id"),
        features.get("source_file", str(features_file)),
        json.dumps(features),
        features.get("produced_at", datetime.datetime.utcnow().isoformat()),
    ))
    conn.execute("""
        INSERT OR IGNORE INTO performance (creative_id, outcome, measured_at)
        VALUES (?, 'pending', ?)
    """, (creative_id, datetime.datetime.utcnow().isoformat()))
    conn.commit()
    print(f"Added creative: {creative_id}")


def update_performance(db_path: Path, creative_id: str, perf_file: Path):
    perf = json.loads(perf_file.read_text())
    conn = connect(db_path)
    conn.execute("""
        UPDATE performance SET
          cpa = ?, ctr = ?, thumbstop_3s = ?, hold_15s = ?, roas = ?,
          spend = ?, impressions = ?, clicks = ?, purchases = ?,
          days_active = ?, decile_rank = ?, outcome = ?, measured_at = ?
        WHERE creative_id = ?
    """, (
        perf.get("cpa"), perf.get("ctr"), perf.get("thumbstop_3s"),
        perf.get("hold_15s"), perf.get("roas"), perf.get("spend"),
        perf.get("impressions"), perf.get("clicks"), perf.get("purchases"),
        perf.get("days_active"), perf.get("decile_rank"),
        perf.get("outcome", "neutral"),
        datetime.datetime.utcnow().isoformat(),
        creative_id,
    ))
    conn.commit()
    print(f"Updated performance: {creative_id} → {perf.get('outcome')}")


def stats(db_path: Path, product_slug: str):
    conn = connect(db_path)
    total = conn.execute(
        "SELECT COUNT(*) FROM creatives WHERE product_slug = ?", (product_slug,)
    ).fetchone()[0]
    by_outcome = conn.execute("""
        SELECT p.outcome, COUNT(*) as n
        FROM creatives c JOIN performance p ON c.id = p.creative_id
        WHERE c.product_slug = ?
        GROUP BY p.outcome
    """, (product_slug,)).fetchall()

    print(f"\n=== DNA Registry Stats — {product_slug} ===")
    print(f"Total creatives: {total}")
    for row in by_outcome:
        print(f"  {row['outcome']}: {row['n']}")


def compute_dna(db_path: Path, product_slug: str) -> dict:
    """Calcula correlação simples entre features e outcome == winner."""
    conn = connect(db_path)
    rows = conn.execute("""
        SELECT c.features_json, p.outcome, p.cpa, p.decile_rank
        FROM creatives c JOIN performance p ON c.id = p.creative_id
        WHERE c.product_slug = ? AND p.outcome != 'pending'
    """, (product_slug,)).fetchall()

    if len(rows) < MIN_CREATIVES_FOR_DNA:
        return {
            "error": "insufficient_data",
            "creatives_with_performance": len(rows),
            "minimum_required": MIN_CREATIVES_FOR_DNA,
            "message": f"Need at least {MIN_CREATIVES_FOR_DNA} creatives with measured performance to extract DNA. Keep running Skill 09 to accumulate data.",
        }

    winners = [r for r in rows if r["outcome"] == "winner"]
    losers = [r for r in rows if r["outcome"] == "loser"]

    feature_stats: dict = {}
    for r in rows:
        features = json.loads(r["features_json"])
        for feat, val in features.items():
            if feat not in feature_stats:
                feature_stats[feat] = {"values": [], "winners": [], "losers": []}
            feature_stats[feat]["values"].append(val)
            if r["outcome"] == "winner":
                feature_stats[feat]["winners"].append(val)
            elif r["outcome"] == "loser":
                feature_stats[feat]["losers"].append(val)

    dna: dict = {}
    for feat, data in feature_stats.items():
        w_vals = data["winners"]
        l_vals = data["losers"]
        if len(w_vals) == 0:
            continue
        sample_val = w_vals[0]
        if isinstance(sample_val, (int, float)) and not isinstance(sample_val, bool):
            try:
                winners_mean = round(mean(w_vals), 3)
                losers_mean = round(mean(l_vals), 3) if len(l_vals) > 0 else None
                delta = None
                if losers_mean is not None:
                    delta = round(winners_mean - losers_mean, 3)
                dna[feat] = {
                    "type": "numeric",
                    "winners_mean": winners_mean,
                    "losers_mean": losers_mean,
                    "winners_count": len(w_vals),
                    "delta_winners_vs_losers": delta,
                }
            except (TypeError, ValueError, ZeroDivisionError):
                continue
        else:
            from collections import Counter
            w_counter = Counter(w_vals)
            l_counter = Counter(l_vals) if len(l_vals) > 0 else None
            top_winner_val = w_counter.most_common(1)[0] if w_counter else (None, 0)
            dna[feat] = {
                "type": "categorical",
                "most_common_in_winners": top_winner_val[0],
                "frequency_in_winners": f"{top_winner_val[1]}/{len(w_vals)}",
                "distribution_winners": dict(w_counter),
                "distribution_losers": dict(l_counter) if l_counter is not None else None,
            }

    snapshot = {
        "generated_at": datetime.datetime.utcnow().isoformat(),
        "product_slug": product_slug,
        "total_creatives": len(rows),
        "winners": len(winners),
        "losers": len(losers),
        "dna": dna,
    }

    conn.execute("""
        INSERT INTO dna_snapshots (product_slug, creative_count, winner_count, dna_json)
        VALUES (?, ?, ?, ?)
    """, (product_slug, len(rows), len(winners), json.dumps(snapshot)))
    conn.commit()

    return snapshot


def show_latest_dna(workspace_product: Path):
    profile_path = workspace_product / "creative-dna" / "dna-profile.json"
    if not profile_path.exists():
        print("No DNA profile yet. Run `dna <product>` to generate.")
        return
    print(profile_path.read_text())


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init")
    s.add_argument("workspace", type=Path)

    s = sub.add_parser("add")
    s.add_argument("workspace", type=Path)
    s.add_argument("creative_id", type=str)
    s.add_argument("features_file", type=Path)
    s.add_argument("--product", required=True)

    s = sub.add_parser("update")
    s.add_argument("workspace", type=Path)
    s.add_argument("creative_id", type=str)
    s.add_argument("perf_file", type=Path)

    s = sub.add_parser("stats")
    s.add_argument("workspace", type=Path)
    s.add_argument("--product", required=True)

    s = sub.add_parser("dna")
    s.add_argument("workspace", type=Path)
    s.add_argument("--product", required=True)

    s = sub.add_parser("show")
    s.add_argument("workspace", type=Path)

    args = p.parse_args()
    db = args.workspace / "creative-dna" / "registry.db"

    if args.cmd == "init":
        init(args.workspace)
    elif args.cmd == "add":
        add_creative(db, args.creative_id, args.features_file, args.product)
    elif args.cmd == "update":
        update_performance(db, args.creative_id, args.perf_file)
    elif args.cmd == "stats":
        stats(db, args.product)
    elif args.cmd == "dna":
        snapshot = compute_dna(db, args.product)
        out = args.workspace / "creative-dna" / "dna-profile.json"
        out.write_text(json.dumps(snapshot, indent=2))
        print(f"DNA profile saved: {out}")
        print(json.dumps(snapshot, indent=2))
    elif args.cmd == "show":
        show_latest_dna(args.workspace)


if __name__ == "__main__":
    main()
