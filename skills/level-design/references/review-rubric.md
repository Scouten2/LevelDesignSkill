# Level Review Rubric

## Contents
1. When to use it
2. Scale, U and blockers
3. The twelve criteria and weights
4. Anchors: what 0, 2 and 4 look like
5. Computing the score and the gate verdict
6. Self-review loop
7. Review report format
8. Compact output template
9. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

No public studio level-review rubric exists. This one is a synthesis; every weight, threshold and verdict rule in it is **[convention]**. Its value is repeatability: the same evidence gets the same score.

---

## 1. When to use it

- **Self-review:** after every design artefact you produce (brief, paper design, blockout spec, revision), before handing it over (§6).
- **Review mode:** when the user asks "review / score / is this ready" for their own level.
- **Gates:** G0–G4 in `process.md` §8 use the verdict rules in §5.
- The rubric judges design quality. It never decides solvability, reachability or jump feasibility; scripts do (`grid-conventions.md` §5). Fun-specific checks and their evidence strength live in `fun-checks.md`; the rubric scores whether they were run and passed.

## 2. Scale, U and blockers

| Score | Meaning |
|---|---|
| 0 | Absent or broken |
| 1 | Major issues: a typical player will be hurt by it |
| 2 | Works, with notable issues |
| 3 | Solid; minor issues only |
| 4 | Exemplary; evidence shown, nothing to fix |
| **U** | Unknown: only a playtest or data can answer. **Never counted as a pass.** Each U becomes a hypothesis card |

- Score from evidence present in the artefact, not from intentions. A 3 or 4 must cite its evidence (table, script output, section drawing).
- **Blockers** (criteria 1, 2, 6, and 9 for photosensitivity): at 0–1 the verdict is Rework regardless of total.
- **Count, don't eyeball:** a solvability or reachability claim with no script run or labelled hand trace makes criteria 2 and 6 **U**; with a hand trace only, they cap at 2; a 4 needs script verification.

## 3. The twelve criteria and weights

| # | Criterion | Weight | Blocker | Main evidence |
|---|---|---|---|---|
| 1 | Intent, pillars and gameplay-first | 10 | yes | Brief, pillars, grey description, verb-per-space table |
| 2 | Critical path and flow | 10 | yes | Bubble diagram, `graph_check.py`, solver/reach output |
| 3 | Guidance and wayfinding | 10 | | Decision-point table with ≥2 cues each, landmark list |
| 4 | Pacing | 8 | | Beat chart, `beat_lint.py` |
| 5 | Teaching and onboarding | 10 | | Teaching inventory, beat chart New concepts column |
| 6 | Metrics fidelity | 8 | yes | Metrics table, `platformer_reach.py` margins, sections |
| 7 | Challenge, failure and fun | 10 | | Expected deaths, replay cost, checkpoints, `fun-checks.md` |
| 8 | Readability and affordances | 6 | | Affordance language, precious list, greyscale capture |
| 9 | Accessibility | 10 | flashing | `accessibility.md` checklist, assist-hook table |
| 10 | Storytelling and place | 4 | | Vignette list, placement on or framed from the path |
| 11 | Production feasibility | 8 | | Kit coverage, perf/streaming zones, scope and cut list |
| 12 | Testability | 6 | | Hypothesis cards, named telemetry events |
| | **Total** | **100** | | |

**Required criteria by gate** [convention]: G0 → 1, 11. G1 (paper) → 1–7, 9, 11, 12 (8 and 10 scored if evidence exists, otherwise deferred). G2–G4 → all twelve.

## 4. Anchors: what 0, 2 and 4 look like

| # | 0 | 2 | 4 |
|---|---|---|---|
| 1 | No stated purpose; spaces exist "because levels have rooms" | Clear concept, but some spaces have no verb or job; grey description is flat in places | One concept carried all the way; 2–3 pillars; every space has a verb or a stated job; grey description is interesting on its own |
| 2 | Goal unreachable, softlock, or unverified puzzle | Path works but is ambiguous in places; a dead end without payoff; a one-way drop with no return | Script-verified reachable; loops and shortcuts back to safety; every branch classified; vertical loops close |
| 3 | Critical decisions with no cue, or colour-only cues | Most decisions have 2 cues; one relies on a single cue or sits outside normal camera pitch | Every critical decision has ≥2 independent cue channels; global landmark; critical info at eye level |
| 4 | Flat or exhausting; no rests | Alternates, but `beat_lint.py` warns (a peak without rest, a long no-choice stretch) | `beat_lint.py` clean; peaks rise; compression before reveals |
| 5 | Mechanic tested before taught; punished while teaching | Taught in order, but one beat adds 2+ new concepts or relies on text | Inventory complete; each concept introduced safely → developed → twisted → concluded; ≤1 new concept per beat |
| 6 | Eyeballed sizes; critical jump beyond the kit | Sizes derived, but a critical jump is above 90% of envelope or a lookalike drop behaves differently | All sizes from the metrics sheet; critical jumps in the safe band by script; drops classified consistently; AI navigable |
| 7 | Long replay before hard beats; unattributable deaths | Checkpoints present but one hard beat exceeds the replay budget; mandatory peak harder than optional | Replay budget met; checkpoint before every high-death beat; mandatory content easier than optional; ≥2 approaches per encounter; fun checks pass |
| 8 | Interactables blend into dressing | Consistent language with exceptions; no precious list yet | Consistent affordance language; precious/flexible list; greyscale test passes; post-art re-check done |
| 9 | Mandatory flashing above threshold, or critical info by fixed colour or sound alone | Second channel on most cues; hooks partly authored | Checklist passes; assist hooks authored per space; level completable with assists on; flashing within XAG 118 |
| 10 | Purely decorative | Vignettes exist but sit off-path or unlit | "What happened here" readable from ≥3 props on or framed from the critical path |
| 11 | Unbounded bespoke content; no cut plan | Scope roughly fits; perf zones vague | Kit coverage stated; streaming and occlusion zones marked; cut list ordered by cost/value |
| 12 | "Playtest it and see" | Hypotheses exist but lack thresholds or events | Hypothesis card per risky beat with metric, sample, threshold, fail action and named events |

1 and 3 sit between the anchors: 1 = closer to 0 than to 2 (a real problem most players will hit); 3 = closer to 4 with minor issues.

## 5. Computing the score and the gate verdict

1. Score each criterion required at this gate. A **U on a required criterion scores as 1** in the arithmetic (it is not a pass) and must also appear as a hypothesis card. A U on a blocker at a gate that requires it means Rework until a script or trace answers it.
2. Exclude criteria not required at this gate; list them as "deferred to G2".
3. **Weighted score** = 100 × Σ(weight × score ÷ 4) ÷ Σ(weights of scored criteria). Report the coverage (Σ weights scored, out of 100).
4. **Verdict** [convention]:
   - **Pass:** score ≥ 75 and no criterion below 2.
   - **Pass-with-conditions:** score 60–74, or any criterion at 1 (including U-as-1). List each condition as a fix or a hypothesis card with a deadline gate.
   - **Rework:** score < 60, or any blocker at 0–1.
5. Show the arithmetic in one line so the user can check it.

Example (G1 paper, coverage 90): scores 1:3, 2:4, 3:2, 4:3, 5:3, 6:3, 7:U→1, 9:2, 11:3, 12:2. Weighted = 100 × (7.5+10+5+6+7.5+6+2.5+5+6+3) ÷ 90 = 65.0 → **Pass-with-conditions** (score 60–74 and criterion 7 is U; conditions: second cue at the weak decision for criterion 3, H3 death-rate card at G2).

## 6. Self-review loop

After producing an artefact, before replying [convention]:
1. **Run the machine checks first** (lint, solve/reach/graph, `beat_lint.py`); their output is evidence for criteria 2, 4, 6.
2. **Score** every required criterion with one line of evidence each. Be a conservative critic: flag only issues you can point to, and treat your own design with the same suspicion as a user's. Don't raise a score because the intent was good.
3. **Fix** every blocker at 0–1, then cheap fixes for any criterion at 1 (a cue, a checkpoint, a rest beat, a hook). Show each fix as a diff (`process.md` §10).
4. **Re-score.** Stop after **2 loops**. Remaining issues go to the user as conditions; unknowns become hypothesis cards.
5. Report before → after briefly ("71 → 78; fixed: 2nd cue at fork F2, checkpoint before beat 7").

Never let self-review rewrite the design into something the user didn't ask for; fix what fails, keep what works.

## 7. Review report format

1. **Header:** level, stage, gate, what evidence was reviewed (and what was missing).
2. **Score table:** criterion, weight, score (0–4 or U), one-line evidence.
3. **Arithmetic, coverage and verdict.**
4. **Blockers** (if any), then **top 3 issues** in the critique format of `playtesting-and-critique.md` §1 (Evidence / Player impact / Fix / Cost).
5. **Conditions to pass** (Pass-with-conditions only), each tied to a criterion and a gate.
6. **U items → hypothesis cards** (`assets/hypothesis-card.md`), with their method: paper/script, small playtest, or telemetry at scale.
7. **What works** (so revisions keep it) and the need-satisfaction verdicts from `fun-checks.md`.

## 8. Compact output template

Use this full template when the user asked for a review or a gate verdict. When you are self-reviewing your own design, fix what the rubric finds and report only the verdict and the open conditions in one or two lines (details in an appendix if at all): scores are a tool for you, not the deliverable.

```
## Review — <level> · <stage> · Gate G<n>
Evidence reviewed: <brief, graph, beat chart, script output…>; missing: <…>

| # | Criterion | W | Score | Evidence |
|---|---|---|---|---|
| 1 | Intent, pillars, gameplay-first | 10 | 3 | grey description has 3 decisions; space S4 has no verb |
| … | … | … | … | … |

Score: 100 × (<terms>) ÷ <coverage> = <NN> (coverage <C>/100)
Verdict: Pass | Pass-with-conditions | Rework
Blockers: <none | list>
Top issues: 1. … 2. … 3. … (Evidence / Player impact / Fix / Cost)
Conditions: <criterion → fix or card → gate>
Unknowns (U): <card ids>
Keep: <what works>
Self-review: <before> → <after>; fixes: <diffs>
```

## 9. Review checklist

- [ ] Machine checks run before scoring; their output cited
- [ ] Every required criterion scored with one line of evidence; scores of 3–4 cite artefacts
- [ ] U used for anything only a playtest can answer; no U counted as a pass
- [ ] Blockers checked first (1, 2, 6, 9-flashing)
- [ ] Weighted score, coverage and arithmetic shown; verdict follows §5 exactly
- [ ] Self-review stopped at 2 loops; fixes shown as diffs; before → after reported
- [ ] Each U and condition has a hypothesis card or a named fix and gate
- [ ] What works is listed
