#!/usr/bin/env python3
"""jump_links.py - check a jump-link table (2D or 3D traversal) against a movement kit.

Usage:
  python3 -I scripts/jump_links.py FILE [--kit KIT.json] [--critical-max 0.9]
          [--teaches MOVE[,MOVE]] [--max-replay 5] [--no-scan] [--up z|y] [--json]

FILE is a UTF-8 markdown file ('-' = stdin) holding up to four tables, found by their
headers (case-insensitive, any column order; extra columns such as Note are ignored), or a
JSON file with the keys kit, moves, nodes, links. The format is assets/jump-sequence-spec.md.

  Kit    | Kit | Value |   rows (all optional): units, player_width, damage_fall (drops this
         high or more hurt), lethal_fall (this high or more kill), safe_fall (used only when
         damage_fall is blank: drops above it cost), fall_from (apex | takeoff: where fall
         height is measured for jumps; default apex)
  Moves  | Move | Distance | Height | Range | Rise | Gate |
         Distance + Height  ballistic jump: flat edge-to-edge distance D and apex H; reach at
                            rise h is D/2 * (1 + sqrt(1 - h/H)) (same parabola as
                            platformer_reach.py), so jumps up reach less and jumps down more
         Range              straight-line reach (grapple, swing, teleport): hypot(gap, rise)
         Rise [+ Distance]  mantle / ledge grab: rise <= Rise, gap <= Distance (0 if blank)
         Gate = yes         a modifier technique (crouch-jump = jump + duck): graded on
                            distance only, because the extra height is a yes/no technique
                            gate, not precision. A rise above its Height is still impossible.
         Built in, no row needed: walk (connected on foot: path, stairs, beam; any length),
         drop (step off an edge, rise < 0), ladder (any rise, no gap), ride (lift, mover,
         scripted: not modelled, always usable), blocked (a pair that geometry such as a
         wall or ceiling stops; only silences the skip scan). Duplicate move names are an error.
  Nodes  | Node | Role | Landing | X | Y | Z | Visible from |
         Role: start, goal, checkpoint, rest, reward, secret (comma-separated, several ok).
         Landing: "AxB" = size along X, then along the other horizontal axis (Y; Z with
         --up y); "A" = square. X/Y/Z optional centre of the landing top; Z is up unless
         --up y. Visible from: nodes the landing can be seen from (taken as written).
  Links  | From | To | Move | Gap | Rise | Camera | Fail | Dir | Window |
         Gap: horizontal edge-to-edge distance. Rise: landing height minus take-off height
         (negative = down). Gap/Rise may be blank when both nodes have coordinates; with
         coordinates, gaps are rectangle-to-rectangle, so corner cuts and offsets are exact.
         Camera: across (screen plane), along (depth axis), diagonal, first-person.
         Fail: what a miss does: "respawn N", "fall N" (lands on node N), "death" (back to
         the nearest checkpoint), "restart", "none" (a miss can't happen or costs nothing).
         Dir: "both" adds the reverse link. Window: seconds of a timed jump (sinking block,
         lift step-off). Move "teaser" = a visible link that must look impossible with every
         move; "teaser:MOVE" = reachable only with MOVE (an ability the player gets later).

Checks (thresholds are [convention] defaults):
  reachability   start reaches a goal; prescriptive fixes for links over 100% of the move
  critical-max   links every route needs stay <= --critical-max of the move (0.9; use 1.0
                 only for opt-in expert content); percentages rounded as printed
  softlock       every node the player can reach (by links or by falling) can still reach a
                 goal; deliberate failing counts as a way out
  respawn        "respawn N" / "fall N" targets exist and lead back to the failed take-off
                 (a respawn past a one-way link is a bug); a miss replays <= --max-replay
                 challenge links (walk, ride, drop and ladder links don't count)
  fail-stated    every challenge link says what a miss does
  depth-axis     "along" jumps: landing >= 3 x player_width along the jump (2 x otherwise)
                 and <= 75% of the move; first-person sequences get one summary line
  falls          drops and miss falls banded free / committed / costly / lethal; lethal
                 drops never required; nothing within +-10% of damage_fall or lethal_fall
  teasers        teaser links sit >= 130% of every move (150% clean); teaser:MOVE is
                 reachable with MOVE
  skip-scan      (needs coordinates; --no-scan turns it off) unlisted node pairs that a move
                 can make and that would skip links; 100-130% ones that look makeable
  consistency    stated Gap/Rise agree with node coordinates
  visibility     (Visible from column) critical landings visible from take-off; secret nodes
                 have a reachable vantage
  teaches        (--teaches) the goal is unreachable without the listed moves (their links
                 are re-tested with the remaining moves), and their first use is <= 75%
                 with a non-lethal miss
Summary: bands per link, easiest route, longest rest-free chain of > 75% links, distinct
techniques, timed links, and a tier estimate on an 8-step scale (1 Very easy ... 8 Death)
[convention]: the hardest link sets the base (<= 50, 70, 80, 90, 95, 100%); a chain of 4+
(and 8+), 3+ techniques above 75%, punishing replays, and a timed window <= 1 s each add one.

Exit codes: 0 no failures (warnings allowed); 1 a check failed; 2 usage/parse error.
"""

import argparse
import heapq
import json
import math
import re
import sys
from collections import deque

NOT_MODELLED = ("Not modelled: walls and ceilings between nodes (the skip scan assumes open "
                "air: list blocked pairs), sightlines (Visible from is taken as written), "
                "camera occlusion, lift and mover timing beyond the Window column, momentum, "
                "air control and speed boosts beyond the parabola, readability of surfaces, "
                "input precision and latency; numbers are only as good as the table.")

EMPTY = {"", "-", "–", "—", "n/a", "na", "--"}
BANDS = ((0.40, "intro"), (0.75, "routine"), (0.90, "skill"), (1.00, "expert"))
TIERS = ("Very easy", "Easy", "Medium", "Advanced", "Hard", "Very hard", "Extreme", "Death")
BUILTIN = ("walk", "drop", "ride", "ladder", "blocked")
FREE = ("walk", "drop", "ride", "ladder")      # links that are not challenges
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


def cell(row, i, keep_none=False):
    if i is None or i >= len(row):
        return ""
    v = row[i].strip()
    if v.lower() in EMPTY or (v.lower() == "none" and not keep_none):
        return ""
    return v


def number(s, what):
    if s in ("", None):
        return None
    if isinstance(s, (int, float)):
        return float(s)
    m = re.match(r"^[~≈]?\s*([-+]?\d+(?:\.\d+)?)", str(s).replace("−", "-"))
    if not m:
        raise InputError("%s: '%s' is not a number" % (what, s))
    return float(m.group(1))


def size(s, what):
    if s in ("", None):
        return None
    if isinstance(s, (int, float)):
        return (float(s), float(s))
    nums = re.findall(r"\d+(?:\.\d+)?", str(s))
    if not nums:
        raise InputError("%s: '%s' is not a size like 2x3" % (what, s))
    v = [float(x) for x in nums[:2]]
    return (v[0], v[1] if len(v) > 1 else v[0])


def yes(v):
    return str(v or "").strip().lower() in ("y", "yes", "true", "1", "x", "gate")


def parse_markdown(text):
    doc = {"kit": {}, "moves": [], "nodes": [], "links": []}
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
            ci = {k: col(head, k) for k in ("distance", "height", "range", "rise", "gate")}
            for r in rows:
                name = cell(r, 0)
                if name:
                    doc["moves"].append(dict({k: cell(r, i) for k, i in ci.items()}, name=name))
        elif kind == "nodes":
            ci = {"role": col(head, "role", "type"), "landing": col(head, "landing", "size", "width"),
                  "x": col(head, exact=("x",)), "y": col(head, exact=("y",)), "z": col(head, exact=("z",)),
                  "visible_from": col(head, "visible", "seen")}
            for r in rows:
                nid = cell(r, 0)
                if nid:
                    n = {k: cell(r, i) for k, i in ci.items()}
                    n["id"] = nid
                    if ci["visible_from"] is None:
                        n.pop("visible_from")
                    doc["nodes"].append(n)
        else:
            ci = {"from": col(head, "from", "take-off", "takeoff"), "to": col(head, exact=("to",)),
                  "move": col(head, "move", "verb", "action"),
                  "gap": col(head, "gap", "dist", "horizontal"),
                  "rise": col(head, "rise", "Δh", "dh", "height", "up"),
                  "camera": col(head, "camera", "view", "axis"),
                  "dir": col(head, "dir", "way", "direction"),
                  "window": col(head, "window", "timing", "time")}
            fi = col(head, "fail", "on fail", "miss")
            for n, r in enumerate(rows, 1):
                l = {k: cell(r, i) for k, i in ci.items()}
                l["fail"] = cell(r, fi, keep_none=True)
                l["row"] = n
                doc["links"].append(l)
    return doc


def normalise(doc, up):
    """Turn markdown strings or JSON values into typed structures."""
    kit = {"fall_from": "apex"}
    for k, v in (doc.get("kit") or {}).items():
        k = k.lower()
        key = {"unit": "units", "safe_fall_height": "safe_fall", "fall_damage_height": "damage_fall",
               "lethal_fall_height": "lethal_fall", "width": "player_width"}.get(k, k)
        if key == "units":
            kit["units"] = str(v)
        elif key == "fall_from":
            kit["fall_from"] = "takeoff" if str(v).strip().lower().startswith("take") else "apex"
        elif key in ("player_width", "player_height", "safe_fall", "damage_fall", "lethal_fall"):
            kit[key] = number(v, "kit " + k)
    raw_moves = doc.get("moves") or []
    if isinstance(raw_moves, dict):
        raw_moves = [dict(m, name=n) for n, m in raw_moves.items()]
    moves = {}
    for m in raw_moves:
        name = str(m["name"]).strip().lower()
        if name in moves:
            raise InputError("move '%s' is listed twice" % name)
        if name in BUILTIN or name.startswith("teaser"):
            raise InputError("move '%s' is built in; don't redefine it" % name)
        mm = {k: number(m.get(k), "move %s %s" % (name, k)) for k in ("distance", "height", "range", "rise")}
        mm["gate"] = yes(m.get("gate"))
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
        moves[name] = mm
    nodes = {}
    hor = ("x", "y") if up == "z" else ("x", "z")
    for n in doc.get("nodes") or []:
        nid = str(n["id"]).strip()
        if nid in nodes:
            raise InputError("node %s is listed twice" % nid)
        role = n.get("role") or ""
        roles = role if isinstance(role, list) else re.split(r"[,;/+ ]+", str(role))
        roles = {r.strip().lower() for r in roles if r.strip()}
        land = size(n.get("landing"), "node %s landing" % nid)
        coords = [n.get(a) for a in ("x", "y", "z")]
        pos = None
        if all(c not in (None, "") for c in coords):
            p = {a: number(n[a], "node %s %s" % (nid, a)) for a in ("x", "y", "z")}
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
        cam = str(l.get("camera") or "").strip().lower()
        if re.match(r"(first|fp|1p|fps)", cam):
            cam = "first-person"
        elif re.match(r"(across|lateral|side|screen|horiz)", cam):
            cam = "across"
        elif re.match(r"(along|depth|into|away|toward|forward|back)", cam):
            cam = "along"
        elif re.match(r"diag|45|oblique", cam):
            cam = "diagonal"
        elif cam:
            cam = "unknown:" + cam
        two = str(l.get("dir") or "").strip().lower() in ("both", "2", "two-way", "two way", "<->", "↔")
        links.append({"row": row, "from": a, "to": b, "move": mv,
                      "gap": number(l.get("gap"), "link %s->%s gap" % (a, b)),
                      "rise": number(l.get("rise"), "link %s->%s rise" % (a, b)),
                      "window": number(l.get("window"), "link %s->%s window" % (a, b)),
                      "camera": cam, "fail_text": str(l.get("fail") or "").strip(), "two_way": two})
    if not links:
        raise InputError("no link table found (needs From and To columns)")
    return kit, moves, nodes, links


def load(path, kit_arg, up):
    if path == "-":
        text = sys.stdin.read()
    else:
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
        has_vis = any("visible_from" in n for n in doc.get("nodes") or [])
    else:
        doc = parse_markdown(text)
        has_vis = any("visible_from" in n for n in doc["nodes"])
    if kit_arg:
        try:
            if kit_arg.strip().startswith("{"):
                extra = json.loads(kit_arg)
            else:
                with open(kit_arg, encoding="utf-8") as f:
                    extra = json.load(f)
        except (OSError, ValueError) as e:
            raise InputError("cannot read kit %s: %s" % (kit_arg, e))
        over = extra.pop("moves", None) or {}
        if over:
            cur = doc.get("moves") or []
            if isinstance(cur, dict):
                cur = [dict(m, name=n) for n, m in cur.items()]
            names = {n.lower() for n in over}
            doc["moves"] = [m for m in cur if str(m["name"]).lower() not in names] + \
                [dict(m, name=n) for n, m in over.items()]
        doc["kit"] = dict(doc.get("kit") or {}, **extra)
    kit, moves, nodes, links = normalise(doc, up)
    return kit, moves, nodes, links, has_vis


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
        p = gap / r
        if not m["gate"]:
            p = max(p, max(0.0, rise) / m["height"])
        return p, r
    if m["type"] == "range":
        return math.hypot(gap, rise) / m["range"], m["range"]
    pr = max(0.0, rise) / m["rise"] if m["rise"] > 0 else math.inf
    d = m["distance"] or 0.0
    pg = gap / d if d > EPS else (0.0 if gap <= 0.05 * max(1.0, m["rise"]) else math.inf)
    return max(pr, pg), d


def rect_gap(a, b):
    """Edge-to-edge horizontal gap between two axis-aligned landings, centre distance."""
    la = a["landing"] or (0.0, 0.0)
    lb = b["landing"] or (0.0, 0.0)
    dx = abs(b["pos"][0] - a["pos"][0])
    dy = abs(b["pos"][1] - a["pos"][1])
    gx = max(0.0, dx - (la[0] + lb[0]) / 2.0)
    gy = max(0.0, dy - (la[1] + lb[1]) / 2.0)
    return math.hypot(gx, gy)


def extent_along(a, b):
    """Depth of b's landing along the a->b direction (min side without coordinates)."""
    land = b["landing"]
    if not land:
        return None
    if not (a["pos"] and b["pos"]):
        return min(land)
    dx, dy = b["pos"][0] - a["pos"][0], b["pos"][1] - a["pos"][1]
    d = math.hypot(dx, dy)
    if d < EPS:
        return min(land)
    ux, uy = abs(dx) / d, abs(dy) / d
    cand = [land[0] / ux if ux > EPS else math.inf, land[1] / uy if uy > EPS else math.inf]
    return min(cand)


def rnd(p):
    return p if p in (None, math.inf) else round(p, 2)


def band(p):
    p = rnd(p)
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


def lname(l):
    return "%s->%s (%s%s)" % (l["from"], l["to"], l["move"], ", reverse" if l.get("reverse") else "")


# ---------- main analysis ----------

def analyse(kit, moves, nodes, links, has_vis, args):
    checks = []
    U = kit.get("units", "")
    pw = kit.get("player_width")

    def add(name, status, details):
        checks.append({"check": name, "status": status, "details": details})

    teach = {m.strip().lower() for m in (args.teaches or "").split(",") if m.strip()}
    full = []
    for l in links:
        full.append(dict(l, reverse=False))
        if l["two_way"]:
            r = dict(l, reverse=True)
            r["from"], r["to"] = l["to"], l["from"]
            if l["rise"] is not None:
                r["rise"] = -l["rise"]
            full.append(r)
    blocked = {(l["from"], l["to"]) for l in full if l["move"] == "blocked"}
    blocked |= {(b, a) for a, b in blocked}
    full = [l for l in full if l["move"] != "blocked"]

    # consistency with coordinates, fill blanks
    cons = []
    for l in full:
        a, b = nodes[l["from"]], nodes[l["to"]]
        if a["pos"] and b["pos"] and l["move"] not in ("walk", "ride"):
            g = rect_gap(a, b)
            dz = b["pos"][2] - a["pos"][2]
            tol = max(0.25 * (pw or 1.0), 0.15 * g)
            if l["gap"] is None:
                l["gap"] = g
            elif abs(l["gap"] - g) > tol:
                cons.append("%s: stated gap %s%s but the landings are %s%s apart edge to edge; fix "
                            "the table or the positions" % (lname(l), fmt(l["gap"]), U, fmt(g), U))
            if l["rise"] is None:
                l["rise"] = dz
            elif abs(l["rise"] - dz) > max(0.25 * (pw or 1.0), 0.15 * abs(dz)):
                cons.append("%s: stated rise %s%s but the Z difference is %s%s" %
                            (lname(l), fmt(l["rise"]), U, fmt(dz), U))
        if l["gap"] is None and l["move"] in ("walk", "drop", "ride", "ladder"):
            l["gap"] = 0.0
        if l["rise"] is None and l["move"] in ("walk", "ride"):
            l["rise"] = 0.0
        if l["gap"] is None or l["rise"] is None:
            raise InputError("%s: needs Gap and Rise (or coordinates on both nodes)" % lname(l))
    if any(n["pos"] for n in nodes.values()):
        add("consistency", "FAIL" if cons else "PASS", cons)

    apex = max([m["height"] for m in moves.values() if m["type"] == "jump"] or [0.0])
    mantle = max([m["rise"] for m in moves.values() if m["type"] == "climb"] or [0.0])

    def fall_band(h):
        lethal, dmg, safe = kit.get("lethal_fall"), kit.get("damage_fall"), kit.get("safe_fall")
        if lethal is not None and h >= lethal - EPS:
            return "lethal"
        if dmg is not None and h >= dmg - EPS:
            return "costly"
        if h <= max(apex, mantle) + EPS:
            return "free"
        if dmg is None and safe is not None and h > safe + EPS:
            return "costly"
        return "committed"

    def near_threshold(h):
        for key in ("damage_fall", "lethal_fall"):
            t = kit.get(key)
            if t and abs(h - t) <= 0.1 * t + EPS:
                return key, t
        return None

    def fall_height(l, drop_to_z=None):
        m = moves.get(l["move"])
        extra = m["height"] if (m and m["type"] == "jump" and kit["fall_from"] == "apex") else 0.0
        if drop_to_z is None:
            return -l["rise"] + extra
        return nodes[l["from"]]["pos"][2] + extra - drop_to_z

    # per-link evaluation
    over, teaser_msgs, fall_msgs, depth_msgs, fail_missing = [], [], [], [], []
    teaser_fail = False
    fp = {"hard": 0, "narrow": 0}
    for l in full:
        mv = l["move"]
        l["teaser"] = mv.startswith("teaser")
        l["usable"], l["pct"], l["band"] = False, None, None
        if l["teaser"]:
            later = mv.split(":", 1)[1].strip() if ":" in mv else None
            if later and later not in moves:
                raise InputError("%s: teaser move '%s' is not in the move table" % (lname(l), later))
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
                p, _ = usage(moves[later], l["gap"], l["rise"])
                if p > 1.0:
                    teaser_fail = True
                    teaser_msgs.append("%s: teaser for %s needs %s of it; the later ability must be "
                                       "able to make it" % (lname(l), later, pct(p)))
            continue
        if mv in ("walk", "ride", "ladder"):
            l["pct"] = 0.0
            l["unmodelled"] = mv == "ride"
        elif mv == "drop":
            l["pct"] = 0.0 if l["rise"] <= 0 else math.inf
            if l["rise"] > 0:
                over.append("%s: drop with positive rise %s%s" % (lname(l), fmt(l["rise"]), U))
        elif mv in moves:
            p, r = usage(moves[mv], l["gap"], l["rise"])
            l["pct"] = p
            if p > 1.0 + EPS:
                over.append(fix_text(l, moves[mv], p, r, 1.0, U))
        else:
            raise InputError("%s: move '%s' is not in the move table (built in: %s, teaser)" %
                             (lname(l), mv, ", ".join(BUILTIN)))
        l["usable"] = l["pct"] <= 1.0 + EPS
        l["band"] = band(l["pct"])
        challenge = mv not in FREE
        # intended falls
        if l["rise"] < 0 and mv not in ("ladder", "ride"):
            h = fall_height(l)
            fb = fall_band(h)
            if mv == "drop" or fb in ("costly", "lethal"):
                l["fall_band"] = fb
            fall_msgs.append(("drop", l, h, None))
        if challenge and not l["fail_text"]:
            fail_missing.append(lname(l))
        # depth axis
        jumpish = mv in moves and moves[mv]["type"] in ("jump", "range")
        if jumpish and pw:
            ext = extent_along(nodes[l["from"]], nodes[l["to"]])
            hard = l["pct"] is not None and 0.75 < rnd(l["pct"]) <= 1.0 + EPS
            if l["camera"] == "first-person":
                fp["hard"] += hard
                fp["narrow"] += ext is not None and ext < 3 * pw - EPS
            elif l["camera"] == "along":
                if ext is not None and ext < 3 * pw - EPS:
                    depth_msgs.append("%s: depth-axis jump onto a landing %s%s deep along the jump; "
                                      "widen it to >= %s%s (3 x player width) or turn the jump across "
                                      "the screen" % (lname(l), fmt(ext), U, fmt(3 * pw), U))
                if hard:
                    depth_msgs.append("%s: %s jump at %s along the depth axis; players judge distance "
                                      "best across the screen: turn it or drop it to <= 75%%" %
                                      (lname(l), l["band"], pct(l["pct"])))
            elif l["camera"] in ("across", "diagonal") and ext is not None and ext < 2 * pw - EPS:
                depth_msgs.append("%s: landing %s%s is under 2 x player width (%s%s); fine for a "
                                  "deliberate beam or post, otherwise widen it" %
                                  (lname(l), fmt(ext), U, fmt(2 * pw), U))
        if l["camera"].startswith("unknown:"):
            depth_msgs.append("%s: camera '%s' not understood (across / along / diagonal / "
                              "first-person)" % (lname(l), l["camera"][8:]))
    if fp["hard"] or fp["narrow"]:
        depth_msgs.append("first person: %d jumps above 75%% and %d landings under 3 x player width "
                          "along the jump; give tops countable grid textures, edge stripes and a "
                          "landing marker or shadow" % (fp["hard"], fp["narrow"]))

    # roles
    starts = [n for n in nodes.values() if "start" in n["roles"]]
    goals = {n["id"] for n in nodes.values() if n["roles"] & {"goal", "end", "exit"}}
    if len(starts) != 1:
        raise InputError("need exactly one node with role 'start' in the node table (found %d)" % len(starts))
    if not goals:
        raise InputError("need at least one node with role 'goal'")
    start = starts[0]["id"]
    cps = {n["id"] for n in nodes.values() if n["roles"] & {"checkpoint", "start"}}

    def edges(skip=None, with_back=True, usable=None):
        g = {n: [] for n in nodes}
        for i, l in enumerate(full):
            ok = l.get("usable") if usable is None else usable(l)
            if not ok or i == skip:
                continue
            g[l["from"]].append((l["to"], i))
            kind, tgt = parse_fail(l, nodes)
            if kind == "fall" and tgt:
                g[l["from"]].append((tgt, None))
            if with_back and kind == "respawn" and tgt:
                g[l["from"]].append((tgt, None))
            if with_back and kind in ("death", "restart"):
                g[l["from"]].append((start, None))
        return g

    def bfs(g, src):
        d = {src: 0}
        dq = deque([src])
        while dq:
            u = dq.popleft()
            for v, _ in g[u]:
                if v not in d:
                    d[v] = d[u] + 1
                    dq.append(v)
        return d

    def goal_reachable(g):
        s = bfs(g, start)
        return any(x in s for x in goals)

    g_all = edges()
    reach_set = bfs(g_all, start)
    goal_ok = any(x in reach_set for x in goals)
    det = []
    if not goal_ok:
        det.append("no route from %s to a goal; reachable: %s" % (start, ", ".join(sorted(reach_set))))
    det += over
    add("reachability", "FAIL" if (not goal_ok or over) else "PASS", det)

    critical = set()
    if goal_ok:
        for i, l in enumerate(full):
            if l.get("usable") and l["from"] in reach_set and not goal_reachable(edges(skip=i, with_back=False)):
                critical.add(i)
                l["critical"] = True
    cm = []
    for i in sorted(critical):
        l = full[i]
        if l["move"] in moves and rnd(l["pct"]) > args.critical_max + EPS:
            _, r = usage(moves[l["move"]], l["gap"], l["rise"])
            cm.append(fix_text(l, moves[l["move"]], l["pct"], r, args.critical_max, U, critical=True))
    add("critical-max", "FAIL" if cm else "PASS", cm)

    # softlock
    rev = {n: [] for n in nodes}
    for u, outs in g_all.items():
        for v, _ in outs:
            rev[v].append(u)
    can_finish = set(goals)
    dq = deque(goals)
    while dq:
        v = dq.popleft()
        for u in rev[v]:
            if u not in can_finish:
                can_finish.add(u)
                dq.append(u)
    if goal_ok:
        sl = ["%s is reachable but has no way to a goal (no exit link, no fail that sends you back); "
              "add a climb-out, a respawn, or a link onward" % n
              for n in sorted(reach_set) if n not in can_finish]
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
        if not l.get("usable") or l["move"] in FREE:
            continue
        kind, tgt = parse_fail(l, nodes)
        if kind == "bad":
            rs_fail = True
            rs.append("%s: fail '%s' names an unknown node" % (lname(l), l["fail_text"]))
            continue
        if kind == "unknown":
            rs.append("%s: fail '%s' not understood (respawn N / fall N / death / restart / none)" %
                      (lname(l), l["fail_text"]))
            continue
        if kind == "fall" and nodes[l["from"]]["pos"] and nodes[tgt]["pos"]:
            h = fall_height(l, nodes[tgt]["pos"][2])
            fall_msgs.append(("miss", l, h, tgt))
        if kind in ("respawn", "fall"):
            path = shortest(g_fwd, tgt, l["from"])
            if path is None:
                if kind == "respawn":
                    rs_fail = True
                    rs.append("%s: a miss respawns at %s, which has no route back to %s (respawn past a "
                              "one-way link); move the respawn before it" % (lname(l), tgt, l["from"]))
                elif tgt in can_finish:
                    rs.append("%s: a miss lands on %s, which never leads back to %s; fine if that is an "
                              "intended lower route" % (lname(l), tgt, l["from"]))
                continue
        elif kind in ("death", "restart"):
            best = None
            for c in ([start] if kind == "restart" else sorted(cps)):
                p = shortest(g_fwd, c, l["from"])
                if p is not None and (best is None or len(p) < len(best)):
                    best = p
            if best is None:
                rs_fail = True
                rs.append("%s: no checkpoint leads back to %s after a death" % (lname(l), l["from"]))
                continue
            path = best
        else:
            continue
        steps = [full[i] for i in path if full[i]["move"] not in FREE]
        l["replay"] = len(steps)
        l["replay_hard"] = sum(1 for s in steps if rnd(s["pct"]) > 0.75)
        l["punishing"] = l["replay"] > args.max_replay or (l["replay_hard"] >= 3 and rnd(l["pct"]) > 0.75)
        if l["punishing"]:
            rs.append("%s: a miss replays %d challenge links (%d above 75%%); add a checkpoint or "
                      "safe-ledge respawn nearer the take-off" % (lname(l), l["replay"], l["replay_hard"]))
    add("respawn", "FAIL" if rs_fail else ("WARN" if rs else "PASS"), rs)
    add("fail-stated", "WARN" if fail_missing else "PASS",
        ["%s: say what a miss does (respawn N / fall N / death / restart / none)" % x for x in fail_missing])

    # falls
    fm, ff = [], False
    for kind, l, h, tgt in fall_msgs:
        fb = fall_band(h)
        what = "drop" if kind == "drop" else "a miss falling to %s" % tgt
        near = near_threshold(h)
        if kind == "drop":
            if fb == "lethal" and l.get("critical"):
                ff = True
                fm.append("%s: required drop of %s%s is lethal (>= lethal_fall); add a catch ledge, "
                          "water or a lower landing" % (lname(l), fmt(h), U))
            elif fb == "lethal":
                fm.append("%s: drop of %s%s is lethal; only as a visible death, never as a route" %
                          (lname(l), fmt(h), U))
            elif fb == "costly":
                fm.append("%s: drop of %s%s costs health (>= damage_fall)%s" %
                          (lname(l), fmt(h), U, "; it is on the critical path" if l.get("critical") else ""))
        elif fb == "lethal":
            fm.append("%s: %s drops %s%s, lethal; write the fail as death or add a catch ledge" %
                      (lname(l), what, fmt(h), U))
        if near:
            fm.append("%s: %s of %s%s is within 10%% of %s (%s%s); players can't tell which side "
                      "it is on: move it clear" % (lname(l), what, fmt(h), U, near[0], fmt(near[1]), U))
    if fall_msgs or any(k in kit for k in ("safe_fall", "damage_fall", "lethal_fall")):
        add("falls", "FAIL" if ff else ("WARN" if fm else "PASS"), fm)
    add("depth-axis", "WARN" if depth_msgs else "PASS", depth_msgs)
    if any(l["teaser"] for l in full):
        add("teasers", "FAIL" if teaser_fail else ("WARN" if teaser_msgs else "PASS"), teaser_msgs)

    # skip scan: an unlisted pair skips links when it brings the player 2+ links nearer a goal
    rg = {n: [] for n in nodes}
    for u, outs in g_fwd.items():
        for v, i in outs:
            rg[v].append((u, i))
    to_goal = {}
    dq = deque(goals)
    for x in goals:
        to_goal[x] = 0
    while dq:
        v = dq.popleft()
        for u, _ in rg[v]:
            if u not in to_goal:
                to_goal[u] = to_goal[v] + 1
                dq.append(u)
    have_pos = [n for n in nodes.values() if n["pos"]]
    if not args.no_scan and len(have_pos) >= 2 and goal_ok:
        linked = {(l["from"], l["to"]) for l in full}
        sk, near_sk = [], []
        jm = {k: m for k, m in moves.items() if m["type"] in ("jump", "range", "climb")}
        for a in have_pos:
            for b in have_pos:
                if a is b or (a["id"], b["id"]) in linked or (a["id"], b["id"]) in blocked:
                    continue
                if a["id"] not in reach_set or a["id"] not in to_goal or b["id"] not in to_goal:
                    continue
                skipped = to_goal[a["id"]] - to_goal[b["id"]] - 1
                if skipped < 1:
                    continue
                gap, rise = rect_gap(a, b), b["pos"][2] - a["pos"][2]
                best, bm = math.inf, None
                for k, m in jm.items():
                    p, _ = usage(m, gap, rise)
                    if p < best:
                        best, bm = p, k
                if best <= 1.0 + EPS:
                    sk.append("%s->%s: unlisted, %s makes it at %s (gap %s%s, rise %s%s) and it skips %d "
                              "link%s; block it (and list it as 'blocked'), move it out of reach, or list "
                              "it as an intended skip" % (a["id"], b["id"], bm, pct(best), fmt(gap), U,
                                                          fmt(rise), U, skipped, "" if skipped == 1 else "s"))
                elif best < 1.3 and skipped >= 2:
                    near_sk.append("%s->%s: unlisted, %s of %s; looks makeable and would skip %d links, so "
                                   "players will try it: push it past 130%% or block it" %
                                   (a["id"], b["id"], pct(best), bm, skipped))
        add("skip-scan", "WARN" if (sk or near_sk) else "PASS", sk + near_sk)

    # visibility
    if has_vis:
        vm = []
        for i in sorted(critical):
            l = full[i]
            vis = nodes[l["to"]]["visible_from"]
            if vis is not None and l["from"] not in vis and l["move"] not in ("walk", "ride", "ladder"):
                vm.append("%s: landing %s is not visible from take-off %s (blind jump on the critical "
                          "path)" % (lname(l), l["to"], l["from"]))
        for n in nodes.values():
            if "secret" in n["roles"] and not any(v in reach_set for v in (n["visible_from"] or [])):
                vm.append("secret %s has no reachable vantage; let it be seen from somewhere first "
                          "(hidden-but-fair rule)" % n["id"])
        add("visibility", "WARN" if vm else "PASS", vm)

    # teaches test: links using the taught moves are re-tested with the remaining moves
    if teach:
        unknown = sorted(m for m in teach if m not in moves)
        if unknown:
            raise InputError("--teaches: move(s) not in the move table: %s" % ", ".join(unknown))
        rest = {k: m for k, m in moves.items() if k not in teach}
        alt = []

        def still_ok(l):
            if not l.get("usable"):
                return False
            if l["move"] not in teach:
                return True
            for k, m in rest.items():
                p, _ = usage(m, l["gap"], l["rise"])
                if p <= 1.0 + EPS:
                    alt.append("%s can also be made with %s (%s)" % (lname(l), k, pct(p)))
                    return True
            return False
        still = goal_reachable(edges(with_back=False, usable=still_ok))
        det = ["goal %s without %s" % ("still reachable" if still else "unreachable", ", ".join(sorted(teach)))]
        det += sorted(set(alt))
        status = "FAIL" if still else "PASS"
        first = [l for l in full if l["move"] in teach and l.get("usable") and l["from"] in reach_set]
        if first and not still:
            d0 = bfs(edges(with_back=False), start)
            l0 = min(first, key=lambda l: d0.get(l["from"], 1e9))
            if rnd(l0["pct"]) > 0.75 or parse_fail(l0, nodes)[0] in ("death", "restart"):
                det.append("first use %s is %s with fail '%s'; teach it at <= 75%% with a cheap miss" %
                           (lname(l0), pct(l0["pct"]), l0["fail_text"] or "?"))
                status = "WARN"
        add("teaches", status, det)

    summary = summarise(full, nodes, start, goals, g_fwd, moves, args) if goal_ok else None
    return checks, full, summary


def fix_text(l, m, p, r, limit, U, critical=False):
    pre = "%s: critical link at %s of %s" % (lname(l), pct(p), l["move"]) if critical else \
        "%s: needs %s of %s, impossible" % (lname(l), pct(p), l["move"])
    if m["type"] == "jump":
        if l["rise"] > m["height"] * (1.0 if m["gate"] else limit):
            cap = m["height"] * (1.0 if m["gate"] else limit)
            return "%s; rise %s%s exceeds %s%s (apex %s%s): lower the landing or add a step" % (
                pre, fmt(l["rise"]), U, fmt(cap), U, fmt(m["height"]), U)
        return "%s; gap %s%s vs reach %s%s at rise %s%s: shorten the gap to <= %s%s, lower the landing, " \
               "or add a node" % (pre, fmt(l["gap"]), U, fmt(r), U, fmt(l["rise"]), U, fmt(r * limit), U)
    if m["type"] == "range":
        return "%s; distance %s%s vs range %s%s: move the anchor within %s%s" % (
            pre, fmt(math.hypot(l["gap"], l["rise"])), U, fmt(m["range"]), U, fmt(m["range"] * limit), U)
    return "%s; rise %s%s gap %s%s vs mantle %s%s: add a hold or step" % (
        pre, fmt(l["rise"]), U, fmt(l["gap"]), U, fmt(m["rise"]), U)


def parse_fail(l, nodes):
    t = l["fail_text"].strip()
    if not t:
        return None, None
    m = re.match(r"(?i)\s*(respawn|reset|fall|drop|land|death|die|dead|kill|checkpoint|restart|none|safe|no)\b"
                 r"(?:\s*(?:to|at|on|onto)?\s*([^\s,;:()]+))?", t)
    if not m:
        return "unknown", None
    k, tgt = m.group(1).lower(), m.group(2)
    if k in ("death", "die", "dead", "kill", "checkpoint"):
        return "death", None
    if k == "restart":
        return "restart", None
    if k in ("none", "safe", "no"):
        return "none", None
    k = "respawn" if k in ("respawn", "reset") else "fall"
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
            cand = (max(mx, rnd(full[i]["pct"])), hops + 1)
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
    R = [full[i] for i in route]
    chain, longest = 0, 0
    for l in R:
        if l["move"] not in FREE and rnd(l["pct"]) > 0.75:
            chain += 1
            longest = max(longest, chain)
        elif l["move"] not in FREE:
            chain = 0
        if nodes[l["to"]]["roles"] & {"rest", "checkpoint"}:
            chain = 0
    maxp = max([rnd(l["pct"]) for l in R] or [0.0])
    techs = sorted({l["move"] for l in R if l["move"] not in FREE})
    hard_techs = {l["move"] for l in R if l["move"] not in FREE and rnd(l["pct"]) > 0.75}
    timed = [l for l in R if l.get("window") is not None]
    tier = 1
    for lim in (0.50, 0.70, 0.80, 0.90, 0.95):
        if maxp > lim + EPS:
            tier += 1
    reasons = ["hardest link %s" % pct(maxp)]
    if longest >= 4:
        tier += 1 + (longest >= 8)
        reasons.append("%d chained links > 75%% without rest" % longest)
    if len(hard_techs) >= 3:
        tier += 1
        reasons.append("%d techniques used above 75%%" % len(hard_techs))
    if any(l.get("punishing") for l in R):
        tier += 1
        reasons.append("hard links with long replays")
    if any(l["window"] <= 1.0 + EPS for l in timed):
        tier += 1
        reasons.append("timed window <= 1 s")
    tier = min(tier, 8)
    counts = {}
    for l in full:
        if l["band"]:
            counts[l["band"]] = counts.get(l["band"], 0) + 1
    return {"route": ["%s->%s" % (l["from"], l["to"]) for l in R],
            "route_text": " ".join([start] + ["-%s-> %s" % (l["move"], l["to"]) for l in R]),
            "hardest": maxp, "longest_chain": longest, "techniques": techs, "bands": counts,
            "timed": ["%s->%s %ss" % (l["from"], l["to"], fmt(l["window"])) for l in timed],
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
    ap.add_argument("--max-replay", type=int, default=5,
                    help="warn when a miss replays more challenge links than this (default 5)")
    ap.add_argument("--no-scan", action="store_true", help="skip the unlisted-pair skip scan")
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
        b = l["band"] or ("teaser" if l["teaser"] else None)
        if l.get("fall_band") in ("costly", "lethal") and l["move"] == "drop":
            b = l["fall_band"]
        table.append({"link": "%s->%s" % (l["from"], l["to"]), "move": l["move"], "gap": l["gap"],
                      "rise": l["rise"], "pct": None if l["pct"] in (None, math.inf) else round(l["pct"], 3),
                      "band": b, "critical": bool(l.get("critical")), "camera": l["camera"] or None,
                      "fail": l["fail_text"] or None, "replay_links": l.get("replay"),
                      "window": l.get("window"), "fall_band": l.get("fall_band")})
    res = {"file": args.file, "units": U, "result": "fail" if failed else "pass", "checks": checks,
           "links": table, "summary": summary, "not_modelled": NOT_MODELLED}
    if args.json:
        print(json.dumps(res, indent=2))
        return 1 if failed else 0
    L = ["jump_links: %s  (%d nodes, %d links, units %s)" % (args.file, len(nodes), len(full), U or "?")]
    L.append("%-16s %-10s %6s %6s %6s  %-8s %s" % ("link", "move", "gap", "rise", "use", "band", "notes"))
    for l, t in zip(full, table):
        notes = []
        if t["critical"]:
            notes.append("critical")
        if t["camera"]:
            notes.append(t["camera"])
        if t["window"] is not None:
            notes.append("window %ss" % fmt(t["window"]))
        if t["fall_band"] and t["fall_band"] != "free":
            notes.append("fall:" + t["fall_band"])
        if t["replay_links"] is not None:
            notes.append("replay %d" % t["replay_links"])
        if l.get("unmodelled"):
            notes.append("not modelled")
        free = l["move"] in ("walk", "ride")
        L.append("%-16s %-10s %6s %6s %6s  %-8s %s" % (
            t["link"], l["move"][:10], "-" if free else fmt(l["gap"]), "-" if free else fmt(l["rise"]),
            "-" if l["pct"] is None else pct(l["pct"]), t["band"] or "-", ", ".join(notes)))
    for c in checks:
        L.append("%-5s %s" % (c["status"], c["check"]))
        for d in c["details"]:
            L.append("      - " + d)
    if summary:
        L.append("Easiest route: " + summary["route_text"])
        L.append("Hardest link %s; longest rest-free chain > 75%%: %d; techniques: %s%s" % (
            pct(summary["hardest"]), summary["longest_chain"], ", ".join(summary["techniques"]) or "-",
            "; timed: " + ", ".join(summary["timed"]) if summary["timed"] else ""))
        L.append("Tier estimate [convention]: %d %s (%s); calibrate in a gym" % (
            summary["tier"], summary["tier_name"], "; ".join(summary["tier_reasons"])))
    L.append(NOT_MODELLED)
    L.append("RESULT: %s" % res["result"].upper())
    print("\n".join(L))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
