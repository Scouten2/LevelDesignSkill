# Multiplayer & Competitive Maps

## Contents
1. Universal rules (all competitive maps)
2. Height in competitive maps: high ground with counters
3. Arena shooters (deathmatch, duel)
4. Tactical / round-based (CS, Valorant, Siege)
5. Team objective (attack/defense, payload, CTF, Conquest, CoD modes)
6. MOBAs
7. Battle royale
8. Extraction / PvPvE (Arc Raiders, Hunt, Tarkov)
9. Fighting stages and arena sports (Smash, Rocket League)
10. Racing (pointer)
11. Review checklist
12. Maps to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Core refs: typology vocabulary (three lane, figure 8, sniper nest) in `layout-and-flow.md`; height and floor planes in `verticality.md`; engagement distances in `metrics.md`; co-op PvE in `genre-coop-pve.md`; tracks in `genre-racing.md`; UGC islands in `genre-ugc-platforms.md`.

---

## 1. Universal rules

- **Three lanes is the default skeleton.** Treyarch's Vonderhaar: three lanes mean "there's never more than three decisions in your brain about how you move or where you check." Separate lanes with buildings or obstructions so each reads as its own space.
- **Every lane needs a purpose** (Scronce, Treyarch): distinct ranges and roles, e.g. a close-quarters mid and longer side lanes. "If this lane has a power position… you most likely want an opposing power position."
- **Flow first, items last.** Settle routes and timings in greybox; items are tuning knobs on a layout that already works.
- **Weapons and space are designed together.** Blood Gulch's base-to-base distance is why Halo's sniper got a scope.
- **Timings decide first contact.** [convention] Stopwatch every spawn-to-objective and spawn-to-choke route at standard speed; equal or deliberately offset arrivals decide who wins each choke. Record timings and re-measure after every change.
- **Spawns.** [convention] No line of sight to enemy spawns or high-traffic power positions; several protected exits with cover outside; several spawn clusters so dynamic spawning can flip without spawn-trapping; one-way doors on attack/defense spawn rooms; distinct landmarks for instant orientation.
- **Readability and callouts.** Every area needs a unique, nameable look: Dust2's "Xbox", Vondel's colour-coded rooftops, giant A/B/C site letters. Respawn relit Kings Canyon purely for readability.
- **Choose a symmetry model on purpose:** mirror (simplest, can carry handedness or lighting bias); rotational (MOBAs, Splatoon, many CTF maps); asymmetric (tactical, attack/defense; balance with side swaps and win rates). Symmetric maps still need hand-tuning (Riot's 2024 Summoner's Rift side fixes).
- **Map size vs player count.** Smaller maps mean more encounters. [convention] Time to first contact ~5–15 s in arena and CoD-style modes; scale area with player count; tune in playtests.
- **Iterate with data.** Riot playtests Valorant maps several times a week; Ascent spent ~3 of its 5 years in greybox. DICE uses movement heatmaps; Treyarch edits maps after launch. Find dead zones and over-used routes.

## 2. Height in competitive maps: high ground with counters

- **Floor planes.** "Most maps tend to max-out at three different floor planes for any given area… a fourth (p)lane doesn't add new dynamics" (TLDB, Verticality). Merge minor height changes into one floor.
- **Aim input sets the height budget.** Console players "often park their camera's vertical rotation aimed at roughly head / chest height"; levels for them "rarely incorporate very tall height changes", and high-frequency height variation frustrates gamepad users (TLDB). Counter-Strike stays "relatively flat" for low-sensitivity aim; boosting (players standing on each other) adds situational height that rewards team coordination.
- **Every height advantage has a counter.** Pair power positions (Scronce); give each high spot a flank route up, an exposure cost on the climb, or a counter-sightline. Q3DM17's jump pads create strong upward flow with little cover, and a far sniper platform counters the predictable flight arcs (TLDB).
- **Lanes tame 3D movement.** Titanfall 2 moved from a "3D 'Swiss cheese' effect" to a "'window pane' effect… the left, the middle, the right", because point-to-point routes "just becomes a mess" (Fukada, Shacknews 2016). Wall-running, jetpacks and grapples still need lane structure.
- **Draw a section** for every multi-floor area; annotate drops, ladders and lifts (`verticality.md`). Callouts must name floors ("A-upper", "B-lower").

## 3. Arena shooters (Quake, Unreal Tournament, Halo arena)

- **Topology:** compact loops, no dead ends, several floors joined by lifts, jump pads and drops. [convention] Circular or figure-eight routes for chase and escape.
- **Item control is the game.** The strongest item (Quad, Overshield, Rocket Launcher) sits behind a choke in a contested central spot; announce spawns (Quake's Quad every ~2 min, lasting ~30 s, with a warning), which schedules the fight; spread major items so holding one costs position on another.
- **Health and ammo:** health where damage is likely, more in areas players revisit; even ammo counts so no weapon is forced.
- **Sightline design:** Halo's Lockout (Carney) joins isolated rooms by bridges: you see where opponents head but not where they end up. Lockout drew on Quake's DM6, three levels where every path feeds back to the middle.
- **Scale:** [convention] a skilled player crosses the map in ~10 s. **Spawns:** many, spread, away from item hotspots, weighted away from enemies.

## 4. Tactical / round-based (Counter-Strike, Valorant, Rainbow Six Siege)

- **Template:** three lanes, two sites, a mid connecting lanes for splits and rotations (Dust2: Long A, B Tunnels, mid).
- **Mid control is round-deciding.** No mid needs a substitute rotation tool: Bind's teleporters.
- **One signature mechanic per map** changes rotation logic: Ascent's doors, Bind's teleporters, Lotus's rotating doors, Siege's destructible walls.
- **Deliberate asymmetry serves a goal.** Fracture's two attacker spawns force defenders out.
- **Site design.** [convention] 2–3 entrances per site; defender spawn closer to sites; rotations through defender-favoured space; break long angles so utility has counterplay.
- **Balance metric:** attacker/defender round win rate per map, ~50/50; expect drift as kits change (Valorant drifted defender-sided).
- **Destruction (Siege):** the level "is going to be opened up and has to make sense": design closed and opened states; protect key routes (Siege limited floor destruction); prototype by toggling walls. [convention] Several objective rooms per building, several breach options per room.

## 5. Team objective (Overwatch, TF2, Call of Duty, Battlefield, Splatoon)

- **Attack/defense points:** defenders get high ground; attackers need 2–3 routes including a flank. A single choke under central high ground fails (Overwatch's Paris first point was removed from rotation).
- **Health packs as risk/reward:** big pack on the flank, small pack near the main route (Oasis).
- **Payload pacing:** the cart's steady speed stops attackers capturing the next point before defenders are ready.
- **Unlock structures:** TF2's Gravel Pit opens A and B, then C once both fall.
- **Class geometry:** [convention] high ledges for jump classes, crossable sniper lines, flank doors for infiltrators, choke widths tuned for turrets.
- **Combined arms (Battlefield):** balance Conquest first; BF V used 5–7 flags; split big maps into sectors (infantry clusters vs vehicle ground), each flag a different fight.
- **CoD-style:** paired power positions, spawns that "make sense", small maps like Nuketown for intensity.
- **Territory (Splatoon):** [convention] rotational symmetry; paintable surfaces are both movement network and score; unpaintable materials gate routes.

## 6. MOBAs

- **Structure:** [convention] three laned towers, quadrant jungle, a river with neutral objectives, bases in opposite corners, rotational symmetry.
- **Brush and vision are the information layer.** Riot moved top-river brush to the river's centre so it was "less side-skewed and more powerful when contested."
- **Objective timing can break lane rhythm.** Early Rift Herald overrode laning; check neutral objectives against the phase they sit in.
- **Side fairness** is tuned by hand; camera angle makes rotational sides unequal.

## 7. Battle royale

- **POI spacing and loot tiers spread the drop.** Hot drops carry proportionally more early fights; outskirts give safer, lower-tier loot.
- **Pacing = distance between POIs + time to cover** (Beenox, Vondel). Mix close, mid and long fight spaces.
- **Rotations:** Respawn reworked Kings Canyon to "encourage proactive rotation strategies over reactive third-party play", removing defensible interiors from a rotation area and cutting routes. A route is open and fast or deliberately risky.
- **Zone:** wait, shrink and damage per phase; bias final circles to the centre; no final location with a structural advantage; no zone traps (long corridors, dead ends).
- **Scale:** ~4×4 to 8×8 km for 100 players, ~1 km² for 30-player mobile maps. [convention] Vendor guides; moderate confidence.
- **Callouts** matter most here: distinct silhouette and colour per POI.

## 8. Extraction / PvPvE (Arc Raiders, Hunt, Tarkov)

Source: Embark, "Refining Risk and Reward" (Arc Raiders blog), the best primary source; Hunt from Crytek dev diaries.
- **Advertise hotspots and match their threat.** "The clearest way we communicate risk is through the map screen": areas with greater ARC threat and high loot. Players "naturally gravitate toward these hotspots", which "drew in more traffic… and generated more player collisions." Embark fixed "high-risk areas which had great loot without a matching ARC presence" by adjusting spawns. Reward and AI threat rise together.
- **Make free extracts loud.** Main extractions "have no direct cost to use, but they draw a lot of attention." Cheap exits cost attention; quiet exits cost something else (a key, a fee, a detour).
- **Extracts dwindle.** "The longer you stay in a session, the number of available extractions steadily diminishes." This forces late-raid convergence, like a battle-royale circle.
- **Cheap, safe exits drain tension.** Keyed hatches were "quiet, quick", and "high-level players used hatches a whopping 40% of the time… far more often than intended… We want heart rates to go up when trying to extract." Price safe exits so they stay occasional.
- **Keyed rooms must pay back** the key's rarity: Embark flagged "locked rooms that didn't provide enough value for the rarity of their keys."
- **Embellish emergent hotspots.** "Rather than trying to remove those points of interest, we're working on applying additional level design to enhance and embellish them." Heatmap spawns, deaths, loot actions, AI spawns and deaths, PvP and PvE damage, extraction starts, successes and failures.
- **Compounds and reactive worlds (Hunt).** Players infiltrate compounds in a sandbox; "opening a gate can cause nearby ravens to take flight", so the world reveals approach; "How you deal with that challenge will reveal or hide your position" (Larbrant). Give each compound several entries and noise-making features on approaches.
- **Map anatomy.** [convention] Perimeter spawns → low-value scatter → mid-value POIs → advertised hotspots with matching threat; assign extracts so spawn-to-extract routes cross contested space. Tarkov's extract variety (always-open, conditional, faction-only, limited-use) comes from player guides [convention].

## 9. Fighting stages and arena sports (Smash, Rocket League)

In mastery-driven competitive games, the stage is part of the muscle memory; variety competes with predictability.
- **Standardise the ranked set.** Psyonix dropped non-standard arenas from competitive Rocket League: "standardization is important and necessary to provide a level playing field and foster consistent competition", and the alternate layouts "simply didn't add enough strategically to offset the corresponding loss in predictability and muscle memory" (PC Gamer). Put layout variety in casual or rotating modes; keep ranked geometry fixed.
- **Rocket League field** (Psyonix_Adam): goal line to goal line 10,248 uu, sideline to sideline 7,680 uu, floor to ceiling 2,048 uu; the ball is ~182 uu tall. Community constants (RLGym: side wall ±4,096, back wall ±5,120) measure a different plane; quote Psyonix's figures for field size.
- **Smash starters and striking** (SmashWiki). Starter stages are "neutral stages, or stages that can be chosen in the first game of a match", in contrast to counterpicks for later games. Players strike alternately, 1-2-1 on a five-stage list; "Any stage can be striked, even starter stages"; "most tournaments ban a majority of stages due to being extremely unbalanced in some way." Design implication: ship a small neutral set (simple, symmetric, no or toggleable hazards) [convention] and let the rest be counterpicks.
- **2D fighting stages.** [convention] Width decides how often fights reach the corner, and walls/corners are a mechanic (corner pressure); background animation must never read as a hitbox or projectile; stage choice should not change frame data.
- **Arena sports generally.** [convention] Symmetric, fixed dimensions; goals and boost/pickup positions mirrored; walls and ceilings either fully playable or clearly not.

## 10. Racing (pointer)

Track design (race line, clipping points, width, camber, height variation, kart route choice) moved to `genre-racing.md`. Multiplayer concerns there: passing zones, field size vs width, item and catch-up layers.

## 11. Review checklist

- [ ] Lane count and purpose: each lane has a distinct range/role; power positions paired
- [ ] Spawn safety: no LOS from enemy spawns/power positions; multiple exits and clusters
- [ ] Timings measured (spawn→choke, spawn→objective, rotations) and recorded per side
- [ ] Every choke/objective has 2–3 approaches incl. a flank; no single spot covers all chokes
- [ ] Height: ≤3 floor planes per area; every high spot countered (paired position, flank up, exposure); section drawn; height budget fits the input device
- [ ] Item/health placement rewards risk; every area has a callout-able landmark (floors named)
- [ ] Symmetry model chosen deliberately; asymmetry has a balancing lever
- [ ] Sightlines match weapon ranges; long angles have counterplay
- [ ] Size matches player count (time-to-first-contact target stated)
- [ ] Extraction: hotspots advertised with matching threat; free extracts loud; extracts dwindle; no cheap safe exit dominates; keyed rooms pay back
- [ ] Fighting/arena sport: ranked set standardised; neutral starters vs counterpicks defined; hazards toggleable or absent in the neutral set
- [ ] Telemetry plan: side win rate, heatmaps, death maps, route and extract usage

## 12. Maps to study

- **Arena:** Q3DM6, Q3DM17 (vertical flow and its sniper counter), UT DM-Deck16, CTF-Face, Halo Lockout, Blood Gulch, The Pit.
- **Tactical:** de_dust2, de_inferno, de_mirage, de_nuke; Valorant Ascent, Bind, Haven; Siege Clubhouse, Bank, Oregon.
- **Objective:** Overwatch King's Row, Eichenwalde (Paris as counterexample); TF2 Badwater Basin, Gravel Pit, 2Fort (stalemate example); CoD Nuketown, Highrise, Terminal, Raid; Battlefield Caspian Border, Operation Métro.
- **MOBA:** Summoner's Rift. **BR:** Erangel, Kings Canyon (pre/post rework), World's Edge.
- **Extraction:** Arc Raiders maps (hotspots, hatches); Hunt: Showdown compounds (Lawson Delta); [convention] Tarkov's Customs and Reserve extracts.
- **Fighting / sport:** Smash Battlefield and Final Destination (starter archetypes); Rocket League's standard arena (DFH Stadium) vs. retired non-standard arenas.

Key sources (full list in `SOURCES.md`): Xbox Wire (Treyarch); Riot dev blogs; TLDB (Verticality, typology); Shacknews (Fukada); Embark (Arc Raiders risk and reward); Crytek and PC Gamer (Hunt dev diaries); PC Gamer (Rocket League standardisation); DevTrackers (Psyonix field size); SmashWiki (starters, striking); PC Gamer (Siege); VGC (Kings Canyon).
