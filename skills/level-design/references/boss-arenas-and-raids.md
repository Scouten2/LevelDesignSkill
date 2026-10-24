# Boss Arenas and Raids

## Contents
1. What a boss fight is for
2. The arena is readable on entry
3. Size the arena from boss reach and player dodge metrics
4. One telegraph language for the whole game
5. Phases re-teach the space
6. Geometry the mechanics use: pillars, cover, line of sight
7. Vertical arenas
8. Checkpoints and run-backs
9. Raids: group size, communication, callouts
10. Raid zones and the teaching gradient
11. Common failures and fixes
12. Review checklist
13. Examples to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

This file is cross-genre: use it for any boss, mini-boss or raid encounter. Combat arena basics (DOOM rules, high ground, cover) are in `genre-action-combat.md`, which also has the shmup stage template; checkpoint spacing and retry budgets in `fun-checks.md`; drop classification in `verticality.md`; colour-independent telegraphs in `accessibility.md`.

---

## 1. What a boss fight is for

- **A test and a summary of what the level taught.** Itay Keren (GDC 2018, "Boss Up"): the boss battle "evaluates and breaks acquired skills, reveals more of the story, and serves as a major, memorable test of strength". Carotenuto (shmup design, Game Developer): "The final boss should feel like a summary of everything you learned… have different phases, and increase the challenge until the final climax. Think of it like a separate stage in itself."
- **Test the player's verbs; don't confiscate them.** Insomniac's GDC 2024 Spider-Man 2 session describes rebuilding bosses around core combat instead of ability-disabling one-offs [unverified: abstract only]. If a boss disables the main verbs, it is a different game and needs its own teaching.
- **Tie the boss to the level's idea.** Zelda dungeons work as item tutorials with the boss as the test (Dan Taylor, Ten Principles, citing Zelda). Write the brief line: "This boss tests ___, learned in ___."
- Keren's four purposes (reward, dazzle, engage, challenge) come from a secondary summary [unverified].

## 2. The arena is readable on entry

- **See the whole fight space in the first seconds** [convention]: boundaries, hazards, cover, the boss, and the exit or reward. The player should be able to say what the space is for before the first attack lands.
- **Blizzard applies this even at zone scale.** Of the Firelands raid zone, Cory Stockton said: "It is built in a way that when you come in you can see everything… off to the left there's a spider type boss… you can see the web right when you come in" (GameBanshee, 2011). Note the correction: the quote is Stockton's (not Greg Street's) and describes the raid *zone*, with boss areas visible from the entrance, not a single arena.
- **Preview before commitment** [convention]: a threshold (fog gate, door, lift ride) where the player can look in, plus a visible edge or barrier that reads as the fight boundary. Lethal edges must look different from safe ones.
- **Readable floor.** Telegraphs live on the floor (§4), so keep floor art low-noise and never use decals that resemble telegraphs. Carotenuto's shmup rule generalises: "Don't put elements in the background… that may be confused with game elements or obstacles."

## 3. Size the arena from boss reach and player dodge metrics

No developer-primary arena dimensions were found; everything in this section is [convention]. Derive size from the project's metrics (`metrics.md`), not from looks:

- **Minimum radius ≈ boss's longest committed reach + 2–3 player dodge distances + camera clearance.** After dodging the longest attack the player should still have room to dodge again without touching a wall.
- **Too small:** lock-on cameras clip walls, attacks become unavoidable, and corners trap the player. **Too large:** the boss spends its time walking, ranged players disengage, and tension leaks.
- **Corners are camera traps.** Round or chamfer corners and keep the camera boom clear of ceilings and pillars along the arena edge.
- **Scale to the boss's movement.** A charging boss needs run-up lanes; a stationary boss can sit in a smaller room with hazards doing the movement work.
- Record the numbers on the arena's brief: boss reach, player dodge distance and i-frames, camera boom length, arena radius, number of safe zones per attack.

## 4. One telegraph language for the whole game

- FFXIV's mechanics "are shown by associated markers before these mechanics are performed… by understanding these markers in general, players will learn the game's encounter design 'language' and be able to apply their knowledge to unfamiliar encounters" (FFXIV community wiki).
- Specifics [unverified: wiki snippets]: orange ground AoEs; damage resolves when the telegraph disappears; spread and stack markers; line-of-sight blocking behind terrain; 4×4 grid arenas with rotating safe tiles; some ground telegraphs removed in high-end content.
- **Rules** [convention]: fix shape = area, colour/icon = type, and a consistent lead time across the game; teach each marker once in a low-stakes fight; reuse it everywhere; remove telegraphs only in opt-in, signposted hard content. Never rely on colour alone (`accessibility.md`); pair colour with shape, icon or sound.

## 5. Phases re-teach the space

- **Phase changes should change or re-read the arena** [convention]: floor breaks, platforms fall, water or lava rises, the boss moves to a new section, adds arrive from new doors. Each is a teaching beat for the new space.
- **Give a short low-threat beat after each transition** so players can re-read boundaries and cover before the next pattern lands. Telegraph arena changes before they hurt (cracks, rumble, light).
- **Escalate without overload.** Blizzard cut an escalation wave from a raid boss after QA and UX testing [unverified: liveblog snippet]. Don't stack mechanics past what players can read at once; follow teach → develop → twist → conclude across phases.
- **Final phase as conclusion**: combine what earlier phases taught rather than inventing new rules at the climax (Carotenuto's "summary").

## 6. Geometry the mechanics use: pillars, cover, line of sight

- **Line-of-sight mechanics need blocking geometry.** FFXIV uses terrain to break line of sight [unverified]; soulslike arenas use destructible pillars that hint at mechanics [unverified: community analysis]. If a mechanic says "hide", the arena must contain enough reliable hiding spots for the whole party, visible from anywhere.
- **Destructible cover is a resource with a budget** [convention]: count it. If the boss destroys pillars, decide how many remain for the last phase, or have them regenerate.
- **No safe spot that trivialises the fight** [convention]: every piece of cover is unsafe against at least one attack. This mirrors DOOM's arena rule of line-of-sight breaks without camping spots (`genre-action-combat.md`).
- **Mechanic geometry is part of the arena brief**: tiles, platforms, pillars, hazards, add doors, each tied to a named mechanic. Geometry with no mechanic is clutter that hides telegraphs.

## 7. Vertical arenas

- **Height changes per phase are strong** [convention]: descending through collapsing floors, climbing to a summit, or fighting on a structure the boss destroys. Match net vertical direction to emotion (`verticality.md`).
- **Keep critical telegraphs within normal camera pitch.** Gamepad players "park" their camera's vertical rotation (TLDB), so attacks from above need a ground shadow or marker; flying bosses need ground-level telegraphs. [convention]
- **Classify every edge** as free, committed, costly or lethal (`verticality.md`); lookalike drops behave alike. An arena edge that kills on one side and is a safe drop on the other is a fairness bug.
- **Platforms metric-check like a platformer** (`platformer-metrics.md`): jumps during a boss fight should sit well inside the jump envelope, since attention is on the boss.

## 8. Checkpoints and run-backs

- **The boss is where deaths cluster**, so its replay cost matters most. Checkpoint immediately before the boss, or keep the run-back short and safe; use the replay-cost budget in `fun-checks.md` and `beat_lint.py` [convention].
- **Soulslike run-backs** are a deliberate cost: keep them short, let exploration open a shortcut that shortens them, and don't place ambushes on them. DS3 places pre-boss bonfires on high ground so players reorient after dying (student analysis, see `genre-action-combat.md`). [convention]
- **Field bosses can be walked away from** [unverified]: open-world bosses should allow disengagement without a lock-in, so failure costs little.
- [convention] Lock the arena during the fight only when the fight needs it, and open a shortcut back to the checkpoint after the kill.

## 9. Raids: group size, communication, callouts

- **Size the group so individual actions matter.** Ion Hazzikostas on WoW's move from 40 to 25 players: "when a raid group had 15 healers and two dozen damage-dealers, each individual player's role often was reduced to that of a cog in a machine. With a somewhat smaller size, individual actions had more impact… while still keeping enough moving parts for strategically complex encounters" (Blizzard via WoW Insider/Engadget, 2014). Logistics was the second reason; 20-player raids showed "plenty of room for involved and challenging encounter mechanics".
- **Communication is the mechanic.** Bungie's Destiny raids were founded on the idea that "both cooperation and communication are required"; the Ghost stays silent so players hear their "five other voices"; callouts such as "Oracles up!" emerge and later become unnecessary as teams learn (Luke Smith, via Kotaku/Mein-MMO).
- **Design for nameable space.** If players must coordinate, the arena needs callout-friendly features: distinct pillars, symbols, colours, unique props at each position, and an unambiguous orientation. [convention] FFXIV players place A–D and 1–4 waymarks, so cardinal symmetry helps there; elsewhere give each side a unique landmark so "left" and "right" never depend on where the speaker stands.
- **Split roles across space** [convention]: mechanics that send sub-teams to separate plates, rooms or heights make each person's job visible and give the callouts something to name.
- Bungie's warning applies: "It's easy to make something incredibly hard. But it's hard to design something so players try, fail, get better and have fun the whole time."

## 10. Raid zones and the teaching gradient

- **Teach slowly, then combine.** Early encounters introduce a mechanic alone; later ones combine them (Bungie's stated theme of teaching players slowly). Destiny raids have no waypoints and normal mode teaches what hard mode executes [unverified].
- **Provide an entry point.** WoW's first TBC raids were "mistuned", "a brick wall"; Patch 2.1's fix set the precedent that each expansion's raids offer an entry point. The first raid of a tier is tuned easier [unverified].
- **Hub zones preview the bosses** (Firelands, §2). Firelands allowed mounts because the zone is about four times the size of Obsidian Sanctum: scale travel to zone size.
- [convention] Trash between bosses works as relax and teaching beats; place them in the beat chart like any other rest/teach beat.

## 11. Common failures and fixes

All [convention]; confirm with playtest death maps and attempt counts.

| Symptom | Likely cause | Fix |
|---|---|---|
| "I didn't see that coming" deaths | Telegraph off-screen, off-pitch, or hidden by floor art | Move the telegraph into normal pitch; add audio; clean the floor |
| Camera fights the player | Arena too small or square corners | Grow radius from metrics; chamfer corners; clear the boom path |
| Players camp one spot | Cover safe against every attack | Give each cover an answer attack; make cover destructible with a budget |
| Long fights with no tension | Arena too large; boss walking | Shrink the arena or add hazards that move the player |
| Party wipes on a call-heavy mechanic | Positions unnameable | Add distinct landmarks/markers per position |
| Quitting after repeated deaths | Long or dangerous run-back | Move the checkpoint, add a shortcut, remove run-back enemies |
| New phase feels unfair | Arena changed without a re-read beat | Telegraph the change; add a short low-threat beat |

## Review checklist

- [ ] Brief states what the boss tests and where the player learned it
- [ ] Arena readable on entry: boundaries, hazards, cover, boss and exit visible; lethal edges look lethal
- [ ] Arena size derived from boss reach, dodge distance and camera clearance, with the numbers written down [convention]
- [ ] No camera-trap corners; floor art low-noise; no decals that resemble telegraphs
- [ ] Every telegraph uses the game's shared language and isn't colour-only
- [ ] Each phase change telegraphs the arena change and gives a short re-read beat; escalation stays readable
- [ ] Line-of-sight/cover mechanics have enough reliable geometry for every phase; no trivialising safe spot
- [ ] Vertical arenas: telegraphs within normal camera pitch; edges classified; jumps well inside the envelope
- [ ] Checkpoint or short safe run-back; replay cost within budget; shortcut after the kill
- [ ] Raids: group size justified; arena positions nameable for callouts; mechanics teach before they combine; an entry-level tier exists

## Examples to study

- **Soulslike:** Dark Souls' Ornstein and Smough (pillars and two-boss spacing); Elden Ring's Margit and Godrick at Stormveil (run-back and gate approach) [convention].
- **Phase-driven arenas:** Cuphead's multi-phase bosses; Hollow Knight's Hornet fights; An Oath to the Stars (Carotenuto's boss-as-summary) [convention].
- **MMO:** WoW's Firelands zone (boss areas visible from the entrance); FFXIV savage fights on grid arenas; Destiny's Vault of Glass (communication and callouts).
- **Zelda:** any dungeon boss that tests the dungeon item (item tutorial → boss test).

Sources: Keren, GDC 2018 "Boss Up" (Game Developer, GDC Vault); Carotenuto, "Designing smart, meaningful SHMUPs" (Game Developer); GDC 2024 Spider-Man 2 session abstract; FFXIV community wiki (markers, AoE); Engadget/WoW Insider on Blizzard raid design (2014); GameBanshee WoW 4.2 interviews (Stockton); Wowhead liveblogs; Mein-MMO on Destiny (Smith); Giant Bomb community blog on FromSoftware bosses; TLDB verticality; Taylor, "Ten Principles of Good Level Design".
