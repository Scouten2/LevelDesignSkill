# Accessibility at Level Scope

## Contents
1. What the level designer owns
2. Information channels: colour, sound, second channel
3. Teaching, practice and timing
4. Difficulty, checkpoints and progress
5. Assist hooks the level authors
6. Camera, motion and field of view
7. Photosensitivity
8. Reference implementations
9. Process: plan early, test with disabled players
10. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Guideline wordings below are quoted from the Game Accessibility Guidelines (GAG full list), the Xbox Accessibility Guidelines (XAG, current text), WCAG 2.3.1 and AbleGamers' Accessible Player Experiences (APX).

---

## 1. What the level designer owns

Menus and remapping belong to UI and systems; the level owns the **data that assists use** and the **spaces that decide who can finish**. Most level-scope accessibility is authored per space: nav goals, ledge volumes, skip states, cue emitters, checkpoint spacing, flash content. "Accessibility is orthogonal to difficulty": a very easy option removes barriers for some players while others still want permadeath, and "challenge and accessibility can coexist" (Gallant, Naughty Dog, 2021). So don't answer an accessibility problem only by lowering difficulty, and don't refuse an assist because the level is meant to be hard.

GAG tiers: **Basic** = "easy to implement, wide reaching"; **Intermediate** = "require some planning and effort but often just good general game design"; **Advanced** = "complex adaptations for profound impairments and specific niche mechanics." Treat Basic items as defaults for every level.

## 2. Information channels: colour, sound, second channel

- "Ensure no essential information is conveyed by a **fixed** colour alone" (GAG Vision, Basic). If colour reliance is unavoidable, let players assign their own colours (XAG 103). Encode paths, hazards and interactables by value contrast and shape as well as hue; check greyscale and colour-blind captures.
- "Ensure no essential information is conveyed by sounds alone" (GAG Hearing, Basic).
- **Second channel:** "Any visual content that's critical to understanding gameplay or comprehending the narrative should be expressed by using at least one other sensory method" (XAG 103; APX "Second Channel", whose example is audio-only gunfire given an increasing haptic buzz). For each critical cue in the decision-point table, list a second channel: spatialised sound at the goal, a haptic pulse at a ledge, a light change with a sound.
- "Give a clear indication that interactive elements are interactive" (GAG, Intermediate); APX "Distinguish This From That": interactables must not look like dressing.
- "Avoid placing essential temporary information outside the player's eye-line" (GAG Vision, Intermediate). Keep critical information within normal camera pitch (`verticality.md`).
- "Indicate / allow reminder of current objectives during gameplay" (GAG Cognitive, Intermediate). Halo 3's playtests produced exactly this fix: new objectives flash on screen (NPR, 2007).
- Advanced aids that need level data: "Provide a pingable sonar-style audio map", "Provide a voiced GPS" (GAG Vision, Advanced). TLOU II's Enhanced Listen Mode scans 10–30 m and changes pitch with the target's height relative to the player, so vertical layouts need height-correct emitter positions.

## 3. Teaching, practice and timing

- "Include **interactive** tutorials" (GAG Cognitive, Basic): teach in the space, by doing (`principles.md`).
- "Include a means of practicing without failure, such as a practice level or sandbox mode" (GAG Cognitive, Intermediate); APX "Training Ground". At level scope: the intro beat of every mechanic has no fail state, matching Hodent's "DON'T PUNISH WHILE TEACHING."
- "Do not make precise timing essential to gameplay – offer alternatives, actions that can be carried out while paused, or a skip mechanism" (GAG Motor, Advanced). Mark every critical-path timing window in the beat chart and give each one an alternative, an assist or a skip.
- "Avoid repeated inputs (button-mashing/quick time events)" and avoid or offer alternatives to held buttons (GAG Motor, Intermediate). No mandatory mash-to-open doors.
- "Avoid any sudden unexpected movement or events" (GAG Cognitive, Advanced). Horror depends on surprise; offer a warning option or a reduced-scare setting rather than dropping the genre (`genre-horror.md`).
- "Offer a means to bypass gameplay elements that aren't part of the core mechanic" (GAG General, Intermediate); APX "Bypass".

## 4. Difficulty, checkpoints and progress

XAG 108's current text asks games to "Include multiple levels of difficulty presets (ideally four or more…)", let players "change difficulty at any time without losing game progress", adjust "different mechanics… (like Puzzle Difficulty and Combat Difficulty) or through a set of assists", "Provide an ultra-low difficulty mode", and "regularly save game progress… so that players can continue after failure without significant loss of progress." Avoid labels that denigrate the player ("Wimp Mode"). GAG adds "Allow difficulty level to be altered during gameplay, either through settings or adaptive difficulty" (Intermediate) and "Provide an autosave feature" (Intermediate).

Level-scope consequences:
- **Checkpoint spacing is how a level delivers "no significant loss of progress."** Use the beat chart's Replay cost and Checkpoint columns and `beat_lint.py`'s budget (P(death) × replay ≤ 10 s [convention]). APX "Save Early, Save Often".
- **Separable challenge:** keep puzzle and combat in separable beats where possible so a player can lower one without the other.
- **Every preset is playable:** at G3, play or simulate the level at the lowest and highest presets; spawn budgets and timers scale, geometry doesn't break.
- **Assist offers after repeated failure:** *Super Mario 3D Land* shows an assist block after 5 deaths and *New Super Mario Bros. Wii* offers Super Guide after 8 (Hayashida interview, 2012). Author where the offer appears.

## 5. Assist hooks the level authors

Put this table in the brief and the one-pager; reference hook ids in the beat chart's Assist hooks column.

| Hook | What the level designer authors | Upkeep / test | Pattern |
|---|---|---|---|
| Nav-assist goal points | A goal point per critical-path step and per arena phase; safe goals in boss fights | Re-check after every layout change; TLOU II patched "goal positions in Navigation Assistance across the entire game" | TLOU II nav assist |
| Ledge guard volumes | Volumes on every fatal edge that **prevent** the fall (plus audio/vibration warning), not just warn | Walk every edge with assists on; intended drops excluded | TLOU II Ledge Guard |
| Traversal-assist tags | Tags on "certain difficult jumps", climbs and squeezes that an assist can auto-perform | Each tagged jump completes with the assist | TLOU II traversal assist |
| Puzzle skip state | A completed state for every puzzle that leaves the level consistent (doors open, items granted) | Skip each puzzle, then finish the level | TLOU II Skip Puzzle; APX Bypass |
| High-contrast class tags | Material/ID tags for allies, enemies, items, interactables | High-contrast capture of each space | TLOU II high contrast display |
| Second-channel emitters | Sound or haptic emitter for each critical visual cue | Play muted, then blind-folded on key beats | XAG 103; APX Second Channel |
| Practice space | A no-fail space at each new mechanic | No death or damage possible there | GAG; APX Training Ground |
| Checkpoints and saves | Checkpoint before every high-death beat; autosave triggers | `beat_lint.py` replay budget | XAG 108; APX Save Early, Save Often |
| Assist offer trigger | Where help is offered after N deaths | Trigger fires at the right beat | 3D Land (5), NSMB Wii (8) |
| Speed tolerance | Scripted timers and moving hazards still work at reduced game speed | Run key beats at the lowest speed setting | APX Slow It Down; Celeste |
| Death-free completion | No progress that requires dying (e.g. a pit you escape only by respawning) | Complete with invincibility on | Celeste Assist Mode |

## 6. Camera, motion and field of view

- XAG 117: "Avoid the use of camera shake, camera bobbing effects, motion blur, mouse blur, and more or provide an option to turn off these behaviors" and "Provide adjustable field of view settings."
- Narrow, low, twisting first-person corridors at a low FOV are a classic sickness trigger [convention]; widen them or keep camera motion calm there. Check tight spaces at the default FOV and at the widest option (wide FOV exposes unfinished geometry).
- No forced camera roll, rapid forced rotation or long forced shake in mandatory beats [convention]. VR comfort rules: `genre-vr.md`.
- Optional guidance intensity: players modded yellow paint out of games with no toggle; offer opt-in guidance aids with landmark redundancy underneath (`principles.md`).

## 7. Photosensitivity

Prevalence of photosensitive epilepsy is about 1 in 4,000, and "eliminating game content that can potentially cause photosensitive seizures is preferred over splash-screen warnings" (XAG 118).

| Test | Threshold |
|---|---|
| What counts as a flash | A pair of opposing luminance changes of **10% or more**, darker value below 0.8 relative luminance (XAG 118; WCAG "general flash") |
| Frequency | Fail above about **3 flashes in any one second** (WCAG: "more than three times in any one second period") |
| Area | About **20% or more of the screen** (XAG 118) or **25% of any 10° visual field** (WCAG; ≈ 341×256 px at 1024×768) |
| Red | Stricter test when either extreme is saturated red, R/(R+G+B) ≥ 0.8 |
| Patterns | High-contrast alternating bands or grids (contrast difference > 10%) over about 20% of the screen fail |
| Duration | Lower-intensity flashing can still fail if it continues for an extended period (XAG 118) |

Level sources to audit: scripted lightning, strobing alarms, muzzle flashes in dark rooms, explosions, flickering lights, emergency beacons, fast light cuts, striped grates, fences and stair textures filling the view. Fix by slowing to ≤3 Hz, cutting luminance change below 10%, shrinking the flashing area, or removing saturated red. Verify with the Harding FPA test (an implementation of Ofcom's guidelines) or equivalent at G4. A mandatory flash above threshold is a rubric blocker (`review-rubric.md`).

## 8. Reference implementations

- **The Last of Us Part II** (Naughty Dog, 2020; more than 60 settings): navigation assistance "faces the camera in the direction of story progression"; traversal assistance performs "certain difficult jumps" and climbs; Ledge Guard "Prevents you from falling from ledges that will kill you"; SKIP PUZZLE advances "to the puzzle's completion"; high contrast display tints allies, enemies, items and interactives. Its patch notes show nav-assist goals are per-space level data that need upkeep.
- **Celeste** Assist Mode: "slowing the game speed, granting yourself invincibility or infinite stamina, and skipping chapters entirely." Invincibility makes the player "immune to almost everything, including falling into a pit," so the level must stay completable when deaths stop happening. Variant Mode game speed runs 50–160% in 10% steps (fan wiki); Assist Mode's own range is [unverified].
- **AbleGamers APX:** 21 patterns, 11 access and 10 challenge. Challenge patterns that map to level hooks: Bypass, Training Ground, Slow It Down, Save Early Save Often, Helping Hand, Undo Redo, Moderation In All Things. Access patterns: Second Channel, Clear Channels, Distinguish This From That.

## 9. Process: plan early, test with disabled players

- Naughty Dog had first prototypes of nav assist, high contrast and enhanced listen by the end of 2017, ran accessibility-focused tests from summer 2018, and called planning "so early in development" "absolutely critical" (Can I Play That?, 2020). Put the hook table in the G0 brief, not after content lock.
- "Include some people with impairments amongst play-testing participants" (GAG General, Intermediate). Add hypothesis cards for assist hooks ("players with nav assist on reach the vista in ≤ 90 s" [convention]).
- Gates: hooks planned at G0, authored at G3 ("Content Complete"), photosensitivity and post-art contrast verified at G4 (`process.md` §8).

## 10. Review checklist

- [ ] No essential information by a fixed colour alone or by sound alone; greyscale and colour-blind captures checked
- [ ] Every critical visual cue has at least one other sensory channel (XAG 103 / APX Second Channel)
- [ ] Interactables clearly interactive and distinct from dressing; critical info within the eye-line
- [ ] Objective reminder available
- [ ] Interactive teaching; a no-fail practice space at each new mechanic
- [ ] No mandatory precise timing without alternative, assist or skip; no mandatory mash or hold
- [ ] Assist hooks authored per space: nav goals, ledge-guard volumes that prevent fatal falls, traversal tags, puzzle skip states, high-contrast tags
- [ ] Level completable with invincibility, infinite stamina and slowed speed; no progress requires dying
- [ ] Checkpoint spacing keeps loss of progress small (replay budget met); difficulty changeable without losing progress
- [ ] Camera shake, bob and blur avoidable; FOV adjustable; tight spaces checked at default and widest FOV
- [ ] Flashing ≤ 3/s or below the 10% / ~20% area thresholds; no saturated-red flashes; no large high-contrast stripes; Harding or equivalent run at G4
- [ ] Players with impairments in at least one playtest round
