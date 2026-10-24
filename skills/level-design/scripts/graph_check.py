#!/usr/bin/env python3
"""graph_check.py - lock-and-key / hub / dungeon graph soundness check.

Usage:
  python3 -I scripts/graph_check.py FILE [--format json|mermaid] [--json]

FILE is UTF-8 text ('-' = stdin). Format is auto-detected (JSON if it starts with '{'),
or forced with --format. A markdown file with a ```mermaid block uses the first such block.

JSON input:
  {"start": "A", "goal": "Z", "hub": "A",            (hub optional, defaults to start)
   "nodes": [{"id": "A", "items": ["red_key"], "label": "Hall"}],
   "edges": [{"from": "A", "to": "B", "requires": ["red_key"], "oneway": false,
              "consumes": false}]}
  Edges are two-way unless "oneway": true. "requires" lists items needed to pass (repeat a
  name to need two). "consumes": true spends one of each required item the first time the
  edge is passed; the door then stays open in both directions.

Mermaid flowchart subset (one statement per line; chains like A --> B --> C allowed):
  A["Hall {item:red_key}"]      node with a label; {item:x} / {items:x,y} put items in the node,
                                {start} {goal} {hub} tag it; any other text (e.g. "F2") is label
  A -->|req:red_key| B          passage (two-way); label tokens are comma-separated:
                                req:x (req:x+y for several), consumes, oneway
  A -.->|oneway| B              dotted arrow = one-way A to B (also any label containing
                                one-way / oneway / drop / the arrow glyph); quotes are stripped
  A <--> B, A --- B, A ==> B    two-way passages
  A -. vista .- B, A -.- B      dotted link without arrowhead = sightline: NOT traversable
                                (reported as a vista); a label containing "vista" is the same
  A -- text --> B               text-on-link form is accepted (text is parsed like a label)
  %% start: A   %% goal: Z      set start/goal (else {start}/{goal} tags, else nodes named
                                start/goal, else start = first node)
  Ignored: flowchart/graph header, classDef, class, style, linkStyle, click, direction,
  subgraph/end, other %% comments, trailing ';'. '&' fan-out is not supported.

Model: the player walks the graph from start; entering a node picks up all its items; an
edge opens when the held items satisfy "requires". Exhaustive search over (position, items
collected, consumed doors opened), capped at 500,000 states (exit 3 when hit).

Reports: goal reachable; reachable % of nodes; unreachable nodes; required items that are
never obtainable (missing or unreachable); gates that never open; key-before-door order (the
event sequence of a shortest winning route: items gained, gates opened); softlocks (reachable
states from which the goal can no longer be reached) with the fatal move, classified as
consumed-key softlocks (a key spent on one door leaves another required door locked) or
one-way traps; dead-end nodes (one neighbour, not start/goal) with/without items; junctions
(3+ neighbours); loop count (independent cycles = E - V + components of the undirected
passage graph); one-way edges with no return path to the hub.

Exit codes: 0 pass; 1 a check failed (goal unreachable, unreachable nodes, unobtainable
required items, gates that never open, softlocks); 2 usage/parse error; 3 state cap hit.
Dead ends, junctions, loops and one-way-without-return are informational warnings.
"""

import argparse
import json
import re
import sys
from collections import deque

STATE_CAP = 500000
NOT_MODELLED = ("Not modelled: distances, travel time and backtracking cost, combat/difficulty, "
                "enemies and timed doors, player choice to skip item pickups (entering a node "
                "takes its items), items lost on death, abilities beyond named items, sequence "
                "breaks that are not drawn as edges, sightlines (vistas are listed only).")


class InputError(Exception):
    pass


class CapHit(Exception):
    pass


def read_text(path):
    if path == "-":
        return sys.stdin.read()
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        raise InputError("cannot read %s: %s" % (path, e))


class Graph:
    def __init__(self):
        self.nodes = {}      # id -> {"label", "items": [], "tags": set()}
        self.order = []
        self.edges = []      # dicts: from,to,requires,oneway,consumes
        self.vistas = []
        self.start = None
        self.goal = None
        self.hub = None
        self.warnings = []

    def add_node(self, nid, label=None, items=(), tags=()):
        if nid not in self.nodes:
            self.nodes[nid] = {"label": label or nid, "items": [], "tags": set()}
            self.order.append(nid)
        n = self.nodes[nid]
        if label:
            n["label"] = label
        n["items"].extend(items)
        n["tags"].update(tags)


# ----------------------------------------------------------------------------- JSON

def parse_json(text):
    try:
        d = json.loads(text)
    except ValueError as e:
        raise InputError("invalid JSON: %s" % e)
    if not isinstance(d, dict) or not isinstance(d.get("edges", []), list):
        raise InputError("JSON must be an object with 'nodes' and 'edges' lists")
    g = Graph()
    for n in d.get("nodes", []):
        if not isinstance(n, dict) or "id" not in n:
            raise InputError("every node needs an 'id'")
        items = n.get("items", []) or []
        if isinstance(items, str):
            items = [items]
        g.add_node(str(n["id"]), n.get("label"), [str(i) for i in items])
    for e in d.get("edges", []):
        if not isinstance(e, dict) or "from" not in e or "to" not in e:
            raise InputError("every edge needs 'from' and 'to'")
        a, b = str(e["from"]), str(e["to"])
        for x in (a, b):
            if x not in g.nodes:
                g.add_node(x)
        req = e.get("requires", []) or []
        if isinstance(req, str):
            req = [req]
        g.edges.append({"from": a, "to": b, "requires": [str(r) for r in req],
                        "oneway": bool(e.get("oneway", False)),
                        "consumes": bool(e.get("consumes", False))})
    g.start = str(d["start"]) if d.get("start") is not None else None
    g.goal = str(d["goal"]) if d.get("goal") is not None else None
    g.hub = str(d["hub"]) if d.get("hub") is not None else None
    return g


# ----------------------------------------------------------------------------- Mermaid

IGNORE_RE = re.compile(r"^(flowchart|graph|classDef|class|style|linkStyle|click|direction|"
                       r"subgraph|end)\b", re.I)
ID_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_\-]*")
CLOSERS = {"[[": "]]", "[(": ")]", "((": "))", "{{": "}}", "[/": "/]", "[\\": "\\]",
           "[": "]", "(": ")", "{": "}", ">": "]"}
LINK_RES = [
    # (regex, dotted, arrow, two-way-prefix)
    (re.compile(r"(<)?-\.\s*([^.|>][^|]*?)\s*\.->"), True, True),
    (re.compile(r"-\.\s*([^.|>-][^|]*?)\s*\.-(?!>)"), True, False),
    (re.compile(r"(<)?-\.+->"), True, True),
    (re.compile(r"-\.+-(?!>)"), True, False),
    (re.compile(r"(<)?==\s*([^=|>][^|]*?)\s*==>"), False, True),
    (re.compile(r"(<)?=+>"), False, True),
    (re.compile(r"={3,}"), False, False),
    (re.compile(r"(<)?--\s*([^-|>.][^|]*?)\s*-->"), False, True),
    (re.compile(r"--\s*([^-|>.][^|]*?)\s*---"), False, False),
    (re.compile(r"(<)?-{2,}>"), False, True),
    (re.compile(r"-{3,}"), False, False),
]


def parse_label_text(raw):
    """Return (label, items, tags) from a node label."""
    items, tags = [], set()

    def take(m):
        body = m.group(1).strip()
        low = body.lower()
        if low.startswith("item:") or low.startswith("items:"):
            items.extend(x.strip() for x in re.split(r"[,+]", body.split(":", 1)[1]) if x.strip())
        elif low in ("start", "goal", "hub"):
            tags.add(low)
        else:
            return m.group(0)
        return ""
    label = re.sub(r"\{([^{}]*)\}", take, raw)
    label = re.sub(r"\s+", " ", label).strip()
    return label, items, tags


def read_node(line, i, g):
    m = ID_RE.match(line, i)
    if not m:
        return None, i
    nid = m.group(0)
    i = m.end()
    for op in ("[[", "[(", "((", "{{", "[/", "[\\", "[", "(", "{", ">"):
        if line.startswith(op, i):
            j = i + len(op)
            close = CLOSERS[op]
            while j < len(line) and line[j] == " ":
                j += 1
            if j < len(line) and line[j] == '"':
                q = line.find('"', j + 1)
                if q < 0:
                    raise InputError("unterminated quote in: %s" % line)
                raw = line[j + 1:q]
                k = line.find(close, q + 1)
            else:
                k = line.find(close, j)
                if op in ("{", "{{"):
                    depth, k = 0, j
                    while k < len(line):
                        if line[k] == "{":
                            depth += 1
                        elif line[k] == "}":
                            if depth == 0:
                                break
                            depth -= 1
                        k += 1
                    k = k if k < len(line) else -1
                raw = line[j:k] if k >= 0 else ""
            if k < 0:
                raise InputError("unterminated node shape in: %s" % line)
            label, items, tags = parse_label_text(raw)
            g.add_node(nid, label, items, tags)
            return nid, k + len(close)
    g.add_node(nid)
    return nid, i


def read_link(line, i):
    s = line[i:]
    for rx, dotted, arrow in LINK_RES:
        m = rx.match(s)
        if m:
            groups = [x for x in m.groups()]
            back = bool(groups and groups[0] == "<")
            text = None
            for gtxt in groups:
                if gtxt and gtxt != "<":
                    text = gtxt
            j = i + m.end()
            while j < len(line) and line[j] == " ":
                j += 1
            if j < len(line) and line[j] == "|":
                k = line.find("|", j + 1)
                if k < 0:
                    raise InputError("unterminated |label| in: %s" % line)
                text = ((text + ", ") if text else "") + line[j + 1:k]
                j = k + 1
            return {"dotted": dotted, "arrow": arrow, "back": back, "text": text or ""}, j
    return None, i


def edge_from_label(text):
    t = text.strip().strip('"').strip()
    low = t.lower()
    req = []
    for m in re.finditer(r"req(?:uires)?\s*:\s*([^,;|]+)", t, re.I):
        req.extend(x.strip().strip('"') for x in m.group(1).split("+") if x.strip())
    oneway = bool(re.search(r"one-?way|\bdrop\b|↓", low))
    consumes = bool(re.search(r"\bconsume[sd]?\b", low))
    vista = "vista" in low
    return req, oneway, consumes, vista


def parse_mermaid(text):
    m = re.search(r"```\s*mermaid\s*\n(.*?)```", text, re.S)
    if m:
        text = m.group(1)
    g = Graph()
    unparsed = []
    for raw in text.replace("\r", "").split("\n"):
        line = raw.strip().rstrip(";").strip()
        if not line or line.startswith("```"):
            continue
        if line.startswith("%%"):
            mm = re.match(r"%%\s*(start|goal|hub)\s*[:=]\s*([A-Za-z0-9_\-]+)", line, re.I)
            if mm:
                setattr(g, mm.group(1).lower(), mm.group(2))
            continue
        if IGNORE_RE.match(line):
            continue
        if "&" in line:
            unparsed.append(line + "  ('&' not supported)")
            continue
        try:
            nid, i = read_node(line, 0, g)
        except InputError:
            unparsed.append(line)
            continue
        if nid is None:
            unparsed.append(line)
            continue
        prev = nid
        ok = True
        while True:
            while i < len(line) and line[i] == " ":
                i += 1
            if i >= len(line):
                break
            link, i = read_link(line, i)
            if link is None:
                ok = False
                break
            while i < len(line) and line[i] == " ":
                i += 1
            nxt, i = read_node(line, i, g)
            if nxt is None:
                ok = False
                break
            req, oneway, consumes, vista = edge_from_label(link["text"])
            if vista or (link["dotted"] and not link["arrow"]):
                g.vistas.append({"from": prev, "to": nxt, "label": link["text"].strip().strip('"')})
            else:
                ow = (link["dotted"] and not link["back"]) or oneway
                if link["back"] and not link["dotted"] and not oneway:
                    ow = False
                g.edges.append({"from": prev, "to": nxt, "requires": req, "oneway": ow,
                                "consumes": consumes})
            prev = nxt
        if not ok:
            unparsed.append(line)
    if unparsed:
        g.warnings.append("unparsed lines ignored: " + " | ".join(unparsed[:5])
                          + (" ..." if len(unparsed) > 5 else ""))
    for nid in g.order:
        tags = g.nodes[nid]["tags"]
        for t in ("start", "goal", "hub"):
            if t in tags and getattr(g, t) is None:
                setattr(g, t, nid)
    for t in ("start", "goal"):
        if getattr(g, t) is None:
            for nid in g.order:
                if nid.lower() == t or g.nodes[nid]["label"].lower() == t:
                    setattr(g, t, nid)
                    break
    return g


# ----------------------------------------------------------------------------- analysis

def analyse(g):
    res = {"failures": [], "warnings": list(g.warnings)}
    if not g.nodes:
        raise InputError("graph has no nodes")
    if g.start is None:
        g.start = g.order[0]
        res["warnings"].append("no start given; using first node '%s'" % g.start)
    for t in ("start", "goal", "hub"):
        v = getattr(g, t)
        if v is not None and v not in g.nodes:
            raise InputError("%s node '%s' is not in the graph" % (t, v))
    if g.goal is None:
        res["warnings"].append("no goal given: goal reachability and softlocks not checked")
    hub = g.hub or g.start
    ids = g.order
    idx = {n: i for i, n in enumerate(ids)}
    inst = []      # (node index, item name)
    node_items = [[] for _ in ids]
    for n in ids:
        for it in g.nodes[n]["items"]:
            node_items[idx[n]].append(len(inst))
            inst.append((idx[n], it))
    node_mask = [sum(1 << b for b in node_items[i]) for i in range(len(ids))]
    cons_edges = [k for k, e in enumerate(g.edges) if e["consumes"] and e["requires"]]
    cons_bit = {k: j for j, k in enumerate(cons_edges)}
    out = [[] for _ in ids]   # (edge index, target index)
    for k, e in enumerate(g.edges):
        a, b = idx[e["from"]], idx[e["to"]]
        out[a].append((k, b))
        if not e["oneway"]:
            out[b].append((k, a))

    def counts(collected, opened):
        c = {}
        for b, (_, name) in enumerate(inst):
            if collected >> b & 1:
                c[name] = c.get(name, 0) + 1
        for k in cons_edges:
            if opened >> cons_bit[k] & 1:
                for r in g.edges[k]["requires"]:
                    c[r] = c.get(r, 0) - 1
        return c

    s0 = (idx[g.start], node_mask[idx[g.start]], 0)
    parent = {s0: None}
    trans = {}
    q = deque([s0])
    goal_i = idx[g.goal] if g.goal is not None else None
    passed_edges = set()
    while q:
        st = q.popleft()
        pos, col, opn = st
        have = counts(col, opn)
        succ = []
        for k, tgt in out[pos]:
            e = g.edges[k]
            nopn = opn
            if e["requires"] and not (k in cons_bit and opn >> cons_bit[k] & 1):
                need = {}
                for r in e["requires"]:
                    need[r] = need.get(r, 0) + 1
                if any(have.get(r, 0) < n for r, n in need.items()):
                    continue
                if k in cons_bit:
                    nopn = opn | (1 << cons_bit[k])
            passed_edges.add(k)
            ns = (tgt, col | node_mask[tgt], nopn)
            succ.append((ns, k))
            if ns not in parent:
                parent[ns] = (st, k)
                if len(parent) > STATE_CAP:
                    raise CapHit()
                q.append(ns)
        trans[st] = succ
    states = list(parent.keys())
    reach_nodes = set(s[0] for s in states)
    res["start"], res["goal"], res["hub"] = g.start, g.goal, hub
    res["states_explored"] = len(states)
    res["nodes"] = len(ids)
    res["reachable_nodes"] = len(reach_nodes)
    res["reachable_pct"] = round(100.0 * len(reach_nodes) / len(ids), 1)
    res["unreachable_nodes"] = [ids[i] for i in range(len(ids)) if i not in reach_nodes]
    goal_states = [s for s in states if s[0] == goal_i] if goal_i is not None else []
    res["goal_reachable"] = bool(goal_states) if goal_i is not None else None

    # items
    ever = 0
    for s in states:
        ever |= s[1]
    got_names = set(inst[b][1] for b in range(len(inst)) if ever >> b & 1)
    placed = set(name for _, name in inst)
    required = sorted(set(r for e in g.edges for r in e["requires"]))
    res["unobtainable_items"] = [{"item": r, "reason": "not placed in any node" if r not in placed
                                  else "placed only in unreachable nodes"}
                                 for r in required if r not in got_names]
    gates = [k for k, e in enumerate(g.edges) if e["requires"]]
    res["gates_never_open"] = [{"from": g.edges[k]["from"], "to": g.edges[k]["to"],
                                "requires": g.edges[k]["requires"]}
                               for k in gates if k not in passed_edges]

    # progression along a shortest winning route
    prog = []
    if goal_states:
        st = goal_states[0]
        path = []
        while parent[st] is not None:
            p, k = parent[st]
            path.append((p, k, st))
            st = p
        path.reverse()
        items0 = [inst[b][1] for b in node_items[idx[g.start]]]
        prog.append("start at %s%s" % (g.start, (" (take " + ", ".join(items0) + ")") if items0 else ""))
        seen_nodes = {idx[g.start]}
        opened_gates = set()
        for p, k, s in path:
            e = g.edges[k]
            if e["requires"] and k not in opened_gates:
                opened_gates.add(k)
                prog.append("open %s%s%s (needs %s%s)" % (
                    ids[p[0]], " -> " if e["oneway"] else " <-> ", ids[s[0]],
                    "+".join(e["requires"]), ", consumed" if e["consumes"] else ""))
            if s[0] not in seen_nodes:
                seen_nodes.add(s[0])
                new = [inst[b][1] for b in node_items[s[0]] if not (p[1] >> b & 1)]
                if new:
                    prog.append("take %s at %s" % (", ".join(new), ids[s[0]]))
        prog.append("reach goal %s (%d moves)" % (g.goal, len(path)))
    res["progression"] = prog

    # softlocks
    soft = []
    if goal_states:
        rev = {}
        for s, succ in trans.items():
            for ns, k in succ:
                rev.setdefault(ns, []).append(s)
        live = set(goal_states)
        stack = list(goal_states)
        while stack:
            s = stack.pop()
            for p in rev.get(s, ()):
                if p not in live:
                    live.add(p)
                    stack.append(p)
        fatal = {}
        for s, succ in trans.items():
            if s not in live:
                continue
            for ns, k in succ:
                if ns in live:
                    continue
                e = g.edges[k]
                if ns[2] != s[2]:
                    kind = "consumed-key softlock"
                elif e["oneway"] and s[0] == idx[e["from"]]:
                    kind = "one-way trap"
                else:
                    kind = "softlock"
                key = (k, kind, s[0], ns[0])
                if key not in fatal:
                    fatal[key] = s
        for (k, kind, a, b), s in sorted(fatal.items(), key=lambda x: (x[0][1], x[0][0])):
            e = g.edges[k]
            have = counts(s[1], s[2])
            locked = []
            if kind == "consumed-key softlock":
                spent = set(e["requires"])
                for k2 in gates:
                    if k2 != k and set(g.edges[k2]["requires"]) & spent and k2 in cons_bit:
                        locked.append("%s-%s" % (g.edges[k2]["from"], g.edges[k2]["to"]))
            soft.append({"type": kind, "move": "%s -> %s" % (ids[a], ids[b]),
                         "requires": e["requires"],
                         "held_before": sorted(n for n, c in have.items() if c > 0),
                         "doors_left_locked": locked})
    res["softlocks"] = soft

    # structure: undirected simple graph
    nb = {i: set() for i in range(len(ids))}
    for e in g.edges:
        a, b = idx[e["from"]], idx[e["to"]]
        if a != b:
            nb[a].add(b)
            nb[b].add(a)
    dead = []
    for i in range(len(ids)):
        if len(nb[i]) == 1 and ids[i] not in (g.start, g.goal):
            dead.append({"node": ids[i], "items": g.nodes[ids[i]]["items"]})
    res["dead_ends"] = dead
    res["junctions"] = [ids[i] for i in range(len(ids)) if len(nb[i]) >= 3]
    und = set((min(a, b), max(a, b)) for a in nb for b in nb[a])
    comp, seen = 0, set()
    for i in range(len(ids)):
        if i in seen:
            continue
        comp += 1
        stack = [i]
        seen.add(i)
        while stack:
            a = stack.pop()
            for b in nb[a]:
                if b not in seen:
                    seen.add(b)
                    stack.append(b)
    res["loops"] = len(und) - len(ids) + comp

    # one-way edges without a return path to the hub (requirements ignored)
    adj = {i: set() for i in range(len(ids))}
    for e in g.edges:
        a, b = idx[e["from"]], idx[e["to"]]
        adj[a].add(b)
        if not e["oneway"]:
            adj[b].add(a)

    def reaches(src, dst):
        seen_, st_ = {src}, [src]
        while st_:
            a = st_.pop()
            if a == dst:
                return True
            for b in adj[a]:
                if b not in seen_:
                    seen_.add(b)
                    st_.append(b)
        return False
    ow = []
    for e in g.edges:
        if e["oneway"]:
            b = idx[e["to"]]
            if not reaches(b, idx[hub]):
                ow.append({"from": e["from"], "to": e["to"],
                           "goal_reachable_after": None if goal_i is None else reaches(b, goal_i)})
    res["oneway_no_return"] = ow
    res["vistas"] = [{"from": v["from"], "to": v["to"], "label": v["label"]} for v in g.vistas]

    if goal_i is not None and not goal_states:
        res["failures"].append("goal '%s' not reachable from start '%s'" % (g.goal, g.start))
    if res["unreachable_nodes"]:
        res["failures"].append("%d unreachable node(s): %s" % (
            len(res["unreachable_nodes"]), ", ".join(res["unreachable_nodes"][:10])))
    for it in res["unobtainable_items"]:
        res["failures"].append("required item '%s' unobtainable (%s)" % (it["item"], it["reason"]))
    for gt in res["gates_never_open"]:
        res["failures"].append("gate %s-%s (needs %s) never opens" % (
            gt["from"], gt["to"], "+".join(gt["requires"])))
    if soft:
        res["failures"].append("%d softlock move(s)" % len(soft))
    for d in dead:
        if not d["items"]:
            res["warnings"].append("dead end without reward: %s" % d["node"])
    for o in ow:
        res["warnings"].append("one-way %s -> %s has no return path to hub %s%s" % (
            o["from"], o["to"], hub,
            "" if o["goal_reachable_after"] is not False else " and the goal is not reachable after it"))
    return res


def human(res, path):
    L = ["graph_check: %s" % path]
    L.append("Start %s, goal %s. Goal: %s. Reachable nodes: %d/%d (%g%%)." % (
        res["start"], res["goal"] or "(none)",
        "n/a" if res["goal_reachable"] is None else ("REACHABLE" if res["goal_reachable"] else "NOT REACHABLE"),
        res["reachable_nodes"], res["nodes"], res["reachable_pct"]))
    if res["unreachable_nodes"]:
        L.append("Unreachable nodes: " + ", ".join(res["unreachable_nodes"]))
    if res["unobtainable_items"]:
        L.append("Unobtainable required items: " + ", ".join(
            "%s (%s)" % (i["item"], i["reason"]) for i in res["unobtainable_items"]))
    if res["progression"]:
        L.append("Key-before-door order (shortest winning route):")
        for i, p in enumerate(res["progression"], 1):
            L.append("  %d. %s" % (i, p))
    if res["softlocks"]:
        L.append("Softlocks:")
        for s in res["softlocks"]:
            L.append("  %s: %s (needs %s; held %s)%s" % (
                s["type"], s["move"], "+".join(s["requires"]) or "nothing",
                ", ".join(s["held_before"]) or "nothing",
                ("; leaves locked: " + ", ".join(s["doors_left_locked"])) if s["doors_left_locked"] else ""))
    elif res["goal_reachable"]:
        L.append("Softlocks: none")
    L.append("Dead ends: %s" % (", ".join(
        "%s%s" % (d["node"], (" [" + ", ".join(d["items"]) + "]") if d["items"] else " (no reward)")
        for d in res["dead_ends"]) or "none"))
    L.append("Junctions (3+ neighbours): %s. Loops: %d." % (", ".join(res["junctions"]) or "none",
                                                           res["loops"]))
    if res["oneway_no_return"]:
        L.append("One-way edges with no return to hub: " + ", ".join(
            "%s->%s" % (o["from"], o["to"]) for o in res["oneway_no_return"]))
    if res["vistas"]:
        L.append("Vistas (not traversable): " + ", ".join(
            "%s~%s" % (v["from"], v["to"]) for v in res["vistas"]))
    for w in res["warnings"]:
        L.append("Warning: " + w)
    for f in res["failures"]:
        L.append("FAIL: " + f)
    L.append(NOT_MODELLED)
    L.append("RESULT: %s" % res["result"].upper())
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="graph_check.py",
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes: 0 pass, 1 check failed, 2 usage/parse error, 3 state cap hit.")
    ap.add_argument("file", help="graph file, '-' for stdin")
    ap.add_argument("--format", choices=("json", "mermaid"), help="input format (default: auto)")
    ap.add_argument("--json", action="store_true", help="machine-readable JSON output")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 2
    try:
        text = read_text(args.file)
        fmt = args.format or ("json" if text.lstrip().startswith("{") else "mermaid")
        g = parse_json(text) if fmt == "json" else parse_mermaid(text)
        res = analyse(g)
    except InputError as e:
        if args.json:
            print(json.dumps({"error": str(e), "not_modelled": NOT_MODELLED}))
        else:
            print("error: %s" % e, file=sys.stderr)
            print(NOT_MODELLED)
        return 2
    except CapHit:
        msg = "state cap of %d reached; result unknown" % STATE_CAP
        print(json.dumps({"result": "unknown", "error": msg, "not_modelled": NOT_MODELLED})
              if args.json else "RESULT: UNKNOWN (%s)\n%s" % (msg, NOT_MODELLED))
        return 3
    res["result"] = "fail" if res["failures"] else "pass"
    res["file"] = args.file
    res["format"] = fmt
    res["not_modelled"] = NOT_MODELLED
    print(json.dumps(res, indent=2) if args.json else human(res, args.file))
    return 1 if res["failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
