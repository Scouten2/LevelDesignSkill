#!/usr/bin/env python3
"""grid_lint.py - format linter for ASCII level grids (puzzle and platformer legends).

Usage:
  python3 -I scripts/grid_lint.py FILE [--legend puzzle|platformer|PATH.json]
         [--width W] [--height H] [--expect GLYPHS=N ...] [--closed]
         [--emit-ruled] [--json]

FILE is a UTF-8 text file ("-" reads stdin). It may be a bare grid or a
markdown file: if it contains a fenced code block (``` or ~~~), only the first
fenced block is read as the grid. Prose lines above/below an unfenced grid are
skipped when most of their characters are not legend glyphs.

Accepted presentation extras (stripped before checking):
  * column ruler lines made only of digits and spaces, e.g.
        "   0         1" and "   0123456789012"
  * row-index prefixes such as "07|#....#" (also "07:" or "07 " + grid);
    the "|" right after the digits is the separator, not a gate glyph.
  * key-object lines: any line holding "(col,row)" pairs is never a grid row.
    If it reads like "player (1,1); boxes (2,2) (8,2); goals (10,6); key a (4,5)"
    each listed position is compared with the grid (puzzle names: player, box,
    goal, key [a-e], door [A-E], ice, pit, switch, gate, exit; platformer names:
    player/start, goal, checkpoint, coin, key/collectible, enemy, hazard, ladder).

Checks (exit 1 if any fails):
  * dimensions, ragged rows (row, length, expected = --width or the most common
    length). Rows longer than expected only by trailing spaces are trimmed with a
    note; shorter rows fail (pad with '-' or '#').
  * unknown glyphs, reported with (col,row), origin top-left, row 0 at top.
  * exactly one player start (puzzle: @ or +; platformer: @ or M).
  * puzzle legend: box/goal balance ($ + * versus . + + + *); with pits (O)
    extra boxes are allowed; a level with no goals needs an X exit.
    Warnings (not failures): door letters without enough keys, gates without
    switches (a gate with no switch is always open), switches without gates.
  * --expect GLYPHS=N (also >= and <=): count of the listed glyphs summed,
    e.g. --expect @=1 --expect '$=4' --expect '$*>=4'.
  * --closed: flood fill from the player through every non-wall cell
    (puzzle: anything but '#'; platformer: any non-solid cell). Reaching the grid
    edge or a missing cell of a short row is a leak, reported with (col,row).
    Without a player start, every border cell must be solid.
  * --width/--height: exact dimensions.

--emit-ruled prints the grid with a column ruler and row indices (the format in
references/grid-conventions.md); the lint summary then goes to stderr.

Custom legend JSON (--legend PATH.json):
  {"name": "mine", "glyphs": {"#": "wall", "-": "floor", "@": "player"},
   "player": "@", "solid": "#"}
  "player" and "solid" are strings of glyphs; include " " in "glyphs" to allow
  spaces. Digit glyphs in a custom legend disable ruler/row-index stripping.

Exit codes: 0 all checks passed, 1 a check failed, 2 usage or read error.
Standard library only; Python 3.8+.
"""
import argparse
import json
import re
import sys
from collections import Counter

NOT_MODELLED = ("Not modelled: playability, solvability or reachability (use grid_puzzle_solve.py / "
                "platformer_reach.py), glyph semantics beyond counts, objects stacked on special tiles "
                "(no combined glyphs), anything written outside the grid except key-object lines.")

PUZZLE_GLYPHS = {
    "#": "wall", "-": "floor", "_": "floor", " ": "floor", "@": "player", "+": "player on goal",
    "$": "box", "*": "box on goal", ".": "goal", "~": "ice", "O": "pit", "!": "switch",
    "|": "gate", "X": "exit",
}
for _k in "abcde":
    PUZZLE_GLYPHS[_k] = "key " + _k
    PUZZLE_GLYPHS[_k.upper()] = "door " + _k.upper()

PLATFORMER_GLYPHS = {
    "-": "empty", ".": "empty", " ": "empty", "=": "one-way platform", "^": "hazard", "E": "enemy",
    "o": "coin", "*": "key collectible", "H": "ladder", "@": "player start", "M": "player start",
    "F": "goal", "G": "goal", "C": "checkpoint", "W": "water",
}
for _k in "X#S?Q<>[]Bb":
    PLATFORMER_GLYPHS[_k] = "solid"

LEGENDS = {
    "puzzle": {"name": "puzzle", "glyphs": PUZZLE_GLYPHS, "player": "@+", "solid": "#"},
    "platformer": {"name": "platformer", "glyphs": PLATFORMER_GLYPHS, "player": "@M",
                   "solid": "X#S?Q<>[]Bb"},
}

# key-object names -> glyphs, per legend
PUZZLE_OBJECTS = [
    (r"players?|start|avatar", "@+"), (r"box(es)?|crates?|blocks?", "$*"),
    (r"goals?|targets?", ".+*"), (r"ice", "~"), (r"pits?|holes?", "O"),
    (r"switch(es)?|plates?|buttons?", "!"), (r"gates?", "|"), (r"exits?", "X"),
]
PLATFORMER_OBJECTS = [
    (r"players?|start", "@M"), (r"goals?|flags?|exits?", "FG"), (r"checkpoints?", "C"),
    (r"coins?", "o"), (r"keys?|collectibles?", "*"), (r"enem(y|ies)", "E"),
    (r"hazards?|spikes?|lava", "^"), (r"ladders?", "H"),
]

COORD_RE = re.compile(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
RULER_RE = re.compile(r"^\s*\d[\d ]*$")
ROWIDX_RE = re.compile(r"^(\s*)(\d+)([|:]?)(.*)$")


class GridError(Exception):
    """Raised when the input cannot be read as a grid at all (exit 2)."""


def read_text(path):
    if path == "-":
        return sys.stdin.read()
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        raise GridError("cannot read %s: %s" % (path, exc))
    except UnicodeDecodeError as exc:
        raise GridError("%s is not UTF-8 text: %s" % (path, exc))


def load_legend(spec):
    """Return a legend dict for 'puzzle', 'platformer' or a JSON file path."""
    if spec in LEGENDS:
        return LEGENDS[spec]
    try:
        with open(spec, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise GridError("cannot load legend %s: %s" % (spec, exc))
    if not isinstance(data, dict) or not isinstance(data.get("glyphs"), dict):
        raise GridError("legend JSON needs a \"glyphs\" object mapping glyph -> meaning")
    for g in data["glyphs"]:
        if len(g) != 1:
            raise GridError("legend glyph %r is not a single character" % g)
    return {"name": data.get("name", spec), "glyphs": data["glyphs"],
            "player": data.get("player", ""), "solid": data.get("solid", "")}


def _glyph_ratio(line, glyphs):
    s = line.rstrip()
    if not s:
        return 1.0
    return sum(1 for ch in s if ch in glyphs) / float(len(s))


def extract_grid(text, glyphs=None):
    """Extract grid rows from text.

    Returns (rows, meta). rows are strings (not padded). meta holds notes,
    'objects' (key-object entries) and flags describing what was stripped.
    Raises GridError if no grid rows remain.
    """
    glyphs = glyphs if glyphs is not None else PUZZLE_GLYPHS
    digits_are_glyphs = any(ch.isdigit() for ch in glyphs)
    meta = {"fenced": False, "ruler_lines": 0, "row_prefix": False, "notes": [],
            "object_lines": [], "ruler_offset": None}
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    # key-object lines anywhere in the file
    obj_lines = [ln for ln in lines if COORD_RE.search(ln)]
    meta["object_lines"] = obj_lines
    # fenced block
    fence_idx = [i for i, ln in enumerate(lines) if FENCE_RE.match(ln)]
    if fence_idx:
        meta["fenced"] = True
        start = fence_idx[0] + 1
        end = fence_idx[1] if len(fence_idx) > 1 else len(lines)
        if len(fence_idx) > 2:
            meta["notes"].append("file has more than one fenced block; only the first was read")
        lines = lines[start:end]
    lines = [ln for ln in lines if not COORD_RE.search(ln)]
    # unfenced prose: drop leading/trailing lines that are mostly non-glyphs
    if not meta["fenced"]:
        def gridlike(ln):
            if not ln.strip() or (not digits_are_glyphs and RULER_RE.match(ln)):
                return True
            body = ln
            if not digits_are_glyphs:
                m = ROWIDX_RE.match(ln)
                if m and m.group(2):
                    body = m.group(4)
            return _glyph_ratio(body, glyphs) >= 0.7
        dropped = 0
        for end in (0, -1):
            while lines and (not lines[end].strip() or not gridlike(lines[end])):
                if lines.pop(end).strip():
                    dropped += 1
        if dropped:
            meta["notes"].append("skipped %d non-grid line(s) around the grid" % dropped)
    # trim blank lines at both ends
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    # ruler lines (top and bottom)
    ruler = []
    if not digits_are_glyphs:
        while lines and RULER_RE.match(lines[0]):
            ruler.append(lines.pop(0))
        while lines and RULER_RE.match(lines[-1]):
            lines.pop()
            meta["ruler_lines"] += 1
        meta["ruler_lines"] += len(ruler)
        while lines and not lines[0].strip():
            lines.pop(0)
    if ruler:
        units = ruler[-1]
        meta["ruler_offset"] = len(units) - len(units.lstrip())
        first = units.strip()[:1]
        if first == "1":
            meta["notes"].append("column ruler starts at 1; coordinates here are 0-based")
    # row-index prefixes
    if not digits_are_glyphs and lines:
        nonblank = [ln for ln in lines if ln.strip()]
        matches = [ROWIDX_RE.match(ln) for ln in nonblank]
        if nonblank and all(m and m.group(2) for m in matches):
            meta["row_prefix"] = True
            seps = [m.group(3) for m in matches]
            all_sep = all(seps)
            all_space = (not all_sep) and all(m.group(4).startswith(" ") for m in matches)
            new_lines, idxs = [], []
            for ln in lines:
                m = ROWIDX_RE.match(ln)
                if not m or not m.group(2):
                    new_lines.append("")
                    continue
                idxs.append(int(m.group(2)))
                if m.group(3):
                    new_lines.append(m.group(4))
                elif meta["ruler_offset"] is not None and len(m.group(1)) + len(m.group(2)) <= meta["ruler_offset"]:
                    new_lines.append(ln[meta["ruler_offset"]:])
                elif all_space:
                    new_lines.append(m.group(4)[1:])
                else:
                    new_lines.append(m.group(4))
            lines = new_lines
            expect0 = idxs[0] if idxs else 0
            if idxs != list(range(expect0, expect0 + len(idxs))):
                meta["notes"].append("row indices are not consecutive: %s" % idxs)
            elif expect0 not in (0,):
                meta["notes"].append("row indices start at %d; coordinates here use row 0 = first row" % expect0)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        raise GridError("no grid rows found")
    if any("\t" in ln for ln in lines):
        meta["notes"].append("tab characters found; tabs are not grid cells (use one character per cell)")
    return lines, meta


def normalise_rows(rows, width=None):
    """Pad rows with spaces to a rectangle (used by the solver/metrics)."""
    w = width or max(len(r) for r in rows)
    return [r.ljust(w) for r in rows]


def parse_objects(object_lines, legend_name):
    """Parse key-object lines into [(name, glyphs, [(c,r), ...])]. Unparsed lines are returned too."""
    table = PUZZLE_OBJECTS if legend_name == "puzzle" else PLATFORMER_OBJECTS
    out, unparsed = [], []
    seg_re = re.compile(r"^\s*(?:[-*]\s*)?(?:key[- ]objects?\s*:\s*)?([A-Za-z][A-Za-z ]*?)\s*"
                        r"((?:\(\s*\d+\s*,\s*\d+\s*\)[\s,]*(?:and\s*)?)+)")
    for line in object_lines:
        got = False
        for seg in line.replace("`", "").split(";"):
            m = seg_re.match(seg)
            if not m:
                continue
            name = m.group(1).strip().lower()
            coords = [(int(c), int(r)) for c, r in COORD_RE.findall(m.group(2))]
            gl = None
            if legend_name == "puzzle":
                km = re.match(r"^(keys?|doors?)(?:\s+([a-eA-E]))?$", name, re.I)
                if km:
                    is_door = km.group(1).lower().startswith("door")
                    letter = m.group(1).strip().split()[-1] if km.group(2) else None
                    if letter:
                        gl = letter.upper() if is_door else letter.lower()
                    else:
                        gl = "ABCDE" if is_door else "abcde"
            if gl is None:
                for pat, g in table:
                    if re.match(r"^(%s)$" % pat, name):
                        gl = g
                        break
            if gl is None:
                continue
            out.append((m.group(1).strip(), gl, coords))
            got = True
        if not got:
            unparsed.append(line.strip())
    return out, unparsed


def emit_ruled(rows):
    """Return the grid with a column ruler and zero-padded row indices."""
    width = max(len(r) for r in rows) if rows else 0
    pw = max(2, len(str(len(rows) - 1)))
    pad = " " * (pw + 1)
    out = []
    if width > 10:
        mags = len(str(width - 1))
        for mag in range(mags - 1, 0, -1):
            div = 10 ** mag
            line = "".join(str((c // div) % 10) if c % div == 0 else " " for c in range(width))
            out.append((pad + line).rstrip())
    out.append(pad + "".join(str(c % 10) for c in range(width)))
    for i, r in enumerate(rows):
        out.append(str(i).zfill(pw) + "|" + r)
    return "\n".join(out)


def _flood_leak(grid, width, height, start, passable):
    """Flood from start through passable cells; return first leak cell or None."""
    seen = {start}
    stack = [start]
    while stack:
        c, r = stack.pop()
        for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nc, nr = c + dc, r + dr
            if nc < 0 or nr < 0 or nr >= height or nc >= width or nc >= len(grid[nr]):
                return (c, r)
            if (nc, nr) in seen or not passable(grid[nr][nc]):
                continue
            seen.add((nc, nr))
            stack.append((nc, nr))
    return None


def lint(rows, meta, legend, width=None, height=None, expects=(), closed=False):
    glyphs = legend["glyphs"]
    name = legend["name"]
    checks, warnings, notes = [], [], list(meta.get("notes", []))

    def check(cname, ok, detail):
        checks.append({"name": cname, "ok": bool(ok), "detail": detail})

    # trailing-space tolerance
    lengths = [len(r) for r in rows]
    if width:
        expected = width
    else:
        cnt = Counter(lengths)
        top = max(cnt.values())
        expected = max(l for l, n in cnt.items() if n == top)
    rows = list(rows)
    trimmed = 0
    for i, r in enumerate(rows):
        if len(r) > expected and r[expected:].strip() == "":
            rows[i] = r[:expected]
            trimmed += 1
    if trimmed:
        notes.append("trimmed trailing spaces beyond column %d on %d row(s)" % (expected - 1, trimmed))
    ragged = [{"row": i, "length": len(r), "expected": expected} for i, r in enumerate(rows) if len(r) != expected]
    grid_w = max(len(r) for r in rows)
    grid_h = len(rows)
    check("rectangular", not ragged,
          "all rows %d wide" % expected if not ragged else
          "; ".join("row %d has %d chars, expected %d" % (x["row"], x["length"], x["expected"]) for x in ragged[:12])
          + (" ..." if len(ragged) > 12 else ""))
    if width is not None or height is not None:
        okw = width is None or grid_w == width
        okh = height is None or grid_h == height
        check("dimensions", okw and okh, "grid is %dx%d (cols x rows), expected %sx%s"
              % (grid_w, grid_h, width if width else "*", height if height else "*"))
    unknown = []
    counts = Counter()
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in glyphs:
                counts[ch] += 1
            else:
                unknown.append({"glyph": ch, "col": c, "row": r})
    check("known_glyphs", not unknown,
          "all glyphs in the %s legend" % name if not unknown else
          ", ".join("%r at (%d,%d)" % (u["glyph"], u["col"], u["row"]) for u in unknown[:20])
          + (" ... (%d total)" % len(unknown) if len(unknown) > 20 else ""))
    players = sum(counts[g] for g in legend.get("player", ""))
    if legend.get("player"):
        pos = [(c, r) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch in legend["player"]]
        check("one_player_start", players == 1,
              "found %d player start(s) (%s)%s" % (players, legend["player"],
                                                    (" at " + " ".join("(%d,%d)" % p for p in pos[:8])) if pos else ""))
    if name == "puzzle":
        boxes = counts["$"] + counts["*"]
        goals = counts["."] + counts["+"] + counts["*"]
        pits = counts["O"]
        if goals == 0:
            check("win_condition", counts["X"] > 0,
                  "no goals; %d exit(s) X" % counts["X"] if counts["X"] else "no goals and no X exit: nothing to win")
        else:
            if pits:
                ok = boxes >= goals
                det = "%d boxes, %d goals, %d pits (pits may consume extra boxes)" % (boxes, goals, pits)
            else:
                ok = boxes == goals
                det = "%d boxes, %d goals" % (boxes, goals)
            check("box_goal_balance", ok, det)
            if counts["X"]:
                warnings.append("X exit present but the level has goals: the win condition is goals only; X is plain floor")
        for k in "abcde":
            if counts[k.upper()] > counts[k]:
                warnings.append("%d door(s) %s but only %d key(s) %s" % (counts[k.upper()], k.upper(), counts[k], k))
        if counts["|"] and not counts["!"]:
            warnings.append("gates (|) but no switches (!): a gate with no switch is always open")
        if counts["!"] and not counts["|"]:
            warnings.append("switches (!) but no gates (|): switches do nothing")
        if counts[" "]:
            notes.append("grid uses spaces as floor; prefer '-' in anything a human will copy")
    if name == "platformer":
        if not (counts["F"] + counts["G"]):
            warnings.append("no goal (F or G)")
    # expects
    for spec in expects:
        gl, op, n = spec
        got = sum(counts[g] for g in gl)
        ok = {"=": got == n, ">=": got >= n, "<=": got <= n}[op]
        check("expect %s%s%d" % (gl, op, n), ok, "count of %r is %d" % (gl, got))
    # closed
    if closed:
        solid = set(legend.get("solid", "")) or {"#"}
        passable = (lambda ch: ch != "#") if name == "puzzle" else (lambda ch: ch not in solid)
        ppos = [(c, r) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch in legend.get("player", "")]
        if ppos:
            leak = _flood_leak(rows, grid_w, grid_h, ppos[0], passable)
            check("closed", leak is None,
                  "player region is sealed" if leak is None else
                  "player region leaks at (%d,%d) to the grid edge or a missing cell" % leak)
        else:
            border = [(c, r) for r in range(grid_h) for c in range(len(rows[r]))
                      if (r in (0, grid_h - 1) or c in (0, len(rows[r]) - 1)) and passable(rows[r][c])]
            check("closed", not border, "border is solid" if not border else
                  "open border cells: " + " ".join("(%d,%d)" % b for b in border[:12]))
    # key objects
    if meta.get("object_lines") and name in ("puzzle", "platformer"):
        objs, unparsed = parse_objects(meta["object_lines"], name)
        for oname, gl, coords in objs:
            actual = sorted((c, r) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch in gl)
            listed = sorted(set(coords))
            missing = [p for p in listed if p not in actual]
            extra = [p for p in actual if p not in listed]
            ok = not missing and not extra
            det = "%s listed %s" % (oname, " ".join("(%d,%d)" % p for p in listed))
            if missing:
                det += "; not in grid at " + " ".join("(%d,%d)" % p for p in missing)
            if extra:
                det += "; grid also has %s at %s" % (gl, " ".join("(%d,%d)" % p for p in extra))
            check("objects %s" % oname, ok, det)
        for u in unparsed:
            notes.append("line with coordinates not read as a key-object list: %r" % u[:80])
    ok = all(c["ok"] for c in checks)
    return {
        "ok": ok, "legend": name, "width": grid_w, "height": grid_h,
        "ragged_rows": ragged, "unknown_glyphs": unknown,
        "counts": {k: counts[k] for k in sorted(counts)},
        "checks": checks, "warnings": warnings, "notes": notes,
        "stripped": {"fenced": meta.get("fenced", False), "ruler_lines": meta.get("ruler_lines", 0),
                     "row_prefix": meta.get("row_prefix", False)},
        "rows": rows,
        "not_modelled": NOT_MODELLED,
    }


EXPECT_RE = re.compile(r"^(.+?)(>=|<=|=)(\d+)$", re.S)


def parse_expect(s):
    m = EXPECT_RE.match(s)
    if not m:
        raise GridError("bad --expect %r (use GLYPHS=N, GLYPHS>=N or GLYPHS<=N)" % s)
    return (m.group(1), m.group(2), int(m.group(3)))


def format_report(rep):
    out = ["grid_lint: %s legend, %dx%d (cols x rows) - %s"
           % (rep["legend"], rep["width"], rep["height"], "PASS" if rep["ok"] else "FAIL")]
    for c in rep["checks"]:
        out.append("  [%s] %s: %s" % ("ok" if c["ok"] else "FAIL", c["name"], c["detail"]))
    cs = " ".join("%s=%d" % ("' '" if k == " " else k, v) for k, v in rep["counts"].items())
    out.append("  counts: " + cs)
    for w in rep["warnings"]:
        out.append("  warning: " + w)
    for n in rep["notes"]:
        out.append("  note: " + n)
    out.append(rep["not_modelled"])
    return "\n".join(out)


def build_parser():
    p = argparse.ArgumentParser(
        prog="grid_lint.py",
        description=__doc__.split("\n\n", 1)[1],
        epilog="Examples:\n  python3 -I scripts/grid_lint.py level.txt --legend puzzle --expect @=1 --expect '$=4' --closed\n"
               "  python3 -I scripts/grid_lint.py level.txt --emit-ruled",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", help="grid file (UTF-8 text or markdown with a fenced block); '-' for stdin")
    p.add_argument("--legend", default="puzzle", help="puzzle (default), platformer, or a legend JSON path")
    p.add_argument("--width", type=int, help="required number of columns")
    p.add_argument("--height", type=int, help="required number of rows")
    p.add_argument("--expect", action="append", default=[], metavar="GLYPHS=N",
                   help="required count of glyph(s), summed; also >= and <=; repeatable")
    p.add_argument("--closed", action="store_true", help="fail if the player's region can reach the grid edge")
    p.add_argument("--emit-ruled", action="store_true", help="print the grid with column ruler and row indices")
    p.add_argument("--json", action="store_true", help="machine-readable JSON output")
    return p


def main(argv=None):
    p = build_parser()
    try:
        args = p.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    try:
        legend = load_legend(args.legend)
        expects = [parse_expect(e) for e in args.expect]
        text = read_text(args.file)
        rows, meta = extract_grid(text, legend["glyphs"])
    except GridError as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc), "not_modelled": NOT_MODELLED}))
        else:
            print("grid_lint: error: %s" % exc)
            print(NOT_MODELLED)
        return 2
    rep = lint(rows, meta, legend, args.width, args.height, expects, args.closed)
    if args.emit_ruled:
        rep["ruled"] = emit_ruled(rep["rows"])
    if args.json:
        print(json.dumps(rep, indent=2))
    elif args.emit_ruled:
        print(rep["ruled"])
        sys.stdout.flush()
        print(format_report(rep), file=sys.stderr)
    else:
        print(format_report(rep))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
