#!/usr/bin/env python3
"""dependency_chart.py - puzzle dependency chart / mission graph analysis.

Usage:
  python3 -I scripts/dependency_chart.py FILE [--mermaid] [--json]

FILE is UTF-8 text ('-' = stdin), either one puzzle per line:
    id: label | needs: a, b | gives: x, y
  ("needs"/"gives" parts optional and in any order; synonyms requires/unlocks/opens;
  lines starting with '#' or '//' and blank lines are ignored; code fences are stripped)
or JSON: [{"id": "...", "label": "...", "needs": [], "gives": []}] (or {"puzzles": [...]}).

Model: a puzzle is open once every item it needs has been given by some solved puzzle (any
giver satisfies a need; gives are permanent). Puzzle B depends on A if B needs something A
gives. Layers are computed by solving everything open each round: layer 0 = needs nothing.

Reports: cycles (error: strongly connected groups in the dependency graph); unreachable
puzzles (needs never given, or only given by unreachable puzzles / cycles); topological
layers with widths (how many puzzles are open at once); critical path (longest chain of
earliest dependencies, its length = number of rounds); bottlenecks (a middle layer of width
1); expanding puzzles (open >= 3 others) and contracting puzzles (need gives from >= 2
puzzles); Gilbert check: solving one puzzle should open 2-3 new ones [convention] - counts
of puzzles opening 0, 1, 2-3 and 4+ others and linear runs (3+ puzzles in a row each opening
exactly one). --mermaid prints a Mermaid flowchart (summary as %% comments).

Exit codes: 0 pass; 1 cycles or unreachable puzzles; 2 usage/parse error.
Bottlenecks and Gilbert-check results are warnings.
"""

import argparse
import json
import re
import sys

NOT_MODELLED = ("Not modelled: puzzle difficulty and solve time, travel between puzzles, "
                "consumable items (gives are permanent), alternative solutions inside one "
                "puzzle, red herrings, hint availability, player knowledge (a puzzle 'open' "
                "on the chart may still be undiscoverable in the level).")


class InputError(Exception):
    pass


def read_text(path):
    if path == "-":
        return sys.stdin.read()
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        raise InputError("cannot read %s: %s" % (path, e))


def split_list(s):
    return [x.strip() for x in re.split(r"[,;]", s) if x.strip() and x.strip() not in ("-", "none")]


def parse(text):
    st = text.strip()
    if st.startswith("[") or st.startswith("{"):
        try:
            d = json.loads(st)
        except ValueError as e:
            raise InputError("invalid JSON: %s" % e)
        if isinstance(d, dict):
            d = d.get("puzzles", d.get("nodes"))
        if not isinstance(d, list):
            raise InputError("JSON must be a list of puzzles")
        out = []
        for p in d:
            if not isinstance(p, dict) or "id" not in p:
                raise InputError("every puzzle needs an 'id'")
            out.append({"id": str(p["id"]), "label": str(p.get("label") or p["id"]),
                        "needs": [str(x) for x in p.get("needs", []) or []],
                        "gives": [str(x) for x in p.get("gives", []) or []]})
        return out
    out = []
    for n, raw in enumerate(text.replace("\r", "").split("\n"), 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("//") or line.startswith("```"):
            continue
        line = re.sub(r"^[-*]\s+", "", line)
        parts = [p.strip() for p in line.split("|")]
        head = parts[0]
        if ":" in head:
            pid, label = head.split(":", 1)
        else:
            pid, label = head, ""
        pid = pid.strip().strip("`")
        if not pid or not re.fullmatch(r"[^\s|:]+", pid):
            raise InputError("line %d: cannot read a puzzle id from %r" % (n, raw))
        p = {"id": pid, "label": label.strip() or pid, "needs": [], "gives": []}
        for part in parts[1:]:
            m = re.match(r"(needs|requires|gives|unlocks|opens)\s*:\s*(.*)$", part, re.I)
            if not m:
                if part:
                    raise InputError("line %d: unknown part %r (use needs: / gives:)" % (n, part))
                continue
            key = "needs" if m.group(1).lower() in ("needs", "requires") else "gives"
            p[key].extend(split_list(m.group(2)))
        out.append(p)
    return out


def analyse(puzzles):
    res = {"failures": [], "warnings": []}
    if not puzzles:
        raise InputError("no puzzles found")
    ids = []
    by = {}
    for p in puzzles:
        if p["id"] in by:
            raise InputError("duplicate puzzle id %r" % p["id"])
        by[p["id"]] = p
        ids.append(p["id"])
    givers = {}
    for p in puzzles:
        for x in p["gives"]:
            givers.setdefault(x, []).append(p["id"])
    deps = {i: set() for i in ids}      # i depends on these
    dependents = {i: set() for i in ids}
    for p in puzzles:
        for x in p["needs"]:
            for gvr in givers.get(x, []):
                deps[p["id"]].add(gvr)
                dependents[gvr].add(p["id"])
    # cycles: Tarjan SCC
    index, low, onst, stack, sccs = {}, {}, set(), [], []
    counter = [0]

    def strong(v):
        work = [(v, iter(sorted(dependents[v])))]
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        onst.add(v)
        while work:
            node, it = work[-1]
            advanced = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter[0]
                    counter[0] += 1
                    stack.append(w)
                    onst.add(w)
                    work.append((w, iter(sorted(dependents[w]))))
                    advanced = True
                    break
                elif w in onst:
                    low[node] = min(low[node], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[node])
            if low[node] == index[node]:
                comp = []
                while True:
                    w = stack.pop()
                    onst.discard(w)
                    comp.append(w)
                    if w == node:
                        break
                if len(comp) > 1 or node in dependents[node]:
                    sccs.append(sorted(comp, key=ids.index))
    for v in ids:
        if v not in index:
            strong(v)
    res["cycles"] = sccs
    # layering
    layer = {}
    have = {}
    rnd = 0
    while True:
        new = [i for i in ids if i not in layer
               and all(x in have and have[x] < rnd for x in by[i]["needs"])]
        if not new:
            break
        for i in new:
            layer[i] = rnd
        for i in new:
            for x in by[i]["gives"]:
                if x not in have:
                    have[x] = rnd
        rnd += 1
    unreachable = []
    in_cycle = set(x for c in sccs for x in c)
    for i in ids:
        if i in layer:
            continue
        missing = [x for x in by[i]["needs"] if x not in givers]
        if missing:
            reason = "needs %s which nothing gives" % ", ".join(missing)
        elif i in in_cycle:
            reason = "in a dependency cycle"
        else:
            reason = "depends on unreachable puzzles"
        unreachable.append({"id": i, "reason": reason})
    res["unreachable"] = unreachable
    nlayers = (max(layer.values()) + 1) if layer else 0
    layers = [[i for i in ids if layer.get(i) == k] for k in range(nlayers)]
    res["layers"] = [{"layer": k, "width": len(l), "puzzles": l} for k, l in enumerate(layers)]
    res["max_width"] = max((len(l) for l in layers), default=0)
    # critical path
    path = []
    if layer:
        end = max(layer, key=lambda i: (layer[i], -ids.index(i)))
        cur = end
        path = [cur]
        while layer[cur] > 0:
            prevs = [d for d in deps[cur] if d in layer and layer[d] == layer[cur] - 1]
            if not prevs:
                break
            cur = sorted(prevs, key=ids.index)[0]
            path.append(cur)
        path.reverse()
    res["critical_path"] = path
    res["critical_path_length"] = len(path)
    res["bottlenecks"] = [l[0] for k, l in enumerate(layers) if len(l) == 1 and 0 < k < nlayers - 1]
    opens = {i: len(dependents[i] - {i}) for i in ids}
    res["opens"] = opens
    res["expanding"] = [i for i in ids if opens[i] >= 3]
    res["contracting"] = [i for i in ids if len(deps[i] - {i}) >= 2]
    sinks = [i for i in ids if opens[i] == 0]
    hist = {"0": len(sinks), "1": sum(1 for i in ids if opens[i] == 1),
            "2-3": sum(1 for i in ids if 2 <= opens[i] <= 3), "4+": sum(1 for i in ids if opens[i] >= 4)}
    runs = []
    seen = set()
    for i in ids:
        if opens[i] != 1 or i in seen:
            continue
        preds = [d for d in deps[i] if opens.get(d) == 1 and len(dependents[d]) == 1]
        if preds:
            continue
        run = [i]
        cur = i
        while opens[cur] == 1:
            nxt = next(iter(dependents[cur]))
            if nxt in run or opens[nxt] != 1:
                break
            run.append(nxt)
            cur = nxt
        seen.update(run)
        if len(run) >= 3:
            runs.append(run)
    nonfinal = len(ids) - len(sinks)
    res["gilbert"] = {"opens_histogram": hist, "non_final": nonfinal,
                      "opening_2_to_3": hist["2-3"], "linear_runs": runs,
                      "ok": nonfinal == 0 or (hist["2-3"] + hist["4+"]) * 2 >= nonfinal and not runs}

    if sccs:
        res["failures"].append("%d dependency cycle(s): %s" % (
            len(sccs), "; ".join(" -> ".join(c) for c in sccs)))
    if unreachable:
        res["failures"].append("%d unreachable puzzle(s): %s" % (
            len(unreachable), ", ".join("%s (%s)" % (u["id"], u["reason"]) for u in unreachable)))
    if res["bottlenecks"]:
        res["warnings"].append("bottleneck layer(s) of width 1: %s" % ", ".join(res["bottlenecks"]))
    if len(sinks) > 1:
        res["warnings"].append("%d puzzles open nothing (%s); only the final one should"
                               % (len(sinks), ", ".join(sinks)))
    if not res["gilbert"]["ok"]:
        res["warnings"].append("Gilbert check [convention]: %d of %d non-final puzzles open 2-3+ "
                               "others%s" % (hist["2-3"] + hist["4+"], nonfinal,
                                             "; linear runs: " + "; ".join(" -> ".join(r) for r in runs)
                                             if runs else ""))
    return res


def mid(s):
    return re.sub(r"[^A-Za-z0-9_]", "_", s)


def mermaid(puzzles, res):
    L = ["flowchart TD"]
    for p in puzzles:
        L.append('  %s["%s"]' % (mid(p["id"]), p["label"].replace('"', "'")))
    givers = {}
    for p in puzzles:
        for x in p["gives"]:
            givers.setdefault(x, []).append(p["id"])
    for p in puzzles:
        for x in p["needs"]:
            gs = givers.get(x)
            if not gs:
                L.append('  missing_%s(["%s ?"]) -.-> %s' % (mid(x), x.replace('"', "'"), mid(p["id"])))
            for gvr in gs or []:
                L.append("  %s -->|%s| %s" % (mid(gvr), x.replace("|", "/"), mid(p["id"])))
    for b in res["bottlenecks"]:
        L.append("  style %s stroke-width:4px" % mid(b))
    for f in res["failures"]:
        L.append("  %% FAIL: " + f)
    for w in res["warnings"]:
        L.append("  %% Warning: " + w)
    L.append("  %% Layers widths: " + ", ".join(str(l["width"]) for l in res["layers"]))
    L.append("  %% " + NOT_MODELLED)
    return "\n".join(L)


def human(res, path):
    L = ["dependency_chart: %s" % path]
    L.append("Puzzles: %d. Layers: %d. Widths: %s (max %d open at once)." % (
        sum(l["width"] for l in res["layers"]) + len(res["unreachable"]), len(res["layers"]),
        ", ".join(str(l["width"]) for l in res["layers"]), res["max_width"]))
    for l in res["layers"]:
        L.append("  L%d (%d): %s" % (l["layer"], l["width"], ", ".join(l["puzzles"])))
    L.append("Critical path (%d): %s" % (res["critical_path_length"], " -> ".join(res["critical_path"])))
    L.append("Cycles: %s" % ("; ".join(" -> ".join(c) for c in res["cycles"]) or "none"))
    L.append("Unreachable: %s" % (", ".join("%s (%s)" % (u["id"], u["reason"])
                                           for u in res["unreachable"]) or "none"))
    L.append("Bottlenecks: %s. Expanding (opens >=3): %s. Contracting (needs >=2 puzzles): %s." % (
        ", ".join(res["bottlenecks"]) or "none", ", ".join(res["expanding"]) or "none",
        ", ".join(res["contracting"]) or "none"))
    g = res["gilbert"]
    L.append("Gilbert check (each solve opens 2-3 [convention]): opens 0/1/2-3/4+ = %s; %s" % (
        "/".join(str(g["opens_histogram"][k]) for k in ("0", "1", "2-3", "4+")),
        "OK" if g["ok"] else "LOW PARALLELISM"))
    for w in res["warnings"]:
        L.append("Warning: " + w)
    for f in res["failures"]:
        L.append("FAIL: " + f)
    L.append(NOT_MODELLED)
    L.append("RESULT: %s" % res["result"].upper())
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="dependency_chart.py",
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes: 0 pass, 1 cycles/unreachable puzzles, 2 usage/parse error.")
    ap.add_argument("file", help="chart file, '-' for stdin")
    ap.add_argument("--mermaid", action="store_true", help="print a Mermaid flowchart")
    ap.add_argument("--json", action="store_true", help="machine-readable JSON output")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 2
    try:
        puzzles = parse(read_text(args.file))
        res = analyse(puzzles)
    except InputError as e:
        if args.json:
            print(json.dumps({"error": str(e), "not_modelled": NOT_MODELLED}))
        else:
            print("error: %s" % e, file=sys.stderr)
            print(NOT_MODELLED)
        return 2
    res["result"] = "fail" if res["failures"] else "pass"
    res["file"] = args.file
    res["not_modelled"] = NOT_MODELLED
    if args.json:
        if args.mermaid:
            res["mermaid"] = mermaid(puzzles, res)
        print(json.dumps(res, indent=2))
    elif args.mermaid:
        print(mermaid(puzzles, res))
    else:
        print(human(res, args.file))
    return 1 if res["failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
