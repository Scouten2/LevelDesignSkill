"""Tests for grid_puzzle_solve.py. Run from the skill root:
python3 -I -m unittest discover -s scripts/tests -p 'test_grid*'
"""
import json
import os
import subprocess
import sys
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
FIX = os.path.join(HERE, "fixtures", "puzzle")
SOLVE = os.path.join(SCRIPTS, "grid_puzzle_solve.py")
sys.path.insert(0, SCRIPTS)
import grid_lint  # noqa: E402
import grid_puzzle_solve as gps  # noqa: E402


def fx(name):
    return os.path.join(FIX, name)


def run(args, stdin=None, timeout=120):
    p = subprocess.run([sys.executable, "-I", SOLVE] + args, input=stdin, capture_output=True,
                       text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def solve(name, *args):
    code, out, err = run([fx(name), "--json"] + list(args))
    return code, json.loads(out)


class SokobanCore(unittest.TestCase):
    def test_unstack_reference_numbers(self):
        # Numbers quoted in references/puzzle-craft.md (worked example "Unstack").
        code, r = solve("unstack.txt", "--metrics", "--classes", "--intended", "rruuullldRDDrruuLrddlluU")
        self.assertEqual(code, 0)
        self.assertEqual(r["result"], "solvable")
        self.assertEqual((r["pushes"], r["moves"]), (5, 24))
        self.assertEqual(r["solution"], "rruuullldRDDrruuLrddlluU")
        self.assertEqual(r["classes"]["count"], 1)
        m = r["metrics"]
        self.assertEqual(m["first_move_traps"]["traps"], 1)
        self.assertEqual(m["first_move_traps"]["first_pushes"], 2)
        self.assertEqual(m["counter_intuitive_pushes"], 1)
        self.assertEqual(m["box_changes"], 2)
        self.assertEqual(m["box_changes_scope"], "minimum over all solutions")
        self.assertEqual(m["entanglement_excess"], 1)
        self.assertEqual(m["dead_end_ratio_note"], "undo need, not difficulty")
        self.assertFalse(r["intended"]["shortcut"])

    def test_unstack_draft_has_two_classes(self):
        code, r = solve("unstack_draft.txt", "--metrics", "--classes")
        self.assertEqual(r["classes"]["count"], 2)
        self.assertEqual(r["metrics"]["first_move_traps"]["traps"], 0)

    def test_unsolvable_start_deadlock(self):
        code, r = solve("unsolvable_corner.txt")
        self.assertEqual(code, 1)
        self.assertEqual(r["result"], "unsolvable")

    def test_unsolvable_needs_search(self):
        code, r = solve("unsolvable_search.txt", "--classes")
        self.assertEqual(code, 1)
        self.assertEqual(r["result"], "unsolvable")
        self.assertGreater(r["nodes_expanded"], 1)
        self.assertEqual(r["classes"]["count"], 0)

    def test_exit_level_with_box_obstacle(self):
        code, r = solve("exit_level.txt")
        self.assertEqual(code, 0)
        self.assertEqual((r["pushes"], r["moves"]), (0, 5))

    def test_human_output(self):
        code, out, _ = run([fx("two_box.txt")])
        self.assertEqual(code, 0)
        self.assertIn("SOLVABLE", out)
        self.assertIn("Not modelled:", out)


class Rules(unittest.TestCase):
    def test_ice_box_slide(self):
        code, r = solve("ice_box_slide.txt")
        self.assertEqual(r["solution"], "R")
        self.assertIn("ice", r["rules_used"])
        code, r = solve("ice_box_slide.txt", "--forbid", "ice")
        self.assertEqual((r["pushes"], r["moves"]), (3, 3))
        self.assertNotIn("ice", r["rules_used"])

    def test_ice_player_slide(self):
        code, r = solve("ice_player_slide.txt")
        self.assertEqual(r["solution"], "rddl")
        self.assertEqual(r["rules_used"], ["ice"])
        code, r = solve("ice_player_slide.txt", "--forbid", "ice")
        self.assertEqual(r["moves"], 10)

    def test_key_door(self):
        code, r = solve("key_door.txt")
        self.assertEqual(code, 0)
        self.assertEqual(r["solution"], "rrdrru")
        self.assertIn("keys", r["rules_used"])
        code, r = solve("key_door.txt", "--forbid", "keys")
        self.assertEqual((code, r["result"]), (1, "unsolvable"))

    def test_key_door_bypass_detected(self):
        code, r = solve("key_door_bypass.txt", "--forbid", "keys")
        self.assertEqual((code, r["result"]), (0, "solvable"))   # solvable without keys -> bypass
        self.assertEqual(r["rules_forbidden"], ["keys"])

    def test_pit_fill(self):
        code, r = solve("pit_fill.txt")
        self.assertEqual(r["solution"], "Rrrr")
        self.assertEqual(r["rules_used"], ["push", "pits"])
        code, r = solve("pit_fill.txt", "--forbid", "pits")
        self.assertEqual(r["result"], "unsolvable")

    def test_switch_gate(self):
        code, r = solve("switch_gate.txt", "--metrics", "--classes")
        self.assertEqual(r["solution"], "rDurrrdd")
        self.assertEqual(r["rules_used"], ["push", "switches"])
        self.assertEqual(r["classes"]["count"], 1)
        code, r = solve("switch_gate.txt", "--forbid", "switches")
        self.assertEqual(r["result"], "unsolvable")

    def test_gate_closes_when_box_leaves_switch(self):
        # The box must stay on the switch while the player walks through the gate.
        rows = ["########",
                "#@$!---#",
                "#----|X#",
                "########"]
        out = gps.analyse(rows)
        self.assertEqual(out["result"], "solvable")
        self.assertEqual(out["solution"], "Rdrrrr")
        lv = gps.Level(rows)
        lv.finalise()
        mm = gps.MoveModel(lv)
        on = lv.pos_of(3, 1)
        off = lv.pos_of(4, 1)
        right = 3
        # player at (4,2) stepping right into the gate (5,2)
        self.assertIsNotNone(mm.step((lv.pos_of(4, 2), 1 << on, 0, 0, 0, 0), right))
        self.assertIsNone(mm.step((lv.pos_of(4, 2), 1 << off, 0, 0, 0, 0), right))

    def test_forbid_box(self):
        code, r = solve("unstack.txt", "--forbid", "box:3,2")
        self.assertEqual(r["result"], "unsolvable")
        self.assertEqual(run([fx("unstack.txt"), "--forbid", "box:9,9"])[0], 2)
        self.assertEqual(run([fx("unstack.txt"), "--forbid", "lava"])[0], 2)


class Intended(unittest.TestCase):
    def test_shortcut_detected(self):
        code, r = solve("shortcut_room.txt", "--intended", "urDldRRRdrU")
        self.assertEqual(code, 1)
        it = r["intended"]
        self.assertTrue(it["legal"] and it["solves"])
        self.assertTrue(it["shortcut"])
        self.assertEqual(it["shorter_by_pushes"], 2)

    def test_optimal_intended_and_case_insensitive(self):
        self.assertEqual(run([fx("shortcut_room.txt"), "--intended", "RRR"])[0], 0)
        code, r = solve("shortcut_room.txt", "--intended", "r r r")
        self.assertEqual(code, 0)
        self.assertTrue(any("case" in n for n in r["intended"]["notes"]))

    def test_walking_detour_is_not_a_shortcut(self):
        code, r = solve("shortcut_room.txt", "--intended", "udRRR")
        self.assertEqual(code, 0)
        self.assertFalse(r["intended"]["shortcut"])
        self.assertTrue(any("walking" in n for n in r["intended"]["notes"]))

    def test_illegal_and_non_solving(self):
        code, r = solve("unstack.txt", "--intended", "rrrr")
        self.assertEqual(code, 1)
        self.assertFalse(r["intended"]["legal"])
        code, r = solve("unstack.txt", "--intended", "rru")
        self.assertEqual(code, 1)
        self.assertFalse(r["intended"]["solves"])
        self.assertEqual(run([fx("unstack.txt"), "--intended", "rrx"])[0], 2)

    def test_move_engine_shortcut(self):
        code, r = solve("ice_player_slide.txt", "--intended", "rddudl")
        self.assertEqual(code, 1)
        self.assertEqual(r["intended"]["shorter_by_moves"], 2)


class CapsAndPerformance(unittest.TestCase):
    def test_open_room_4box_8x10_within_cap(self):
        t = time.time()
        code, r = solve("open_room_4box_8x10.txt", "--max-seconds", "60")
        self.assertLess(time.time() - t, 75)
        self.assertIn(r["result"], ("solvable", "unknown"))
        self.assertIn(code, (0, 3))

    def test_open_room_4box_8x10_metrics_within_cap(self):
        t = time.time()
        code, r = solve("open_room_4box_8x10.txt", "--metrics", "--classes", "--max-seconds", "30")
        self.assertLess(time.time() - t, 45)
        self.assertIn(r["result"], ("solvable", "unknown"))

    def test_node_cap_returns_unknown(self):
        code, r = solve("walled_12x12_5box.txt", "--max-nodes", "50")
        self.assertEqual(code, 3)
        self.assertEqual(r["result"], "unknown")
        self.assertEqual(r["cap_reason"], "node cap")

    def test_time_cap_returns_unknown_quickly(self):
        t = time.time()
        code, r = solve("open_room_7box_cap.txt", "--max-seconds", "0.05")
        self.assertLess(time.time() - t, 10)
        self.assertEqual(code, 3)
        self.assertEqual(r["result"], "unknown")


class Soundness(unittest.TestCase):
    """The pruned push-level search must agree with an unpruned move-level BFS."""

    def check(self, rows):
        lv = gps.Level(rows)
        lv.finalise()
        fast = gps.analyse(rows)
        mm = gps.MoveModel(lv)
        mm.dead_state = lambda boxes: False
        slow = gps.search(mm, gps.Budget(500000, 30), want_dag=False)
        self.assertEqual(fast["result"], slow["status"], rows)
        if fast["result"] == "solvable":
            self.assertGreaterEqual(fast["moves"], slow["best"])
            path = gps.first_path(slow, slow["goals"][0])
            self.assertLessEqual(fast["pushes"], sum(1 for e in path if e[1] >= 0))

    def test_fixtures_agree(self):
        for name in ("unstack.txt", "unstack_draft.txt", "two_box.txt", "unsolvable_search.txt",
                     "exit_level.txt", "shortcut_room.txt"):
            with open(fx(name)) as fh:
                rows, _ = grid_lint.extract_grid(fh.read())
            self.check(rows)

    def test_random_small_levels_agree(self):
        import random
        rnd = random.Random(1234)
        for _ in range(150):
            w, h = rnd.choice([(6, 5), (7, 6)])
            cells = [["#" if r in (0, h - 1) or c in (0, w - 1) else ("#" if rnd.random() < 0.1 else "-")
                      for c in range(w)] for r in range(h)]
            free = [(c, r) for r in range(h) for c in range(w) if cells[r][c] == "-"]
            nb = rnd.choice([1, 2])
            if len(free) < 2 * nb + 2:
                continue
            rnd.shuffle(free)
            c, r = free[0]
            cells[r][c] = "@"
            for c, r in free[1:1 + nb]:
                cells[r][c] = "$"
            for c, r in free[1 + nb:1 + 2 * nb]:
                cells[r][c] = "."
            self.check(["".join(x) for x in cells])


class Errors(unittest.TestCase):
    def test_parse_errors(self):
        self.assertEqual(run(["-"], stdin="#####\n#@Z.#\n#####\n")[0], 2)
        self.assertEqual(run(["-"], stdin="#####\n#@@.#\n#$--#\n#####\n")[0], 2)
        self.assertEqual(run(["-"], stdin="#####\n#@--#\n#####\n")[0], 2)
        self.assertEqual(run([fx("missing.txt")])[0], 2)
        code, out, _ = run(["-", "--json"], stdin="#####\n#@Z.#\n#####\n")
        self.assertEqual(json.loads(out)["result"], "error")

    def test_help(self):
        code, out, _ = run(["--help"])
        self.assertEqual(code, 0)
        for word in ("--forbid", "--intended", "Size envelope", "box_changes", "undo need"):
            self.assertIn(word, out)

    def test_stdin_and_ruled_markdown(self):
        code, r = solve("ruled_fenced.md")
        self.assertEqual((r["pushes"], r["moves"]), (5, 24))
        with open(fx("unstack.txt")) as fh:
            code, out, _ = run(["-", "--json"], stdin=fh.read())
        self.assertEqual(json.loads(out)["pushes"], 5)


if __name__ == "__main__":
    unittest.main()
