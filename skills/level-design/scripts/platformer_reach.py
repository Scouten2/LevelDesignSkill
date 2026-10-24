#!/usr/bin/env python3
"""platformer_reach.py - gravity-true reachability and jump-margin check for ASCII platformer maps.

Usage:
  python3 -I scripts/platformer_reach.py FILE --kit KIT.json [--teaches MOVE]
          [--enemies hazard|ignore] [--margin 0.9] [--json]

FILE is a tile map (UTF-8 text, '-' = stdin). Rows run top to bottom, row 0 is the top;
coordinates in every message are (col,row), origin top-left. Code fences, a column ruler line
(digits and spaces only) and row-index prefixes like "07|" are stripped. Short rows are padded
with empty tiles (reported as a warning).

Glyphs (VGLC / Mario-AI superset):
  - . space   empty                 X # S ? Q < > [ ] B b   solid
  =           one-way platform (stand on top, pass through from below and the sides)
  ^           hazard (touching kills)  E  enemy (a static hazard cell unless --enemies ignore)
  o           coin / collectible     *  key collectible (must be reachable)
  H           ladder (climb up/down; the top rung can be stood on)
  @ or M      player start (marks the player's lower-left cell)
  F or G      goal (reached when the player's box overlaps it, mid-air included)
  C           checkpoint             W  water (treated as empty; reported in a note)
Left and right map edges are walls, above the map is open air, below the map is a death pit.

KIT.json (lengths in tiles, times in seconds). --kit also accepts an inline JSON object.
  {"jump_height": 4.0, "jump_distance": 6.0, "player_width": 1, "player_height": 1,
   "air_control": true, "coyote_time": 0.1, "double_jump": false, "wall_jump": false,
   "dash_distance": 0, "fall_damage_height": null, "safe_fall_height": null}
  safe_fall_height = highest drop with no cost; fall_damage_height = drop at which falls
  damage or kill. Falls on the easiest route over safe_fall_height are reported "costly",
  at/over fall_damage_height "damaging" (lethal only with "fall_kills": true). Warnings only.
  Required: jump_height (max apex rise of a full jump) and jump_distance (max horizontal
  distance of a full running jump that lands at take-off height). Optional extras:
  "time_to_apex" (s, default 0.4 [convention]; only converts coyote_time into tiles),
  "fall_kills" (default false: falls >= fall_damage_height are reported, not lethal; true
  makes them lethal), "drop_through" (default false: down+jump drops through '=').

Model:
  - The player is an axis-aligned box player_width x player_height tiles. Jumps are parabolas
    derived from (jump_height H, jump_distance D): gravity and launch speed give apex H at
    time 1, horizontal run speed is D/2 per unit time, so a full running jump covers D at
    take-off height. Variable jump height: launches at 25/50/75/100% of H.
  - Fixed-step integration (30 steps to apex) with axis-separated tile collision: walls stop
    horizontal motion only (the player slides up a wall and hops onto the ledge once clear),
    ceilings stop the rise (head bonk), floors/one-way tops/ladder tops stop the fall.
  - air_control true: at the apex (or 0.5 into a walk-off fall) the player may switch to
    any of -1, -1/2, 0, +1/2, +1 x run speed. false: horizontal speed is fixed at take-off.
  - double_jump: one extra full or half jump at the apex (or 0.5 into a fall).
  - wall_jump: touching a wall in the air creates a cling state; from it the player kicks
    away at full speed (with air_control may steer back after a short kick: single-wall climbs).
  - dash_distance > 0: one horizontal dash of that length per airtime (ground or at the apex),
    gravity suspended during the dash, walls stop it.
  - Double jump and dash refresh on ground, ladders and wall clings.
  - Take-off and landing positions are tile-snapped (no ledge overhang), so an equal-height
    gap of G empty tiles needs jump_distance >= G (about +-0.1 tile from the time step), and a
    wall/step h tiles taller than the take-off floor needs jump_height >= h (equality passes:
    the apex is hit exactly; a 1-tall player needs h, a 2-tall player also needs 2 tiles of
    headroom above the step top). @/M, C, F/G, o, * are non-solid (empty) cells.
    coyote_time adds run_speed x coyote_time tiles of take-off past a ledge.
  - Ladders: climb up/down, step or jump off, grab mid-air when the box passes over one.

Reports: goal reachable from start; reachable/unreachable checkpoints and collectibles (and
collectibles you can only collect by entering a softlock); the "easiest route" (the route
minimising the hardest move) with each jump's dx, dh and their % of the open-air kit
envelope; critical jumps on that route above --margin of the envelope (they are unavoidable:
every route needs a jump at least that hard); softlock pits (reachable standing places from
which the goal is unreachable); falls over safe_fall_height / fall_damage_height; frontier
(furthest column; when the goal is unreachable, the reached cells nearest to it).

Margins: dx = horizontal tiles the jump must clear (|col change| - 1), dh = rows climbed
(negative = drop). dx% = dx / max horizontal reach at that dh; dh% = dh / H (2H with a double
jump); usage = max(dx%, dh%). The envelope is open-air: ceilings that shorten real arcs are
not reflected in the percentage (the reachability itself does include them).

--teaches MOVE  (double_jump | wall_jump | dash | jump_height=X | jump_distance=X):
  re-runs with the move removed (or the value reduced to X). PASS when the goal is reachable
  with the full kit and NOT reachable without the move.

Exit codes: 0 all checks passed; 1 a check failed (goal unreachable, unreachable key or coin,
softlock pit, critical jump over --margin, --teaches FAIL); 2 usage or parse error;
3 the search hit its time cap (result unknown). Falls over safe heights are warnings.
"""

import argparse
import json
import math
import re
import sys
import time
from collections import deque

EMPTY, SOLID, ONEWAY, HAZARD, LADDER = 0, 1, 2, 3, 4
SOLID_GLYPHS = set("X#S?Q<>[]Bb")
EMPTY_GLYPHS = set("-. ")
SP_COIN, SP_KEY, SP_GOAL, SP_CHECK = 1, 2, 3, 4
SP_GLYPH = {"o": SP_COIN, "*": SP_KEY, "F": SP_GOAL, "G": SP_GOAL, "C": SP_CHECK}
EPS = 1e-6
FPS = 30
HEIGHT_FRACS = (0.25, 0.5, 0.75, 1.0)
VX_FRACS_FIXED = (0.0, 0.25, 0.5, 0.75, 1.0)
VX_FRACS_AC = (0.0, 0.5, 1.0)
AC_CHOICES = (-1.0, -0.5, 0.0, 0.5, 1.0)
TIME_CAP = 120.0

F_LAUNCH, F_DJ, F_DASH, F_WALL, F_COYOTE, F_DROP, F_WALK, F_LADDER = 1, 2, 4, 8, 16, 32, 64, 128

NOT_MODELLED = ("Not modelled: enemy movement/AI (E is a static hazard or ignored), moving platforms, "
                "lifts, springs, conveyors and crumbling/breakable blocks (missing ones show up as "
                "frontier stops - a known false-positive class), acceleration/momentum (instant run "
                "speed), slopes, swimming (W = empty), ledge overhang (tile-snapped take-off/landing), "
                "corner correction, jump buffering, reaction-time windows, camera, diagonal dashes, "
                "timing of hazards.")

KIT_DEFAULTS = {
    "jump_height": None, "jump_distance": None, "player_width": 1, "player_height": 1,
    "air_control": True, "coyote_time": 0.1, "double_jump": False, "wall_jump": False,
    "dash_distance": 0, "fall_damage_height": None, "safe_fall_height": None,
    "time_to_apex": 0.4, "fall_kills": False, "drop_through": False,
}


class InputError(Exception):
    pass


class CapHit(Exception):
    pass


# ----------------------------------------------------------------------------- parsing

def read_text(path):
    if path == "-":
        return sys.stdin.read()
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        raise InputError("cannot read %s: %s" % (path, e))


def parse_map(text):
    """Return (rows, warnings). Strips fences, rulers and row-index prefixes."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    rows = [ln for ln in lines if not ln.strip().startswith("```")]
    while rows and rows[-1].strip() == "":
        rows.pop()
    while rows and rows[0].strip() == "":
        rows.pop(0)
    rows = [r for r in rows if not re.fullmatch(r"[\d ]*\d[\d ]*", r)]
    prefix = re.compile(r"^\s*\d+\s?\|")
    nonblank = [r for r in rows if r.strip()]
    if nonblank and all(prefix.match(r) for r in nonblank):
        rows = [prefix.sub("", r, count=1) for r in rows]
    if not rows:
        raise InputError("map is empty")
    warnings = []
    width = max(len(r) for r in rows)
    ragged = [(i, len(r)) for i, r in enumerate(rows) if len(r) != width]
    if ragged:
        desc = ", ".join("row %d has %d" % (i, n) for i, n in ragged[:8])
        warnings.append("ragged rows padded with empty tiles to width %d (%s%s)"
                        % (width, desc, "..." if len(ragged) > 8 else ""))
    rows = [r.ljust(width, "-") for r in rows]
    return rows, warnings


def load_kit(arg):
    text = arg if arg.lstrip().startswith("{") else read_text(arg)
    try:
        raw = json.loads(text)
    except ValueError as e:
        raise InputError("kit is not valid JSON: %s" % e)
    if not isinstance(raw, dict):
        raise InputError("kit must be a JSON object")
    kit = dict(KIT_DEFAULTS)
    unknown = sorted(k for k in raw if k not in KIT_DEFAULTS)
    kit.update({k: v for k, v in raw.items() if k in KIT_DEFAULTS})
    for key in ("jump_height", "jump_distance"):
        if not isinstance(kit[key], (int, float)) or isinstance(kit[key], bool) or kit[key] <= 0:
            raise InputError("kit.%s must be a positive number" % key)
    for key in ("player_width", "player_height"):
        if not isinstance(kit[key], (int, float)) or kit[key] <= 0 or kit[key] > 8:
            raise InputError("kit.%s must be a number in (0, 8]" % key)
    for key in ("coyote_time", "dash_distance", "time_to_apex"):
        if kit[key] is None:
            kit[key] = 0
        if not isinstance(kit[key], (int, float)) or kit[key] < 0:
            raise InputError("kit.%s must be a non-negative number" % key)
    if kit["time_to_apex"] <= 0:
        raise InputError("kit.time_to_apex must be positive")
    for key in ("fall_damage_height", "safe_fall_height"):
        if kit[key] is not None and (not isinstance(kit[key], (int, float)) or kit[key] <= 0):
            raise InputError("kit.%s must be null or a positive number" % key)
    for key in ("air_control", "double_jump", "wall_jump", "fall_kills", "drop_through"):
        kit[key] = bool(kit[key])
    return kit, unknown


# ----------------------------------------------------------------------------- level

class Level:
    def __init__(self, rows, enemies="hazard"):
        self.rows = rows
        self.H = len(rows)
        self.W = len(rows[0])
        self.notes = []
        self.unknown = []
        self.starts, self.goals, self.coins, self.keys, self.checks = [], [], [], [], []
        self.enemy_cells, self.water = [], 0
        self.cls = [[EMPTY] * self.W for _ in range(self.H)]
        self.spec = [[0] * self.W for _ in range(self.H)]
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                k = EMPTY
                if ch in SOLID_GLYPHS:
                    k = SOLID
                elif ch == "=":
                    k = ONEWAY
                elif ch == "^":
                    k = HAZARD
                elif ch == "E":
                    self.enemy_cells.append((c, r))
                    k = HAZARD if enemies == "hazard" else EMPTY
                elif ch == "H":
                    k = LADDER
                elif ch in "@M":
                    self.starts.append((c, r))
                elif ch in SP_GLYPH:
                    self.spec[r][c] = SP_GLYPH[ch]
                    {SP_COIN: self.coins, SP_KEY: self.keys, SP_GOAL: self.goals,
                     SP_CHECK: self.checks}[SP_GLYPH[ch]].append((c, r))
                elif ch == "W":
                    self.water += 1
                elif ch not in EMPTY_GLYPHS:
                    self.unknown.append((ch, c, r))
                self.cls[r][c] = k
        if self.unknown:
            desc = ", ".join("'%s' at (%d,%d)" % u for u in self.unknown[:10])
            self.notes.append("unknown glyphs treated as empty: " + desc
                              + ("..." if len(self.unknown) > 10 else ""))
        if self.water:
            self.notes.append("%d water tile(s) treated as empty air (no swim physics)" % self.water)
        if self.enemy_cells:
            self.notes.append("%d enemy cell(s) treated as %s" % (
                len(self.enemy_cells), "static hazards" if enemies == "hazard" else "empty (ignored)"))


# ----------------------------------------------------------------------------- simulation

class Out:
    __slots__ = ("nodes", "goal", "death")

    def __init__(self):
        self.nodes = {}   # node -> {flags: [fall, touched_set]}
        self.goal = {}    # goal cell -> min flags-set {flags: True}
        self.death = False

    def add(self, node, flags, fall, touched):
        d = self.nodes.setdefault(node, {})
        cur = d.get(flags)
        if cur is None:
            d[flags] = [fall, set(touched)]
        else:
            if fall < cur[0]:
                cur[0] = fall
            cur[1].update(touched)


class Reach:
    def __init__(self, level, kit, deadline):
        self.L = level
        self.kit = kit
        self.deadline = deadline
        H = float(kit["jump_height"])
        D = float(kit["jump_distance"])
        self.Hj, self.Dj = H, D
        self.grav = 2.0 * H
        self.v = 2.0 * H
        self.s = D / 2.0
        self.pw = float(kit["player_width"])
        self.ph = float(kit["player_height"])
        self.ac = kit["air_control"]
        self.dj_full = 1 if kit["double_jump"] else 0
        self.dash_d = float(kit["dash_distance"] or 0)
        self.dash_full = 1 if self.dash_d > 0 else 0
        self.walljump = kit["wall_jump"]
        tc = float(kit["coyote_time"] or 0) / float(kit["time_to_apex"])
        self.coyote_t = tc
        self.coyote_tiles = self.s * tc
        self.fall_kill = kit["fall_damage_height"] if kit["fall_kills"] else None
        self.drop_through = kit["drop_through"]
        self.dt = 1.0 / FPS
        self.maxk = FPS * 40
        # padded grid: PT rows of air on top (row 0 of the pad is a ceiling), PB rows below
        self.PT = int(math.ceil(2 * H * (2 if self.dj_full else 1) + self.ph)) + 4
        self.PB = int(math.ceil(self.ph)) + 4
        W = level.W
        self.G = [[SOLID] * (W + 2)]
        for _ in range(self.PT - 1):
            self.G.append([SOLID] + [EMPTY] * W + [SOLID])
        for r in range(level.H):
            self.G.append([SOLID] + level.cls[r] + [SOLID])
        for _ in range(self.PB):
            self.G.append([SOLID] + [EMPTY] * W + [SOLID])
        self.S = [[0] * (W + 2) for _ in range(self.PT)]
        for r in range(level.H):
            self.S.append([0] + level.spec[r] + [0])
        for _ in range(self.PB):
            self.S.append([0] * (W + 2))
        self.has_spec = bool(level.goals or level.coins or level.keys or level.checks)
        self.has_ladder = any(LADDER in row for row in level.cls)
        self.death_y = level.H + 1.0
        self.frames = 0

    # --- cell helpers (map coordinates) ---
    def cell(self, c, r):
        rr = r + self.PT
        if rr < 0:
            return SOLID
        if rr >= len(self.G):
            return EMPTY
        return self.G[rr][c + 1] if -1 <= c <= self.L.W else SOLID

    def cols(self, x):
        return range(int(math.floor(x + EPS)), int(math.floor(x + self.pw - EPS)) + 1)

    def rows_of(self, y):
        return range(int(math.floor(y + EPS)), int(math.floor(y + self.ph - EPS)) + 1)

    def box_free(self, x, y):
        for r in self.rows_of(y):
            for c in self.cols(x):
                if self.cell(c, r) == SOLID:
                    return False
        return True

    def box_hazard(self, x, y):
        for r in self.rows_of(y):
            for c in self.cols(x):
                if self.cell(c, r) == HAZARD:
                    return True
        return False

    def is_support(self, c, r):
        k = self.cell(c, r)
        if k in (SOLID, ONEWAY):
            return True
        return k == LADDER and self.cell(c, r - 1) != LADDER

    def node_y(self, r):
        return r + 1 - self.ph

    def supported(self, c, r):
        return any(self.is_support(cc, r + 1) for cc in self.cols(c))

    def oneway_only_support(self, c, r):
        ks = [self.cell(cc, r + 1) for cc in self.cols(c)]
        return ONEWAY in ks and SOLID not in ks

    def on_ladder(self, c, r):
        return any(self.cell(cc, r) == LADDER for cc in self.cols(c))

    def ladder_below(self, c, r):
        return any(self.cell(cc, r + 1) == LADDER for cc in self.cols(c))

    def node_ok(self, c, r):
        y = self.node_y(r)
        return self.box_free(c, y) and not self.box_hazard(c, y)

    def standable(self, c, r):
        return self.node_ok(c, r) and (self.supported(c, r) or self.on_ladder(c, r))

    def touch_cells(self, x, y):
        res = []
        for r in self.rows_of(y):
            for c in self.cols(x):
                if 0 <= r < self.L.H and 0 <= c < self.L.W and self.L.spec[r][c]:
                    res.append((c, r))
        return res

    # --- trajectories ---
    def apex_dec(self, vy0, dj, dash, wall_kick=False):
        """Decision time and kind for a fresh segment, or (None, None)."""
        if wall_kick and self.ac:
            return 0.15, "kick"
        has = self.ac or dj > 0 or dash > 0
        if not has:
            return None, None
        if vy0 < 0:
            return -vy0 / self.grav, "apex"
        return 0.5, "fall"

    def branch(self, kind, x, y, vy, vx, flags, dj, dash, touched, out, side=0):
        s = self.s
        if kind == "kick":
            for nvx in (side * s, 0.0):  # steer back toward the wall, or stop
                if nvx != vx:
                    dt_, dk = (None, None)
                    if dj > 0 or dash > 0:
                        dt_, dk = (max(0.0, -vy / self.grav), "apex") if vy < 0 else (0.5, "fall")
                    self.run(x, y, vy, nvx, flags, dj, dash, dt_, dk, y, touched, out)
            return
        if self.ac:
            for f in AC_CHOICES:
                nvx = f * s
                if abs(nvx - vx) > 1e-9:
                    self.run(x, y, vy, nvx, flags, dj, dash, None, None, y, touched, out)
        if dj > 0:
            vxs = (-s, 0.0, s) if self.ac else (vx,)
            for hf in (0.5, 1.0):
                vy0 = -self.v * math.sqrt(hf)
                for nvx in vxs:
                    dt_, dk = (-vy0 / self.grav, "apex") if (self.ac or dash > 0) else (None, None)
                    self.run(x, y, vy0, nvx, flags | F_DJ | F_LAUNCH, dj - 1, dash, dt_, dk,
                             y, touched, out)
        if dash > 0:
            for d in (-1, 1):
                self.dash_run(x, y, d, flags | F_DASH, dj, dash - 1, y, touched, out)

    def wall_contact(self, x, side, y, flags, touched, out):
        cx = int(round(x))
        r = int(math.ceil(y + self.ph - 1 - EPS))
        if r < 0 or r >= self.L.H:
            return
        if not self.node_ok(cx, r):
            return
        ny = self.node_y(r)
        wc = cx + int(math.ceil(self.pw - EPS)) if side > 0 else cx - 1
        if not any(self.cell(wc, rr) == SOLID for rr in self.rows_of(ny)):
            return
        if self.supported(cx, r) or self.on_ladder(cx, r):
            out.add((cx, r, 0), flags, 0.0, touched)
        else:
            out.add((cx, r, side), flags, 0.0, touched)

    def ladder_grab(self, x, y, flags, ypeak, touched, out):
        cx = int(round(x))
        r = int(math.floor(y + self.ph - EPS))
        if 0 <= r < self.L.H and self.on_ladder(cx, r) and self.node_ok(cx, r):
            out.add((cx, r, 0), flags, max(0.0, self.node_y(r) - ypeak), touched)

    def dash_run(self, x, y, d, flags, dj, dash, ypeak, touched, out):
        n = max(1, int(math.ceil(self.dash_d / 0.25)))
        step = d * self.dash_d / n
        touched = tuple(touched)
        for _ in range(n):
            nx = x + step
            if self.box_free(nx, y):
                x = nx
            else:
                x = (math.floor(nx + self.pw - EPS) - self.pw) if d > 0 else (math.floor(nx + EPS) + 1)
                if self.walljump:
                    self.wall_contact(x, d, y, flags, touched, out)
                break
            if self.box_hazard(x, y):
                out.death = True
                return
            if self.has_spec:
                for cell in self.touch_cells(x, y):
                    if self.L.spec[cell[1]][cell[0]] == SP_GOAL:
                        out.goal.setdefault(cell, set()).add(flags)
                    elif cell not in touched:
                        touched = touched + (cell,)
        dt_, dk = (0.5, "fall") if dj > 0 else (None, None)
        self.run(x, y, 0.0, d * self.s, flags, dj, dash, dt_, dk, ypeak, touched, out)
        if self.ac:
            self.run(x, y, 0.0, 0.0, flags, dj, dash, dt_, dk, ypeak, touched, out)

    def run(self, x, y, vy0, vx, flags, dj, dash, dec_t, dec_kind, ypeak, touched, out, side=0):
        """Integrate one segment; recurse at the decision point; record outcomes in out."""
        G, S, PT = self.G, self.S, self.PT
        pw, ph, g, dt = self.pw, self.ph, self.grav, self.dt
        floor = math.floor
        y0 = y
        k = 0
        touched = tuple(touched)
        has_spec, has_ladder, walljump = self.has_spec, self.has_ladder, self.walljump
        death_y = self.death_y
        self.frames += 1
        if self.frames % 2000 == 0 and time.time() > self.deadline:
            raise CapHit()
        while k < self.maxk:
            if dec_t is not None and k / FPS >= dec_t:
                tp = k / FPS
                self.branch(dec_kind, x, y, vy0 + g * tp, vx, flags, dj, dash, touched, out, side)
                dec_t = None
            k += 1
            t = k / FPS
            # horizontal
            if vx != 0.0:
                nx = x + vx * dt
                if vx > 0:
                    cold = floor(x + pw - EPS)
                    cnew = floor(nx + pw - EPS)
                else:
                    cold = floor(x + EPS)
                    cnew = floor(nx + EPS)
                blocked = False
                if cnew != cold:
                    rowsl = floor(y + EPS)
                    rowsh = floor(y + ph - EPS)
                    for r in range(rowsl, rowsh + 1):
                        rr = r + PT
                        if rr <= 0:
                            continue
                        if rr < len(G) and G[rr][cnew + 1] == SOLID:
                            blocked = True
                            break
                if blocked:
                    x = (cnew - pw) if vx > 0 else (cnew + 1)
                    if walljump:
                        self.wall_contact(x, 1 if vx > 0 else -1, y, flags, touched, out)
                else:
                    x = nx
            # vertical
            ny = y0 + vy0 * t + 0.5 * g * t * t
            if ny > y:
                rb_old = floor(y + ph - EPS)
                rb_new = floor(ny + ph - EPS)
                hit = None
                if rb_new > rb_old and ny < death_y:
                    cl = floor(x + EPS)
                    ch = floor(x + pw - EPS)
                    for R in range(rb_old + 1, rb_new + 1):
                        row = G[R + PT]
                        above = G[R + PT - 1]
                        for c in range(cl, ch + 1):
                            kk = row[c + 1]
                            if kk == SOLID:
                                hit = R
                                break
                            if (kk == ONEWAY or (kk == LADDER and above[c + 1] != LADDER)) \
                                    and y + ph <= R + EPS:
                                hit = R
                                break
                        if hit is not None:
                            break
                if hit is not None:
                    yl = hit - ph
                    feet = hit - 1
                    fall = yl - ypeak if yl > ypeak else 0.0
                    for c in (int(round(x)), int(floor(x)), int(math.ceil(x))):
                        if self.standable(c, feet):
                            if self.fall_kill is not None and fall >= self.fall_kill:
                                out.death = True
                                return
                            tl = touched
                            if has_spec:
                                for cell in self.touch_cells(c, self.node_y(feet)):
                                    if self.L.spec[cell[1]][cell[0]] == SP_GOAL:
                                        out.goal.setdefault(cell, set()).add(flags)
                                    elif cell not in tl:
                                        tl = tl + (cell,)
                            out.add((c, feet, 0), flags, fall, tl)
                            return
                    if self.box_hazard(x, yl):
                        out.death = True
                    return
                y = ny
            elif ny < y:
                rt_old = floor(y + EPS)
                rt_new = floor(ny + EPS)
                bonk = None
                if rt_new < rt_old:
                    cl = floor(x + EPS)
                    ch = floor(x + pw - EPS)
                    for R in range(rt_old - 1, rt_new - 1, -1):
                        rr = R + PT
                        row = G[rr] if rr >= 0 else G[0]
                        if rr <= 0 or any(row[c + 1] == SOLID for c in range(cl, ch + 1)):
                            bonk = R
                            break
                if bonk is not None:
                    y = bonk + 1.0
                    y0, vy0, k = y, 0.0, 0
                    if dec_t is not None:
                        dec_t = 0.0
                    continue
                y = ny
            if y > death_y:
                out.death = True
                return
            if y < ypeak:
                ypeak = y
            # hazards
            rl = floor(y + EPS)
            rh = floor(y + ph - EPS)
            cl = floor(x + EPS)
            ch = floor(x + pw - EPS)
            for r in range(rl, rh + 1):
                row = G[r + PT]
                for c in range(cl, ch + 1):
                    if row[c + 1] == HAZARD:
                        out.death = True
                        return
            if has_spec:
                for r in range(rl, rh + 1):
                    srow = S[r + PT]
                    for c in range(cl, ch + 1):
                        sp = srow[c + 1]
                        if sp:
                            if sp == SP_GOAL:
                                out.goal.setdefault((c, r), set()).add(flags)
                            elif (c, r) not in touched:
                                touched = touched + ((c, r),)
            if has_ladder:
                self.ladder_grab(x, y, flags, ypeak, touched, out)
        return

    def jump_roots(self, x, y, flags, out, vx_fracs, heights=HEIGHT_FRACS, dirs=(-1, 1),
                   touched=()):
        s = self.s
        for hf in heights:
            vy0 = -self.v * math.sqrt(hf)
            dt_, dk = self.apex_dec(vy0, self.dj_full, self.dash_full)
            done = set()
            for f in vx_fracs:
                for d in dirs:
                    vx = d * f * s
                    if vx in done:
                        continue
                    done.add(vx)
                    self.run(x, y, vy0, vx, flags, self.dj_full, self.dash_full, dt_, dk, y,
                             touched, out)

    def expand(self, node):
        c, r, m = node
        out = Out()
        y = self.node_y(r)
        s = self.s
        djf, dashf = self.dj_full, self.dash_full
        vx_fracs = VX_FRACS_AC if self.ac else VX_FRACS_FIXED
        if m == 0:
            sup = self.supported(c, r)
            lad = self.on_ladder(c, r)
            for d in (-1, 1):
                nc = c + d
                if not self.box_free(nc, y):
                    continue
                if self.box_hazard(nc, y):
                    out.death = True
                    continue
                t0 = tuple(self.touch_cells(nc, y))
                if self.supported(nc, r) or self.on_ladder(nc, r):
                    out.add((nc, r, 0), F_WALK, 0.0, t0)
                else:
                    dt_, dk = self.apex_dec(0.0, djf, dashf)
                    for f in (0.0, 0.5, 1.0):
                        self.run(nc, y, 0.0, d * f * s, 0, djf, dashf, dt_, dk, y, t0, out)
            if sup or lad:
                self.jump_roots(c, y, F_LAUNCH, out, vx_fracs)
                if sup and self.coyote_tiles > 0:
                    ct = self.coyote_tiles
                    for d in (-1, 1):
                        if not self.box_free(c + d, y) or self.supported(c + d, r):
                            continue
                        xs = c + d * ct
                        ys = y + self.Hj * self.coyote_t ** 2
                        if not self.box_free(xs, ys):
                            ys = y
                        if not self.box_free(xs, ys) or self.box_hazard(xs, ys):
                            continue
                        self.jump_roots(xs, ys, F_LAUNCH | F_COYOTE, out, (0.5, 0.75, 1.0),
                                        dirs=(d,))
                if self.dash_full:
                    for d in (-1, 1):
                        self.dash_run(c, y, d, F_DASH, djf, 0, y, (), out)
                if sup and self.drop_through and self.oneway_only_support(c, r):
                    if self.box_free(c, y + 1):
                        dt_, dk = self.apex_dec(0.0, djf, dashf)
                        self.run(c, y + 1, 0.0, 0.0, F_DROP, djf, dashf, dt_, dk, y, (), out)
            # ladders
            if lad and self.node_ok(c, r - 1) and (self.on_ladder(c, r - 1) or self.supported(c, r - 1)):
                out.add((c, r - 1, 0), F_LADDER, 0.0, self.touch_cells(c, y - 1))
            if (lad or self.ladder_below(c, r)) and self.box_free(c, y + 1):
                if self.box_hazard(c, y + 1):
                    out.death = True
                elif self.on_ladder(c, r + 1) or self.supported(c, r + 1):
                    out.add((c, r + 1, 0), F_LADDER, 0.0, self.touch_cells(c, y + 1))
                else:
                    self.run(c, y + 1, 0.0, 0.0, F_LADDER, djf, dashf, None, None, y + 1, (), out)
        else:
            side = m
            for hf in HEIGHT_FRACS:
                vy0 = -self.v * math.sqrt(hf)
                if self.ac:
                    dt_, dk = 0.15, "kick"
                else:
                    dt_, dk = self.apex_dec(vy0, djf, dashf)
                    if not (djf or dashf):
                        dt_, dk = None, None
                self.run(c, y, vy0, -side * s, F_LAUNCH | F_WALL, djf, dashf, dt_, dk, y, (), out,
                         side=side)
            dt_, dk = self.apex_dec(0.0, djf, dashf)
            for vx in (0.0, -side * s * 0.5):
                self.run(c, y, 0.0, vx, F_WALL, djf, dashf, dt_, dk, y, (), out)
        return out

    # --- envelopes ---
    def env_single(self, dh):
        H = self.Hj
        if dh > H:
            return 0.0
        return self.s * (1.0 + math.sqrt(1.0 - dh / H))

    def env_double(self, dh):
        H = self.Hj
        best = 0.0
        for i in range(0, 301):
            t1 = i / 100.0
            y1 = 2 * H * t1 - H * t1 * t1
            if y1 < dh:
                break
            rem = dh - y1
            if rem > H:
                continue
            tot = t1 + 1.0 + math.sqrt(1.0 - rem / H)
            if tot > best:
                best = tot
        return self.s * best

    def usage(self, u, v, flags, touch=False):
        """(usage, dx, dh, dx_pct, dh_pct) for a move u -> v (v = (col,row,...))."""
        c0, r0 = u[0], u[1]
        c1, r1 = v[0], v[1]
        if touch:
            dx = max(0, abs(c1 - c0) - int(math.ceil(self.pw - EPS)))
            dh = max(0, r0 - int(math.ceil(self.ph - EPS)) - r1)
        else:
            dx = max(0, abs(c1 - c0) - 1)
            dh = r0 - r1
        if flags & (F_WALK | F_LADDER) and not flags & (F_LAUNCH | F_DASH | F_DJ):
            return 0.0, dx, dh, 0.0, 0.0
        H = self.Hj
        if flags & (F_LAUNCH | F_DJ):
            henv = H * (2 if flags & F_DJ else 1)
            env = self.env_double(dh) if flags & F_DJ else self.env_single(dh)
            if not flags & F_WALL:
                env += self.coyote_tiles
        else:
            henv = H
            env = self.s * math.sqrt(max(0.0, -dh) / H)
        if flags & F_DASH:
            env += self.dash_d
        dh_pct = max(0, dh) / henv
        if dx == 0:
            dx_pct = 0.0
        else:
            dx_pct = dx / env if env > 0 else 9.99
        return max(dh_pct, dx_pct), dx, dh, dx_pct, dh_pct


def kind_name(flags):
    parts = []
    if flags & F_WALL:
        parts.append("wall_jump" if flags & F_LAUNCH else "wall_slide")
    elif flags & F_LAUNCH and not flags & F_DJ:
        parts.append("jump")
    if flags & F_DJ:
        parts.append("double_jump")
    if flags & F_DASH:
        parts.append("dash")
    if flags & F_DROP:
        parts.append("drop")
    if flags & F_COYOTE:
        parts.append("coyote")
    if not parts:
        if flags & F_WALK:
            return "walk"
        if flags & F_LADDER:
            return "ladder"
        return "fall"
    return "+".join(parts)


# ----------------------------------------------------------------------------- analysis

def analyse(level, kit, margin, deadline):
    R = Reach(level, kit, deadline)
    res = {"failures": [], "warnings": []}
    if not level.starts:
        raise InputError("no player start ('@' or 'M') in map")
    if len(level.starts) > 1:
        res["warnings"].append("%d starts found; using the first at (%d,%d)"
                               % ((len(level.starts),) + level.starts[0]))
    sc, sr = level.starts[0]
    if not R.node_ok(sc, sr):
        raise InputError("player start (%d,%d) overlaps a solid or hazard tile for a %gx%g player"
                         % (sc, sr, R.pw, R.ph))
    # start node: land the player if the start cell is in the air
    start_nodes = []
    if R.standable(sc, sr):
        start_nodes.append((sc, sr, 0))
    else:
        o = Out()
        R.run(sc, R.node_y(sr), 0.0, 0.0, 0, 0, 0, None, None, R.node_y(sr), (), o)
        start_nodes = list(o.nodes.keys())
    START = ("START",)
    GOAL = ("GOAL",)
    edges = {START: {}}
    for n in start_nodes:
        edges[START][n] = (0.0, F_WALK, 0.0)
    seen = set(start_nodes)
    q = deque(start_nodes)
    coll_hits = {}       # cell -> set of nodes where the player is after collecting it
    dies = set()
    goal_hits = {}
    while q:
        if time.time() > deadline:
            raise CapHit()
        u = q.popleft()
        out = R.expand(u)
        if out.death:
            dies.add(u)
        eu = edges.setdefault(u, {})
        if u[2] == 0:
            for cell in R.touch_cells(u[0], R.node_y(u[1])):
                if level.spec[cell[1]][cell[0]] == SP_GOAL:
                    out.goal.setdefault(cell, set()).add(F_WALK)
                else:
                    coll_hits.setdefault(cell, set()).add(u)
        for v, fd in out.nodes.items():
            best = None
            minfall = min(f[0] for f in fd.values())
            for flags, (fall, touched) in fd.items():
                us = R.usage(u, v, flags)[0]
                if best is None or us < best[0] or (us == best[0] and flags & (F_WALK | F_LADDER)):
                    best = (us, flags)
                for cell in touched:
                    coll_hits.setdefault(cell, set()).add(v)
            prev = eu.get(v)
            if prev is None or best[0] < prev[0]:
                eu[v] = (best[0], best[1], minfall)
            if v not in seen:
                seen.add(v)
                q.append(v)
        for cell, flagset in out.goal.items():
            best = min((R.usage(u, cell, fl, touch=True)[0], fl) for fl in flagset)
            if F_WALK in flagset:
                best = (0.0, F_WALK)
            prev = eu.get(GOAL)
            if prev is None or best[0] < prev[0]:
                eu[GOAL] = (best[0], best[1], 0.0)
                goal_hits[u] = cell
    goal_reached = any(GOAL in e for e in edges.values())

    # reverse reachability to goal
    rev = {}
    for u, e in edges.items():
        for v in e:
            rev.setdefault(v, set()).add(u)
    can_goal = set()
    if goal_reached:
        stack = [GOAL]
        while stack:
            n = stack.pop()
            for p in rev.get(n, ()):
                if p not in can_goal:
                    can_goal.add(p)
                    stack.append(p)

    res["goal_present"] = bool(level.goals)
    res["goal_reachable"] = goal_reached
    res["reachable_positions"] = len([n for n in seen if n[2] == 0])
    res["wall_cling_positions"] = len([n for n in seen if n[2] != 0])
    res["start"] = [sc, sr]
    res["goals"] = [list(g) for g in level.goals]

    # easiest route: minimise (hardest usage, total usage-steps)
    route = []
    hardest = None
    if goal_reached:
        import heapq
        dist = {START: (0.0, 0)}
        prev = {}
        pq = [(0.0, 0, 0, START)]
        cnt = 0
        while pq:
            mx, hops, _, u = heapq.heappop(pq)
            if dist.get(u) != (mx, hops):
                continue
            if u == GOAL:
                break
            for v, (us, fl, fall) in edges.get(u, {}).items():
                nd = (max(mx, us), hops + 1)
                if v not in dist or nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    cnt += 1
                    heapq.heappush(pq, (nd[0], nd[1], cnt, v))
        path = [GOAL]
        while path[-1] != START:
            path.append(prev[path[-1]])
        path.reverse()
        hardest = dist[GOAL][0]
        for a, b in zip(path, path[1:]):
            if a == START:
                continue
            us, fl, fall = edges[a][b]
            if b == GOAL:
                cell = goal_hits[a]
                u_, dx, dh, dxp, dhp = R.usage(a, cell, fl, touch=True)
                to = list(cell)
            else:
                u_, dx, dh, dxp, dhp = R.usage(a, b, fl)
                to = [b[0], b[1]]
            route.append({"from": [a[0], a[1]], "to": to, "kind": kind_name(fl),
                          "to_goal": b == GOAL, "dx": dx, "dh": dh,
                          "dx_pct": round(dxp * 100, 1), "dh_pct": round(dhp * 100, 1),
                          "usage_pct": round(u_ * 100, 1), "fall": round(fall, 2)})
    res["easiest_route"] = {
        "hardest_usage_pct": None if hardest is None else round(hardest * 100, 1),
        "moves": len(route),
        "jumps": [m for m in route if m["kind"] not in ("walk", "ladder")],
    }
    critical = [m for m in route if m["usage_pct"] > margin * 100 + 1e-9]
    res["critical_jumps"] = critical

    # collectibles and checkpoints
    def coll_entry(cell):
        g = level.rows[cell[1]][cell[0]]
        hits = coll_hits.get(cell, set())
        e = {"glyph": g, "cell": list(cell), "reachable": bool(hits)}
        if hits and goal_reached:
            e["safe"] = any(h in can_goal for h in hits)
        return e

    colls = [coll_entry(c) for c in sorted(level.coins + level.keys, key=lambda p: (p[1], p[0]))]
    res["collectibles"] = {"reachable": [c for c in colls if c["reachable"]],
                           "unreachable": [c for c in colls if not c["reachable"]]}
    checks = [coll_entry(c) for c in sorted(level.checks, key=lambda p: (p[1], p[0]))]
    res["checkpoints"] = {"reachable": [c["cell"] for c in checks if c["reachable"]],
                          "unreachable": [c["cell"] for c in checks if not c["reachable"]]}

    # softlocks
    pits = []
    if goal_reached:
        soft = set(n for n in seen if n not in can_goal)
        adj = {}
        for u, e in edges.items():
            for v in e:
                if u in soft and v in soft:
                    adj.setdefault(u, set()).add(v)
                    adj.setdefault(v, set()).add(u)
        done = set()
        for n in sorted(soft, key=lambda p: (p[0], p[1], p[2])):
            if n in done or n[2] != 0:
                continue
            comp, stack = set([n]), [n]
            while stack:
                a = stack.pop()
                for b in adj.get(a, ()):
                    if b not in comp:
                        comp.add(b)
                        stack.append(b)
            done |= comp
            cells = sorted(set((p[0], p[1]) for p in comp if p[2] == 0))
            entries = sorted(set((u[0], u[1]) for u, e in edges.items()
                                 if u != START and u in can_goal for v in e if v in comp))
            pits.append({"cells": [list(c) for c in cells[:20]], "count": len(cells),
                         "entered_from": [list(c) for c in entries[:10]],
                         "escape_only_by_dying": any(p in dies for p in comp)})
    res["softlock_pits"] = pits

    # falls
    safe = kit["safe_fall_height"]
    dmg = kit["fall_damage_height"]
    falls = {"safe_fall_height": safe, "fall_damage_height": dmg, "on_route": [], "forced_cells": []}
    limit = min([h for h in (safe, dmg) if h is not None], default=None)
    if limit is not None:
        for m in route:
            if m["fall"] > limit + 1e-9:
                falls["on_route"].append({"from": m["from"], "to": m["to"], "height": m["fall"],
                                          "class": "damaging" if dmg is not None and m["fall"] >= dmg else "costly"})
        minin = {}
        for u, e in edges.items():
            for v, (_, _, fall) in e.items():
                if v != GOAL and v[2] == 0:
                    minin[v] = min(minin.get(v, 1e9), fall)
        forced = sorted((v for v, f in minin.items() if f > limit + 1e-9), key=lambda p: (p[0], p[1]))
        falls["forced_cells"] = [[v[0], v[1], round(minin[v], 2)] for v in forced[:20]]
        falls["forced_count"] = len(forced)
    res["falls"] = falls

    # frontier
    stand = [n for n in seen if n[2] == 0]
    front = {"furthest_col": max((n[0] for n in stand), default=None), "cells": []}
    if level.goals and not goal_reached and stand:
        gx, gy = level.goals[0]
        near = sorted(stand, key=lambda n: ((n[0] - gx) ** 2 + (n[1] - gy) ** 2, n[0], n[1]))
        front["cells"] = [[n[0], n[1]] for n in near[:5]]
        front["nearest_goal"] = [gx, gy]
    res["frontier"] = front

    # verdicts
    if not level.goals:
        res["warnings"].append("no goal glyph (F/G): goal reachability and softlocks not checked")
    elif not goal_reached:
        res["failures"].append("goal not reachable from start")
    for c in res["collectibles"]["unreachable"]:
        res["failures"].append("%s collectible at (%d,%d) unreachable" % (
            "key" if c["glyph"] == "*" else "coin", c["cell"][0], c["cell"][1]))
    for c in res["collectibles"]["reachable"]:
        if c.get("safe") is False:
            res["failures"].append("collectible at (%d,%d) can only be collected by entering a softlock"
                                   % tuple(c["cell"]))
    for c in res["checkpoints"]["unreachable"]:
        res["warnings"].append("checkpoint at (%d,%d) unreachable" % tuple(c))
    if pits:
        res["failures"].append("%d softlock pit(s)" % len(pits))
    if critical:
        res["failures"].append("%d critical jump(s) over %d%% of the envelope on the easiest route"
                               % (len(critical), round(margin * 100)))
    if falls["on_route"]:
        res["warnings"].append("%d fall(s) over the safe/damage height on the easiest route"
                               % len(falls["on_route"]))
    if falls.get("forced_count"):
        res["warnings"].append("%d position(s) reachable only by a fall over %g tiles"
                               % (falls["forced_count"], limit))
    return res


def reduced_kit(kit, move):
    k = dict(kit)
    if move == "double_jump":
        k["double_jump"] = False
    elif move == "wall_jump":
        k["wall_jump"] = False
    elif move == "dash":
        k["dash_distance"] = 0
    else:
        m = re.fullmatch(r"(jump_height|jump_distance)=([0-9]*\.?[0-9]+)", move)
        if not m:
            raise InputError("--teaches must be double_jump, wall_jump, dash, jump_height=X or "
                             "jump_distance=X")
        val = float(m.group(2))
        if val <= 0:
            raise InputError("--teaches value must be positive")
        k[m.group(1)] = val
    return k


# ----------------------------------------------------------------------------- output

def fmt_pct(p):
    return "%g%%" % p


def human(res, args, level, kit):
    L = []
    L.append("platformer_reach: %s  (%dx%d tiles; kit H=%g D=%g, player %gx%g%s%s%s%s)" % (
        args.file, level.W, level.H, kit["jump_height"], kit["jump_distance"],
        kit["player_width"], kit["player_height"],
        ", air control" if kit["air_control"] else ", no air control",
        ", double jump" if kit["double_jump"] else "",
        ", wall jump" if kit["wall_jump"] else "",
        (", dash %g" % kit["dash_distance"]) if kit["dash_distance"] else ""))
    L.append("Start (%d,%d). Reachable standing positions: %d." % (
        res["start"][0], res["start"][1], res["reachable_positions"]))
    if res["goal_present"]:
        L.append("Goal: %s" % ("REACHABLE" if res["goal_reachable"] else "NOT REACHABLE"))
    er = res["easiest_route"]
    if er["hardest_usage_pct"] is not None:
        L.append("Easiest route: %d moves, %d non-walk; hardest move uses %s of the envelope "
                 "(every route needs at least this)." % (er["moves"], len(er["jumps"]),
                                                       fmt_pct(er["hardest_usage_pct"])))
        for m in er["jumps"]:
            L.append("  (%d,%d)->(%d,%d)%s %-14s dx=%d (%s) dh=%+d (%s) usage %s%s" % (
                m["from"][0], m["from"][1], m["to"][0], m["to"][1], " [goal]" if m["to_goal"] else "",
                m["kind"], m["dx"], fmt_pct(m["dx_pct"]), m["dh"], fmt_pct(m["dh_pct"]),
                fmt_pct(m["usage_pct"]), (" fall %g" % m["fall"]) if m["fall"] else ""))
    cj = res["critical_jumps"]
    L.append("Critical jumps (> %d%% of envelope): %s" % (
        round(args.margin * 100),
        "none" if not cj else "; ".join("(%d,%d)->(%d,%d) %s" % (
            m["from"][0], m["from"][1], m["to"][0], m["to"][1], fmt_pct(m["usage_pct"])) for m in cj)))
    co = res["collectibles"]
    if co["reachable"] or co["unreachable"]:
        L.append("Collectibles: %d/%d reachable%s" % (
            len(co["reachable"]), len(co["reachable"]) + len(co["unreachable"]),
            "" if not co["unreachable"] else "; UNREACHABLE: " + ", ".join(
                "%s (%d,%d)" % (c["glyph"], c["cell"][0], c["cell"][1]) for c in co["unreachable"])))
    ch = res["checkpoints"]
    if ch["reachable"] or ch["unreachable"]:
        L.append("Checkpoints reached: %s%s" % (
            ", ".join("(%d,%d)" % tuple(c) for c in ch["reachable"]) or "none",
            "" if not ch["unreachable"] else "; unreachable: " + ", ".join(
                "(%d,%d)" % tuple(c) for c in ch["unreachable"])))
    if res["goal_present"] and res["goal_reachable"]:
        if res["softlock_pits"]:
            for p in res["softlock_pits"]:
                L.append("Softlock pit: %d cell(s) e.g. %s; entered from %s%s" % (
                    p["count"], ", ".join("(%d,%d)" % tuple(c) for c in p["cells"][:6]),
                    ", ".join("(%d,%d)" % tuple(c) for c in p["entered_from"][:4]) or "?",
                    " (escape only by dying)" if p["escape_only_by_dying"] else " (no escape at all)"))
        else:
            L.append("Softlock pits: none")
    fl = res["falls"]
    if fl["safe_fall_height"] is not None or fl["fall_damage_height"] is not None:
        L.append("Falls over limit on easiest route: %s; positions reachable only by such a fall: %d" % (
            "none" if not fl["on_route"] else ", ".join(
                "(%d,%d)->(%d,%d) %g tiles (%s)" % (f["from"][0], f["from"][1], f["to"][0], f["to"][1],
                                                    f["height"], f["class"]) for f in fl["on_route"]),
            fl.get("forced_count", 0)))
    fr = res["frontier"]
    L.append("Frontier: furthest column %s%s" % (
        fr["furthest_col"], "" if not fr["cells"] else "; nearest reached cells to goal (%d,%d): %s" % (
            fr["nearest_goal"][0], fr["nearest_goal"][1],
            ", ".join("(%d,%d)" % tuple(c) for c in fr["cells"]))))
    if res.get("teaches"):
        t = res["teaches"]
        L.append("Teaches %s: %s (full kit reaches goal: %s; reduced kit reaches goal: %s)" % (
            t["move"], t["result"], "yes" if t["full_kit_reaches_goal"] else "no",
            "yes" if t["reduced_kit_reaches_goal"] else "no"))
    for n in res["notes"]:
        L.append("Note: " + n)
    for w in res["warnings"]:
        L.append("Warning: " + w)
    for f in res["failures"]:
        L.append("FAIL: " + f)
    L.append(NOT_MODELLED)
    L.append("RESULT: %s" % res["result"].upper())
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="platformer_reach.py",
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes: 0 pass, 1 check failed, 2 usage/parse error, 3 time cap (unknown).")
    ap.add_argument("file", help="map file (UTF-8 text), '-' for stdin")
    ap.add_argument("--kit", required=True,
                    help="movement kit JSON file (tiles, seconds) or an inline JSON object")
    ap.add_argument("--teaches", metavar="MOVE",
                    help="double_jump | wall_jump | dash | jump_height=X | jump_distance=X")
    ap.add_argument("--enemies", choices=("hazard", "ignore"), default="hazard",
                    help="treat E as a static hazard cell (default) or ignore it")
    ap.add_argument("--margin", type=float, default=0.9,
                    help="critical-jump threshold as a fraction of the kit envelope (default 0.9)")
    ap.add_argument("--json", action="store_true", help="machine-readable JSON output")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 2
    try:
        if not 0 < args.margin <= 2:
            raise InputError("--margin must be in (0, 2]")
        kit, unknown_keys = load_kit(args.kit)
        rows, warns = parse_map(read_text(args.file))
        level = Level(rows, args.enemies)
        deadline = time.time() + TIME_CAP
        res = analyse(level, kit, args.margin, deadline)
        res["warnings"] = warns + res["warnings"]
        if unknown_keys:
            res["warnings"].append("unknown kit keys ignored: " + ", ".join(unknown_keys))
        res["notes"] = level.notes
        if args.teaches:
            rk = reduced_kit(kit, args.teaches)
            red = analyse(level, rk, args.margin, deadline)
            full_ok = res["goal_reachable"]
            red_ok = red["goal_reachable"]
            t = {"move": args.teaches, "full_kit_reaches_goal": full_ok,
                 "reduced_kit_reaches_goal": red_ok,
                 "result": "PASS" if (full_ok and not red_ok) else "FAIL"}
            if not full_ok:
                t["reason"] = "goal unreachable even with the full kit"
            elif red_ok:
                t["reason"] = ("goal reachable without %s: the level does not require it "
                               "(reduced-kit easiest route hardest move %s%%)"
                               % (args.teaches, red["easiest_route"]["hardest_usage_pct"]))
            res["teaches"] = t
            if t["result"] == "FAIL":
                res["failures"].append("teaches %s: %s" % (args.teaches, t["reason"]))
        else:
            res["teaches"] = None
    except InputError as e:
        msg = "error: %s" % e
        if args.json:
            print(json.dumps({"error": str(e), "not_modelled": NOT_MODELLED}))
        else:
            print(msg, file=sys.stderr)
            print(NOT_MODELLED)
        return 2
    except CapHit:
        if args.json:
            print(json.dumps({"result": "unknown", "error": "time cap of %gs reached" % TIME_CAP,
                              "not_modelled": NOT_MODELLED}))
        else:
            print("RESULT: UNKNOWN (search hit the %gs time cap; split the map into chunks)" % TIME_CAP)
            print(NOT_MODELLED)
        return 3
    res["result"] = "fail" if res["failures"] else "pass"
    res["file"] = args.file
    res["size"] = [level.W, level.H]
    res["kit"] = kit
    res["margin"] = args.margin
    res["not_modelled"] = NOT_MODELLED
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(human(res, args, level, kit))
    return 1 if res["failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
