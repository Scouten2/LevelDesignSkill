# Platformer Craft (2D and 3D)

## Contents
1. The method: kit, concept, beats, rhythm, geometry, checks
2. One concept per level, four beats
3. Worked example: World 1-1, measured in tiles
4. Teaching ladders and first encounters
5. Rhythm groups and rest platforms
6. Rule trust and surprise
7. Failure severity
8. Optional layers
9. Secrets, hidden and vertical routes
10. Enemies as obstacles, platforms and tools
11. Moving platforms, crushers and timing
12. Difficulty across a world
13. Flow, momentum and speedrun-friendly design
14. 3D platformers: course, sandbox, mission world
15. Authoring order and deliverable
16. Review checklist
17. Levels to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Companion files: numbers and budgets in `platformer-metrics.md`, camera in `platformer-camera.md`, paper checks and the reach script in `platformer-checks.md`, general teaching and pacing in `principles.md`, height as a design axis in `verticality.md`.

---

## 1. The method: kit, concept, beats, rhythm, geometry, checks

Platformers are where "mechanics drive space" is most literal: every gap, ledge and ceiling is a statement about the movement kit. Work in this order and don't skip ahead to geometry.

1. **Freeze the movement kit** as numbers (`assets/movement-kit.md`, `platformer-metrics.md` §2). If the user has none, propose one and label it assumed.
2. **Write a one-line concept** and a four-beat table (§2). The concept is one mechanic in one context ("crumbling floors over a rising lava line").
3. **Write each beat as rhythm groups** (§5): the actions the player performs, with timing, before any geometry.
4. **Fit geometry from the kit's bands** (`platformer-metrics.md` §6): every jump gets a (Δx, Δh) and a band.
5. **Join groups with rest platforms**; put checkpoints, camera reframes and rewards there. Write the per-region camera spec (`platformer-camera.md` §5).
6. **Run the checks** (`platformer-checks.md`): paper checks, `platformer_reach.py`, `beat_lint.py`, `level_metrics.py`. Report numbers, not impressions.

Prove it in grey: a platformer level that isn't fun as untextured blocks won't be saved by art. Art then has to keep safe, hazardous and one-way surfaces readable; re-check them after every art pass.

## 2. One concept per level, four beats

Hayashida (Super Mario 3D Land interview, 2012) became "a lot more rigorous" on 3D Land about levels "where you have a clear concept in the beginning, and that's carried through absolutely all the way"; Galaxy 1 had put "lots of different gameplay concepts in a single stage." His four steps, modelled on four-panel manga (kishōtenketsu): "learn how to use that gameplay mechanic", then "a slightly more complicated scenario", then "something crazy happens that makes you think about it in a way you weren't expecting", then "demonstrate, finally, what sort of mastery you've gained over it." Miyamoto stressed the third step: "That ten [twist] that really surprises people."

- **The twist is a new use of the same mechanic**, not a new mechanic. A new mechanic in beat 3 breaks the one-concept rule.
- **Concept sentence test** [convention]: if the concept needs "and", it is two levels or one concept plus a garnish; demote the garnish.
- **Four-beat table** (put it in the brief):

| Beat | Geometry that forces it | Variable changed | Failure cost (§7) |
|---|---|---|---|
| Learn | single instance, safe ground, unavoidable | none | free or knock-back |
| Develop | 2–3 instances, one variable raised | e.g. gap width | hazard respawn |
| Twist | same mechanic, new context or reversed role | context | checkpoint |
| Mastery | short combination, then goal | combined | checkpoint |

- **Worked template (crumbling platforms)**: Learn, one crumbling platform over solid floor; Develop, a chain of three over a short pit; Twist, crumbling platforms you must break to open a path below; Mastery, chain plus break-through, then the goal.
- "Cakewalk Flip" (Super Mario 3D World) is a popular example of the structure, but the reading is analysts' framing (GMTK), not Hayashida's.
- **Length**: 3D Land sized a stage to a train ride of "a couple of stations", clear or Game Over, after Galaxy stages took "10, 20, or even 30 minutes" (Hayashida, 2012). Pick a target play time per level and design to it.

## 3. Worked example: World 1-1, measured in tiles

Counts from the VGLC tile map of Super Mario Bros. 1-1 (202×14 tiles; columns from the left edge) and the Mario-AI annotated copy. The beat labels are this guide's reading, not Nintendo's; 1-1 predates Hayashida's framing.

| Columns | What is there | Reading |
|---|---|---|
| 3 | Start on open flat ground | free space to try the controls |
| 16 | First ?-block, 3 empty tiles above the floor | reward before threat |
| 20–24, 22 | Block row; a second ?-block 4 rows higher | teaches that blocks are platforms |
| 21 | First Goomba, about one 16-tile screen in, walking toward Mario | Learn: stomp or hop; a death here costs ~18 tiles |
| 28, 38, 46, 57 | Pipes 2, 3, 4, 4 tiles tall, Goombas between | Develop: a jump-height ladder, one variable, top value repeated |
| 64 | Hidden 1-up block | secret for the curious |
| 69, 86 | Bottomless pits 2 and 3 wide | pits arrive only after jumping is learned |
| 134–158 | Stair pyramids 4 high; the second pair has a 2-wide pit between the tops | Twist: stairs and pits combined |
| 181–189, 198 | 8-tall staircase, then the flagpole | Mastery: climb and choose how high to hit the pole |

Lessons to reuse: **first threat about one screen in, after a reward; ladders vary one parameter and repeat the top value; early pits sit far below the kit's limit.** A 1×1-tile reach model needs about a 5-tile apex and 6-tile run jump to finish 1-1 (it stops at the 3- and 4-tall pipes with less), so the 2–3-tile pits use well under half of the jump. Late difficulty in SMB comes from *more and denser* gaps (8-1 has 18 one-tile pits plus pits of 2–6), not from making every gap near-max. Miyamoto wanted players to "gradually and naturally understand what they're doing" (Kerr, Game Developer, 2015). The bonus pipe and hidden blocks let experts skip much of the level (Wikipedia's 1-1 article, citing Eurogamer and 1UP).

## 4. Teaching ladders and first encounters

- **One variable per rung**; repeat the top value once before moving on (2-3-4-4).
- **First encounters are safe, unavoidable and framed**: the lesson can't be skipped, failure costs nothing, and the element is fully on screen. `--teaches` in `platformer_reach.py` checks "unavoidable" mechanically (`platformer-checks.md` §4).
- **Don't punish while teaching** (Hodent's rule; McMillen: "When you are trying to teach someone something, you don't punish them when they make a mistake"). Put the first spike row over solid floor, the first pit with a floor.
- **Show the hazard working on something else first** [convention]: a crusher flattens a crate, a laser cuts an enemy.
- **Pickups as trajectory hints** [convention]: a coin arc draws the jump line; a trail into a pit edge says "this is makeable".
- **Designers underrate their own difficulty.** Wonder's team "didn't think it was that challenging" until a tester kept falling at the opening jumps, and fixed it with more freedom (Nintendo, *Ask the Developer* Vol. 11, 2023). Make mandatory content easier than feels right (`fun-checks.md`).

## 5. Rhythm groups and rest platforms

Launchpad builds levels from "rhythm groups, which are short, non-overlapping sections of a level made up of a rhythm and geometry"; the rhythm is "that which players feel in their hands", and groups are joined by "a small platform that acts as a rest area" (Smith & Whitehead, 2010). Its parameters make a usable spec:

- **Rhythm type**: regular (even beats), swing ("a short followed by long beat, like a heartbeat"), random. **Density**: low, medium, high. **Length**: 5, 10, 15 or 20 s.
- Write each group as an action string before geometry, e.g. `RG3 (swing, 10 s, medium): R J . J(+1) W1.0 J(Δx5,Δh-2)` where `R` run, `J` jump, `.` short beat, `W1.0` wait 1 s, `(+1)` lands 1 tile higher.
- Swing and spring-heavy rhythms constrain geometry: a spring jump needs far more airtime than a short hop.
- **Rest platforms** ≥ 3 tiles flat and ≥ ~1 s of calm [convention]; they hold the checkpoint, the camera reframe and often a reward.
- **Screen = rhythm group = checkpoint = refill** in screen-based games: Celeste's code refills dash and stamina on every screen transition, so every screen is solvable from its entry state. Never require a resource carried in from the previous screen unless that is the explicit puzzle.
- **Dead air**: no stretch over ~5 s without an action or decision unless it is a deliberate rest beat [convention].
- **Music-synced courses** need designers who think in beats; Wonder's level designers "didn't know much about beat or meter" and trained with the sound team.

## 6. Rule trust and surprise

- **Keep core affordances stable.** "We all know pipes are solid… Keeping this feeling of trust in a side-scrolling 2D Mario game was crucial" (Sato, Wonder, 2023). A surface that looks solid is solid; a hazard looks like a hazard every time.
- **Put at least one surprise in every level.** Mouri wanted "at least one element in each course that would surprise or delight players", chosen over difficulty-scaled variations; "take everything to the extreme. If you think you've gone too far, you can make adjustments later." Name the surprise in the brief.
- **Surprise changes the situation, never a promise.** The Wonder effect transforms the course in plain view. Fake floors, hidden blocks over pits and invisible walls are rule breaks: allowed only off the critical path and telegraphed. Kaizo "troll" design inverts fairness deliberately for an audience that opted in.

## 7. Failure severity

Choose one rung per section and justify it in the beat chart:

1. **Knock-back or bump**: lose position, not progress.
2. **Fall to a lower route**: lose time; the level catches you (Sonic's low roads [unverified]).
3. **Hazard respawn** at the last safe ground or screen entry (Celeste screens; Hollow Knight spikes [unverified]).
4. **Checkpoint respawn.**
5. **Level restart**: only for micro-levels (Super Meat Boy).
6. **Progress loss**: only when loss *is* the design (Getting Over It, which still adds "outcroppings designed for you to hook onto when falling").

McMillen: "(Percent chance the player will die) X (Penalty for dying) = Difficulty"; Super Meat Boy could be very hard because it removed lives, made respawn "almost instantaneous" and kept "the goal always in sight." Compute the retry budget per section (`platformer-metrics.md` §9) and make every death attributable: the player should see what killed them and why.

## 8. Optional layers

- **Keep the main path comfortably inside the kit; put the hard version beside it**, visible, so players opt in knowingly. Optional layers never block the main ending.
- **Collectibles off the critical path**: Celeste strawberries sit behind optional platforming and are lost if you die while carrying one, so they test the route *and* the return.
- **Expert remixes** of the same idea: Celeste B-sides; Super Meat Boy's dark world, unlocked by beating a level "under a set par" ("Dark world 1-5 is almost as difficult as level 3-5"); Celeste's golden strawberry, where one death restarts the chapter.
- **Assists and badges**: 3D Land offers an assist block after 5 deaths and rewards never triggering it with "five stars that are sparkling"; Wonder's badges include beginner aids (auto-bounce out of pits) and challenge badges. Thorson: strawberries, B-sides and Assist Mode "are all there to help players find the challenge level that's right for them." Trigger numbers in `platformer-metrics.md` §10.
- **Quota gates** [convention]: when worlds gate on collectibles (Odyssey moons, Mario 64 star doors), set the quota well below the total so players can skip what they dislike.

## 9. Secrets, hidden and vertical routes

- **Secrets skip or reward; they never block.** 1-1's bonus pipe skips much of the level for experts.
- **Hidden-but-fair**: a hidden route needs its grammar taught somewhere safe, a view of it from at least one vantage (optional content may skip this), an invitation to look (a glint, a coin, a gap in the wall pattern), and a cheap failure. Full rule in `verticality.md` §4, drop signalling in §5.
- **Keep secret tells consistent** [convention]: if cracked walls break once, every cracked wall breaks.
- **No guessing with death as the only feedback** [convention]: "pick the right pipe" or a blind drop is a leap of faith (`platformer-checks.md` §2).
- **Height as progress**: in climbing levels the vertical axis is the progress bar (the other uses of height are in `verticality.md` §2). Give upward look-ahead (`platformer-camera.md` §6), catch ledges if falls lose progress, and a look-back moment at what you've climbed.
- **Layered routes** [convention]: a high route that is faster or richer and needs skill, a low route that is safe; a missed jump drops you to the low route instead of killing you.

## 10. Enemies as obstacles, platforms and tools

- **Obstacle**: an enemy is a moving hazard with a timing window; first ones walk slowly toward the player in open space (1-1's first Goomba).
- **Platform**: stomp-bounces extend reach; if the level needs one, add the bounce height to the kit and treat the enemy as a moving platform in checks (the reach script treats `E` as a hazard).
- **Tool**: shells, throwables and carried enemies open routes. Teach the tool use in the Learn beat like any mechanic.
- **Showcase spaces**: Wonder's designers built "nice gaps for the Goombas to get stuck in" to show off new enemy animations; a safe spot to watch an enemy is a teaching beat.
- Enemy timing is not modelled by the scripts; state patrol ranges and periods in the notes list.

## 11. Moving platforms, crushers and timing

- **State collision semantics** (Thorson, Celeste and TowerFall physics): moving solids carry riders and push actors; push wins over carry; a squeezed actor dies. Never let a crush happen off-screen or without a telegraph.
- **Lift momentum**: Celeste adds a moving platform's momentum to the jump and "stores" it for "a few frames after the platform has stopped moving." Decide whether your kit does this; it changes reachable gaps.
- **Let the player watch one full cycle from safety before committing** [convention]; state period, travel and dwell time in seconds next to the map.
- Moving platforms, lifts and springs are absent from the tile notation; list them with coordinates and expect the reach checker to stop there (`platformer-checks.md` §3).

## 12. Difficulty across a world

- **Sawtooth** [convention]: difficulty rises through a world, drops when the next world introduces its concept, then climbs past the previous peak.
- **Harder = denser and longer, not near-max**: raise gap count, shorten rest platforms, combine known elements, tighten the retry budget; keep critical jumps below 90% of the envelope (`platformer-metrics.md` §6).
- **Show difficulty and allow choice**: Wonder shows a difficulty rating per course and allows non-linear course order. Chosen challenge is enjoyed more than imposed challenge (`fun-checks.md`).
- **Plot it**: per-level leniency and replay cost on one chart; flag any step up of more than one band without a rest or checkpoint (`platformer-checks.md` §6).

## 13. Flow, momentum and speedrun-friendly design

- **Momentum sections** [convention]: runways before long jumps, slopes into launches, no stop-start walls; put the hard stop *before* a flow section, not inside it.
- **Keep the action constant**: instant respawn, fast transitions, no unskippable interruptions (McMillen).
- **Multiple lines through one space** reward mastery: a safe line, a fast line, a collectible line.
- **Speedrun-friendly** [convention]: consistent physics, skippable cutscenes, sequence breaks that don't softlock (run the softlock check on skip routes too), timers and replays where the audience wants them.

## 14. 3D platformers: course, sandbox, mission world

- **Course levels** (3D Land, 3D World, Astro Bot): linear, one concept, four beats, a clear goal. Treat them like 2D levels with a depth axis.
- **Sandbox worlds** (Odyssey kingdoms): dense small spaces, a reward or curiosity on every sightline, a big landmark for orientation, and collecting does not eject the player. Structure is a hub with radiating challenges, not a line.
- **Mission worlds** (Mario 64): one space reconfigured per objective (Whomp's Fortress); many objectives out of order.
- **Depth is the weak axis**: shadow directly under the player and every floating object, countable geometry along depth, wider landings for depth-axis jumps, and jump aids where judgement is hard (3D Land kept Tanooki's slow fall as an optional aid). Camera rules and 3D-specific checks in `platformer-camera.md` §8–9.
- **Choose the space with the camera**: Galaxy's small planets let the team tune play "without ever having to think about the camera" (Koizumi, MIGS 2007).

## 15. Authoring order and deliverable

Spelunky's generator is a good hand-authoring order (Kazemi, *Spelunky Generator Lessons*): a solution path across a 4×4 room grid first; rooms typed by guaranteed exits (left-right, plus bottom, plus top); 10×8-tile room templates filled to honour those exits; then probabilistic hazards and 5×3 obstacle chunks.

1. **Path graph**: rooms or screens as a Mermaid graph with the critical path, optional rooms, `↓drop(one-way)`, `↑ladder`, `⇅lift`.
2. **Room contracts**: per room, entry and exit sides, entry state (resources, power-ups), beat and rhythm group, failure rung.
3. **Fill**: geometry per room from the kit bands; chunks ≤ ~40×20 tiles per `grid-conventions.md`.
4. **Hazard pass**: add hazards and enemies last, then re-run reach (hazards change which landings are safe).
5. **Checks and report**: lint, reach with `--teaches`, metrics, beat chart lint; list unmodelled features.

Deliverable: kit table, concept and four-beat table, path graph, beat chart with replay costs and checkpoints, ruled grids per room with key-object and notes lists, camera spec per region, script output quoted, open risks.

## 16. Review checklist

- [ ] Movement kit frozen as numbers (or assumed values labelled) before any geometry
- [ ] One-line concept; four beats each name the geometry that forces them; the twist reuses the mechanic
- [ ] First encounters safe, unavoidable, fully on screen; `--teaches` passes for the level's concept
- [ ] Teaching ladders change one variable per rung
- [ ] Rhythm groups written as action strings (type, density, 5–20 s) and joined by rest platforms
- [ ] Every screen or section completable from its entry state
- [ ] Failure rung chosen per section; retry budget within target (`platformer-metrics.md` §9)
- [ ] No affordance behaves unlike its look on the critical path; at least one named surprise
- [ ] Optional layer present (collectible, harder line, expert remix) and never required
- [ ] Hidden routes meet the hidden-but-fair rule; no leap of faith on the critical path
- [ ] Enemies, movers and springs listed with coordinates, timing and semantics
- [ ] Difficulty curve across the world plotted; no unsupported spikes
- [ ] 3D: shadows under player and floating objects; landmark per area; depth jumps have wider landings
- [ ] Script results quoted (reach, teaches, metrics, beat lint) with what wasn't modelled

## 17. Levels to study

- **Super Mario Bros. 1-1** (teaching ladder) **and 8-1** (late-game gap density).
- **Celeste**, Chapter 1 screens (screen = rhythm group) and any B-side (expert remix of the same idea).
- **Super Meat Boy**, a light-world level and its dark-world twin (retry economics).
- **Super Mario Bros. Wonder**, any course with a Wonder effect (surprise without breaking rules).
- **Super Mario 3D Land** (one concept per course, assist block) and **Super Mario 3D World** "Cakewalk Flip".
- **Super Mario 64** Whomp's Fortress (mission world) and **Super Mario Odyssey** Cascade Kingdom (sandbox density).
- **Super Mario Galaxy** planetoids (space shaped around the camera).
- **Spelunky** (path-first room generation) and **Getting Over It** (progress loss as the design; catch ledges).
