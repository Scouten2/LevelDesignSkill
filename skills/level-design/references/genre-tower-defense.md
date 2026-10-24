# Tower Defense

## Contents
1. Decide fixed path or mazing first
2. Path design: length is the budget, bends are the decisions
3. Build spots and placement
4. Wave design that defeats mono-builds
5. The first wave shows off a tool
6. Economy, spots and waves are one system
7. Progression across maps and replay modes
8. Mazing maps (Defense Grid, Desktop Tower Defense)
9. Greybox, coverage tables and the bundled scripts
10. Common failures → fixes
- Review checklist
- Levels to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

A tower defense level is three coupled parts: the path enemies walk, where the player may build, and the waves. Change one and the other two must be re-tuned. Teaching rhythm is in `principles.md`; fun checks in `fun-checks.md`.

---

## 1. Decide fixed path or mazing first

Write this in the brief before drawing; it changes what "level design" means.

- **Fixed path** (Kingdom Rush, Bloons): the designer authors the route; the layout carries the challenge. You design bends, junctions, entries and build spots.
- **Mazing** (Defense Grid, Desktop Tower Defense): towers block movement, so the player builds the path. The map is a canvas: you design the frame (playable area, entrances, exits, unbuildable tiles, fixed obstacles), and the player designs the maze. Desktop Tower Defense was made because few games supported mazing (Wikipedia) [unverified].
- **Hybrid** [convention]: fixed path plus blockers that reroute (Kingdom Rush barracks hold enemies in place without changing the route). Say which rules apply where.
- **Lane variant** [unverified]: Plants vs. Zombies uses fixed parallel lanes; the "path" is the lane set, and each level introduces one plant or zombie, then tests it.

## 2. Path design: length is the budget, bends are the decisions

- **Damage ≈ DPS × time in range** (player guide, Steam) [convention]. A tower's value is how long enemies spend inside its radius, so geometry near build spots matters more than total path length.
- **Total path length sets the difficulty budget; bend density sets where the interesting choices are** [convention]. A U-bend or switchback inside one tower's range doubles that tower's exposure time. Place bends where you want a decision, not everywhere.
- **Junctions are strategic.** Kingdom Rush plots cluster around path intersections, where enemies from two routes pass (Pocket Gamer strategy guide) [convention].
- **Hard-map levers** [convention]: more entries or exits, shorter paths, flying units that ignore the path, line-of-sight and placement blockers. Bloons' wiki describes higher map tiers as having "shorter paths and/or multiple paths, line of sight and placement blockers, and removable objects" [unverified].
- **Read every route from spawn to exit.** Each spawn needs a visible route, a spawn marker and an exit marker; players must see where enemies will go before wave 1 [convention].
- **Return trips double path value** [unverified]. In Defense Grid aliens carry power cores back out, so path length counts twice.

## 3. Build spots and placement

- **Three models:** fixed plots (Kingdom Rush), free placement on allowed terrain (Bloons; water spots only for water towers) [unverified], and maze-building on a grid (Defense Grid). Pick one per game; mixing confuses the player's mental model.
- **Put plots at bends and junctions** [convention] so one tower covers several path segments, and leave a few on long straights as weaker but cheaper options.
- **Count the plots as a budget, not decoration** [convention]. Kingdom Rush levels carry a fixed set of plots [unverified: typical count]. Each plot should have a reason (covers junction A, covers exit B, supports barracks C).
- **No single dominant spot** [convention]. If one plot covers most of the path, every player builds there and the map has one answer. Cap the path cells any single spot covers (§9).
- **Blockers and removable objects** let a later map, or later in the same map, open new spots or cut sightlines [convention].
- **Verticality is minor here.** Height usually appears as line-of-sight blockers or a higher plot with more coverage [convention]; if you give height a range bonus, show it in the build preview.

## 4. Wave design that defeats mono-builds

- **Waves are the enemy encounters; design them as data.** Describe each level as a list of waves with enemy types, counts and timing, separate from spawning code [convention]. It makes per-wave re-tuning cheap.
- **Alternate demands.** Defense Grid waves alternate between groups suited to area damage and groups that need single-target damage [unverified]. Mix armoured with fast, swarm with tank, ground with flying, so no single tower type wins every wave.
- **Enemy properties as keys** [convention]. Bloons' camo, lead and MOAB-class properties require specific towers or upgrades; each property gates tower variety the way a key gates a door.
- **Introduce one new enemy type per level or wave block**, then combine it with known ones (teach → develop → twist → conclude). Kingdom Rush's early campaign is mostly goblins, then brings in more threatening enemies to stay interesting (community analysis).
- **Preview upcoming waves.** Defense Grid 2 shows upcoming waves as icons so players plan instead of react [unverified]. Planning is where TD autonomy lives (`fun-checks.md`).
- **Boss waves summarise** [convention]: a boss that tests the level's key tool and path feature, not just a large health bar.
- **Let the player set tempo.** In Kingdom Rush, calling a wave early gives "free Gold equal to the number of seconds left before the wave would have come in naturally" (community analysis, Game Developer blog). A risk/reward pacing lever the player owns.

## 5. The first wave shows off a tool

- Kingdom Rush: "the first wave sends out 3 Goblins, who will be stopped completely by the 3 soldiers; Ironhide Studios wants you to see the appeal of the Barracks" (community analysis, Game Developer blog). The first threat is sized exactly to the first tool, so the player sees the tool work perfectly before it is tested.
- **Rule:** for every new tower or ability, script one wave that it handles cleanly on its own, then a wave that needs it plus something else [convention].
- **Teaching waves are cheap to fail** [convention]: low leak cost, so experimenting with placement is free.

## 6. Economy, spots and waves are one system

- Ironhide on *Kingdom Rush 6: Genesis* Patch 1 (2026): "tower spots are fixed, so if we add more without adding gold, the same gold gets spread across more towers… And if we add gold without reviewing the waves, the game simply gets easier." The patch adjusted "tower spots and waves" on specific stages, and "balancing four difficulty levels is hard and takes time."
- **Tune per stage, together.** Any change to gold, spot count or wave composition triggers a re-check of the other two on that stage.
- **Starting gold vs first-wave threat** [convention]: starting gold should buy the tool the first wave is built to show off (§5), with little slack.
- **Interest and early-call income** [convention] reward greed; test the greediest viable line, since it sets the effective difficulty for strong players.

## 7. Progression across maps and replay modes

- **Map tiers** [unverified]. BTD6 groups maps as Beginner, Intermediate, Advanced and Expert, though the wiki notes tier doesn't always match real difficulty (Geared, an Advanced map, is rated harder than several Expert maps). Tag your own maps by measured outcomes, not intent.
- **Separate map difficulty from mode difficulty** [convention]. Bloons sets round count by mode separately from map tier [unverified: exact counts]; Kingdom Rush replays a level in challenge modes with restricted towers or lives [unverified]. One layout, several tests.
- **Stars by lives remaining** [convention] make completion lenient and mastery optional, which fits the "hard content opt-in" stance.
- **Avoid steep difficulty swings.** A reviewer felt Kingdom Rush Origins was less fun because the difficulty swing was "so quick and so high" (Ironhide forum) [unverified]. Chart difficulty per stage across the campaign, not just within a stage.

## 8. Mazing maps (Defense Grid, Desktop Tower Defense)

- **Frame, don't route** [convention]. Define the build area, entrances, exits and fixed obstacles; leave the maze to the player.
- **Guarantee a path always exists** [convention]. Either forbid placements that block every route (the usual rule) or define what enemies do when blocked. Communicate the rule on the first map.
- **Towers as walls change costs.** In Defense Grid 2 a cheap boost tower doubles as a wall [unverified]. Price wall-only pieces so mazing competes with damage.
- **Fixed obstacles shape the canvas** [convention]: pillars and unbuildable tiles create natural funnel points; place them so several maze designs are viable, not one.

## 9. Greybox, coverage tables and the bundled scripts

- **Gameplay first.** Prove the level with placeholder towers and enemies at final speeds and ranges; art comes after the coverage numbers work.
- **Coverage table.** For each build spot, count path cells inside each tower's range and note which segments are covered twice. Hand-count on the grid or with a short throwaway script; say which. Flag spots whose coverage is far above the others (§3).
- **Route graph.** Model spawns, junctions and exits as nodes and run `python3 -I scripts/graph_check.py path.json` once per spawn (start = spawn, goal = exit) to confirm every spawn reaches an exit and to count junction loops. For mazing maps, draw the buildable grid with the puzzle legend (`#` unbuildable or obstacle, `-` buildable floor) and run `scripts/level_metrics.py map.txt --legend puzzle`; regions > 1 means a sealed pocket. Neither script models tower range, DPS or waves.
- **Never claim a wave set is beatable** without a playtest or a labelled hand trace of the intended build; tag tuning numbers as provisional.

## 10. Common failures → fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Everyone builds the same spot and tower | One dominant spot; waves don't punish mono-builds | Cap coverage per spot; alternate wave demands |
| Level suddenly too easy after a patch | Gold changed without re-tuning waves | Re-tune waves, spots and gold together, per stage |
| Players leak on wave 1 and quit | First wave not matched to the first tool | Size wave 1 to show off the starting tower |
| Players can't predict enemy routes | No spawn/exit markers; ambiguous junctions | Draw routes, mark spawns and exits, preview waves |
| Mazing map has one solution | Obstacles allow a single funnel | Move obstacles so several mazes work |
| Difficulty spike between stages | Campaign curve not charted | Chart per-stage difficulty; smooth or signpost spikes |

## Review checklist

- [ ] Fixed path, mazing or hybrid chosen and written in the brief
- [ ] Every spawn has a visible route to an exit; checked with `graph_check.py` per spawn
- [ ] Bends and junctions placed where decisions should be; total path length matches the difficulty budget
- [ ] Coverage table done; no spot dominates; each plot has a written reason
- [ ] Waves written as data; demands alternate; no single tower type clears every wave
- [ ] One new enemy type per level or wave block; upcoming waves previewed
- [ ] First wave sized to show off the starting tool; teaching waves cheap to fail
- [ ] Gold, spots and waves re-tuned together after any change, per stage
- [ ] Map difficulty and mode difficulty kept separate; stars or modes make mastery optional
- [ ] Mazing: a path always exists or the blocked rule is taught; several maze designs viable
- [ ] Beatability claims backed by a playtest or a labelled hand trace

## Levels to study

- **Kingdom Rush:** the first campaign stage (3 goblins vs 3 soldiers), and stages adjusted in *Kingdom Rush 6: Genesis* Patch 1 for spot and wave re-tuning.
- **Bloons TD 6:** a Beginner map vs an Expert map side by side for path count, length and blockers; Geared as a tier-mismatch case [unverified].
- **Defense Grid / Defense Grid 2:** an open mazing map and a fixed-platform map [unverified].
- **Desktop Tower Defense:** the open canvas as the purest mazing case.
- **Plants vs. Zombies:** early levels for one-new-thing-per-level lane design [unverified].
