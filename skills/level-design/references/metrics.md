# Metrics & Scale

## Contents
1. Rule: everything derives from the player character
2. What to measure, and how to get it in-engine
3. Jump math, gap bands and falls
4. Dead zones: buffer every capability threshold
5. Derived dimensions
6. Reference real-world sizes
7. Engine units and default-value traps
8. The metrics gym (test level)
9. Grid and modular snapping
10. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Engine values are labelled **verify in your project**: templates, versions and project settings change them. Platformer movement kits, gap and height bands, drop bands tied to the kit and retry budgets live in `platformer-metrics.md`; height as a design axis and general drop bands in `verticality.md`.

---

## 1. Rule: everything derives from the player character

- The Level Design Book defines metrics as "the sense of scale, distance, and measurements across the entire level / game." Metrics are a property of the *game*, not of one level: fix them before production so art can swap in final assets at matching sizes (doors, wall heights, stair sizes, jump gaps).
- **Measure, then freeze.** Write the numbers into a metrics doc early and change them only deliberately; every change invalidates built geometry.
- The most common greybox failure is building to eyeballed scale instead of the actual capsule and movement values. Eyeballed levels almost always come out too big **[convention]**.
- Express every dimension two ways: absolute units *and* the metric it derives from ("corridor 2.0 m = 2.4 × player width"). If player metrics are unknown, state assumed values and how to measure them before giving any size.
- Non-human players get their own table. A wolf-sized player in one student project: width 1 m, entrance clearance 1.5 m, minimum doorway 3 m. Don't reuse human door sizes for vehicles, creatures or mechs.

## 2. What to measure, and how to get it in-engine

| Metric | Why it matters | How to obtain (generic) |
|---|---|---|
| Collider/capsule radius & height | Hard minimum for every opening; nav fit | Read the character's collision component. Unreal stores *half* height (total = 2 × half height). |
| Eye / camera height | Sightlines, cover that hides vs reveals, window/railing heights | Camera socket or camera component offset from feet. |
| Walk / run / sprint speed | Traversal times, encounter timing, map size, jump distance | Movement component max speeds. Verify with a stopwatch run over a measured 10 m strip. |
| Jump apex height | Ledge heights: reachable vs not | Compute from jump velocity and gravity (§3), then confirm on a stepped test wall. |
| Jump horizontal distance | Gap widths | Compute at run *and* sprint speed, then confirm on a gap ladder (§8). Air control changes it. |
| Step height | Which ledges are stepped over vs need a jump; stair rise | Movement "max step height" / character controller "step offset". |
| Max walkable slope | Which ramps/terrain are walkable vs slide | Movement "walkable floor angle" / "slope limit". |
| Crouch height | Crawlspaces, cover heights, vents | Crouched collider height (crouch speed too). |
| Mantle / climb reach | Which ledges are climbable | Traversal system parameters; test with a ledge ladder. |
| Camera type, FOV, boom length | Corridor width, ceiling height, framing | Camera settings. Third person: boom length + collision probe size. |
| AI nav agent radius/height/step/slope | Whether enemies can follow the player | Navmesh agent settings; visualize the navmesh. Often differs from the player capsule. |
| Weapon/ability ranges | Engagement distances, arena size | Weapon data; effective (not max) range. See `genre-action-combat.md`. |

- **AI is a separate client of the space.** A gap the player fits through can break pathing. Check every new opening against the *largest* nav agent and every jump/drop the AI must use (nav links).
- Measure **effective** values in play, not only the config numbers: acceleration, coyote time, ledge forgiveness and animation root motion all change what players can actually do. Reference point: Celeste's released code uses 0.1 s of coyote time and ½-tile corner correction (`platformer-metrics.md` §2).

## 3. Jump math, gap bands and falls

Symbols: `v` = vertical take-off velocity, `g` = effective gravity magnitude (base gravity × gravity scale), `s` = horizontal speed at take-off, `Δh` = landing height relative to take-off (positive = higher).

```
Apex height          h_max = v² / (2g)
Time to apex         t_up  = v / g
Airtime (flat)       t_air = 2v / g
Horizontal distance  d     = s × t_air            (flat; no air control)
Land Δh higher/lower t(Δh) = (v + sqrt(v² − 2gΔh)) / g     d(Δh) = s × t(Δh)
                     (Δh > h_max → unreachable; Δh < 0 → longer airtime, longer reach)
```

- Unreal exposes this directly: max jump height = JumpZVelocity² / (2 × |GravityZ|), and `GetMaxJumpHeight` computes it.
- These formulas assume constant horizontal speed and no air control, variable-height jumps, apex hang, double jumps or coyote time. Treat the computed value as a ceiling and **confirm in-engine**. Forgiveness windows (coyote time, corner correction) are slack for human error: band gaps without them.
- Landing on a ledge needs the *feet* (collider bottom) to clear the edge, and the collider's radius gives a little extra reach at both edges **[convention]**. Engines handle ledge edges differently (perching, ledge-snap, mantle assists) — test the real behavior.

**Worked example** (Unreal-style values, `verify in your project`): v = 700 cm/s, base gravity 980 cm/s².

| Case | g | h_max | t_air (flat) | d at s = 500 cm/s |
|---|---|---|---|---|
| Gravity scale 1.0 | 980 | 700²/1960 ≈ **250 cm** | 1.43 s | ≈ 714 cm |
| Gravity scale 1.75 | 1715 | 700²/3430 ≈ **143 cm** | 0.82 s | ≈ 408 cm |

Using the gravity-scale 1.75 row:
- Land on a ledge **100 cm higher**: t = (700 + √(490000 − 343000)) / 1715 = (700 + 383) / 1715 ≈ 0.63 s → d ≈ **316 cm**.
- Land **100 cm lower**: t = (700 + √(490000 + 343000)) / 1715 = (700 + 913) / 1715 ≈ 0.94 s → d ≈ **470 cm**.
- Engine default for comparison: v = 420 cm/s at gravity scale 1.0 gives ≈ 90 cm apex (`verify in your project`).
- Lesson: a 250 cm apex is floaty; many projects raise gravity scale. Never reuse jump numbers across projects.

**Gap bands** **[convention]**, as % of the measured maximum at the same Δh (anchored on Super Mario Bros. 1-1, whose pits are 2–3 tiles, far under a full running jump; details in `platformer-metrics.md` §5–6):

| Band | Gap as % of measured max | Use |
|---|---|---|
| Intro / tutorial | ≤ ~40 % | First encounters. |
| Routine critical path | 50–75 % | Works with imperfect take-off, analog input, lag. |
| Signposted skill check | 75–90 % | Deliberate, after a checkpoint. No critical jump above 90 %. |
| Optional / expert | 90–100 % | Only where retries are cheap and nothing gates on it. |
| Unreachable but looks possible | 100–~130 % | **Avoid.** Players burn lives and trust trying it. |
| Clearly impossible | ≥ ~150 %, or a visibly huge drop / no landing affordance | Boundaries, vistas, foreshadowed later routes. |

Apply the same bands to ledge heights versus apex/mantle reach (routine ledges ≤ ~70 % of apex).

**Falls.** Fall-damage thresholds given as impact speed convert with h = v² / 2g at the game's effective gravity. Classify every drop as free / committed / costly / lethal from these numbers: general bands and signals in `verticality.md` §5, platformer bands tied to the movement kit in `platformer-metrics.md` §8.

## 4. Dead zones: buffer every capability threshold

Schatz (Naughty Dog, "Defining Environment Language for Video Games", 80.lv, 2017) buffers metrics so nothing sits where the player can't tell whether it works:

- **Ledges:** Drake reaches a ledge "3.5m or less above him", so no climbable edge may sit between **3.25 m and 4 m**.
- **Slopes:** walkable surfaces are under a 35° grade, and the team "enforced a rule of no surfaces between 30 and 45" degrees (the article's own numbers; the 30/35 mismatch is in the source).
- **Low cover:** 0.9–1.25 m tall rectilinear objects, with nothing similar within **0.5 m above or below** that range.
- **Walkable ground:** even, hardened surfaces larger than 1.0 m in length and width.

Generalise to your own metrics [convention]: for every capability threshold (jump apex, gap distance, mantle reach, crouch height, step height, walkable slope), list the values the player can't use and keep a buffer of roughly −7 % to +15 % around the threshold empty of anything that looks usable (Schatz's ledge zone is −7 %/+14 % of 3.5 m). Pair it with her placement rule: objects that must read as affordances need "a border zone" free of competing detail (`principles.md`).

## 5. Derived dimensions

Let `W` = collider width (2 × radius), `H` = standing height, `Hc` = crouched height, `E` = eye height.

| Element | Hard minimum | Recommended | Notes |
|---|---|---|---|
| Doorway / opening width | `W` + small margin | 110–140 cm (real doors) | Doors narrower than corridors so a frame reads. The Level Design Book's Unity example: door 1.25 × 2.5 m. |
| Doorway height | `H` + margin | 210–230 cm (+10–20 cm frame) | Taller for third-person cameras and jumping through. |
| Corridor (1P, 1 player) | > `W` | ≥ 2 × `W`; LDB example 2.0 m min hall | Combat corridors need room to dodge **[convention]**. |
| Corridor (3P) | — | `W` + camera arm room each side + margin | MY.GAMES: passage width = capsule + two camera arms + margin. In practice ≥ 200–300 cm **[convention]**. |
| Co-op corridor | 2 × `W` side by side | ≥ 2 characters abreast + margin | Avoid single-file chokepoints that block a partner unless intended. |
| Crawlspace / vent | `Hc` + margin | `Hc` × ~1.2 **[convention]** | Must read as crouch-only from outside. |
| Ceiling (1P) | `H` + jump clearance | ≥ `H` + h_max + margin where jumping happens **[convention]** | Low ceilings = refuge/tension; high = prospect/awe. |
| Ceiling (3P) | camera clearance | Higher than 1P; boom must not clip **[convention]** | Test with camera collision on. |
| Stairs | rise ≤ max step height | 15 cm rise × 30 cm depth (WoLD) | Collision as a ramp is common; check walkable slope. |
| Ramp | slope < walkable limit | Several degrees under the limit **[convention]** | A slope at the exact limit slides on some frames. |
| Half cover | ≥ `Hc` (hides crouched player) | ≈ waist height, under `E` so player can see/shoot over **[convention]** | Derive from measured crouch height; no sourced standard numbers. |
| Full cover | ≥ `H` | ≥ `H` + margin; wide enough to hide `W` with lean room **[convention]** | Third-person cover adds camera offset. |
| Railings / windowsills | — | Below `E` if sightlines matter, above `E` to block **[convention]** | Eye height decides what a wall reveals. |
| Jump gap | — | Routine band (§3) | Skill-check band signposted; optional band off the critical path. |

- Third-person cameras need wider corridors and higher ceilings than the capsule suggests; first-person needs attention to eye height and FOV for sightlines.
- Doors and openings must also pass the largest **AI agent** and any carried object or vehicle.
- Halo 2's editing kit lists 40 units as the minimum path width for a player — every shipped game has its own table; build yours.

## 6. Reference real-world sizes

| Item | Size | Source |
|---|---|---|
| Player height | ~180 cm (≈ 6 ft); 50 × 50 × 180 placeholder | WoLD UE5 scale guide |
| Door | 210–230 tall × 110–140 cm wide, +10–20 cm frame | WoLD UE4 guide |
| Stair step | 15 cm rise × 30 cm depth | WoLD UE4 guide |
| Hallway | ≥ 2 × player width; e.g. 2.0 m | Level Design Book |
| Door (Unity example) | 1.25 × 2.5 m | Level Design Book |
| Greybox door height | 200 cm common | **[convention]** |
| Counter / table | ~90 / ~75 cm | **[convention]** (real-world) |
| Storey height (floor to floor) | ~300 cm real; games often 350–450 for readability | **[convention]** |
| Shipping container | ~244 wide × 259 high × 610 or 1220 cm long | **[convention]** (ISO standard; handy cover/landmark unit) |

Real-world sizes are a starting point. Games routinely exaggerate doors, ceilings and corridors for camera and readability; keep proportions consistent within the game.

## 7. Engine units and default-value traps

| Engine | 1 unit = | Up axis | Example defaults (`verify in your project`) |
|---|---|---|---|
| Unreal | 1 cm | Z | Base `ACharacter` capsule radius 34 / half height 88; movement JumpZVelocity 420, MaxWalkSpeed 600. Third Person template capsule 42 / 96 (84 cm wide, 192 cm tall), JumpZVelocity 700 reported. Recalled (unverified): MaxStepHeight 45, WalkableFloorAngle ≈ 44.77°, CrouchedHalfHeight 40; navmesh agent radius ~34–35, height 144, step 35, slope 44. |
| Unity | 1 m | Y | **[convention]** CharacterController defaults recalled as height 2, radius 0.5, step offset 0.3, slope limit 45°. |
| Godot | 1 m | Y | **[convention]** CharacterBody3D floor max angle recalled as 45°; collider size is whatever the shape is set to. |
| Source (CS:GO etc.) | ≈ 1.9 cm (0.75 in) | Z | Player 32 units wide, 72 tall (WoLD). |
| Doom | power-of-two map units | — | Textures in multiples of 8/16/32 (LDB). |
| Quake | "nominally an inch" | Z | No consistent scale in practice (LDB). |

- **Template-vs-default trap.** In Unreal, the engine class defaults (34/88, JumpZ 420) differ from the Third Person template (42/96, JumpZ 700), and newer template variants may differ again. Some tutorials use 35/90. Always read the actual character in the user's project before giving numbers.
- **Unit trap.** Asset scale is lost between DCC tools and engines (cm vs m, Y-up vs Z-up). Import a 180 cm reference figure and the metrics gym kit first, and check them against the capsule.
- Half-height vs full height: Unreal capsule half height 96 means 192 cm tall, not 96.

## 8. The metrics gym (test level)

A dedicated level, built before production levels, containing every metric measured and labelled **[convention]**:
- **Gap ladder:** gaps at 25/50 cm steps from 50 % to 150 % of computed max, at Δh = −200, 0, +50, +100 cm. Mark the measured success limit at run and sprint.
- **Ledge wall:** heights in 10–25 cm steps covering step height, jump apex, mantle reach and climb limit; mark each threshold's dead zone (§4).
- **Drop tower:** drops at each band edge (free, committed, costly, lethal) to confirm fall-damage thresholds.
- **Slope ramp set:** angles in 5° steps around the walkable limit.
- **Openings:** door widths/heights from hard minimum to generous; crawlspaces; vents.
- **Corridors:** widths with the camera in its real mode, including turns (third-person cameras fail on corners first).
- **Cover set:** low/half/full heights with the real crouch, lean and aim.
- **Ranges:** ground markings at engagement distances for each weapon class.
- **Lighting & readability swatches:** walkable/climbable/hazard materials under level lighting.
- **AI lane:** the same openings and jumps tested by each nav agent type.
- Re-run the gym after any movement, camera or animation change. It doubles as a regression test for the whole game's levels.

## 9. Grid and modular snapping

- Pick one grid and keep it. Power-of-two grids (8/16/32/64…) are traditional because Doom-era tools and textures were built on them (Doom textures in multiples of 8/16/32). Quake shows the cost of loose scale: its unit is nominally an inch with no consistent scale.
- In metric engines a 50 cm / 100 cm grid (or 25 cm sub-grid) is common **[convention]**. In Unreal, power-of-two grid snaps (16, 32, 64, 128 uu) are also common **[convention]**.
- Size modular pieces to the grid and to metrics: wall height, door module, stair module, corridor module, and transition pieces between kits. Bethesda's modular kits (Skyrim, Fallout) depend on strict sizes so pieces snap; see `process.md`.
- Snap greybox geometry; off-grid blockouts become impossible to convert into kits and hide metric errors.
- Keep pivots at predictable corners or centres so swapping greybox for final art does not shift geometry **[convention]**.

## 10. Review checklist

- [ ] Player metrics read from the real character (not engine defaults or memory): W, H, Hc, E, speeds, jump v, gravity scale, step, slope, crouch, mantle
- [ ] Units and up-axis stated; capsule half-height vs height not confused
- [ ] Jump apex and gap distances computed AND confirmed in a metrics gym; forgiveness windows measured but not counted as reach
- [ ] Critical-path gaps/ledges in the intro or routine band; skill checks ≤ 90 % and signposted; nothing in the 100–130 % zone
- [ ] Dead zones kept around every threshold (ledge, gap, slope, cover); affordances have a border zone
- [ ] Every drop classified free / committed / costly / lethal from the game's thresholds
- [ ] Every opening passes player capsule, largest AI agent, carried objects/vehicles
- [ ] Corridors ≥ 2 × W (1P); camera allowance for 3P; co-op fits two abreast
- [ ] Ceilings clear jumps and third-person camera
- [ ] Stairs within step height (15/30 cm default); ramps under walkable slope with margin
- [ ] Cover heights derived from measured crouch/stand/eye height
- [ ] Engagement distances match weapon ranges
- [ ] Grid chosen and geometry snapped; modular pieces sized to metrics
- [ ] Metrics doc written, frozen, and re-verified after movement/camera changes

Sources (details in `SOURCES.md`): The Level Design Book (Metrics, Doom/Quake metrics, Modular); Schatz, 80.lv 2017; WorldOfLevelDesign UE4/UE5 and CS:GO scale guides; Epic CharacterMovementComponent API; Celeste `Player.cs`; MY.GAMES cinematic techniques (camera arms); H2 Editing Kit metrics.
