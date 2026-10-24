# Horror & Survival Horror

## Contents
1. Universal rules (the horror loop)
2. Pacing dread: anticipation, scare, release
3. Descent as dread: the vertical meaning of fear
4. Hub structure and backtracking as mastery (Resident Evil)
5. Key/lock economy and resource scarcity
6. Safe rooms and rest beats
7. Stalkers and unkillable threats (Mr. X, the Alien)
8. No-combat horror (Amnesia)
9. Darkness, fog and sound
10. Other references (Dead Space, Silent Hill, P.T.)
11. Common failures → fixes
12. Review checklist
13. Levels to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Core refs: tension/release and beat charts in `principles.md` and `process.md`; hubs and lock-and-key in `layout-and-flow.md` and `genre-dungeon-metroidvania.md`; height and drops in `verticality.md`; sizes in `metrics.md` (stalker AI needs its own nav metrics); photosensitivity and other assist hooks in `accessibility.md`.

---

## 1. Universal rules

- **Cut anything that doesn't serve the horror.** Frictional removed combat from Amnesia partly because they weren't good at it, and cut anything that didn't serve horror (Grip). Audit every mechanic and space: does this make the player more afraid or more vulnerable?
- **Familiarity is the resource you spend.** Players master a space, then the game breaks that safety (a pursuer, a state change, a new route). Horror level design is managing when the player feels in control and when that control is taken away.
- **Sound is the main channel of dread.** Critics single out Dead Space 2's sound; RE2's Mr. X is announced by footsteps; Amnesia's visions use sound only. Draw the audio map alongside the layout.
- **Don't reveal where enemies wait.** Dead Space doesn't telegraph enemy positions (critic analysis). Uncertainty about *where* matters more than *what*.
- **Step back from the player.** Alien: Isolation's team "step[ped] back from the player as often as possible" (Hope). Minimise scripting so systemic threats feel unpredictable.
- **Gameplay first, with the horror exception.** Prove routes, sightlines, hiding and pursuit loops in grey. Dread itself depends on light and sound, so it is one of the cases where grey can't answer everything (`process.md`): say so, and test a cheap representative slice with real lighting and audio early, rather than waiting for the art pass.

## 2. Pacing dread: anticipation, scare, release

- **Real quiet periods.** Critics found Dead Space 2 often lacks quiet breaks, leaving players drained; calm sections are often the most unsettling. Horror rest beats are low-action, high-anticipation, not "intensity 1".
- **Anticipation over scare.** [convention] Build tension with ambience, lighting and false alarms; ration jump scares and place them after long quiet stretches.
- **Learned safety, then broken.** [convention] RE1's dog-through-the-window corridor: a corridor walked safely becomes the scare. Plan scares on spaces the player already trusts.
- **Change of movement as pacing.** Dead Space 2 varies movement (vents, sprinting, creeping) for pacing (critic analysis). [convention] Zero-G and vacuum sections act as pacing shifts.
- **Companions dilute fear.** Co-op chatter undermines suspense (critic view of Dead Space 3). Plan stretches without companions.
- **Suggested beat shape.** [convention] build (sound, environmental storytelling) → false alarm → longer build → threat → escape/fight → safe-room release. Vary it so the rhythm stays unpredictable.

## 3. Descent as dread: the vertical meaning of fear

Height carries emotion: up reads as effort, hope and progress; down as dread, isolation and distance from safety (`verticality.md` §2, "meaning"). Most of this section is design inference **[convention]**; the supporting observations are noted.
- **Going down is cheap; coming back is not.** "With gravity, it is easier to drop down than to climb up. Downward flow is heavier than upward flow" (TLDB). A one-way drop into the depths commits the player and cuts the retreat: use it at the threshold of the scariest stretch, and make the return a climb.
- **Distance from safety is vertical.** Of Dark Souls: "the further you plunge, the further from the safety of the central hub you get - if you aren't prepared, you have to make the climb back up" (TheGamer, opinion). Subnautica pushes the player downward and ties depth to darkness and fear (critic analyses; `genre-open-world.md` §8).
- **The deepest point is the most dangerous.** Put the stalker's lair, the hardest encounter or the worst revelation at the bottom; let the floor index on the section drawing match the intensity curve.
- **Compress as you descend.** [unverified: one article, snippet only] Basements read as isolated territory with low ceilings and poor light, and climbing back up reads as relief. Lower ceilings, narrower stairs, fewer light sources and longer reverb per level down.
- **Ascent is the release.** End a descent with a climb toward light: a stair to the surface, a lift to the hub, a window at the top. The climb-out is a rest beat and an orientation moment.
- **Show the way down before it's needed.** A shaft, a stairwell or a grate glimpsed early plants the dread; going down it later pays it off ("see it, then reach it").
- **Keep falls legible.** Dread comes from what is down there, not from guessing which drop kills. Classify every drop free / committed / costly / lethal (`verticality.md`).

## 4. Hub structure and backtracking as mastery (Resident Evil)

- **A compact, interconnected hub.** RE2's Raccoon Police Station is praised for puzzles woven into the architecture and "intricate hub-based level design"; players "learn the RPD as well as you know your neighborhood". The station–sewer loop is compared to returning to a familiar Dark Souls area: return builds mastery.
- **Camera shapes backtracking cost.** The remake's over-the-shoulder camera makes backtracking less cumbersome than fixed angles did. Budget backtracking distance to camera and movement speed.
- **Get to the hub quickly.** The remake shortened the path to the station.
- **Loops and locked shortcuts** let mastery replace fear until a pursuer or a state change resets the threat (§7). [convention] Non-respawning enemies on chokepoint corridors turn route planning into resource planning.
- **Stack the hub.** [convention] Basement, ground floor and upper floor (plus sewer below) give the hub a vertical spine; the lowest layer should be the most hostile (§3). Draw a section; keep ≤3 floor planes per area.

## 5. Key/lock economy and resource scarcity

- **Key/lock economy.** [convention] RE-style keys (spade, diamond, heart, club) each open doors across the hub, so one pickup re-opens several old areas. Show locked doors early. Graph dependencies before building and check them with `graph_check.py` (`genre-dungeon-metroidvania.md` §2).
- **Scarcity forces choices.** [convention] Limited inventory forces trade-offs; zombies can be dodged, killed or blocked (RE2 Remake's boarded windows), so every enemy is a resource decision.
  - A repeated heuristic is ammo for ~60–70% of enemies. [convention] Unsourced; tune in playtests.
- **Geometry must support avoidance.** [convention] Corridors wide enough to dodge a slow enemy at a cost; bypass routes; blockable doors and windows. If space only allows killing, scarcity becomes a soft-lock.
- **Multiple puzzle solutions.** Amnesia's puzzles have several solutions so the path always feels intuitive. A stuck player stops being afraid and starts being bored.

## 6. Safe rooms and rest beats

- **Safe rooms are release and refuge.** With Mr. X roaming, safe rooms feel "like cages you want to stay inside" (Unwinnable). The safe room/corridor contrast is the pacing engine.
- **Placement.** [convention] Item boxes and save rooms at hub junctions, so the safe room is also an orientation anchor. Each exit faces a decision, not a guaranteed ambush.
- **Make safety legible.** [convention] A consistent audio cue, light colour and prop set; never violate it (or once, as a major beat, knowing the cost).
- **Replay cost.** Save rooms bound what a death costs. Keep the replay after death short before high-tension beats (`fun-checks.md`).

## 7. Stalkers and unkillable threats

- **A stalker turns the familiar hub back into a threat.** Kadoi (RE2 Remake): the original Tyrant rarely broke through rooms outside scripted events; the remake's tracks the player between rooms. The hub needs loops a pursuer can chase you around, and connections the pursuer can use.
- **Telegraph with audio.** Mr. X's footsteps layer several recordings to sell his weight; hearing them means he's close, and they turn metallic when he shares your room (Unwinnable). Every stalker needs a distance cue readable without sight. Add a floor cue: footsteps above vs. on your level.
- **Multiple routes for player and creature.** Alien: Isolation needed several routes for both so the systems could interact; the alien is sense-driven, reacts to noise and can't be killed. Its size was a navigation challenge: check creature nav, and make player-only routes (vents, lockers) only where intended.
- **Hiding spots spread through the space.** [convention] Lockers, vents, under-desk spots, never far apart in stalker zones; the motion tracker trades information for noise.
- **Tune lethality.** GDC 2014 previews suggested the alien might be too smart. [unverified] Alien: Isolation reportedly uses a menace gauge that sends the alien back to the vents after sustained tension. Build a release valve into any persistent threat.
- **Stalker zones and rest zones.** [convention] Define where the stalker may go; keep safe rooms and some puzzle spaces off-limits, and say so in the spec.

## 8. No-combat horror (Amnesia)

- **Remove the fight, keep the threat.** Every encounter becomes avoidance: sightlines, hiding, doors, darkness and routes are the only tools. Every threat space needs an escape or hiding option.
- **Sanity and darkness as systems.** [convention] Amnesia ties fear to light and seeing monsters, so the player chooses between darkness (hidden, losing sanity) and light (visible, stable). Place light sources as scarce resources.
- **Sound-only visions** are cheap and let the imagination fill the gap.

## 9. Darkness, fog and sound

- **Limit view distance on purpose.** [convention] Silent Hill's fog (originally a hardware limit) makes every corridor a reveal; plan landmarks that read at short range (silhouette, sound, light).
- **Audio warnings.** [convention] Silent Hill's radio static is an in-world proximity meter. Give an imperfect early warning so dread starts before the threat.
- **Orientation in the dark.** Darkness must not mean lost: ≥2 independent cues per decision point, favouring light shafts, sound sources and silhouettes. [convention]
- **Flashes and strobes.** Lightning, muzzle flashes and flickering lights must stay within photosensitivity limits (`accessibility.md`).

## 10. Other references (Dead Space, Silent Hill, P.T.)

- **Dead Space.** [convention] Vents as monster entry points so the player stops trusting walls; diegetic UI keeps eyes in the world.
- **Silent Hill.** [convention] The otherworld re-skins and re-routes known spaces: familiarity spent twice.
- **P.T.** [convention] One looping corridor that changes on each pass: dread through small, cumulative deviations from a space known intimately.

## 11. Common failures → fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Drained, not scared | No quiet stretches (Dead Space 2 critique) | Low-action, high-anticipation beats; scares later |
| Fear fades after an hour | Hub fully mastered, nothing resets it | Pursuer or state change (lights out, re-route) on the known hub |
| Depths feel flat | Lowest areas no worse than the surface; easy way back | Deepest = most dangerous; one-way drop in, climb out; compress space per level |
| Stalker feels unfair | No distance cue; too few loops/hides; too lethal | Audio telegraph, evasion loops, hiding spots, menace release valve |
| Fight everything, then soft-lock | No avoidance geometry; ammo too generous early | Bypass routes, blockable doors; tune ammo so avoidance is optimal |
| Lost, then bored | Darkness hides guidance; one-solution puzzles | Short-range landmarks and sound beacons; multiple solutions |
| Safe room feels pointless | Inconsistent safety language; no threat outside | Fixed safety cue; dangerous corridor outside |

## 12. Review checklist

- [ ] Every mechanic and space serves fear or vulnerability; the rest is cut
- [ ] Routes, hiding and pursuit loops proven in grey; a lit, scored slice tested early for mood
- [ ] Beat chart has real quiet stretches; scares follow long builds; rhythm varies
- [ ] At least one "learned safety, then broken" moment on a trusted space
- [ ] Section drawn; net vertical direction matches the emotion; deepest point is the most dangerous; climb-out is a release
- [ ] Every drop classified (free / committed / costly / lethal); one-way drops into danger read as one-way
- [ ] Hub compact and looped; backtracking budgeted to camera and movement speed
- [ ] Key/lock graph drawn and checked; locked doors shown before keys; each key re-opens old areas
- [ ] Resources tuned so avoidance is viable; geometry supports dodging, bypassing, blocking
- [ ] Safe rooms at hub junctions with a consistent safety language; exits face decisions; replay cost short
- [ ] Stalker: audio distance cue (incl. which floor), evasion loops, nav at creature size, off-limits zones
- [ ] Hiding or escape in every threat space (mandatory without combat)
- [ ] Persistent threat has a release valve; playtest for exhaustion vs. dread
- [ ] Darkness never means lost: ≥2 cues per decision, readable at short range
- [ ] Audio map drawn with the layout; flashes within photosensitivity limits
- [ ] Companion chatter doesn't undercut key tension beats

## Levels to study

- **Survival horror hubs:** RE2 (1998 and Remake) Raccoon Police Station with Mr. X; [convention] RE1 Spencer Mansion.
- **Systemic stalker:** Alien: Isolation's Sevastopol.
- **No combat:** Amnesia: The Dark Descent.
- **Descent:** Dark Souls' plunge from Firelink to Blighttown and the climb back; Subnautica's depth bands.
- **Pacing (critic analysis):** Dead Space 2, as a counterexample for missing quiet breaks.
- **[convention]:** Silent Hill (fog, radio, otherworld); P.T. (the looping corridor).

Key sources (full list in `SOURCES.md`): Game Developer (Grip; "The Perfect Organism"; Amnesia sanity meter); PC Gamer (Kadoi on Mr. X); Unwinnable (safe rooms); TechRadar (Hope); TLDB (Verticality); TheGamer (Dark Souls interconnection); Dead Space critic reviews.
