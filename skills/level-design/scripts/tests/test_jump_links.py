"""Tests for jump_links.py."""
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "jump_links.py")
FIX = os.path.join(HERE, "fixtures", "links")
EXAMPLE = os.path.join(HERE, "..", "..", "assets", "example-jump-sequence.md")


def run(path, *extra, stdin=None):
    p = subprocess.run([sys.executable, "-I", SCRIPT, path, "--json"] + list(extra),
                       capture_output=True, text=True, input=stdin)
    d = json.loads(p.stdout)
    return p.returncode, d, {c["check"]: c for c in d.get("checks", [])}


def fix(name):
    return os.path.join(FIX, name)


class TestJumpLinks(unittest.TestCase):
    def test_worked_example_passes(self):
        code, d, c = run(EXAMPLE)
        self.assertEqual(code, 0, c)
        self.assertTrue(all(x["status"] == "PASS" for x in d["checks"]), c)
        links = {x["link"]: x for x in d["links"]}
        self.assertEqual(links["BM->AL"]["band"], "routine")
        self.assertAlmostEqual(links["BM->AL"]["pct"], 2.6 / (2.0 * (1 + (1 - 0.5 / 1.2) ** 0.5)), 3)
        self.assertEqual(links["AL->RF"]["fall_band"], "committed")
        self.assertEqual(d["summary"]["tier"], 3)

    def test_broken_draft_gets_prescriptive_fix(self):
        with open(EXAMPLE, encoding="utf-8") as f:
            text = f.read()
        text = text.replace("| BM | AL | jump | 2.6 | 0.5 |", "| BM | AL | jump | 3.6 | 1.0 |")
        text = text.replace("| 8.2 | 11.6 | 12 |", "| 8.2 | 12.6 | 12.5 |")
        code, d, c = run("-", stdin=text)
        self.assertEqual(code, 1)
        msg = " ".join(c["reachability"]["details"])
        self.assertIn("128%", msg)
        self.assertIn("shorten the gap to <= 2.82m", msg)
        self.assertEqual(c["softlock"]["status"], "SKIP")

    def test_traps(self):
        code, d, c = run(fix("traps.md"))
        self.assertEqual(code, 1)
        self.assertEqual(c["softlock"]["status"], "FAIL")
        self.assertIn("P is reachable", c["softlock"]["details"][0])
        self.assertEqual(c["respawn"]["status"], "FAIL")
        self.assertIn("respawns at C", c["respawn"]["details"][0])
        self.assertEqual(c["falls"]["status"], "FAIL")
        self.assertEqual(c["fail-stated"]["status"], "WARN")

    def test_teasers(self):
        code, d, c = run(fix("teasers.md"))
        self.assertEqual(code, 1)
        det = c["teasers"]["details"]
        self.assertEqual(len(det), 1)
        self.assertIn("S->T1", det[0])     # 108%: looks makeable
        # T2 at 154% is clean; T3 is reachable with the later double jump only

    def test_depth_consistency_and_critical(self):
        code, d, c = run(fix("depth.md"))
        self.assertEqual(code, 1)
        self.assertEqual(c["consistency"]["status"], "FAIL")
        self.assertIn("B->G", c["consistency"]["details"][0])
        self.assertEqual(c["critical-max"]["status"], "FAIL")
        self.assertIn("<= 3.6m", c["critical-max"]["details"][0])
        self.assertEqual(c["depth-axis"]["status"], "WARN")
        self.assertEqual(len(c["depth-axis"]["details"]), 2)
        links = {x["link"]: x for x in d["links"]}
        self.assertAlmostEqual(links["A->B"]["gap"], 3.8, 6)    # filled from coordinates

    def test_critical_max_flag(self):
        code, d, c = run(fix("depth.md"), "--critical-max", "1.0")
        self.assertEqual(c["critical-max"]["status"], "PASS")

    def test_json_chain_tier_and_teaches(self):
        code, d, c = run(fix("chain.json"))
        self.assertEqual(code, 0, c)
        s = d["summary"]
        self.assertEqual(s["longest_chain"], 5)
        self.assertEqual(s["techniques"], ["bhop", "jump"])
        self.assertEqual(s["tier"], 6)
        self.assertEqual(c["respawn"]["status"], "WARN")
        code, d, c = run(fix("chain.json"), "--teaches", "bhop")
        self.assertEqual(c["teaches"]["status"], "WARN")    # required, but first use is 87%
        code, d, c = run(fix("chain.json"), "--teaches", "jump,bhop")
        self.assertEqual(c["teaches"]["status"], "WARN")

    def test_teaches_bypass_fails(self):
        code, d, c = run(EXAMPLE, "--teaches", "mantle")
        self.assertEqual(c["teaches"]["status"], "FAIL")
        self.assertEqual(code, 1)

    def test_kit_override_and_bad_input(self):
        code, d, c = run(EXAMPLE, "--kit", '{"moves": {"jump": {"distance": 3.0, "height": 1.2}}}')
        self.assertEqual(code, 1)    # shorter jump breaks BM->AL
        code, d, _ = run("-", stdin="| From | To |\n|---|---|\n| A | B |\n")
        self.assertEqual(code, 2)
        self.assertIn("Gap and Rise", d["error"])
        moves = "| Move | Distance | Height |\n|---|---|---|\n| jump | 4 | 1 |\n\n"
        code, d, _ = run("-", stdin=moves + "| From | To | Gap | Rise |\n|---|---|---|---|\n| A | B | 1 | 0 |\n")
        self.assertEqual(code, 2)
        self.assertIn("start", d["error"])
        code, d, _ = run("-", stdin="no tables here\n")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
