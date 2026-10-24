#!/usr/bin/env python3
"""level_metrics.py - structural metrics for ASCII level grids, and a near-duplicate check.

Usage:
  python3 -I scripts/level_metrics.py FILE [--legend puzzle|platformer]
         [--compare FILE2 ...] [--json]

FILE is a grid in the puzzle (default) or platformer legend (see
references/grid-conventions.md); "-" reads stdin; markdown with a fenced block,
column rulers and "07|" row prefixes are accepted (same reader as grid_lint.py).

Grid metrics (both legends). "Blocking" = '#' for puzzle; the solid glyphs
X # S ? Q < > [ ] B b for platformer. Every other cell is "open".
  size                cols x rows
  wall_density        blocking cells / all cells
  open_floor_ratio    open interior cells / all cells
  regions             4-connected components of open interior cells
  corridor_ratio      open cells with exactly 2 open orthogonal neighbours / open cells
  dead_end_cells      open cells with exactly 1 open neighbour (isolated cells listed separately)
  Puzzle legend only: open components that touch the grid edge and hold no player
  or object are "exterior" (the blank margin of a ragged Sokoban map) and are left
  out of the interior counts.

Platformer extras:
  per-column leniency proxy: gap (bottom cell not solid), hazards (^), enemies (E);
    harshness = gap + hazards + enemies per column; worst 10-column window [convention]
  gap runs: widths of consecutive gap columns (max gap width)
  ground height per column: contiguous solid cells up from the bottom row
  linearity: population std-dev of ground height over non-gap columns (0 = flat)

--compare FILE2 ...: every pair among all files gets
  hamming: differing cells after normalising glyph aliases and padding to the larger
    size (puzzle: padded with '#', aligned top-left, minimum over the 8 rotations /
    mirrors and shifts of up to 2 cells; platformer: padded with '-', aligned
    bottom-left, shifts of up to 2 cells, no mirroring); hamming_norm = hamming / cells.
  structural: Euclidean distance between normalised metric vectors.
  near_duplicate: hamming_norm <= 0.10 [convention]; structurally_similar:
    structural <= 0.05 [convention] (reported, not a failure).

Exit codes: 0 ok (no near-duplicates), 1 a compared pair is a near-duplicate,
2 usage or read error. Unknown glyphs are counted as open cells with a warning
(run grid_lint.py first). Standard library only; Python 3.8+.
"""
import argparse
import json
import math
import os
import sys
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grid_lint  # noqa: E402

NOT_MODELLED = ("Not modelled: playability, solvability, difficulty, jump physics, sightlines, verticality "
                "beyond ground height, art or theme; metrics describe layout shape only.")

NEAR_DUP = 0.10
STRUCT_SIM = 0.05
PUZZLE_OBJECTS = set("@+$*.~abcdeABCDEO!|X")
PLAT_SOLID = set("X#S?Q<>[]Bb")


def norm_glyph(ch, legend):
    if legend == "puzzle":
        if ch in "-_ ":
            return "-"
        if ch == "+":
            return "@"
        return ch
    if ch in PLAT_SOLID:
        return "X"
    if ch in "-. ":
        return "-"
    if ch == "M":
        return "@"
    if ch == "G":
        return "F"
    return ch


def load(path, legend):
    text = grid_lint.read_text(path)
    glyphs = grid_lint.LEGENDS[legend]["glyphs"]
    rows, _meta = grid_lint.extract_grid(text, glyphs)
    w = max(len(r) for r in rows)
    pad = " " if legend == "puzzle" else "-"
    return [r.ljust(w, pad) for r in rows]


def grid_metrics(rows, legend):
    h, w = len(rows), len(rows[0])
    glyphs = grid_lint.LEGENDS[legend]["glyphs"]
    unknown = sorted({ch for r in rows for ch in r if ch not in glyphs})
    blocking = (lambda ch: ch == "#") if legend == "puzzle" else (lambda ch: ch in PLAT_SOLID)
    open_ = [[not blocking(ch) for ch in r] for r in rows]
    comp = [[-1] * w for _ in range(h)]
    comps = []
    for r in range(h):
        for c in range(w):
            if open_[r][c] and comp[r][c] < 0:
                idx = len(comps)
                cells = []
                q = deque([(c, r)])
                comp[r][c] = idx
                while q:
                    x, y = q.popleft()
                    cells.append((x, y))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and open_[ny][nx] and comp[ny][nx] < 0:
                            comp[ny][nx] = idx
                            q.append((nx, ny))
                comps.append(cells)
    exterior = set()
    if legend == "puzzle":
        for i, cells in enumerate(comps):
            edge = any(x in (0, w - 1) or y in (0, h - 1) for x, y in cells)
            objs = any(rows[y][x] in PUZZLE_OBJECTS for x, y in cells)
            if edge and not objs:
                exterior.add(i)
    interior = [i for i in range(len(comps)) if i not in exterior]
    open_cells = [(x, y) for i in interior for x, y in comps[i]]
    inset = set(open_cells)
    corridor = dead_end = isolated = 0
    dead_list = []
    for x, y in open_cells:
        n = sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (x + dx, y + dy) in inset)
        if n == 2:
            corridor += 1
        elif n == 1:
            dead_end += 1
            if len(dead_list) < 20:
                dead_list.append([x, y])
        elif n == 0:
            isolated += 1
    cells = float(w * h)
    walls = sum(1 for r in rows for ch in r if blocking(ch))
    m = {
        "size": [w, h],
        "wall_density": round(walls / cells, 3),
        "open_floor_ratio": round(len(open_cells) / cells, 3),
        "regions": len(interior),
        "exterior_cells": sum(len(comps[i]) for i in exterior),
        "corridor_ratio": round(corridor / float(len(open_cells)), 3) if open_cells else 0.0,
        "dead_end_cells": dead_end,
        "dead_end_examples": dead_list,
        "isolated_cells": isolated,
    }
    if legend == "puzzle":
        m["boxes"] = sum(r.count("$") + r.count("*") for r in rows)
        m["goals"] = sum(r.count(".") + r.count("+") + r.count("*") for r in rows)
    else:
        m.update(platformer_metrics(rows))
    warnings = []
    if unknown:
        warnings.append("unknown glyph(s) %s counted as open; run grid_lint.py" % " ".join(repr(u) for u in unknown))
    if len(interior) > 1:
        sizes = sorted((len(comps[i]) for i in interior), reverse=True)
        warnings.append("%d separate open regions (sizes %s)" % (len(interior), sizes[:8]))
    return m, warnings


def platformer_metrics(rows):
    h, w = len(rows), len(rows[0])
    gaps, hazards, enemies, ground = [], [], [], []
    for c in range(w):
        col = [rows[r][c] for r in range(h)]
        gap = 0 if col[-1] in PLAT_SOLID else 1
        gaps.append(gap)
        hazards.append(sum(1 for ch in col if ch == "^"))
        enemies.append(sum(1 for ch in col if ch == "E"))
        gh = 0
        for r in range(h - 1, -1, -1):
            if col[r] in PLAT_SOLID:
                gh += 1
            else:
                break
        ground.append(gh)
    harsh = [g + hz + e for g, hz, e in zip(gaps, hazards, enemies)]
    win = min(10, w)
    worst = max(sum(harsh[i:i + win]) for i in range(0, w - win + 1)) if w else 0
    worst_at = max(range(0, w - win + 1), key=lambda i: sum(harsh[i:i + win])) if w else 0
    runs, cur = [], 0
    for g in gaps:
        if g:
            cur += 1
        elif cur:
            runs.append(cur)
            cur = 0
    if cur:
        runs.append(cur)
    solid_cols = [gh for gh, g in zip(ground, gaps) if not g]
    if solid_cols:
        mean = sum(solid_cols) / float(len(solid_cols))
        lin = math.sqrt(sum((x - mean) ** 2 for x in solid_cols) / len(solid_cols))
    else:
        lin = 0.0
    return {
        "gap_columns": sum(gaps), "gap_runs": runs, "max_gap_width": max(runs) if runs else 0,
        "hazards": sum(hazards), "enemies": sum(enemies),
        "harshness_per_column": harsh,
        "mean_harshness": round(sum(harsh) / float(w), 3) if w else 0.0,
        "worst_window": {"start_col": worst_at, "width": win, "harshness": worst},
        "ground_height": ground,
        "linearity_stddev": round(lin, 3),
    }


def feature_vector(m, legend):
    v = [m["wall_density"], m["open_floor_ratio"], m["corridor_ratio"],
         (m["dead_end_cells"] / float(max(1, m["open_floor_ratio"] * m["size"][0] * m["size"][1]))),
         min(m["regions"], 5) / 5.0]
    if legend == "platformer":
        w, h = m["size"]
        v += [m["gap_columns"] / float(w), m["hazards"] / float(w), m["enemies"] / float(w),
              m["linearity_stddev"] / float(max(1, h))]
    return v


def _transforms(rows, legend):
    out = [("identity", rows)]
    if legend != "puzzle":
        return out
    def rot(g):
        return ["".join(g[len(g) - 1 - r][c] for r in range(len(g))) for c in range(len(g[0]))]
    def mir(g):
        return [r[::-1] for r in g]
    g = rows
    names = ["identity", "rot90", "rot180", "rot270"]
    out = []
    for i in range(4):
        out.append((names[i], g))
        out.append((names[i] + "+mirror", mir(g)))
        g = rot(g)
    return out


def hamming(a, b, legend):
    """Minimum differing cells over allowed transforms/shifts. Returns (count, cells, how)."""
    pad = "#" if legend == "puzzle" else "-"
    na = [[norm_glyph(ch, legend) for ch in r] for r in a]
    best = None
    for name, tb in _transforms(b, legend):
        nb = [[norm_glyph(ch, legend) for ch in r] for r in tb]
        H = max(len(na), len(nb)) + 2
        W = max(len(na[0]), len(nb[0])) + 2
        cells = max(len(na), len(nb)) * max(len(na[0]), len(nb[0]))
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                diff = 0
                for y in range(H):
                    for x in range(W):
                        ya, yb = y, y - dy
                        if legend == "platformer":   # bottom-align
                            ya = len(na) - H + y
                            yb = len(nb) - H + y - dy
                        ca = na[ya][x] if 0 <= ya < len(na) and x < len(na[0]) else pad
                        xb = x - dx
                        cb = nb[yb][xb] if 0 <= yb < len(nb) and 0 <= xb < len(nb[0]) else pad
                        if ca != cb:
                            diff += 1
                if best is None or diff < best[0]:
                    best = (diff, cells, "%s shift(%d,%d)" % (name, dx, dy))
    return best


def compare(items, legend):
    pairs = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            (fa, ra, ma), (fb, rb, mb) = items[i], items[j]
            diff, cells, how = hamming(ra, rb, legend)
            va, vb = feature_vector(ma, legend), feature_vector(mb, legend)
            struct = math.sqrt(sum((x - y) ** 2 for x, y in zip(va, vb)))
            hn = diff / float(cells) if cells else 0.0
            pairs.append({"a": fa, "b": fb, "hamming": diff, "hamming_norm": round(hn, 3),
                          "best_alignment": how, "structural": round(struct, 3),
                          "near_duplicate": hn <= NEAR_DUP, "structurally_similar": struct <= STRUCT_SIM})
    return pairs


def format_metrics(name, m, legend, warnings):
    out = ["%s (%s legend): %dx%d" % (name, legend, m["size"][0], m["size"][1]),
           "  wall density %.3f, open floor ratio %.3f, regions %d, corridor ratio %.3f, dead-end cells %d%s"
           % (m["wall_density"], m["open_floor_ratio"], m["regions"], m["corridor_ratio"], m["dead_end_cells"],
              (" e.g. " + " ".join("(%d,%d)" % tuple(p) for p in m["dead_end_examples"][:6])) if m["dead_end_cells"] else "")]
    if m.get("exterior_cells"):
        out.append("  exterior (outside the walls) cells ignored: %d" % m["exterior_cells"])
    if legend == "puzzle":
        out.append("  boxes %d, goals %d" % (m["boxes"], m["goals"]))
    else:
        ww = m["worst_window"]
        out.append("  gaps: %d columns, max width %d; hazards %d; enemies %d; mean harshness %.3f; "
                   "worst %d-col window from col %d: %d"
                   % (m["gap_columns"], m["max_gap_width"], m["hazards"], m["enemies"], m["mean_harshness"],
                      ww["width"], ww["start_col"], ww["harshness"]))
        out.append("  linearity (std-dev of ground height): %.3f" % m["linearity_stddev"])
    for w in warnings:
        out.append("  warning: " + w)
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="level_metrics.py",
        description=__doc__.split("\n\n", 1)[1],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", help="grid file; '-' for stdin")
    p.add_argument("--legend", choices=["puzzle", "platformer"], default="puzzle")
    p.add_argument("--compare", nargs="+", default=[], metavar="FILE2",
                   help="other grids to compare pairwise (with FILE and each other)")
    p.add_argument("--json", action="store_true", help="JSON output")
    try:
        args = p.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    items = []
    try:
        for f in [args.file] + args.compare:
            rows = load(f, args.legend)
            m, warns = grid_metrics(rows, args.legend)
            items.append((f, rows, m, warns))
    except grid_lint.GridError as exc:
        if args.json:
            print(json.dumps({"error": str(exc), "not_modelled": NOT_MODELLED}))
        else:
            print("level_metrics: error: %s" % exc)
            print(NOT_MODELLED)
        return 2
    pairs = compare([(f, r, m) for f, r, m, _w in items], args.legend) if args.compare else []
    dup = any(pp["near_duplicate"] for pp in pairs)
    if args.json:
        print(json.dumps({"legend": args.legend,
                          "levels": [{"file": f, "metrics": m, "warnings": w} for f, _r, m, w in items],
                          "pairs": pairs, "near_duplicates": dup, "not_modelled": NOT_MODELLED}, indent=2))
    else:
        for f, _r, m, w in items:
            print(format_metrics(f, m, args.legend, w))
        if pairs:
            print("pairwise comparison (hamming_norm <= %.2f = near-duplicate [convention]):" % NEAR_DUP)
            for pp in pairs:
                flag = " NEAR-DUPLICATE" if pp["near_duplicate"] else (
                    " structurally similar" if pp["structurally_similar"] else "")
                print("  %s vs %s: hamming %d (%.3f, %s), structural %.3f%s"
                      % (pp["a"], pp["b"], pp["hamming"], pp["hamming_norm"], pp["best_alignment"],
                         pp["structural"], flag))
        print(NOT_MODELLED)
    return 1 if dup else 0


if __name__ == "__main__":
    sys.exit(main())
