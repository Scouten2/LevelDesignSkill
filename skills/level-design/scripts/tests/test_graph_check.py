"""Tests for graph_check.py."""
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "graph_check.py")
FIX = os.path.join(HERE, "fixtures", "graph")


def run(fixture, *extra, stdin=None):
    path = os.path.join(FIX, fixture) if fixture != "-" else "-"
    p = subprocess.run([sys.executable, "-I", SCRIPT, path, "--json"] + list(extra),
                       capture_output=True, text=True, input=stdin)
    return p.returncode, json.loads(p.stdout)


class TestGraphCheck(unittest.TestCase):
    def test_key_before_door_order(self):
        code, d = run("keys_ok.json")
        self.assertEqual(code, 0)
        self.assertTrue(d["goal_reachable"])
        prog = d["progression"]
        red = next(i for i, p in enumerate(prog) if "take red_key" in p)
        gate = next(i for i, p in enumerate(prog) if "needs red_key" in p)
        blue = next(i for i, p in enumerate(prog) if "take blue_key" in p)
        boss = next(i for i, p in enumerate(prog) if "needs blue_key" in p)
        self.assertTrue(red < gate < blue < boss)
        self.assertEqual(d["softlocks"], [])

    def test_consumed_key_softlock(self):
        code, d = run("consumed_softlock.json")
        self.assertEqual(code, 1)
        self.assertTrue(d["goal_reachable"])
        types = [s["type"] for s in d["softlocks"]]
        self.assertIn("consumed-key softlock", types)
        s = d["softlocks"][0]
        self.assertEqual(s["move"], "S -> Closet")
        self.assertIn("S-Corridor", s["doors_left_locked"])

    def test_unreachable_nodes_and_items(self):
        code, d = run("unreachable.json")
        self.assertEqual(code, 1)
        self.assertFalse(d["goal_reachable"])
        self.assertEqual(sorted(d["unreachable_nodes"]), ["C", "Island"])
        self.assertEqual(d["unobtainable_items"][0]["item"], "gold_key")
        self.assertEqual(len(d["gates_never_open"]), 1)

    def test_dead_ends_and_cycles(self):
        code, d = run("cycle_dead.mmd")
        self.assertEqual(code, 0)
        dead = {x["node"]: x["items"] for x in d["dead_ends"]}
        self.assertEqual(dead, {"D": [], "E": ["charm"]})
        self.assertEqual(d["loops"], 1)
        self.assertEqual(d["start"], "A")
        self.assertEqual(d["goal"], "F")

    def test_oneway_trap(self):
        code, d = run("oneway_trap.json")
        self.assertEqual(code, 1)
        self.assertEqual(d["softlocks"][0]["type"], "one-way trap")
        self.assertEqual(d["oneway_no_return"][0]["to"], "Pit")

    def test_mermaid_subset(self):
        code, d = run("dungeon.md")
        self.assertEqual(code, 0, d)
        self.assertEqual(d["format"], "mermaid")
        self.assertEqual(d["nodes"], 7)
        self.assertTrue(d["goal_reachable"])
        self.assertEqual(d["vistas"], [{"from": "Tower", "to": "Keep", "label": "vista"}])
        self.assertEqual(d["loops"], 1)
        self.assertFalse([w for w in d["warnings"] if "unparsed" in w])

    def test_mermaid_oneway_quoted_label_and_vista(self):
        src = ("flowchart LR\n%% start: A\n%% goal: C\n"
               'A["Ledge F2"] -.->|"↓drop 4m(one-way)"| B["Pit F0"]\n'
               "B -->|req:rope| C\nA -. vista .- C\nA -->|\"one-way\"| D\n")
        code, d = run("-", stdin=src)
        self.assertEqual(code, 1)  # rope is never placed
        self.assertEqual({(o["from"], o["to"]) for o in d["oneway_no_return"]},
                         {("A", "B"), ("A", "D")})
        self.assertEqual(d["vistas"][0]["from"], "A")
        self.assertEqual(d["unobtainable_items"][0]["reason"], "not placed in any node")

    def test_parse_errors(self):
        p = subprocess.run([sys.executable, "-I", SCRIPT, "-", "--format", "json"],
                           capture_output=True, text=True, input="{bad")
        self.assertEqual(p.returncode, 2)
        self.assertIn("Not modelled:", p.stdout)
        p = subprocess.run([sys.executable, "-I", SCRIPT, "--help"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
