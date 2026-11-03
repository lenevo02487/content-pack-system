import json
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from content_pack.generator import schedule, target_counts
from content_pack.model import Pillar, Seed
from content_pack.validator import validate

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "pack_config.json").read_text(encoding="utf-8"))
SEEDS = json.loads((ROOT / "seeds.json").read_text(encoding="utf-8"))


class TestPack(unittest.TestCase):
    def setUp(self):
        self.pillars = [Pillar(**p) for p in CFG["pillars"]]
        self.seeds = [Seed(**s) for s in SEEDS]
        self.posts = schedule(self.seeds, self.pillars, date(2026, 11, 2))

    def test_pack_validates_clean(self):
        self.assertEqual(validate(self.posts, self.pillars), [])

    def test_post_count(self):
        self.assertEqual(len(self.posts), 15)

    def test_pillar_targets(self):
        counts = target_counts(self.pillars, 15)
        self.assertEqual(sum(counts.values()), 15)
        self.assertEqual(counts, {"Educate": 5, "Engage": 4, "Story": 3,
                                  "Offer": 3})

    def test_weekday_matches_calendar(self):
        first = self.posts[0]
        self.assertEqual((first.date, first.day), ("2026-11-02", "Monday"))

    def test_validator_catches_missing_cta(self):
        bad = [Seed(pillar="Educate", platform="Instagram", format="Photo post",
                    theme="t", caption="Sirf ek statement, koi sawal nahi.",
                    design="d", hashtags=["#a", "#b", "#c"], best_time="9 AM")]
        posts = schedule(bad, [Pillar("Educate", "educate", 100)], date(2026, 11, 2))
        problems = validate(posts, [Pillar("Educate", "educate", 100)])
        self.assertTrue(any("call to action" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
