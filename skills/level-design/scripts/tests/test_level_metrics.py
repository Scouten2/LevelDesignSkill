"""Tests for level_metrics.py. Run from the skill root:
python3 -I -m unittest discover -s scripts/tests -p 'test_level_metrics.py'
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
FIX = os.path.join(HERE, "fixtures", "puzzle")
METRICS = os.path.join(SCRIPTS, "level_metrics.py")


def fx(name):
    return os.path.join(FIX, name)


def run(args, stdin=None):
    p = subprocess.run([sys.executable, "-I", METRICS] + args, input=stdin, capture_output=True,
                       text=True, timeout=60)
    return p.returncode, p.stdout, p.stderr


def run_json(args, stdin=None):
    code, out, _ = run(args + ["--json"], stdin)
    return code, json.loads(out)


class LevelMetricsTests(unittest.TestCase):
    def test_unstack_metrics(self):
        code, r = run_json([fx("unstack.txt")])
        self.assertEqual(code, 0)
        m = r["levels"][0]["metrics"]
        self.assertEqual(m["size"], [7, 7])
        self.assertEqual(m["wall_density"], round(35 / 49.0, 3))
        self.assertEqual(m["regions"], 1)
        self.assertEqual(m["dead_end_cells"], 1)
        self.assertEqual(m["dead_end_examples"], [[3, 5]])
        self.assertEqual((m["boxes"], m["goals"]), (2, 2))

    def test_corridor_and_dead_ends(self):
        code, r = run_json(["-"], stdin="#####\n#@-.#\n#####\n")
        m = r["levels"][0]["metrics"]
        self.assertEqual(m["dead_end_cells"], 2)
        self.assertEqual(m["corridor_ratio"], round(1 / 3.0, 3))

    def test_exterior_excluded_and_regions(self):
        code, r = run_json([fx("ragged_sokoban.txt")])
        m = r["levels"][0]["metrics"]
        self.assertEqual(m["regions"], 1)
        self.assertGreater(m["exterior_cells"], 0)
        code, r = run_json(["-"], stdin="#######\n#@-#--#\n#$.#--#\n#######\n")
        self.assertEqual(r["levels"][0]["metrics"]["regions"], 2)
        self.assertTrue(r["levels"][0]["warnings"])

    def test_platformer(self):
        code, r = run_json([fx("platformer_chunk.txt"), "--legend", "platformer"])
        m = r["levels"][0]["metrics"]
        self.assertEqual(m["gap_columns"], 2)
        self.assertEqual(m["max_gap_width"], 2)
        self.assertEqual((m["hazards"], m["enemies"]), (2, 1))
        self.assertEqual(len(m["harshness_per_column"]), 16)
        self.assertGreater(m["linearity_stddev"], 0)
        code, r = run_json(["-", "--legend", "platformer"], stdin="------\n@----F\nXXXXXX\n")
        self.assertEqual(r["levels"][0]["metrics"]["linearity_stddev"], 0.0)

    def test_compare_flags_mirror_as_duplicate(self):
        with open(fx("two_box.txt")) as fh:
            rows = fh.read().split()
        mirrored = "\n".join(r[::-1] for r in rows) + "\n"
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "mirror.txt")
            with open(p, "w") as fh:
                fh.write(mirrored)
            code, r = run_json([fx("two_box.txt"), "--compare", p])
        self.assertEqual(code, 1)
        pair = r["pairs"][0]
        self.assertEqual(pair["hamming"], 0)
        self.assertTrue(pair["near_duplicate"])
        self.assertIn("mirror", pair["best_alignment"])

    def test_compare_different_levels(self):
        code, r = run_json([fx("unstack.txt"), "--compare", fx("two_box.txt"), fx("open_room_4box.txt")])
        self.assertEqual(code, 0)
        self.assertEqual(len(r["pairs"]), 3)
        self.assertFalse(any(p["near_duplicate"] for p in r["pairs"]))
        code, out, _ = run([fx("unstack.txt"), "--compare", fx("unstack_draft.txt")])
        self.assertEqual(code, 1)
        self.assertIn("NEAR-DUPLICATE", out)
        self.assertIn("Not modelled:", out)

    def test_errors_and_help(self):
        self.assertEqual(run([fx("missing.txt")])[0], 2)
        code, out, _ = run(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("--compare", out)


if __name__ == "__main__":
    unittest.main()
