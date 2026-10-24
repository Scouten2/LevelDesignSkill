"""Tests for dependency_chart.py."""
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "dependency_chart.py")
FIX = os.path.join(HERE, "fixtures", "graph")


def run(fixture, *extra):
    p = subprocess.run([sys.executable, "-I", SCRIPT, os.path.join(FIX, fixture)] + list(extra),
                       capture_output=True, text=True)
    return p.returncode, p.stdout


class TestDependencyChart(unittest.TestCase):
    def test_layers_widths_bottlenecks(self):
        code, out = run("deps_ok.txt", "--json")
        d = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual([l["width"] for l in d["layers"]], [1, 1, 3, 1, 1])
        self.assertEqual(d["critical_path_length"], 5)
        self.assertEqual(d["critical_path"][0], "start")
        self.assertEqual(d["critical_path"][-1], "gate")
        self.assertEqual(d["bottlenecks"], ["dig", "wall"])
        self.assertEqual(d["expanding"], ["dig"])
        self.assertIn("wall", d["contracting"])
        self.assertFalse(d["gilbert"]["ok"])

    def test_cycles_and_unreachable(self):
        code, out = run("deps_bad.txt", "--json")
        d = json.loads(out)
        self.assertEqual(code, 1)
        self.assertEqual(d["cycles"], [["b", "c"]])
        reasons = {u["id"]: u["reason"] for u in d["unreachable"]}
        self.assertIn("crowbar", reasons["d"])
        self.assertIn("cycle", reasons["b"])

    def test_json_input_and_width(self):
        code, out = run("deps_wide.json", "--json")
        d = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(d["max_width"], 4)
        self.assertEqual(d["opens"]["hub"], 4)

    def test_mermaid(self):
        code, out = run("deps_ok.txt", "--mermaid")
        self.assertTrue(out.startswith("flowchart TD"))
        self.assertIn("dig -->|yard_access| guard", out)
        self.assertIn("%% Not modelled:", out)
        code, out = run("deps_bad.txt", "--mermaid")
        self.assertEqual(code, 1)
        self.assertIn("missing_crowbar", out)

    def test_parse_error(self):
        p = subprocess.run([sys.executable, "-I", SCRIPT, "-"], input="a: x | wants: y\n",
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("Not modelled:", p.stdout)


if __name__ == "__main__":
    unittest.main()
