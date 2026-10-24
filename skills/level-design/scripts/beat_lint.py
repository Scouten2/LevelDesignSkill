#!/usr/bin/env python3
"""beat_lint.py - paper checks on a level's beat chart (markdown table).

Usage:
  python3 -I scripts/beat_lint.py FILE [--json] [--peak 4] [--rest 2] [--max-peak-run 2]
          [--concepts-warn 2] [--concepts-fail 4] [--max-no-choice 120] [--replay-budget 10]
          [--checkpoint-deaths 2] [--checkpoint-window 1] [--flat-run 3]

FILE is a UTF-8 markdown file ('-' = stdin). The first markdown table with an Intensity
column is used. Headers are matched by prefix, case-insensitively, in any order; other
columns (Mechanic (stage), Emotion, Guidance cues, Assist hooks, Telemetry, Hypothesis...)
are ignored:
  #                  beat number          Beat            beat name
  Intensity          1-5 ("Intensity 1-5", "Intensity (1-5)" also match; "4 (peak)" reads 4)
  New concepts       count ("0" = none) or a comma/semicolon/+ list of concept names
                     (a name counts as brand-new only the first time it appears)
  Expected deaths    number, decimals allowed (0.5); a range "1-2" reads as 2
  Replay cost        seconds or mm:ss (time lost per death); "Replay cost (s)" matches
  Checkpoint         id or blank; a checkpoint on a beat's own row sits at the start of that
                     beat, so it counts as preceding it
  Duration           mm:ss, seconds, "45s", "2m"
  Choice             y/n or text (any text other than no/none counts as a real choice)
  Empty cells: blank, "-", en dash, em dash, "none", "n/a" read as zero/empty.

Checks (every threshold is a [convention] default; set a numeric flag to 0 to disable):
  rest-around-peaks  each run of peak beats (intensity >= --peak) has a rest beat
                     (<= --rest) before it and after it (a chart that ends on its peak gets
                     a warning, not a failure)
  peak-run           no more than --max-peak-run consecutive peak beats
  new-concepts       brand-new concepts per beat: warn at --concepts-warn, fail at
                     --concepts-fail (one per beat is the target; Hodent: <= 3 in learning mode)
  choice-gaps        consecutive beats without a choice must total <= --max-no-choice seconds
                     (needs Choice and Duration)
  replay-budget      for beats with expected deaths d > 0: P(death) x replay cost <=
                     --replay-budget s, with P = min(1, d/(d+1)); replay cost from the column,
                     else estimated as durations since the last checkpoint (labelled)
  peak-vs-replay     the highest-intensity beat must not also carry the highest replay cost
  checkpoints        every beat with expected deaths >= --checkpoint-deaths has a checkpoint
                     on its own row or within the previous --checkpoint-window rows
  flat-stretches     no run of >= --flat-run consecutive beats at the same intensity
Checks whose columns are missing are reported as skipped.

Exit codes: 0 no failures (warnings allowed); 1 a check failed; 2 usage/parse error
(no table with an Intensity column).
"""

import argparse
import json
import re
import sys

NOT_MODELLED = ("Not modelled: actual play time and player skill spread, difficulty of each "
                "beat beyond the stated deaths, what makes a choice meaningful, audio/visual "
                "intensity, whether concepts were really taught; numbers come from the table "
                "as written.")

EMPTY = {"", "-", "–", "—", "none", "n/a", "na", "——", "--"}
NO = EMPTY | {"n", "no", "false", "0", "x"}


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


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells = re.split(r"(?<!\\)\|", s)
    return [c.strip().replace("\\|", "|") for c in cells]


def is_sep(cells):
    return cells and all(re.fullmatch(r":?-{1,}:?", c.replace(" ", "")) for c in cells if c) \
        and any(c for c in cells)


def find_tables(text):
    tables, cur = [], []
    for line in text.replace("\r", "").split("\n"):
        if "|" in line and line.strip():
            cur.append(line)
        else:
            if cur:
                tables.append(cur)
            cur = []
    if cur:
        tables.append(cur)
    out = []
    for t in tables:
        if len(t) < 2:
            continue
        head = split_row(t[0])
        if not is_sep(split_row(t[1])):
            continue
        rows = [split_row(r) for r in t[2:]]
        out.append((head, rows))
    return out


def classify(h):
    k = re.sub(r"\s+", " ", h.strip().lower().strip("*_` "))
    if k in ("#", "no", "no.", "n", "beat #", "#.") or k.startswith("#"):
        return "num"
    for key, prefixes in (("intensity", ("intensity",)),
                          ("concepts", ("new concept", "new mechanic", "concepts")),
                          ("deaths", ("expected death", "deaths", "exp. deaths")),
                          ("replay", ("replay", "retry cost")),
                          ("checkpoint", ("checkpoint",)),
                          ("duration", ("duration", "time", "length")),
                          ("choice", ("choice",)),
                          ("beat", ("beat", "name"))):
        if any(k.startswith(p) for p in prefixes):
            return key
    return None


def num(cell):
    c = cell.strip().lower()
    if c in EMPTY:
        return None
    m = re.findall(r"\d+(?:\.\d+)?", c)
    if not m:
        return None
    if re.search(r"\d\s*[-–]\s*\d", c):
        return max(float(x) for x in m)
    return float(m[0])


def seconds(cell):
    c = cell.strip().lower().lstrip("~≈")
    if c in EMPTY:
        return None
    m = re.fullmatch(r"(\d+):(\d{1,2})(?::(\d{1,2}))?", c)
    if m:
        if m.group(3):
            return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        return int(m.group(1)) * 60 + int(m.group(2))
    m = re.fullmatch(r"(?:(\d+(?:\.\d+)?)\s*m(?:in)?)?\s*(?:(\d+(?:\.\d+)?)\s*s(?:ec)?)?", c)
    if m and (m.group(1) or m.group(2)):
        return float(m.group(1) or 0) * 60 + float(m.group(2) or 0)
    m = re.match(r"(\d+(?:\.\d+)?)", c)
    return float(m.group(1)) if m else None


def parse(text):
    for head, rows in find_tables(text):
        cols = {}
        for i, h in enumerate(head):
            k = classify(h)
            if k and k not in cols:
                cols[k] = i
        if "intensity" not in cols:
            continue
        beats = []
        for n, r in enumerate(rows, 1):
            if not any(c.strip() for c in r):
                continue
            r = r + [""] * (len(head) - len(r))

            def get(k):
                return r[cols[k]] if k in cols else ""
            b = {"row": n, "num": get("num") or str(n), "name": get("beat")}
            b["intensity"] = num(get("intensity"))
            cc = get("concepts").strip()
            if "concepts" not in cols or cc.lower() in EMPTY:
                b["concepts"], b["concept_names"] = 0, []
            elif re.fullmatch(r"\d+", cc):
                b["concepts"], b["concept_names"] = int(cc), None
            else:
                names = [x.strip() for x in re.split(r"[,;+/]|\band\b", cc)
                         if x.strip() and x.strip().lower() not in EMPTY]
                b["concepts"], b["concept_names"] = len(names), names
            b["deaths"] = num(get("deaths")) or 0.0
            b["replay"] = seconds(get("replay")) if "replay" in cols else None
            ck = get("checkpoint").strip()
            b["checkpoint"] = ck if ck.lower() not in NO else ""
            b["duration"] = seconds(get("duration")) if "duration" in cols else None
            ch = get("choice").strip()
            b["choice"] = ch.lower() not in NO
            beats.append(b)
        if not beats:
            raise InputError("beat table has no rows")
        return beats, cols
    raise InputError("no markdown table with an 'Intensity' column found")


def label(b):
    return "#%s%s" % (b["num"], (" " + b["name"]) if b["name"] else "")


def lint(beats, cols, a):
    checks = []

    def add(name, status, details, conv=True):
        checks.append({"check": name, "status": status, "details": details})

    ints = [b["intensity"] for b in beats]
    missing = [label(b) for b in beats if b["intensity"] is None]
    if missing:
        add("intensity-values", "WARN", ["no intensity for " + ", ".join(missing)])

    # rest around peaks + peak runs
    if a.peak > 0:
        runs, i = [], 0
        while i < len(beats):
            if ints[i] is not None and ints[i] >= a.peak:
                j = i
                while j + 1 < len(beats) and ints[j + 1] is not None and ints[j + 1] >= a.peak:
                    j += 1
                runs.append((i, j))
                i = j + 1
            else:
                i += 1
        fails, warns = [], []
        for n, (s, e) in enumerate(runs):
            lo = runs[n - 1][1] + 1 if n > 0 else 0
            hi = runs[n + 1][0] - 1 if n + 1 < len(runs) else len(beats) - 1
            before = any(ints[k] is not None and ints[k] <= a.rest for k in range(lo, s))
            after = any(ints[k] is not None and ints[k] <= a.rest for k in range(e + 1, hi + 1))
            if not before:
                fails.append("no rest (<=%g) before peak %s" % (a.rest, label(beats[s])))
            if not after:
                if e == len(beats) - 1:
                    warns.append("chart ends on peak %s with no cool-down beat" % label(beats[e]))
                else:
                    fails.append("no rest (<=%g) after peak %s" % (a.rest, label(beats[e])))
        add("rest-around-peaks", "FAIL" if fails else ("WARN" if warns else "PASS"), fails + warns)
        if a.max_peak_run > 0:
            long_runs = [r for r in runs if r[1] - r[0] + 1 > a.max_peak_run]
            add("peak-run", "FAIL" if long_runs else "PASS",
                ["%d consecutive peaks %s..%s (max %d)" % (e - s + 1, label(beats[s]), label(beats[e]),
                                                           a.max_peak_run) for s, e in long_runs])

    # new concepts
    if "concepts" not in cols:
        add("new-concepts", "SKIPPED", ["no New concepts column"])
    elif a.concepts_fail > 0 or a.concepts_warn > 0:
        seen, fails, warns = set(), [], []
        for b in beats:
            if b["concept_names"] is None:
                new = b["concepts"]
            else:
                new = 0
                for nm in b["concept_names"]:
                    if nm.lower() not in seen:
                        seen.add(nm.lower())
                        new += 1
            b["new_concepts"] = new
            if a.concepts_fail > 0 and new >= a.concepts_fail:
                fails.append("%s introduces %d brand-new concepts (fail at %d)" % (label(b), new, a.concepts_fail))
            elif a.concepts_warn > 0 and new >= a.concepts_warn:
                warns.append("%s introduces %d brand-new concepts (target 1)" % (label(b), new))
        add("new-concepts", "FAIL" if fails else ("WARN" if warns else "PASS"), fails + warns)

    # choice gaps
    if a.max_no_choice > 0:
        if "choice" not in cols or "duration" not in cols:
            add("choice-gaps", "SKIPPED", ["needs Choice and Duration columns"])
        else:
            fails, run, total, unknown = [], [], 0.0, False
            for b in beats + [None]:
                if b is None or b["choice"]:
                    if run and total > a.max_no_choice:
                        fails.append("%s..%s: %gs without a choice%s (max %gs)" % (
                            label(run[0]), label(run[-1]), total,
                            " (some durations missing)" if unknown else "", a.max_no_choice))
                    run, total, unknown = [], 0.0, False
                else:
                    run.append(b)
                    if b["duration"] is None:
                        unknown = True
                    else:
                        total += b["duration"]
            add("choice-gaps", "FAIL" if fails else "PASS", fails)

    # effective replay cost
    est_used = False
    last_ck = None
    for i, b in enumerate(beats):
        if b["checkpoint"]:
            last_ck = i
        b["replay_eff"] = b["replay"]
        b["replay_estimated"] = False
        if b["replay"] is None and "duration" in cols:
            start = last_ck if last_ck is not None else 0
            ds = [beats[k]["duration"] for k in range(start, i + 1)]
            if all(d is not None for d in ds):
                b["replay_eff"] = sum(ds)
                b["replay_estimated"] = True
    if a.replay_budget > 0:
        deadly = [b for b in beats if b["deaths"] > 0]
        if not ("deaths" in cols):
            add("replay-budget", "SKIPPED", ["no Expected deaths column"])
        else:
            fails, notes = [], []
            for b in deadly:
                if b["replay_eff"] is None:
                    notes.append("%s: no replay cost or durations to estimate it" % label(b))
                    continue
                p = min(1.0, b["deaths"] / (b["deaths"] + 1.0))
                cost = p * b["replay_eff"]
                b["retry_cost"] = round(cost, 1)
                if b["replay_estimated"]:
                    est_used = True
                if cost > a.replay_budget + 1e-9:
                    fails.append("%s: P(death) %.2f x replay %gs%s = %.1fs > %gs" % (
                        label(b), p, b["replay_eff"], " (estimated)" if b["replay_estimated"] else "",
                        cost, a.replay_budget))
            add("replay-budget", "FAIL" if fails else ("WARN" if notes else "PASS"), fails + notes)

    # peak intensity vs peak replay cost
    reps = [b["replay_eff"] for b in beats if b["replay_eff"] is not None]
    if not reps or max(reps) <= 0:
        add("peak-vs-replay", "SKIPPED", ["no replay costs"])
    else:
        mi = max(x for x in ints if x is not None)
        mr = max(reps)
        clash = [b for b in beats if b["intensity"] == mi and b["replay_eff"] == mr]
        add("peak-vs-replay", "FAIL" if clash else "PASS",
            ["%s has both the peak intensity (%g) and the peak replay cost (%gs)" % (label(b), mi, mr)
             for b in clash])

    # checkpoints
    if a.checkpoint_deaths > 0:
        if "deaths" not in cols or "checkpoint" not in cols:
            add("checkpoints", "SKIPPED", ["needs Expected deaths and Checkpoint columns"])
        else:
            fails = []
            for i, b in enumerate(beats):
                if b["deaths"] >= a.checkpoint_deaths:
                    window = beats[max(0, i - a.checkpoint_window):i + 1]
                    if not any(w["checkpoint"] for w in window):
                        fails.append("%s expects %g deaths but no checkpoint on its row or the %d row(s) before"
                                     % (label(b), b["deaths"], a.checkpoint_window))
            add("checkpoints", "FAIL" if fails else "PASS", fails)

    # flat stretches
    if a.flat_run > 0:
        fails, i = [], 0
        while i < len(beats):
            j = i
            while j + 1 < len(beats) and ints[i] is not None and ints[j + 1] == ints[i]:
                j += 1
            if ints[i] is not None and j - i + 1 >= a.flat_run:
                fails.append("%s..%s: %d beats at intensity %g" % (label(beats[i]), label(beats[j]),
                                                                    j - i + 1, ints[i]))
            i = j + 1
        add("flat-stretches", "FAIL" if fails else "PASS", fails)
    return checks, est_used


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="beat_lint.py",
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes: 0 pass (warnings allowed), 1 check failed, 2 usage/parse error.")
    ap.add_argument("file", help="markdown file, '-' for stdin")
    ap.add_argument("--json", action="store_true", help="machine-readable JSON output")
    ap.add_argument("--peak", type=float, default=4, help="peak intensity threshold (default 4)")
    ap.add_argument("--rest", type=float, default=2, help="rest intensity threshold (default 2)")
    ap.add_argument("--max-peak-run", type=int, default=2, help="max consecutive peaks (default 2)")
    ap.add_argument("--concepts-warn", type=int, default=2, help="warn at this many new concepts (default 2)")
    ap.add_argument("--concepts-fail", type=int, default=4, help="fail at this many new concepts (default 4)")
    ap.add_argument("--max-no-choice", type=float, default=120, help="max seconds without a choice (default 120)")
    ap.add_argument("--replay-budget", type=float, default=10, help="max P(death) x replay seconds (default 10)")
    ap.add_argument("--checkpoint-deaths", type=float, default=2,
                    help="beats expecting this many deaths need a checkpoint (default 2)")
    ap.add_argument("--checkpoint-window", type=int, default=1,
                    help="rows before the beat that may hold its checkpoint (default 1)")
    ap.add_argument("--flat-run", type=int, default=3, help="flag runs of this many equal intensities (default 3)")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 2
    try:
        beats, cols = parse(read_text(args.file))
        checks, est = lint(beats, cols, args)
    except InputError as e:
        if args.json:
            print(json.dumps({"error": str(e), "not_modelled": NOT_MODELLED}))
        else:
            print("error: %s" % e, file=sys.stderr)
            print(NOT_MODELLED)
        return 2
    failed = any(c["status"] == "FAIL" for c in checks)
    res = {"file": args.file, "beats": len(beats), "columns": sorted(cols),
           "result": "fail" if failed else "pass", "checks": checks,
           "replay_estimated_from_durations": est,
           "beat_table": [{k: b.get(k) for k in ("num", "name", "intensity", "new_concepts", "deaths",
                                                   "replay_eff", "replay_estimated", "retry_cost",
                                                   "checkpoint", "duration", "choice")} for b in beats],
           "not_modelled": NOT_MODELLED}
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        L = ["beat_lint: %s  (%d beats; columns: %s)" % (args.file, len(beats), ", ".join(sorted(cols)))]
        L.append("Intensity: " + " ".join("-" if b["intensity"] is None else "%g" % b["intensity"]
                                           for b in beats))
        for c in checks:
            L.append("%-8s %s" % (c["status"], c["check"]))
            for d in c["details"]:
                L.append("         - " + d)
        L.append(NOT_MODELLED)
        L.append("RESULT: %s" % res["result"].upper())
        print("\n".join(L))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
