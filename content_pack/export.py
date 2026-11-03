"""Export a scheduled pack to CSV (calendar) + Markdown (reading copy)."""
from __future__ import annotations

import csv
from pathlib import Path

from .model import ScheduledPost

COLUMNS = ["Post No", "Date", "Day", "Pillar", "Purpose", "Platform", "Format",
           "Theme", "Caption", "Design Direction", "Hashtags",
           "Best Posting Time", "Repurposing"]


def _row(p: ScheduledPost) -> list[str]:
    return [str(p.number), p.date, p.day, p.pillar, p.purpose, p.platform,
            p.format, p.theme, p.caption, p.design, " ".join(p.hashtags),
            p.best_time, "; ".join(p.derivatives)]


def write_csv(posts: list[ScheduledPost], path: str | Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(COLUMNS)
        for p in posts:
            writer.writerow(_row(p))


def write_md(posts: list[ScheduledPost], path: str | Path,
             business: str) -> None:
    lines = [f"# Content Pack — {business}", "",
             f"{len(posts)} posts, {posts[0].date} to {posts[-1].date}.", ""]
    for p in posts:
        lines += [
            f"## Post {p.number} — {p.day}, {p.date} · {p.platform} · {p.format}",
            f"**Pillar:** {p.pillar} ({p.purpose}) · **Theme:** {p.theme}",
            "", p.caption, "",
            f"**Design:** {p.design}",
            f"**Hashtags:** {' '.join(p.hashtags)}",
            f"**Best time:** {p.best_time}",
        ]
        if p.derivatives:
            lines.append(f"**Repurpose as:** {'; '.join(p.derivatives)}")
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")
