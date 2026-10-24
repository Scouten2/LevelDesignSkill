"""Tests for beat_lint.py."""
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "beat_lint.py")
FIX = os.path.join(HERE, "fixtures", "beats")


def run(fixture, *extra, stdin=None):
    path = os.path.join(FIX, fixture) if fixture != "-" else "-"
    p = subprocess.run([sys.executable, "-I", SCRIPT, path, "--json"] + list(extra),
                       capture_output=True, text=True, input=stdin)
    d = json.loads(p.stdout)
    return p.returncode, d, {c["check"]: c for c in d.get("checks", [])}


class TestBeatLint(unittest.TestCase):
    def test_process_md_headers_and_cell_conventions(self):
        code, d, c = run("good.md")
        self.assertEqual(code, 0, c)
        self.assertEqual(d["beats"], 6)
        for col in ("num", "beat", "intensity", "concepts", "choice", "deaths", "replay",
                    "checkpoint", "duration"):
            self.assertIn(col, d["columns"])
        t = d["beat_table"]
        self.assertEqual(t[0]["new_concepts"], 0)        # "0" = none
        self.assertEqual(t[2]["new_concepts"], 0)        # em dash = none
        self.assertEqual(t[1]["deaths"], 0.5)            # decimal deaths
        self.assertTrue(t[3]["replay_estimated"])       # n/a -> empty, estimated from durations
        self.assertEqual(t[3]["checkpoint"], "")
        self.assertEqual(t[4]["checkpoint"], "C2")       # own-row checkpoint precedes beat 5
        self.assertEqual(c["checkpoints"]["status"], "PASS")
        self.assertTrue(all(x["status"] == "PASS" for x in d["checks"]))

    def test_all_failures(self):
        code, d, c = run("bad.md")
        self.assertEqual(code, 1)
        for name in ("rest-around-peaks", "peak-run", "new-concepts", "choice-gaps",
                     "replay-budget", "peak-vs-replay", "checkpoints", "flat-stretches"):
            self.assertEqual(c[name]["status"], "FAIL", name)

    def test_overrides(self):
        code, d, c = run("bad.md", "--max-peak-run", "3", "--flat-run", "0", "--concepts-fail", "0",
                         "--replay-budget", "50")
        self.assertEqual(c["peak-run"]["status"], "PASS")
        self.assertNotIn("flat-stretches", c)
        self.assertEqual(c["new-concepts"]["status"], "WARN")
        self.assertEqual(c["replay-budget"]["status"], "PASS")

    def test_concept_warning_and_estimated_replay(self):
        md = ("| Beat | Intensity | New concepts | Expected deaths | Checkpoint | Duration |\n"
              "|---|---|---|---|---|---|\n"
              "| A | 1 | dash, glide | 0 | C1 | 10 |\n"
              "| B | 2 | dash | 1 | | 30 |\n"
              "| C | 1 | — | 0 | | 5 |\n")
        code, d, c = run("-", stdin=md)
        self.assertEqual(code, 1)  # 0.5 x 40 s estimated replay > 10 s budget
        self.assertEqual(c["new-concepts"]["status"], "WARN")
        self.assertEqual(c["replay-budget"]["status"], "FAIL")
        self.assertIn("(estimated)", c["replay-budget"]["details"][0])
        self.assertTrue(d["replay_estimated_from_durations"])
        self.assertEqual(d["beat_table"][1]["replay_eff"], 40)
        self.assertEqual(c["choice-gaps"]["status"], "SKIPPED")

    def test_no_table(self):
        p = subprocess.run([sys.executable, "-I", SCRIPT, "-"], input="no table here\n",
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("Not modelled:", p.stdout)
        p = subprocess.run([sys.executable, "-I", SCRIPT, "--help"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
