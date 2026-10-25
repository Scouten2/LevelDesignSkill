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

**Nodes** (Z up; X across the screen, Y into it while the camera faces the beam)

| Node | Role | Landing | X | Y | Z | Visible from | Note |
|---|---|---|---|---|---|---|---|
| LB | start, checkpoint | 3x3 | 0 | 0 | 0 | | lift bottom; grace site beside it |
| LM | | 3x3 | 0 | 0 | 12 | | lift car mid-ride (moves at 2 m/s) |
| E1 | | 2x4 | 4 | 0 | 11.5 | LM | ledge the car passes; rubble "steps" mark it |
| E2 | | 1.6x3 | 8.2 | 0 | 11.5 | E1 | broken railing: the take-off cue |
| BM | | 0.6x6 | 8.2 | 4.5 | 11.5 | E2 | beam into the shaft wall |
| AL | goal, reward, secret | 3x3 | 8.2 | 11.6 | 12 | LM, BM | lit alcove, seen from the lift on every ride |
| RF | rest | 4x4 | 8.2 | 15.1 | 8 | AL | roof below the alcove |

**Links**

| From | To | Move | Gap | Rise | Camera | Fail | Note |
|---|---|---|---|---|---|---|---|
| LB | LM | ride | | | | | lift; the car passes E1 for ~1 s, a readable window |
| LM | E1 | jump | 1.5 | -0.5 | across | fall LB | step-off jump, 34%: intro band |
| E1 | E2 | jump | 2.4 | 0 | across | fall LB | 60%, routine |
| E2 | BM | walk | | | along | | beam walk; narrow on purpose, no jump on it |
| BM | AL | jump | 2.6 | 0.5 | along | respawn BM | 74%; depth-axis, so a 3 m landing |
| AL | RF | drop | 0 | -4 | across | | committed one-way drop: the loop back |
| RF | LB | walk | | | | | stairs down to the courtyard |

**First draft and fix.** The draft had BM → AL as gap 3.6 m, rise +1.0 m. The checker said:

```
FAIL  reachability
      - BM->AL (jump): needs 128% of jump, impossible; gap 3.6m vs reach 2.82m at rise 1m:
        shorten the gap to <= 2.82m, lower the landing, or add a node
```

Lowering the alcove 0.5 m raises the reach to 3.53 m, and moving it 1 m closer makes the jump 74%: skill-adjacent but not over the 75% depth-axis warning. The current tables pass (tier estimate 3, Medium).

**Why it works** (the hidden-detour contract in `references/jump-puzzles.md` §2): the reward is seen before the route (from the lift, every ride); one take-off cue (the rubble steps, then the broken railing); a miss costs a fall to the lift bottom with damage, not death, and the checkpoint is beside it (2 links of replay); the reward sits at the end; the drop loops back so nobody walks back along the beam. **Not modelled:** the lift's timing window (state it: 1 s at 2 m/s), camera framing in the shaft, and whether the alcove's light reads at the lift's speed. Playtest those.
