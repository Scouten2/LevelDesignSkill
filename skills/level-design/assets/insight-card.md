# Insight Card

Fill one card per puzzle **before** drawing the grid or room (method: `references/puzzle-craft.md` §5–8).
Fill the solver block only from script output (`references/puzzle-verification.md`); write "not run" otherwise.
Coordinates are `(col,row)`, origin top-left.

```
ID:                     Tier:            Slot: introduce | gate | develop | combine | twist | conclude | side
Mechanics used:         New concept (≤1):
Stance: showcase | revelation           Difficulty source: ingenuity | patience
Slack space: deliberate (where) | none   Protected leap: yes (primed by IDs ___) | no

THE TRUTH (one sentence — the non-obvious consequence of the rules this puzzle demonstrates):

FALSE ASSUMPTION it overturns (what players believe before solving):

TEMPTING WRONG MOVE:
  -> VISIBLE RULE that defeats it (what the player sees happen, and what it teaches):

PREREQUISITES (facts the player must already have; puzzle IDs that taught them):

KEY MOVE (the move/deduction the puzzle is reverse-engineered from; where it happens):

INTENDED SOLUTION (solver notation, UDLR, uppercase = push; or numbered steps for non-grid puzzles):

ELEMENTS + DELETION TEST (each element and why removing it breaks solvability, the truth, or readability):
  -
  -

KEY OBSERVATION in default view / eye level?  yes | no (fix):
FAIRNESS LINT (puzzle-craft.md §10) — failures:
ESCAPE VALVES: parallel puzzle | hint ladder rungs | unlock-all | skip state | optional

POST-SOLVE SENTENCE ("Of course…!"):

SOLVER RESULTS (paste verbatim; "not run" / "hand-traced, not machine-verified" if so)
  Lint:            grid_lint.py --legend puzzle --expect @=1 --closed  ->
  Solve:           solvable | unsolvable | unknown(cap)   moves:    pushes:    nodes:
  Rules used:                         (must include the key rule)
  Bypass:          --forbid ______  ->  unsolvable? (required: yes)
  Shortcut:        --intended ...   ->  legal / solves / shorter by ___ ; decision: keep (smart) | close (broken) | spin off
  Classes:         --classes        ->  ___ (introduce/gate: 1)
  Metrics:         counter-intuitive ___ | box changes ___ | entanglement excess ___ | first-move traps ___ | dead-end ratio ___ (undo need)
  Not modelled:
  Re-verified after last change (date / what changed):

PLAYTEST (fill after testing): n ___ | median time ___ | % who can state the truth ___ |
  wrong hypotheses heard (verbatim): | missed observations: | accidental solves: | delight:
```
