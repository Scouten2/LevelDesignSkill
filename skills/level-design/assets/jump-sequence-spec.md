# Jump Sequence Spec

Fill this for any 3D jump sequence, embedded jump puzzle, traversal route or movement map, and for 2D levels that aren't tile maps (method: `references/platformer-3d.md`). The four tables are the input to `scripts/jump_links.py`, so keep the headers. A filled, passing example is in `assets/example-jump-sequence.md`. Write "assumed" next to any number that wasn't read from code or measured in a gym.

```
Sequence:                       Type: detour | optional puzzle | chamber | movement map | critical route
Think / Do / Think+Do:          Concept (one line):
Reward (sized to the risk):     How it's discovered (vantage, cue):
Camera mode: fixed | rail | hinted free | free     Failure model: A safe-ledge respawn | B checkpoint | C catch ledges | D progress loss (opt-in only)
Target tier (1-8):              Target retries / expected deaths:
```

## Kit

| Kit | Value |
|---|---|
| units | m |
| player_width | |
| player_height | |
| damage_fall | |
| lethal_fall | |
| fall_from | apex |

`damage_fall`: drops this high or more hurt; `lethal_fall`: this high or more kill; `fall_from`: whether your game measures falls from the jump's apex (default) or the take-off. (`safe_fall` is only used when there's no `damage_fall`.)

## Moves

One row per traversal move, from code or a gap-ladder gym; use the reliable value (what testers make 9 times in 10). Distance = flat edge-to-edge running jump; Height = apex rise of the feet; Range = straight-line reach (grapple, swing); Rise = highest ledge a mantle or grab takes (with Distance as its reach). Combined moves are their own rows: jump + mantle, jump from a standstill, re-jump off a sinking block. Gate = yes for a modifier technique such as crouch-jump: it's graded on distance only, since its extra height is a yes/no gate. Built in: `walk`, `drop`, `ladder`, `ride`, `blocked`.

| Move | Distance | Height | Range | Rise | Gate |
|---|---|---|---|---|---|
| jump | | | | | |

## Nodes

Every place the player stands: ledges, beams, lift cars (at the moment of the jump), rest spots. Roles: `start`, `goal`, `checkpoint`, `rest`, `reward`, `secret`. Landing = top size in units, along X then the other horizontal axis ("2x3"). X/Y/Z = centre of the landing top (Z up; `--up y` for Unity/Godot). With coordinates, gaps are computed rectangle to rectangle and the checker scans every unlisted pair for skips. Visible from = nodes this landing can be seen from (it drives the blind-jump and vantage checks).

| Node | Role | Landing | X | Y | Z | Visible from | Note |
|---|---|---|---|---|---|---|---|
| | start | | | | | | |
| | goal | | | | | | |

## Links

One row per traversal. Gap = horizontal edge-to-edge distance; Rise = landing height minus take-off height. Leave both blank to compute them from coordinates. Camera: `across` (screen plane), `along` (depth axis), `diagonal`, `first-person`. Fail: `respawn N`, `fall N`, `death`, `restart`, `none`. Dir `both` = also traversable backwards. Window = seconds for a timed jump (sinking block, lift step-off). Move `teaser` = seen but must look impossible; `teaser:MOVE` = reachable only with a later ability; `blocked` = a pair in jumping range that a wall, railing or ceiling stops (silences the skip scan).

| From | To | Move | Gap | Rise | Camera | Fail | Dir | Window | Note |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

## Views and notes

- **Section view** (side) with heights, and **plan view** (top) with a camera arrow per area; mark the take-off cue and the reward's sightline. In text, draw them from the node coordinates at a stated scale ("1 char = 1 m"), so they can't drift from the tables.
- **State changes** (a ladder kicked down, a gate opened, a bridge collapsed): one spec per state, checked separately, e.g. first visit and after the shortcut opens.
- **Timing**: every lift, mover, crumbling floor or timed jump with period, travel and window in seconds (the checker treats `ride` as not modelled).
- **Unmodelled risks**: camera collision spots, surfaces that might read as climbable but aren't, latency (online), art that could hide the cue.

Check: `python3 -I scripts/jump_links.py this-file.md [--teaches MOVE] [--critical-max 1.0 for opt-in expert content]`. Repair until it passes (≤ 3 rounds), then quote the result in one plain line.
