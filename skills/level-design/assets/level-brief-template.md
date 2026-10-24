# Level Brief: <Level name>

> One page per level where possible (Librande-style: tables and a plan, not prose). A field you can't fill is a design question to answer before blockout. Process and gates: `references/process.md`.

## 0. Concepts considered
| # | Concept (one sentence) | Key insight | Topology | Pacing shape | Riskiest assumption |
|---|---|---|---|---|---|
| A | | | | | |
| B | | | | | |
| C | | | | | |
- **Chosen:** <A/B/C> because <reason tied to purpose and pillars>
- **Cliché check:** <defaults flagged and kept on purpose, or replaced>. Not a copy of a known level: <yes / note>

## 1. Purpose
- **One-sentence pitch:** <what happens here, in player terms>
- **Job in the game arc:** <intro / teach / escalate / climax / breather / finale; what comes before and after>
- **Single concept carried all the way:** <the one idea>
- **Pillars (2–3):** <e.g. "see it before you reach it", "every fight has a high and a low route">
- **Core verbs used:** <e.g. sprint, mantle, grapple, push block>
- **Target emotions (in order):** <e.g. curiosity → dread → panic → relief>

## 2. Player & constraints
- **Player metrics / movement kit:** <height, width, speeds, jump height and distance, camera and FOV>; platformers: `assets/movement-kit.md`
- **Player state on entry:** <abilities, items, health/resources, knowledge>
- **Player count / mode:** <single-player, co-op N, PvP NvN>
- **Target duration:** <first-time minutes; replay/speedrun minutes>
- **Scope & tech limits:** <budget, kit available, streaming, performance>
- **Numeric targets to verify:** <e.g. grid ≤ 12×10, 4 boxes, ≥ 15 pushes; no critical jump > 90% of envelope>

## 3. Teaching inventory
| Concept (verb, enemy, hazard, system) | New or assumed | Introduced (beat, safe?) | Developed | Twisted | Tested / concluded |
|---|---|---|---|---|---|
| | | | | | |
- ≤ 1 brand-new concept per beat; ≤ 3 new items at once while learning (Hodent); no punishment while teaching.

## 4. Structure
- **Topology:** <linear / loop / hub-and-spoke / branching / open / lock-and-key / vertical stack>
- **Critical path (start → goal):** <beats in order>
- **Optional content:** <pockets, secrets, rewards, and why the player wants them>
- **Gates & shortcuts:** <what blocks progress; what opens back to safety>
- **Landmarks:** <1–3 orienting landmarks; where each is first seen>
- **Bubble diagram:** Mermaid, floor index per node (`F0`, `F1`), edges `gate`/`one-way`/`shortcut`/`vista`/`↓drop(one-way)`/`↑ladder`/`⇅lift`; `graph_check.py` result: <paste>

## 5. Verticality & fall-cost policy
- **Floor planes per area (≤ 3):** <list; section drawn for each multi-level area>
- **Look-up / look-down / look-back moments:** <where>
- **Vertical loop back to safety:** <lift, ladder, kick-down ladder, drop>
- **Hidden vertical route (optional):** grammar taught at <where>; visible from <vantage>; invitation <glint, corpse, light>; cost to try <survivable fall / nearby checkpoint>
- **Drop classes:** free ≤ <h>, committed <h–h>, costly <h–h>, lethal ≥ <h>; lookalike drops behave alike (`references/verticality.md`)
- **Fall-cost policy:** <respawn at ledge / damage / back to checkpoint / lose progress>; catch ledges for punishing climbs: <where>

## 6. Gameplay first
- **Grey description** (no materials, lighting, props or mood words; only spaces, sizes, heights, connections, verbs, threats, rewards, choices):
  <paragraph — if it isn't interesting, fix the layout before the art>
- **Verb-per-space table:**

| Space | Primary verb(s) | Decision posed | What changes on return | Job if no verb (rest / reveal / story) | Keep / merge / cut |
|---|---|---|---|---|---|
| | | | | | |

- **Precious (art must not change):** <dimensions, sightlines, heights, ledges, affordance colours, per space>
- **Flexible (art may change):** <cosmetic walls, dressing, silhouettes that carry no play>
- **Mood/place exception?** <no / yes: cheapest representative slice to test = …>

## 7. Beat chart
Run `beat_lint.py` on this table and paste its output below it.

| # | Beat | Mechanic (stage) | Intensity | Emotion | New concepts | Choice | Expected deaths | Replay cost | Checkpoint | Duration | Guidance cues | Assist hooks | Telemetry | Hypothesis |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | | | | | |

Intensity 1–5 · Choice y/n · Replay cost in seconds · Checkpoint id at the beat's start · Guidance ≥ 2 independent cues per decision · Telemetry `enter_` / `exit_` / `death_` / `checkpoint_`.

## 8. Accessibility hooks
| Hook id | Type (nav goal / ledge guard / traversal tag / puzzle skip / high-contrast tag / second-channel emitter / practice space / assist offer) | Location (space, coords) | Purpose | Guideline |
|---|---|---|---|---|
| | | | | |
- Completable with invincibility, infinite stamina and slowed speed: <yes / issue>. Flashing content audited: <list> (`references/accessibility.md`)

## 9. Story & setting
- **What happened here?** <the environmental story a player can reconstruct without text>
- **Key vignettes and their position relative to the critical path:**

## 10. Risks, hypotheses & kill criteria
- **Riskiest interaction (prove in grey first):**
- **Hypothesis cards:** <ids; one per risky beat, `assets/hypothesis-card.md`>
- **Kill criteria (with numbers):** <e.g. "rework the vista if < 60% notice the landmark within 30 s after two cue iterations">
- **Cut list (ordered by cost/value):**

## 11. Review & change log
- **Gate / rubric verdict:** <G#, score, verdict (`references/review-rubric.md`)>
- **Changes:** <diffs: "moved box (4,3) → (5,3) to remove a dead corner; solver 23 → 27 pushes">
