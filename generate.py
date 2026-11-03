#!/usr/bin/env python3
"""Generate a validated content pack (CSV + Markdown) from config + seeds.

    python generate.py --config pack_config.json --seeds seeds.json --out out/
Exits non-zero if the pack fails validation — a broken pack never ships.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from content_pack.export import write_csv, write_md
from content_pack.generator import schedule
from content_pack.model import Pillar, Seed
from content_pack.validator import validate


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default="pack_config.json")
    ap.add_argument("--seeds", default="seeds.json")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    raw_seeds = json.loads(Path(args.seeds).read_text(encoding="utf-8"))
    pillars = [Pillar(**p) for p in cfg["pillars"]]
    seeds = [Seed(**s) for s in raw_seeds]
    start = date.fromisoformat(cfg["start_date"])

    posts = schedule(seeds, pillars, start)
    problems = validate(posts, pillars)
    if problems:
        print("VALIDATION FAILED:")
        for p in problems:
            print(" -", p)
        return 1
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(posts, out / "content-pack.csv")
    write_md(posts, out / "content-pack.md", cfg["business"])
    print(f"OK: {len(posts)} posts validated, wrote {out}/content-pack.csv "
          f"and content-pack.md ({posts[0].date} .. {posts[-1].date})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
