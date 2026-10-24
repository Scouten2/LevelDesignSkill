# Turn-Based Grid Tactics

## Contents
1. Choose the information model first
2. Map size and the tile economy
3. Cover lines, flanks and chokes
4. Elevation, line of sight and shove (verticality)
5. Objectives that defeat turtling
6. Deployment, spawns and reinforcement telegraphs
7. The environment as a toolset
8. Readability on a grid
9. Campaign pacing across maps
10. Procedural maps: authored sockets, not cells
11. Symmetric and versus maps (Advance Wars-like)
12. Greybox, verification and the bundled scripts
13. Common failures → fixes
- Review checklist
- Levels to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Tactics maps are information puzzles: the layout decides what the player knows, where friction sits and why standing still loses. General encounter theory is in `genre-action-combat.md`; grid notation in `grid-conventions.md`; height in `verticality.md`.

---

## 1. Choose the information model first

Write one line in the brief before drawing anything: *at the start of a player turn, what does the player know?* (enemy positions, enemy intentions, hit odds, reinforcement timing and location). Everything else follows from it.

- **Perfect information, deterministic (Into the Breach).** "Battles are fought on a relatively small eight-by-eight grid"; "There is no fog of war and no percentages governing whether my attacks hit or miss"; the Vek "show you their intended attack and give you a chance to respond before they execute it" (PC Gamer preview). Justin Ma: "We wanted to come up with something that would be fun regardless of the AI." The map is a puzzle you can read completely; difficulty comes from more threats than the player can answer in one turn, not from surprise.
- **Hidden information, probabilistic (XCOM, Fire Emblem fog).** XCOM enemies sit in pods at set points and activate, moving to cover, once revealed (Game Developer, XCOM deep dive). The map is a scouting-and-risk problem: it needs room to probe, fall back and choose where the first fight happens.
- **Bounded chance keeps lost positions worth playing.** Apart from random spawns, Into the Breach's only chance element is "Resist" (a building may survive a hit). Ma: before it, "if you knew you were going to lose the game from the next enemy attack, there was no reason to hit End Turn" (Cliqist interview, 2018). If you add randomness, add it where it rescues hopeless turns, not where it punishes good plans.
- **Don't mix models silently.** A perfect-information game with one unannounced ambush breaks its contract. Any exception must be taught and signposted (§6).

## 2. Map size and the tile economy

- **Size scales inversely with information** [convention]. Full information plus deterministic rules works on a tiny board where every tile matters (ITB's 64 tiles); hidden information needs room to scout and retreat, so the board grows.
- **Count live tiles.** List every tile that changes a decision (cover, hazard, blocker, objective, spawn, height change, chokepoint). On a perfect-information board, aim for most tiles to be live [convention]; on a larger map, aim for each *region* to offer a distinct decision. Dead acreage is walking tax.
- **Measure the map in unit-turns, not tiles** [convention]. Record: turns for a standard unit to cross the map; turn of expected first contact; turns from deployment to the objective. Put these numbers in the brief and recheck after any change to move ranges.
- **One move should reach the next useful position** [convention]. If a standard move from cover cannot reach other cover or a flank tile, the open gap is a kill zone; make that deliberate or close it.

## 3. Cover lines, flanks and chokes

- **Cover is a number, so place it like one.** XCOM 2 low cover gives +20 Defense and high cover +40 (XCOM wiki; not checked against game config) [unverified]; Defense subtracts from attacker aim. A blog simplification quotes "25%/50%"; don't use it.
- **Every cover line has a flank, and every flank has a cost** [convention]. Flanking negates directional cover in XCOM [unverified]. If cover is absolute, the fight is a stand-off; if flanks are free, cover is meaningless. Price flanks in exposure, an extra turn, or a hazard.
- **Cover everywhere, quality uneven** [convention]. Movement should be cover-to-cover; the decision is *which* cover (high vs low, near the objective vs safe).
- **Single-tile routes jam both sides** (Fire Emblem community map critique, FE Universe) [convention]. The cheapest fix is a second traversable tile. Keep a one-tile choke only when the stall is the intended puzzle, and say so in the brief.
- **Penalty terrain belongs off the critical path** (FE community critique) [convention]. Slowing terrain on the only route makes the map tedious, not tactical.
- **Fliers skip terrain** ("fly-skipping", FE community) [convention]. Water and mountains meant to slow the player do nothing to flying units; counter with anti-air placement or accept the skip as a reward.

## 4. Elevation, line of sight and shove (verticality)

Height on a tactics grid is a combat position first, but give it a second job from `verticality.md` (preview, cheap commitment, hidden route).

- **High ground is a modifier, so it needs a counter** [convention]. XCOM and BG3 both reward attacking from above (XCOM forum figure +20 aim; BG3 attack bonus from height) [unverified]. Every perch needs a contest: a reachable route up, a flank onto it, a destructible support, or exposure while climbing.
- **Survey perches** [convention]. A climbable tower that reveals a pod or the objective turns height into information, the strongest reason to climb in a hidden-information game.
- **Drops are cheap, climbs are expensive.** Let units drop quickly (with clear fall-damage bands) and climb slowly; this creates one-way commitments the player plans around. BG3 players complain about fall damage from ledges "barely over your character's head" (Steam forum) [unverified]; keep damage bands consistent and readable.
- **Shove makes ledges a weapon** (BG3, ITB push/pull) [convention]. Each ledge or hazard edge is usable by both sides; telegraph it so a lost unit was a readable mistake.
- **Readable tiers.** Draw a section view for any map with ≥2 floor planes; in game, height needs silhouette, cliff-edge shading and a UI tier indicator, not texture alone.
- ITB has no height; mountains do the work of blockers that stop movement and shots (ITB wiki) [unverified]. Don't add elevation just because the genre usually has it.

## 5. Objectives that defeat turtling

Turtling means the best play is to hold the deployment zone. If it is, the map's geometry doesn't matter.

- **State why the player must move.** Into the Breach makes buildings the stakes: each building lost brings the mechs closer to shutdown (Cliqist, 2018). XCOM 2 uses mission timers [unverified: typical length]. Fire Emblem's vocabulary is Rout, Seize, Defeat Boss, Defend/Survive N turns, Escape [convention].
- **One geometry, several plays.** The same map plays differently under rout, seize, escort, defend or escape. Vary objectives across a campaign before you vary layouts.
- **Side objectives create routes** [convention]. Villages to visit before bandits reach them, chests, a rescue: put them off the main line so the player trades tempo for reward (autonomy; see `fun-checks.md`).
- **Check the optimal line leaves cover at least once** [convention]. Trace the route that the best player would take; if it never crosses exposure, the objective isn't doing its job.

## 6. Deployment, spawns and reinforcement telegraphs

- **Deployment is the first decision.** A restricted deployment zone with options inside it (which flank, who goes forward) gives autonomy before turn 1 [convention].
- **Telegraph spawns.** ITB shows attacks before they resolve; in a deterministic game, spawn tiles shown a turn ahead [unverified: exact rule] let the player block or prepare.
- **Front-load; limit reinforcements; never drop an untaught rear ambush** (FE community: "2–3 guys drop on you" stalls the advance; powerful surprise reinforcements "feel cheap") [convention]. Announce reinforcements through narrative, visible doors or markers.
- **Reinforcements don't act on arrival** [convention]. A unit that appears and attacks in the same enemy phase is unanswerable, so it reads as unfair.
- **Where the reveal happens matters more than how many** [convention]. Place XCOM-style pods so the first contact occurs where the player has cover options, not mid-street.

## 7. The environment as a toolset

- **Hazards are puzzle pieces** [convention]. ITB's push/pull into water, chasms and other units, and BG3's surfaces and explosive barrels [unverified: specific combos], turn the map into the player's arsenal. List each hazard and the verb that exploits it.
- **Hazards work for both sides and show their result before commit** [convention]. In a perfect-information game, preview the outcome; in a hidden-information game, at least preview the area.
- **Destructible cover changes the board mid-fight** [convention]. Use it to stop stand-offs; never let it delete the only route to the objective.

## 8. Readability on a grid

- **Every tile state readable at a glance:** passable, blocking, cover level, hazard, height tier, objective, spawn. Use shape and icon as well as colour (`accessibility.md`).
- **Preview what will happen:** movement range, line of sight from the hovered tile, threat ranges, and (in deterministic games) the enemy's queued attacks.
- **Art must not hide a proven affordance** (gameplay-first stance). After the art pass, recheck cover readability: a prop that looks like cover but isn't is a bug.

## 9. Campaign pacing across maps

- **One new terrain or enemy idea per map**, then develop and combine it (teach → develop → twist → conclude; `principles.md`).
- **Raise difficulty through composition, objective and tempo, not HP** [convention]. Bigger health bars make turns longer, not decisions harder.
- **Mandatory maps easier than you think; hard maps optional and signposted** (`fun-checks.md`).

## 10. Procedural maps: authored sockets, not cells

- **XCOM 2's plot-and-parcel model.** Jake Solomon: "If you view our maps as a giant quilt, than [sic] we simply punch out the individual tiles in the quilt and replace them with whatever we want." Plots are the groundwork; parcels (a parking lot, a building) are inserted piece by piece (Solomon via Game Developer; Hess, GDC 2018). The motivation was repeat players meeting the same maps.
- **Author the parcels; generate only the combination.** Each parcel carries its own cover and sightlines; sockets fix size, entry points and road connections.
- **Validate every combination** [convention]: all deployment and objective tiles reachable; no spawn within one enemy move of deployment; cover density within bounds per region; no LOS lane spanning the whole map unless intended. See `genre-roguelike-procedural.md` §8.

## 11. Symmetric and versus maps (Advance Wars-like)

- **Symmetric maps are nearly always balanced; asymmetric ones are hard to balance** (ModDB skirmish-map guide) [convention]. Disguise symmetry with features that look different but work the same.
- **Compensate first-move advantage** (extra income, an extra property or unit for player 2) [convention]; test both seats.
- **Income sources snowball.** A designer found two generators produced a 2-vs-0 lead the loser "can almost never recover from", and richer maps were more lopsided (BGDF forum) [convention]. Advance Wars cities fund units each turn [unverified: amounts]. See `genre-strategy-rts.md` §6.

## 12. Greybox, verification and the bundled scripts

- **Prove it on paper first.** A tactics greybox is a grid, tokens and the rules sheet: play three turns by hand before any 3D. If the map isn't interesting with tokens, art won't save it.
- **Never claim a map is balanced or winnable without evidence.** For a deterministic puzzle-mission, write the enemy turn out move by move and label it "hand-traced, not machine-verified"; traces past ~20–25 moves are unverified by default.
- **Lint and measure grid maps.** Draw the walkability layer with the puzzle legend (`#` blocking, `-` floor; list cover, hazards and spawns as a `(col,row)` key-object list per `grid-conventions.md`) and run `python3 -I scripts/grid_lint.py map.txt --legend puzzle` then `scripts/level_metrics.py map.txt --legend puzzle`. Read *corridor ratio* and *dead-end cells* as a jam warning (§3), *regions* > 1 as an unreachable pocket, and `--compare` to prove procedural variants are actually different. The scripts do not model cover, LOS, elevation or unit stats; check those by hand and say so.
- **Zone graphs.** For larger maps, draw deployment → regions → objective as a graph and run `scripts/graph_check.py` to confirm reachability and count loops (flank routes show up as cycles).

## 13. Common failures → fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Players turtle in the start zone | Objective doesn't force movement | Add stakes (buildings, timer, escape, villages) |
| Stand-off behind cover | Cover absolute, no flank | Add a priced flank route or destructible cover |
| Traffic jam on one tile | Single-tile route | Widen to two tiles or add a parallel route |
| "Cheap" loss after a spawn | Untelegraphed or acting-on-arrival reinforcements | Show spawn tiles, front-load, delay first action |
| Fliers trivialise the map | Terrain is the only obstacle | Anti-air coverage, objectives fliers can't solve alone |
| Hopeless turns, players quit | Deterministic loss foreseeable | Bounded rescue chance (Resist) or a clearer earlier warning |
| Height ignored | High ground unreachable or unreadable | Visible climb routes, tier UI, a survey reward |

## Review checklist

- [ ] Information model written in one line before layout
- [ ] Unit-turn numbers recorded: crossing time, first contact, deployment-to-objective
- [ ] Live-tile list made; no large dead regions
- [ ] Every cover line has a flank with a cost; no unintended single-tile route
- [ ] Penalty terrain off the critical path; flier behaviour considered
- [ ] Every high-ground perch has a counter; at least one height gives information, not just a bonus
- [ ] Section view drawn for ≥2 floor planes; fall-damage bands consistent
- [ ] The optimal line leaves cover at least once; objective explains why the player must move
- [ ] Spawns and reinforcements telegraphed; none act on arrival; no untaught rear ambush
- [ ] Each hazard listed with the verb that exploits it; outcomes previewed
- [ ] Tile states readable without colour alone; post-art cover recheck done
- [ ] Procedural parcels validated per combination; variants compared with `level_metrics.py --compare`
- [ ] Balance/winnability claims backed by a script run or a labelled hand trace

## Levels to study

- **Into the Breach:** any early island mission, for the 8×8 tile economy, telegraphs and building stakes.
- **XCOM 2:** timed missions and pod reveals for anti-turtling and reveal placement; **XCOM: Enemy Unknown** for its handcrafted maps.
- **Fire Emblem:** chapters discussed in the FE Universe map-design threads, for jams, fly-skipping and reinforcement critique [convention].
- **Baldur's Gate 3:** elevation, shove and surface combos in Act 1 encounters [unverified].
- **Advance Wars:** pre-deployed campaign maps (puzzle-like) vs build maps (economic) [convention].
