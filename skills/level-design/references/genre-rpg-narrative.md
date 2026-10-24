# RPGs, Narrative & Exploration Games, Survival Worlds

## Contents
1. Universal rules
2. Hubs and towns
3. CRPG reactive levels (multiple solutions, verticality)
4. Steering in open RPGs without walls
5. Dense small worlds and dungeon crawlers
6. Narrative / exploration games (Journey, Outer Wilds, walking sims)
7. Survival and sandbox (pointer)
8. Review checklist
9. Levels to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact. "Critics" or "players" = reviewer or community observations, not developer intent. Primary CRPG developer sources were thin, so expect more tags here than in other guides.

Core refs: environmental storytelling and Lynch in `principles.md`; hubs, gating and loops in `layout-and-flow.md`; height and the hidden-but-fair rule in `verticality.md`; dungeon interiors and souls-like vertical loops in `genre-dungeon-metroidvania.md`; outdoor macro structure, layered worlds and survival-crafting in `genre-open-world.md`; tactical grids in `genre-tactics.md`; playtest protocol in `playtesting-and-critique.md`.

---

## 1. Universal rules

- **The level is the story structure.** In narrative-led games, decide what the player should feel and learn in each space before deciding its shape. Plot points become spatial gates, reveals and vistas.
- **Measure density in interactions, not area.** [convention] An RPG space is "full" when it offers choices, conversations, readable objects and reactions, not when it is big. A small map with deep interactions beats a large one with shallow ones.
- **Every solution needs a space.** If the design allows talking, sneaking, fighting and using the environment, the level must contain a physical approach for each: a door to talk through, a vent or ledge to sneak by, ground to fight on, a hazard to exploit.
- **Lock off rarely, and say so.** Larian's BG3 rarely locks areas except at story-critical points of no return. Flag points of no return clearly and before the player commits.
- **Blockers must read as blockers.** New Vegas's lead designer Josh Sawyer reportedly wanted "as few invisible walls as possible" (secondhand quote), yet players still complain about mountains that look climbable but are blocked (near Nipton and Black Mountain). Make every barrier look like what it is.

## 2. Hubs and towns

[convention] throughout; primary hub-design sources were not found. Reference cases: Mass Effect's Citadel, Disco Elysium's Martinaise.

- **Short walks between quest givers.** Pack NPCs, vendors and quest givers within a short walk of each other and of the hub's entrance. Long walks through an already-explored town are dead time.
- **One central landmark** visible from most of the hub (a tower, a statue, a market square) for orientation. Give each district of the town its own look, function and population (Lynch districts, `principles.md`).
- **Reuse the hub as the world changes.** A hub returned to across the game should show consequences: new NPCs, damage, changed factions, opened or closed doors. The changed state of a familiar place is cheap, strong storytelling.
- **Layer by commitment.** Main-street services up front; side quests in side streets; secrets and optional content on roofs, cellars and back alleys.
- **Hub exits read as exits.** Give every route out of town a distinct gate, sign or landmark tied to the region it leads to.

## 3. CRPG reactive levels (multiple solutions, verticality)

- **Design solutions per space, then build each.** Baldur's Gate 3 examples:
  - Fights can be skipped through persuasion.
  - The foundry can be bombed, or taken by siding with the Gondians.
  - Moonrise Towers can be stormed with an allied army, or cleared quietly by removing enemies before reinforcements arrive.
- **Multiple solutions need multiple entry points.** List the approaches in the level brief and check that every one has a physical route and a way to find it.
- **A layered build for a reactive space.** [convention]
  1. One main approach (the obvious door).
  2. At least one stealth or vertical route (roof, ladder, cave, window).
  3. A dialogue bypass (a guard to persuade, a password to learn elsewhere).
  4. Environmental hazards (oil, water, explosive barrels) placed near likely combat positions.
- **Verticality is the tactical layer.** Critics call verticality "the big word" for BG3 combat: shoving, ledges, high ground. Put high ground at every planned combat space, give both sides a way up, and place drops where a shove matters.
- **Check detection across height.** A known BG3 issue: line of sight ignores height, so enemies spot the player across vertical distance more readily than across horizontal distance. Test stealth routes over and under enemies, not only past them.
- **Height beyond combat.** Use it for preview (survey a camp from a cliff before choosing an approach), hidden routes (a cave or ladder found by looking over an edge) and footprint reuse (a tower or cellar under the same building). Hidden alternative routes must pass the hidden-but-fair rule (`verticality.md`); a solution nobody finds is not a solution. Draw a section for multi-floor spaces and state the fall-damage policy, since a ledge "barely over your character's head" that hurts reads as unfair [unverified: player forum report on BG3].
- **Reactivity hint:** [convention] put the clue to an alternative solution where curious players look (a note in a side room, an overheard conversation, a suspicious wall), so finding it feels earned.

## 4. Steering in open RPGs without walls

- **Lethal fauna as a soft gate.** [convention] Fallout: New Vegas steers new players south and then clockwise along I-15, using deathclaws at Quarry Junction and cazadores on the northern route from Goodsprings. The direct route is physically open but practically lethal. This is widely discussed, including by Sawyer, but no source was retrieved.
- **Rules for soft gates.** [convention]
  - The danger must be visible and readable before it kills (a carcass, a warning sign, a distant roar).
  - The intended route must be visibly easier.
  - Breaking through should be possible for skilled or prepared players, and should pay off.
- **Enemy level as gating** works only if the player can read it. Pair it with an environmental warning.

## 5. Dense small worlds and dungeon crawlers

- **Disco Elysium's model.** [convention] A small map made deep: nearly every object and NPC is a dialogue node tied to skill checks. Size the map for walking distance and reuse; spend the budget on interactions per square metre.
- **Grid crawlers.** [convention] Legend of Grimrock is built on a tile grid with puzzles from pressure plates, secret buttons and teleporters. The grid lets players map by hand, which is part of the appeal. Keep to the grid strictly if mapping is part of the fun.
- **Tile-and-vault dungeons.** [convention] Diablo assembles dungeons from tiles and set pieces, with hand-made "vaults" or quest rooms placed into procedural layouts. See `genre-roguelike-procedural.md`.

## 6. Narrative / exploration games

### Journey (Jenova Chen, GDC 2013 "Designing Journey"; GDC 2012 coverage)
- **Map the emotional arc of the whole game first**, then split it into per-segment gameplay and story beats. Each segment carries one dominant emotion with a terrain metaphor: desert, sliding sands, dark underground, snow ascent, flight.
- **Teach the payoff's rule early.** Before the final walk, the game takes time to teach that freezing means death, so the last field *feels* deadly. An emotional peak needs earlier level-based teaching to land.
- **Terrain as a progress bar.** Dunes and sand trails were added partly because large 3D spaces made progress hard to gauge.
- **Space serves the target feeling.** The goal was to make the player feel small and full of wonder, so that meeting another player becomes connection, not combat. Prototyping started from the music.

### Outer Wilds (knowledge-gated exploration)
- **Knowledge gates instead of item gates.** Progress comes from information recorded in the ship's log, not from gear. There are no objectives or indicators. An orange asterisk marks log entries with unexplored information.
- **Persistent log.** The log persists across time loops. Because nearly everything is reachable on loop one, players reach "later" content without its context, and the design has to handle that.
- **Rules for knowledge gating:**
  - Make each location *physically* reachable early but *understandable* only with clues found elsewhere.
  - Write every clue so it still reads without context.
  - Cross-reference clues so that any order of discovery converges on the answer.
  - Give the player a record (a log, a map, a journal) so learning isn't held only in memory.
- **Failure mode:** some players feel lost with no direction. Use the log's "unexplored" markers, or an equivalent, as a pull that doesn't dictate a route.

### Walking sims and houses as levels
- **Grey can't answer everything here.** Firewatch's greybox "did not answer any of the important questions" because pacing was a narrative and environment-art problem (Jane Ng, GDC 2016, via TLDB). When the core experience is mood, story or place, say so and test the cheapest representative slice with real art and audio (`process.md`). Routes, gates and sightlines still get proved in grey.
- **Firewatch** (Nels Anderson and Jake Rodkin, GDC) covered world structure, goals and gating, and "encounter" design; the hand-built world is about the size of a major theme park. [convention] Lookout towers on the ridgelines act as orientation landmarks, and the paper map and compass are diegetic items held in Henry's hands.
- **Gone Home and What Remains of Edith Finch.** [convention] A single house is the level. Locked doors and secret passages pace the narrative reveals; Edith Finch's house rises in added bedrooms as a visible vertical goal.
- **Density rule.** Every room needs at least one readable story object. Gate spaces by narrative order, not by challenge.
- **Environmental storytelling techniques** (staging, traces, contrast) are in `principles.md`.

## 7. Survival and sandbox (pointer)

Survival-crafting worlds moved to `genre-open-world.md` §8 (Robert Yang on Subnautica: "Caves become mini-bosses; deep trenches become mega-bosses"; key wrecks mid-biome; world edges that read differently from explorable danger; goal beacons through the late game; biome ladders). Descent as dread is in `genre-horror.md` §3.
- [convention] The Long Dark uses hand-authored regions with fixed landmarks (Camp Office in Mystery Lake) joined by transition zones, with weather as the hazard that hides them. Minecraft joins structure templates at connector points over noise terrain.

## Review checklist

- [ ] Brief lists the target emotion per space and the narrative beat each space delivers
- [ ] Routes, gates and solutions proved in grey; mood-led spaces flagged and tested as a cheap lit slice
- [ ] Every intended solution (talk / sneak / fight / environment) has a physical route and a findable clue
- [ ] Each combat space has high ground reachable by both sides; shove/drop opportunities placed
- [ ] Stealth routes tested over/under enemies (vertical detection), not just past them
- [ ] Hidden alternative routes pass hidden-but-fair; fall-damage policy stated and legible
- [ ] Hub: quest givers within a short walk; central landmark; districts distinct; changes over the game
- [ ] Points of no return flagged before commitment; nothing else locked off without reason
- [ ] Soft gates (fauna, level, hazards) readable before they kill; intended route visibly easier
- [ ] No invisible walls on terrain that looks traversable
- [ ] Knowledge gates: clues readable without context; any discovery order converges; persistent log
- [ ] Payoffs taught earlier (the "freezing means death" test)
- [ ] Every walking-sim room has at least one readable story object

## Levels to study

- **Reactive CRPG spaces:** Baldur's Gate 3 (the goblin camp, the foundry, Moonrise Towers); Divinity: Original Sin 2.
- **Hubs:** Mass Effect's Citadel; Disco Elysium's Martinaise; Fallout: New Vegas's Freeside and the Strip.
- **Soft steering:** Fallout: New Vegas (Goodsprings → Primm → I-15).
- **Narrative exploration:** Journey; Outer Wilds; Firewatch; Gone Home; What Remains of Edith Finch.
- **Survival:** Subnautica (Safe Shallows → Grassy Plateaus → Lost River); The Long Dark (Mystery Lake).
- **Grid crawlers:** Legend of Grimrock.

Key sources (full list in `SOURCES.md`): D&D Beyond, "9 DM Lessons from Baldur's Gate 3"; GameRant and ScreenRant on BG3; Steam forums on New Vegas; GDC Vault, "Designing Journey" (Chen, 2013); TLDB (Blockout, on Firewatch and Untitled Goose Game); Campo Santo blog on Firewatch; Edge, Scientific Gamer on Outer Wilds; Radiator Blog (Robert Yang) on Subnautica.
