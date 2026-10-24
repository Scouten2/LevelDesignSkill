# Platformer Metrics: Movement Kit, Bands and Budgets

## Contents
1. Freeze the kit before the level
2. Reference kit: Celeste's released constants
3. Derived jump envelope
4. The forgiveness layer
5. Super Mario Bros. and generator measurements
6. Gap and height bands
7. The "looks jumpable" zone and dead zones
8. Drop bands tied to the kit
9. Retry budget and checkpoint spacing
10. Assist triggers
11. Filling the kit template and kit JSON
12. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

General jump math (apex, airtime, reach at Δh), engine units and the metrics gym are in `metrics.md`. This file turns them into platformer decisions.

---

## 1. Freeze the kit before the level

- Every platformer number derives from the movement kit: run speed, jump apex and distance at tap and full hold, airtime, air control, forgiveness windows and extra moves. Fill `assets/movement-kit.md` first; a level drawn before the kit is frozen gets redrawn.
- Work in **tiles** (or player widths in 3D) and **seconds**. State the tile size in pixels or metres once at the top.
- If the user has no kit, propose one, label it **assumed**, and design with margins so later tuning doesn't break every jump.
- Measure in a gym (gap ladder, ledge wall; `metrics.md` §8) or read the code. Never estimate jump numbers from a video.
- Any kit change invalidates every gap: re-run `platformer_reach.py` on all levels after tuning.

## 2. Reference kit: Celeste's released constants

From Celeste's released `Player.cs` (pixels and seconds; 1 tile = 8 px, per Thorson's "2 pixels… a quarter of a tile").

| Quantity | Celeste | In tiles | Design meaning |
|---|---|---|---|
| Tile / screen | 8 px; 320×180 view | room view 40 × 22.5 tiles | one screen = one challenge |
| Run speed | 90 px/s | 11.25 tiles/s | converts distance to replay seconds |
| Ground / air acceleration | 1000 px/s²; air ×0.65 | full speed in ~0.09 s | snappy starts; runways barely needed |
| Gravity; max fall | 900 px/s²; 160 px/s (240 holding down) | 20 tiles/s max fall | fast-fall lets players shorten arcs |
| Jump | 105 px/s up, +40 px/s horizontal kick | — | |
| Variable-jump hold | 0.2 s | — | apex range ≈ 4:1 tap vs full |
| Apex hang | gravity halved while \|vy\| < 40 px/s and jump held | — | "more time to adjust for landing" |
| Coyote time | 0.1 s (6 frames at 60 fps) | ≈ 1.1 tiles past the edge at full run | slack for late presses |
| Corner correction | 4 px, jump and dash | ½ tile | head-bonks forgiven |
| Wall-jump reach | 2 px (Thorson); code probe 3 px | ¼ tile | |
| Super wall-jump reach | "I think it's 5 pixels" (Thorson) | > ½ tile | harder move, wider window |
| Dash | 240 px/s for 0.15 s, then 160 px/s | 4.5 tiles | refilled on landing and screen transition |
| Climb stamina | 110; climbing up 45.5/s, holding 10/s, climb-jump 27.5 | ~13–14 tiles up from full | stamina is a vertical budget |
| Hitbox / hurtbox | 8×11 / 8×9 px | 1 × 1.4 tiles | hurtbox 2 px shorter: lenient spikes |
| Jump buffer | not in the released file | — | ~0.08 s is often quoted [unverified] |

Thorson's design rule behind the list: every technique widens "timing or positioning windows… it wants you to succeed" (*Celeste & Forgiveness*).

## 3. Derived jump envelope

Computed by simulating the released constants at 60 fps, full run speed (approximate: ignores pixel snapping):

| Jump | Apex | Flat travel | Airtime |
|---|---|---|---|
| Full hold | ≈ 3.6 tiles | ≈ 8.0 tiles | 0.68 s |
| 12-frame hold | 3.3 tiles | 6.7 tiles | 0.57 s |
| 6-frame hold | 2.0 tiles | 4.8 tiles | 0.40 s |
| 1-frame tap | 0.9 tiles (< 1 tile) | 3.2 tiles | 0.25 s |

- Landing reach at Δh = +1 / +2 / +3 tiles: ≈ 7.3 / 6.7 / 5.8 tiles. Use the reach at the jump's Δh, not the flat number, when banding a gap.
- Dash alone: 4.5 tiles in 0.15 s; jump + horizontal dash ≈ 11–13 tiles (crude).
- A full room is 40 tiles wide: about 3.5 s of running, so per-screen respawn keeps replay under ~4 s.

## 4. The forgiveness layer

Specify these numbers in the kit; they change which gaps feel fair:

- coyote time; jump buffer; apex hang; jump and dash corner correction; semi-solid popping; wall-jump reach; hurtbox smaller than hitbox; lift momentum storage; resource refills (Celeste refills dash and stamina on every screen transition).
- **Scale forgiveness with precision demand**: Celeste's super wall jump gets more than twice the normal reach.
- **Band without the slack.** Measure gaps from the ledge edge with no coyote extension (in Celeste the 0.1 s window adds about a tile of take-off at full run). Forgiveness absorbs human error; if a critical jump needs the coyote window, it is a skill check.

## 5. Super Mario Bros. and generator measurements

Counted from VGLC processed maps (bottomless pits only; lifts and springs are not encoded):

| Level | Pit widths in tiles |
|---|---|
| 1-1 | 2, 3, 2 (pipes 2, 3, 4, 4 tall; final staircase 8 tall) |
| 2-1 | 4, 3, 3, 2 |
| 4-1 | 2, 4, 2, 3, 2, 2 |
| 8-1 | 18 one-tile pits, plus 2, 2, 3, 3, 4, 5, 6 |

- Notch's Infinite Mario generator (Mario-AI Framework): landing pads 2–5 tiles, gaps 2–3 tiles; enemy chance per tile = (difficulty + 1)/35.
- A 1×1-tile reach model (the research prototype of `platformer_reach.py`) fails 1-1 at jump height 3–4 (stopped by the 3- and 4-tall pipes) and passes at height 5, distance 6; 8-1 and 3-1 need distance 8. That is a model's minimum, not SMB's real physics, which were not sourced.
- Reading: SMB's introductions use at most about half the jump; late levels add density and a few longer gaps.

## 6. Gap and height bands

Percentages of the kit's measured maximum at the same Δh (`jump_distance` for gaps, `jump_height` for ledges). All values **[convention]**, anchored on SMB 1-1's 2–3-tile pits, Notch's 2–3-tile gaps, and Celeste's 6-frame hop (4.8 tiles, 60% of full) clearing most early gaps.

| Band | Gap (% of max distance) | Ledge (% of max apex) | Use |
|---|---|---|---|
| Intro / tutorial | ≤ ~40% | ≤ ~50% | first encounters, Learn beats |
| Routine critical path | 50–75% | ≤ ~70% | most jumps |
| Signposted skill check | 75–90% | 70–90% | Mastery beats, after a checkpoint |
| Optional / expert | 90–100% | 90–100% | only where retries are cheap and nothing gates on it |
| Looks jumpable, isn't | 100–130% | 100–130% | avoid (§7) |
| Clearly impossible | ≥ ~150% or no landing affordance | ≥ ~150% | boundaries, vistas, later-ability teasers |

- **No critical-path jump above 90% of the envelope.** `platformer_reach.py --margin 0.9` lists offenders.
- Combine bands: a 75% gap onto a +2 ledge is harder than either alone; band it against reach at that Δh (§3).
- Ceilings over jumps: leave head room ≥ apex + player height where full jumps happen, or the ceiling becomes an unintended limiter (`metrics.md` §5).
- Teaching a jump-height ladder? Make each rung's required height land in a different band, like the 2-3-4-4 pipes.

## 7. The "looks jumpable" zone and dead zones

- A gap or ledge at 100–130% of the kit reads as possible, so players burn lives and trust on it. Make it **clearly impossible** (≥ ~150%, no landing lip, a visible wall or void) or **reachable**.
- Schatz (Naughty Dog, 2017) applies the same idea as metric dead zones: Drake reaches ledges "3.5m or less above him", so no climbable edge sits between 3.25 m and 4 m. Translate to your kit [convention]: keep anything that looks usable out of roughly −7% to +15% of each capability threshold (jump apex, gap distance, dash length, wall-jump shaft width). Precision platformers may use the lower side (90–100%) for optional, signposted content; keep the upper side empty everywhere.
- Ability-gated teasers (a ledge needing the next upgrade) must be far enough past the current kit that nobody mistakes them for a hard jump.

## 8. Drop bands tied to the kit

Classify every drop; the general bands, threshold conversion and signalling rules are in `verticality.md` §5.

| Band | Height | Behaviour | Kit JSON |
|---|---|---|---|
| Free | ≤ jump apex, landing within reach of a way back | two-way, repeatable | — |
| Committed | above apex, below any damage height | safe but one-way: must read as one-way | `safe_fall_height` |
| Costly | at or above the damage height | damage or hazard respawn; only with visible reward or on optional routes | `fall_damage_height` |
| Lethal | kill plane, void, or beyond the lethal height | death | bottom of map = death |

- Most 2D platformers have no fall damage, so the real line is free (reversible) vs committed (one-way). Wall-jump or climb kits make drops beside a wall reversible; say which drops stay one-way.
- Lookalike drops behave alike game-wide. In 3D, 3D Land's testers called one pit fall "so high I'm scared!" and the team readjusted the height: perceived height matters as well as measured.

## 9. Retry budget and checkpoint spacing

McMillen (*Super Meat Boy*): "(Percent chance the player will die) X (Penalty for dying) = Difficulty"; without lives the penalty became "the amount of time you took to restart after death and the length of the current level."

- **Per-section budget** [convention]: P(death) × (respawn + replay seconds) ≤ ~5–10 s for hard sections. At P = 0.5, replay ≤ 10–20 s; at P = 0.9 (Meat-Boy-hard), ≤ ~5 s, i.e. micro-levels.
- **Replay seconds** = distance from the checkpoint ÷ run speed + respawn time + forced waits (lift cycles, enemy patterns, unskippable animations). Celeste: 40 tiles ÷ 11.25 tiles/s ≈ 3.6 s per room.
- **`beat_lint.py`** checks P × replay ≤ 10 s with P ≈ min(1, deaths ÷ (deaths + 1)) from the beat chart's `Expected deaths` and `Replay cost` columns, plus a checkpoint before every beat with ≥ 2 expected deaths and peak intensity never on the beat with peak replay cost.
- Also sanity-check the total [convention]: 6 expected deaths × 15 s replay is 90 s of repetition for a 20 s beat; move the checkpoint or lower the difficulty.

Checkpoint spacing [convention]:

| Game style | Respawn point | Replay target before a beat with ≥ 2 expected deaths |
|---|---|---|
| Precision, screen-based (Celeste) | screen entry | ≤ ~5 s |
| Mainstream course (Mario, DKC) | mid-level checkpoint plus before set pieces | ≤ ~15–20 s |
| Micro-levels (Super Meat Boy) | level start | whole level ≤ ~5–20 s |
| Progress-loss climbs (Getting Over It) | none; catch ledges limit loss | state the worst-case loss |

Place a checkpoint after anything tedious to repeat and before skill spikes and bosses; never make players replay a long easy stretch to retry a hard one.

## 10. Assist triggers

- 3D Land offers an assist block after 5 deaths on a stage (some staff wanted 3); New Super Mario Bros. Wii's Super Guide appears after 8 (Hayashida, 2012). Use these as anchors for a per-segment death counter.
- Celeste's Assist Mode changes game speed, stamina, air dashes and invincibility; Wonder's badges include auto-bounce out of pits. Levels must stay completable when deaths stop happening (no death-required routes, timed elements still passable at slower speeds).
- Author the hooks per level: death counter per checkpoint segment, guide path or assist item spawn point, fatal-pit behaviour under invincibility. Details in `accessibility.md`.

## 11. Filling the kit template and kit JSON

`assets/movement-kit.md` holds the full table. `platformer_reach.py` takes a JSON summary (lengths in tiles, times in seconds):

| JSON key | Fill with | Notes |
|---|---|---|
| `jump_height` | full-hold apex, feet rise in tiles; round **down** to 0.1 | `platformer_reach.py` lets a 1-tall box land on an h-tall step when `jump_height` ≥ h; leave real-game margin on top |
| `jump_distance` | flat full running jump, take-off edge to landing edge | the script fits a parabola to (height, distance) |
| `player_width`, `player_height` | hitbox in tiles, rounded **up** | conservative for clearances |
| `air_control` | `true` if the player can steer mid-air | |
| `coyote_time` | seconds (Celeste 0.1) | |
| `double_jump`, `wall_jump` | booleans | |
| `dash_distance` | tiles, 0 if none | |
| `safe_fall_height`, `fall_damage_height` | tiles or `null` | see §8; check `--help` for exact semantics |

Celeste as a kit JSON (rounded as above):

```json
{"jump_height": 3.5, "jump_distance": 8.0, "player_width": 1, "player_height": 2,
 "air_control": true, "coyote_time": 0.1, "double_jump": false, "wall_jump": true,
 "dash_distance": 4.5, "fall_damage_height": null, "safe_fall_height": null}
```

The model is a parabola with variable height; it ignores apex hang, acceleration, momentum and lift boosts, so treat its margins as approximate and keep critical jumps inside 90%. For 3D kits, use the jump math in `metrics.md` and the paper checks; the script is 2D only.

## 12. Review checklist

- [ ] Kit filled in `assets/movement-kit.md` from code or a gym; assumed values labelled
- [ ] Forgiveness numbers stated (coyote, buffer, corner correction, apex hang, wall-jump reach, refills)
- [ ] Every critical-path jump banded against reach at its Δh; none above 90% of the envelope
- [ ] Intro beats ≤ ~40% gaps; skill checks signposted and after a checkpoint
- [ ] Nothing sits in the 100–130% "looks jumpable" zone; dead zones kept around each threshold
- [ ] Every drop classified free / committed / costly / lethal; lookalikes behave alike
- [ ] Retry budget computed per beat; `beat_lint.py` passes or exceptions justified
- [ ] Checkpoints before every beat with ≥ 2 expected deaths; no long easy replay
- [ ] Assist hooks authored (death counter, guide path, invincibility-safe pits)
- [ ] Kit JSON written and `platformer_reach.py` re-run after any kit change
