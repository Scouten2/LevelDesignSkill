# Playtesting & Critique

## Contents
1. Critique workflow (when given a level to review)
2. Symptom → likely causes → fixes
3. Playtest protocol
4. Hypotheses, instrumentation and telemetry
5. Small samples vs data at scale
6. Accessibility (pointer)
7. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

---

## 1. Critique workflow

Use when the user gives a level description, map image, screenshots, video notes, grids or layout data. For a formal scored review with a gate verdict, run this workflow and then score with `review-rubric.md`.

**Step 1 — Gather context.** Without these the critique is guesswork; ask, or state assumptions explicitly:
- Genre and camera (1P/3P/top-down/2D); player count.
- Player verbs and abilities available *at this point*; player metrics or movement kit if sizes matter (`metrics.md`).
- Intended experience: purpose, mechanic taught/tested, target emotions, position in the arc, target duration.
- Stage (paper, greybox, art pass): critique what is still changeable at that stage.

**Step 2 — Run the checks that don't need opinions.** If the level is a grid or graph, run the bundled scripts first (`grid-conventions.md` §5) and quote their output. Never call a level solvable, reachable or "too hard" without a script run or a labelled hand trace.

**Step 3 — Walk the critical path as a first-time player.** Narrate it beat by beat: what is visible on entry, what pulls the eye, where the first decision is, what the player would most likely try, where they would hesitate. Repeat as an explorer (what's off-path, does it pay) and as a struggling player (where failure happens, what it costs in replay seconds).

**Step 4 — Evaluate** (each item → pass / issue / U = unknown, needs playtest):

| Area | Questions |
|---|---|
| Purpose | Does every space have a job (verb, rest, reveal, story)? Does the grey description stay interesting (`process.md` §6)? |
| Flow | Critical path continuous and recognisable? Loops vs dead ends; do dead ends pay? Shortcuts return to safety? |
| Guidance | **Every critical-path decision has ≥2 independent cues** (landmark, light, leading line, motion, affordance shape/colour, sound, enemy placement)? Critical info within normal camera pitch? |
| Verticality | Sections drawn; drops classified; hidden routes fair (`verticality.md`) |
| Pacing | Intensity alternates; rest around peaks; compression before reveals; peaks rise |
| Teaching | Introduce safely → develop → twist → conclude; nothing tested before taught; no punishment while teaching |
| Metrics | Sizes derived from the character; critical jumps in the safe band; impossible things look impossible; AI can path |
| Challenge | Encounter space authored for the encounter; ≥2 approaches; failure attributable and cheap to retry (`fun-checks.md`) |
| Readability | Consistent affordance language; interactables distinct from dressing; survives the art pass |
| Storytelling | "What happened here" readable from ≥3 associated props, on or framed from the critical path |
| Accessibility | Run the checklist in `accessibility.md` |

**Step 5 — Output.** Lead with the **top 3 issues by player impact**, then secondary notes, then what works (so it's kept). Each issue:

```
### <N>. <Problem in one line>
- Evidence: what in the layout causes it (location as (col,row) or space id, geometry, cue, sightline, script output)
- Player impact: what a first-time player will do/feel, and how many players it hits
- Fix: concrete change (dimensions, cue added, geometry moved); 2–3 options when useful
- Cost: cheap (cue, light, prop) / medium (geometry tweak, re-script) / expensive (re-layout, new asset/mechanic)
```

Rank fixes cheapest-first when impact is equal. End with the hypotheses the next playtest should test, written as hypothesis cards (§4).

## 2. Symptom → likely causes → fixes

Diagnose before fixing: confirm the symptom in observation or telemetry, check causes in order, try the cheapest fix first. Many fixes are [convention] practitioner defaults.

| Symptom | Likely causes | Fixes (cheap → expensive) |
|---|---|---|
| **Players get lost** | <2 cues at a decision; no global landmark; repeated rooms with no district identity; critical exit darker than an optional one; sight blocker hides the exit; loop with no recognisable return point; stacked layers with no map support | Light the exit, add a leading line, frame a landmark through it; motion/sound at the goal; differentiate districts by material, colour, light; sight-block the wrong way; curve the path so the goal stays in view; remove the redundant branch; flash or remind the objective (Halo 3) |
| **Miss the shortcut / secret** | Revealed from the wrong side; no "click" moment; no foreshadowing; secret tell identical to dressing | Show the far end (locked door, lift) earlier so opening it is recognised; frame the familiar area through it; unlock sound; a consistent subtle tell (crack, odd light) |
| **Skip optional content** | Reward invisible; branch looks like the critical path or a dead end; too long; no safety to explore | Show the reward from the main path (vista, glint); keep reward dead ends short; place optional pockets after rest beats; make branches read as optional (smaller, off-axis) |
| **Fight too hard** | Wrong cover height; spawns behind or out of view; no retreat or flank; sightlines beyond player weapon range; no resources; untaught enemy; stacked hazards | Telegraph spawns; add cover or a flank route; risky health/ammo pickup; shorten sightlines; teach the enemy alone first; stagger waves |
| **Fight too easy** | One position covers everything; enemies can't path to the player; entrance is a holdable choke; overpowered pickup | Break the cheese sightline; add enemy routes or a ranged enemy aimed at the spot; move pickups into contested space; second wave from another side; vertical threat |
| **Players camp / turtle** | Safe spot with full view; no reason to move; regenerating safety | Resources forward among enemies; flush-out enemies; time pressure or moving objective; temporary cover; remove the perfect refuge (DOOM's push-forward design) |
| **Area feels empty / boring** | Built at eyeballed scale; no verb exercised; no landmark or vista; uniform light; long traversal with no decision | Shrink it; add a verb or a route choice; frame a vista or vignette; vary light and ceiling height; add a risk-vs-safe micro-choice; cut it |
| **Backtracking tedious** | Return identical to outbound; no shortcut; respawned enemies with no change | Shortcut or one-way door back to the hub at the end of the dangerous stretch; change the space on return; lift or fast travel; new route with a new ability |
| **Don't understand the mechanic** | Introduced under pressure; several variables at once; no safe failure; inconsistent tell; text instead of space | Rebuild as safe intro (only exit requires it) → develop → twist; one variable at a time; consistent affordance; let the space force the first use (World 1-1's first Goomba) |
| **Players die "unfairly"** | Threat off-screen; "barely possible" critical jump; ambiguous surface; camera obstructs; untelegraphed instant death; long replay to retry | Telegraph hazards; move gaps into the safe band (`platformer_reach.py` margins); consistent lethal-surface language; fix camera volumes; checkpoint before the challenge; first instance survivable |
| **Ignore story vignettes** | Off-path or behind the view direction; competing with combat; unlit; too few props | Place at a rest beat on the critical path; frame through a doorway the player faces; light it; ≥3 associated props; sound cue |
| **Motion sickness** | Low FOV; narrow, low, twisting 1P corridors; forced shake, bob or rotation | Widen and straighten, raise ceilings; no forced camera motion in mandatory sections; toggles and FOV option (`accessibility.md` §6) |
| **Pacing drags** | Many low beats in a row; traversal longer than estimated; same encounter type repeated | Compress traversal; interleave a reveal or micro-challenge; vary encounter and space type; re-plot the beat chart with measured times and re-run `beat_lint.py` |
| **Players sequence-break** | Unintended jump or climb; cosmetic gate; physics stacking; order-dependent triggers | Valve's rule: keep it if it makes the player feel smart, remove it if it makes the game feel broken; order-independent triggers; real collision on gates; or design an intended expert route |
| **Level 65 problem** (a spike that converts or retains short-term but drives churn) | Mandatory difficulty wall | Lower mandatory difficulty; move the challenge to an opt-in path with an honest forecast (§5, `fun-checks.md`) |

## 3. Playtest protocol

**Frame.** Ambinder's Valve slides: "Game designs are hypotheses / Playtests are experiments / Evaluate designs off playtest results / Repeat" (GDC 2009), and judge by what people do, not what they say. Valve's first *Half-Life* rewrite came from watching testers in silence: "Just because you were sure something was going to be fun didn't make it so" (Birdwell, "The Cabal").

**Before the test**
- Write a **hypothesis card** per risky beat (`assets/hypothesis-card.md`): prediction, metric, method, sample, pass threshold, fail action, events. A test without hypotheses produces anecdotes.
- Fix the build, starting state and observers. Use **fresh players** for first-time readability; a tester is "burned" after their first play [convention]. Include some players with impairments (GAG).
- Cadence: self-test daily (TLDB). One studio's rhythm worth copying, from Phil Co on Valve's cabals: "Every Friday, we would playtest the section of the game that we're responsible for with someone from outside the team… Everything we do during the week is focused on that Friday playtest… On Mondays, we have meetings where we decide what the goals are for the playtest" (via TLDB).

**During the test**
- "The golden rule of playtesting is: do not help." The instant you explain how something works, the test is contaminated.
- **Stuck = data.** Note where, for how long, what they tried. Set a rescue threshold in advance and log every rescue [convention].
- Write notes during the session. Think-aloud reveals intent but distorts timing and difficulty data; alternatives are silent play plus interview, or retrospective think-aloud over the recording [convention]. Puzzle-specific protocol (narrated video, batches of one or two, watch whole sessions before changing): `puzzle-verification.md`.

**What to record:** timestamped stops, look-arounds, backtracks, wrong turns and deaths with cause; missed pickups, secrets, shortcuts and vignettes; where the player looked at each planned reveal; time per beat vs the beat chart; spontaneous comments and emotion at planned peaks; unintended routes and exploits.

**After the test** — open, non-leading questions: "Describe the level to someone who hasn't played it." "Where did you feel lost?" "What were you trying to do here?" "What was the most memorable moment?" "Sketch a map from memory" (tests the cognitive map, Lynch). Then score each hypothesis card pass/fail and apply its fail action.

**Iteration.** RITE (Medlock et al. 2002): fix a problem as soon as it and a clear fix are known, sometimes after one participant, and let later participants test the fix. Log each change as a coordinate diff (`process.md` §10).

## 4. Hypotheses, instrumentation and telemetry

- **Name events per beat** so funnels and death maps fall out of the design [convention]: `enter_<beat>`, `exit_<beat>`, `death_<beat>` (with cause and position), `checkpoint_<id>`; optional `choice_<decision>_<option>`, `assist_<hook>`, `skip_<puzzle>`. Use the beat-chart ids (`enter_b04`). Payload: timestamp, session id, position with floor plane, difficulty preset, assists on.
- **Derived measures:** beat funnel = exits ÷ enters; time in beat = exit − enter (compare medians to the beat chart; long tails mark confusion, short outliers mark skips); death map from `death_` positions (project dots to the floor; centre-of-character dots float near ledges, Klonk Games); quit point = enter with no exit before session end; replay seconds = time between `checkpoint_` and the next `death_`.
- **Halo 3 (Microsoft user research):** testers' routes mapped and aggregated into scattergrams, plus a pop-up asking players every few minutes to rate engagement or frustration; findings became fixes such as objectives that "flash on the screen" and a barrier on a highway where players kept flying to their deaths. Pagulayan's goal: find "the discrepancy… between what the player's actual experience is versus the designer's vision" (NPR, 2007). No logging interval is verified; don't quote one.
- **Possibility vs actual maps** ("Game Metrics Without Players", AIIDE): a map of where death *can* occur shows structure; comparing it with actual deaths separates layout effects from behaviour.
- Numbers show what happens, rarely why; pair them with observation. Confusion vs boredom: quitters who spend much longer on a step than passers suggest confusion [unverified] (vendor heuristic).

## 5. Small samples vs data at scale

- **Small playtests (about 5–8 fresh players)** find lost, usability and readability problems. Nielsen's ~5-users heuristic applies to usability only [convention], not to balance, difficulty or fun.
- **Difficulty, churn and monetisation need data at scale.** King's Candy Crush level 65 was the highest-converting, highest-revenue level and also the biggest source of churn; "increasing difficulty raised conversions short term. Over the long run, though, making the level easier retained players longer," and designers should "be prepared for long A/B tests" (Guardiola and Wedekind, GDC 2024). A small test would have shown only that level 65 was hard.
- So each hypothesis card states its method: paper/script (solvability, reachability, beat budget), small playtest (noticing, understanding, getting lost), or telemetry at scale (pass rate, attempts per win, quit rate).
- Bots and simulated player populations can predict pass and churn rates before launch but are corrected with human data (Roohi et al., CHI PLAY 2020); see `genre-casual-mobile.md`.

## 6. Accessibility (pointer)

Level-scope accessibility (colour and sound redundancy, assist hooks, photosensitivity, camera motion, difficulty and checkpoints) lives in `accessibility.md`. Run its checklist during every critique and at G4.

## 7. Review checklist

- [ ] Context gathered or assumed explicitly: genre, camera, verbs, metrics, intent, stage
- [ ] Scripts run first where applicable; output quoted; unverified claims labelled
- [ ] Critical path walked as first-time player, explorer and struggling player
- [ ] Every area in §1 evaluated; unknowns marked U, not passed
- [ ] Top 3 issues first; each = problem → evidence → player impact → fix → cost; what works listed
- [ ] Hypothesis cards written before the session, with thresholds and fail actions
- [ ] Fresh players; no help; rescue threshold set and logged; impaired players included where possible
- [ ] Events named per beat (`enter_`, `exit_`, `death_`, `checkpoint_`); funnels and death maps planned
- [ ] Method matched to question: small playtest for readability, data at scale for difficulty and churn
- [ ] Changes logged as diffs and re-tested (RITE)
- [ ] `accessibility.md` checklist run; formal reviews scored with `review-rubric.md`
