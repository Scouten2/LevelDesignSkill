# 3D Platforming and Traversal

## Contents
1. The route: kit, link table, checker, fix
2. Readability: one affordance language
3. Depth: the weak axis
4. Camera for jump sequences
5. Failure models and respawns
6. Keep the physics
7. Writing the link table; calibrating in a gym
8. 3D level structures: course, sandbox, mission world
9. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[unverified]** = could not be checked; don't quote it as fact.

Load this for any 3D jump sequence, traversal route, climbing level or movement map, in any genre. Pattern recipes for optional and hidden jump puzzles, puzzle-platforming, ability gates and difficulty tiers are in `jump-puzzles.md`. 2D tile levels use `platformer-craft.md`, `platformer-metrics.md` and `platformer-checks.md` instead.

---

## 1. The route: kit, link table, checker, fix

Prose descriptions of 3D jumps can't be checked, and models misjudge distances in them. Write every sequence as numbers:

1. **Kit**: fill the Kit and Moves tables of `assets/jump-sequence-spec.md` from code or a gym (§7). If the user has none, propose one and label it assumed.
2. **Header**: type, Think/Do label, camera mode, failure model, target tier, reward and how it's discovered (`jump-puzzles.md` §1).
3. **Nodes and links**: one row per standing place and per traversal, with gap, rise, move, camera axis and what a miss does. Coordinates are optional but catch arithmetic slips.
4. **Check**: `python3 -I scripts/jump_links.py spec.md`. It bands every link as a % of its move, finds critical links, softlocks, respawns past one-way links, lethal required drops and falls near the damage thresholds, depth-axis precision jumps, teasers that look makeable, unlisted pairs in jumping range that would skip links, and estimates a tier. Fix and re-run (≤ 3 rounds); its messages say what to change ("shorten the gap to ≤ 3.6 m"). List walls that stop a flagged pair as `blocked` only when the geometry really does.
5. **Views**: a section view and a plan view with camera arrows, then the timing list for lifts and movers.

Bands are the same as 2D [convention]: intro ≤ 40%, routine ≤ 75%, skill ≤ 90%, expert ≤ 100% of the move at that rise. No critical link above 90%; opt-in expert content may go to 100% (`--critical-max 1.0`). Worked example: `assets/example-jump-sequence.md`.

## 2. Readability: one affordance language

- **Schatz's affordance types** (Naughty Dog): cultural and inferred affordances first (a ledge looks like a ledge); explicit and "defined" ones like painted handholds are the fallback. Shape language: rectangles read "usable", rounded shapes safe and unusable, diagonals and points danger. Artists removed rock cracks that read as false handholds near climbable areas.
- **Combined moves are capabilities too**: jump + mantle, jump + ledge grab, a standing jump, a re-jump off a sinking block. Give each its own move row, and check that no route node can be reached early with a combo (the skip scan does this for listed moves).
- **Dead zones** around every capability (Schatz): Drake reaches ledges up to 3.5 m, so no climbable edge sits between 3.25 m and 4 m; walkable slopes stay under 35° and nothing is built at 30°–45°. Apply the same −7%/+15% buffer to your jump distance, jump height, mantle height and grapple range (`metrics.md` §4).
- **What you see is what you get.** Dying Light's rule was that "anything that looked climbable will be climbable"; Supraworld promises "the geometry you see is exactly what you get". The opposite failure is decorative geometry that reads as a route. Decide which surfaces are traversable before the art pass and keep them distinct.
- **Explicit markers (yellow paint)** are contested: Remedy's Control Resonant director rejected them because "Somebody already decided for you"; Mirror's Edge's red runner vision was justified in-fiction, and its level designer Elisabetta Silli noted "Red is an odd choice because it means danger or stop". Default: consistent shape and material language first; add markers where playtests show misses; offer a toggle if you can (Star Wars Outlaws reportedly does [unverified]).
- **One take-off cue per hidden route**: a broken railing, rubble shaped like steps, ground sticking out of a shaft (Elden Ring; `jump-puzzles.md` §2). One irregularity is a cue; ten are noise.

## 3. Depth: the weak axis

- **Shadow straight down**, under the player and every floating object, whatever the light direction. Koizumi (Mario 64): "It might not be realistic, but it's much easier to play with the shadow directly below." 3D Land also drops the player's shadow onto enemies to make stomps easier. In first person, the shadow or a landing marker matters more, not less.
- **Jump across the screen, not into it.** Nesky (GDC 2014, *50 Game Camera Mistakes* #24): players judge distance far better in the plane of the screen. Put precision jumps across the view. A jump along the view axis gets a landing ≥ 3 × player width, a gap no more than 75% of the move, countable geometry along the depth (posts, tiles, coin rows), or a raised camera that shows the gap side-on [convention; the checker warns on all of these].
- **Landing size** [convention, no published 3D number]: ≥ 2 × player width across the screen, ≥ 3 × along it. Narrower beams and posts are fine when deliberate, walked rather than jumped onto, and their failure is cheap.
- **Fixed-angle 3D**: Super Meat Boy 3D built levels around a fixed camera, 45° geometry, 8-way input, and a ground circle plus a height line under the player. Consider this for precision content.
- **Jump aids** where judgement stays hard: 3D Land kept the Tanooki suit's slow fall as an optional aid.
- **Perceived height** is a separate check: 3D Land's testers said a pit fall was "so high I'm scared!" and the team lowered it. Check fear and readability, not just metres.

## 4. Camera for jump sequences

- **Pick the camera mode per sequence** and write it in the spec: fixed or rail for precision and depth-axis jumps; hinted free camera for exploration with set-piece jumps; free for open traversal [convention]. Galaxy's small planets let players "play without ever having to think about the camera" (Koizumi).
- **Nesky's airborne rules** (#22, #25, #28, #45): don't rely on players steering the camera during hard moves; at a ledge, tilt down to show the edge and the player's relation to it; in the air, frame the landing spot (tilt up early, down as the jump loses energy); don't re-aim on every small hop. Designer camera hints help in cramped spaces (#29) but switch off once they've done their job (#36) and never fight the player's input (#34).
- **Frame the feet.** Guild Wars 2 added camera options for jumping puzzlers: lower collision sensitivity (the one with "the biggest impact" for puzzle jumpers), a first-person zoom, and focusing on the character's feet. Lesson: in cluttered puzzles, thin decorative geometry must not trigger camera collision, and the default framing must show footing.
- **Koizumi's three 3D problems**: "problematic depth perception, getting lost, and even getting motion sickness". Fixes: the shadow (§3); one large landmark visible from most of each area; a vertical dead zone so the camera doesn't pan on every jump.
- **Players rarely look up** (Valve) and gamepad players tend to park the camera pitch: anything required above eye level needs structure, light or motion leading the eye, and a retest after the art pass (`verticality.md`).
- **Landing visible at take-off**: on the critical path the landing is on screen from the take-off at the default camera. Use the `Visible from` column; the checker flags blind critical jumps.

## 5. Failure models and respawns

Choose one per sequence and write it in the header:

| Model | What a miss costs | Use for | Examples |
|---|---|---|---|
| A. Safe-ledge respawn | a few seconds; small health cost | action-adventure traversal, anything embedded in a combat game | Jedi: Fallen Order respawns you "to your most recent piece of solid ground" with health loss by difficulty; Prince of Persia's rewind "came first, very early" |
| B. Checkpoint | the section since the checkpoint | optional puzzles, movement maps, chambers | Guild Wars 2's long puzzles have save points you teleport to; KZ checkpoints (TP runs) |
| C. Catch ledges | a partial fall, then you climb again | climbs where falling is the tension | Getting Over It's outcroppings "designed for you to hook onto when falling" |
| D. Progress loss | everything above the landing | opt-in "Foddian" games only | Getting Over It, Jump King |

- **Respawn never behind a one-way link.** Every fall volume maps to a respawn on the near side of every one-way transition (drop, closing gate, collapsing bridge, scripted sequence). A reported Fallen Order bug respawned falls past a scripted gate [unverified]. The checker fails `respawn N` when N can't get back to the take-off.
- **Momentum Mod's checkpoint rules** for movement maps: "the player should not get sent back before a checkpoint when they fail"; checkpoints mark clear progress, are at least ~10 s apart in a good run, and reset destinations never face the player backwards.
- **Failure cost scales inversely with readability.** Bennett Foddy criticises hidden hazards you can only learn by playing "100 times to memorise the position". Instant death is acceptable only with precise controls, a near-instant nearby restart and familiar physics (Ghostrunner's instant restart; Hollow Knight's White Palace keeps the physics and is optional) [synthesis].
- **Tune against a retry target.** Respawn tuned Jedi: Survivor's traversal against a target average number of retries. Write the target in the header, then compare with playtest telemetry.
- **Long sequences need checkpoints**: anything longer than about 3–5 jumps in a game whose controls and camera were built for combat gets model A or B [convention]. The checker warns when a miss replays more than 6 links.

## 6. Keep the physics

Half-Life's Xen is the canonical failure: "the biggest problem is the sudden change in physics", momentum carries the player "over the edge", and nearly every big jump kills (The Game Design Forum). Never change gravity, air control or momentum for one section; if a section needs a new move, teach it there (`platformer-craft.md` §4) and put first uses in the intro band with a cheap miss (`--teaches MOVE`). Online, budget for latency: avoid frame-tight timing in MMO jump puzzles [convention].

## 7. Writing the link table; calibrating in a gym

- No shipped game publishes a text format for 3D jump sequences; the spec's tables are this skill's convention, close to engine nav links. Psychonauts 2's editor previewed jump arcs to place objects "reachable by the intended jump type" (Level Design Book).
- **Gap-ladder gym** before the level: rows of gaps at 50/75/90/100/110% of each move, ledges at the same steps of jump and mantle height, a slope ramp in 5° steps, and a fall tower marking safe, damage and lethal heights (Level Design Book's metrics zoo). Measure with grid textures and record the numbers in the Kit and Moves tables.
- **Ranges, not single values**: kits vary with run-up, input timing and animation; record the reliable value (what testers make 9 times in 10), not the record [convention]. Assassin's Creed III reportedly specified jump ranges such as 0.8–1.2 m [unverified].
- **Units**: Unreal cm, Unity and Godot m, Source units (`metrics.md` §7). State units in the Kit table.
- **One spec per state**: when a shortcut, kicked-down ladder or collapsing bridge changes the graph, check a spec for each state (first visit, after the shortcut).

## 8. 3D level structures: course, sandbox, mission world

- **Course levels** (3D Land, 3D World, Astro Bot): linear, one concept, four beats, a clear goal; treat them like 2D levels with a depth axis (`platformer-craft.md` §2).
- **Sandbox worlds** (Odyssey kingdoms): dense small spaces, a reward or curiosity on every sightline, a big landmark for orientation; collecting doesn't eject the player. A hub with radiating challenges, not a line.
- **Mission worlds** (Mario 64): one space reconfigured per objective (Whomp's Fortress).
- **Embedded traversal** (Elden Ring, Jedi, Guild Wars 2): jump content inside a combat or open world. Patterns in `jump-puzzles.md` §2–4.

## 9. Review checklist

- [ ] Kit and Moves from code or a gym; assumed values labelled; units stated
- [ ] Header filled: type, Think/Do, camera mode, failure model, target tier, reward, discovery
- [ ] `jump_links.py` passes; result quoted in one line; unmodelled items listed (lifts, movers, camera)
- [ ] No critical link above 90% (opt-in expert content ≤ 100%); nothing usable in a dead zone
- [ ] Precision jumps across the screen; depth-axis jumps ≤ 75% with ≥ 3 × player-width landings
- [ ] Shadow or landing marker under the player; one landmark per area; feet framed in cluttered spaces
- [ ] Landing visible at take-off on the critical path; required things above eye level are led to
- [ ] Failure model chosen; every respawn on the near side of one-way links; long sequences checkpointed
- [ ] Physics unchanged from the rest of the game; new moves taught with a cheap miss
- [ ] Traversable and decorative surfaces distinct; art pass re-checked against the spec
