# Level Design Process

## Contents
1. Pipeline and gates at a glance
2. Stage 0: three divergent concepts, cliché check, no famous levels
3. Brief and the one-page design
4. Bubble diagram → top-down plan
5. Beat chart (extended columns, worked example)
6. Gameplay first: prove it in grey
7. Blockout, machine checks, playtest, iterate
8. Stage gates G0–G4: entry and kill criteria
9. Art pass and post-art re-check
10. Revising, scoping and cutting
11. Production practice: passes, kits, collaboration
12. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

---

## 1. Pipeline and gates at a glance

A layout is a hypothesis; only blockout plus playtest confirms it (TLDB). Each stage produces an artefact that a gate (§8) scores with `review-rubric.md`.

| Stage | Artefact | What it must prove | Gate |
|---|---|---|---|
| 0 Concepts | 3 one-line concepts, one chosen with a reason | The idea is not the first cliché that came to mind | G0 |
| 1 Brief | One-page brief (`assets/level-brief-template.md`) | Purpose, verbs, pillars, teaching inventory, risks, kill criteria | G0 |
| 2 Bubble diagram | Mermaid graph, floor index per node | Topology, critical path, loops, gates; `graph_check.py` passes | G1 |
| 3 Beat chart | Extended table (§5) | Rhythm, teaching order, retry budget; `beat_lint.py` passes | G1 |
| 4 Top-down + section | Plan at stated scale; side view for ≥2 floor planes | Sizes in player metrics; sightlines; reveals | G1 |
| 5 Blockout spec | Grey geometry or grids, verb-per-space table | Fun in grey (§6); metrics fit | G2 |
| 5b Machine checks | Script output, verbatim | Lint, solve/reach, metrics (`grid-conventions.md` §5) | G1/G2 |
| 6 Playtest → iterate | Hypothesis cards with results, change log | Hypotheses confirmed or the space changed | G2/G3 |
| 7 Art pass | Final assets and lighting, precious list honoured | Art carries play; nothing proven was lost | G4 |

Studio variants worth copying:
- **Valve (Portal 2):** start from a specific goal ("We never sit down and throw random pieces at the whiteboard to see what sticks"), isometric sketch, Hammer build, heavy playtesting (Game Informer, 2010). Alternate solutions found in tests were kept if they made the tester "feel smart" and removed if they made the game feel broken.
- **Naughty Dog (Uncharted 2):** a per-level "Macro" sheet of story beats, mechanics, enemies; simple geometry playtested early. Lesson from *Drake's Fortune*: spaces built before combat was worked out caused pacing problems; author space for its encounter.
- **Bethesda (Burgess):** passes across all levels, see §11.

## 2. Stage 0: three divergent concepts, cliché check, no famous levels

LLM ideation fixates on its first output, and prompts in level-generation contests kept reproducing one structure until diversity was scored (fixation study 2026; ChatGPT4PCG 2). Before any brief:
1. Write **three concepts**, one sentence each, that differ in at least two of: **key insight** (the mechanic interaction or truth the level is about), **topology** (linear, loop, hub, vertical stack, open), **pacing shape** (slow build, two peaks, constant pressure, quiet-then-burst). Draft each from a different perspective, e.g. explorer, speedrunner, nervous first-timer [convention].
2. Name each concept's riskiest assumption and its cheapest test.
3. Pick one with a reason tied to the brief, or let the user pick. Keep the others as fallbacks if G2 kills the first.
4. For grid levels, run `level_metrics.py --compare` on the candidates; near-duplicates don't count as alternatives.

**Cliché check** [convention]: clichés are fine when chosen on purpose, never by default. Flag any of these that appear unasked:

| Genre | Defaults to question |
|---|---|
| Push puzzle | box one push from its goal in a corridor; symmetric two-box starter; padding the board to "make it harder" |
| Platformer | flat run → pit → pipe → walking enemy opener; coin arc over every gap; bottomless pit as the only hazard |
| Shooter / action | locked-door arena with waves; red barrels beside enemies; sniper on the one high balcony |
| Stealth / horror | vent route as the only alternate path; jump-scare closet; flickering-light corridor before every scare |
| Dungeon / metroidvania | key behind the boss door; colour-coded keycards; dead-end treasure room with a chest |
| Open world / multiplayer | tower climb that reveals the map; three-lane symmetric map regardless of mode |

**Don't reproduce famous levels.** Pretraining contamination is a documented risk (Todd et al. 2023). When a user says "like World 1-1", take the principle (safe first threat, one variable per step), not the tile layout. If a draft resembles a known level, say so and change its key insight or topology.

## 3. Brief and the one-page design

- **Research:** one written breakdown of a reference (footprint, circulation, sightlines, reveals) plus one line per reference on what to take ("the courtyard's ring circulation", not "this vibe") (TLDB).
- **Brief:** every field of `assets/level-brief-template.md`; a blank field is a design question. Start from the target emotion and the verbs (Taylor). Keep one concept "carried through absolutely all the way" (Hayashida, *Super Mario 3D Land* interview, 2012); five hooks means four too many.
- **Pillars:** 2–3 level pillars; every space traces to a pillar or a job.
- **Teaching inventory:** every verb, enemy, hazard and system the level teaches or assumes, with the beat where it is introduced and tested. At most 3 new items at once in learning mode, and "DON'T PUNISH WHILE TEACHING" (Hodent, GDC 2016).
- **One-page design (Librande, GDC 2010):** Librande answered "the age-old design problems of thick 'design bibles'" with single annotated sheets modelled on blueprints, placemats, schematics and timelines; his examples were a Blizzard prototype, a paper prototype from *The Simpsons Hit and Run*, and systems of *Spore*. He argued that the process "forces a complete understanding of the idea." Text version for your output: title + single idea + pillars at top; annotated top-down or Mermaid graph in the middle (critical path, numbered beats, landmarks, checkpoints, streaming gates); callouts for metrics, teaching inventory, risks and kill criteria; the beat chart along the bottom; data tables for spaces, decision points, encounters, checkpoints, accessibility hooks and performance zones. Leave room for the team's notes.

## 4. Bubble diagram → top-down plan

1. **Parti thumbnails (3–5):** core shapes (ring, spine with pockets, tower, descent, figure-eight); choose the one that serves the concept.
2. **Bubble diagram** as Mermaid: nodes = spaces with role, intensity and floor index (`F0`, `F1`); edges labelled `gate`, `one-way`, `shortcut`, `vista`, and vertical edges `↓drop(one-way)`, `↑ladder`, `⇅lift`. Mark the critical path. Classify every branch: critical, optional-with-reward, loop/shortcut, vista-only; a branch that fits none is a cut candidate. Run `graph_check.py` for reachability, key-before-door order and consumed-key softlocks.
3. **Top-down plan** at a stated scale (`1 cell = 2 m`), footprints checked against run speed and metrics (`metrics.md`); sightlines, reveals, cover, hazards, entries and exits marked. Draw a **section** for any space with ≥2 floor planes (`verticality.md`). Grids follow `grid-conventions.md`.

## 5. Beat chart (extended columns, worked example)

Columns (headers are what `beat_lint.py` reads; extra columns are ignored by it): `# | Beat | Mechanic (stage) | Intensity | Emotion | New concepts | Choice | Expected deaths | Replay cost | Checkpoint | Duration | Guidance cues | Assist hooks | Telemetry | Hypothesis`.
- **Intensity** 1–5. **New concepts**: names of brand-new things introduced here. **Choice**: y/n, is there a real route, approach, risk or order choice. **Expected deaths**: first-time player estimate. **Replay cost**: seconds of already-beaten content replayed per death. **Checkpoint**: id of a checkpoint at the start of this beat. **Assist hooks / Telemetry / Hypothesis**: see `accessibility.md` §5, `playtesting-and-critique.md` §4, `assets/hypothesis-card.md`.
- Validate with `beat_lint.py` (defaults are [convention]): rest (≤2) before and after each peak (≥4); ≤2 consecutive beats at ≥4; ≤1 brand-new concept per beat; no no-choice stretch over 120 s; P(death) × replay ≤ 10 s; peak intensity not on the peak replay cost; a checkpoint before every beat expecting ≥2 deaths; no 3 flat beats in a row. Also check by hand: peaks rise toward the climax; compression precedes reveals; nothing tested before taught; total duration matches the brief.

Example: third-person level teaching a grapple, target 12 min.

| # | Beat | Mechanic (stage) | Intensity | Emotion | New concepts | Choice | Expected deaths | Replay cost | Checkpoint | Duration | Guidance cues | Assist hooks | Telemetry | Hypothesis |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Bridge ledge, tower visible | walk, look | 1 | curiosity | 0 | y | 0 | 0 | CP1 | 0:45 | tower framed by arch; light beyond | nav goal NG1 | enter_b01 | H1 |
| 2 | Yard: grapple 1 m gap over safe ground | grapple (intro) | 1 | delight | grapple | n | 0 | 0 | | 1:30 | hook points in affordance colour; only exit | no-fail practice | exit_b02 | |
| 3 | Canyon: chain two hooks over shallow water | grapple (develop) | 2 | confidence | hook chaining | y | 0.5 | 10 | | 2:00 | canyon walls lead; water sound | traversal-assist tags | death_b03 | |
| 4 | Ring arena ambush, 3 melee | grapple escape + melee | 4 | tension | 0 | y | 1 | 10 | CP2 | 2:30 | spawns telegraphed from above | high-contrast enemy tag | enter_b04, death_b04 | H2 |
| 5 | Campfire; shortcut lift to beat 1 | rest, shortcut | 1 | relief | 0 | y | 0 | 0 | CP3 | 1:00 | warm light; lift sound; view back | nav goal NG3 | checkpoint_CP3 | |
| 6 | Quarry: hooks on moving cranes, two routes | grapple (twist) | 2 | focus | moving hooks | y | 1 | 12 | | 2:15 | crane motion; tower visible again | slow-speed safe timing | death_b06 | |
| 7 | Tower climb under ranged fire | all (conclude) | 5 | exhilaration | 0 | y | 2 | 10 | CP4 | 1:30 | spiral keeps goal above; muzzle flashes | ledge guard on tower | death_b07, exit_b07 | H3 |
| 8 | Summit vista, next region | look | 1 | awe | 0 | n | 0 | 0 | | 0:30 | next landmark on horizon | | exit_b08 | |

## 6. Gameplay first: prove it in grey

**Stance.** Gameplay matters more than graphics; graphics serve gameplay. Prove the verb–space interaction in placeholder form first. Art then carries landmarks, affordances, danger and routes; art that hides a proven affordance is a bug and gets reverted.

**Why.** Valve's first *Half-Life* "wasn't any fun… We had some cool levels, but they didn't fit together well"; the team started over from one prototype level crammed with every working idea, and silent playtests settled arguments: "Just because you were sure something was going to be fun didn't make it so" (Birdwell, "The Cabal", 1999). Fujibayashi pitched *Breath of the Wild* with a 2D NES-style prototype where he could shake trees, roll logs and shoot arrows through flames before the 3D game existed (GDC 2017; BotW, not TotK). Miyamoto: graphics "wouldn't matter if the games weren't fun to play" (2006). TLDB: "99% of the time, your blockout will not survive a playtest… Want to delete an entire room? Do it." Art direction should serve play too: BotW's art director chose a style that made it "easy to lie" because realism "would interfere with how the game's weapons and magic feel."

**Paper checks to run** (no published validation; [convention], proposed):
1. **Grey description test.** Rewrite the level summary with no materials, lighting, props or mood adjectives: only spaces, sizes, heights, connections, verbs, threats, rewards and choices. If it stops being interesting (no decisions, no variation, no surprise), the layout is the problem; fix it before discussing art. Example: "A 30×60 m hall on two planes (0 m, 6 m). 3 ranged enemies on the balcony, 4 melee on the floor. Choice: rush the floor or take the north ladder to flank; a mid-hall drop returns to the floor one-way."
2. **Verb-per-space table.** `Space | Primary verb(s) | Decision posed | What changes on return | Job if no verb (rest / reveal / story) | Keep / merge / cut`. A space with no verb and no stated job is cut or merged.
3. **Riskiest interaction first.** The first blockout milestone exercises the riskiest verb–space interaction (for vertical levels: drops, climbs and vertical sightlines).
4. **Precious/flexible list** for the art handoff. Yang: "Which walls must absolutely stay the same dimensions, and which walls are more cosmetic?… document your intent." Reece (Apex Legends): decide "what's precious and what's flexible." List per space the dimensions, sightlines, heights, ledges and affordance colours art must not change, and what it may change.
5. **Art states its job.** Every art-direction proposal names the play information it carries or protects (landmark, affordance, danger, route).
6. **Post-art re-check** (§9), including every vertical cue.

**Honest exception.** When the core experience is mood, story or place, grey can't answer it. Firewatch's team found "Greyboxing did not answer any of the important questions" because pacing was a narrative and environment-art problem (Ng, GDC 2016); Untitled Goose Game's grey village felt inauthentic until the designer scouted real locations (Strasser, GDC 2021). Then say so, and test the **cheapest representative slice**: one space at target art and audio quality with its real interactions, before scaling. The gameplay-first rule still applies to everything the player does there.

## 7. Blockout, machine checks, playtest, iterate

- **Build at true metrics from the first block:** capsule fit, head clearance, step height, jump gaps, cover heights, AI navigation (`metrics.md`). Self-test with full gravity, collision and speed, not by flying the editor camera (TLDB). Block out vertical connections first.
- **Massing before detail:** volumes, landmark silhouettes and light direction first. Colour-code walkable / climbable / blocking / hazard [convention], with placeholder landmarks so wayfinding can be tested.
- **Machine checks (stage 5b):** lint → solve or reach or graph → metrics → repair, max 3 rounds; report the script's numbers verbatim; label anything unchecked "hand-traced, not machine-verified" (`grid-conventions.md` §5–7).
- **Playtest:** self-test daily (TLDB); fresh testers per iteration; protocol and hypothesis cards in `playtesting-and-critique.md`.
- Unintended routes will appear: support them if they make players feel smart and don't break progression, block them if they make the space feel broken.

## 8. Stage gates G0–G4: entry and kill criteria

Gate verdicts (Pass / Pass-with-conditions / Rework) come from `review-rubric.md`. Write kill criteria **before** the gate, with numbers. All thresholds here are [convention].

| Gate | Entry criteria (all present) | Kill or re-brief when |
|---|---|---|
| **G0 Concept + brief** | 3 divergent concepts, one chosen; brief complete; 2–3 pillars; teaching inventory; riskiest assumption with its cheapest test; kill criteria written | No concept survives the grey description test; the single idea can't be said in one sentence; the riskiest assumption has no cheap test |
| **G1 Paper** | Bubble diagram passing `graph_check.py`; beat chart passing `beat_lint.py`; top-down + sections; verb-per-space table; decision-point table; hypothesis card per risky beat; one-pager | Rubric verdict Rework; goal unreachable or softlock found; a critical-path space has no verb and no job |
| **G2 Blockout** | Playable at true metrics; machine checks clean or failures listed; 5–8 first-time testers; hypothesis results; perf/streaming zones blocked in | The riskiest interaction fails its hypothesis after two cue or geometry iterations; it is not fun in grey and the cause isn't one of the §6 exceptions |
| **G3 Gameplay complete** ("Content Complete") | Encounters, scripting, AI nav, checkpoints and assist hooks work; telemetry events fire; difficulty pass at every preset | An optional beat's cost exceeds its value (cut whole beats, not polish); a beat's death or quit rate misses its card's threshold twice |
| **G4 Art + readability** | Post-art fresh-player test; greyscale and colour-blind captures; photosensitivity check; landmarks read under final lighting; precious list honoured | Any art change that breaks a proven affordance or vertical cue is reverted, not argued |

Example kill criterion: "Rework the vista beat if fewer than 60% of first-time testers notice the landmark within 30 s after two cue iterations."

## 9. Art pass and post-art re-check

- Light in TLDB's order before the art pass: global light, then wayfinding and critical path, then gameplay, then mood.
- Realistic props hide affordances that worked in grey; players "skip over environmentally realistic props" (yellow-paint debate). Portal 2's team redesigned the emancipation grid's effect after testers didn't notice it: art serving a gameplay need.
- Re-run first-time tests with **fresh** players; compare hesitation spots, missed routes and section times with greybox results.
- Re-check every precious item, every vertical cue (drop signals, look-up leads, hidden-route invitations: props and lighting break these first), affordance consistency (Schatz), landmarks at distance under final fog and post, greyscale and colour-blind views (`accessibility.md`).

## 10. Revising, scoping and cutting

- **Show diffs when revising.** List each change with coordinates, reason and re-check result: "moved box from (4,3) to (5,3) to remove a dead corner; re-ran solver: 23 → 27 pushes"; "lowered ledge at (12,6) from 4 to 3 tiles: jump margin 96% → 72% of envelope". Never silently re-issue a whole new map; keep a change log in the brief.
- **Weekly scoping questions** (TLDB): what will you work on, and when? Which features or levels are nice-to-haves that can be cut? Content off the critical path is seen by fewer players and must earn its cost.
- **Kill** an idea that fails repeated tests of its intent and can't be fixed cheaply, or that is optional and costly [convention]. Don't get attached to spaces players don't use. Prove the riskiest idea first; if it dies, re-brief before building more. Cut whole beats or spaces, not polish spread thin.
- **Common greybox mistakes** [convention]: wrong (usually too big) scale; detailing before testing; corridors wider than combat needs or too narrow for a third-person camera; no landmarks; one colour; collision that differs from the mesh; encounters fitted into finished geometry; testing only as the designer; openings players use that AI can't path.

## 11. Production practice: passes, kits, collaboration

- **Iterative passes (Burgess, Bethesda, GDC 2014):** each pass is done across all levels before any level moves on, so nothing is polished while another level is unplayable and cuts fall on whole levels early. A "Content Complete" pass, internally the "Ship With Shame" pass, precedes polish, which takes as many passes as fit. Reported pass names and counts conflict [contested]; don't quote a fixed number.
- **Modular kits:** Burgess & Purkeypile, *Skyrim* (GDC 2013), with a *Fallout 4* follow-up at GDC 2016. Build to a grid sized from the metrics doc; include transition pieces; stress-test the kit in a gym; agree kit sizes with art before greyboxing so the art swap is 1:1 [convention].
- **Door problem (England, 2014):** every interactive element touches design, art, audio, AI, scripting, narrative and QA. Ask per element: who owns its state, how is it signalled, can AI use it, can it be sequence-broken?
- **Holistic design (Steve Lee, Arkane, GDC 2017):** consider gameplay, presentation and story together. Share the brief and beat chart with every discipline before blockout so audio and narrative peaks match yours [convention].

## 12. Review checklist

- [ ] Three concepts differing in key insight, topology or pacing; choice justified; cliché check run; no famous level reproduced
- [ ] Brief complete: pillars, teaching inventory, riskiest assumption, kill criteria, hypotheses as cards
- [ ] One-page design: graph/plan, beat strip, callouts and data tables
- [ ] Bubble diagram with floor indices and labelled edges; `graph_check.py` run; sections for ≥2 floor planes
- [ ] Beat chart has all extended columns; `beat_lint.py` run and output reported
- [ ] Grey description test passed; verb-per-space table has no unjustified empty space
- [ ] Precious/flexible list written before art; post-art re-check planned
- [ ] Mood/place exception stated if it applies, with the cheapest representative slice
- [ ] Machine checks reported verbatim; unverified claims labelled
- [ ] Gate entry criteria met; verdict from `review-rubric.md`; kill criteria have numbers
- [ ] Revisions shown as coordinate diffs with re-check results
