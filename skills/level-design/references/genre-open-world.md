# Open Worlds, Layered Worlds & Survival-Crafting Regions

## Contents
1. Universal rules (macro structure)
2. Pull and concealment: BotW's gravity and triangles
3. Points of interest: density, variety, empty space
4. Regional anchors: legacy dungeons and landmark-led guidance
5. Layered worlds: sky, surface, depths (TotK, Shadow of the Erdtree)
6. Wayfinding without a HUD
7. Optional dungeons inside the world (Skyrim)
8. Survival-crafting worlds (Subnautica, Valheim)
9. Failure modes: templating and checklist fatigue
10. Review checklist
11. Worlds to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact. "Critics" = reviewer or player observations, not developer intent.

Core refs: landmarks and Lynch in `principles.md`; topology, reveals and sightlines in `layout-and-flow.md`; height functions, layered maps and the hidden-but-fair rule in `verticality.md`; scale in `metrics.md`; heatmaps in `playtesting-and-critique.md`; dungeon interiors in `genre-dungeon-metroidvania.md`.

---

## 1. Universal rules

- **Design the macro graph before the terrain.** Regions, their anchors (castle, city, tower) and the main traversal corridors as a bubble diagram first. Terrain is how you hide, reveal and connect those nodes.
- **Traversal speed sets world scale.** [convention] POI spacing, landmark height and empty stretches derive from how fast the player moves (walk, horse, glider, swing, vehicle). Design spacing for the speed most used in each region; check the others. Spider-Man's Manhattan uses tall buildings as swing anchors. [convention]
- **Give each region an identity** (a Lynch *district*): one dominant biome, palette, silhouette language, faction and anchor landmark. Edges separate districts; paths and nodes join them. A screenshot should name the region.
- **Gate softly; make hard blockers read as blockers.** Lethal fauna, cold, darkness and enemy level steer without walls (New Vegas, `genre-rpg-narrative.md`). Invisible walls on climbable-looking terrain are a recurring complaint.
- **Open with a vista.** [convention] An early high, safe vantage showing several anchors (BotW's Great Plateau) sets up the main pulls and teaches "what you can see, you can reach".
- **Validate distribution with heatmaps, not intuition** (§2).
- **Prove traversal in grey.** Climb, glide and ride across a blockout at real speed before dressing; the grey description test (`process.md`) applies to regions too.

## 2. Pull and concealment: BotW's gravity and triangles

Source: Fujibayashi and Yonezu, CEDEC 2017 (Matt Walker's translation; confirmed by Game Developer).
- **Gravity.** Tall, distinctive structures pull the player without HUD markers. Spreading towers with events between them felt "too linear" in playtests; "gravity" means "placing structures of varying visibility/importance in different places, leading players in different directions and allowing [them] to get sidetracked." Before/after heat maps showed better-distributed paths. (Coverage reported the early "points and lines" design as an "awkward 80/20 split" of crowded lines and unseen space.)
- **Triangles at three scales.** "The largest are landmarks… the medium sized triangles serve to obstruct the player's view… the smallest triangles serve the tempo — be it to change whatever buttons the player is pressing or for more concrete play." Triangles also give "a choice as to whether to go straight over the triangle, or around", and hide *part* of what is behind them, so the designer controls the reveal.
- **Rectangles hide completely.** "Rects are good for completely hiding something from sight." Rectangles for hard reveals; triangles for teasing partial views.
- **Chain of interest.** Hill → bridge structure → tower: each reveal hands over the next pull before the current one is used up. Walk the likely line and list what becomes visible at each crest.
- **Fix clustering with curiosities, not markers.** If heatmaps collapse onto straight lines between major POIs, add mid-distance curiosities (a ruin, a lone tree, smoke, an odd rock) so the path bends.
- **Laps.** Development ran in laps: prototype → full production without polish → polish. Whole-world passes stop a few polished areas hiding many unfinished ones (see §7).
- **Towers as a reward, not a chore.** A tower works when the climb is traversal play and the top is a real vista from which to pick the next goal (TotK's dive does the same job; §5).

## 3. Points of interest: density, variety, empty space

There are no sourced POI-per-km² or "reward every N seconds" figures; use a method.
- **Sightline test.** [convention] From any reachable vantage, at least one intriguing thing is visible: one far gravity landmark plus one nearer, partly hidden curiosity. Nothing on screen = density hole; ten competing things = noise.
- **Density follows speed.** [convention] Measure time between "new thing noticed" moments along likely routes at the dominant speed; set a target per region; tune in playtests.
- **Tier POIs by scale.** [convention] *Anchors* (one per region, visible across it), *destinations* (worth a detour of minutes), *curiosities* (seconds-long finds; Elden Ring's invisible scarab, BotW's Korok anomalies [convention]).
- **Vary the verb, not just the position.** For each POI type, what does it ask the player to *do*: climb, solve, fight, sneak, talk, look?
- **Keep deliberate empty space.** Critics of Witcher 3 argue the "empty wilderness" between POIs has value; plan quiet stretches as rest beats.
- **Living density.** Critics call RDR2 "hundreds of tiny stories playing out in plain sight"; Guerrilla aimed for tribes whose NPC behaviour reveals who they are. Systemic life can fill a stretch that would otherwise need a POI.

## 4. Regional anchors: legacy dungeons and landmark-led guidance (Elden Ring)

- **Legacy dungeons anchor regions** ("islands of classic level design", critics). Stormveil is built into the cliffside; lifts and ravines join surface to underground. Inside: loops, shortcuts, height, rooftop traversal. Interior rules (and Stormveil's lesson about untaught roof drops) are in `genre-dungeon-metroidvania.md` §6.
- **Landmarks, not markers.** Castles and cities visible from afar do the guiding and are packed with shortcuts and items, so following your eyes pays. Without markers, every major goal needs a silhouette that reads from its region's main vantages.
- **Build the anchor into the terrain.** A dungeon growing from a cliff or a city on the horizon is both landmark and foreshadowing vista.
- **Caution: repeated mini-dungeons.** Critics find the catacombs and caves smaller, without shortcuts and repetitive. Give each kit-built dungeon a signature, or make fewer.

## 5. Layered worlds: sky, surface, depths (TotK, Shadow of the Erdtree)

Stacked layers multiply a world without multiplying its footprint, and they are the hardest worlds to read. Floor-plane and map rules: `verticality.md`.
- **Use height to survey.** TotK's director: sky diving "brings more value as a tool for gathering information about the surface by surveying it from above." Dohta: diving works because the world is familiar; "If a location were completely unfamiliar to you, you'd probably be hesitant to dive down from the sky" (Nintendo, Ask the Developer). Give each new layer a vantage over a layer the player already knows.
- **Mirror layers so knowledge transfers.** [convention] TotK's Depths are commonly described as an inverted mirror of the surface, with Lightroots under surface shrines. A mapping rule between layers lets surface knowledge navigate the dark layer.
- **Blend open field and dungeon vertically.** Miyazaki on Shadow of the Erdtree: "not quite open field and not quite legacy dungeon, but something that kind of blends the two together and creates that better sense of verticality" (via GamingBolt quoting PC Gamer). A reviewer found himself "peep[ing] over cliffsides for hidden ledges… perplexing and, at times, discombobulating, but the promise of discovery kept me forging ahead" (PCGamesN).
- **The cost: the map stops working.** Critics: with stacked areas and no layer toggle, "players often have no idea how to get to a certain area of the map"; Sites of Grace overlap on the map though they are far apart in play; a map fragment (Ancient Ruins of Rauh) "is locked in a ravine deep below the zone", another (Jagged Peak) sits "all the way down in Cerulean Coast" (eXputer, opinion).
- **Fixes for layered worlds:**
  - Show layers on the map: a layer toggle or separate sheets, with markers saying which layer an objective or grace is on.
  - Put each map fragment on, or in clear view of, the layer it reveals.
  - Mark inter-layer connections (lifts, shafts, chasms) on every layer they touch.
  - Make the main entrance to each layer visible. Elden Ring's Siofra lift sits "in plain sight", trading surprise for accessibility, unlike Dark Souls' Great Hollow behind an illusory wall. Hide only optional entrances, and those must pass hidden-but-fair.
  - Give each layer a distinct palette, light and sound so the player always knows which layer they are on.
  - Keep any one area to ≤3 floor planes (TLDB).

## 6. Wayfinding without a HUD

- **Diegetic pointers.** Ghost of Tsushima's Guiding Wind blows toward the set waypoint; one wind field drives cloth, particles and grass, so the scene points the way (Rockenbeck, GDC 2021).
- **Know the pointer's blind spot.** Reviewers found the wind unclear on steep terrain. A 2D direction cue loses meaning where height matters; back it with a second cue on cliffs, in canyons and in caves (≥2 independent cues per critical decision).
- **Optional followers.** [convention] Golden birds to POIs, foxes to shrines, smoke columns at encounters: diegetic, and the player chooses to follow.
- **Markers as a setting.** [convention] If you ship markers, the world must still work with them off: the real test of the landmark layer.
- **Progress readability.** Journey added dunes and sand trails partly so terrain could show progress (`genre-rpg-narrative.md`). Roads, rivers and a growing horizon landmark do the same.

## 7. Optional dungeons inside the world (Skyrim)

Source: Burgess and Purkeypile, "Skyrim's Modular Approach to Level Design" (GDC 2013), and Burgess's iterative-process talk (GDC 2014).
- **Work in whole-world passes.** Bethesda ran iterative passes across all levels, finishing each pass everywhere before the next, with a "Content Complete" milestone nicknamed "Ship With Shame" before polish (The Escapist). Accounts of the exact number and names of passes conflict, so don't quote a count. The industry schedules for "done" when it should schedule for "good".
- **Plan layouts as flowcharts** carrying "beats, and pacing, and a general feeling of connectivity" before geometry.
- **Modular kits, small team.** Two staff built and refined the kits; repetition was hidden with clutter and "inserts". [convention] Strict grid, transition pieces, variation by lighting and silhouette (`metrics.md`).
- **The loopback ending.** Players observe that nearly every dungeon ends with a shortcut back to the entrance, a door that opens only from inside. Critics find it predictable when every dungeon does it; vary the exit (somewhere new, a vista, a one-way drop).

## 8. Survival-crafting worlds (Subnautica, Valheim)

Source: Robert Yang, "Mapping the sea floors of Subnautica" (Radiator Blog, 2018), unless tagged.
- **Without a map, terrain is the enemy.** Subnautica gives no world map, so "your real enemy is the land itself… Caves become mini-bosses; deep trenches become mega-bosses." Treat complex terrain as encounters to place and pace, not filler. Players navigate by "feeling the topology" and by landmarks ("pointy reef… round hill… kelp forest"): give each biome shape-distinct landmarks.
- **Key wrecks sit mid-biome.** "The designers usually have to place the key 'wrecks'… in the middle of each biome, and then just pray you see it." In a no-map world put progression POIs at biome centres and make them emit light or sound; in mapped worlds edges can be the interesting places.
- **World edges must read differently from explorable danger.** Crossing into the dead zone spawns a giant monster "with little warning", and its warnings are "impossible to differentiate… with any other dark dangerous void that you're actually supposed to explore." Give the boundary its own language (colour, sound, emptiness, a diegetic warning) that no playable area uses. Yang suggests an incomplete map poster players can photograph.
- **Goal beacons shouldn't stop mid-game.** "For the first half of the game, new SOS beacons appear every hour or so… by the second half of the game, there's no more beacons"; Yang missed about a quarter of the world in 40 hours. Keep a steady supply of pulls through the late game, or provide fallback beacons.
- **Depth as the progression axis.** Danger rises with depth and distance; the Safe Shallows are a lit, harmless home to return to; each ring outward needs a new tool (oxygen, vehicle depth module). Draw the rings and the item that opens each on the macro map (critic analyses).
- **Biome ladder table.** [convention] Per tier: threat, resources provided, capability required, boss or gate, and a landmark visible from the previous tier. [unverified] Valheim's progression (Meadows → Black Forest → Swamp → Mountains → Plains → Mistlands → Ashlands) is often cited with boss drops unlocking the next tier.
- **Procedural survival worlds need guarantees.** [unverified] Valheim's generator reportedly requires the Ashlands to border only sea. Encode progression-critical adjacency and resource sufficiency as generator checks (`genre-roguelike-procedural.md` §8).
- **Travel friction keeps geography meaningful.** [convention] Limits on what can be fast-travelled (e.g. Valheim's no-metal portals) make distance matter; provide flat, defensible base sites near resource borders.

## 9. Failure modes: templating and checklist fatigue

- **Template "?" marks.** Critics count Witcher 3's "?" POIs as about 20 templates reused many times; others argue they're optional filler. Watch the templated-to-unique ratio and avoid clusters of identical icons.
- **Map-reveal towers plus outposts.** Critics call the formula a cliché; the tower becomes a chore when its payoff is icons rather than a vista.
- **Symptoms:**
  - Players follow icons and ignore terrain → landmarks too weak or markers too strong.
  - Heatmap lines with dead space between → missing mid-range curiosities (§2).
  - "Seen it" fatigue by hour 10 → too few POI types; templates without signatures.
  - Players lost with nothing on screen → sightline test failed (§3).
  - Players stuck at a "climbable" cliff → blocker doesn't read as a blocker.
  - "How do I get there?" in a layered region → no layer map or hidden layer entrances (§5).
  - Late-game wandering with no goals → beacons stopped (§8).

## 10. Review checklist

- [ ] Macro graph: regions, anchors, corridors, soft gates and layers drawn before terrain
- [ ] Each region has a district identity; dominant traversal speed stated; spacing and landmark height derived from it
- [ ] Sightline test passed at every reachable vantage (≥1 far landmark + ≥1 nearer curiosity)
- [ ] Chains of interest authored; triangles at three scales (landmark / view-blocker / tempo); rectangles for hard reveals
- [ ] POIs tiered and varied by verb; deliberate empty stretches planned
- [ ] World works with markers off; diegetic pointer backed by a second cue on steep or enclosed terrain
- [ ] Layered worlds: map shows layers; fragments on the layer they reveal; inter-layer links marked; main layer entrances visible; layers look and sound distinct; ≤3 floor planes per area
- [ ] Optional dungeons: loopback exit varied; each kit-built dungeon has a signature
- [ ] Survival: key POIs mid-biome and emissive; world edge has its own warning language; beacons continue through the late game; biome ladder table written; generator guarantees checked
- [ ] Hard blockers read as blockers; no invisible walls on climbable-looking terrain
- [ ] Heatmap plan for clustering and untouched regions; fix with curiosities, not markers

## 11. Worlds to study

- **Pull and concealment:** Breath of the Wild (Great Plateau, tower placement, Korok anomalies).
- **Layered worlds:** Tears of the Kingdom (sky, surface, Depths); Elden Ring underground (Siofra, Ainsel); Shadow of the Erdtree (as achievement and as map-readability warning).
- **Anchors:** Elden Ring (Stormveil, Leyndell, Volcano Manor; catacombs as counterexample).
- **Diegetic wayfinding:** Ghost of Tsushima, Ghost of Yōtei.
- **Optional dungeons at scale:** Skyrim (Blackreach, Labyrinthian), Fallout 3.
- **Survival-crafting:** Subnautica (Safe Shallows → Lost River; the dead zone as a counterexample); [convention] Valheim biome ladder.
- **Living density / speed-driven scale:** Red Dead Redemption 2, Horizon Forbidden West; Marvel's Spider-Man.
- **Failure modes to study critically:** Witcher 3 with markers on vs off; tower-era Assassin's Creed and Far Cry.

Key sources (full list in `SOURCES.md`): CEDEC 2017 translation (Walker gist) and Game Developer on BotW; Nintendo Ask the Developer (TotK); GamingBolt (Miyazaki), PCGamesN and eXputer on Shadow of the Erdtree; "The Best of Elden Ring's Level Design" (Substack); Robert Yang, Radiator Blog (Subnautica); The Escapist (Burgess); GDC 2021 (Rockenbeck).
