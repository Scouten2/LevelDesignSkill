# Stealth & Immersive Sim Spaces

## Contents
1. Universal rules (stealth and immersive sim)
2. Visibility: light, shadow and feedback
3. Guards and patrols
4. Detection, failure and recovery
5. Observation, sightlines and sound
6. Vertical route layers (roofs, vents, sewers)
7. Social-stealth sandboxes (Hitman): spirals, Swiss cheese, guidance
8. Immersive sim multi-path design (Deus Ex, Dishonored, Prey)
9. Legible complex spaces: the Clockwork Mansion rules
10. Writing the route spec
11. Common failures → fixes
12. Review checklist
13. Levels to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Core refs: affordances and the guidance rule in `principles.md`; loops and gating in `layout-and-flow.md`; height, drops and the hidden-but-fair rule in `verticality.md`; crouch/crawl/vent sizes in `metrics.md`; route heatmaps in `playtesting-and-critique.md`. Loud/stealth hybrid combat: `genre-action-combat.md`.

---

## 1. Universal rules

- **Stealth is a puzzle made of predictable parts.** Good stealth rests on predictable rather than smart enemies, and shadow that hides reliably (Kayin on Thief). Unpredictable guards turn planning into trial and error.
- **An "open building", not an open world.** Immersive sims work best as dense, limited spaces with many routes, stealth and combat viable everywhere (CBR on Arkane). Density of options beats square metres.
- **Guide and attract, don't dictate.** Arkane (Colantonio & Smith, GDC 2013): "guiding and attracting, as opposed to dictating" the player's path.
- **Readable states.** The player can always answer: am I visible, am I heard, does this guard know about me? Each answer needs a cue (light, meter, bark, music). [convention: barks on every AI state change]
- **Failure is a new situation, not a reload** (§4).
- **Prove it in grey.** Patrol timing, light pools and route choice are testable in blockout; if the level is only tense once lit and dressed, the layout is not done (`process.md`, gameplay-first checks).

## 2. Visibility: light, shadow and feedback

- **Show visibility explicitly.** Thief's light gem was added because players couldn't tell how hidden they were; it works alongside audio cues. Give a continuous visibility read, not a detected/undetected flag.
- **Light pools are the level's grammar.** Lay out light and shadow first, then geometry detail. Light the critical path before mood (TLDB lighting order: global → wayfinding → gameplay → mood). [convention] High-contrast pools and a consistent set of hideable surfaces.
- **Balance the darkness.** Too bright removes hiding; too dark and guards never find anyone (Thievery UT lighting guide). Every crossing gets at least one shadow route and one lit risk.
- **Lights are tools and lures.** Thief players douse lights, which can alert a guard; players exploit this to lure guards, and guards concentrate on lit areas. Each light is a player tool, an AI magnet and a risk.

## 3. Guards and patrols

- **Every guard is there for a reason**: inspecting an important area or guarding an entrance (Thief 2014 Q&A). If you can't say what a guard protects, cut or move it.
- **Patrol shapes.** [convention]
  - Loops or ping-pongs with readable timing and pauses at points of interest.
  - Gaps long enough to cross the lit area they cover, measured at crouch speed (`metrics.md`).
  - Stationary guards at entrances and assets; patrols on connecting routes.
  - Overlapping patrols only where you want a hard crossing, stated in the spec.
- **Escalation phases.** [convention] Caution → evasion → alert with reinforcements gives the space a second job: where reinforcements come from and where contact can be broken.
- **AI senses define the space.** Vision cones, hearing radius and search behaviour set cover heights, corridor widths and loop sizes. Fix them early. [convention]

## 4. Detection, failure and recovery

- **Failure → chase → search → de-escalation.** Guards give up after a while, so mistakes become a chase (Thief 2014 Q&A). Layout needs: hiding spots guards are less likely to search; loops around blocks, rooms and floors to break line of sight [convention]; no dead-end hiding traps on the main route [convention].
- **Survivable alarms.** [convention] An alarm leads to fight or flee, never a forced reload; the loud path is never the only one that works.
- **Checkpoint philosophy.** IOI aimed for huge, checkpoint-free sandboxes; recovery comes from space and AI. Even if your game saves often, design spaces that recover gracefully. Keep failure attributable: the player should see why they were spotted (`fun-checks.md`).

## 5. Observation, sightlines and sound

- **Scout before commit.** Give each area an observation point from which patrols can be read before entry. Prospect–refuge is **[contested]**: TLDB cites a meta-analysis supporting prospect but not refuge and recommends sightlines/vistas and cover/enclosure/safe house instead. Use those terms and test what players actually do. [convention: balconies, rafters, vents, windows as observation points]
- **Sound surfaces.** [convention] Thief-style material noise (metal and tile loud, carpet and grass quiet) turns floors into routing information. A quiet route must look quiet.
- **Audio as feedback.** AI barks reveal state and position; let players hear guards before seeing them at blind corners. [convention]

## 6. Vertical route layers (roofs, vents, sewers)

Height is the stealth genre's second map. See `verticality.md` for the eight functions; here the key ones are survey, hidden routes and position.
- **The second layer overlooks the first.** [convention] Vents, crawlspaces, rafters and pipes (Splinter Cell, MGS); rooftops above and sewers below the street (immersive sims). A route above the guards doubles as an observation point; a route below is blind and should surface at a safe peek point.
- **High places read as safe.** [unverified] Thief is often said to teach early that high places are safe. If your game does, keep it true or break it once, on purpose (rooftop patrols, snipers).
- **Vertical powers shape the level.** Dishonored's Blink reportedly became core near alpha partly because the environments were built "open, sandboxy and vertical" [unverified: interview snippet]. If the kit includes a vertical move, every district needs places it matters; if not, don't build roofs the player can see but never use.
- **Hidden-but-fair vertical routes.** A roof drop, window or vent the player is meant to find must pass the four-part rule (`verticality.md`): grammar taught safely; visible from another vantage; an edge invitation (light, item, overheard line); cheap to try. Critical routes may not rely on being noticed by chance.
- **Detection across height.** Test vision cones over and under enemies, not only past them; some games detect too readily across vertical distance (BG3; `genre-rpg-narrative.md`).
- **Floor planes.** Most areas max out at three (TLDB). More layers make patrols impossible to model mentally.

## 7. Social-stealth sandboxes (Hitman)

- **Big sandbox + layered guidance.** "Level Design in HITMAN: Guiding Players in a Non-Linear Sandbox" (Mikkelsen & Poedenphant Andersen, GDC Europe 2016): late user research found the learning curve too steep and Paris too big to understand. IOI kept the sandbox and added a tutorial plus "a linear guidance system that's capable of supporting (without overshadowing) the open-ended sandbox" (opportunities). When a sandbox overwhelms, add opt-in guidance before shrinking it.
- **Snail-house spirals.** Lead level designer Torbjørn Christensen: Sapienza and Hokkaido are "basically spirals, or a snail house", which players can walk every inch of without hitting a wall (Game Developer, 2017). They "wrap around themselves, with their layers interconnected with slopes and stairways", and "feel bigger than they really are" (80.lv summary of an RPS interview). Apply it: wind the route around a central target so every layer connects back to the others by ramps and stairs, and no street ends in a wall.
- **Swiss-cheese connectivity.** Creative director Christian Elverdam: "we built a volume filled with connections, and these connections mean that you will never get lost… You don't have to backtrack necessarily" (PC Gamer, Sapienza). He contrasts a palace (floors, basement, attic: easy to model mentally) with a coastal town, where "it's much harder to guess where the level starts and stops." Pick a building type players can model, or add structure (spirals, landmarks) when you can't.
- **Living, believable spaces.** NPC routines are the content; give them believable reasons to move (work, errands, conversations).
- **Onion layout.** [convention] Public outside, staff and restricted zones inside, the target's private space at the core. Each ring needs a disguise or trespass; several crossings per ring let replays reveal new routes.
- **Opportunities as mini-stories.** [convention] Overheard conversations trigger chains ending in a target-exposure moment. Put the overhearing spot on a natural route.
- **Restricted zones read as restricted.** [convention] Signage, guards, lighting and architecture change, so trespass is always a choice.

## 8. Immersive sim multi-path design

- **Multiple solutions per task.** Spector's Deus Ex rules include "Multiple solutions"; Human Revolution's level design is "Multi-Path, Multi-Solution".
- **Three ways in.** [convention] At every gate: one combat, one stealth/traversal, one systemic or social route (hack, vent, keycode in a note, dialogue). Folk wisdom, not an official rule.
- **Holistic consistency and self-evidence.** Steve Lee (Arkane, GDC 2017, "An Approach to Holistic Level Design"): design gameplay, presentation and story together, valuing consistency, self-evidence, affordances and intentionality (every element has a believable reason to be there). A climbable pipe is climbable everywhere; a vent that looks enterable is enterable.
- **Redesign around exploits.** When Dishonored testers exploited powers, the designers redesigned levels to accommodate them; every mission can be completed non-lethally. Ask whether an exploit is a route to support before closing it. (Puzzle games differ: Valve keeps an unintended solution if it "makes the tester feel smart" and removes it if it makes the game feel broken; `puzzle-verification.md`.)
- **Abilities multiply routes.** Test against each power set (Corvo, Emily) and the no-power run.
- **Player-authored paths.** Prey's GLOO Gun lets players build their own routes; assume they reach any ledge within GLOO range. [unverified] Colantonio called Talos I "very vertical and very crafted", a place where "you come back and the context has changed."
- **Scope honestly.** Deus Ex cut a mid-game White House level as too complex. Cut a whole level before thinning every level.
- **Typical patterns.** [convention] Rooftop and sewer layers; vents as the crawler route; keycodes in readable notes; hub plus mission districts with a safe house (Hound Pits). Stealth routes must not skip narrative beats.

## 9. Legible complex spaces: the Clockwork Mansion rules

Source: Game Developer deep dive (Carrier, 2017) on Dishonored 2's Clockwork Mansion (level designer Dana Nightingale, level architect David Di Giacomo). Switches reconfigure rooms; players fight through the shifting rooms, sneak through the gears behind the walls, or mix both. The rules generalise to any transforming, layered or hidden-route level:
1. **Players must be able to "construct a mental picture of the house."** Keep the overall massing simple enough to model.
2. **"Avoid long and tight passages that go in and around the walls."** Backstage routes are short hops, not mazes.
3. **"Every backstage area had to be… visually connected to the big areas of the building."** From inside the walls, the player keeps seeing the main rooms (gaps, grilles, windows), so the hidden layer stays oriented.
4. **Rooms have real-world functions**, so "attentive players could understand the house and even play without markers on a second playthrough." Function names double as landmarks.
5. **AI locomotion must work while rooms move.** Test nav in every configuration.
6. **State is readable.** [convention] Show the current configuration from the switch and from the room it changes.

## 10. Writing the route spec

One row per gate or objective. [convention]

| Gate | Combat route | Stealth / traversal route | Systemic / social route | Observation point | Fail-state recovery |
|---|---|---|---|---|---|
| Courtyard → manor | Front door, 4 guards, alarm bell | Rooftop (F2) → balcony drop ↓, 1 lit gap | Servant disguise via kitchen; keycode in gardener's note | Clock tower | Loop through hedges; cellar hide spot |

Every route is signposted with ≥2 independent cues; no route is strictly better for every playstyle. Annotate floor indices and vertical edges as in `verticality.md`.

## 11. Common failures → fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Trial-and-error reloads | Unpredictable guards; no observation point; unclear visibility | Readable loops with pauses; add a vantage; continuous visibility meter |
| Players always go loud | Stealth routes unreadable or gaps too short | Signpost the second layer; widen gaps; add shadow routes |
| One route dominates | Strictly better risk/reward; others poorly signposted | Rebalance rewards; add cues to neglected routes (heatmaps) |
| Big sandbox overwhelms | Too much to read at once (Hitman Paris) | Opt-in guidance layer before shrinking; spiral structure; buildings players can model |
| Lost inside the walls | Backstage routes long and blind | Clockwork rules: short hops, visual connection to main rooms |
| Roof route never found | Untaught or invisible vertical route | Hidden-but-fair rule: teach the move, show it from a vantage, invite the look |
| Exploit skips the level | Tool not anticipated | Support it as a route or close it consistently, never invisibly |
| Lights feel decorative | No AI response to light changes | Make lights tools and lures; guards investigate changes |

## 12. Review checklist

- [ ] Every guard has a stated reason; patrol timings measured; gaps crossable at crouch speed
- [ ] Visibility read is continuous (meter + audio); AI state changes barked
- [ ] Each crossing has a shadow route and a lit risk; lights work as tools and lures
- [ ] Observation point before each major area; second layer overlooks the first
- [ ] Section drawn for multi-floor areas; ≤3 floor planes; vertical routes annotated (↓ ↑ ⇅)
- [ ] Hidden vertical routes pass the four-part hidden-but-fair rule; critical routes don't rely on chance discovery
- [ ] Vision tested over and under enemies, not only past them
- [ ] Floor materials encode noise consistently and look like they sound
- [ ] Detection → chase → search → de-escalation; loops and hide spots; no forced reload
- [ ] Each gate has ≥3 routes, all signposted with ≥2 cues
- [ ] Sandbox: spiral or Swiss-cheese connectivity, no street ends in a wall; opt-in guidance layer
- [ ] Transforming or backstage spaces: mental picture possible; backstage short and visually connected; rooms have functions; AI nav works in every state
- [ ] Tested with every power set including none; exploits supported or deliberately closed
- [ ] Non-lethal completion possible if promised; stealth routes don't skip story beats
- [ ] Restricted zones read as restricted

## Levels to study

- **Stealth:** Thief and Thief 2 mansion levels; Hitman (2016) Paris (the too-big-at-first lesson); Hitman Sapienza and Hokkaido (snail-house spirals).
- **Immersive sim:** Dishonored 2 Clockwork Mansion; [convention] Deus Ex Liberty Island; Prey's Talos I.
- **Hybrid:** TLOU / Uncharted 4 stealth-to-combat encounters (`genre-action-combat.md`).

Key sources (full list in `SOURCES.md`): Game Developer (Hitman GDC Europe 2016 video; "the secret to expansive level design is spirals" 2017; Clockwork Mansion deep dive 2017; Steve Lee GDC 2017); PC Gamer (making of Sapienza; Arkane GDC 2013); 80.lv (snail structure); Thief developer Q&A and analyses; TLDB (prospect–refuge, lighting, verticality).
