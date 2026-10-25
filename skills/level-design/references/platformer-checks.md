# Platformer Checks: Paper Checks and Scripts

## Contents
1. What checks can and can't tell you
2. The paper-check table
3. Running `platformer_reach.py`
4. The teaches-M test
5. Retry budget with `beat_lint.py`
6. Leniency and linearity with `level_metrics.py`
7. Worked example: a jump-height ladder
8. Repair moves
9. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Grid format, legends and the general check loop are in `grid-conventions.md`; kit numbers and bands in `platformer-metrics.md`; camera rules in `platformer-camera.md`.

---

## 1. What checks can and can't tell you

- LLM-drawn platformer maps fail in predictable ways: ragged rows, jumps that look fine but exceed the kit, and paths with impossible "airtime". MarioGPT's path annotations drew routes a real agent couldn't follow, so a checker must model gravity and jump arcs, not grid adjacency. Never call a platformer level "beatable" or a jump "makeable" without a script run or a labelled hand trace.
- The reach script answers **"can a perfect player with this kit get there?"** It does not answer whether a human will, whether the jump is readable, or whether the camera shows it. The paper checks cover those.
- Every result names what wasn't modelled (enemy timing, moving platforms, lifts, springs, camera). Repeat that line in your report.
- **Not a tile map?** 3D sequences, embedded jump puzzles and movement maps go in a jump-link table and through `jump_links.py` instead (`platformer-3d.md` §1); the same bands apply.

## 2. The paper-check table

Run every row on the ASCII map plus the camera spec and beat chart. "Script" names the tool that helps; a blank means paper only.

| Check | Pass rule | How | Script |
|---|---|---|---|
| Landing visible at take-off | landing inside the frame the camera shows at take-off | take-off x + Δx within forward view; drop ≤ downward view | — |
| Critical-jump margin | no required jump above 90% of the envelope at its Δh | list required jumps with (Δx, Δh) as % of kit | `platformer_reach.py --margin 0.9` |
| Looks jumpable, isn't | nothing at 100–130% of the kit unless reachable | measure every gap and ledge near a route | reach frontier + manual |
| Hazard warning time | hazard on screen ≥ ~1 s of travel before commitment [convention] | run speed × 1 s ahead of the commit point | — |
| Entry-state completable | each screen or section beatable with the resources it is entered with | rerun reach from the screen entry with a reduced kit | `platformer_reach.py` per screen |
| Teaches-M | beatable with the full kit, not beatable without the taught move (Green et al., 2018) | §4 | `--teaches` |
| Leap of faith / blind drop | no critical-path drop whose landing is out of view | camera spec + drop height | — |
| Softlock | no reachable spot from which the goal is unreachable, unless it is a visible death | list pits with no exit | softlock list in reach output |
| Unreachable collectibles | every `o` and `*` reachable (or deliberately decorative) | — | unreachable `o`/`*` list |
| Unfair hazard | first encounter not lethal; each hazard type looks unique; no hidden block over a pit on the critical path | read legend and beats | — |
| Rule break | no tile behaves unlike its look on the critical path | list fakes and hidden blocks | — |
| Retry distance | P(death) × replay ≤ budget; checkpoint before beats with ≥ 2 expected deaths | beat chart | `beat_lint.py` |
| Difficulty spike | leniency rises ≤ one band between adjacent groups without a rest or checkpoint | per-group leniency | `level_metrics.py` |
| Dead air | no stretch > ~5 s with no action or decision unless a planned rest [convention] | rhythm strings | `beat_lint.py` (choice gaps) |
| 3D depth | depth-axis jumps have shadow, countable geometry, ≥ 25% landing margin [convention] | section view | — |

## 3. Running `platformer_reach.py`

```
python3 -I scripts/grid_lint.py level.txt --legend platformer --expect M=1 --expect F=1
python3 -I scripts/platformer_reach.py level.txt --kit kit.json [--teaches MOVE] \
    [--enemies hazard|ignore] [--margin 0.9] [--json]
```

- **Map**: raw grid, platformer legend (`grid-conventions.md` §3): `-` empty; `X # S ? Q < > [ ] B b` solid; `=` one-way; `^` hazard; `E` enemy; `o` coin; `*` required collectible; `H` ladder; `@`/`M` start; `F`/`G` goal; `C` checkpoint; `W` water. Row 0 is the top; coordinates are `(col,row)`. Anything below the bottom row is a pit.
- **Kit**: JSON in tiles and seconds (`platformer-metrics.md` §11). The script fits a parabola to `jump_height` and `jump_distance` and allows any arc up to the maximum.
- **Output**: goal reachable from start; reachable checkpoints and collectibles; unreachable `o`/`*`; frontier cells (where progress stops); per-jump margins (Δx, Δh as % of the envelope) for jumps required on some path to the goal; critical jumps over `--margin`; softlock pits; falls beyond `safe_fall_height`/`fall_damage_height`; a "Not modelled:" line.
- **Exit codes**: 0 pass, 1 checks failed, 2 bad input, 3 search cap (unknown, not a pass).
- **Enemies**: default `--enemies hazard` treats `E` cells as deadly. If the route depends on stomping, run again with `--enemies ignore` and say which result you trust and why.

**Reading false positives.** The checker stops wherever the notation lacks the thing that carries the player: lifts, moving platforms, springs, vines, wind, bounce-off-enemy routes. On real Super Mario Bros. maps the prototype stopped at lifts and springs the notation doesn't encode. When the frontier sits next to an entry in your notes list (e.g. "lift at (40,6), travels rows 6–12, 3 s period"), report it as **"not modelled: lift at (40,6); reach beyond it hand-checked"**, then check the far side by running the script on the section after the lift with its own start. Never delete a real failure by calling it a false positive: a frontier with no unmodelled feature beside it is a real block.

**Reading true positives carefully.** Reachable means reachable by a perfect player with exact inputs. A required jump at 88% passes `--margin 0.9` and still needs a checkpoint before it and a signpost.

## 4. The teaches-M test

Green, Khalifa, Barros, Nealen and Togelius (FDG 2018) define a level that teaches a mechanic as one that "a perfect agent… wins" while "an agent that cannot perform one mechanic loses or cannot finish." That is the mechanical form of "the first encounter is unavoidable."

- `--teaches double_jump|wall_jump|dash` removes the move; `--teaches jump_height=X` or `jump_distance=X` reduces it. PASS = goal reachable with the full kit and not reachable with the reduced one.
- Pick X just below the requirement you intend to teach: if the level teaches "jump 3 tiles high", test `jump_height=2.9`. In the checker a step h tiles tall needs `jump_height` ≥ h (an exact match lands), and take-off and landing snap to whole tiles.
- A FAIL means a bypass: a stepping stone, a wall-jump cheese, an enemy bounce or an alternate route. Find it from the reduced run's frontier and reachable set.
- Run it per Learn beat, not only per level, by cutting the beat into its own chunk.

## 5. Retry budget with `beat_lint.py`

```
python3 -I scripts/beat_lint.py beats.md [--json]
```

It reads the beat-chart table (columns `#`, `Beat`, `Intensity`, `New concepts`, `Expected deaths`, `Replay cost`, `Checkpoint`, `Duration`, `Choice`) and checks, with [convention] defaults: rest (≤ 2) around each peak (≥ 4); no more than two consecutive beats at ≥ 4; new concepts per beat (warn at 2, fail at 4); choice gaps over 120 s; P(death) × replay ≤ 10 s, with P ≈ min(1, deaths ÷ (deaths + 1)); peak intensity not on the beat with peak replay cost; a checkpoint before every beat with ≥ 2 expected deaths; flat runs of ≥ 3 equal beats. Replay cost comes from `platformer-metrics.md` §9 (tiles from checkpoint ÷ run speed + respawn + forced waits).

## 6. Leniency and linearity with `level_metrics.py`

```
python3 -I scripts/level_metrics.py level.txt --legend platformer [--compare alt1.txt alt2.txt] [--json]
```

- **Smith & Whitehead (2010) definitions**: *linearity* fits a regression line through platform midpoints and averages the absolute distances to it, normalised to [0, 1] with **0 highly linear and 1 highly non-linear** (Launchpad's levels rarely exceeded 0.7). *Leniency* scores each beat's geometry: +1 gaps, enemies, falls; +0.5 springs, stompers; −0.5 moving platforms; −1 jumps with no gap, with **higher scores meaning less lenient** (range −1 to 1). Read the sign before reporting.
- **What the script reports instead**: a per-column leniency proxy (gaps, hazards and enemies per column) and a linearity proxy (standard deviation of ground height). They track the same ideas but are not the paper's numbers; call them "leniency proxy" and "ground-height spread".
- Use the per-column profile to find spikes (a run of harm-dense columns with no rest) and to compare levels in a world. Smith & Whitehead's warning applies: one small authoring habit (re-picking the same component) biased Launchpad toward linear levels, so measure, don't assume.
- `--compare` gives tile Hamming distance and a metric-difference vector, and flags near-duplicates; use it whenever you offer alternatives.

## 7. Worked example: a jump-height ladder

Concept: "jump height control", taught with a 1-2-3 pillar ladder, then a coin-arc pit as a rest beat. Kit: generic, `jump_height` 4, `jump_distance` 6. Grid 40×6, 1 cell = 1 tile, `(col,row)` origin top-left.

```
   0         1         2         3
   0123456789012345678901234567890123456789
00|----------------------------------------
01|-----------------------------o----------
02|------------------------##--o-o---------
03|---------------##-------##-o---o--------
04|---M----##-----##-------##----------F---
05|XXXXXXXXXXXXXXXXXXXXXXXXXXXXX---XXXXXXXX
```

Key objects: start M (3,4); goal F (36,4); pillars cols 8–9 (1 tall), 15–16 (2 tall), 24–25 (3 tall); pit cols 29–31 (3 wide, bottomless); coin arc (27,3) (28,2) (29,1) (30,2) (31,3). Notes: no movers, no enemies.

`kit.json`:

```json
{"jump_height": 4.0, "jump_distance": 6.0, "player_width": 1, "player_height": 1,
 "air_control": true, "coyote_time": 0.1, "double_jump": false, "wall_jump": false,
 "dash_distance": 0, "fall_damage_height": null, "safe_fall_height": null}
```

Commands:

```
python3 -I scripts/grid_lint.py height_ladder.txt --legend platformer --expect M=1 --expect F=1
python3 -I scripts/platformer_reach.py height_ladder.txt --kit kit.json --teaches jump_height=2.9 --margin 0.9
```

Real `grid_lint.py` output (abridged): `grid_lint: platformer legend, 40x6 (cols x rows) - PASS`, one player start at (3,4), `counts: #=12 -=184 F=1 M=1 X=37 o=5`; the ruled grid above is its `--emit-ruled` output.

**Real `platformer_reach.py` output** (this map ships as `scripts/tests/fixtures/platformer/height_ladder.txt`; abridged):

```
Start (3,4). Reachable standing positions: 37.
Goal: REACHABLE
Easiest route: 13 moves, 9 non-walk; hardest move uses 59.3% of the envelope (every route needs at least this).
  (6,4)->(8,3) jump   dx=1 (15.8%) dh=+1 (25%) usage 25%
  ...
  (23,4)->(28,4) jump dx=4 (59.3%) dh=+0 (0%) usage 59.3% fall 4
Critical jumps (> 90% of envelope): none
Collectibles: 5/5 reachable
Softlock pits: none
Teaches jump_height=2.9: PASS (full kit reaches goal: yes; reduced kit reaches goal: no)
Not modelled: enemy movement/AI ..., moving platforms, lifts, springs ..., ledge overhang (tile-snapped take-off/landing), ...
RESULT: PASS
```

Draft A (pillars 3 tiles apart) on the same kit: `Teaches jump_height=2.9: FAIL (full kit reaches goal: yes; reduced kit reaches goal: yes)`.

How to read it:

- **Draft A failed the teaches test.** Its pillars stood 3 tiles apart (cols 8–9, 13–14, 18–19), so the 2-tall pillar top was a stepping stone onto the 3-tall one (Δh +1) and a 2.9-tile jump still finished. The repair spread the pillars 5–7 tiles apart, beyond reach from the previous top.
- **The repaired ladder passes**: the full kit reaches the goal and clears the 3-tall pillar; a 2.9-tile jump cannot. The 3-tall pillar asks for 75% of the kit's jump height: the signposted skill-check band, right for a Mastery beat.
- **The easiest route's hardest move is 59.3%** of the envelope (the 4-tile hop over the tall pillar region), and nothing exceeds the 90% critical line, so the pit and pillars sit in the routine and skill-check bands.
- Quote the real run like this in deliverables; never paraphrase a PASS you didn't get.

A matching beat chart for `beat_lint.py` (hand-computed expectation: passes, since beat 3's 2 expected deaths × 6 s gives P × replay ≈ 4 s and it has its own checkpoint):

| # | Beat | Intensity | New concepts | Expected deaths | Replay cost | Checkpoint | Duration | Choice |
|---|---|---|---|---|---|---|---|---|
| 1 | Learn: 1-tall pillar | 1 | jump height | 0 | 0 | C0 | 0:04 | n |
| 2 | Develop: 2-tall pillar | 2 | 0 | 0.5 | 3 | | 0:04 | n |
| 3 | Mastery: 3-tall pillar | 4 | 0 | 2 | 6 | C1 | 0:05 | n |
| 4 | Rest: coin-arc pit | 2 | 0 | 0.5 | 3 | | 0:05 | y |

## 8. Repair moves

| Failure | Cheapest fixes |
|---|---|
| Goal unreachable | widen landing, lower ledge, add a step, move the frontier feature into the notes list if it is a lift or spring |
| Critical jump > 90% | shrink the gap, raise the landing, move it to an optional route, add a run-up |
| Teaches-M fails | remove the stepping stone or alternate route; space instances beyond the reduced kit's reach |
| Softlock pit | add an exit (ladder, step, wall), make it a visible death, or block entry |
| Unreachable collectible | move it, or make it reachable by the intended harder line and verify that line |
| Retry budget over | add a checkpoint, shorten the replay, lower P(death) by widening windows |
| Leniency spike | insert a rest platform, split the group, move the hardest jump after a checkpoint |
| Blind landing | lower the drop, add a camera lead or attractor, add a coin trail into view |

Show every repair as a diff ("moved pillar from cols 18–19 to 24–25 to remove a stepping stone") and re-run the checks; stop after three rounds and report what still fails (`grid-conventions.md` §5).

## 9. Review checklist

- [ ] Grid lints clean with the platformer legend; ruled version and key-object list shown
- [ ] Unmodelled features (movers, lifts, springs, enemy timing) listed with coordinates
- [ ] `platformer_reach.py` run with the real kit; goal reachable; result quoted with its "Not modelled" line
- [ ] No required jump above 90% of the envelope; nothing in the 100–130% zone
- [ ] `--teaches` PASS for each taught move or height
- [ ] No softlocks; every collectible reachable or labelled decorative
- [ ] Each screen completable from its entry state
- [ ] Paper checks done: landings visible, hazards visible ~1 s ahead, no blind drops, no rule breaks
- [ ] `beat_lint.py` run on the beat chart; retry budget and checkpoint coverage pass
- [ ] `level_metrics.py` profile checked for spikes; alternatives compared with `--compare`
- [ ] Anything unchecked labelled "hand-traced, not machine-verified"
