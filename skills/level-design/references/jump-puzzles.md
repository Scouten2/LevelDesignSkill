# Jump Puzzles: Hidden Routes, Optional Courses, Hybrids and Movement Maps

## Contents
1. Classify the challenge first
2. The hidden-detour contract (Elden Ring-style)
3. Optional jumping puzzles in a world (Guild Wars 2, Destiny)
4. Challenge chambers (Jedi, tombs, shrines)
5. Puzzle-platforming: keep thinking and doing apart
6. Abilities that reopen the world (Supraland-style)
7. Movement maps and difficulty tiers (KZ, obbies, Celeste mods)
8. Set pieces: escapes, chases, medal courses
9. Anti-patterns
10. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[unverified]** = could not be checked; don't quote it as fact. **[synthesis]** = this guide's generalisation across sources.

Write every sequence in `assets/jump-sequence-spec.md` and check it with `scripts/jump_links.py` (method and 3D craft in `platformer-3d.md`). This file says *what* to build; that one says how to make it readable and checkable.

---

## 1. Classify the challenge first

Fill these in the spec header before drawing anything:

| Field | Options | Why it matters |
|---|---|---|
| Type | hidden detour (§2) · optional puzzle in the world (§3) · challenge chamber (§4) · ability route (§6) · movement map (§7) · set piece (§8) · critical-path traversal | decides discovery, failure model and reward |
| Think / Do | **Think**: the route must be deduced. **Do**: the route is obvious, execution is hard. **Think+Do**: both | never stack a hard Think and a hard Do on the critical path (§5) |
| Target tier | 1–8 (§7) | the checker estimates it; compare |
| Reward | consumable · upgrade or material · cosmetic or achievement · shortcut · vista or lore | size it to the risk; upgrades for the hardest |

## 2. The hidden-detour contract (Elden Ring-style)

FromSoftware's detours are small leaps of faith, each cued by something visible. A fair hidden detour meets all six [synthesis]:

1. **Goal before path.** The reward or destination is seen first: an item glinting from a lift (Raya Lucaria), an alcove across a pit (Hidden Path to the Haligtree). Respawn's rule for Jedi: show the main goal on entry, then let the player take a winding path.
2. **One take-off cue.** An irregularity in the architecture: a broken railing (Haligtree), rubble "formed like steps" (Stormveil), "ground sticking out" in a lift shaft (Raya Lucaria).
3. **A way to test before committing**, where the risk is invisible: Elden Ring's walkthroughs advise dropping a Rainbow Stone to find the invisible floor. A probe item, a thrown object, a visible shadow or a safe peek.
4. **A cheap miss.** Fall damage, not death; or death with the grace site nearby. Long detours get a checkpoint (`platformer-3d.md` §5).
5. **A reward proportional to the risk**, at the end, never along the way.
6. **A loop back**: a one-way drop, a shortcut door or a lift that returns to the main path, so nobody walks back along the hard part.

**Detour recipes** (FromSoftware examples verified on the series wikis):
- **Lift step-off**: a ledge in the shaft that the lift passes. Raya Lucaria's rotating lift: step off mid-ride; on the way up a well-timed running jump reaches an item. Sen's Fortress's lift pauses at a mid-ride exit before a trap; in the Grand Archives (Dark Souls 3) rolling off a moving lift brings a second lift and a Titanite Slab. Cheap to author: one shaft, one ledge, a visible reward. Work out the details [convention]:
  - **Window (s) = (highest step-up the player can make + deepest drop the opening allows) ÷ lift speed.** The opening's clear height caps the drop. Keep it ≥ ~1.2 s; a faster lift needs a taller opening. Put it in the link's Window column.
  - **Make a mistimed try free**: a car-to-wall gap narrower than the player means nobody falls past the car; they ride on and try again on the way back.
  - **The empty car carries on** after a step-off: add call levers at both ends, or the wait for it becomes most of the miss cost.
  - **Engine risks to test**: velocity inherited from the moving car, the player straddling the car lip and the ledge (chamfer the edge so the lintel can't crush them), mantling from a moving platform.
- **Drop chain**: ledges stepped down a cliff or shaft, each a free or committed drop, ending in a cave or item; seen from the top or from across a valley (`verticality.md` §3–5).
- **Rooftop or beam traverse**: a route over the main path's roofs or rafters (Stormveil's lower rooftops), entered through a window or rubble ramp and ending above an enemy or at a shortcut.
- **Invisible or illusory floor**: only with a probe item and a visible destination (Haligtree); never on the critical path.
- **Launcher or spring**: Elden Ring's spiritsprings launch you on Torrent, cancel fall damage and can be chained upward; some in Shadow of the Erdtree must first be woken at a nearby cairn: a mini-puzzle before the jump.
- **"Beat the level designer"**: Supraland puts secrets where "you will think you are about to get out of bounds and beat the level designer", and a chest is waiting. Put a reward on the obvious out-of-bounds line players try, so curiosity pays.

## 3. Optional jumping puzzles in a world (Guild Wars 2, Destiny)

- **They can grow out of the art.** Guild Wars 2's lead designer said the puzzles "just came about as the map artists were playing around"; artists competed to make more, then designers added rewards. A jumping puzzle can be an artist's or level designer's side project; it still needs the checks.
- **Shape**: an entrance disguised as part of the world; the reward at the top or bottom (chest, achievement, often a vista); save points in long ones. Puzzle types seen in Guild Wars 2: timed platforms, wind that pushes you off, cave descents, and clockwork towers.
- **Discoverability is the main failure.** A player critic wrote that without the wiki "it would generally not even be evident that this point was reachable". Give every optional puzzle a vantage that shows the goal and one in-world hint (an NPC line, a note, a visible chest) [synthesis].
- **Social valves**: let players carry others (Guild Wars 2 mesmer portals); Destiny 2's Zero Hour answered Whisper's complaint that weaker jumpers were left behind with switches, reachable only at the end of a section, that make it easier for those still behind.
- **Difficulty by time pressure** (Destiny's Whisper, roughly 40 minutes on normal and 20 on the harder mode [unverified]): a timer raises difficulty without changing a single gap.
- **Camera and latency**: action-MMO controls and cameras weren't built for precision. Guild Wars 2 later added jumper-specific camera options (`platformer-3d.md` §4). Keep timing windows wide online [convention].
- **Don't lock important rewards behind optional jumping.** Final Fantasy XIV players objected when real rewards were gated behind its Kugane tower climb [unverified]; a vista, a log entry or a cosmetic is the safe reward for a pure-skill optional puzzle.

## 4. Challenge chambers (Jedi, tombs, shrines)

- **Self-contained rooms with one idea**, entered from the world and returning to it: Jedi: Survivor's chambers and Fallen Order's Zeffo tombs, Tomb Raider's challenge tombs, Zelda shrines. Teach, develop, twist, master inside the room (`platformer-craft.md` §2; `puzzle-craft.md` for the puzzle half).
- **Keep fights out** while the player is solving: Supraland: Six Inches Under removed enemies from puzzle spaces; Portal's boss failed while action drowned out the puzzle audience.
- **Save the trickiest for those who look**: Jedi: Survivor's level designer said they "save the trickiest challenges for players who are actively looking for them".
- **Players notice when chambers are missing or thin**: Rise of the Tomb Raider added more and larger tombs after criticism of the 2013 game.
- **Readable reset**: a chamber that can break (a physics ball lost in a pit) needs a visible reset or auto-respawn of the object (`puzzle-craft.md` §10).

## 5. Puzzle-platforming: keep thinking and doing apart

- **The route is the puzzle; execution stays easy.** Münnich (Supraland): "once you understand the idea behind a puzzle, you can pretty much immediately solve it instead of having to go through a cumbersome, frustrating execution." Blow confined The Witness's input to grooves so input skill couldn't gate solutions. Valve keeps GLaDOS quiet while players think.
- **Rule**: critical-path Think challenges use routine-band jumps (≤ 75%) and a checkpoint right before; Do challenges have an obvious route; Think+Do lives on optional content or a final mastery beat [synthesis]. Six Inches Under simplified main-path puzzles and moved the hard ones to optional content, much of it after the credits.
- **Route-as-puzzle patterns** (pick one per room):
  1. **Build the path**: the player places the platform (Supraland's cubes, BotW's stasis and magnesis objects, Portal 2's paint).
  2. **Become the path**: take another traversal profile (Odyssey's captures, Astro Bot's power-ups).
  3. **Redirect momentum**: Portal flings turn an unreachable ledge into a velocity problem; introduce one fling type at a time.
  4. **Twist a learned rule** at the end (Braid's key that isn't exempt from rewind; Valve's challenges involve "taking a previously learned rule and turning it on its head").
  5. **Systemic routes**: consistent physics and chemistry rules let players invent a route (BotW).
  6. **Split the route between co-op partners** (It Takes Two).
  7. **Perspective or time** (Braid's rewind; Fez's rotation [unverified]).
- **Failed attempts should be legible**: Münnich wants players to "have seen exactly why it didn't [work]".

## 6. Abilities that reopen the world (Supraland-style)

- **Decide the ability model first.** Persistent, accumulating moves (Supraland, Pseudoregalia, metroidvanias) reopen explored space; level-scoped power-ups (Astro Bot, It Takes Two) give each level a fresh idea but no backtracking.
- **Six-use test.** Münnich "dismissed any ability that didn't at least have six completely different use cases" (his example: a magnet used for climbing and, later, to erase a hard disk). List the uses before adding a move.
- **Loop the world back on itself** so each new ability opens nearby routes, not distant ones (Supraland's world "constantly loops back on itself"). No map was "a central design decision": orientation comes from large distant landmarks.
- **See it before you can reach it.** Show the ledge, chest or door the next ability opens. Mark it in the spec as `teaser:MOVE`: the checker confirms the current kit can't make it (≥ 130% of every current move, so it can't be mistaken for a hard jump) and the later move can.
- **Mandatory gates more visible than optional ones**: Pseudoregalia keeps only five mandatory keys, and after launch enlarged a key-room entrance players were missing.
- **Chainable moves make soft gates**: skilled players will sequence-break. Decide which gates are hard (physical: a weak floor, a hard wall) and run the softlock check on skip routes (`genre-dungeon-metroidvania.md` §9).
- **Reward tiers for observation** [synthesis]: tier 1 secrets where playtests show players wander off the path (Astro Bot) or at the perceived boundary; deeper tiers after the ending (Odyssey adds moons after the credits and gates its Dark Side and Darker Side behind 250 and 500 moons). Give observation rewards mechanical value (Supraland's upgrades), not just a counter.

## 7. Movement maps and difficulty tiers (KZ, obbies, Celeste mods)

Maps that use only the game's base movement, from very easy to near-impossible. **CS2KZ** is the best-documented ladder: 1 Very Easy ("for the average player who has never touched KZ before"), 2 Easy, 3 Medium, 4 Advanced, 5 Hard, 6 Very Hard, 7 Extreme, 8 Death, 9 Unfeasible (TAS only), 10 Impossible; ranked play caps at 8, and an approval team assigns tiers after public testing.

- **Tiers move several dials at once**, not gap width alone. CS2KZ's mapper guide: T1 needs "no multi-strafing" (blocks ≤ 235 units), longjump blocks then step ~240, ~250, ~260, ~270, ~275 and > 275 to T7; T4–T5 add timed and anti-bhop blocks that "force a longjump or pre-keep"; T6 has "sequential intermixed gameplay elements", T7 "almost entirely" so. A tier attaches to a course and movement mode, not to a map: the same course can be T2 in one mode and T5 in another.
- **Which scale?** The table below is for the game's own base kit, with "the move" = the reliable full running jump. Use it for any "KZ-style" or obby request without advanced movement tech. When the game has strafe or bhop tech (CS KZ, surf), measure each technique's envelope as its own move row: in those communities the tiers crowd into the top ~15% of a technique's range (CS2KZ blocks sit at ~83–98% of the GOKZ top longjump threshold) [synthesis].
- **Portable template** [synthesis; calibrate in your game]:

| Tier | Hardest gap (% of the move) | Techniques | Chain without rest | Timing | Checkpoints |
|---|---|---|---|---|---|
| 1 Very easy | ≤ 50% | run + jump | 1–2 | none | short sections, frequent |
| 2 Easy | ≤ 70% | + one basic (air control, mantle) | 2–3 | none | every section |
| 3 Medium | ≤ 80% | + a second (ladder, wall, slide) | 3–5 | gentle | every section |
| 4 Advanced | ≤ 90% | forced techniques appear | 4–6 | some timed blocks | per stage |
| 5 Hard | ≤ 95% | mixed per section | 6+ | common | per stage |
| 6 Very hard | ≤ 100% | sequential mixes | long | tight | sparse |
| 7–8 Extreme–Death | at the limit | everything | almost no rests | frame-tight | optional (PRO runs) |

  The checker's tier estimate follows this table: the hardest link on the easiest route sets the base, and long chains, three or more techniques above 75%, punishing replays and a timed window of 1 s or less each add one.
- **Technique gates** (crouch-jump, a dash-only gap): mark the move `Gate = yes` so it's graded on distance, then place each gate where the base move clearly fails (≥ ~104% of it, so a plain jump visibly almost makes it) and the technique still has margin. Give gate walls one consistent look (the same pipe or rail band) so players learn "this means duck". Teach each gate on a staircase where the plain move works, barely works, then fails.
- **Scan for skips.** On movement maps the checker's skip scan matters most: unintended corner cuts and long-range jumps that skip stages are the classic flaw. List deliberate skips as links and walls that stop the rest as `blocked`.
- **Checkpoints are a separate dial from tier.** KZ splits runs into PRO (no teleports) and TP (checkpoints allowed), so one map serves learners and competitors. Momentum Mod's rules for ranked maps: never send a failing player back before a checkpoint; checkpoints at least ~10 s apart in a good run; reset destinations face forward; start zones big enough to build speed. Easy courses can checkpoint more often; the ~10 s rule keeps competitive splits meaningful.
- **Mapping etiquette** (CS2KZ, Momentum): visible start and end, lighting readable for gameplay, no "jumps along a wall" corridors ("utilize the full 3D volume of your room"), teleports never face backwards.
- **Teach before testing**: Celeste's Strawberry Jam collab has five difficulty lobbies, each with a gym that "teaches you all the tips and techniques you'll need", and a green-to-red meter per map. Build a gym for each technique a tier requires.
- **Length is its own scale**: Eternal Towers of Hell (Roblox) sets length by tower type: 5–6 floors for a steeple, 10 for a tower, 12–25 for a citadel, 30+ for an obelisk.
- **Replay value**: timers, leaderboards, ghosts, bonus routes, and at least one optional shortcut per course (Neon White has one per level and medal tiers from Bronze to Ace). Skips are expected; make checkpoints unskippable.
- **Progress loss is a genre, not a tier.** Getting Over It and Jump King have no checkpoints by design; Only Up! drew criticism for unpolished, random-feeling obstacles. With no checkpoints, readability matters even more.

## 8. Set pieces: escapes, chases, medal courses

- **Escape as final exam**: Ori's escape sequences chain every move learned in an area; Will of the Wisps added checkpoints between segments and lets players replay them [unverified]. Segment long set pieces; never restart a two-minute chase from the top.
- **Adaptive help**: Crash Bandicoot N. Sane Trilogy adds help after repeated deaths (extra masks, extra checkpoints) [unverified]; keep a separate no-death reward for experts. Same principle as 3D Land's assist block (`platformer-metrics.md` §10).
- **Music-locked runs**: Rayman Legends' music levels fix the player's speed so jumps land on the beat, and place obstacles and pickups on musical events.
- **Medal courses**: World of Warcraft's Skyriding races and Destiny's Ascendant Challenges give Bronze for the obvious line; Silver and Gold need resource management and hidden shortcuts [unverified]. Reverse variants reuse the course.

## 9. Anti-patterns

| Anti-pattern | Example | Fix |
|---|---|---|
| Physics change for one section | Half-Life's Xen | keep the kit; teach new moves (`platformer-3d.md` §6) |
| Goal visible only on the wiki | Guild Wars 2 critics | vantage + one in-world hint (§3) |
| Long sequence, full restart | early Ori escapes, Kugane tower [unverified] | checkpoints per segment; failure model B |
| Respawn past a one-way gate | reported Fallen Order bug [unverified] | respawn on the near side; checker `respawn` |
| Precision jumps in a combat engine | Cartwright: jumping in an action engine is hard to make feel right | wider bands, model A respawns, routine gaps |
| Jump targets that appear only up close | Sonic Frontiers critics [unverified] | targets visible from the take-off; `Visible from` column |
| Decoration that reads as a route | false handholds (Schatz removed cracks) | one affordance language (`platformer-3d.md` §2) |
| Hard Think + hard Do on the critical path | Portal's discarded boss versions | split them (§5) |
| Ability teaser that looks makeable | gaps at 100–130% | `teaser:MOVE` ≥ 130% of current moves |
| Important reward behind optional skill | Kugane tower complaints [unverified] | cosmetic or vista for pure skill |

## 10. Review checklist

- [ ] Type, Think/Do, target tier, reward and discovery written before geometry
- [ ] Hidden detours meet all six points of §2; secret nodes have a reachable vantage (checker `visibility`)
- [ ] Optional puzzles: vantage plus one in-world hint; save points if long; a social or skip valve where co-op
- [ ] Chambers: one idea, no combat while solving, readable reset
- [ ] No hard Think and hard Do together on the critical path
- [ ] Each ability passes the six-use test; teasers checked with `teaser:MOVE`; mandatory gates more visible than optional
- [ ] Movement maps: tier dials stated (gap %, techniques, chain, timing, checkpoints); gym per technique; checkpoint rules met
- [ ] Set pieces segmented; help after repeated failure; no full restart of long runs
- [ ] `jump_links.py` result quoted; anti-pattern table scanned
