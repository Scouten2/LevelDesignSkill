# Level Design Principles (the canon)

## Contents
1. Dan Taylor's ten principles
2. Guidance cues
3. Lighting order
4. Affordances and readability
5. Teaching mechanics
6. Pacing
7. Spatial psychology
8. Environmental storytelling
9. The level designer's role
10. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

---

## 1. Dan Taylor's ten principles

Dan Taylor (Square Enix Montreal), GDC 2013 talk and the two-part Game Developer article "Ten Principles of Good Level Design" (Sep/Oct 2013), modelled loosely on Dieter Rams. Each title begins "Good level design…". Titles below are the article's headings; cite the article, not talk recaps.

| # | Good level design… | Use it as this check |
|---|---|---|
| 1 | is fun to navigate | "Basic progress through the level should be effortless"; interest comes from verticality, secondary paths, hidden areas. Feeling lost is fine for tension only with "the necessary visual or narrative clues". Navigation must not fight combat (Mirror's Edge kept combat light). |
| 2 | does not rely on words to tell the story | Leave a gap the player closes (Taylor's "broken circle": not too small, not too big). Layers: explicit (text, VO, cutscenes), implicit (mise-en-scène), emergent (the player's own story). See §8. |
| 3 | tells the player what to do, but not how to do it | Objectives distinct by "location, form, lighting and animation"; "players should never be forced to use a singular technique". Prefer several concurrent objectives, any order, each reward helping the next (Cerny). |
| 4 | constantly teaches the player something new | Every level introduces a mechanic "or put[s] a spin on an old one". Zelda dungeon = item tutorial, boss = test. See §5. |
| 5 | is surprising | The roller-coaster curve goes stale; plan at least one "rapid surge in uncertainty" per level (Mandryka, quoted by Taylor). Manage the risk: greybox the surprise early. |
| 6 | empowers the player | Actions "must have a noticeable effect on the game world". Never ask players to do what they can easily do in real life. |
| 7 | allows the player to control the difficulty | Main path paced for moderate ability; skilled players get optional challenge "clearly called out using the level's language" (risk and reward both visible). Taylor criticises up-front Easy/Medium/Hard settings. Examples: Burnout Paradise's yellow-barrier shortcuts; a Skyrim chest reachable only by advanced technique. |
| 8 | is efficient | Design modular, mechanic-driven encounters that string together (Medal of Honor's 30 s–5 min "Battle Moments"); reuse spaces bi-directionally "with a key modifier on the second pass" (Halo 3's The Ark, return by tank). |
| 9 | creates emotion | Start from the target emotion and work back to mechanics, spatial metrics and narrative devices. Height carries emotion: a window below knee height gives power and voyeurism, above shoulder height persecution. |
| 10 | is driven by your game's mechanics | The level is "a gameplay delivery system". A space that exercises no verb needs another job (rest, reveal, story) or is cut. Prove the verb–space interaction in grey first (`process.md`, `fun-checks.md` §6). |

## 2. Guidance cues

**The ≥2 cues rule.** Every critical-path decision needs at least two independent cues on different channels. When a tester misses a cue, add a second channel (light + sound, landmark + motion) before making the first louder.

- **Landmarks / weenies.** Large, distinctive, visible from far away. "Weenie" is the Disney term for a visual magnet; Totten uses "architectural weenies" to orient players. Place landmarks where they are visible *from decision points*. Give global landmarks unique silhouettes and never repeat one in the same level [convention].
- **Terrain that pulls and hides (BotW, Fujibayashi & Yonezu, CEDEC 2017).** Triangles work at three sizes: large ones are landmarks, medium ones block the view (go over or around, and the designer can surprise behind them), small ones set the tempo. Rectangles hide completely. **"Gravity":** evenly spaced towers felt "too linear", so the team placed structures of varying visibility to pull players in different directions; heat maps showed better-spread paths. See `genre-open-world.md`.
- **Leading lines.** Edges, pipes, cables, roof lines and light strips that converge on the goal. A line works when it is near the eye line and ends at something worth reaching; it focuses attention, it does not guarantee behaviour.
- **Eye level.** Put required cues within normal camera pitch. Valve's Portal 2 team: "Players very rarely look up, and they almost never look at the things that are obvious to us as designers" (Game Informer, 2010). Valve fixed a Portal 2 room testers could not solve by moving a single hole through the glass "down to the eye level of the player" (Portal 2 commentary, "Fizzler Intro"). Above-eye and below-ledge space suits optional content unless a chain of cues leads the eye there (`verticality.md` §2, §7).
- **Lighting.** Bright attracts, dark warns. See §3 for order and rules.
- **Breadcrumbs.** Pickups, footprints, blood trails, floor-material changes. They say "keep going"; they should not be the only sign of where a route starts.
- **Motion.** A fleeing NPC, birds lifting off, cloth, a creature crossing a far doorway. Use it at the moment of choice [convention].
- **Sound.** Spatialised audio at goals works without line of sight and is the redundant channel for low-vision players.
- **Colour / material language.** Consistent coding across the whole game (see §4). Never signal "by a fixed colour alone" (Game Accessibility Guidelines): pair with value contrast and shape.
- **Enemies and NPCs** face, guard or come from the way forward; a guarded door reads as important [convention].
- **Framing.** Doorways and arches frame the next goal (`layout-and-flow.md` §8).

## 3. Lighting order

The Level Design Book (TLDB, "Lighting") gives an order; do it early, **before the art pass**:
1. **Global** light (sun, sky, ambient) for overall value and time of day.
2. **Wayfinding / critical path** lights: exits, doorways, objectives. "Brightly lit doorways help players understand the flow of the room" (Jenssen, via TLDB).
3. **Gameplay** lights: enemies, hazards, cover, pickups, interactables.
4. **Detail and mood** last, never overriding 1–3.

Rules [convention]: at each choice the exit should hold the strongest value contrast in the frame; check in greyscale; re-check after the art pass because props and mood lights break wayfinding first.

## 4. Affordances and readability

**Emilia Schatz (Naughty Dog), "Defining Environment Language for Video Games" (80.lv, 2017)** names four affordance types:
- **Explicit:** a break from realism (glowing ammo, a button prompt, Uncharted 4's rope-throw icon).
- **Defined:** arbitrary visuals consistently tied to a mechanic ("all climbable handholds painted yellow").
- **Cultural:** known from life or other games (ladder, padlock, valve on a pipe).
- **Inferred:** deduced from the game's own rules and systems.
- "Explicit and Defined messaging break immersion and so should be considered a fallback plan." Prefer cultural and inferred; fall back when tests fail (UC4's rope-wrapped grapple points still failed in combat, so they got a HUD icon).

Procedure:
1. **Catalogue every mechanic that touches the environment** (move, clamber, jump, cover, climb…). For each, define what affords it and what clearly does not: "There cannot be any middle ground."
2. **Buffer the metrics** with dead zones around capability thresholds (ledges, slopes, cover heights; numbers in `metrics.md`).
3. **Buffer placement with a "border zone":** keep confusing look-alikes away from true affordances. Naughty Dog removed "tiny cracks and ripples" and strong horizontal lines from rock near climbable routes.
4. **Shape language:** rectangles read as affordance, round shapes as lacking it, diagonal and pointy shapes negate it. Preserve silhouettes. Deny unwanted affordances with rounder shapes, lower contrast, broken silhouettes.
5. **Self-test:** "play it 'wrong', try to go where you're not supposed to."

**Yellow paint debate (2023, Resident Evil 4 remake).** Players mocked painted ledges; developers defended them because "people skip over environmentally realistic props". Players then modded the paint out of RE4R and FF7 Rebirth because neither offered a toggle. Lessons: readability beats realism when tests show players missing props; one language game-wide (an unpainted climbable ledge erodes trust in all of them); make it diegetic where possible (wear, rope, scratches, lit edges) [convention]; offer a guidance-intensity option where the genre allows; re-test after art.

**Make the impossible clearly impossible.** Unreachable areas look unreachable (out of range, sheer, no affordance language). "Barely possible" belongs only in deliberate optional challenge [convention].

## 5. Teaching mechanics

- **Kishōtenketsu (Koichi Hayashida, "The Structure of Fun", Game Developer interview on *Super Mario 3D Land*, 2012).** Introduce a concept → develop it → a "change-up", the "ten [twist]" that "throws them for a loop" → conclusion. On 3D Land he enforced "a clear concept in the beginning, and that's carried through absolutely all the way": one concept per level, exhausted before adding another. "Mastery test / victory lap" and the 3D World "Cakewalk Flip" example are analysts' framing, not his.
- **Valve (Portal, Portal 2).** Every chamber "starts with a specific goal in mind". Isolate each fact the player must hold and test it alone (Portal's chamber that exists only to show both portals are entrance and exit). Later chambers combine rules or turn one on its head. **Alternate solutions:** keep one if it "makes the tester feel smart"; remove or reconfigure it if it makes the game feel "broken" (Game Informer, 2010). Skips that take more skill can stand.
- **Alyx's room test (Robin Walker, Road to VR):** ask of every room "what happens in this room that hasn't happened in any of the previous rooms and fits into where we're going with the next room?"
- **World 1-1 (Super Mario Bros.).** The first Goomba walks at you and forces the discovery of jump. The first threat teaches exactly one response and is survivable to experiment with; the start screen makes the right action the natural one.
- **Fun as learning.** Koster: "Fun is just another word for learning" (*A Theory of Fun*); Crawford's earlier wording: "fun is the emotional response to learning". When a level stops teaching or recombining, expect boredom.
- **Don't punish while teaching** (Hodent, GDC 2016); at most ~3 new items at once in learning mode.
- **Recipe:** safe intro (no or cheap fail state) → one added variable → twist (invert, combine, change context) → test → reuse in a mixed context, then a rest beat. Parallel model: Dormans's kihon → kata → kumite. Puzzle and platformer specifics: `puzzle-sequencing.md`, `platformer-craft.md`.

## 6. Pacing

- **Interest curve (Schell, *The Art of Game Design*):** hook, rising peaks separated by valleys, climax, short resolution. Plot it per level; a flat stretch or a peak with no valley before it is a problem.
- **Rest after every peak** (safe room, vista, vignette); each peak higher than the last up to the climax.
- **Compress and release** [convention]: narrow, low or dark before wide, bright or high. Use it before every major fight or reveal.
- **Chokepoints** put players in the designed space at the planned moment; pair a clear main route with side pockets for explorers.
- **Left 4 Dead's AI Director** cycles build-up → sustained peak → relax, measuring player stress rather than spawn count and guaranteeing a relax period. Hand-authored lesson: measure intensity by stress and always schedule the relax.
- **Encounter rhythm (id, DOOM 2016, "combat chess", Stratton via Game Developer 2017):** ranged demons hold position, few melee chasers at once, line-of-sight breaks without camping spots, arena size tuned to make the player feel fast; "make me think, make me move". Detail: `genre-action-combat.md`.
- **Naughty Dog:** Uncharted 1's spaces were built before its combat was understood and pacing suffered; Uncharted 2's "Macro" spreadsheet mapped every level to beats, mechanics and enemies. Design the encounter and beat first, then the space.
- Beat-chart format and machine checks: `process.md` §4 and `fun-checks.md` §5.

## 7. Spatial psychology

- **Lynch, *The Image of the City* (1960): paths, edges, districts, nodes, landmarks.** Use as a wayfinding checklist: is the main path continuous; does each edge read as barrier or seam; can districts be told apart by material, colour or light; do nodes get a landmark or light; is a global landmark visible from most of the space? A design checklist, not proven cognition (a 3-player Sable study found only 2 of 5 in player maps).
- **Prospect–refuge [contested].** Appleton (1975), adapted by Totten: prospect = open, exposed space; refuge = enclosed space with views out but not in. TLDB argues it has "limited application", citing a 2016 meta-analysis that supports prospect but not refuge ("maybe don't"). Use TLDB's actionable forms instead:
  - **Sightline / vista:** preview the space, landmarks and arena layout before an encounter.
  - **Cover / enclosure / safe house:** places that protect and let the player plan.
- **Totten's spatial size types** (*An Architectural Approach to Level Design*; emotional mapping [convention]): narrow (tension, forced motion), intimate (safety), prospect (exposure, awe). Alternating them is pacing; tag every beat-chart space.
- **Jenkins's narrative spaces:** evocative (draws on genre), enacted (story performed in space), embedded (props carry it), emergent (systems). Embedded and enacted are the designer's direct levers.
- **Alexander / Barney patterns:** name recurring solutions as context–problem–solution patterns so they can be reused and critiqued. Intimacy gradient: public hub → semi-private spoke → private reward room [convention].

## 8. Environmental storytelling

- **Definition (Harvey Smith & Matthias Worch, "What Happened Here?", GDC 2010):** "staging player-space with environmental properties that can be interpreted as a meaningful whole, furthering the narrative of the game." The player *pulls* the story.
- **Association and closure:** two or three associated props make a story; show before and after, leave out the middle (Smith & Worch's shoe example).
- **Telegraphing:** environmental story can guide and warn (Doom 3's blood trail into a bathroom telegraphs a monster).
- **Persistence:** "It's memorable to come back and see your own mess." Corpses stay, doors stay broken.
- **Missability:** "It has to be possible to miss some things to make finding them meaningful" (Smith, 2011). Critical information must not be missable; lore may be.
- **Critique:** can a player reconstruct "what happened here" from 3+ props without text? Is the vignette lit and framed? Does it serve the level's emotion? Does it contradict known fiction? Does it reward a second look [convention]?

## 9. The level designer's role

- **The Door Problem (Liz England, 2014).** The level designer's line: "I put the door in my level and locked it. After an event, I unlocked it." For every door ask who owns its lock state, how it is signalled, what happens on the far side, and whether AI and co-op can use it ("Enemies and allies now know if a door is there…" is the AI programmer's line).
- **Holistic level design (Steve Lee, Arkane, GDC 2017):** design gameplay, presentation and story together. Consistency (a vent that looks crawlable is crawlable) and self-evidence (a guard post sits where a guard would stand) [convention for these applied rules].
- **30 seconds of fun (Jaime Griesemer, Engadget interview, 2011).** The Halo 2 documentary line: "In Halo 1, there was maybe 30 seconds of fun that happened over and over and over and over again." The cut second half: play it "in different environments, with different weapons, different vehicles, against different enemies… No 30 second stretch of Halo is ever repeated." Structure: "a 3-second loop inside of a 30-second loop inside of a 3-minute loop that is always different." Check all three: the 3 s verb feels good, each 30 s encounter changes a variable (range, height, enemy mix, weapon), each 3 min stretch changes context.

## Review checklist

- [ ] All ten Taylor principles checked; at least one deliberate surprise, greyboxed early
- [ ] Main path paced for moderate ability; optional harder routes show risk and reward in the level's language
- [ ] Goal unambiguous; method left open where the genre allows; no single forced technique
- [ ] Every critical-path decision has ≥2 independent cues on different channels
- [ ] Landmarks visible from decision points; unique silhouettes; BotW-style triangles/rectangles used to pull and hide
- [ ] Required cues sit within normal camera pitch, or a chain of cues leads the eye up or down
- [ ] Lighting pass in TLDB order (global → wayfinding → gameplay → mood) before art; exit has the strongest value contrast
- [ ] Affordance catalogue: every environmental mechanic has afford/deny rules, dead zones and border zones; explicit/defined cues only as fallback
- [ ] One affordance language game-wide; nothing signalled by a fixed colour alone; unreachable looks unreachable
- [ ] Each mechanic: introduce → develop → twist → conclude, one clear concept per level, reused later in a mixed context
- [ ] Alternate solutions reviewed: kept if they feel smart, removed if they feel broken
- [ ] Every room passes the Alyx test (something new happens here)
- [ ] Interest curve plotted: hook, rising peaks, rest after each peak, compression before reveals
- [ ] Encounters and beats designed before the spaces that hold them
- [ ] Lynch's five elements legible; vistas and cover used instead of assuming prospect–refuge
- [ ] Environmental vignettes readable without text, lit, framed; critical info not missable; player's mess persists
- [ ] Every door: lock state owned, signalled, works for AI, co-op and the far side
- [ ] Core loop checked at 3 s / 30 s / 3 min; each encounter changes at least one variable
