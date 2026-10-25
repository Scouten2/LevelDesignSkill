# Worked example: the lift-shaft detour

An optional, Elden Ring-style detour in a third-person action game. The lift carries the player from the courtyard (LB) to the ramparts on the main path. Riding it, the player can see a lit alcove part-way up the shaft. If they step off the lift at the right moment, a short chain of jumps leads to the alcove, and a drop from it loops back to the courtyard. This file is valid input for `scripts/jump_links.py`; run `python3 -I scripts/jump_links.py assets/example-jump-sequence.md`.

**Kit (assumed: measure it in a gym before you build)**

| Kit | Value |
|---|---|
| units | m |
| player_width | 0.8 |
| damage_fall | 6 |
| lethal_fall | 15 |

| Move | Distance | Height | Range | Rise |
|---|---|---|---|---|
| jump | 4.0 | 1.2 | | |
| mantle | 0.4 | | | 1.8 |

**Nodes** (Z up; X across the screen, Y into it while the camera faces the beam; Landing = X size x Y size)

| Node | Role | Landing | X | Y | Z | Visible from | Note |
|---|---|---|---|---|---|---|---|
| LB | start, checkpoint | 3x3 | 0 | 0 | 0 | | lift bottom; grace site beside it |
| LM | | 3x3 | 0 | 0 | 12 | | lift car at the moment it is level with E1 (moves at 2 m/s) |
| E1 | | 2x4 | 3 | 0 | 11.5 | LM | breach in the shaft wall; daylight through it is the one take-off cue |
| E2 | | 1.6x3 | 7.2 | 0 | 11.5 | E1 | ledge outside the breach |
| BM | | 0.6x6 | 7.2 | 4.5 | 11.5 | E2 | beam into the shaft wall |
| AL | goal, reward, secret | 3x3 | 7.2 | 11.6 | 12 | LM, BM | lit alcove, seen through a grille from the lift on every ride |
| RF | rest | 4x4 | 7.2 | 15.1 | 8 | AL | roof below the alcove |

**Links**

| From | To | Move | Gap | Rise | Camera | Fail | Dir | Window | Note |
|---|---|---|---|---|---|---|---|---|---|
| LB | LM | ride | | | | | | | lift |
| LM | E1 | jump | 0.5 | -0.5 | across | none | | 1.2 | step-off; the car-to-wall gap is narrower than the player, so a mistimed try just rides on |
| E1 | E2 | jump | 2.4 | 0 | across | fall LB | | | 60%, routine; a miss falls 12.7 m from the apex: costly, clear of lethal |
| E2 | BM | walk | | | along | | | | beam walk; narrow on purpose, no jump on it |
| BM | AL | jump | 2.6 | 0.5 | along | respawn BM | | | 74%; depth-axis, so a 3 m landing |
| AL | RF | drop | 0 | -4 | across | | | | committed one-way drop: the loop back |
| RF | LB | walk | | | | | both | | stairs down to the courtyard |
| LM | BM | blocked | | | | | | | shaft walls: only the breach opens |
| E1 | BM | blocked | | | | | | | a wall pier between the breach and the beam |

**First draft and fix.** The draft had BM → AL as gap 3.6 m, rise +1.0 m. The checker said:

```
FAIL  reachability
      - BM->AL (jump): needs 128% of jump, impossible; gap 3.6m vs reach 2.82m at rise 1m:
        shorten the gap to <= 2.82m, lower the landing, or add a node
```

Lowering the alcove 0.5 m raises the reach to 3.53 m, and moving it 1 m closer makes the jump 74%, just under the 75% depth-axis limit. The skip scan then flagged E1 → BM (2.9 m, 73%: the beam is in reach straight from the breach) and LM → BM (123%: looks makeable from the lift); a wall pier and the shaft walls stop both, so they are listed as `blocked`. The current tables pass (tier estimate 3, Medium: hardest jump 74%, and the 1.2 s step-off window is above the 1 s that would add a tier).

**Why it works** (the hidden-detour contract in `references/jump-puzzles.md` §2): the reward is seen before the route (from the lift, every ride); one take-off cue (daylight through the breach); a miss costs a fall to the lift bottom with damage, not death, and the checkpoint is beside it (2 links of replay); the reward sits at the end; the drop loops back so nobody walks back along the beam. **Not modelled:** the lift's step-off window beyond the Window column (1.2 s: the car is within jumping height of E1 for 2.4 m of travel at 2 m/s; see `references/jump-puzzles.md` §2), camera framing in the shaft, and whether the alcove's light reads at the lift's speed. Playtest those.
