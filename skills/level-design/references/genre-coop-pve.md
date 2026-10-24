# Co-op PvE Level Design

## Contents
1. What a pacing director needs from the level (Left 4 Dead)
2. Director numbers and what they mean for space
3. Crescendos, finales and hold points
4. Arenas: chains of smaller arenas, detours with their own perils
5. Procedural co-op: room templates with exit nodes (Deep Rock Galactic)
6. Live game-mastering (Helldivers 2)
7. Separation, disablers and revive spacing
8. Two-player asymmetric co-op (Hazelight)
9. Versus and PvP conversions of co-op maps
10. Verticality in co-op
11. Review checklist
12. Levels to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Related: the Director loop summary in `principles.md`, beat charts and pacing in `process.md`, encounter design in `genre-action-combat.md`, co-op puzzle priming in `puzzle-sequencing.md`, verticality functions in `verticality.md`.

---

## 1. What a pacing director needs from the level (Left 4 Dead)

Valve's primary source is Michael Booth, "The AI Systems of Left 4 Dead" (Valve, 2009). Its case against hand-placed encounters: "Players are good at memorizing all static locations… Removes suspense… Results in 'optimal strategy'… Kills cooperation and degenerates into a race." Even "multiple sets of manually placed triggers/scripts fails". The Director replaces placement with "structured unpredictability" ("not purely random, nor deterministically uniform"), but it can only spend what the level gives it. The designer's side of the contract:

- **A clean nav mesh and an unambiguous escape route.** The Director measures **flow distance** ("travel distance from the starting safe room to each area"); the escape route is the shortest path from start safe room to exit. Side areas are fine; keep flow distance mostly increasing along the route so "ahead" and "behind" stay meaningful. [convention]
- **Off-sightline spawn pockets on every side, including behind and above.** Population is created and destroyed in the Active Area Set around the team. Specials spawn in areas "not visible by the Survivor team"; "Boomers spawn ahead, since they are slow… Smokers attempt to select areas above the Survivor team." Mobs mostly come from behind (§2). Every stretch needs hidden pockets ahead, behind and above.
- **Designer-placed candidate item spots.** "Map designer creates several possible weapon caches in each map, the AI Director chooses which will actually exist" (same for scavenge items). Booth's reasons: it "allows visual storytelling/intention" and solves placement problems (a gun leaning on a wall, mounted in a rack). Place several candidates per cache, each in a spot that tells a story.
- **Boss slots along the route.** Bosses are "positioned every N units along 'escape route' +/- random amount… Three Boss events are shuffled and dealt out: Tank, Witch, and Nothing. Successive repeats are not allowed." So any stretch of the route may host a Tank fight: avoid long sections too narrow to fight a boss in. [convention]
- **Safe rooms bracket each map.** Wanderer counts are set at map start from escape-route length and target density.
- **Off-sight recovery spots.** A SurvivorBot that falls out of place "is teleported near the team when no human is looking at it", which needs geometry where nobody is looking.

## 2. Director numbers and what they mean for space

| Booth (2009) | Value | Level implication |
|---|---|---|
| Mob size | "a large group (20-30)" | Routes and holds must fit a 20–30 enemy rush; chokes become kill zones, so give them a second approach |
| Mob interval | "randomized intervals (90-180 seconds on Normal difficulty)" | A stretch the team crosses in under ~90 s may see no mob; long stretches will see several |
| Mob direction | "75% of Mobs come from behind, since wanderers and Special/Boss Infected are usually engaged ahead" | Every segment needs an open rear arrival route, not only a front one |
| Sustain Peak | "3-5 seconds" | Peaks are short; the fade waits for "a natural break in the action" |
| Relax | "for 30-45 seconds, or until Survivors have traveled far enough toward the next safe room" | Fill relax stretches with traversal, scavenging and orientation, not empty corridors |
| Intensity | rises with damage, incapacitation, being pulled or pushed off a ledge, nearby kills; doesn't decay while infected are engaging | Ledges and drops are intensity sources: place them where you want peaks |

Bosses are not affected by adaptive pacing, and Booth is explicit: "Algorithm adjusts pacing, not difficulty." Don't describe a director as dynamic difficulty; design levels whose structure survives any pacing roll. When you write a co-op beat chart (`process.md`, `beat_lint.py`), mark which beats are authored and which are director-variable.

## 3. Crescendos, finales and hold points

- **Make the most fun way also the best way.** L4D's original formula ended maps in a "crescendo moment" hold, which "led to players yelling at each other for not playing the game 'right'" (Chet Faliszek, Joystiq 2009). L4D2 redesigned crescendos so the fun way was also the optimal way: in The Parish, the alarm-off switch sits atop a central tower, so the team must "battle through a gauntlet" instead of camping.
- **Objectives that force movement** beat static holds. If the optimal strategy is to camp one corner, the event degenerates; move the objective, add a timer that moves, or put the switch across the arena.
- **Pacing tools in geometry.** In L4D2 the Director can make a graveyard path "longer or shorter depending on how well the Survivors are doing"; a storm level cuts visibility and hides teammate outlines in fog. Author variable-length sections and weather that changes sightlines.
- **Finale anatomy** (radio trigger, finale nav area, escape vehicle, all-aboard check, teleport spots) comes from Valve's wiki, which could not be read [unverified].
- **Hold points** [convention]: at least three approaches including one from above; a resupply point the team must leave cover to use; revive-safe pockets (§7); a readable end condition; and no single spot that covers every approach.

## 4. Arenas: chains of smaller arenas, detours with their own perils

Fatshark's "Level Design Lookback" (Vermintide 2 dev blog):

- **Chain medium arenas instead of one big one.** An end event "was originally intended to be an open arena, but it was confusing and hard to balance, so we made it a linear event with a number of smaller 'arenas'… we could balance the event and control the experience better."
- **Detours must cost something.** An optional detour around a Beastmen trap "needed to have its own perils as we didn't want players taking the detour every time without weighing the risk."
- **Unique rooms beat mazes.** Castle Drachenfels was made less maze-like: "make the rooms more unique so it would be easier to understand where you are", with balconies for a sense of upward progress.
- **Puzzle mix for co-op.** Challenge puzzles: "one puzzle should be co-op oriented, one should engage the community, and one should be randomized". Candle timers were lengthened so solo players could also solve them; check co-op puzzles at the lowest supported player count.
- Correction: Fatshark's posts do not say "no long chokepoints"; don't attribute that rule to them.

## 5. Procedural co-op: room templates with exit nodes (Deep Rock Galactic)

Ghost Ship Games' cave-generation post ("Below Decks"):

- **Pearls on a string.** "Cave systems come together like pearls on a string: one room at a time, connected by narrow, winding tunnels." Rooms are hand-crafted, "over 100 cave room templates" (later "119 hand-crafted rooms and 10 biomes").
- **Templates are sockets.** Rooms are built from intersecting spheres, half-spheres and planes with inner and outer noise bounds; **half-domes on the perimeter mark potential exits**, which the generator links with tunnels. Author your own templates the same way: shape, size class, marked exit nodes.
- **Rooms funnel without being mazes.** A cave "should require players to carve out terrain and use their traversal tools… but it shouldn't feel like a maze… individual rooms should still feel intuitive, with their shapes 'funneling' players through to the next exit" (Anders Heindorff Frederiksen).
- **Playtest each room with each class.** Frederiksen plays each room "with Scout, then Driller, and so on", and fails rooms with bad visibility or that are "unplayable as some classes".
- **Mission arc.** "It begins with the descent… dig up the necessary resources… Once that quota has been filled, the countdown is triggered, and you battle upward to the extraction pod" (PCGamesN). Deeper networks are "far trickier to traverse and escape from".
- For generator guarantees (reachability, item placement) see `genre-roguelike-procedural.md`.

## 6. Live game-mastering (Helldivers 2)

- Each planet has "several randomly generated sets of drops", and a single Game Master adjusts enemy forces "stronger or more forgiving depending on objective progress", modelled on tabletop RPGs (Arrowhead, via MP1st/PC Gamer).
- Players formed attachments to specific planets (Malevelon Creek), and Arrowhead has talked about making planets "more of a character". Give each map or biome a distinct identity players can name and remember.
- No primary source covers Helldivers' objective or extraction placement; treat any spacing numbers as [convention].

## 7. Separation, disablers and revive spacing

No primary source gives revive timings or co-op spacing; everything here is [convention] unless noted.

- **Separation is the threat.** Pinning or pulling enemies (L4D's Smoker, Hunter, Charger, Jockey; Vermintide's Packmaster) punish isolation. Ledges, ladders and side rooms are isolation risks; Booth confirms being pulled or pushed off a ledge raises intensity.
- **Forced splits rejoin fast.** If geometry splits the team (one-way drops, single-file ladders, two-lever doors), rejoin them within sight and a short walk, and don't spawn a horde at the split.
- **Revive needs a stationary teammate for several seconds.** Give hold areas and long fights small revive pockets: cover on two sides, out of the main mob lane.
- **Regroup points** after every one-way drop or vertical split: a visible, safe-ish spot where the team naturally re-forms.
- **Optional side rooms** should be short enough that the rest of the team can wait or follow without losing tempo.

## 8. Two-player asymmetric co-op (Hazelight)

Hazelight's sources were mostly unreadable (JS-only blog, GDC abstract only), so these are [unverified] or [convention].

- *It Takes Two* is co-op-first, with each level introducing a new mechanic [unverified]. *Split Fiction* uses per-chapter asymmetric ability pairs and puzzles that are impossible unless both players contribute [unverified]. Hannes Gille's GDC talk "Designing the Final Level of Split Fiction" argues for simplifying so players have room to be "blown away" [unverified].
- Design recipe [convention]: give each chapter an ability pair; make puzzles need both players, ideally acting at the same time rather than taking turns; let one player create the other's path (hold a platform, light a room, carry); retire or twist the pair each chapter (teach → develop → twist → conclude); never leave one player idle for long while the other solves.
- Prime the hard leap early: Valve found that a stepping-stone puzzle right before Portal 2's trickiest co-op leap "almost completely robbed the appeal", while priming it four chambers earlier kept the epiphany (`puzzle-sequencing.md`).
- With a shared screen or split screen, keep both players' immediate goals visible to both; communication is part of the puzzle.

## 9. Versus and PvP conversions of co-op maps

Fatshark on converting a Vermintide 2 map to Versus ("A Grudge Served Cold"):

- Good candidates have open layouts and few "empty backfaces or 'half-built' structures", because attacking specials climb and leap everywhere; "geometrically complicated" levels are hard to convert. Finish every surface a player could reach.
- Built-in world events help. The level was too long, so its start was cut; capture zones and a payload were added "to reduce the endless running and allow the pact-sworn to break the Heroes' dash".
- "Shortcuts, vantage points, etc. are very important." Cover the level with a "net" of climb transition points, but not too many, or the UI bloats. Scale enemy compositions and terror events down when players add pressure.

## 10. Verticality in co-op

- **Above is a spawn direction.** Smokers choose areas above the team; place spawn pockets on roofs, catwalks and ledges, not only around corners.
- **Descend to work, climb to escape.** DRG's arc (descent, quota, countdown, battle upward to the pod) turns vertical direction into pacing; cave intersections create "huge, 100 metre drops" (PCGamesN). See `verticality.md` on matching net vertical direction to emotion.
- **Upward progress reads as progress.** Fatshark added balconies to Castle Drachenfels for a sense of climbing.
- **Vertical splits are separation risks** (§7): single-file ladders and one-way drops need a regroup point at the far end. [convention]

## Review checklist

- [ ] Escape route unambiguous; flow distance increases along it; safe rooms (or equivalents) bracket the map
- [ ] Hidden spawn pockets ahead, behind and above along every stretch; open rear arrival routes (mobs mostly come from behind)
- [ ] Several designer-placed candidate spots per item cache, each telling a story
- [ ] Boss-capable space at regular intervals along the route; no long stretch too narrow for a boss fight
- [ ] Relax stretches have traversal/scavenge content; ledges and drops placed where peaks are wanted
- [ ] Crescendos/finales force movement; no single camping spot is optimal
- [ ] End events are chains of medium arenas; optional detours carry their own risk
- [ ] Rooms are distinct and nameable; procedural templates have marked exit nodes and pass a per-class playtest
- [ ] Forced splits rejoin quickly; revive pockets in hold areas; regroup points after one-way drops [convention]
- [ ] Two-player puzzles need both players, minimise idle time, and are primed before the hard leap
- [ ] Co-op puzzles and timers work at the lowest supported player count
- [ ] Beat chart marks authored vs director-variable beats; "pacing, not difficulty" respected

## Levels to study

- **Left 4 Dead / Left 4 Dead 2** (Valve): No Mercy (safe-room-to-finale structure); The Parish (tower crescendo that forces movement); Hard Rain (storm visibility as pacing) [convention].
- **Deep Rock Galactic** (Ghost Ship Games): any standard mission for room-and-tunnel structure; Refinery missions for merged caverns.
- **Vermintide 2** (Fatshark): Castle Drachenfels (unique rooms, balconies); end events built as chains of smaller arenas.
- **Helldivers 2** (Arrowhead): live game-mastering and planet identity.
- **It Takes Two, Split Fiction** (Hazelight): asymmetric ability pairs; **Portal 2** co-op (Valve): priming the logical leap.

Sources: Booth, "The AI Systems of Left 4 Dead" (Valve, 2009); Joystiq/Engadget L4D2 hands-on (Faliszek, 2009); Ghost Ship "Below Decks" (via DevTrackers); PCGamesN on DRG; Vermintide dev blogs ("Level Design Lookback", "A Grudge Served Cold"); MP1st/PC Gamer on Helldivers 2; Wikipedia and TechRadar on It Takes Two; Hazelight blog and GDC schedule (unread); Portal 2 developer commentary.
