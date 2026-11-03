"""Schedule seeds into a dated pack, honouring pillar shares.

Posts are spread over consecutive days starting from `start_date`
(two posts on Sundays by default, like a real small-business rhythm),
ordered so pillars interleave instead of clumping.
"""
from __future__ import annotations

import math
from datetime import date, timedelta

from .model import Pillar, ScheduledPost, Seed

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
            "Saturday", "Sunday"]


def target_counts(pillars: list[Pillar], total: int) -> dict[str, int]:
    exact = {p.name: total * p.share_percent / 100 for p in pillars}
    counts = {name: math.floor(v) for name, v in exact.items()}
    remaining = total - sum(counts.values())
    by_frac = sorted(exact, key=lambda n: exact[n] - counts[n], reverse=True)
    for name in by_frac[:remaining]:
        counts[name] += 1
    return counts


def schedule(seeds: list[Seed], pillars: list[Pillar], start: date,
             posts_per_day: int = 1, double_days: frozenset[int] = frozenset({6})
             ) -> list[ScheduledPost]:
    counts = target_counts(pillars, len(seeds))
    purpose = {p.name: p.purpose for p in pillars}
    by_pillar: dict[str, list[Seed]] = {}
    for seed in seeds:
        by_pillar.setdefault(seed.pillar, []).append(seed)
    chosen: list[Seed] = []
    for name, want in counts.items():
        pool = by_pillar.get(name, [])
        if len(pool) < want:
            raise ValueError(
                f"pillar {name!r} needs {want} seeds for this pack size, "
                f"only {len(pool)} provided")
        chosen.extend(pool[:want])
    # Interleave pillars round-robin so the feed never clumps one theme.
    queues = {name: [s for s in chosen if s.pillar == name] for name in counts}
    ordered: list[Seed] = []
    while any(queues.values()):
        for name in counts:
            if queues[name]:
                ordered.append(queues[name].pop(0))

    posts: list[ScheduledPost] = []
    day = start
    idx = 0
    while idx < len(ordered):
        slots = 2 if (posts_per_day == 1 and day.weekday() in double_days) else posts_per_day
        for _ in range(slots):
            if idx >= len(ordered):
                break
            seed = ordered[idx]
            idx += 1
            posts.append(ScheduledPost(
                number=idx, date=day.isoformat(), day=WEEKDAYS[day.weekday()],
                pillar=seed.pillar, purpose=purpose[seed.pillar],
                platform=seed.platform, format=seed.format, theme=seed.theme,
                caption=seed.caption, design=seed.design,
                hashtags=seed.hashtags, best_time=seed.best_time,
                derivatives=seed.derivatives))
        day += timedelta(days=1)
    return posts
