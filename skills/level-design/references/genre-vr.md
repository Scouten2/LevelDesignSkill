# VR Level Design

## Contents
1. Comfort is geometry
2. Build the locomotion test map before any level
3. Locomotion-agnostic critical paths
4. Room-scale levels
5. Scale, density and arm's reach
6. Heights, drops and verticality in VR
7. Threat pacing: tools before threats
8. Third-person and diorama VR
9. Greybox and playtest in the headset
10. Review checklist
11. Levels to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Core theory lives elsewhere: verticality functions in `verticality.md`, metrics method in `metrics.md`, fun checks in `fun-checks.md`, comfort and motion options in `accessibility.md`. This file covers what changes when the player's head is the camera.

---

## 1. Comfort is geometry

In VR, vection (seeing motion the inner ear doesn't feel) causes sickness, and level geometry controls how much of it the player gets. Treat layout, wall distance and texture as comfort settings, not only as art. Meta's current guidance (Meta Horizon docs, "Locomotion – Virtual environments" and "Locomotion comfort and usability", 2025) gives the rules:

- **Flat critical paths.** "Limit movement to flat surfaces and avoid slopes and stairs when possible." Slopes cause vertical acceleration and vection.
- **Slopes, not stairs, when height must change.** Use "gentle slopes instead of stairs, minimize steps, and reduce texture details" in stair and elevator areas; or put teleport nodes on slopes and stairs.
- **No spiral staircases.** Forward movement is the most comfortable; avoid layouts that force strafing, back-stepping, spinning or continuous turning. Route the player so the next goal is ahead, not behind or circling.
- **Distant walls.** Textured surfaces near the eye create optic flow; prefer "open spaces or large rooms that keep users away from walls". [convention] Start smooth-locomotion corridors around 2.5–3 m wide and test narrower ones in the headset.
- **Low-noise surfaces near the camera path.** Use "solid textures and minimize visible edges or noise in art style". Grates, tiles, stripes and busy decals on walls and floors the player moves past are comfort bugs, not just style choices.
- **Climbs and gaps become teleports.** For climbing, teleport the player to a safe spot near the top or bottom; for a gap, "use a teleport with a warping mechanic" rather than a physical leap.
- **Speeds.** Measure routes at walking ~1.4 m/s and running ~2.8 m/s (Meta), not at flat-game sprint speeds. Quantised velocity (instant stop/walk/run) is more comfortable than gradual acceleration.
- **Stable camera height and predictable motion.** Keep camera elevation stable over uneven terrain; users are less uncomfortable when they can predict camera motion, so lifts and moving platforms should move at constant, telegraphed speed.
- **Static rest frames help.** Cockpits, cabins and opaque peripheral geometry reduce optic flow (Meta). In a between-subjects study (N=90), a static rest frame reduced sickness and a dynamic one didn't (Peripheral Teleportation, arXiv 2025). Give lifts and vehicles a cabin frame.
- **Frame rate is a level budget.** Valve's SIGGRAPH 2021 talk states VR needs 90+ fps for PC VR. Note: that PDF (often cited as "Half-Life: Alyx locomotion slides") is about **NPC foot animation**, not player locomotion; cite it only for the frame-rate line. Budget draw distance, density and dynamic lights per room accordingly.

## 2. Build the locomotion test map before any level

Meta: "Create a test environment that encompasses all potential locomotion scenarios… a variety of slopes, materials, doorway dimensions, step heights, path obstructions, tunnels, and ceilings of various heights, as well as features like ledges and ladders." Build it first; derive the project's metrics from it (see `metrics.md`).

- Add the VR-specific cases: teleport targets on edges and near walls, gaps of increasing width, squeezes, lifts, low pipes, a seated play position, and a room-scale boundary.
- Run every locomotion mode (smooth, teleport, any shift/blink variant) and both tall and short (or seated) testers through it. Record which cases cause discomfort, collision bugs or false "I can fit there" readings, and write the results into the level metrics sheet.

## 3. Locomotion-agnostic critical paths

Half-Life: Alyx shipped Continuous, Shift and Blink locomotion. Valve's stated teleport goals: "ensure the end player position is a valid place for the player's body and that the path to get there is viable" (Greg Coomer, UploadVR). Robin Walker framed it as "traversal, not teleporting": the game computes the path, NPCs "saw you move across", and footstep and clothing sounds play along it.

- **The critical path completes in every mode.** Time it in each. Never require smooth-movement timing (a closing door, a moving platform) without a teleport-valid alternative.
- **Use a normalised body for teleport validity.** Tall testers kept hitting low pipes and players didn't duck before teleporting, so Valve validated teleports against a standard minimum body size (PC Gamer). Validate every destination against one capsule.
- **Gaps that look passable must be passable.** Testers said they could reach a spot "by squeezing through a gap, catapulting over an object or sliding under an obstacle"; Valve allowed squeezing through gaps a person could plausibly fit, not grates or cracks. If a gap isn't passable, make that obvious (stance 9: make impossible clearly impossible).
- **Ledges and ceilings.** Peeking over ledges risks accidental falls: use a wider collision capsule or a "short leash" for the head. Tall users hit low ceilings and short users get blocked: use dynamic capsule height or a collision-free camera (Meta).
- **Camera-collision policy.** Without it, players see into hidden areas and interact through walls. Collide with solid objects or blank the view inside invalid space (Meta). Check every secret and sequence gate against head-through-wall peeking.
- **Seated play.** Support it unless incompatible: artificial turning ("not all chairs spin"), crouch toggle, must-use objects reachable seated. Snap-turn increments: 15, 30, 45, 90 or 180° (Meta).
- **Teleport costs orientation.** Teleportation "causes little to no VR sickness" but brings "lower presence and an increase in spatial disorientation"; spatial updating is worst for point-and-teleport (Frontiers in VR mini-review, 2021). Compensate with strong landmarks visible across teleport hops and a forward-facing route (`layout-and-flow.md`). In multi-user VR, others can't predict a teleporter's path, so show destinations or traversal.

## 4. Room-scale levels

When the game uses only the real play area, the room is the level (Owlchemy Labs, *Job Simulator*).

- **Minimum area.** Job Simulator "requires 2m x 1.5m minimum of space… you won't need to teleport" (Owlchemy staff, Steam). Design the layout for the minimum, then for larger size classes.
- **Hand-build size variants.** Alex Schwartz: scaling the room "wouldn't give the right feeling", so they chose "'hard mode' — to manually build a number of sized rooms, lay out each by hand", with automatic detection of which to use (Meta developer blog).
- **Forward anchor, nothing behind.** "There's a 'forward' where the window is… things to your right and left, and minimal things directly behind you" (Schwartz, MCV/DEVELOP). Nothing the player wants may sit behind a real wall. Put main interactables in a forward ~180° arc.
- **Throw and swing into open space.** A parent reported a child punching a wall while throwing an item (Steam thread). Aim throw targets, swing interactions and lunges toward the centre of the play area, never toward its edges.
- [convention] Real-world dimensions read instantly in VR: doors ~2.0–2.1 m, counters ~0.9 m, ceilings ≥2.4 m. Keep must-grab items roughly between waist and shoulder height; avoid required floor-level grabs for seated and mobility-limited players.

## 5. Scale, density and arm's reach

- **Large VR spaces feel empty.** Astro Bot Rescue Mission's cut multiplayer levels "were too large and felt empty. There wasn't enough use of verticality or perspective" because the camera had to fit four players; the team cut multiplayer and "Levels such as Vertigo-go appeared as the new benchmark" (PlayStation Blog). Interaction density substitutes for distance.
- **Arm's-reach dioramas.** Moss: "In every scene, you have a spot to be… they're all laid out like a diorama, just in your arms' reach… because we wanted the game to heavily feature physical interaction" (Tam Armstrong, Polyarc, GamesBeat).
- **Every room adds something.** Alyx was built room by room around the question "what happens in this room that hasn't happened in any of the previous rooms and fits into where we're going with the next room?" (Walker, Road to VR). Use it as the verb-per-space test (`fun-checks.md`) for each room.
- Spend detail where hands go (tables, shelves, interactables) more than on distant set dressing; save vistas as rewards. [convention]

## 6. Heights, drops and verticality in VR

Height is stronger in VR because the body reads it directly, so it is both a powerful tool and a comfort risk. The eight functions in `verticality.md` still apply; the means change.

- **Look up and look down are cheap.** The head moves freely, unlike a gamepad camera that players "park" at one pitch, so previews above and below land well. [convention] Use them for preview/survey and aspiration (Astro Bot's use of perspective is the model).
- **Move the player vertically without moving the camera vertically.** Climbs teleport to the top or bottom (Meta); lifts get cabin frames and constant speed; avoid long smooth slopes and stairs on the critical path.
- **No involuntary falls.** An unchosen fall is both a comfort failure (uncontrolled vertical acceleration) and a fairness failure. Protect ledges with a leash or wider capsule (Meta); make the "drop" verb a deliberate teleport or fade. [convention]
- **Sell height with sound.** Playtesters expected louder landing sounds after teleporting from high to low, so Valve added them (UploadVR).
- [unverified] Hand-over-hand physical climbing is often tolerated better than stick-driven vertical motion because motion follows the player's hands. Test it in the test map before relying on it.
- **Acrophobia is real fear, not just discomfort.** Use exposed heights deliberately for meaning (a vista, a dare), never as a mandatory long walk; offer a railing or an alternative. [convention]

## 7. Threat pacing: tools before threats

VR amplifies threat because the enemy is in the player's personal space.

- **Introduce tools before threats.** Alyx: "You get the gun and you get the ammo before you have any kind of threat to you whatsoever… we didn't want to overwhelm people from the very beginning" (PC Gamer).
- **Cut fast lungers.** Valve cut fast headcrabs and fast zombies: "The shock of having that guy come around the corner and latch onto you before you'd even know what was going on was just too much" (Dario Casali). Give enemies readable approach time and lanes.
- **Threats come from the forward arc.** Players backpedalling or spinning under smooth locomotion is the least comfortable motion (Meta), and room-scale players shouldn't need to turn around. Put spawns and approach routes ahead or to the sides; put cover and the next objective ahead so fights move forward. [convention]
- [convention] Physical reloading, aiming and grabbing slow players down; plan lower enemy counts and longer gaps between waves than in the flat-screen equivalent and verify in playtests.

## 8. Third-person and diorama VR

- **Root the player; move the scene.** Moss keeps the player at "a spot to be" per scene, then "the next thing is around you"; page-turn sounds signal the scene change. Rooting avoids motion-sickness complaints.
- **Use the body as a camera control.** Astro Bot's developers describe "360 gameplay in VR while keeping the experience comfortable, and how moving your body gives you a unique perspective" (PlayStation Blog). Hide secrets that require leaning or looking around a corner; make sure the critical path never does.
- **Design each scene readable from one position**, with the avatar's route inside a comfortable head-turn range. [convention]
- **Modular chunks pay off.** Astro Bot's cut Canyon section was re-skinned into the Volcano stage.

## 9. Greybox and playtest in the headset

- **Review greybox only in the headset.** Scale, wall distance and reach can't be judged on a monitor. [convention]
- **Prove the physical verb first.** In VR the core verb is often a hand interaction; prove grab-throw-manipulate against the space in grey before art (stance 11). Then re-check comfort after the art pass, since texture noise arrives with art.
- **Playtest by room.** Alyx's room-by-room development used individual playtests [unverified: snippet only]. Log a comfort rating per room per locomotion mode, and include VR novices plus tall, short and seated testers.
- *Boneworks* is a useful cautionary case: reviews call it physics-first with "one-note" level design and "real motion sickness" [unverified: review snippet].

## Review checklist

- [ ] Locomotion test map built and run in every locomotion mode, with tall, short and seated testers
- [ ] Critical path flat or gently sloped; no spiral stairs; climbs and gaps are teleport/warp points
- [ ] Routes face forward; no required strafing, backpedalling or circling
- [ ] Walls kept distant on smooth-movement paths; low-noise textures near the camera path (re-checked after art)
- [ ] Route times measured at 1.4 / 2.8 m/s; lifts move at constant, predictable speed with a cabin frame
- [ ] Every teleport destination valid for the normalised body capsule; looks-passable gaps are passable or clearly blocked
- [ ] Ledge leash or wide capsule; ceiling/height policy; camera-collision policy checked against secrets and gates
- [ ] Seated mode playable; artificial turning; must-grab items within waist-to-shoulder band
- [ ] Room-scale: designed for 2 × 1.5 m minimum, size variants, forward anchor, nothing wanted behind the player, throws aimed at open space
- [ ] Each room adds something new; dense interaction within arm's reach; no large empty spaces
- [ ] Heights used for meaning; no involuntary falls; landing audio sells height
- [ ] Tools before threats; no fast lungers; threats approach from the forward arc
- [ ] Frame-rate budget (90+ fps on PC VR) checked per room

## Levels to study

- **Half-Life: Alyx** (Valve): the opening chapters (tools before threats), any dense interior for locomotion-agnostic layout and body-valid squeezes.
- **Job Simulator** (Owlchemy Labs): the office and kitchen rooms for forward anchor and room-scale sizing.
- **Moss** (Polyarc): any chapter, for rooted diorama scenes at arm's reach.
- **Astro Bot Rescue Mission** (Team Asobi): "Vertigo-go" as the team's own benchmark level for verticality and perspective.
- **Boneworks** (Stress Level Zero): as a contrast case for physics-first design and comfort [unverified].

Sources: Meta Horizon design docs (virtual environments; comfort and usability; best practices); Game Developer, UploadVR (×2), PC Gamer (×2) and Road to VR on Half-Life: Alyx; Valve SIGGRAPH 2021 NPC-locomotion slides; Owlchemy (Steam thread, Meta blog, MCV/DEVELOP); GamesBeat (Moss); PlayStation Blog (Astro Bot ×2); arXiv 2502.15227; Frontiers in VR 2021 teleportation review.
