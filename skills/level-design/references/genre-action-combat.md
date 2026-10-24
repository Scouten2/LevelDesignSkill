# Action & Combat Spaces (FPS campaigns, cover shooters, character action, soulslikes, shmups)

## Contents
1. Encounter anatomy (the unit of design)
2. Macro rhythm: arenas, corridors and DOOM's arena rules
3. Combat space vocabulary (cover, sightlines, flanks, entries)
4. Height in combat: high ground with counters
5. Authored vs. systemic: designer hard points and AI
6. Teaching combat and one mechanic per level
7. FPS campaigns (Valve, Bungie, id, Respawn)
8. Third-person cover shooters (Gears, Uncharted, The Last of Us)
9. Character action and melee arenas (God of War, DMC, Bayonetta)
10. Soulslike combat spaces (Dark Souls, Elden Ring)
11. Shmup stages
12. Bosses
13. Review checklist
14. Levels to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Core refs: teaching and pacing in `principles.md`; topology and reveals in `layout-and-flow.md`; the Z-axis in `verticality.md`; engagement distances in `metrics.md`; boss fights in `boss-arenas-and-raids.md`; co-op horde pacing in `genre-coop-pve.md`; fun checks (close contests, cheap failure) in `fun-checks.md`.

---

## 1. Encounter anatomy

- **Design the loop, then vary its context.** Griesemer (Halo, Engadget 2011): "In Halo 1, there was maybe 30 seconds of fun that happened over and over and over and over again." The half usually cut: vary it across environments, weapons, vehicles and enemy combinations, so "no 30 second stretch of Halo is ever repeated." He describes "a 3-second loop inside of a 30-second loop inside of a 3-minute loop that is always different." For each encounter, name the 3 s action, the 30 s tactical problem and the 3 min arc, and say what differs from the previous encounter.
- **Phases: enter → read → plan → execute → resolve.** Damian Isla (Bungie) describes an encounter as entering a space, planning an approach, then executing it. Give each phase a spatial answer:
  - **Enter:** a threshold crossed deliberately (door, ledge, crest), ideally with a vantage.
  - **Read:** enemy groupings and roles visible from that vantage; landmarks that name sub-areas.
  - **Plan:** at least two viable approaches (direct, flank, high ground, stealth opener).
  - **Execute:** room to move between positions; no dead ends that trap the player.
  - **Resolve:** a clear end state (last enemy, door opens, music drops) and a rest beat with pickups. [convention]
- **Two time scopes.** Bungie's "Illusion of Intelligence" (Butcher & Griesemer): design owns the ~3-minute strategic scope (where the fight goes, fallback lines, reinforcement beats); AI owns the ~30-second tactical scope. Sketch the strategic plan per encounter and trust the AI for moment-to-moment play.
- **Start enemies unaware.** Halo 3's best encounters let the player scout patrols before engaging. Put the entry vantage before the detection boundary.
- **Make the player think about space.** Straley's principle via Benson Russell (Uncharted 2): the best encounters make the player think about and move around the space. If optimal play is standing still, the encounter has failed.
- **Every fight feels distinct.** GoW 2018 tuned encounters to the end so each felt different (Barlog). Change at least one of: enemy mix, space shape, height, objective, tools. [convention]
- **Aim for a narrow win.** Close contests are the most enjoyed (see `fun-checks.md`). Set an expected outcome per set piece: narrow win, not a walkover or a wall.

## 2. Macro rhythm: arenas, corridors and DOOM's arena rules

- **Baseline: corridor–arena–corridor–arena.** Critics called DOOM 2016 a "pulsing rhythm" of this; Gears links "combat bowls" with confined corridors. Corridors compress and rest; arenas release. Chart it on the beat chart (`process.md`).
- **Then break it.** For DOOM Eternal, Marty Stratton said id made arenas bigger and put enemies in connecting corridors to break the pattern. Adam Saltsman names two tall-arena types:
  - **Jungle gym:** distinct floors joined by traversal (bars, pads, ledges); rewards vertical movement.
  - **Canyon:** open, fewer layers; rewards lateral circling and long reads.
- **Push-forward combat** (Campbell & Loudy, GDC 2018). DOOM removed regenerating health, reloading and cover; the player takes what they need from enemies. Reloading went because it broke flow; double jump was added to close distance (Tommy Thompson, "Cyber Demons", 2018). Paraphrased: the player is not trapped with the demons, the demons are trapped with the player. (Do not quote the "locked in a room with YOU" line; it could not be found.)
- **"Combat chess" is Stratton's phrase** (Game Developer, 2017): speed of movement, distinct demons, distinct weapons, player power, and "make me think, make me move." id's verified arena rules came from playtests where players backed into walls and chokepoints, "a cheesy way to play":
  1. **Ranged demons hold position.** "Demons, except for melee demons, should hold their position."
  2. **Cap melee chasers.** "We can't put too many melee demons in [an arena] at the same time… If all the pieces moved all at the same time towards you, chess becomes very much not fun." Let the player "engage one guy… and then move on to the next."
  3. **Line-of-sight breakers without camping spots.** Give "opportunities to break line of sight with certain enemies, but force them to keep moving." Every occluder is a pass-through, not a bunker: no enclosed corner with one entrance.
  4. **Size the arena to feel fast.** "The right size arena, with just the right amount of space, actually made the player feel even faster" (Martin). Test sizes on a movement test map before dressing.
- **Arena layout consequences:** medium-to-large, asymmetric, vertical, closer to multiplayer maps than campaign rooms; loops around a central structure for repositioning and height; resources placed to pull the player through enemies rather than into a corner. [convention] Health and armour at edges and along loops, not the centre; waves spawn out of direct view (rim portals); heavies arrive in later waves; the arena stays locked until the last wave.
- **Don't script the path.** Eternal's mission docs never scripted the route through an area. Write the intent and beats, not a walkthrough.
- **Retreat space is a dial.** Regenerating-health shooters need somewhere to recover; DOOM removes it to force pressure. Decide which game you are making. [convention]

## 3. Combat space vocabulary

- **Cover is a sightline tool first.** TLDB: cover is "any object or structure that blocks a sightline or shields someone from attack", classified by height, width, solidity, facing, verticality, corners, permanence and authorship. Respect cover-height dead zones (`metrics.md`: Naughty Dog keeps nothing within ±0.5 m of the 0.9–1.25 m low-cover band).
- **Less cover is often better** (TLDB). Leave gaps so moving between cover is a decision; wall-to-wall cover makes every position equal.
- **Avoid fuzzy cover.** Epic's Gears map theory: Mansion's columns and railings make players think they're safe "when they're really not"; TrainStation uses simple, readable geometry. Railings, thin columns and see-through props must read unambiguously as cover or not-cover.
- **Place cover perpendicular to expected fire** (Epic). State each piece's purpose in the spec ("low wall, faces the balcony gunners").
- **Cover shapes flow.** Gears cover is "set up really, really deliberately to allow for flow through the environment" (Osieja). Lay cover chains that suggest the forward path.
- **Pinner/flusher pairs.** Gears' Pinner keeps you in cover, the Flusher forces you out: a long lane for one, a flank route for the other. Cover is never permanently safe.
- **Sightlines sized to weapons.** [convention] Short favour shotguns and melee, mid rifles, long snipers; break long lines where sniping shouldn't dominate. Distances in `metrics.md`.
- **Flanks both ways.** [convention] A main approach plus a side route that wraps toward the enemy flank; enemies get flanks too, so the player can't turtle.
- **Enemy entry points.** [convention] Reinforcements arrive out of view but from a readable source (doors, dropships, rim portals); never behind the player without a telegraph, never into an area the player just cleared and is watching.
- **Combat bubble.** [convention] The volume where AI is active; leaving it resets or ends the fight. Halo-style AI uses designer zones and firing positions and pulls squads back as they lose members.
- **Movement penalties must pay.** A Naughty Dog pre-production test found players disliked wade-height water that gave nothing back. Slowing terrain needs a reward (cover, stealth, shortcut).

## 4. Height in combat: high ground with counters

Combat position is one of eight functions of height (`verticality.md` §2); use the others too (preview the arena from above before the fight, see the exit from below).
- **High ground needs a counter.** [convention] Reachable at a cost (exposure on the climb, a long route), and contestable: a sightline onto it, a flank route up, or a hazard that denies it. One-way drops let the player commit forward.
- **Limit floor planes.** Most maps "max-out at three different floor planes for any given area" (TLDB, Verticality). Merge minor height changes into one floor.
- **Fit the input.** Gamepad players "park their camera's vertical rotation" near head height; "high frequency height variation… will frustrate gamepad users"; flying enemies should keep moderate distance and stable height (TLDB). Put critical threats within normal camera pitch.
- **3D movement needs lanes.** Titanfall 2 tamed wall-running with a "window pane" effect of left, middle and right lanes, because point-to-point 3D routes "become a mess" (Fukada, Shacknews 2016).
- **Draw a section.** Any arena with two or more floor planes gets a side view with floor indices and `↓drop(one-way)`, `↑ladder`, `⇅lift` edges (`verticality.md`).
- **Nav links for AI.** Author drop, jump and ladder links for every vertical connection enemies should use; note deliberate gaps as player escape routes.

## 5. Authored vs. systemic: designer hard points and AI

- **Uncharted 4 lesson** (Gallant, "Authored vs. Systemic", GDC 2017). Wide-linear spaces and deeper stealth outgrew scripting, and purely systemic position scoring was inconsistent. Fix: designers place **hard points** (strong positions, places to defend); systemic logic decides which NPC uses which.
- Mark hard points, fallback lines and no-go zones per encounter; let AI handle assignment. [convention: the markup format]
- **Validate AI navigation** with the real agent size; a gap the player fits through can still break pathing.

## 6. Teaching combat and one mechanic per level

- **Teach in a flat, safe space.** TLOU's first human combat space is simple and flat; scripted NPCs don't flank, giving players time to read the fight (Silli, GDC 2014; MapCore analysis). Add height and flanking AI after the basics land. Hodent: don't punish while teaching.
- **Foreshadow before the fight.** GoW 2018's first Draugr ambush is foreshadowed; its first arena is circular and open so the player can read enemy behaviour.
- **One mechanic per level, then retire it.** Titanfall 2's Effect and Cause swaps between a ruined present and a working past mid-fight and mid-platforming. Built as **two copies of the level, "one floating directly above the other"**; Respawn spent more time on it than any other level, and Jake Keating's prototype had "some puzzles… some combat encounters, just to show it had some design legs" (Game Developer, 2016). Lessons: prototype the riskiest mechanic with both puzzle and combat uses; budget for exact alignment of stacked copies; show where enemies are in the other layer. [convention] Into the Abyss (moving factory) is the companion example; Respawn prototyped levels as "action blocks" (Dionne, GDC 2018, via 80.lv).
- **Arc:** teach safe → develop → twist → conclude (Hayashida; `principles.md`).

## 7. FPS campaigns

- **Valve's cabals.** The first Half-Life "wasn't any fun… We had some cool levels, but they didn't fit together well"; Valve rebuilt from one prototype level packed with every working idea and settled arguments by watching testers in silence (Birdwell, "The Cabal"). For HL2, cabals mixed level designers and programmers because iteration ran through AI, code and layout together. Put a programmer in the level team when a level depends on new AI or physics.
- **Ravenholm: let the verb define the level.** The gravity gun "ended up defining the level": saw blades and environmental kills instead of guns. [convention] Stage the tool in view before the need.
- **Halo:** discrete encounters across wide outdoor spaces, unaware enemies, constantly changing context (§1).
- **Hybrid stealth/loud.** [convention] Wolfenstein's commanders call reinforcements; spaces support killing them quietly first or going loud. See `genre-stealth-immersive-sim.md`.

## 8. Third-person cover shooters

- **Recipe:** designer hard points with AI occupancy (§5); pin/flush pairs; cover lines for forward flow; flat, non-flanking tutorial spaces.
- **Shared guidelines.** TLOU designers and artists followed common combat-space guidelines (Newman). Write yours as a precious/flexible list so the art pass doesn't break cover readability (`process.md`).
- **Wide-linear and vertical.** TLOU Part II encounters are more open and vertical because of Ellie's movement (Licea, flooded mall); wider verbs justify wider, taller spaces.
- **Stealth-to-combat loops.** [convention] Start unseen; grass and low-cover lanes; a perimeter loop to break line of sight and re-stealth, since enemies search the last known position.
- [convention] Uncharted uses climbable walls as traversal flanks; Gears is mostly planar; TLOU's scarce ammo sits at encounter edges and in optional rooms.

## 9. Character action and melee arenas

- **Open, readable floor.** Melee needs room to circle groups and read tells (GoW 2018's first arena).
- **Camera constrains shape.** GoW 2018's close over-the-shoulder camera with no cuts (Oksuz) means: no tight corners where enemies clip out of view; telegraph offscreen attacks; arenas wide enough to keep threats mostly in frame. [convention] Pair with threat indicators and visible spawn sources.
- **DMC/Bayonetta.** [convention] Flat, mostly convex rooms that lock on entry; few obstacles; room for aerial juggling. Difficulty from wave composition, not geometry; no exploitable chokepoints.

## 10. Soulslike combat spaces

- **Shortcuts turn lines into circles.** Lordran: "a path that could be reached in a straight line is forcibly made into a circle"; the Undead Parish lift back to Firelink is the canonical "aha". End each dangerous stretch with a one-way door, lift or ladder back to the last checkpoint.
- **See it, then reach it.** FromSoftware previews destinations from above or across (Blighttown from Firelink; the Lake of Rot from an Ainsel side path), then pays them off by an unexpected vertical route. Hidden drops must pass the hidden-but-fair rule (`verticality.md`); Stormveil's lower-roof drop is the cautionary case (`genre-dungeon-metroidvania.md` §6).
- **Checkpoint spacing.** DS2's uneven bonfire spacing forced backtracking through repopulated areas. Space checkpoints by difficulty, not distance; pair long stretches with a shortcut. Check replay cost per death (`fun-checks.md`).
- **Checkpoints on high ground.** DS3's High Wall puts pre-boss bonfires on high ground with a view of the route ahead (student analysis; moderate confidence).
- **Moderate ambushes.** DS2 overused ambushes until they felt cheap. An ambush must be readable on the second attempt; never at a checkpoint exit.
- [convention] Teach an enemy alone, then in a group, then on a hazard (ledge, narrow bridge). Legacy dungeons offer a defended main gate and side paths.

## 11. Shmup stages

Source: Carotenuto (Himeki Games), "Designing smart, meaningful SHMUPs" (Game Developer). The stage is a timeline of waves; the screen is the arena.
- **Theme and emotion per stage:** urgency (many fast spawns) or a calmer phase with bigger, fewer enemies. One mechanic or enemy concept per stage; "avoid introducing lots of different mechanic and new enemies in a single level."
- **Waves are puzzles.** "Each one a logical consequence of the other… there should be an elegant, smart solution." Vary each wave's spatial demand (screen region, aimed vs. static fire, from where).
- **Stage template:**
  1. **Gentle opener:** "interesting but not too challenging."
  2. **Develop:** more enemies and twists on the same mechanic.
  3. **Mid-boss** around the middle as a check.
  4. **Mix** the new mechanic with earlier ones.
  5. **Slower lead-in:** "try to go slower… build momentum and anticipation."
  6. **Boss as summary:** "everything you learned", in phases, "like a separate stage in itself" (detail: `boss-arenas-and-raids.md`).
- **Fairness rules:** "Players should always be able to find a way to survive in each situation": never an unsurvivable pattern. No background element "that may be confused with game elements or obstacles."
- **Readability.** [convention] Bullets contrast with every background; player effects never resemble enemy bullets; hitboxes no larger than they look (usually smaller); limit enemy types per stage.
- [convention] Arcade stages often run 2–5 min with deterministic spawn timelines so players can route for score. Survivors-like arenas: `genre-roguelike-procedural.md` §9.

## 12. Bosses

Arena readability, telegraph vocabulary, phases and run-backs are in `boss-arenas-and-raids.md`. Here: put a checkpoint and short run-back before every boss; make the boss test the level's mechanic; build the arena geometry the fight uses.

## Review checklist

- [ ] Purpose stated: what this fight teaches/tests and how it differs from the last; 3 s / 30 s / 3 min loops named
- [ ] Grey description test passes: the fight is interesting described as spaces, heights, enemies and verbs only
- [ ] Entry vantage before the detection boundary; groupings and roles readable from it
- [ ] ≥2 viable approaches; no single dominant spot
- [ ] Arena rules (push-forward games): ranged enemies hold position; melee chasers capped; LOS breakers with no camping corners; size tested for speed
- [ ] Every cover piece has a facing and purpose; no fuzzy cover; deliberate gaps; cover heights outside dead zones
- [ ] Sightline lengths match the weapon set
- [ ] High ground reachable at a cost and countered; ≤3 floor planes; section drawn; critical threats within normal camera pitch
- [ ] Reinforcement entries off-view but readable; none behind the player without a telegraph
- [ ] Hard points / fallback lines marked; AI nav (incl. vertical links) tested at real agent size
- [ ] Resources pull the player through the fight or reward exploration; clear resolve signal, then rest
- [ ] Arena/corridor rhythm broken at least once per level; expected outcome per set piece is a narrow win
- [ ] Third-person: no corners hiding attackers; offscreen threats telegraphed
- [ ] Soulslike: checkpoint with a view ahead; shortcut back after each hard stretch; hidden drops pass hidden-but-fair
- [ ] Shmup: one concept per stage; opener → develop → mid-boss → mix → slow lead-in → summary boss; no unsurvivable pattern; background never mimics hazards
- [ ] Playtest: death map vs. intended danger zones; where players camped or stood still

## Levels to study

- **FPS:** HL2 Ravenholm, Route Kanal, Water Hazard; Halo 3's open encounters; [convention] Halo CE The Silent Cartographer; Titanfall 2 Effect and Cause, Into the Abyss; DOOM Eternal jungle-gym vs. canyon arenas; DOOM 2016 Kadingir Sanctum (Łukasz Maj breakdown); [convention] Foundry and Argent arenas.
- **Cover:** Gears "Knock Knock" combat bowls; Gears MP TrainStation vs. Mansion; Uncharted 4 wide-linear spaces; TLOU first human combat; TLOU Part II flooded mall.
- **Melee / soulslike:** GoW 2018 first Draugr arena; DS3 High Wall of Lothric; DS2 bonfire spacing (counterexample); DS1 Undead Parish lift to Firelink.
- **Shmup:** [convention] An Oath to the Stars (Carotenuto's own game); classic arcade stages with mid-bosses and summary bosses.

Key sources (full list in `SOURCES.md`): Engadget (Griesemer 2011); Game Developer ("Make me think, make me move" 2017; GDC 2018 push-forward preview; "Cyber Demons"; Effect and Cause 2016; Carotenuto shmups; "The Cabal"); Butcher & Griesemer; Saltsman on DOOM Eternal; TLDB (Cover, Verticality); Epic Gears map theory; Gallant (GDC 2017); Shacknews (Fukada).
