# Fun Checks

## Contents
1. What fun checks are, and are not
2. Evidence labels and the wording rule
3. The check table
4. Resolving tensions between checks
5. Running the checks on a beat chart
6. The grey description test (run first)
7. Need-satisfaction verdicts
8. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

---

## 1. What fun checks are, and are not

There are no validated numeric thresholds for "fun" on paper. What the evidence supports is a set of **directional** checks: autonomy is the strongest measured predictor of enjoyment, mandatory content should be easier than designers expect, hard content should be chosen, big contests should end close, and failure should be cheap and readable. Run these checks on every design and every critique, before claiming a level is fun. They catch likely problems; they do not prove fun. The playtest is the truth.

Controls and metrics are necessary but not sufficient: intuitive controls are "the gatekeeper to experience, and not the experience itself" (Ryan, Rigby & Przybylski, *Motivation and Emotion*, 2006).

## 2. Evidence labels and the wording rule

Each check below carries one of these labels:
- **measured:** controlled or large-sample studies support the *direction* (not a number).
- **one study:** a single small or correlational study.
- **heuristic:** a published model with weak validation (GameFlow, MDA, Lazzaro).
- **practitioner:** developer or designer practice.
- **theory:** derived from a theory, not tested at level scale.

**Wording rule** (follow it in every output):
1. Only these may be introduced as "research shows": close contests (#3), assigned-vs-chosen difficulty (#4), early success for newcomers (#5), autonomy as the strongest enjoyment predictor (#7), moderate novelty (#11), and the PENS need-satisfaction summary (§7).
2. Juul-based checks (#1, #2, #6) say "one player study suggests".
3. Everything else is "practitioner guidance" or "a heuristic".
4. Every number is a tunable default [convention]; say so when you use one.
5. Don't repeat these errors: "players rate games higher if they fail at least once" (a non-significant trend, p = 0.06); Lazzaro's keys as "Hard / Easy / People / Serious" or "three keys within 20 minutes"; the To et al. "closable gap" quote as 2016 video-game evidence (it is a 2018 tabletop study).

## 3. The check table

Compute each check on the brief, bubble diagram and beat chart. Report every flag with the beat number and a fix.

| # | Check | Compute on the design | Flag when | Evidence |
|---|---|---|---|---|
| 1 | Attributable failure | Each fail element: telegraphed before it hurts, perceivable when it matters, avoidable by a taught skill | Any element fails one of the three | one study (Juul, n = 85, self-reported, correlational: players "prefer feeling responsible for failing"); heuristic (GameFlow: "supported in recovering from errors") |
| 2 | Setback cost | Seconds of already-mastered play replayed per failure, per beat; expected cost = P(death) × replay (McMillen: P(death) × penalty = difficulty) | Long replays of mastered content before a hard beat; expected cost > 10 s [convention] | one study / theory (Juul: casual appeal is "never… having to mechanically replay a game sequence"); practitioner (Chen's flOw "minimal death penalty") |
| 3 | Close contest | Expected outcome per set piece for a typical player | "Trivial" or "likely wall"; target a narrow win | measured (Abuhamdeh & Csikszentmihalyi 2012: close games and stronger opponents more enjoyable; Lomas et al. 2017, suspense in close games) |
| 4 | Mandatory vs optional difficulty | Critical-path peak vs optional peak; is hard content opt-in and signposted with an honest forecast? | Critical-path peak ≥ optional peak; hard content unsignposted; skipping it feels like failing | measured (Lomas 2017, n = 10,472: moderate difficulty best when self-selected, easiest best when assigned; Lomas 2013; Klimmt 2009) |
| 5 | Early success | Successes and expected deaths in the game's first section and in each new mechanic's first section | Expected deaths > 1 [convention] or few visible successes there | measured (Klimmt 2009: new players "heavily depend on visible success"; Lomas 2013: easier games played longer) |
| 6 | Earned struggle | At least one beat per level where struggle precedes success (frustration → triumph); most players overcome it | None, or placed inside onboarding | heuristic (Lazzaro, Hard Fun); one study (Juul, p = 0.06 trend only) |
| 7 | Choice density | Longest critical-path stretch with no route, approach, risk or order choice | > 120 s [convention] | measured direction (Ryan 2006: autonomy β = .49 vs competence .24 for enjoyment, n = 730); number [convention] |
| 8 | Strategies per encounter | Viable approaches per major encounter or puzzle room | < 2 [convention] | heuristic (GameFlow: "free to play the game the way that they want"); theory (Ryan: "flexibility over movement and strategies") |
| 9 | Risk/reward visibility | Before each optional risk: reward visible, difficulty forecast honest | Hidden reward or misleading forecast | practitioner (Taylor #7: "clearly called out using the level's language"); theory (Lomas 2013 "feedforward") |
| 10 | Forced slowdowns | Forced walks, walk-and-talks, waits for doors or VO, long lifts | Any not justified as a rest or story beat | practitioner; heuristic (GameFlow: tasks that "don't feel important"; PENS reversed item "controlled and pressured") |
| 11 | Novelty cadence | Brand-new concepts per beat; stretches with nothing new | ≥ 2 brand-new concepts in one beat; ≥ 3 flat beats [convention] | measured direction (Lomas 2017, n = 5,065: moderate novelty optimal, in an educational game; Lomas 2013: less repetition, more engagement) |
| 12 | Re-contextualised core loop | Contexts per core verb (space, height, enemy mix, combination); loops at 3 s / 30 s / 3 min | A verb used in one context; a 30 s stretch that repeats | practitioner (Griesemer: "No 30 second stretch of Halo is ever repeated") |
| 13 | Develop what you introduce | Each introduced mechanic is developed, twisted and reused | Introduced then dropped | practitioner (Hayashida); theory (Koster: games teach patterns; Crawford: fun is "the emotional response to learning") |
| 14 | Curiosity hooks | Visible-but-unreached spaces (vistas, ledges, locked doors, sounds); can the player tell *that* and roughly *how* each becomes reachable? Is each paid off? | No hint of access, or never paid off | theory (To et al. 2016: tolerance depends on "confidence in their ability to close it"; give warm/cold feedback) |
| 15 | No empty dead ends | Payoff per branch (reward, vista, story, shortcut) | Any branch with none | practitioner; heuristic (GameFlow: "rewarded appropriately for their effort") |
| 16 | Return trips change | New route, traversal method, enemy mix or state on each revisit | Identical revisit | practitioner (Taylor #8, "key modifier on the second pass") |
| 17 | Loop-back shortcuts | Route back to hub or checkpoint after long excursions | Walk back through cleared content | practitioner (FromSoftware); consistent with check 2 |
| 18 | Goal clarity | One-sentence current goal per beat | You can't write it | heuristic (GameFlow: goals "clear and presented early… at appropriate times") |
| 19 | Feedback coverage | Every action, progress step and state change signalled | Silent state changes (a door opening off-screen, a switch with no response) | heuristic (GameFlow: "immediate feedback on their actions") |
| 20 | Cognitive load | New mechanics taught in low-threat space; new items at once | Teaching under threat; > 3 new items at once | heuristic (GameFlow; Hodent: "don't punish while teaching", ≤ 3 new items in learning mode) |
| 21 | Metrics-driven geometry | Sizes derived from avatar metrics; spaces that show off the best verbs; no snag collision | Eyeballed sizes; no showcase space | practitioner (Swink, *Game Feel*: "context"); one study (Ryan: controls are a gatekeeper) |
| 22 | Experience mix | Beats tagged with MDA aesthetics (sensation, fantasy, narrative, challenge, fellowship, discovery, expression, submission; non-exhaustive) or Lazzaro's 2004 keys (Hard Fun, Easy Fun, Altered States, The People Factor) | One aesthetic or key across a whole level when the brief wants breadth | heuristic (MDA 2004; Lazzaro 2004: best-sellers analysed hit "at least three of the Four Keys"; apply at level or game scale, no time window) |

## 4. Resolving tensions between checks

- **Early success (#5) vs earned struggle (#6) vs close contest (#3):** resolve by *position*. Easy and frequently successful at the start and wherever difficulty is assigned; struggle and narrow wins after onboarding, preferably in content the player chose.
- **Optional challenge is not automatically good.** In an A/B test reported by Lomas 2013, optional "bonus coins" had "a strong negative effect on engagement". So signpost optional hard content with an honest difficulty forecast, and never let skipping it make the main path feel incomplete.
- **Choice (#7, #8) vs pacing control:** linear set pieces are fine; keep them short and bracket them with choice.
- **Novelty (#11) vs develop-what-you-introduce (#13):** one new concept per beat at most, then development beats that add a variable rather than a new concept.

## 5. Running the checks on a beat chart

Use the extended beat-chart columns so the checks can be counted, not eyeballed. `scripts/beat_lint.py` reads a markdown table with these headers (any order, extra columns ignored): `#`, `Beat`, `Intensity` (1–5), `New concepts`, `Expected deaths`, `Replay cost` (seconds), `Checkpoint`, `Duration` (mm:ss), `Choice` (y/n).

Run from the skill root: `python3 -I scripts/beat_lint.py beats.md` (add `--json` for machine output). It checks, with [convention] defaults you can override (see `--help`): rest (≤ 2) before and after each peak (≥ 4); no more than 2 consecutive beats at ≥ 4; new concepts per beat (warn at 2, fail at 4); no-choice stretches over 120 s; expected setback P(death) × replay ≤ 10 s, with P ≈ deaths / (deaths + 1); peak intensity not on the peak replay cost; a checkpoint before every beat with expected deaths ≥ 2; flat stretches of 3+ beats. Report its output verbatim. If the script is unavailable, hand-check and label the result "hand-checked, not machine-verified".

Example (grapple level, hand-checked, not machine-verified):

| # | Beat | Intensity | New concepts | Expected deaths | Replay cost | Checkpoint | Duration | Choice |
|---|---|---|---|---|---|---|---|---|
| 1 | Survey quarry from ledge | 1 | | 0 | 0 | C1 | 0:40 | n |
| 2 | Grapple over safe gap | 2 | grapple | 0 | 5 | | 1:20 | n |
| 3 | Chain hooks, side-ledge reward | 2 | | 0.5 | 10 | | 1:30 | y |
| 4 | Ring-arena ambush | 4 | | 1 | 40 | C2 | 2:30 | y |
| 5 | Camp rest, lift shortcut | 1 | | 0 | 0 | | 1:00 | n |
| 6 | Hooks on moving cranes | 3 | moving hooks | 1 | 15 | | 2:00 | n |
| 7 | Tower climb under fire | 5 | | 2 | 90 | | 1:40 | y |
| 8 | Summit vista | 1 | | 0 | 0 | C3 | 0:30 | n |

Flags: beat 4 setback 0.5 × 40 = 20 s > 10 s (fix: checkpoint at the arena door, replay 15 s → 7.5 s). Beat 7 setback 0.67 × 90 = 60 s, peak intensity on peak replay cost, and no checkpoint before a beat with 2 expected deaths (fix: checkpoint at the tower base, replay 12 s → 8 s). Beats 5–6 run 180 s without a choice (fix: high and low crane routes). Beat 7's peak follows a 3, not a rest (fix: a short ledge rest between 6 and 7).

## 6. The grey description test (run first)

Gameplay first: if a level is only interesting once its art is described, the layout is not done. Rewrite the level summary with **no materials, lighting, props or mood adjectives**: only spaces, sizes, heights, connections, verbs, threats, rewards and decisions. Then ask: are there decisions, variation and surprises? If not, fix the layout before discussing art [convention: no validation study; supported in spirit by Valve's "Just because you were sure something was going to be fun didn't make it so" (Birdwell, "The Cabal") and TLDB's "99% of the time, your blockout will not survive a playtest"].

- *Before:* "A moonlit cathedral of shattered stained glass where the player duels cultists among candlelit pews."
- *Grey:* "A 40 × 20 m hall, two floor planes (0 m, 6 m) joined by one ladder; five ranged enemies on the 6 m balcony; one route through."
- *Verdict:* one route, one decision, height used only against the player. Fix: a collapsed pillar as a second way up, a 4 m committed drop from the balcony onto a flank, and a side chapel reward visible from the balcony.

Pair it with the verb-per-space table and precious/flexible list (`process.md`). **Exception:** when the core experience is mood, story or place (Firewatch's greybox "did not answer any of the important questions"; Untitled Goose Game's village), say so and test the cheapest representative slice instead.

## 7. Need-satisfaction verdicts

End every design review and critique with a short forecast phrased in PENS item wording (Ryan et al. 2006). It is a prediction from the paper design, not a measurement; confirm it in playtests (`playtesting-and-critique.md`).

```
Need-satisfaction forecast (paper design, not measured)
- Competence: met / at risk / not met. Would a typical player say "I felt very capable and effective"
  and "the game kept me on my toes but did not overwhelm me"? Basis: checks 1–6, 20–21.
- Autonomy: met / at risk / not met. Would they say "I did things in the game because they interested me",
  and not "I felt controlled and pressured to be a certain way"? Basis: checks 7–10, 14.
- Relatedness (multiplayer, co-op, companions) or Presence (single-player): met / at risk / not met. Basis: ...
- Biggest risk and the one change that most improves it: ...
```

Relatedness evidence comes from an MMO survey, so apply it mainly to multiplayer and companion content. Presence rose with autonomy and competence, so judge it from those plus control feel.

## 8. Review checklist

- [ ] Grey description test run; the level is still interesting without art words (or the mood/place exception is stated)
- [ ] Every fail element telegraphed, perceivable and avoidable by a taught skill
- [ ] Setback cost per beat computed; checkpoint before every beat with ≥ 2 expected deaths
- [ ] Critical-path peak below the optional peak; optional hard content signposted with a difficulty forecast
- [ ] First section of the game and of each mechanic gives frequent visible success
- [ ] Set pieces forecast as narrow wins, not trivial or walls; one earned-struggle beat after onboarding
- [ ] No critical-path stretch over ~120 s without a choice [convention]; ≥ 2 strategies per major encounter
- [ ] At most one brand-new concept per beat; no flat stretch of 3+ beats
- [ ] Each core verb appears in several contexts; 3 s / 30 s / 3 min loops all vary
- [ ] Curiosity hooks hint at how they become reachable and are paid off
- [ ] No empty dead ends; revisits change; shortcut home after long excursions
- [ ] One-sentence goal per beat; every action and state change has feedback
- [ ] Beats tagged by MDA aesthetic or Lazzaro key; mix matches the brief
- [ ] `beat_lint.py` output reported verbatim, or results labelled "hand-checked, not machine-verified"
- [ ] Wording rule followed; every number labelled a tunable default
- [ ] Review ends with competence / autonomy / relatedness-or-presence verdicts in PENS wording
