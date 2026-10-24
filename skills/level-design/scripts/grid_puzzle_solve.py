#!/usr/bin/env python3
"""grid_puzzle_solve.py - solver and analyser for Sokoban-style grid puzzles.

Usage:
  python3 -I scripts/grid_puzzle_solve.py FILE [--max-nodes N] [--max-seconds S]
         [--forbid RULE ...] [--intended MOVES] [--metrics] [--classes] [--json]

Input: a grid in the puzzle legend (see references/grid-conventions.md); FILE may
be "-" (stdin) or a markdown file with a fenced block. Column rulers, row-index
prefixes ("07|") and key-object lines are stripped as in grid_lint.py.
  #  wall          - _ space  floor      @ player     + player on goal
  $  box           *  box on goal         .  goal
  ~  ice: anything moving onto it keeps sliding that way until blocked or off ice
  a-e keys / A-E doors: walking onto a key picks it up; a door is a wall unless
     the player holds its key; entering consumes the key and the door stays open
  O  pit: the player cannot enter; a box pushed in fills it (box and pit -> floor)
  !  switch / | gate: a gate is solid unless every switch holds a box
  X  exit: the win tile when the level has no goals
Win: every goal holds a box (extra boxes allowed); with no goals, the player
reaches an X. Off-grid cells and missing cells of short rows count as walls/floor
respectively (run grid_lint.py --closed first).
Rule details the legend leaves open (fixed here): boxes cannot be pushed onto
uncollected keys or closed doors; gate state is evaluated at the moment of entry
with the moving box already lifted off its old cell; anything already inside a
gate may leave it; a gate with no switches is always open; the player stops
sliding when the next cell is blocked or when it reaches a non-ice cell.

Engines (chosen automatically from the glyphs left after --forbid):
  push-level A*  - only walls/floor/boxes/goals/exits. States are (box layout,
                   player's reachable region), so walking is free and the search
                   is push-optimal. Pruning: dead squares (no goal reachable by
                   pushing) and 2x2/freeze deadlocks (frozen box off a goal), both
                   only when boxes == goals. Moves are then minimised among the
                   push-optimal solutions (exact player positions).
  move-level BFS - when ice, keys/doors, pits or switches/gates are present.
                   States hold player, boxes, held keys, collected keys, opened
                   doors and filled pits; move-optimal. Pruning: fewer boxes on
                   squares that can still reach a goal (relaxed map: every rule
                   tile counted as floor) than there are goals.

Output: solvable | unsolvable | unknown, pushes and moves, solution string
(udlr = walk, UDLR = push), nodes expanded, rules detected / forbidden / used.
Exit codes: 0 solvable (and every requested check passed), 1 unsolvable or a
check failed (--intended illegal, not solving, or a shortcut exists), 2 usage
or parse error, 3 a search cap was hit (unknown).

Options:
  --max-nodes N     node cap per search pass (default 2000000)
  --max-seconds S   wall-clock cap for the whole run (default 60)
  --forbid RULE     bypass test; repeatable. RULE is one of:
                      ice       ice behaves as floor (no sliding)
                      keys      keys are inert floor, doors are walls
                      pits      pits are walls (cannot be filled)
                      switches  switches are floor, gates are walls
                      push      every box is immovable (a wall)
                      box:C,R   the box at (col,row) is immovable
                    For rules that enable moves (keys, pits, switches, box:C,R),
                    still solvable means the rule is bypassable. Ice only removes
                    control, so --forbid ice nearly always stays solvable; compare
                    the solution with and without it instead.
  --intended MOVES  the designer's solution in the solver's own notation (u d l r,
                    case-insensitive; uppercase = push, lowercase = walk; spaces and
                    commas ignored). Checked for legality and for solving; then
                    compared with the optimum: push engine - a shortcut is a
                    solution with strictly fewer pushes (fewer moves only = walking
                    note); move engine - strictly fewer moves.
  --metrics         Jarusek & Pelanek (2010) difficulty proxies:
                      counter_intuitive_pushes: minimum, over push-optimal (push
                        engine) / move-optimal (move engine) solutions, of pushes
                        that increase the pushed box's push-distance to its nearest
                        goal (distance ignores other boxes and all rules).
                      box_changes: how often the pushed box differs from the
                        previous push, MINIMISED OVER ALL SOLUTIONS of any length
                        (0-1 BFS on the explored state space). If the full space
                        exceeds the cap it falls back to the minimum over optimal
                        solutions only (an upper bound); "box_changes_scope" says
                        which. entanglement_excess = box_changes - (boxes that start
                        off a goal - 1), floored at 0; 0 = fully decomposable.
                      first_move_traps: legal first pushes (from the start region)
                        that lead to a state from which the goal is unreachable.
                      dead_end_ratio: share of reachable states (deadlocked states
                        counted when first entered) that cannot reach the goal -
                        "undo need, not difficulty".
                      moves_per_cell: moves / grid cells (Khalifa & Fayek prior for
                        PuzzleScript-style levels: about 1.22 +- 0.46).
  --classes         distinct optimal solutions up to reordering: two optimal
                    solutions are one class when every box makes the same pushes
                    in the same order (only the interleaving between boxes
                    differs) and the same rule events happen (keys, doors, pits,
                    player ice slides). Counting stops at 1000 classes / 200000
                    partial signatures ("capped": true).
  --json            JSON output instead of the human summary.

Size envelope (measured with CPython 3.13 on one core of a cloud container):
  push-only (A* with dead-square, freeze and box-goal matching pruning)
    open 8x10 room, 4 boxes ............ 0.1 s   (--metrics --classes: ~3 s)
    open 12x10 room, 5 boxes ........... ~2 s
    walled 12x12, 5 boxes, 37 pushes ... ~2 s    (--metrics: state space >450k,
                                                   capped at 60 s -> metrics partial)
    open 14x11 room, 7 boxes ........... ~1-6 s
  move-level (ice / keys / pits / switches)
    10x10, 1-2 boxes, several rules .... <1 s
    12x9 open, 3 boxes + ice ........... ~6 s
    10x10 open, 3 boxes + ice + key .... ~15 s; a 4th box usually hits the cap
  Push engine: pruning is off when boxes != goals (extra boxes): such open rooms
  with 5+ boxes can return "unknown". --metrics explores the whole reachable
  space, so it is the first thing to hit the cap; the solve result still stands.
  Memory: roughly 0.5-1 KB per stored state (a 2M-node run can use ~1-2 GB).

Not modelled: real-time elements, pulling or other push variants, multiple
avatars, objects that start on ice/switch/key tiles (no combined glyphs), undo
cost, readability or human difficulty beyond the listed proxies.
Standard library only; Python 3.8+.
"""
import argparse
import heapq
import json
import os
import sys
import time
from array import array
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grid_lint  # noqa: E402  (shared grid extraction)

NOT_MODELLED = ("Not modelled: real-time elements, pulling/other push variants, multiple avatars, "
                "objects starting on ice/switch/key tiles, undo cost, readability; difficulty metrics "
                "are proxies validated only on 4-box Sokoban.")

DIR_NAMES = "udlr"
INF = float("inf")
EV_PUSH, EV_ICE, EV_KEYS, EV_PITS, EV_SWITCH, EV_PSLIDE = 1, 2, 4, 8, 16, 32
RULE_EVENTS = [("push", EV_PUSH), ("ice", EV_ICE), ("keys", EV_KEYS), ("pits", EV_PITS),
               ("switches", EV_SWITCH)]
CLASS_CAP = 1000
SIG_CAP = 200000


class UsageError(Exception):
    pass


class Budget(object):
    def __init__(self, max_nodes, max_seconds):
        self.max_nodes = max_nodes
        self.t0 = time.time()
        self.deadline = self.t0 + max_seconds

    def out_of_time(self):
        return time.time() > self.deadline

    def elapsed(self):
        return time.time() - self.t0


def bits(m):
    while m:
        low = m & -m
        yield low.bit_length() - 1
        m ^= low


def popcount(m):
    return bin(m).count("1")


# --------------------------------------------------------------------------- level

class Level(object):
    """Parsed level in a padded grid (one wall cell of border on every side)."""

    def __init__(self, rows):
        self.h = len(rows)
        self.w = max(len(r) for r in rows)
        self.W = W = self.w + 2
        self.N = W * (self.h + 2)
        self.wall = bytearray([1]) * self.N
        self.goals = self.boxes = self.ice = self.pits = self.switches = self.gates = self.exits = 0
        self.keys, self.doors = {}, {}
        players, unknown = [], []
        for r, row in enumerate(rows):
            for c in range(self.w):
                ch = row[c] if c < len(row) else " "
                pos = (r + 1) * W + c + 1
                if ch == "#":
                    continue
                self.wall[pos] = 0
                b = 1 << pos
                if ch in ".+*":
                    self.goals |= b
                if ch in "$*":
                    self.boxes |= b
                if ch in "@+":
                    players.append(pos)
                if ch == "~":
                    self.ice |= b
                elif ch in "abcde":
                    self.keys[pos] = "abcde".index(ch)
                elif ch in "ABCDE":
                    self.doors[pos] = "ABCDE".index(ch)
                elif ch == "O":
                    self.pits |= b
                elif ch == "!":
                    self.switches |= b
                elif ch == "|":
                    self.gates |= b
                elif ch == "X":
                    self.exits |= b
                elif ch not in " -_.+*$@":
                    unknown.append("%r at (%d,%d)" % (ch, c, r))
        if unknown:
            raise grid_lint.GridError("unknown glyph(s): " + ", ".join(unknown[:12]))
        if len(players) != 1:
            raise grid_lint.GridError("need exactly one player (@ or +), found %d" % len(players))
        self.player = players[0]
        self.forbidden = []
        self.warnings = []

    def cr(self, pos):
        return (pos % self.W - 1, pos // self.W - 1)

    def fmt(self, pos):
        return "(%d,%d)" % self.cr(pos)

    def pos_of(self, c, r):
        return (r + 1) * self.W + c + 1

    def apply_forbid(self, rule):
        if rule == "ice":
            self.ice = 0
        elif rule == "keys":
            for p in self.doors:
                self.wall[p] = 1
            self.doors, self.keys = {}, {}
        elif rule == "pits":
            for p in bits(self.pits):
                self.wall[p] = 1
            self.pits = 0
        elif rule == "switches":
            for p in bits(self.gates):
                self.wall[p] = 1
            self.gates = self.switches = 0
        elif rule == "push":
            for p in bits(self.boxes):
                self._freeze_box(p)
        elif rule.startswith("box:"):
            try:
                c, r = [int(x) for x in rule[4:].strip("()").split(",")]
            except ValueError:
                raise UsageError("bad --forbid %r (use box:C,R)" % rule)
            p = self.pos_of(c, r)
            if not (0 <= c < self.w and 0 <= r < self.h) or not (self.boxes >> p) & 1:
                raise UsageError("--forbid %s: no box at (%d,%d)" % (rule, c, r))
            self._freeze_box(p)
        else:
            raise UsageError("unknown --forbid rule %r (ice, keys, pits, switches, push, box:C,R)" % rule)
        self.forbidden.append(rule)

    def _freeze_box(self, p):
        self.boxes &= ~(1 << p)
        self.goals &= ~(1 << p)   # a frozen box on a goal keeps that goal satisfied
        self.wall[p] = 1

    def finalise(self):
        if self.gates and not self.switches:
            self.warnings.append("gates with no switches are always open")
            self.gates = 0
        if self.switches and not self.gates:
            self.switches = 0
        if not self.goals and not self.exits:
            raise grid_lint.GridError("no win condition: no goals (. + *) and no exit X")
        if self.goals and self.exits:
            self.warnings.append("level has goals, so the X exit is ignored (plain floor)")
            self.exits = 0
        nb, ng = popcount(self.boxes), popcount(self.goals)
        if ng > nb:
            self.warnings.append("%d goals but only %d boxes" % (ng, nb))

    def rules_present(self):
        out = []
        if self.boxes:
            out.append("push")
        if self.ice:
            out.append("ice")
        if self.keys or self.doors:
            out.append("keys")
        if self.pits:
            out.append("pits")
        if self.gates:
            out.append("switches")
        return out

    def needs_move_engine(self):
        return bool(self.ice or self.keys or self.doors or self.pits or self.gates)

    def push_distances(self, goals=None):
        """Push distance from each cell to the nearest goal (or the given goal mask),
        ignoring other boxes and treating every non-wall cell as floor (reverse 'pull' BFS)."""
        W, wall = self.W, self.wall
        dist = [INF] * self.N
        q = deque()
        for g in bits(self.goals if goals is None else goals):
            dist[g] = 0
            q.append(g)
        D = (-W, W, -1, 1)
        while q:
            y = q.popleft()
            for d in D:
                x = y - d          # box was at x, pushed in direction d onto y
                if wall[x] or wall[x - d] or dist[x] != INF:
                    continue
                dist[x] = dist[y] + 1
                q.append(x)
        return dist

    def walk(self, src, boxes):
        """Distances and parents for walking (no rules) from src."""
        W, wall = self.W, self.wall
        dist, par = {src: 0}, {src: None}
        q = deque([src])
        D = (-W, W, -1, 1)
        while q:
            c = q.popleft()
            for di, d in enumerate(D):
                n = c + d
                if wall[n] or (boxes >> n) & 1 or n in dist:
                    continue
                dist[n] = dist[c] + 1
                par[n] = (c, di)
                q.append(n)
        return dist, par


def walk_letters(par, dst):
    out = []
    while par[dst] is not None:
        c, di = par[dst]
        out.append(DIR_NAMES[di])
        dst = c
    return "".join(reversed(out))


# --------------------------------------------------------------------------- push model

class PushModel(object):
    """Push-level model: key = boxes << PB | min cell of the player's region."""
    name = "push-level A* (push-optimal; moves minimised among push-optimal solutions)"
    is_push_level = True

    def __init__(self, lv):
        self.lv = lv
        W = self.W = lv.W
        self.D = (-W, W, -1, 1)
        self.PB = lv.N.bit_length()
        self.PMASK = (1 << self.PB) - 1
        self.wall = lv.wall
        floor = 0
        for p in range(lv.N):
            if not lv.wall[p]:
                floor |= 1 << p
        self.floor = floor
        self.goals = lv.goals
        self.exits = lv.exits
        self.nboxes = popcount(lv.boxes)
        self.ngoals = popcount(lv.goals)
        self.prune = self.ngoals > 0 and self.nboxes == self.ngoals
        self.pdist = lv.push_distances() if self.goals else [INF] * lv.N
        self.dead = 0
        self.deadarr = bytearray(lv.N)
        if self.prune:
            for p in bits(floor):
                if self.pdist[p] == INF:
                    self.dead |= 1 << p
                    self.deadarr[p] = 1
        self.use_h = self.prune
        self.gdist = [lv.push_distances(1 << g) for g in bits(lv.goals)] if self.prune else []
        n = len(self.gdist)
        self.full = (1 << n) - 1
        self.hcache = {}
        self.masks_by_pc = [[m for m in range(1 << n) if popcount(m) == i] for i in range(n + 1)]
        self.free_js = [[j for j in range(n) if not (m >> j) & 1] for m in range(1 << n)]

    def match_cost(self, boxes):
        """Minimum-cost assignment of boxes to goals by push distance (INF = deadlock).
        Consistent: one push changes any box-goal distance by at most 1."""
        v = self.hcache.get(boxes)
        if v is not None:
            return v
        tables = self.gdist
        dp = [INF] * (self.full + 1)
        dp[0] = 0
        free_js = self.free_js
        for i, b in enumerate(bits(boxes)):
            row = [tab[b] for tab in tables]
            for mask in self.masks_by_pc[i]:
                val = dp[mask]
                if val == INF:
                    continue
                for j in free_js[mask]:
                    c = row[j]
                    if c != INF:
                        nm = mask | (1 << j)
                        if val + c < dp[nm]:
                            dp[nm] = val + c
        v = dp[self.full]
        if len(self.hcache) > 2000000:
            self.hcache.clear()
        self.hcache[boxes] = v
        return v

    def flood(self, seed, free):
        W = self.W
        r = seed
        while True:
            n = (r | (r << 1) | (r >> 1) | (r << W) | (r >> W)) & free
            if n == r:
                return r
            r = n

    def start(self):
        boxes = self.lv.boxes
        reg = self.flood(1 << self.lv.player, self.floor & ~boxes)
        npos = (reg & -reg).bit_length() - 1
        return (boxes << self.PB) | npos, reg

    def start_dead(self):
        boxes = self.lv.boxes
        if not self.prune:
            return False
        if boxes & self.dead or self.match_cost(boxes) == INF:
            return True
        return any(self._frozen_bad(b, boxes) for b in bits(boxes))

    def boxes_of(self, key):
        return key >> self.PB

    def h(self, key):
        if not self.use_h:
            return 0
        return self.match_cost(key >> self.PB)

    def is_win(self, key, reg):
        if self.goals:
            return ((key >> self.PB) & self.goals) == self.goals
        return bool(reg & self.exits)

    def _frozen(self, x, boxes, path):
        wall, dead, W = self.wall, self.deadarr, self.W
        path.add(x)
        try:
            for a, b in ((x - 1, x + 1), (x - W, x + W)):
                if wall[a] or wall[b] or (dead[a] and dead[b]):
                    continue
                blocked = False
                for n in (a, b):
                    if (boxes >> n) & 1 and (n in path or self._frozen(n, boxes, path)):
                        blocked = True
                        break
                if not blocked:
                    return False
            return True
        finally:
            path.discard(x)

    def _frozen_bad(self, x, boxes):
        return not (self.goals >> x) & 1 and self._frozen(x, boxes, set())

    def deadlocked(self, boxes, t):
        W = self.W
        for x in (t, t - 1, t + 1, t - W, t + W):
            if (boxes >> x) & 1 and self._frozen_bad(x, boxes):
                return True
        return False

    def successors(self, key, reg, include_dead=False):
        """Yield (child_key, child_region, edge, dead). edge = (dir, box_from, box_to)."""
        PB = self.PB
        boxes = key >> PB
        floor = self.floor
        free_box = floor & ~boxes
        if not include_dead:
            free_box &= ~self.dead
        out = []
        for di, d in enumerate(self.D):
            if d > 0:
                m = boxes & (reg << d) & (free_box >> d)
            else:
                m = boxes & (reg >> -d) & (free_box << -d)
            while m:
                low = m & -m
                m ^= low
                b = low.bit_length() - 1
                t = b + d
                nb = boxes ^ low ^ (1 << t)
                dead = False
                if self.prune and ((self.dead >> t) & 1 or self.deadlocked(nb, t)
                                   or self.match_cost(nb) == INF):
                    dead = True
                    if not include_dead:
                        continue
                creg = self.flood(low, floor & ~nb)
                npos = (creg & -creg).bit_length() - 1
                out.append(((nb << PB) | npos, creg, (di, b, t), dead))
        return out

    def describe_edge(self, edge):
        di, b, t = edge
        return "%s%s" % (self.lv.fmt(b), DIR_NAMES[di].upper())


# --------------------------------------------------------------------------- move model

class MoveModel(object):
    """Move-level model with every rule. State = (player, boxes, held, taken, opened, filled)."""
    name = "move-level BFS (move-optimal)"
    is_push_level = False

    def __init__(self, lv):
        self.lv = lv
        W = self.W = lv.W
        self.D = (-W, W, -1, 1)
        self.wall = lv.wall
        self.goals, self.exits = lv.goals, lv.exits
        self.ice, self.pits = lv.ice, lv.pits
        self.switches, self.gates = lv.switches, lv.gates
        self.keymask = 0
        for p in lv.keys:
            self.keymask |= 1 << p
        self.doormask = 0
        for p in lv.doors:
            self.doormask |= 1 << p
        self.keyletter = lv.keys
        self.doorletter = lv.doors
        self.ngoals = popcount(lv.goals)
        self.nboxes = popcount(lv.boxes)
        self.pdist = lv.push_distances() if self.goals else [INF] * lv.N
        # Goal-dead squares on a relaxed map (ice, doors, gates, keys and pits all treated
        # as floor; only '#' blocks). Every real box move is also a legal relaxed push, so
        # a box on such a square can never reach a goal under any rule.
        self.goal_dead = 0
        for p in range(lv.N):
            if not lv.wall[p] and self.pdist[p] == INF:
                self.goal_dead |= 1 << p
        self.use_h = False

    def start(self):
        lv = self.lv
        return (lv.player, lv.boxes, 0, 0, 0, 0), None

    def start_dead(self):
        return self.dead_state(self.lv.boxes)

    def boxes_of(self, st):
        return st[1]

    def h(self, st):
        return 0

    def is_win(self, st, aux=None):
        if self.goals:
            return (st[1] & self.goals) == self.goals
        return bool((self.exits >> st[0]) & 1)

    def dead_state(self, boxes):
        if not self.goals:
            return False
        return popcount(boxes & ~self.goal_dead) < self.ngoals

    def _gate_open(self, boxes):
        return (boxes & self.switches) == self.switches

    def _box_can_enter(self, c, boxes_wo, opened, taken, gate_open):
        if self.wall[c] or (boxes_wo >> c) & 1:
            return False
        b = 1 << c
        if self.doormask & b and not opened & b:
            return False
        if self.keymask & b and not taken & b:
            return False
        if self.gates & b and not gate_open:
            return False
        return True

    def step(self, st, di):
        """Apply one move. Returns (new_state, events, box_from, box_to) or None if illegal.
        box_from = -1 for a walk; box_to = -1 if the box fell into a pit."""
        p, boxes, held, taken, opened, filled = st
        d = self.D[di]
        n = p + d
        ev = 0
        bf = bt = -1
        if self.wall[n]:
            return None
        if (boxes >> n) & 1:
            boxes_wo = boxes & ~(1 << n)
            gopen = self._gate_open(boxes_wo)
            t = n + d
            if not self._box_can_enter(t, boxes_wo, opened, taken, gopen):
                return None
            ev |= EV_PUSH
            bf = n
            while True:
                tb = 1 << t
                if self.gates & tb:
                    ev |= EV_SWITCH
                if self.pits & tb and not filled & tb:
                    filled |= tb
                    ev |= EV_PITS
                    t = -1
                    break
                if self.ice & tb:
                    ev |= EV_ICE
                    nt = t + d
                    if self._box_can_enter(nt, boxes_wo, opened, taken, gopen):
                        t = nt
                        continue
                break
            bt = t
            boxes = boxes_wo | (1 << t) if t >= 0 else boxes_wo
        # player enters n, then slides on ice
        gopen = self._gate_open(boxes)
        c = n
        first = True
        while True:
            if not first:
                nc = c + d
            else:
                nc = c
            if self.wall[nc] or (boxes >> nc) & 1:
                if first:
                    return None
                break
            b = 1 << nc
            if self.pits & b and not filled & b:
                if first:
                    return None
                break
            if self.gates & b and not gopen:
                if first:
                    return None
                break
            if self.doormask & b and not opened & b:
                L = self.doorletter[nc]
                if (held >> (4 * L)) & 15 == 0:
                    if first:
                        return None
                    break
                held -= 1 << (4 * L)
                opened |= b
                ev |= EV_KEYS
            if self.keymask & b and not taken & b:
                taken |= b
                held += 1 << (4 * self.keyletter[nc])
            if self.gates & b:
                ev |= EV_SWITCH
            if not first:
                ev |= EV_PSLIDE
            c = nc
            first = False
            if self.ice & b:
                ev |= EV_ICE
                continue
            break
        return (c, boxes, held, taken, opened, filled), ev, bf, bt

    def successors(self, st, aux=None, include_dead=False):
        out = []
        for di in range(4):
            r = self.step(st, di)
            if r is None:
                continue
            nst, ev, bf, bt = r
            dead = bool(ev & EV_PUSH) and self.dead_state(nst[1])
            if dead and not include_dead:
                continue
            out.append((nst, None, (di, bf, bt), dead))
        return out


# --------------------------------------------------------------------------- searches

def search(model, budget, want_dag=True, dag_extra=5000):
    """A* (h=0 -> uniform-cost BFS). Returns dict with best cost, goal keys, node info.

    info[key] = (g, parent_key, edge); extra[key] = further equal-g parents.
    After the first goal, keeps expanding nodes with f == best to collect every
    optimal solution (for moves minimisation, classes and metrics); that phase is
    capped at the expansions the first phase used (min dag_extra) and the time cap.
    """
    skey, saux = model.start()
    res = {"status": None, "expanded": 0, "best": None, "goals": [], "start": skey,
           "info": {skey: (0, None, None)}, "extra": {}, "dag_complete": True}
    if model.start_dead():
        res["status"] = "unsolvable"
        res["start_dead"] = True
        return res
    info, extra = res["info"], res["extra"]
    heap = [(model.h(skey), 0, skey, saux)]
    closed = set()
    best = None
    expanded = 0
    limit = budget.max_nodes
    while heap:
        f, ng, key, aux = heapq.heappop(heap)
        if best is not None and f > best:
            break
        if key in closed:
            continue
        closed.add(key)
        gk = -ng
        if model.is_win(key, aux):
            if best is None:
                best = gk
                limit = min(budget.max_nodes, expanded + max(dag_extra, expanded))
            res["goals"].append(key)
            if not want_dag:
                break
            continue
        expanded += 1
        if expanded > limit or (expanded & 63 == 0 and budget.out_of_time()):
            if best is None:
                res["status"] = "unknown"
                res["cap_reason"] = "node cap" if expanded > limit else "time cap"
            else:
                res["dag_complete"] = False
            break
        cg = gk + 1
        for ckey, caux, edge, _dead in model.successors(key, aux):
            old = info.get(ckey)
            if old is None or cg < old[0]:
                info[ckey] = (cg, key, edge)
                if old is not None:
                    extra.pop(ckey, None)
                heapq.heappush(heap, (cg + model.h(ckey), -cg, ckey, caux))
            elif cg == old[0]:
                extra.setdefault(ckey, []).append((key, edge))
    del closed, heap
    res["expanded"] = expanded
    res["best"] = best
    if res["status"] is None:
        res["status"] = "solvable" if best is not None else "unsolvable"
    return res


def build_dag(res):
    """Nodes on optimal paths: {key: g} and children lists {key: [(child, edge)]}."""
    info, extra = res["info"], res["extra"]
    nodes = set(res["goals"])
    stack = list(res["goals"])
    children = {}
    while stack:
        k = stack.pop()
        plist = []
        if info[k][1] is not None:
            plist.append(info[k][1:])
        plist.extend(extra.get(k, ()))
        for pk, e in plist:
            children.setdefault(pk, []).append((k, e))
            if pk not in nodes:
                nodes.add(pk)
                stack.append(pk)
    order = sorted(nodes, key=lambda k: info[k][0])
    return order, children


def first_path(res, key):
    edges = []
    while res["info"][key][1] is not None:
        _g, pk, e = res["info"][key]
        edges.append(e)
        key = pk
    return list(reversed(edges))


def push_moves_dp(model, res, order, children, budget):
    """Push model: among push-optimal solutions find fewest moves. Returns (moves, solution)."""
    lv = model.lv
    PB = model.PB
    start = res["start"]
    goalset = set(res["goals"])
    best = {(start, lv.player): (0, None)}
    info = res["info"]
    by_layer = {}
    for k in order:
        by_layer.setdefault(info[k][0], []).append(k)
    entries = {start: [lv.player]}
    final = None
    for gl in sorted(by_layer):
        for k in by_layer[gl]:
            if budget.out_of_time():
                return None, None
            for ppos in entries.get(k, ()):
                moves, _ = best[(k, ppos)]
                boxes = k >> PB
                dist, _par = lv.walk(ppos, boxes)
                if k in goalset:
                    extra_m = 0
                    if not model.goals:
                        extra_m = min((dist[x] for x in bits(model.exits) if x in dist), default=None)
                        if extra_m is None:
                            continue
                    tot = moves + extra_m
                    if final is None or tot < final[0]:
                        final = (tot, k, ppos)
                    continue
                for ck, (di, b, t) in children.get(k, ()):
                    src = b - model.D[di]
                    if src not in dist:
                        continue
                    cand = moves + dist[src] + 1
                    ek = (ck, b)
                    if ek not in best or cand < best[ek][0]:
                        if ek not in best:
                            entries.setdefault(ck, []).append(b)
                        best[ek] = (cand, (k, ppos, (di, b, t)))
    if final is None:
        return None, None
    # reconstruct
    tot, k, ppos = final
    pushes = []
    cur = (k, ppos)
    while best[cur][1] is not None:
        pk, pp, e = best[cur][1]
        pushes.append(e)
        cur = (pk, pp)
    pushes.reverse()
    return tot, pushes_to_moves(model, pushes)


def pushes_to_moves(model, pushes):
    """Turn a push list [(dir, box_from, box_to)] into a move string (push model)."""
    lv = model.lv
    boxes = lv.boxes
    p = lv.player
    out = []
    for di, b, t in pushes:
        src = b - model.D[di]
        dist, par = lv.walk(p, boxes)
        if src not in dist:
            raise RuntimeError("internal: push not reachable")
        out.append(walk_letters(par, src))
        out.append(DIR_NAMES[di].upper())
        boxes = boxes ^ (1 << b) ^ (1 << t)
        p = b
    if not model.goals:
        dist, par = lv.walk(p, boxes)
        ex = [x for x in bits(model.exits) if x in dist]
        if ex:
            out.append(walk_letters(par, min(ex, key=lambda x: dist[x])))
    return "".join(out)


def replay(lv, moves):
    """Simulate a move string with the full rule set. Returns dict."""
    mm = MoveModel(lv)
    st, _ = mm.start()
    rules = 0
    pushes = 0
    case_notes = []
    solved_at = None
    if mm.is_win(st):
        solved_at = 0
    for i, ch in enumerate(moves):
        di = DIR_NAMES.find(ch.lower())
        r = mm.step(st, di)
        if r is None:
            return {"legal": False, "illegal_at": i, "move": ch, "state": st, "pushes": pushes,
                    "rules": rules, "solved_at": solved_at, "case_notes": case_notes, "model": mm}
        st, ev, bf, bt = r
        rules |= ev
        if ev & EV_PUSH:
            pushes += 1
            if ch.islower():
                case_notes.append(i)
        elif ch.isupper():
            case_notes.append(i)
        if solved_at is None and mm.is_win(st):
            solved_at = i + 1
    return {"legal": True, "illegal_at": None, "state": st, "pushes": pushes, "rules": rules,
            "solved_at": solved_at, "case_notes": case_notes, "model": mm}


def rules_from_mask(mask):
    return [name for name, bit in RULE_EVENTS if mask & bit]


# --------------------------------------------------------------------------- metrics

def explore(model, budget):
    """Full forward exploration (BFS) storing edges in flat arrays.

    Edges of node s are e in range(offs[s], offs[s+1]); edge e is
    ebuf[4*e : 4*e+4] = (child index or -1 if deadlocked, dir, box_from, box_to)."""
    skey, saux = model.start()
    index = {skey: 0}
    keys = [skey]
    auxs = [saux]
    ebuf = array("i")
    offs = array("i", [0])
    win = bytearray()
    deadkeys = set()
    i = 0
    complete = True
    while i < len(keys):
        if i > budget.max_nodes or (i & 255 == 0 and budget.out_of_time()):
            complete = False
            break
        key, aux = keys[i], auxs[i]
        auxs[i] = None
        w = model.is_win(key, aux)
        win.append(1 if w else 0)
        if not w:
            for ckey, caux, (di, bf, bt), dead in model.successors(key, aux, include_dead=True):
                if dead:
                    deadkeys.add(ckey)
                    ebuf.extend((-1, di, bf, bt))
                    continue
                ci = index.get(ckey)
                if ci is None:
                    ci = len(keys)
                    index[ckey] = ci
                    keys.append(ckey)
                    auxs.append(caux)
                ebuf.extend((ci, di, bf, bt))
        offs.append(len(ebuf) // 4)
        i += 1
    if not complete:
        return {"complete": False, "states": len(keys)}
    del auxs, index
    n = len(keys)
    # reverse reachability to wins (reverse CSR)
    indeg = array("i", [0]) * (n + 1)
    for e in range(0, len(ebuf), 4):
        ci = ebuf[e]
        if ci >= 0:
            indeg[ci + 1] += 1
    for k in range(n):
        indeg[k + 1] += indeg[k]
    rsrc = array("i", [0]) * indeg[n]
    fill = array("i", indeg)
    for s_ in range(n):
        for e in range(offs[s_], offs[s_ + 1]):
            ci = ebuf[4 * e]
            if ci >= 0:
                rsrc[fill[ci]] = s_
                fill[ci] += 1
    alive = bytearray(n)
    stack = [s_ for s_ in range(n) if win[s_]]
    for s_ in stack:
        alive[s_] = 1
    while stack:
        t = stack.pop()
        for j in range(indeg[t], indeg[t + 1]):
            s_ = rsrc[j]
            if not alive[s_]:
                alive[s_] = 1
                stack.append(s_)
    return {"complete": True, "keys": keys, "ebuf": ebuf, "offs": offs, "win": win, "alive": alive,
            "deadkeys": deadkeys, "states": n}


def edges_of(ex, s):
    ebuf = ex["ebuf"]
    for e in range(ex["offs"][s], ex["offs"][s + 1]):
        yield ebuf[4 * e], ebuf[4 * e + 1], ebuf[4 * e + 2], ebuf[4 * e + 3]


def box_changes_all(ex, budget):
    """0-1 BFS over (state, last pushed box position). Returns min changes or None."""
    win = ex["win"]
    start = (0, -1)
    dist = {start: 0}
    dq = deque([start])
    popped = 0
    while dq:
        node = dq.popleft()
        s, last = node
        c = dist[node]
        popped += 1
        if popped > budget.max_nodes or (popped & 1023 == 0 and budget.out_of_time()):
            return None
        if win[s]:
            return c
        for ci, _di, bf, bt in edges_of(ex, s):
            if ci < 0:
                continue
            if bf < 0:
                nn, w = (ci, last), 0
            else:
                w = 0 if (last == -1 or bf == last) else 1
                nn = (ci, bt if bt >= 0 else -2)
            nc = c + w
            if nc < dist.get(nn, INF):
                dist[nn] = nc
                if w == 0:
                    dq.appendleft(nn)
                else:
                    dq.append(nn)
    return None


def dag_box_changes(order, children, start):
    best = {(start, -1): 0}
    out = INF
    childset = children
    pending = {start: {-1: 0}}
    for k in order:
        lasts = pending.get(k)
        if not lasts:
            continue
        kids = childset.get(k)
        if not kids:
            out = min(out, min(lasts.values()))
            continue
        for last, c in lasts.items():
            for ck, (_di, bf, bt) in kids:
                if bf < 0:
                    nl, w = last, 0
                else:
                    w = 0 if (last == -1 or bf == last) else 1
                    nl = bt if bt >= 0 else -2
                d = pending.setdefault(ck, {})
                if c + w < d.get(nl, INF):
                    d[nl] = c + w
    del best
    return None if out == INF else out


def dag_counter_intuitive(model, order, children, start):
    pd = model.pdist
    ci = {start: 0}
    goals_min = INF
    for k in order:
        if k not in ci:
            continue
        kids = children.get(k)
        if not kids:
            goals_min = min(goals_min, ci[k])
            continue
        for ck, (_di, bf, bt) in kids:
            inc = 1 if (bf >= 0 and bt >= 0 and pd[bt] > pd[bf] and pd[bt] != INF) else 0
            v = ci[k] + inc
            if v < ci.get(ck, INF):
                ci[ck] = v
    return None if goals_min == INF else goals_min


def first_move_traps(model, ex):
    """Pushes available before any push is made; trap = leads to a dead state."""
    alive = ex["alive"]
    seen = {0}
    stack = [0]
    traps, total = 0, 0
    pushed = set()
    examples = []
    while stack:
        s = stack.pop()
        for ci, di, bf, bt in edges_of(ex, s):
            if bf < 0:
                if ci >= 0 and ci not in seen:
                    seen.add(ci)
                    stack.append(ci)
                continue
            sig = (bf, di, ci)
            if sig in pushed:
                continue
            pushed.add(sig)
            total += 1
            if ci < 0 or not alive[ci]:
                traps += 1
                if len(examples) < 6:
                    examples.append(model.lv.fmt(bf) + DIR_NAMES[di].upper())
    return traps, total, examples


# --------------------------------------------------------------------------- classes

def count_classes(model, res, order, children, budget):
    """Distinct optimal solutions up to interleaving of different boxes' pushes."""
    lv = model.lv
    start = res["start"]
    goalset = set(res["goals"])
    box_ids = tuple(sorted((p, i) for i, p in enumerate(bits(lv.boxes))))
    nb = len(box_ids)
    init = (box_ids, tuple(() for _ in range(nb)), frozenset(), ())
    sigs = {start: {init: None}}
    total = 1
    capped = False
    classes = {}
    for k in order:
        here = sigs.pop(k, None)
        if not here:
            continue
        if k in goalset:
            for sig, back in here.items():
                ck = sig[1:]
                if ck not in classes:
                    classes[ck] = (k, sig, back)
                    if len(classes) >= CLASS_CAP:
                        capped = True
            if capped:
                break
            continue
        if budget.out_of_time():
            capped = True
            break
        for ck, edge in children.get(k, ()):
            di, bf, bt = edge
            evkey = None
            if not model.is_push_level:
                st2, ev, _bf, _bt = model.step(k, di)
                evs = set()
                for idx, (a, b2) in enumerate(zip(k[3:], ck[3:])):
                    for pos in bits(a ^ b2):
                        evs.add(("key", "door", "pit")[idx] + lv.fmt(pos))
                slide = (lv.fmt(k[0]) + DIR_NAMES[di]) if ev & EV_PSLIDE and bf < 0 else None
                evkey = (evs, slide)
            dest = sigs.setdefault(ck, {})
            for sig, _back in here.items():
                ids, trajs, events, slides = sig
                if bf >= 0:
                    idmap = dict(ids)
                    bid = idmap.pop(bf)
                    if bt >= 0:
                        idmap[bt] = bid
                    ids2 = tuple(sorted(idmap.items()))
                    tl = list(trajs)
                    tl[bid] = tl[bid] + ((bf, di),)
                    trajs2 = tuple(tl)
                else:
                    ids2, trajs2 = ids, trajs
                events2, slides2 = events, slides
                if evkey is not None:
                    if evkey[0]:
                        events2 = events | frozenset(evkey[0])
                    if evkey[1]:
                        slides2 = slides + (evkey[1],)
                nsig = (ids2, trajs2, events2, slides2)
                if nsig not in dest:
                    dest[nsig] = (k, sig, edge)
                    total += 1
                    if total > SIG_CAP:
                        capped = True
                        break
            if capped:
                break
        if capped:
            break
    # examples: reconstruct a path per class (first 5)
    examples = []
    for ck, (k, sig, back) in list(classes.items())[:5]:
        if model.is_push_level:
            parts = []
            for bid, traj in enumerate(sig[1]):
                if traj:
                    parts.append(" ".join(lv.fmt(p) + DIR_NAMES[d].upper() for p, d in traj))
            examples.append("; ".join(parts))
        else:
            parts = []
            for traj in sig[1]:
                if traj:
                    parts.append(" ".join(lv.fmt(p) + DIR_NAMES[d].upper() for p, d in traj))
            ev = sorted(sig[2])
            if ev:
                parts.append("events " + " ".join(ev))
            if sig[3]:
                parts.append("slides " + " ".join(sig[3]))
            examples.append("; ".join(parts) if parts else "(walk only)")
    count = len(classes) if (classes or not capped) else None
    return {"count": count, "capped": capped, "examples": examples}


# --------------------------------------------------------------------------- main analysis

def analyse(rows, forbid=(), max_nodes=2000000, max_seconds=60.0, intended=None,
            metrics=False, classes=False):
    lv = Level(rows)
    for f in forbid:
        lv.apply_forbid(f)
    lv.finalise()
    budget = Budget(max_nodes, max_seconds)
    model = MoveModel(lv) if lv.needs_move_engine() else PushModel(lv)
    out = {"result": None, "engine": model.name, "size": [lv.w, lv.h],
           "boxes": popcount(lv.boxes), "goals": popcount(lv.goals),
           "rules_detected": lv.rules_present(), "rules_forbidden": list(lv.forbidden),
           "rules_used": [], "pushes": None, "moves": None, "solution": None,
           "nodes_expanded": 0, "seconds": None, "cap_reason": None,
           "warnings": list(lv.warnings), "not_modelled": NOT_MODELLED}
    full_dag = metrics or classes
    res = search(model, budget, want_dag=True,
                 dag_extra=budget.max_nodes if full_dag else 5000)
    out["nodes_expanded"] = res["expanded"]
    out["result"] = res["status"]
    if res.get("start_dead"):
        out["warnings"].append("the start position is already deadlocked (a box is on a dead square or frozen off a goal)")
    if res["status"] == "unknown":
        out["cap_reason"] = res.get("cap_reason")
    order = children = None
    if res["status"] == "solvable":
        order, children = build_dag(res)
        if model.is_push_level:
            moves, sol = push_moves_dp(model, res, order, children, budget)
            if sol is None:
                sol = pushes_to_moves(model, first_path(res, res["goals"][0]))
                moves = len(sol)
                res["dag_complete"] = False
        else:
            path = first_path(res, res["goals"][0])
            sol = "".join(DIR_NAMES[di].upper() if bf >= 0 else DIR_NAMES[di] for di, bf, _bt in path)
            moves = len(sol)
        rp = replay(lv, sol)
        if not rp["legal"] or rp["solved_at"] != len(sol):
            out["warnings"].append("internal check: solution replay failed")
        out["solution"] = sol
        out["moves"] = moves
        out["pushes"] = rp["pushes"]
        out["rules_used"] = rules_from_mask(rp["rules"])
        if not res["dag_complete"]:
            out["warnings"].append("stopped collecting optimal solutions early (%s): moves are the fewest among the "
                                   "push-optimal solutions found, not necessarily all of them%s"
                                   % ("time cap" if budget.out_of_time() else "collection limit; --classes or "
                                      "--metrics collects all", "; classes/optimal-path metrics are partial"
                                      if full_dag else ""))
        if model.is_push_level:
            out["optimality"] = "pushes optimal; moves fewest among push-optimal solutions"
        else:
            out["optimality"] = "moves optimal"
    # intended
    if intended is not None:
        out["intended"] = check_intended(lv, model, intended, out)
    if classes:
        if res["status"] == "solvable":
            if res["dag_complete"]:
                out["classes"] = count_classes(model, res, order, children, budget)
            else:
                out["classes"] = {"count": None, "capped": True, "examples": [],
                                  "note": "optimal-solution graph incomplete (cap)"}
        else:
            out["classes"] = {"count": 0 if res["status"] == "unsolvable" else None,
                              "capped": res["status"] == "unknown", "examples": []}
    if metrics:
        out["metrics"] = compute_metrics(model, res, order, children, budget, out)
    out["seconds"] = round(budget.elapsed(), 3)
    return out


def check_intended(lv, model, text, out):
    moves = "".join(ch for ch in text if not ch.isspace() and ch not in ",;")
    bad = [ch for ch in moves if ch.lower() not in DIR_NAMES]
    if bad:
        raise UsageError("--intended may contain only u d l r (any case); found %r" % "".join(sorted(set(bad))))
    rp = replay(lv, moves)
    info = {"moves_given": len(moves), "legal": rp["legal"], "solves": False, "shortcut": None,
            "notes": []}
    if not rp["legal"]:
        st = rp["state"]
        info["notes"].append("move %d (%r) is illegal; player at %s"
                             % (rp["illegal_at"] + 1, rp["move"], lv.fmt(st[0])))
        return info
    if rp["solved_at"] is None:
        info["notes"].append("the intended moves are legal but do not solve the level")
        return info
    info["solves"] = True
    used = moves[:rp["solved_at"]]
    if rp["solved_at"] < len(moves):
        info["notes"].append("solved after move %d; %d trailing move(s) ignored" % (rp["solved_at"], len(moves) - rp["solved_at"]))
    rp2 = replay(lv, used)
    info["moves"] = len(used)
    info["pushes"] = rp2["pushes"]
    info["rules_used"] = rules_from_mask(rp2["rules"])
    if rp2["case_notes"]:
        info["notes"].append("letter case does not match push/walk at move(s) %s (accepted)"
                             % ",".join(str(i + 1) for i in rp2["case_notes"][:10]))
    if out["result"] != "solvable":
        info["shortcut"] = None
        info["notes"].append("optimum unknown (search capped); shortcut check not possible")
        return info
    if model.is_push_level:
        diff = info["pushes"] - out["pushes"]
        info["shortcut"] = diff > 0
        info["shorter_by_pushes"] = max(0, diff)
        info["shorter_by_moves"] = max(0, info["moves"] - out["moves"])
        if diff <= 0 and info["moves"] > out["moves"]:
            info["notes"].append("same pushes, %d fewer moves possible (walking only, not a shortcut)"
                                 % (info["moves"] - out["moves"]))
    else:
        diff = info["moves"] - out["moves"]
        info["shortcut"] = diff > 0
        info["shorter_by_moves"] = max(0, diff)
        info["shorter_by_pushes"] = max(0, info["pushes"] - out["pushes"])
        if diff > 0:
            info["shortcut_kind"] = ("fewer pushes" if out["pushes"] < info["pushes"] else
                                     "same or more pushes, fewer moves")
    return info


def compute_metrics(model, res, order, children, budget, out):
    m = {"note": "Jarusek & Pelanek proxies; use to order levels, not as absolute difficulty"}
    lv = model.lv
    m["moves_per_cell"] = round(out["moves"] / float(lv.w * lv.h), 3) if out["moves"] is not None else None
    off_goal = popcount(lv.boxes & ~lv.goals)
    if res["status"] == "solvable" and res["dag_complete"] and lv.goals:
        m["counter_intuitive_pushes"] = dag_counter_intuitive(model, order, children, res["start"])
    else:
        m["counter_intuitive_pushes"] = None
    ex = explore(model, Budget(budget.max_nodes, max(0.0, budget.deadline - time.time())))
    m["states_explored"] = ex["states"]
    m["complete"] = ex["complete"]
    bc = None
    scope = None
    if ex["complete"]:
        n = ex["states"] + len(ex["deadkeys"])
        dead = ex["states"] - sum(ex["alive"]) + len(ex["deadkeys"])
        m["dead_end_ratio"] = round(dead / float(n), 3) if n else 0.0
        m["dead_end_ratio_note"] = "undo need, not difficulty"
        if lv.boxes:
            t, tot, exs = first_move_traps(model, ex)
            m["first_move_traps"] = {"traps": t, "first_pushes": tot,
                                     "fraction": round(t / float(tot), 3) if tot else 0.0,
                                     "trap_pushes": exs}
        if res["status"] == "solvable" and lv.boxes:
            bc = box_changes_all(ex, budget)
            if bc is not None:
                scope = "minimum over all solutions"
    else:
        m["dead_end_ratio"] = None
        m["first_move_traps"] = None
        m["incomplete_note"] = "state space exceeded the cap; dead_end_ratio and first_move_traps unavailable"
    if bc is None and res["status"] == "solvable" and res["dag_complete"] and lv.boxes:
        bc = dag_box_changes(order, children, res["start"])
        scope = "minimum over optimal solutions only (upper bound)"
    m["box_changes"] = bc
    m["box_changes_scope"] = scope
    if bc is not None:
        m["entanglement_excess"] = max(0, bc - (max(off_goal, 1) - 1))
        m["entanglement_basis"] = "boxes starting off a goal = %d" % off_goal
    else:
        m["entanglement_excess"] = None
    return m


# --------------------------------------------------------------------------- output

def format_summary(out):
    lines = []
    res = out["result"]
    lines.append("grid_puzzle_solve: %s" % res.upper())
    lines.append("  engine: %s" % out["engine"])
    lines.append("  size %dx%d, boxes %d, goals %d" % (out["size"][0], out["size"][1], out["boxes"], out["goals"]))
    lines.append("  rules detected: %s; forbidden: %s; used in solution: %s" % (
        ", ".join(out["rules_detected"]) or "none", ", ".join(out["rules_forbidden"]) or "none",
        ", ".join(out["rules_used"]) or ("none" if res == "solvable" else "-")))
    if res == "solvable":
        lines.append("  pushes %d, moves %d (%s)" % (out["pushes"], out["moves"], out["optimality"]))
        lines.append("  solution: %s" % (out["solution"] or "(already solved)"))
    if res == "unknown":
        lines.append("  search stopped at the %s - shrink the level, add walls, or raise --max-nodes/--max-seconds"
                     % out["cap_reason"])
    lines.append("  nodes expanded %d, %.2f s" % (out["nodes_expanded"], out["seconds"]))
    it = out.get("intended")
    if it is not None:
        if not it["legal"] or not it["solves"]:
            lines.append("  intended: FAIL - " + "; ".join(it["notes"]))
        else:
            s = "  intended: legal, solves in %d moves / %d pushes" % (it["moves"], it["pushes"])
            if it["shortcut"]:
                s += "; SHORTCUT: optimum is %d pushes / %d moves (shorter by %d pushes, %d moves)" % (
                    out["pushes"], out["moves"], it.get("shorter_by_pushes", 0), it.get("shorter_by_moves", 0))
            elif it["shortcut"] is False:
                s += "; no shorter solution"
            lines.append(s)
            for n in it["notes"]:
                lines.append("    note: " + n)
    m = out.get("metrics")
    if m is not None:
        lines.append("  metrics (Jarusek & Pelanek proxies, for ordering levels):")
        lines.append("    counter-intuitive pushes: %s" % _s(m.get("counter_intuitive_pushes")))
        lines.append("    box changes: %s (%s); entanglement excess: %s%s" % (
            _s(m.get("box_changes")), m.get("box_changes_scope") or "n/a", _s(m.get("entanglement_excess")),
            (" [" + m["entanglement_basis"] + "]") if m.get("entanglement_basis") else ""))
        fm = m.get("first_move_traps")
        if fm:
            lines.append("    first-move traps: %d of %d first pushes%s" % (
                fm["traps"], fm["first_pushes"], (" (" + " ".join(fm["trap_pushes"]) + ")") if fm["trap_pushes"] else ""))
        else:
            lines.append("    first-move traps: n/a")
        lines.append("    dead-end ratio: %s (undo need, not difficulty); states explored %d%s" % (
            _s(m.get("dead_end_ratio")), m["states_explored"], "" if m["complete"] else " (capped)"))
        lines.append("    moves per cell: %s" % _s(m.get("moves_per_cell")))
    c = out.get("classes")
    if c is not None:
        lines.append("  solution classes (up to reordering): %s%s" % (
            _s(c["count"]), " (capped, at least this many)" if c["capped"] and c["count"] else ""))
        for i, e in enumerate(c.get("examples", [])):
            lines.append("    class %d: %s" % (i + 1, e))
    for w in out["warnings"]:
        lines.append("  warning: " + w)
    lines.append(out["not_modelled"])
    return "\n".join(lines)


def _s(v):
    return "n/a" if v is None else str(v)


def exit_code(out):
    if out["result"] == "unknown":
        return 3
    if out["result"] == "unsolvable":
        return 1
    it = out.get("intended")
    if it is not None:
        if not it["legal"] or not it["solves"]:
            return 1
        if it["shortcut"] is None:
            return 3
        if it["shortcut"]:
            return 1
    return 0


def build_parser():
    p = argparse.ArgumentParser(
        prog="grid_puzzle_solve.py",
        description=__doc__.split("\n\n", 1)[1],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", help="level file in the puzzle legend; '-' for stdin")
    p.add_argument("--max-nodes", type=int, default=2000000, help="node cap per search pass (default 2000000)")
    p.add_argument("--max-seconds", type=float, default=60.0, help="wall-clock cap (default 60)")
    p.add_argument("--forbid", action="append", default=[], metavar="RULE",
                   help="ice | keys | pits | switches | push | box:C,R (repeatable)")
    p.add_argument("--intended", metavar="MOVES", help="intended solution, e.g. rruLLd (uppercase = push)")
    p.add_argument("--metrics", action="store_true", help="Jarusek & Pelanek difficulty proxies")
    p.add_argument("--classes", action="store_true", help="count optimal solution classes up to reordering")
    p.add_argument("--json", action="store_true", help="JSON output")
    return p


def main(argv=None):
    p = build_parser()
    try:
        args = p.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    try:
        if args.max_nodes < 1 or args.max_seconds <= 0:
            raise UsageError("--max-nodes and --max-seconds must be positive")
        text = grid_lint.read_text(args.file)
        rows, _meta = grid_lint.extract_grid(text, grid_lint.PUZZLE_GLYPHS)
        out = analyse(rows, args.forbid, args.max_nodes, args.max_seconds, args.intended,
                      args.metrics, args.classes)
    except (grid_lint.GridError, UsageError) as exc:
        if args.json:
            print(json.dumps({"result": "error", "error": str(exc), "not_modelled": NOT_MODELLED}))
        else:
            print("grid_puzzle_solve: error: %s" % exc)
            print(NOT_MODELLED)
        return 2
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(format_summary(out))
    return exit_code(out)


if __name__ == "__main__":
    sys.exit(main())
