"""Tests for platformer_reach.py (run: python3 -I -m unittest discover -s scripts/tests)."""
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "platformer_reach.py")
FIX = os.path.join(HERE, "fixtures", "platformer")


def run(fixture, kit, *extra):
    if isinstance(kit, dict):
        kit = json.dumps(kit)
    p = subprocess.run([sys.executable, "-I", SCRIPT, os.path.join(FIX, fixture), "--kit", kit,
                        "--json"] + list(extra), capture_output=True, text=True)
    data = json.loads(p.stdout) if p.stdout.strip().startswith("{") else None
    return p.returncode, data, p


def kit(**kw):
    k = {"jump_height": 4.0, "jump_distance": 6.0, "coyote_time": 0}
    k.update(kw)
    return k


class TestPlatformerReach(unittest.TestCase):
    def test_regression_steps_need_height_3(self):
        code, d, _ = run("steps3.txt", kit(jump_height=2))
        self.assertEqual(code, 1)
        self.assertFalse(d["goal_reachable"])
        self.assertLessEqual(d["frontier"]["furthest_col"], 8)
        code, d, _ = run("steps3.txt", kit(jump_height=3))
        self.assertTrue(d["goal_reachable"])
        self.assertEqual(d["easiest_route"]["hardest_usage_pct"], 100.0)
        code, d, _ = run("steps3.txt", kit(jump_height=2.9))
        self.assertFalse(d["goal_reachable"])

    def test_gap(self):
        code, d, _ = run("gap5.txt", kit())
        self.assertEqual(code, 0)
        self.assertTrue(d["goal_reachable"])
        jump = [m for m in d["easiest_route"]["jumps"] if m["dx"] == 5]
        self.assertTrue(jump)
        code, d, _ = run("gap7.txt", kit())
        self.assertEqual(code, 1)
        self.assertFalse(d["goal_reachable"])

    def test_critical_jump_margin(self):
        code, d, _ = run("gap5.txt", kit(jump_distance=5.5))
        self.assertTrue(d["goal_reachable"])
        self.assertEqual(code, 1)
        self.assertEqual(len(d["critical_jumps"]), 1)
        code, d, _ = run("gap5.txt", kit(jump_distance=5.5), "--margin", "0.95")
        self.assertEqual(code, 0)

    def test_hazard_kills(self):
        code, d, _ = run("spikes_narrow.txt", kit())
        self.assertTrue(d["goal_reachable"])
        code, d, _ = run("spikes_wide.txt", kit())
        self.assertFalse(d["goal_reachable"])
        self.assertEqual(code, 1)

    def test_softlock_pit(self):
        code, d, _ = run("softlock.txt", kit())
        self.assertTrue(d["goal_reachable"])
        self.assertEqual(code, 1)
        self.assertEqual(len(d["softlock_pits"]), 1)
        self.assertIn([6, 8], d["softlock_pits"][0]["cells"])

    def test_teaches_double_jump(self):
        code, d, _ = run("tall_wall.txt", kit(double_jump=True), "--teaches", "double_jump")
        self.assertEqual(code, 0)
        self.assertEqual(d["teaches"]["result"], "PASS")
        code, d, _ = run("gap5.txt", kit(double_jump=True), "--teaches", "double_jump")
        self.assertEqual(code, 1)
        self.assertEqual(d["teaches"]["result"], "FAIL")

    def test_teaches_wall_jump_and_height(self):
        code, d, _ = run("tall_wall.txt", kit(wall_jump=True), "--teaches", "wall_jump")
        self.assertEqual(d["teaches"]["result"], "PASS")
        code, d, _ = run("steps3.txt", kit(), "--teaches", "jump_height=2")
        self.assertEqual(d["teaches"]["result"], "PASS")

    def test_one_way_platform(self):
        code, d, _ = run("oneway.txt", kit())
        self.assertTrue(d["goal_reachable"])
        code, d, _ = run("oneway_solid.txt", kit())
        self.assertFalse(d["goal_reachable"])

    def test_ladder(self):
        code, d, _ = run("ladder.txt", kit(jump_height=2))
        self.assertTrue(d["goal_reachable"])
        code, d, _ = run("ladder_removed.txt", kit(jump_height=2))
        self.assertFalse(d["goal_reachable"])

    def test_player_height_2_needs_clearance(self):
        code, d, _ = run("tunnel.txt", kit())
        self.assertTrue(d["goal_reachable"])
        code, d, _ = run("tunnel.txt", kit(player_height=2))
        self.assertFalse(d["goal_reachable"])

    def test_collectibles_and_checkpoints(self):
        code, d, _ = run("collectibles.txt", kit())
        self.assertTrue(d["goal_reachable"])
        self.assertEqual(code, 1)
        self.assertEqual([c["cell"] for c in d["collectibles"]["unreachable"]], [[1, 1]])
        self.assertEqual([c["cell"] for c in d["collectibles"]["reachable"]], [[12, 2]])
        self.assertEqual(d["checkpoints"]["reachable"], [[4, 3]])

    def test_falls_reported(self):
        code, d, _ = run("height_ladder.txt", kit(safe_fall_height=2, fall_damage_height=4))
        self.assertTrue(d["goal_reachable"])
        self.assertTrue(d["falls"]["on_route"])
        self.assertIn(d["falls"]["on_route"][0]["class"], ("costly", "damaging"))

    def test_height_ladder_docs_fixture(self):
        code, d, _ = run("height_ladder.txt", os.path.join(FIX, "kit.json"))
        self.assertEqual(code, 0)
        self.assertEqual(d["frontier"]["furthest_col"], 39)
        code, d, _ = run("height_ladder.txt", kit(jump_height=2.9))
        self.assertFalse(d["goal_reachable"])
        self.assertEqual(d["frontier"]["furthest_col"], 23)

    def test_not_modelled_and_usage_errors(self):
        p = subprocess.run([sys.executable, "-I", SCRIPT, os.path.join(FIX, "gap5.txt"), "--kit",
                            json.dumps(kit())], capture_output=True, text=True)
        self.assertIn("Not modelled:", p.stdout)
        code, d, p = run("gap5.txt", '{"jump_height": 0}')
        self.assertEqual(code, 2)
        code, d, p = run("gap5.txt", kit(), "--teaches", "fly")
        self.assertEqual(code, 2)
        p = subprocess.run([sys.executable, "-I", SCRIPT, "--help"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
