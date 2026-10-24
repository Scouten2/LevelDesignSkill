"""Tests for grid_lint.py. Run from the skill root:
python3 -I -m unittest discover -s scripts/tests -p 'test_grid*'
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
LINT = os.path.join(SCRIPTS, "grid_lint.py")


def run(args, stdin=None):
    p = subprocess.run([sys.executable, "-I", LINT] + args, input=stdin, capture_output=True,
                       text=True, timeout=60)
    return p.returncode, p.stdout, p.stderr


def run_json(args, stdin=None):
    code, out, _err = run(args + ["--json"], stdin)
    return code, json.loads(out)


def fx(name):
    return os.path.join(FIX, name)


def check(rep, name):
    for c in rep["checks"]:
        if c["name"] == name:
            return c
    raise AssertionError("no check %s in %s" % (name, [c["name"] for c in rep["checks"]]))


class GridLintTests(unittest.TestCase):
    def test_clean_level_passes(self):
        code, out, _ = run([fx("unstack.txt"), "--legend", "puzzle", "--expect", "@=1", "--expect", "$=2", "--closed"])
        self.assertEqual(code, 0, out)
        self.assertIn("PASS", out)
        self.assertIn("Not modelled:", out)

    def test_fenced_ruled_markdown_and_object_list(self):
        code, rep = run_json([fx("ruled_fenced.md"), "--closed"])
        self.assertEqual(code, 0, rep)
        self.assertTrue(rep["stripped"]["fenced"])
        self.assertTrue(rep["stripped"]["row_prefix"])
        self.assertEqual(rep["stripped"]["ruler_lines"], 1)
        with open(fx("unstack.txt")) as fh:
            self.assertEqual(rep["rows"], fh.read().split())
        names = [c["name"] for c in rep["checks"]]
        self.assertTrue(any(n.startswith("objects") for n in names), names)

    def test_object_list_mismatch_fails(self):
        with open(fx("unstack.txt")) as fh:
            text = fh.read() + "Player (3,4); boxes (3,2) (4,3); goals (3,1) (3,5)\n"
        code, rep = run_json(["-"], stdin=text)
        self.assertEqual(code, 1)
        bad = [c for c in rep["checks"] if not c["ok"]]
        self.assertEqual(len(bad), 1)
        self.assertIn("(4,3)", bad[0]["detail"])

    def test_emit_ruled_round_trip_wide(self):
        code, out, err = run([fx("walled_12x12_5box.txt"), "--emit-ruled"])
        self.assertEqual(code, 0, err)
        lines = out.splitlines()
        self.assertEqual(lines[0], "   0         1")
        self.assertEqual(lines[1], "   012345678901")
        self.assertTrue(lines[2].startswith("00|#"))
        self.assertIn("Not modelled:", err)
        code2, rep = run_json(["-"], stdin=out)
        self.assertEqual(code2, 0)
        with open(fx("walled_12x12_5box.txt")) as fh:
            self.assertEqual(rep["rows"], fh.read().split())

    def test_space_separated_row_index_and_prose(self):
        text = "My level:\n\n 0 #####\n 1 #@$.#\n 2 #####\n\nThat is all.\n"
        code, rep = run_json(["-"], stdin=text)
        self.assertEqual(code, 0, rep)
        self.assertEqual(rep["rows"], ["#####", "#@$.#", "#####"])

    def test_ragged_rows_reported(self):
        code, rep = run_json(["-"], stdin="#####\n#@$.#\n####\n#####\n")
        self.assertEqual(code, 1)
        self.assertEqual(rep["ragged_rows"], [{"row": 2, "length": 4, "expected": 5}])
        self.assertIn("row 2 has 4 chars, expected 5", check(rep, "rectangular")["detail"])

    def test_trailing_spaces_are_trimmed_not_ragged(self):
        code, rep = run_json(["-"], stdin="#####\n#@$.#   \n#####\n")
        self.assertEqual(code, 0, rep)
        self.assertTrue(any("trimmed" in n for n in rep["notes"]))

    def test_unknown_glyph_coordinates(self):
        code, rep = run_json(["-"], stdin="#####\n#@$.#\n#-Z-#\n#####\n")
        self.assertEqual(code, 1)
        self.assertEqual(rep["unknown_glyphs"], [{"glyph": "Z", "col": 2, "row": 2}])
        self.assertIn("(2,2)", check(rep, "known_glyphs")["detail"])

    def test_expect_operators(self):
        f = fx("unstack.txt")
        self.assertEqual(run([f, "--expect", "$=3"])[0], 1)
        self.assertEqual(run([f, "--expect", "$*>=2", "--expect", ".<=2"])[0], 0)
        self.assertEqual(run([f, "--expect", "$4"])[0], 2)

    def test_box_goal_balance(self):
        code, rep = run_json(["-"], stdin="######\n#@$$.#\n######\n")
        self.assertEqual(code, 1)
        self.assertFalse(check(rep, "box_goal_balance")["ok"])
        # pits allow extra boxes
        code, rep = run_json(["-"], stdin="#######\n#@$$O.#\n#######\n")
        self.assertTrue(check(rep, "box_goal_balance")["ok"])

    def test_no_goals_needs_exit(self):
        self.assertEqual(run(["-"], stdin="#####\n#@--#\n#####\n")[0], 1)
        self.assertEqual(run(["-"], stdin="#####\n#@-X#\n#####\n")[0], 0)

    def test_player_count(self):
        code, rep = run_json(["-"], stdin="#####\n#@@.#\n#$--#\n#####\n")
        self.assertEqual(code, 1)
        self.assertIn("found 2", check(rep, "one_player_start")["detail"])

    def test_closed_leak(self):
        code, rep = run_json(["-", "--closed"], stdin="#####\n#@$.-\n#####\n")
        self.assertEqual(code, 1)
        self.assertIn("(4,1)", check(rep, "closed")["detail"])
        # outside spaces of a ragged-style map are fine when the player's area is sealed
        code, rep = run_json([fx("ragged_sokoban.txt"), "--closed"])
        self.assertTrue(check(rep, "closed")["ok"])

    def test_width_height(self):
        f = fx("unstack.txt")
        self.assertEqual(run([f, "--width", "7", "--height", "7"])[0], 0)
        self.assertEqual(run([f, "--width", "8"])[0], 1)

    def test_platformer_legend(self):
        f = fx("platformer_chunk.txt")
        code, rep = run_json([f, "--legend", "platformer"])
        self.assertEqual(code, 0, rep)
        self.assertEqual(rep["counts"]["E"], 1)
        code, rep = run_json([f, "--legend", "puzzle"])
        self.assertEqual(code, 1)

    def test_custom_legend(self):
        with tempfile.TemporaryDirectory() as d:
            leg = os.path.join(d, "leg.json")
            with open(leg, "w") as fh:
                json.dump({"name": "td", "glyphs": {"#": "wall", "-": "floor", "@": "player", "T": "tower"},
                           "player": "@", "solid": "#"}, fh)
            code, rep = run_json(["-", "--legend", leg, "--closed"], stdin="#####\n#@-T#\n#####\n")
            self.assertEqual(code, 0, rep)
            self.assertEqual(rep["legend"], "td")
            self.assertEqual(run(["-", "--legend", os.path.join(d, "missing.json")], stdin="#")[0], 2)

    def test_errors_and_help(self):
        self.assertEqual(run([fx("does_not_exist.txt")])[0], 2)
        self.assertEqual(run(["-"], stdin="\n\n")[0], 2)
        code, out, _ = run(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("--emit-ruled", out)


if __name__ == "__main__":
    unittest.main()
