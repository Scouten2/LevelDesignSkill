# Strategy Maps: RTS, Territory Control and Builders

## Contents
1. The map is an economy
2. Distances: rush distance in worker-seconds
3. Playable area and base count
4. The base ladder: each base harder to hold
5. Value tracks exposure
6. Symmetry, asymmetry and balanced pools
7. Terrain tools: chokes, rocks, watchtowers, high ground (verticality)
8. Territory and cut-offs (Company of Heroes)
9. Random map scripts and live tuning
10. Builders and colony sims: the start map as an economic level
11. Greybox, measurement and the bundled scripts
12. Common failures → fixes
- Review checklist
- Maps to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

A competitive RTS map is an economic layout first: where bases and resources sit, how far armies travel, and how defensible each expansion is decide which strategies are viable. Shooter-style competitive rules (timings, lanes, power positions) are in `genre-multiplayer.md`; grid tactics in `genre-tactics.md`.

---

## 1. The map is an economy

- **Design the resource layout before the terrain art.** Small changes to where resources sit flip which strategies win (AoE2's front gold, §5; CoH munitions points, §8). Playtest the resource layout on flat greybox before decorating.
- **Every base trades value against exposure.** A safe base with high income ends games in stalemate; an exposed base with low income is never taken. Put both numbers in the map doc for each base.
- **Write the intended strategy profile** in one line: rush map, standard, or macro (long games, many bases). Distances and area follow from it (§2–3).
- **Gameplay first:** an RTS greybox is untextured terrain, start locations and resource nodes. Run worker timings and a few build orders on it before any art.

## 2. Distances: rush distance in worker-seconds

- **Measure in time, not tiles.** Liquipedia gives SC2 rush distance as the time a worker needs to walk from the main base start location to the centre of the opponent's natural: Winter's Gate LE, "41 seconds" on a 128×132 map.
- **Bands are guidelines.** TeamLiquid Map Contest #11 asked for an average rush distance of **35–45 s for standard maps** and **40–55 s for macro maps**, noting "The average rush distance and playable map dimensions are guidelines and not strict restrictions" (TL MC11).
- **Measure it the cheap way:** in a custom game, send one worker between start locations and time it; repeat both directions [convention].
- **Report every spawn pair.** On maps with more than two spawns, distances differ by pair (Liquipedia lists Revolver at 42 s cross, 30.5 s vertical, 35 s horizontal) [unverified]. The shortest pair sets the rush risk; state it.
- **Air distance vs ground distance** [convention]. A map can have a long ground path and a short air path (or a cliff drop path); measure both, since harassment uses the short one.
- For non-SC2 games, keep the method and swap the unit: seconds for the game's standard worker or scout. The bands above are SC2-specific.

## 3. Playable area and base count

- **TL MC11 playable area:** standard "approximately between 16,000 and 22,000" cells (example: Catalyst, 136×144 = 19,584); macro "approximately 20,000 and up" (example: Odyssey, 152×156 = 23,712). Again guidelines.
- **Base count** [convention]. SC2 1v1 maps commonly carry around 12–16 bases [unverified]; Altitude LE has 16, including 2 rich bases (Liquipedia) [unverified]. Enough bases that both players can expand past their thirds without meeting; few enough that the centre is contested.
- **Standard base composition** in SC2 is often given as 8 mineral fields (4×1,800 + 4×900) plus two geysers [unverified]. Deviate deliberately and document it (e.g. a reduced main to speed games up).

## 4. The base ladder: each base harder to hold

- **Main → natural → third → fourth, each harder to defend than the last** [convention]. The SC2 pattern: main on high ground with one ramp (wallable), a natural below with a narrow choke, then several third options with falling defensibility [unverified as a rule; it is community practice].
- **Count attack paths per base** [convention]. One path to the main, one or two to the natural, more to the third. More paths favour mobile armies and harassment; fewer favour turtling.
- **Offer third-base choices**, e.g. a close but exposed third vs a far but tucked one [convention]. A choice of third is a strategic decision; a single obvious third is a script.
- **Chokes have a width budget** [convention]. A ramp narrow enough to wall is a defensive tool for early game; a centre choke too narrow for armies to fight through rewards whoever sieges first. Measure in unit widths for the largest common unit.

## 5. Value tracks exposure

- **Rich bases sit in exposed places by design.** Blizzard: rich mineral clusters "provide 7 minerals per trip, instead of 5" with the same total, and "tend to be placed in locations which are hard to defend and more exposed to attack" (Blizzard SC2 resource guide).
- **Resource placement inside a base matters too.** On AoE2's Arabia, "The limited amount of gold and stone in the area surrounding the Town Center can lend itself to becoming the target of a Feudal Age rush when generated in the front of a players base" (AoE wiki). The wiki lists per-player gold as one 7-tile and two 5-tile mines, stone 5 + 4 tiles [unverified: counts vary by version and game size; check in game].
- **Community variants prove the lever** [convention]. Map-script variants such as "Open Arabia" redistribute food, gold and stone to push aggressive Feudal play over walling; an official hill and mining-camp rebalance drew criticism for making walls and early towers harder.
- **Rule:** for every high-value node, write where the attack comes from and how long it takes defenders to arrive [convention].

## 6. Symmetry, asymmetry and balanced pools

- **Two-player ladder maps are usually rotationally (point) symmetric** [convention]; either way, check that the camera, UI and lighting don't favour one seat.
- **Symmetry is not automatic balance** [contested]. A TeamLiquid thread argues perfect symmetry doesn't make maps much more balanced and cites an asymmetric 4-player map that became a tournament staple because varied spawns kept games unpredictable.
- **Disguise mirrored halves** with themed art that works identically [convention] (one side a train, the other a truck, both hiding the same start).
- **Balance across a pool, not only a map** [convention]. A seasonal pool where one map leans rush, one macro and one positional lets each map tilt while the pool stays fair; vetoes let players dodge their worst matchup. Ladder pools run about seven maps [unverified].

## 7. Terrain tools: chokes, rocks, watchtowers, high ground (verticality)

- **Destructible rocks** close a path or protect a base until someone invests to break them [convention]: a timed gate on map topology.
- **Watchtowers are survey points** (the preview function in `verticality.md`). Blizzard's ladder notes describe a tower between the mains that "allows for scouting on both expansions and enemy attacks" [unverified: snippet]. Place them so holding one costs army position.
- **High ground is vision first.** In SC2, units on low ground can't see up a cliff without a vision source [convention]; in AoE2, units on hills get a damage bonus [unverified]. Every high-ground position needs a way up (ramp, air, cliff-jumping unit) and a way to gain vision of it, or it becomes an unanswerable siege spot.
- **Mains on high ground with one ramp** make the early game defensible and the ramp a landmark [convention].
- **Readable cliffs** [convention]. Tiers must read from the top-down camera through silhouette, shadow and edge trim, so players can judge pathing and vision at a glance. Recheck after the art pass: a cliff edge that blends into ground texture hides a proven affordance.
- **Slow and speed zones** (SC2's inhibitor and acceleration zones) tune attack-path timing without changing topology [unverified: exact values].

## 8. Territory and cut-offs (Company of Heroes)

- **Income needs a supply chain.** In CoH2, a territory point produces income only when an unbroken chain of controlled sectors connects it to base; cut-off points link the base to a region and are prime harassment targets (Prima CoH2 guide) [convention].
- **Put fuel and munitions points where the fight should be** [convention]. One community map's changelog moved munitions points toward the middle to stop "sector lockdown" and added bushes near the central victory point to break machine-gun lockdown.
- **Victory points drive tempo** [unverified: ticket counts]. Lay out VPs so holding the majority stretches the holder.
- **Cover, garrisons and destructible terrain** make a CoH map a tactical surface; apply the cover and flank rules of `genre-tactics.md` §3.

## 9. Random map scripts and live tuning

- **AoE2 maps are random map scripts** [convention]: balance comes from generation rules (fixed distances to the Town Center, mirrored "fair" resources), not one handcrafted layout. Test many seeds, not one.
- **Open–closed and land–water axes** classify AoE2 maps (Arabia open and rush-friendly; Arena and Black Forest closed and boom-friendly) [convention].
- **Tune from results** [convention]: track per-map win rates by faction and spawn, move one resource node or ramp at a time, and re-measure rush distances after each change.

## 10. Builders and colony sims: the start map as an economic level

Evidence here is thin (wikis and community guides), so the rules are **[convention]** throughout.

- **Frostpunk** places buildings on a circular grid around the generator, the main heat source; steam hubs create smaller heat zones at a coal cost. Frostpunk 2 rewards districts placed in sheltered areas such as crevasses. The layout is radial: distance from the centre is cost.
- **Anno 1800** exposes world settings: start world size, island size and difficulty, raw materials, fertilities (Ubisoft devblog). Community guides describe several start islands per world with basic fertilities, which AI rivals compete for.
- **RimWorld**'s landing-site panel shows biome, temperature, growing season, terrain and stone; beginners are steered to temperate forest with mountains (natural walls and roof). Site choice doubles as difficulty choice.
- **Rules:** guarantee every basic resource within early reach of the start; put scarce or advanced resources further out or behind terrain or technology gates; give terrain a strategic role (mountains = defence, crevasses = shelter, fertility = specialisation); grade danger and richness with distance from the start (Factorio-style) [unverified]; let site choice signal difficulty explicitly. For survival-crafting worlds see `genre-open-world.md`.

## 11. Greybox, measurement and the bundled scripts

- **Measure, don't estimate.** Rush distance, base-to-base reinforcement times and choke widths come from in-engine timing. Label any figure you estimated from a sketch "estimated from layout, not measured".
- **Attack-path graph.** Model mains, naturals, thirds, chokes and the centre as nodes and ground paths as edges (rocks as `requires: [break_rocks]`, cliff drops as one-way), then run `python3 -I scripts/graph_check.py map.json`. Cycle count shows how many independent attack routes exist; degree-1 nodes are pocket bases (fine if intended); one-way edges without return flag cliff-drop paths. The script does not model distance or time; pair it with the stopwatch numbers.
- **Seat test.** Play or simulate both seats (and every spawn pair) before calling a map balanced; one seat is not evidence.

## 12. Common failures → fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Every game is a rush | Short rush distance, gold/stone at the front | Lengthen the shortest spawn pair; move contested resources behind the base |
| Every game is a stalemate | Too few attack paths, safe high-value bases | Open a path to the third; move rich bases to exposed spots |
| One spawn pair dominates | Unequal distances on a multi-spawn map | Measure all pairs; equalise or remove the pair |
| Siege position nobody can break | High ground with no vision or approach | Add a ramp, a vision tower or a cliff path |
| Sector lockdown | Income points clustered behind one choke | Spread points; add cover to break the choke |
| Builders: dull or impossible starts | Basics missing or all resources adjacent | Guarantee basics nearby; gate advanced ones by distance or terrain |

## Review checklist

- [ ] Strategy profile (rush / standard / macro) written in one line
- [ ] Rush distance measured in worker-seconds for every spawn pair; air distance noted
- [ ] Playable area and base count recorded against the profile (bands are guidelines)
- [ ] Each base harder to hold than the last; attack paths counted per base; third-base choice exists
- [ ] Every high-value node has an exposure note: approach route and defender arrival time
- [ ] Symmetry type chosen; mirrored halves disguised; both seats tested
- [ ] Every high-ground position has a way up and a vision counter; cliffs readable after art
- [ ] Territory games: supply chains and cut-offs drawn; income points not locked behind one choke
- [ ] RMS games: many seeds tested, not one
- [ ] Builders: basics guaranteed near start; scarce resources gated; site choice signals difficulty
- [ ] Attack-path graph checked with `graph_check.py`; timings from in-engine measurement, labelled

## Maps to study

- **StarCraft II:** Winter's Gate LE (rush distance documented), Altitude LE (rich centre bases behind destructible towers) [unverified details], and TeamLiquid Map Contest entries with published guidelines.
- **Age of Empires II:** Arabia (open, rush-prone resource layout) vs Arena and Black Forest (closed, boom-friendly) [convention].
- **Company of Heroes 2:** maps with published changelogs showing point and cut-off iteration.
- **Builders:** Frostpunk's scenario craters (radial heat economy); a RimWorld landing in temperate forest vs ice sheet for site-as-difficulty [convention].
