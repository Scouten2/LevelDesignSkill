# Puzzle Verification: Solvers, Difficulty Metrics and Playtests

## Contents
1. Why puzzles need machine checks
2. The protocol at a glance
3. Lint and solve
4. Bypass test
5. Shortcut test
6. Uniqueness up to reordering
7. Difficulty metrics and their evidence
8. Make it harder by entanglement, never by padding
9. Sanity priors for generated levels
10. Re-verify after every change
11. When scripts can't run: hand traces
12. Non-grid puzzles
13. Reporting results honestly
14. Playtest protocol for puzzles
15. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Grid format, legends and the general machine-check loop: `grid-conventions.md`. Designing the puzzle: `puzzle-craft.md`. Ordering puzzles: `puzzle-sequencing.md`.

---

## 1. Why puzzles need machine checks

- **LLM puzzle levels fail in known ways.** ScriptDoctor (Earle et al., 2025) gave models examples, compiler errors and BFS feedback with 10 repair attempts; at best 20% of games (o3-mini) had every level solvable with a solution longer than 10 moves, and GPT-4o managed 0–10%. Levels were "overly short", and when asked to make them harder the model "stretch[ed] the level out by a few rows or columns, or add[ed] some scattered obstacles."
- **Length and difficulty can't be prompted.** In Todd et al. (2023) solution length stayed uncontrollable even after fine-tuning.
- **Mental solving is unreliable.** SokoBench (2026) saw planning degrade "when more than 25 moves are required"; in PuzzleJAX, uninformed BFS out-played LLM agents.
- **Solvable isn't the same as intended.** ScriptDoctor's most complex games were solvable "in spite of or even as a result of their broken mechanics". Check *how* a level is solved, not only whether.

So: never claim solvable, unique or hard without a script run or a labelled hand trace. These checks are necessary safeguards, not proof of quality or fun (`fun-checks.md`).

## 2. The protocol at a glance

| # | Step | Command (from the skill root) | Pass | On failure |
|---|---|---|---|---|
| 1 | Lint | `python3 -I scripts/grid_lint.py L.txt --legend puzzle --expect @=1 --closed` | exit 0 | One format-repair pass using the exact errors |
| 2 | Solve | `python3 -I scripts/grid_puzzle_solve.py L.txt` | `solvable` | Unsolvable: fix. `unknown`: shrink |
| 3 | Bypass | `... --forbid RULE` (each key rule) | `unsolvable` | Cheese: block the route, re-run 2–3 |
| 4 | Shortcut | `... --intended MOVES` | Legal, solves, no shorter solution (or a shorter one you keep) | Valve rule (§5) |
| 5 | Classes | `... --classes` | 1 class for introduce/gate slots | Close alternatives or move the slot |
| 6 | Metrics | `... --metrics` | Matches the card's targets | Deepen (§8), never pad |
| 7 | Compare | `python3 -I scripts/level_metrics.py a.txt --compare b.txt c.txt` | Options structurally different | Redesign the near-duplicate |
| 8 | Re-verify | Steps 1–6 after any change | Same results, or explained diffs | §10 |

Cap automated repair at 3 rounds [convention], then report what still fails (`grid-conventions.md` §5). Exit codes for every script: 0 pass, 1 fail/unsolvable, 2 usage or parse error, 3 search cap reached (unknown).

## 3. Lint and solve

- **Lint first.** `grid_lint.py` reports size, ragged rows, unknown glyphs at `(col,row)`, glyph counts, `--expect` results (box/goal balance is always checked for the puzzle legend), `--closed` border and exactly one player. `--emit-ruled` prints the grid with ruler and row indices for the user.
- **Solve.** `grid_puzzle_solve.py FILE [--max-nodes N] [--max-seconds S] [--forbid RULE ...] [--intended MOVES] [--metrics] [--classes] [--json]`; defaults 2,000,000 nodes and 60 s. Rules are auto-detected from glyphs: push always; ice, keys/doors, pits, switches/gates when present. Output: `solvable|unsolvable|unknown`, optimal moves and pushes, a solution string (`UDLR`, uppercase = push), nodes expanded, and the **rules actually used**. Compare that list with the insight card: if the key rule isn't used, the level doesn't teach it.
- **Unknown is a result.** The node or time cap returns `unknown` (exit 3). Shrink or simplify; don't report it as solvable. The size envelope is in `--help`. The unpruned research prototype failed to finish in five minutes on an open 8×10 room with four boxes, so open rooms with many boxes are the hard case.
- **"Not modelled:"** every run prints what it ignores. Copy that line into your report.
- **Soft-locks.** The dead-end ratio (share of reachable states that can no longer win) measures how much undo matters, not difficulty. If the game has no undo, every dead state must be visibly dead and one action from a reset.

## 4. Bypass test

Disable the key rule and re-solve. What counts as a pass depends on whether the rule *enables* moves or *restricts* them.
- **Enabling rules** (keys/doors, pits, switches/gates, a box the solution needs): `--forbid keys|pits|switches` or `--forbid box:<col,row>`. The level should become **unsolvable**. Still solvable means cheese: the player can finish without the truth. Block the route and re-run steps 2–4.
- **Restricting rules** (ice, and any rule that only takes control away): `--forbid ice` turns ice into plain floor, which gives the player *more* control, so the level almost always stays solvable. That proves nothing. Instead, check that the rule **changes the solution**: compare the optimal solution with and without the rule (the moves and pushes should differ), and replay the obvious no-ice plan with `--intended` on the real level to show it fails. A level whose optimal solution is identical with ice treated as floor doesn't use ice.
- Run once per rule the card calls essential, and report which kind of test you ran.
- Smith, Butler and Popović framed this as "solvable, and no solution avoids concept C" for *Refraction* puzzles (FDG 2013) [unverified: secondhand summary].
- For pure push puzzles the key move is a push pattern, not a rule. Use the first-push count and counter-intuitive count, and argue necessity in one sentence (worked example: `puzzle-craft.md` §12).

## 5. Shortcut test

`--intended MOVES` (solver notation, uppercase = push) checks that your intended solution is legal and solves, and reports whether a strictly shorter solution exists and by how much. A shorter solution isn't automatically bad. Decide by Valve's rule: "If the solution is interesting and makes the tester feel smart, it might be left in… If… it makes the player feel as if the game is broken, the team will… remove or reconfigure" (Game Informer, 2010). Portal also let "ninja" skips stand where skipping "arguably takes more skill than solving the puzzle properly."
- **Feels smart:** it uses a real consequence of the rules that the player could state afterwards. Keep it, or turn it into its own level (Traynor: "make a second puzzle where that alternate solution is actually forced"). Talos rewards some unique solutions with star sigils.
- **Feels broken:** it exploits an edge the player can't reason about, or skips the truth. Close it.
- Write the decision on the insight card.

## 6. Uniqueness up to reordering

Raw solution counts mislead: the research prototype found 84 "distinct" push-optimal solutions on a small 3-box level, almost all re-orderings of independent pushes. `--classes` counts distinct optimal solutions **up to reordering** (capped).
- Introduce and gate puzzles: 1 class. Portal: "For training purposes, there's generally just one correct solution to these early puzzles… Later in the game, however, the puzzles become more open-ended."
- Mirror solutions are separate classes. Accept them only if both pass through the same truth.
- Classes cover optimal solutions only; a longer route around the truth won't show here. The bypass test (§4) covers that.

## 7. Difficulty metrics and their evidence

Jarušek and Pelánek (2010) correlated metrics with median human solve time on **35 four-box Sokoban puzzles** (about 2,000 solves, 780 hours). Spearman values:

| Metric | ρ | Status in the skill |
|---|---|---|
| 2-decomposition (boxes split into two groups; group alternations) | 0.82 | Best signal; approximated by entanglement excess |
| Box changes (alternations of the pushed box) | 0.74 | `--metrics` |
| Counter-intuitive moves (against "get boxes closer to goals") | 0.69 | `--metrics` |
| Shortest solution length (Pearson 0.30 is the same metric) | 0.47 | Weak; never the main lever |
| Area change | 0.35 | Not computed |
| State-space size | −0.07 | No correlation; don't use for difficulty |

A decomposable puzzle took a median 3:02 against 53:49 for an indecomposable one of similar size. Humans "are not good at systematic search, but they are good at… abstraction, pattern recognition, and problem decomposition", so puzzles that resist decomposition are hard.

What `--metrics` reports: **counter-intuitive pushes** (pushes that increase the box's distance to its nearest goal); **box changes**; **entanglement excess** = box changes − (boxes − 1), where 0 means fully decomposable; **first-move traps** (share of legal first pushes leading to dead or unsolvable states; no correlation data, a design signal only [convention]); **dead-end ratio**, labelled "undo need, not difficulty". Jarušek and Pelánek take box changes as the minimum over all solutions; if `--help` says the script measures one optimal solution, treat it as an upper bound.

Use metrics to **order** puzzles and spot outliers, never as absolute grades: the sample is small and of one type, no published thresholds map values to easy/medium/hard, and transfer to ice, keys or other mechanics is untested. Pelánek's Sudoku work points to the same two sources in general: step complexity and the dependency structure among steps.

## 8. Make it harder by entanglement, never by padding

Raise difficulty with levers the metrics reward:
- Interleave two sub-goals so neither can be finished first (raises entanglement excess).
- Force a counter-intuitive push: a box must leave its goal line to let another pass.
- Make one object serve two roles, or route two boxes through one shared cell.
- Place a first-move trap that fails visibly.

Never: enlarge the board, scatter obstacles, add boxes that don't interact, or lengthen walks. Length correlates weakly and padding is the documented LLM failure. To make a puzzle easier, reverse the levers: decompose, remove the counter-intuitive push, add slack. Report before/after numbers ("entanglement excess 0 → 2, counter-intuitive 0 → 1, pushes 9 → 12"). When the user gives no targets, propose them up front, e.g. "4 boxes, ≤10×10, ≥15 pushes, ≥1 counter-intuitive push".

## 9. Sanity priors for generated levels

Khalifa and Fayek (2015) measured 40 hand-made levels from 5 PuzzleScript games: solution length / level area ≈ 1.22 ± 0.46, and rule applications per move ≈ 0.42 ± 0.13. Their evaluator also checks that every "critical" object (one appearing in rules with both the player and a winning object) is present. Treat a deviation beyond about 2σ as a flag to inspect, not a defect [convention]. A tiny teaching room sits low; a long walk with few interactions sits high on length but low on rules per move.

## 10. Re-verify after every change

Croteam found that "the process of creating the video game around the puzzle could create unsolvable situations or unforeseen shortcuts". Their bot replayed a human's broad-action plan after every environment change, logged about 15,000 hours, and took 30–60 minutes per full-game run (*The Talos Principle*). Valve sends maps "right back into playtesting" after the art pass. Practice:
- Store each level's intended solution string next to the level file.
- After any geometry, collision, art, rule or glyph change, re-run steps 1–6 and diff the numbers. A change in optimal length, classes or rules used needs an explanation.
- Report edits as diffs ("wall added at (1,2) to close the mirror solution").

## 11. When scripts can't run: hand traces

No code tool, or a mechanic the solver doesn't model (rule rewriting, line drawing, physics):
- Trace step by step in a table: `step | move | player (col,row) | objects after | rule applied`.
- Label it **"hand-traced, not machine-verified."** Traces longer than about 20–25 moves count as unverified (SokoBench).
- A trace proves one solution exists. It proves nothing about shortcuts, bypasses or uniqueness; say so.
- Recount glyphs per row and boxes vs goals by hand; give the user the exact commands to run later.
- For rule systems the solver can't express, prototype in PuzzleScript, whose rule notation (`[ > Player | Crate ] -> [ > Player | > Crate ]`) and engine can test them.

## 12. Non-grid puzzles

- **Logic and deduction.** Write the answer space and every clue as a table. By elimination, check that exactly one assignment fits; for each answer, list which clues pin it and when the player can first see them (Pope's chronology × discovery-order spreadsheet). Small answer spaces invite guessing: batch confirmation as Obra Dinn does (sets of three among 60 crew).
- **Adventure and inventory.** Chart with `dependency_chart.py` (`puzzle-sequencing.md` §8). Add an item table: `item | where found | where used | consumed? | missable? | reachable when needed?`. Any "missable: yes" on a required item fails (Gilbert's "I forgot to pick it up"). Spatial keys and doors with consumption go to `graph_check.py`.
- **Multi-state rooms** (water levels, rotating rooms, power routing). A state table: `state | reachable areas | available actions | ways back`. Every state must reach the goal or reset visibly; no silent one-way states.
- **Physics.** Run many trials with perturbed inputs; set targets with tolerance. Rovio tunes star thresholds longer than it builds the level (`genre-casual-mobile.md`).
- **Line/panel puzzles.** Enumerate all solution paths (the community Witness solver does this) and confirm each obeys the intended rule.

## 13. Reporting results honestly

- "Verified by `grid_puzzle_solve.py`: solvable, optimal 23 moves / 9 pushes, 1 solution class, 2 counter-intuitive pushes, entanglement excess 2; `--forbid keys`: unsolvable; `--intended`: matches optimal. Not modelled: …"
- "Unknown at cap (2,000,000 nodes): not verified; shrinking the room."
- "Hand-traced, not machine-verified (18 moves); shortcuts and uniqueness unchecked."
- Quote numbers verbatim; never round "unknown" up to "solvable"; never state a difficulty without metrics or playtest data.

## 14. Playtest protocol for puzzles

Traynor's protocol for Parabox (GDC 2024): fresh playtesters each time; non-experts; batches of 1 or 2; play the full game; narrated video ("hear their theories and emotions… measure time taken"); watch the entire video before changing anything; about 15 full-game playtests, which "did not reach diminishing returns". Valve watched a new player "from beginning to end" every week, with think-aloud "unprompted and uncorrected", judging "what people do—not what they say" (Ambinder, 2009).

Log per puzzle per tester [convention]: solve time; resets; **every voiced hypothesis, verbatim**; fixation (minutes on one approach); frustration loop (repeating without new information); accidental solve (can't state the truth); bypass; missed observation (never looked at the key feature); hint use; quit; delight.

Decision rules [convention]:
- Most testers miss the same feature → move it into view with geometry before adding text (Portal 2's eye-level hole).
- A wrong hypothesis shared by several testers → remove the false association, or add a puzzle that refutes it.
- Accidental solve → the next puzzle must force the concept, or tighten this one.
- Long median but strong delight → keep it as a protected leap; prime earlier instead of adding a stepping stone (`puzzle-sequencing.md` §5).
- Fatigue after 2–3 hard puzzles → insert a break.
- Fix proportionally: Valve's lethal rails were "too much of an over correction" and were reverted.

If you can't run a playtest, deliver the plan: hypotheses per puzzle (`assets/hypothesis-card.md`), what to log, and the decision rules above.

## 15. Review checklist

- [ ] Grid lint-clean; ruled version shown; key-object list matches
- [ ] Solver result quoted verbatim, including "Not modelled:"; `unknown` reported as unknown
- [ ] Rules actually used include the card's key rule
- [ ] Bypass test run for every key rule: enabling rules → unsolvable when forbidden; restricting rules (ice) → solution changes (or necessity argued for push-pattern insights)
- [ ] Shortcut test run against the intended solution; keep/close decision recorded with Valve's rule
- [ ] Solution classes counted up to reordering; 1 class for introduce/gate puzzles
- [ ] `--metrics` quoted; difficulty claims rest on entanglement and counter-intuitive counts, not length or state space
- [ ] "Harder" changes add entanglement or counter-intuitive pushes, with before/after numbers; no padding
- [ ] Khalifa priors checked for generated levels; outliers explained
- [ ] Everything re-run after the last geometry, art or rule change; intended solution stored
- [ ] Hand traces labelled, ≤20–25 moves, with no uniqueness claims
- [ ] Non-grid puzzles: answer/item/state tables complete; no missable required item
- [ ] Playtest plan: fresh non-experts, narrated, full sessions watched before changes, hypotheses logged
