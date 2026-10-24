# Grid Conventions and Machine Checks

## Contents
1. Why grids need conventions
2. Writing a grid
3. Legends (puzzle, platformer, top-down)
4. Graphs before grids
5. The machine-check loop
6. Reporting results honestly
7. When scripts can't run
8. Review checklist

Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

---

## 1. Why grids need conventions

LLMs read ASCII maps far better than they write them (Text2Space's "read-write asymmetry"). Raw ASCII tokens straddle cell boundaries, so models lose columns, swap x/y, and produce ragged rows; Word2World's code ships a fixer for exactly that, and in ChatGPT4PCG 2 "the majority of prompts are unable to generate a response in the correct format." Pruning irrelevant cells helped more than the choice of format. Properties you can count (empty-space share) were controllable by prompt; properties that need search (solution length, difficulty) were not, even after fine-tuning (Todd et al. 2023). So: write grids in a rigid, self-checking format, keep them small, and let code answer every path, reachability and solvability question.

## 2. Writing a grid

- **Declare size first:** `Grid 12×9 (cols×rows), 1 cell = 1 tile (16 px) / 2 m`.
- **Coordinates are `(col,row)`, origin top-left, row 0 at the top.** Say this in every deliverable that lists coordinates; never mix in `(x,y)` with y-up.
- **Column ruler and row indices** when presenting to a human (generate them with `grid_lint.py --emit-ruled`):
  ```
     0         1
     0123456789012
  00|#############
  01|#@...#......#
  02|#.$..#..$...#
  ```
  Write the *raw* grid (no ruler) inside the file you lint; the linter strips rulers and row prefixes if present.
- **One character per cell, fixed width, no tabs.** Never use bare spaces for floor in output a human will copy (trailing spaces get trimmed): use `-` (or `.` for platformers).
- **A key-object list beside the grid:** `player (1,1); boxes (2,2) (8,2); goals (10,6) (10,7); key a (4,5); door A (6,3)`. Lint compares it with the grid.
- **Chunk size:** keep each grid ≤ ~40×20 [convention]; design big levels as screens or rooms joined by a graph (§4), Spelunky-style.
- **Emit from code when you can.** If a code tool is available, build or edit the grid with a short script (place features at coordinates) rather than retyping rows, then lint.
- **Edits are diffs:** "moved box `$` from (4,3) to (5,3) to remove a dead corner", not a silently retyped map.

## 3. Legends

**Puzzle (Sokoban-standard + extensions)** — used by `grid_lint.py --legend puzzle` and `grid_puzzle_solve.py`:

| Glyph | Meaning |
|---|---|
| `#` | wall |
| `-` `_` (space) | floor |
| `@` / `+` | player / player on goal |
| `$` / `*` | box / box on goal |
| `.` | goal |
| `~` | ice: anything moving onto it slides until blocked or off the ice |
| `a`–`e` / `A`–`E` | key / matching door (door consumes the key) |
| `O` | pit: player can't enter; a pushed box fills it, both become floor |
| `!` / `\|` | switch / gate (gate open only while every switch holds a box) |
| `X` | exit (win condition when the level has no goals) |

**Platformer (VGLC / Mario-AI compatible superset)** — used by `grid_lint.py --legend platformer` and `platformer_reach.py`:

| Glyph | Meaning |
|---|---|
| `-` `.` (space) | empty |
| `X` `#` `S` `?` `Q` `<` `>` `[` `]` `B` `b` | solid (ground, brick, blocks, pipe parts, cannon) |
| `=` | one-way platform (stand on top, pass from below) |
| `^` | hazard (spikes, lava) |
| `E` | enemy (treated as hazard unless `--enemies ignore`) |
| `o` / `*` | coin / required collectible |
| `H` | ladder |
| `@` or `M` / `F` or `G` / `C` | start / goal / checkpoint |
| `W` | water (treated as empty, noted) |

Anything the notation can't express (moving platforms, lifts, springs, timed hazards) goes in a **notes list with coordinates**, and you must expect the reach checker to report false stops there.

**Top-down and 3D spaces** don't need character grids. Use a Mermaid graph for topology, a dimensioned space table for metrics, and a small ASCII plan only for local layout (cover, sightlines), with scale and legend stated.

## 4. Graphs before grids

Design structure as a graph first, geometry second (Dormans, mission and space, 2010): the mission graph (what the player must do, in what order) is a different object from the space graph (where those things happen).

- Bubble diagram / space graph: Mermaid `flowchart`; node = space with role, intensity and floor index (`F2`); edge labels `gate:red_key`, `one-way`, `shortcut`, `vista`, `↓drop(one-way)`, `↑ladder`, `⇅lift`.
- Lock-and-key soundness: `graph_check.py` (JSON or the Mermaid subset) reports unreachable nodes, key-before-door order, consumed-key softlocks, dead ends and loop count.
- Puzzle dependencies: `dependency_chart.py` reports cycles, unreachable puzzles, layer widths (how many puzzles are open at once), bottlenecks and a Mermaid export.
- Only then draw grids for the rooms that need them.

## 5. The machine-check loop

Every system in the LLM level-generation literature that works pairs the model with external checks; multi-round feedback lifted Word2World from 60% to 90% playable worlds, while ScriptDoctor's ten rounds still left most games trivially short. Run this loop on every grid or graph you deliver:

1. **Lint** — `python3 -I scripts/grid_lint.py level.txt --legend puzzle --expect @=1 --closed`. On failure, do one format-repair pass using the exact errors ("row 7 has 19 chars, expected 20").
2. **Solve / reach / graph** — `grid_puzzle_solve.py` (puzzles), `platformer_reach.py --kit kit.json` (platformers), `graph_check.py` (dungeons, hubs, open-world gating).
3. **Metrics** — solver `--metrics`, `level_metrics.py`, `beat_lint.py` on the beat chart.
4. **Repair** — change the design to fix what failed, feeding back *numbers*, not adjectives ("gap at (31,12) uses 96% of max jump", "solvable without the key").
5. **Cap at 3 automated rounds** [convention]; then stop and report what still fails rather than looping.

Run scripts from the skill directory with `python3 -I`; every script has `--help`, a `--json` mode and prints what it does **not** model. Exit codes: 0 pass, 1 fail/unsolvable, 2 usage/parse error, 3 search cap reached (unknown).

When offering alternatives, run `level_metrics.py --compare a.txt b.txt c.txt` so "three options" are structurally different, not reshuffles (LLMs fixate on their first idea and converge on similar outputs).

## 6. Reporting results honestly

- Quote the script's result: "Verified by `grid_puzzle_solve.py`: solvable, optimal 23 pushes, 2 counter-intuitive pushes, entanglement excess 3; bypass test with `--forbid keys`: unsolvable (the key is required)."
- **Never** write "solvable", "reachable", "requires X" or "difficulty N" without a script run or a labelled hand trace.
- "Unknown at cap" is a result: say so and shrink or simplify the level.
- Say what wasn't modelled (enemy timing, moving platforms, physics, camera).
- Checks are safeguards, not proof of fun: no study yet shows that solver-checked LLM levels are more fun, and no benchmark measures player enjoyment. A valid level still needs the fun checks (`fun-checks.md`) and a playtest.

## 7. When scripts can't run

No code tool, or a mechanic the scripts don't model:

- Hand-trace the intended solution move by move with coordinates and state after each step; label it **"hand-traced, not machine-verified."**
- Treat any hand trace longer than ~20–25 moves as unverified (LLM planning degrades past ~25 moves in SokoBench) and say so.
- Count, don't eyeball: tally glyphs per row, recount boxes vs goals, list every key and door.
- Provide the exact commands the user can run later, with the files they need.

## 8. Review checklist

- [ ] Size, scale, coordinate frame `(col,row)` origin top-left stated
- [ ] Raw grid lints clean (fixed width, known glyphs, one start, boxes = goals, closed border)
- [ ] Ruled version shown to the user; key-object list matches the grid
- [ ] Topology graph drawn before grids; `graph_check.py` / `dependency_chart.py` run where gating exists
- [ ] Solver / reach checker run; results quoted with numbers; unmodelled features listed
- [ ] ≤3 repair rounds; remaining failures reported, not hidden
- [ ] Alternatives compared with `level_metrics.py --compare`
- [ ] No solvability or difficulty claim without a script result or a labelled hand trace
