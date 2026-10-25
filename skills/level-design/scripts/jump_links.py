#!/usr/bin/env python3
"""jump_links.py - check a jump-link table (2D or 3D traversal) against a movement kit.

Usage:
  python3 -I scripts/jump_links.py FILE [--kit KIT.json] [--critical-max 0.9]
          [--teaches MOVE[,MOVE]] [--max-replay-links 6] [--up z|y] [--json]

FILE is a UTF-8 markdown file ('-' = stdin) holding up to four tables, found by their
headers (case-insensitive, any column order; extra columns such as Note are ignored), or a
JSON file with the keys kit, moves, nodes, links. The format is assets/jump-sequence-spec.md.

  Kit    | Kit | Value |   rows: units, player_width, safe_fall, damage_fall, lethal_fall
         (safe_fall = highest drop with no cost; damage_fall = drop that hurts;
         lethal_fall = drop that kills; all optional)
  Moves  | Move | Distance | Height | Range | Rise |
         Distance + Height  ballistic jump: flat edge-to-edge distance D and apex H; reach at
                            rise h is D/2 * (1 + sqrt(1 - h/H)) (same parabola as
                            platformer_reach.py), so jumps up reach less and jumps down more
         Range              straight-line reach (grapple, swing, teleport): hypot(gap, rise)
         Rise [+ Distance]  climb / mantle / ledge grab: rise <= Rise, gap <= Distance (0 if
                            blank)
         Built in, no row needed: walk (connected on foot: path, stairs, beam; any length),
         drop (step off an edge, rise < 0, banded by the fall heights), ride (lift, mover,
         scripted: not modelled, always usable). walk/ride skip the coordinate check.
  Nodes  | Node | Role | Landing | X | Y | Z | Visible from |
         Role: start, goal, checkpoint, rest, reward, secret (comma-separated, several ok).
         Landing: "2x3" or "2" (size in units). X/Y/Z optional centre of the landing top;
         Z is up unless --up y. Visible from: nodes the landing can be seen from.
  Links  | From | To | Move | Gap | Rise | Camera | Fail | Dir |
         Gap: horizontal edge-to-edge distance. Rise: landing height minus take-off height
         (negative = down). Gap/Rise may be blank when both nodes have coordinates.
         Camera: across (screen plane), along (into/out of the screen, depth axis), diagonal.
         Fail: what a miss does: "respawn N", "fall N" (lands on node N), "death" (back to
         the nearest checkpoint), "restart", "none". Dir: "both" adds the reverse link.
         Move "teaser" = a visible link that must look impossible with every move;
         "teaser:MOVE" = reachable only with MOVE (an ability the player gets later).

Checks (thresholds are [convention] defaults):
  reachability   start reaches a goal; prescriptive fixes for links over 100% of the move
  critical-max   links every route needs stay <= --critical-max of the move (0.9; use 1.0
                 only for opt-in expert content)
  softlock       every node the player can reach (by links or by falling) can still reach a
                 goal; deliberate failing counts as a way out
  respawn        "respawn N" / "fall N" targets exist and lead back to the failed take-off
                 (a respawn past a one-way link is a bug); replay <= --max-replay-links links
  fail-stated    every link says what a miss does
  depth-axis     camera "along" links: landing >= 3 x player_width (2 x otherwise) and no
                 skill-band (> 75%) jump along the depth axis
  falls          drops banded free / committed / costly / lethal; lethal drops never required
  teasers        teaser links sit >= 130% of every move (150% clean); teaser:MOVE is
                 reachable with MOVE
  consistency    stated Gap/Rise agree with node coordinates
  visibility     (Visible from column) critical landings visible from take-off; secret nodes
                 have a reachable vantage
  teaches        (--teaches) the goal is unreachable without the listed moves, and their first
                 use is below 75% with a non-lethal miss (first encounters are safe)
Summary: bands per link, easiest route, longest rest-free chain of > 75% links, distinct
techniques, and a tier estimate on an 8-step scale (1 Very easy ... 8 Death) [convention].

Exit codes: 0 no failures (warnings allowed); 1 a check failed; 2 usage/parse error.
"""

import argparse
import heapq
import json
import math
import re
import sys
from collections import deque

NOT_MODELLED = ("Not modelled: camera occlusion and framing, timing of lifts, movers and "
                "enemies ('ride' links), momentum, air control and speed boosts beyond the "
                "parabola, readability of the surfaces, input precision and latency; numbers "
                "are only as good as the table.")

EMPTY = {"", "-", "–", "—", "none", "n/a", "na", "--"}
BANDS = ((0.40, "intro"), (0.75, "routine"), (0.90, "skill"), (1.00, "expert"))
TIERS = ("Very easy", "Easy", "Medium", "Advanced", "Hard", "Very hard", "Extreme", "Death")
EPS = 1e-9


class InputError(Exception):
    pass


# ---------- markdown tables ----------

def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s)]


def is_sep(cells):
    return any(cells) and all(re.fullmatch(r":?-+:?", c.replace(" ", "")) for c in cells if c)


def find_tables(text):
    blocks, cur = [], []
    for line in text.replace("\r", "").split("\n"):
        if "|" in line and line.strip():
            cur.append(line)
        else:
            if cur:
                blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    out = []
    for b in blocks:
        if len(b) >= 2 and is_sep(split_row(b[1])):
            out.append(([h.strip("*_` ").lower() for h in split_row(b[0])],
                        [split_row(r) for r in b[2:]]))
    return out


def col(head, *prefixes, exact=()):
    for i, h in enumerate(head):
        if h in exact or any(h.startswith(p) for p in prefixes):
            return i
    return None


def cell(row, i):
    if i is None or i >= len(row):
        return ""
    v = row[i].strip()
    return "" if v.lower() in EMPTY else v


def number(s, what):
    if s == "":
        return None
    m = re.match(r"^[~≈]?\s*([-+]?\d+(?:\.\d+)?)", s.replace("−", "-"))
    if not m:
        raise InputError("%s: '%s' is not a number" % (what, s))
    return float(m.group(1))


def size(s, what):
    if s == "":
        return None
    nums = re.findall(r"\d+(?:\.\d+)?", s)
    if not nums:
        raise InputError("%s: '%s' is not a size like 2x3" % (what, s))
    v = [float(x) for x in nums[:2]]
    return (min(v), max(v))


def parse_markdown(text, up):
    doc = {"kit": {}, "moves": {}, "nodes": [], "links": []}
    seen = set()
    for head, rows in find_tables(text):
        if col(head, "from", "take-off", "takeoff") is not None and col(head, exact=("to",)) is not None:
            kind = "links"
        elif col(head, "kit", "param", "setting") == 0:
            kind = "kit"
        elif col(head, exact=("move", "moves", "verb", "ability")) == 0:
            kind = "moves"
        elif col(head, "node", "id", "name") == 0:
            kind = "nodes"
        else:
            continue
        if kind in seen:
            continue
        seen.add(kind)
        rows = [r for r in rows if any(c.strip() for c in r)]
        if kind == "kit":
            vi = col(head, "value") if col(head, "value") is not None else 1
            for r in rows:
                k = cell(r, 0).lower().replace(" ", "_")
                if k:
                    doc["kit"][k] = cell(r, vi)
        elif kind == "moves":
            ci = {k: col(head, k) for k in ("distance", "height", "range", "rise")}
            for r in rows:
                name = cell(r, 0).lower()
                if name:
                    doc["moves"][name] = {k: number(cell(r, i), "move %s %s" % (name, k))
                                          for k, i in ci.items()}
        elif kind == "nodes":
            ci = {"role": col(head, "role", "type"), "landing": col(head, "landing", "size", "width"),
                  "x": col(head, exact=("x",)), "y": col(head, exact=("y",)), "z": col(head, exact=("z",)),
                  "visible": col(head, "visible", "seen")}
            for r in rows:
                nid = cell(r, 0)
                if not nid:
                    continue
                n = {"id": nid, "role": cell(r, ci["role"]), "landing": cell(r, ci["landing"]),
                     "visible_from": cell(r, ci["visible"]) if ci["visible"] is not None else None}
                for a in ("x", "y", "z"):
                    n[a] = cell(r, ci[a])
                doc["nodes"].append(n)
            doc["has_visible"] = ci["visible"] is not None
        else:
            ci = {"from": col(head, "from", "take-off", "takeoff"), "to": col(head, exact=("to",)),
                  "move": col(head, "move", "verb", "action"),
                  "gap": col(head, "gap", "dist", "horizontal"),
                  "rise": col(head, "rise", "Δh", "dh", "height", "up"),
                  "camera": col(head, "camera", "view", "axis"),
                  "fail": col(head, "fail", "on fail", "miss"),
                  "dir": col(head, "dir", "way", "direction")}
            for n, r in enumerate(rows, 1):
                doc["links"].append(dict({k: cell(r, i) for k, i in ci.items()}, row=n))
    return doc


def normalise(doc, up):
    """Turn markdown strings or JSON values into typed structures."""
    kit = {}
    for k, v in (doc.get("kit") or {}).items():
        k = k.lower()
        if k in ("units", "unit"):
            kit["units"] = str(v)
        elif k in ("player_width", "width", "player_radius_x2"):
            kit["player_width"] = number(str(v), "kit player_width") if v not in ("", None) else None
        elif k in ("safe_fall", "safe_fall_height", "damage_fall", "fall_damage_height",
                   "lethal_fall", "lethal_fall_height"):
            key = {"safe_fall_height": "safe_fall", "fall_damage_height": "damage_fall",
                   "lethal_fall_height": "lethal_fall"}.get(k, k)
            kit[key] = number(str(v), "kit " + k) if v not in ("", None) else None
    moves = {}
    for name, m in (doc.get("moves") or {}).items():
        mm = {k: (float(m[k]) if m.get(k) not in (None, "") else None)
              for k in ("distance", "height", "range", "rise")}
        if mm["distance"] is not None and mm["height"] is not None and mm["rise"] is None:
            if mm["distance"] <= 0 or mm["height"] <= 0:
                raise InputError("move %s: distance and height must be > 0" % name)
            mm["type"] = "jump"
        elif mm["range"] is not None:
            mm["type"] = "range"
        elif mm["rise"] is not None:
            mm["type"] = "climb"
        else:
            raise InputError("move %s needs Distance+Height, Range, or Rise" % name)
        moves[name.lower()] = mm
    nodes = {}
    hor = ("x", "y") if up == "z" else ("x", "z")
    for n in doc.get("nodes") or []:
        nid = str(n["id"]).strip()
        if nid in nodes:
            raise InputError("node %s is listed twice" % nid)
        roles = {r.strip().lower() for r in re.split(r"[,;/+ ]+", str(n.get("role") or "")) if r.strip()}
        land = n.get("landing")
        land = size(str(land), "node %s landing" % nid) if land not in (None, "") else None
        coords = [n.get(a) for a in ("x", "y", "z")]
        pos = None
        if all(c not in (None, "") for c in coords):
            p = {a: number(str(n[a]), "node %s %s" % (nid, a)) for a in ("x", "y", "z")}
            pos = (p[hor[0]], p[hor[1]], p[up])
        elif any(c not in (None, "") for c in coords):
            raise InputError("node %s: give all of X, Y, Z or none" % nid)
        vis = n.get("visible_from")
        if isinstance(vis, str):
            vis = [v.strip() for v in re.split(r"[,;]", vis) if v.strip() and v.strip().lower() not in EMPTY]
        nodes[nid] = {"id": nid, "roles": roles, "landing": land, "pos": pos, "visible_from": vis}
    links = []
    auto = not nodes
    for i, l in enumerate(doc.get("links") or [], 1):
        row = l.get("row", i)
        a, b = str(l.get("from") or "").strip(), str(l.get("to") or "").strip()
        if not a or not b:
            raise InputError("link row %d needs From and To" % row)
        for x in (a, b):
            if x not in nodes:
                if not auto:
                    raise InputError("link row %d: node '%s' is not in the node table" % (row, x))
                nodes[x] = {"id": x, "roles": set(), "landing": None, "pos": None, "visible_from": None}
        mv = str(l.get("move") or "").strip().lower() or "jump"
        gap = l.get("gap")
        rise = l.get("rise")
        gap = number(str(gap), "link %s->%s gap" % (a, b)) if gap not in (None, "") else None
        rise = number(str(rise), "link %s->%s rise" % (a, b)) if rise not in (None, "") else None
        cam = str(l.get("camera") or "").strip().lower()
        if re.match(r"(across|lateral|side|screen|horiz)", cam):
            cam = "across"
        elif re.match(r"(along|depth|into|away|toward|forward|back)", cam):
            cam = "along"
        elif re.match(r"diag|45|oblique", cam):
            cam = "diagonal"
        elif cam:
            cam = "unknown:" + cam
        fail = str(l.get("fail") or "").strip()
        two = str(l.get("dir") or "").strip().lower() in ("both", "2", "two-way", "two way", "<->", "↔")
        links.append({"row": row, "from": a, "to": b, "move": mv, "gap": gap, "rise": rise,
                      "camera": cam, "fail_text": fail, "two_way": two})
    if not links:
        raise InputError("no link table found (needs From and To columns)")
    return kit, moves, nodes, links


def load(path, kit_arg, up):
    text = sys.stdin.read() if path == "-" else None
    if text is None:
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            raise InputError("cannot read %s: %s" % (path, e))
    if text.lstrip().startswith("{"):
        try:
            doc = json.loads(text)
        except ValueError as e:
            raise InputError("bad JSON: %s" % e)
        doc.setdefault("kit", {})
        if "moves" not in doc and "moves" in doc["kit"]:
            doc["moves"] = doc["kit"].pop("moves")
        doc["has_visible"] = any("visible_from" in n for n in doc.get("nodes") or [])
    else:
        doc = parse_markdown(text, up)
    if kit_arg:
        try:
            if kit_arg.strip().startswith("{"):
                extra = json.loads(kit_arg)
            else:
                with open(kit_arg, encoding="utf-8") as f:
                    extra = json.load(f)
        except (OSError, ValueError) as e:
            raise InputError("cannot read kit %s: %s" % (kit_arg, e))
        doc["moves"] = dict(doc.get("moves") or {}, **(extra.pop("moves", None) or {}))
        doc["kit"] = dict(doc.get("kit") or {}, **extra)
    kit, moves, nodes, links = normalise(doc, up)
    return kit, moves, nodes, links, bool(doc.get("has_visible"))


# ---------- geometry ----------

def reach(m, rise):
    """Max horizontal gap for a ballistic move at this rise (0 if the rise is above apex)."""
    D, H = m["distance"], m["height"]
    if rise > H + EPS:
        return 0.0
    return D / 2.0 * (1.0 + math.sqrt(max(0.0, 1.0 - rise / H)))


def usage(m, gap, rise):
    """(fraction of the move used, the move's reach at this rise)."""
    if m["type"] == "jump":
        if rise > m["height"] + EPS:
            return rise / m["height"], 0.0
        r = reach(m, rise)
        return max(gap / r, max(0.0, rise) / m["height"]), r
    if m["type"] == "range":
        return math.hypot(gap, rise) / m["range"], m["range"]
    # climb
    pr = max(0.0, rise) / m["rise"] if m["rise"] > 0 else math.inf
    d = m["distance"] or 0.0
    pg = (gap / d if d > EPS else (0.0 if gap <= 0.05 * max(1.0, m["rise"]) else math.inf))
    return max(pr, pg), d


def band(p):
    for lim, name in BANDS:
        if p <= lim + EPS:
            return name
    return "over"


def fmt(x):
    if x is None:
        return "?"
    if x == math.inf:
        return "inf"
    return ("%.2f" % x).rstrip("0").rstrip(".")


def pct(p):
    return "inf" if p == math.inf else "%d%%" % round(p * 100)


# ---------- main analysis ----------

def analyse(kit, moves, nodes, links, has_visible, args):
    checks = []
    U = kit.get("units", "")
    pw = kit.get("player_width")

    def add(name, status, details):
        checks.append({"check": name, "status": status, "details": details})

    without = {m.strip().lower() for m in (args.teaches or "").split(",") if m.strip()}
    # expand two-way links
    full = []
    for l in links:
        full.append(dict(l, reverse=False))
        if l["two_way"]:
            r = dict(l, reverse=True)
            r["from"], r["to"] = l["to"], l["from"]
            if l["rise"] is not None:
                r["rise"] = -l["rise"]
            full.append(r)

    # consistency with coordinates, fill blanks
    cons = []
    for l in full:
        a, b = nodes[l["from"]], nodes[l["to"]]
        if a["pos"] and b["pos"] and l["move"] not in ("walk", "ride"):
            cd = math.hypot(b["pos"][0] - a["pos"][0], b["pos"][1] - a["pos"][1])
            la = a["landing"] or (0.0, 0.0)
            lb = b["landing"] or (0.0, 0.0)
            lo = max(0.0, cd - (la[1] + lb[1]) / 2.0)
            hi = max(0.0, cd - (la[0] + lb[0]) / 2.0)
            dz = b["pos"][2] - a["pos"][2]
            tol_base = 0.25 * (pw or 1.0)
            if l["gap"] is None:
                l["gap"], l["gap_from_coords"] = hi, True
            elif not (lo - max(tol_base, 0.15 * lo) <= l["gap"] <= hi + max(tol_base, 0.15 * hi)):
                rng = fmt(lo) if abs(hi - lo) < 0.005 else "%s-%s" % (fmt(lo), fmt(hi))
                cons.append("%s: stated gap %s%s but coordinates give %s%s; fix the table or the "
                            "positions" % (lname(l), fmt(l["gap"]), U, rng, U))
            if l["rise"] is None:
                l["rise"] = dz
            elif abs(l["rise"] - dz) > max(tol_base, 0.15 * abs(dz)):
                cons.append("%s: stated rise %s%s but Z difference is %s%s" %
                            (lname(l), fmt(l["rise"]), U, fmt(dz), U))
        if l["gap"] is None:
            l["gap"] = 0.0 if l["move"] in ("walk", "drop", "ride") else None
        if l["rise"] is None:
            l["rise"] = 0.0 if l["move"] in ("walk", "ride") else None
        if l["gap"] is None or l["rise"] is None:
            raise InputError("%s: needs Gap and Rise (or coordinates on both nodes)" % lname(l))
    if any(n["pos"] for n in nodes.values()):
        add("consistency", "FAIL" if cons else "PASS", cons)

    # per-link evaluation
    over, teaser_msgs, fall_msgs, depth_msgs, fail_missing = [], [], [], [], []
    teaser_fail = False
    for l in full:
        mv = l["move"]
        l["teaser"] = mv.startswith("teaser")
        l["usable"], l["pct"], l["band"] = False, None, None
        if l["teaser"]:
            later = mv.split(":", 1)[1].strip() if ":" in mv else None
            best, bestm = math.inf, None
            for name, m in moves.items():
                if name == later:
                    continue
                p, _ = usage(m, l["gap"], l["rise"])
                if p < best:
                    best, bestm = p, name
            l["pct"] = best
            if best < 1.0:
                teaser_fail = True
                teaser_msgs.append("%s: teaser is reachable with %s (%s); move it beyond 150%% or "
                                   "make it a real route" % (lname(l), bestm, pct(best)))
            elif best < 1.3:
                teaser_fail = True
                teaser_msgs.append("%s: teaser at %s of %s looks makeable; push it to >= 150%% "
                                   "(gap or rise) or remove the landing lip" % (lname(l), pct(best), bestm))
            elif best < 1.5:
                teaser_msgs.append("%s: teaser at %s of %s; >= 150%% reads clearly impossible" %
                                   (lname(l), pct(best), bestm))
            if later:
                if later not in moves:
                    raise InputError("%s: teaser move '%s' is not in the move table" % (lname(l), later))
                p, _ = usage(moves[later], l["gap"], l["rise"])
                if p > 1.0:
                    teaser_fail = True
                    teaser_msgs.append("%s: teaser for %s needs %s of it; the later ability must be "
                                       "able to make it" % (lname(l), later, pct(p)))
            continue
        if mv == "walk":
            l["pct"] = 0.0
        elif mv == "drop":
            l["pct"] = 0.0 if l["rise"] <= 0 else math.inf
            if l["rise"] > 0:
                over.append("%s: drop with positive rise %s%s" % (lname(l), fmt(l["rise"]), U))
        elif mv == "ride":
            l["pct"], l["unmodelled"] = 0.0, True
        elif mv in moves:
            p, r = usage(moves[mv], l["gap"], l["rise"])
            l["pct"] = p
            if p > 1.0 + EPS:
                over.append(fix_text(l, moves[mv], p, r, 1.0, U))
        else:
            raise InputError("%s: move '%s' is not in the move table (built in: walk, drop, ride, "
                             "teaser)" % (lname(l), mv))
        l["usable"] = l["pct"] is not None and l["pct"] <= 1.0 + EPS
        l["band"] = band(l["pct"]) if l["pct"] is not None else None
        # falls
        if l["rise"] < 0:
            h = -l["rise"]
            fb = fall_band(h, kit, moves)
            l["fall_band"] = fb
            if fb in ("costly", "lethal"):
                fall_msgs.append((fb, l, h))
        if not l["fail_text"] and mv not in ("walk", "drop", "ride"):
            fail_missing.append(lname(l))
        # depth axis
        if l["camera"] == "along" and pw and nodes[l["to"]]["landing"]:
            need = 3 * pw
            if nodes[l["to"]]["landing"][0] < need - EPS and mv not in ("walk", "ride"):
                depth_msgs.append(("WARN", "%s: depth-axis jump onto a %s%s landing; widen it to >= %s%s "
                                   "(3 x player width) or turn the jump across the screen" %
                                   (lname(l), fmt(nodes[l["to"]]["landing"][0]), U, fmt(need), U)))
        elif l["camera"] in ("across", "diagonal") and pw and nodes[l["to"]]["landing"]:
            if nodes[l["to"]]["landing"][0] < 2 * pw - EPS and mv not in ("walk", "ride"):
                depth_msgs.append(("WARN", "%s: landing %s%s is under 2 x player width (%s%s); fine for a "
                                   "deliberate beam or post, otherwise widen it" %
                                   (lname(l), fmt(nodes[l["to"]]["landing"][0]), U, fmt(2 * pw), U)))
        if l["camera"] == "along" and l["pct"] is not None and 0.75 < l["pct"] <= 1.0 + EPS and mv not in ("walk", "drop", "ride"):
            depth_msgs.append(("WARN", "%s: %s jump at %s along the depth axis; players judge distance "
                               "best across the screen: turn it or drop it below 75%%" %
                               (lname(l), l["band"], pct(l["pct"]))))
        if l["camera"].startswith("unknown:"):
            depth_msgs.append(("WARN", "%s: camera '%s' not understood (across / along / diagonal)" %
                               (lname(l), l["camera"][8:])))

    # roles
    starts = [n for n in nodes.values() if "start" in n["roles"]]
    goals = {n["id"] for n in nodes.values() if n["roles"] & {"goal", "end", "exit"}}
    if len(starts) != 1:
        raise InputError("need exactly one node with role 'start' in the node table (found %d)" % len(starts))
    if not goals:
        raise InputError("need at least one node with role 'goal'")
    start = starts[0]["id"]
    cps = {n["id"] for n in nodes.values() if n["roles"] & {"checkpoint", "start"}}

    # graph
    def edges(skip=None, with_fail=True, with_back=True, skip_moves=()):
        g = {n: [] for n in nodes}
        for i, l in enumerate(full):
            if not l.get("usable") or i == skip or l["move"] in skip_moves:
                continue
            g[l["from"]].append((l["to"], i))
            if with_fail:
                kind, tgt = parse_fail(l, nodes)
                if kind == "fall" and tgt:
                    g[l["from"]].append((tgt, None))
                if with_back and kind == "respawn" and tgt:
                    g[l["from"]].append((tgt, None))
                if with_back and kind in ("death", "restart"):
                    g[l["from"]].append((start, None))
        return g

    def bfs(g, src):
        seen = {src: None}
        dq = deque([src])
        while dq:
            u = dq.popleft()
            for v, i in g[u]:
                if v not in seen:
                    seen[v] = (u, i)
                    dq.append(v)
        return seen

    g_all = edges()
    reach_set = bfs(g_all, start)
    goal_ok = any(x in reach_set for x in goals)
    det = []
    if not goal_ok:
        frontier = sorted(reach_set)
        det.append("no route from %s to a goal; reachable: %s" % (start, ", ".join(frontier)))
    det += over
    add("reachability", "FAIL" if (not goal_ok or over) else "PASS", det)

    # critical links: removing them cuts every route (falls into a lower route count as routes)
    g_prog = edges(with_back=False)

    def goal_reachable(g):
        s = bfs(g, start)
        return any(x in s for x in goals)

    critical = set()
    if goal_ok:
        for i, l in enumerate(full):
            if l.get("usable") and l["from"] in reach_set and not goal_reachable(edges(skip=i, with_back=False)):
                critical.add(i)
    for i in critical:
        full[i]["critical"] = True
    cm = []
    for i in sorted(critical):
        l = full[i]
        if l["pct"] is not None and l["pct"] > args.critical_max + EPS and l["move"] in moves:
            _, r = usage(moves[l["move"]], l["gap"], l["rise"])
            cm.append(fix_text(l, moves[l["move"]], l["pct"], r, args.critical_max, U, critical=True))
    add("critical-max", "FAIL" if cm else "PASS", cm)

    # softlock
    rev = {n: [] for n in nodes}
    for u, outs in g_all.items():
        for v, _ in outs:
            rev[v].append(u)
    can_finish = set()
    dq = deque(goals)
    can_finish |= set(goals)
    while dq:
        v = dq.popleft()
        for u in rev[v]:
            if u not in can_finish:
                can_finish.add(u)
                dq.append(u)
    stuck = sorted(n for n in reach_set if n not in can_finish)
    sl = ["%s is reachable but has no way to a goal (no exit link, no fail that sends you back); "
          "add a climb-out, a respawn, or a link onward" % n for n in stuck]
    if goal_ok:
        add("softlock", "FAIL" if sl else "PASS", sl)
    else:
        add("softlock", "SKIP", ["no route to a goal yet; fix reachability first"])

    # respawn / replay
    g_fwd = {n: [] for n in nodes}
    for i, l in enumerate(full):
        if l.get("usable"):
            g_fwd[l["from"]].append((l["to"], i))
    rs, rs_fail = [], False
    for l in full:
        if not l.get("usable") or l["move"] in ("walk", "ride"):
            continue
        kind, tgt = parse_fail(l, nodes)
        if kind == "bad":
            rs_fail = True
            rs.append("%s: fail '%s' names an unknown node" % (lname(l), l["fail_text"]))
            continue
        if kind == "fall" and nodes[l["from"]]["pos"] and nodes[tgt]["pos"]:
            h = nodes[l["from"]]["pos"][2] - nodes[tgt]["pos"][2]
            if fall_band(h, kit, moves) == "lethal":
                rs.append("%s: a miss 'falls to %s' but that drop is %s%s, lethal; write the fail as "
                          "death or add a catch ledge" % (lname(l), tgt, fmt(h), U))
        if kind in ("respawn", "fall"):
            path = shortest(g_fwd, tgt, l["from"])
            if path is None:
                if kind == "respawn":
                    rs_fail = True
                    rs.append("%s: a miss respawns at %s, which has no route back to %s (respawn past a "
                              "one-way link); move the respawn before it" % (lname(l), tgt, l["from"]))
                elif tgt not in can_finish:
                    pass  # reported by softlock
                else:
                    rs.append("%s: a miss lands on %s, which never leads back to %s; fine if that is an "
                              "intended lower route" % (lname(l), tgt, l["from"]))
                continue
            l["replay"] = len(path)
        elif kind in ("death", "restart"):
            src_set = [start] if kind == "restart" else sorted(cps)
            best = None
            for c in src_set:
                p = shortest(g_fwd, c, l["from"])
                if p is not None and (best is None or len(p) < len(best[1])):
                    best = (c, p)
            if best is None:
                rs_fail = True
                rs.append("%s: no checkpoint leads back to %s after a death" % (lname(l), l["from"]))
                continue
            l["replay"], l["replay_from"] = len(best[1]), best[0]
            path = best[1]
        else:
            continue
        hard = sum(1 for i in path if full[i]["pct"] is not None and full[i]["pct"] > 0.75)
        l["replay_hard"] = hard
        if l["replay"] > args.max_replay_links or (hard >= 3 and l["pct"] and l["pct"] > 0.75):
            rs.append("%s: a miss replays %d links (%d above 75%%); add a checkpoint or safe-ledge "
                      "respawn nearer the take-off" % (lname(l), l["replay"], hard))
    add("respawn", "FAIL" if rs_fail else ("WARN" if rs else "PASS"), rs)
    add("fail-stated", "WARN" if fail_missing else "PASS",
        ["%s: say what a miss does (respawn N / fall N / death / none)" % x for x in fail_missing])

    # falls
    fm, ff = [], False
    for fb, l, h in fall_msgs:
        need = l.get("critical")
        if fb == "lethal" and need:
            ff = True
            fm.append("%s: required drop of %s%s is lethal (>= lethal_fall); add a catch ledge, water "
                      "or a lower landing" % (lname(l), fmt(h), U))
        elif fb == "lethal":
            fm.append("%s: drop of %s%s is lethal; only as a visible death, never as a route" % (lname(l), fmt(h), U))
        else:
            fm.append("%s: drop of %s%s costs health (>= damage_fall)%s" %
                      (lname(l), fmt(h), U, "; it is on the critical path" if need else ""))
    if fall_msgs or any(k in kit for k in ("safe_fall", "damage_fall", "lethal_fall")):
        add("falls", "FAIL" if ff else ("WARN" if fm else "PASS"), fm)
    add("depth-axis", "WARN" if depth_msgs else "PASS", [m for _, m in depth_msgs])
    if any(l["teaser"] for l in full):
        add("teasers", "FAIL" if teaser_fail else ("WARN" if teaser_msgs else "PASS"), teaser_msgs)

    # visibility
    if has_visible:
        vm = []
        for i in sorted(critical):
            l = full[i]
            vis = nodes[l["to"]]["visible_from"]
            if vis is not None and l["from"] not in vis and l["move"] not in ("walk", "ride"):
                vm.append("%s: landing %s is not visible from take-off %s (blind jump on the critical "
                          "path)" % (lname(l), l["to"], l["from"]))
        for n in nodes.values():
            if "secret" in n["roles"]:
                vis = n["visible_from"] or []
                if not any(v in reach_set for v in vis):
                    vm.append("secret %s has no reachable vantage; let it be seen from somewhere first "
                              "(hidden-but-fair rule)" % n["id"])
        add("visibility", "WARN" if vm else "PASS", vm)

    # teaches test: beatable with the full kit, not beatable without the taught moves
    if without:
        unknown = sorted(m for m in without if m not in moves)
        if unknown:
            raise InputError("--teaches: move(s) not in the move table: %s" % ", ".join(unknown))
        still = goal_reachable(edges(with_back=False, skip_moves=without))
        det = ["goal %s without %s" % ("still reachable" if still else "unreachable",
                                       ", ".join(sorted(without)))]
        if still:
            det.append("add a link only the taught move can make on every route, or remove the bypass")
        first = [l for l in full if l["move"] in without and l.get("usable") and l["from"] in reach_set]
        if first:
            depth = bfs_depth(g_prog, start)
            l0 = min(first, key=lambda l: depth.get(l["from"], 1e9))
            if (l0["pct"] or 0) > 0.75 or parse_fail(l0, nodes)[0] in ("death", "restart"):
                det.append("first use %s is %s with fail '%s'; teach it below 75%% with a cheap miss" %
                           (lname(l0), pct(l0["pct"]), l0["fail_text"] or "?"))
                still = still or "warn"
        add("teaches", "FAIL" if still is True else ("WARN" if still else "PASS"), det)

    summary = summarise(full, nodes, start, goals, g_fwd, moves, args) if goal_ok else None
    return checks, full, summary


def bfs_depth(g, src):
    d = {src: 0}
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, _ in g[u]:
            if v not in d:
                d[v] = d[u] + 1
                dq.append(v)
    return d


def lname(l):
    return "%s->%s (%s%s)" % (l["from"], l["to"], l["move"], ", reverse" if l.get("reverse") else "")


def fix_text(l, m, p, r, limit, U, critical=False):
    pre = "%s: critical link at %s of %s" % (lname(l), pct(p), l["move"]) if critical else \
        "%s: needs %s of %s, impossible" % (lname(l), pct(p), l["move"])
    if m["type"] == "jump":
        if l["rise"] > m["height"] * limit:
            return "%s; rise %s%s exceeds %s%s (%d%% of apex %s%s): lower the landing or add a step" % (
                pre, fmt(l["rise"]), U, fmt(m["height"] * limit), U, round(limit * 100), fmt(m["height"]), U)
        # find gap so that usage <= limit at this rise
        target = r * limit
        return "%s; gap %s%s vs reach %s%s at rise %s%s: shorten the gap to <= %s%s, lower the landing, " \
               "or add a node" % (pre, fmt(l["gap"]), U, fmt(r), U, fmt(l["rise"]), U, fmt(target), U)
    if m["type"] == "range":
        return "%s; distance %s%s vs range %s%s: move the anchor within %s%s" % (
            pre, fmt(math.hypot(l["gap"], l["rise"])), U, fmt(m["range"]), U, fmt(m["range"] * limit), U)
    return "%s; rise %s%s gap %s%s vs climb %s%s: add a hold or step" % (
        pre, fmt(l["rise"]), U, fmt(l["gap"]), U, fmt(m["rise"]), U)


def fall_band(h, kit, moves):
    lethal, dmg, safe = kit.get("lethal_fall"), kit.get("damage_fall"), kit.get("safe_fall")
    if lethal is not None and h >= lethal - EPS:
        return "lethal"
    if dmg is not None and h >= dmg - EPS:
        return "costly"
    apex = max([m["height"] for m in moves.values() if m["type"] == "jump"] or [0.0])
    climb = max([m["rise"] for m in moves.values() if m["type"] == "climb"] or [0.0])
    if h <= max(apex, climb) + EPS:
        return "free"
    if safe is not None and dmg is None and h > safe + EPS:
        return "costly"
    return "committed"


def parse_fail(l, nodes):
    t = l["fail_text"].strip()
    if not t:
        return None, None
    m = re.match(r"(?i)\s*(respawn|reset|fall|drop|land|death|die|dead|kill|checkpoint|restart|none|safe|no)\b"
                 r"(?:\s*(?:to|at|on|onto)?\s*([^\s,;()]+))?", t)
    if not m:
        return "unknown", None
    k = m.group(1).lower()
    tgt = m.group(2)
    if k in ("respawn", "reset"):
        k = "respawn"
    elif k in ("fall", "drop", "land"):
        k = "fall"
    elif k in ("death", "die", "dead", "kill", "checkpoint"):
        return "death", None
    elif k == "restart":
        return "restart", None
    else:
        return "none", None
    if not tgt or tgt not in nodes:
        return "bad", None
    return k, tgt


def shortest(g, src, dst):
    """Link indices on a fewest-links path src -> dst over forward links, [] if src == dst."""
    if src == dst:
        return []
    prev = {src: None}
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, i in g[u]:
            if v not in prev:
                prev[v] = (u, i)
                if v == dst:
                    path = []
                    while prev[v]:
                        u2, i2 = prev[v]
                        path.append(i2)
                        v = u2
                    return path[::-1]
                dq.append(v)
    return None


def summarise(full, nodes, start, goals, g_fwd, moves, args):
    # easiest route: minimise the hardest link, then the number of links
    best = {start: (0.0, 0)}
    prev = {start: None}
    pq = [(0.0, 0, start)]
    while pq:
        mx, hops, u = heapq.heappop(pq)
        if (mx, hops) > best.get(u, (math.inf, 0)):
            continue
        for v, i in g_fwd[u]:
            cand = (max(mx, full[i]["pct"] or 0.0), hops + 1)
            if cand < best.get(v, (math.inf, math.inf)):
                best[v], prev[v] = cand, (u, i)
                heapq.heappush(pq, (cand[0], cand[1], v))
    g = min((x for x in goals if x in best), key=lambda x: best[x])
    route, v = [], g
    while prev[v]:
        u, i = prev[v]
        route.append(i)
        v = u
    route = route[::-1]
    chain, longest = 0, 0
    for i in route:
        l = full[i]
        if l["pct"] is not None and l["pct"] > 0.75:
            chain += 1
            longest = max(longest, chain)
        else:
            chain = 0
        if nodes[l["to"]]["roles"] & {"rest", "checkpoint"}:
            chain = 0
    maxp = max([full[i]["pct"] or 0.0 for i in route] or [0.0])
    techs = sorted({full[i]["move"] for i in route if full[i]["move"] not in ("walk", "drop", "ride")})
    hard_techs = {full[i]["move"] for i in route if (full[i]["pct"] or 0) > 0.75}
    tier = 1
    for lim in (0.50, 0.70, 0.80, 0.90, 0.95):
        if maxp > lim + EPS:
            tier += 1
    reasons = ["hardest link %s" % pct(maxp)]
    if longest >= 4:
        tier += 1
        reasons.append("%d chained links > 75%% without rest" % longest)
    if longest >= 8:
        tier += 1
    if len(hard_techs) >= 3:
        tier += 1
        reasons.append("%d techniques used above 75%%" % len(hard_techs))
    punishing = [full[i] for i in route if (full[i]["pct"] or 0) > 0.75 and
                 (full[i].get("replay", 0) >= args.max_replay_links or
                  parse_fail(full[i], nodes)[0] in ("restart",))]
    if punishing:
        tier += 1
        reasons.append("hard links with long replays")
    tier = min(tier, 8)
    counts = {}
    for l in full:
        if l["band"]:
            counts[l["band"]] = counts.get(l["band"], 0) + 1
    return {"route": ["%s->%s" % (full[i]["from"], full[i]["to"]) for i in route],
            "route_text": " ".join([start] + ["-%s-> %s" % (full[i]["move"], full[i]["to"]) for i in route]),
            "hardest": maxp, "longest_chain": longest, "techniques": techs, "bands": counts,
            "tier": tier, "tier_name": TIERS[tier - 1], "tier_reasons": reasons}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="jump_links.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="Exit codes: 0 pass (warnings allowed), 1 check failed, 2 usage/parse error.")
    ap.add_argument("file", help="markdown or JSON file, '-' for stdin")
    ap.add_argument("--kit", help="kit JSON file or inline object (overrides the file's Kit/Moves)")
    ap.add_argument("--critical-max", type=float, default=0.9,
                    help="max fraction of a move for links every route needs (default 0.9)")
    ap.add_argument("--teaches", help="comma-separated moves the sequence must require (teaches test)")
    ap.add_argument("--max-replay-links", type=int, default=6,
                    help="warn when a miss replays more links than this (default 6)")
    ap.add_argument("--up", choices=("z", "y"), default="z", help="vertical axis of X/Y/Z (default z)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 2
    try:
        kit, moves, nodes, links, has_vis = load(args.file, args.kit, args.up)
        checks, full, summary = analyse(kit, moves, nodes, links, has_vis, args)
    except InputError as e:
        if args.json:
            print(json.dumps({"error": str(e), "not_modelled": NOT_MODELLED}))
        else:
            print("error: %s" % e, file=sys.stderr)
        return 2
    failed = any(c["status"] == "FAIL" for c in checks)
    U = kit.get("units", "")
    table = []
    for l in full:
        table.append({"link": "%s->%s" % (l["from"], l["to"]), "move": l["move"], "gap": l["gap"],
                      "rise": l["rise"], "pct": None if l["pct"] in (None, math.inf) else round(l["pct"], 3),
                      "band": l["band"] or ("teaser" if l["teaser"] else None),
                      "critical": bool(l.get("critical")), "camera": l["camera"] or None,
                      "fail": l["fail_text"] or None, "replay_links": l.get("replay"),
                      "fall_band": l.get("fall_band")})
    res = {"file": args.file, "units": U, "result": "fail" if failed else "pass", "checks": checks,
           "links": table, "summary": summary, "not_modelled": NOT_MODELLED}
    if args.json:
        print(json.dumps(res, indent=2, default=lambda x: None if x == math.inf else x))
        return 1 if failed else 0
    L = ["jump_links: %s  (%d nodes, %d links, units %s)" % (args.file, len(nodes), len(full), U or "?")]
    L.append("%-16s %-10s %6s %6s %6s  %-8s %s" % ("link", "move", "gap", "rise", "use", "band", "notes"))
    for l, t in zip(full, table):
        notes = []
        if t["critical"]:
            notes.append("critical")
        if t["camera"]:
            notes.append(t["camera"])
        if t["fall_band"] and t["fall_band"] != "free":
            notes.append("fall:" + t["fall_band"])
        if t["replay_links"] is not None:
            notes.append("replay %d" % t["replay_links"])
        if l.get("unmodelled"):
            notes.append("not modelled")
        free = l["move"] in ("walk", "ride")
        L.append("%-16s %-10s %6s %6s %6s  %-8s %s" % (t["link"], l["move"][:10], "-" if free else fmt(l["gap"]),
                                                       "-" if free else fmt(l["rise"]),
                                                       "-" if l["pct"] is None else pct(l["pct"]),
                                                       t["band"] or "-", ", ".join(notes)))
    for c in checks:
        L.append("%-5s %s" % (c["status"], c["check"]))
        for d in c["details"]:
            L.append("      - " + d)
    if summary:
        L.append("Easiest route: " + summary["route_text"])
        L.append("Hardest link %s; longest rest-free chain > 75%%: %d; techniques: %s" % (
            pct(summary["hardest"]), summary["longest_chain"], ", ".join(summary["techniques"]) or "-"))
        L.append("Tier estimate [convention]: %d %s (%s); calibrate in a gym" % (
            summary["tier"], summary["tier_name"], "; ".join(summary["tier_reasons"])))
    L.append(NOT_MODELLED)
    L.append("RESULT: %s" % res["result"].upper())
    print("\n".join(L))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
