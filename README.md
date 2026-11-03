# Content Pack System — Pillars In, Validated Calendar Out

A small system that turns content *seeds* into a ready-to-post social
media pack (CSV calendar + Markdown reading copy) for a small business —
and refuses to ship a broken pack: generation runs a validation gate
and exits non-zero if any post fails a check.

## How it works

1. **Content pillars first** (`pack_config.json`) — 4 pillars with fixed
   shares that must sum to 100: Educate 34%, Engage 26%, Story 20%,
   Offer 20%. The scheduler guarantees the mix lands exactly on target.
2. **Seeds** (`seeds.json`) — one entry per post idea: pillar, platform,
   format, theme, a fully written caption, design direction, hashtags,
   best posting time, and optional repurposing notes (a Reel's last frame
   becomes a Story teaser — derivatives are planned, not copy-pasted).
3. **Schedule** — posts interleave pillars round-robin over consecutive
   days (two on Sundays by default), so the feed never clumps one theme.
4. **Validate** — every post must have a call to action, 3–10 well-formed
   hashtags, no empty fields, no placeholder text, a weekday that matches
   the real calendar, and a unique caption.

## Run it

```bash
python generate.py --config pack_config.json --seeds seeds.json --out out/
python -m unittest discover -s tests   # 5 tests
```

## Sample run (actual output)

```
OK: 15 posts validated, wrote out/content-pack.csv and content-pack.md
    (2026-11-02 .. 2026-11-15)
```

A full generated pack is kept in `sample_output/` — 15 posts for a
fictional sample tea house, with per-post pillar, purpose, platform
adaptation and repurposing notes.

## Layout

```
content_pack/
  model.py       Pillar / Seed / ScheduledPost dataclasses
  generator.py   share-exact scheduling, pillar interleaving
  validator.py   the quality gate (CTA, hashtags, weekdays, mix)
  export.py      CSV calendar + Markdown pack
generate.py      CLI — validate, then write
```

## Honest scope

Captions in the sample pack are real, finished writing for a fictional
business. On a client pack, prices, offers and testimonials are replaced
with the client's own verified details before anything is posted.

## Want a pack for your business?

Send me your business type and offers — I'll draft a free sample post in
your voice first. Judge the writing, then decide. — Abhishek
