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
| safe_fall | |
| damage_fall | |
| lethal_fall | |

## Moves

One row per traversal move, from code or a gap-ladder gym. Distance = flat edge-to-edge running jump; Height = apex rise of the feet; Range = straight-line reach (grapple, swing); Rise = highest ledge a climb or mantle takes (with Distance as its reach). `walk`, `drop` and `ride` are built in.

| Move | Distance | Height | Range | Rise |
|---|---|---|---|---|
| jump | | | | |

## Nodes

Every place the player stands: ledges, beams, lift cars, rest spots. Roles: `start`, `goal`, `checkpoint`, `rest`, `reward`, `secret`. Landing = top size in units ("2x3"). X/Y/Z = centre of the landing top (Z up; `--up y` for Unity/Godot). Visible from = nodes this landing can be seen from (it drives the blind-jump and vantage checks).

| Node | Role | Landing | X | Y | Z | Visible from | Note |
|---|---|---|---|---|---|---|---|
| | start | | | | | | |
| | goal | | | | | | |

## Links

One row per traversal. Gap = horizontal edge-to-edge distance; Rise = landing height minus take-off height. Leave both blank to compute them from coordinates. Camera: `across` (screen plane), `along` (depth axis), `diagonal`. Fail: `respawn N`, `fall N`, `death`, `restart`, `none`. Dir `both` = also traversable backwards. Move `teaser` = seen but must look impossible; `teaser:MOVE` = reachable only with a later ability.

| From | To | Move | Gap | Rise | Camera | Fail | Dir | Note |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## Views and notes

- **Section view** (side) with heights, and **plan view** (top) with a camera arrow per area; mark the take-off cue and the reward's sightline.
- **Timing**: every lift, mover, crumbling floor or timed jump with period, travel and window in seconds (the checker treats `ride` as not modelled).
- **Unmodelled risks**: camera collision spots, surfaces that might read as climbable but aren't, latency (online), art that could hide the cue.

Check: `python3 -I scripts/jump_links.py this-file.md [--teaches MOVE] [--critical-max 1.0 for opt-in expert content]`. Repair until it passes (≤ 3 rounds), then quote the result in one plain line.
