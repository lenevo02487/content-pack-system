"""Core model: content pillars with fixed shares, post seeds, scheduled posts.

System design (from current content-calendar practice):
- 3-5 content pillars, each with a % share of the pack; shares sum to 100.
- Every post has ONE job: educate, engage, build story/trust, or convert —
  and every caption ends with a call to action.
- Repurposing is part of the data: a hero post declares its derivatives
  (e.g. a Reel also becomes a Story teaser) instead of copy-pasting the
  same caption everywhere.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Pillar:
    name: str
    purpose: str            # educate | engage | story | convert
    share_percent: int


@dataclass(frozen=True)
class Seed:
    pillar: str
    platform: str           # Instagram | Facebook | LinkedIn
    format: str             # Photo post | Reel | Carousel | Text post
    theme: str
    caption: str
    design: str
    hashtags: list[str]
    best_time: str
    derivatives: list[str] = field(default_factory=list)  # repurposing notes


@dataclass(frozen=True)
class ScheduledPost:
    number: int
    date: str               # ISO
    day: str
    pillar: str
    purpose: str
    platform: str
    format: str
    theme: str
    caption: str
    design: str
    hashtags: list[str]
    best_time: str
    derivatives: list[str]
