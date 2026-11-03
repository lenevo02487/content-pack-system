"""Quality gate: a pack does not ship until every check passes.

Checks: no empty fields, every caption carries a CTA, hashtag count in
platform range, weekday matches the real calendar, captions unique,
pillar mix stays within +/-1 post of the configured shares, and no
placeholder/lorem text anywhere.
"""
from __future__ import annotations

from collections import Counter
from datetime import date

from .generator import WEEKDAYS, target_counts
from .model import Pillar, ScheduledPost

CTA_MARKERS = ("?", "comment", "tag karo", "batao", "save karo", "share",
               "order", "aao", "visit", "book", "dm", "vote")
BANNED = ("lorem", "placeholder", "todo", "xxx")


def validate(posts: list[ScheduledPost], pillars: list[Pillar]) -> list[str]:
    problems: list[str] = []
    if not posts:
        return ["pack is empty"]
    seen_captions: set[str] = set()
    for p in posts:
        tag = f"post {p.number} ({p.date})"
        for field_name in ("theme", "caption", "design", "best_time"):
            if not getattr(p, field_name).strip():
                problems.append(f"{tag}: empty {field_name}")
        low = p.caption.lower()
        if not any(m in low for m in CTA_MARKERS):
            problems.append(f"{tag}: caption has no call to action")
        if any(b in low for b in BANNED):
            problems.append(f"{tag}: banned placeholder text in caption")
        if not (3 <= len(p.hashtags) <= 10):
            problems.append(f"{tag}: hashtag count {len(p.hashtags)} outside 3-10")
        if any(not h.startswith("#") or " " in h for h in p.hashtags):
            problems.append(f"{tag}: malformed hashtag")
        real_day = WEEKDAYS[date.fromisoformat(p.date).weekday()]
        if p.day != real_day:
            problems.append(f"{tag}: weekday {p.day} != real {real_day}")
        if p.caption in seen_captions:
            problems.append(f"{tag}: duplicate caption")
        seen_captions.add(p.caption)
    if sum(p.share_percent for p in pillars) != 100:
        problems.append("pillar shares do not sum to 100")
    targets = target_counts(pillars, len(posts))
    actual = Counter(p.pillar for p in posts)
    for name, want in targets.items():
        if abs(actual.get(name, 0) - want) > 0:
            problems.append(f"pillar {name}: {actual.get(name, 0)} posts, target {want}")
    return problems
