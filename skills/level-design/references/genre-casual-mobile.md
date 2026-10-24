# Casual and Mobile Level Progression (Match-3, Physics Puzzlers)

## Contents
1. The curve is the deliverable
2. King's four pillars, per level
3. Level anatomy: board, goal, blockers, move limit
4. Define your metrics before you set targets
5. The difficulty curve: sawtooth, hard slots, relief
6. Hard slots are retention risks (the level 65 lesson)
7. Introducing mechanics across hundreds of levels
8. Simulate before people: bots plus a player population
9. Physics puzzlers: build fast, tune the stars slowly
10. Producing hundreds of levels: templates, data, pruning
11. Common failures → fixes
- Review checklist
- Levels to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

This guide covers designing and tuning *sequences* of short levels with live data. For the craft of a single puzzle (insight, fairness, verification) use `puzzle-craft.md`, `puzzle-sequencing.md` and `puzzle-verification.md`; this file does not repeat them.

---

## 1. The curve is the deliverable

- **One level is one data point on a curve.** When asked for "a level", also say where it sits (level number, slot type, what precedes and follows it) and what pass rate it targets. A great level in the wrong slot is a bad level.
- **Judge changes across the whole progression.** King's designers argue for looking at "the impact and the ripple effects that change might have for the whole progression… and be prepared for long A/B tests" (Guardiola and Wedekind, GDC 2024, via Mobilegamer.biz).
- **Disentangle difficulty from fun.** Wedekind "urged designers to disentangle difficulty from fun" (same source). A hard level is not automatically a good one; a dull level is not fixed by making it harder.
- **Setback cost is the casual contract.** Juul identifies casual games' appeal as "sparing use of setback punishment"; keep retries instant and failure attributable (see `fun-checks.md`).
- **Gameplay first:** prototype a board in the editor with placeholder tiles; if the level's idea doesn't read in grey, theming won't save it.

## 2. King's four pillars, per level

Jeremy Kang (King, GDC Europe 2016, via PocketGamer.biz): "A game then needs to be broken down into four different concepts: difficulty, rhythm, flow and hooks."

| Pillar | King's wording | What you write for each level |
|---|---|---|
| Difficulty | "keep giving players challenges throughout their progression" | Slot type and target pass rate (§4–5) |
| Rhythm | "varying the experience to keep them entertained" | How it differs in pace or goal from the previous 3 levels [convention] |
| Flow | "how to keep players moving toward their goal, sometimes through the use of hints" | Where the player's eye goes first; what hint fires if stuck |
| Hook | "how to ensure one level is different from another, perhaps with a twist on previous gameplay mechanics" | The one twist this level adds |

King's process "typically starts from paper, before going to the level editor and onto play testing", and "The loop of testing and balancing goes on forever."

## 3. Level anatomy: board, goal, blockers, move limit

- **Board shape** controls where matches can happen and where cascades fall; shape is the first lever on difficulty and the cheapest variety [convention].
- **Goal type** [convention]: score, clear layers (jelly), drop items to the bottom, collect N of a colour, clear blockers. Royal Match-style goals and obstacles (locked tiles, multi-layer ice, portals, spreading hazards) are described in third-party analyses [unverified].
- **Blockers are enemies.** King's Lucien Chen describes designing blockers by analogy to RPG enemies, with goals to slow progression, stop wins and raise difficulty, and a stats-based blocker analysis shared across studios (GDC 2020) [unverified: snippet]. Give each blocker a stat line: layers (HP), spread behaviour (punishes passivity), what clears it, what it protects.
- **Move limit is the main tuning knob** [convention]; blocker layers and spread rate are the second. Change one knob at a time when re-tuning.
- **Readability.** Every blocker's state (layers left, countdown, spread next turn) must show on the tile, not in a tooltip, and not by colour alone (`accessibility.md`).

## 4. Define your metrics before you set targets

Published targets use undefined metrics. devtodev reports "some developers set the difficulty of easy levels at 30-40% and difficult levels at 80-85%, other developers strike balance at 50-60% for easy levels and 90-95% for difficult ones… the best way to find it is to run A/B tests"; its "difficulty" is most likely a failure share of attempts, but the page never defines it [unverified: metric]. Quote those bands as "reported studio practice, metric undefined". Use these definitions instead, and state them in every spec [convention]:

| Metric | Definition | Note |
|---|---|---|
| Pass rate | wins ÷ attempts, over all players on the level | Population-level |
| Fail share | losses ÷ attempts = 1 − pass rate | What "difficulty %" usually means |
| Attempts-per-win | attempts ÷ wins = 1 ÷ pass rate | Skewed by heavy players |
| Attempts to first win | per-player distribution; report median and 90th percentile | Shows the tail that churns |
| Level churn | share of players whose last play (within a fixed window) was this level | Fix the window, e.g. 7 days |
| Near-miss | moves or targets short on a loss | devtodev lists "how many more moves are needed to win" |

devtodev's other indicators: "the number of attempts needed to pass a location… churn rate; how many gamers spend money."

## 5. The difficulty curve: sawtooth, hard slots, relief

- **Mostly easy, then spikes.** devtodev: "the majority of game levels should be easy, but after a number of easy levels should follow one or some very difficult levels."
- **Sawtooth** [convention]: a rising trend broken by drops that give a breather. A blog puts each tooth at about 5–15 levels [unverified]; claims that sawtooth curves retain players 20–40% longer rest on unpublished data and should not be quoted [unverified].
- **Slot types** [convention]: relief (just after a spike), normal, hard, super-hard. Define a target band per slot from your own data; fix the spacing per chapter (a public clone copies a Royal Match pattern of a hard level at 5 and a super-hard at 10 in each 10-level chapter [unverified]).
- **Signpost hard slots.** Candy Crush and Royal Match label "Hard" and "Super Hard" levels [unverified]; the label tells the player failure is expected, which matches the stance that hard content should be signposted (`fun-checks.md`).
- **Compare projected to real.** Playrix designs against a projected difficulty curve and compares it with player results: "where the curves diverge, there is likely to be a problem" (Game World Observer, 2019) [unverified: snippet].

## 6. Hard slots are retention risks (the level 65 lesson)

Guardiola and Wedekind (King, GDC 2024, via Mobilegamer.biz): level 65 "was originally intended to be the final stage of the game. It was too hard, and as a result it became both the highest converting level in the game and the stage that has 'made the most revenue ever'… But it has also caused the most player churn." And: "increasing difficulty raised conversions short term. Over the long run, though, making the level easier retained players longer."

- **Treat every hard slot as a churn risk first and a conversion lever second.** Its success measure is long-run retention, not booster sales that week.
- **Long A/B tests.** Short tests reward conversion; churn shows later. Run tests long enough to see retention, and read them across the following levels.
- **Avoid hard walls early in the progression** [convention], where players have the least investment.
- **Prune.** King prunes and replaces poor levels (Mobilegamer.biz). Levels with outlier attempts-per-win or churn are retuned (move count first) or replaced [convention].

## 7. Introducing mechanics across hundreds of levels

- **Introduce → test → twist → combine** [convention], the same arc as Hayashida's teach → develop → twist → conclude (`principles.md`), stretched across a chapter.
- **The introduction level is low-pressure** [convention]: generous moves, the new blocker placed where the first natural match touches it.
- **One new element per chapter or block** [convention]; re-teach after a long gap. For sequencing tools (tiers, priming, airlocks), see `puzzle-sequencing.md`.
- **Rhythm across levels.** Alternate goal types and board shapes so consecutive levels feel different even at equal difficulty (King's rhythm pillar).

## 8. Simulate before people: bots plus a player population

- **Bots predict pass and churn per level.** Roohi et al. (Aalto University and Rovio, CHI PLAY 2020) predict "per-level churn and pass rates of Angry Birds Dream Blast". Their "primary contribution is to combine AI gameplay using Deep Reinforcement Learning (DRL) with a simulation of how the player population evolves over the levels… with simulated skill, persistence, and boredom." The population model matters: a bot's pass rate alone is not a human pass rate.
- **Use best-case runs.** The follow-up (CHI PLAY 2021) found that "enhancing DRL with Monte Carlo Tree Search" helps and "an AI agent's best-case performance can yield stronger correlations with human data than the agent's average performance."
- **Earlier work** [unverified: details]: King trained a CNN on human play to predict match-3 difficulty (Gudmundsson et al., 2018); MCTS has been used to predict average human pass rates (Poromaa, 2017).
- **Calibrate to humans** [convention]: fit the bot-to-human mapping on levels with live data, then use it on new levels. Re-fit when mechanics change.
- **Bundled scripts don't simulate match-3 or physics.** Say so; label difficulty claims "predicted by [your bot]" or "designer estimate", never as fact. For deterministic grid puzzles, `grid_puzzle_solve.py` applies (`puzzle-verification.md`).

## 9. Physics puzzlers: build fast, tune the stars slowly

Arttu Mäki (Rovio) on making an Angry Birds level (Pocket Gamer interview; about 15 years old):

- **Six steps:** theme → birds → building → star ratings → playtest/QA → golden eggs. "Rovio chooses its birds before its buildings": the tools the player gets decide the structure.
- **One designer per level:** "Level design in this case is always done by one individual."
- **Thresholds cost more than building:** "We spend more time developing and tweaking the ratings than building the level." Star thresholds are "usually an average from a score that can be achieved with a certain skill shot or method."
- **Testing:** "In total, 5-10 different people test the level multiple times."
- **Separate completion from mastery** [convention]. Lenient completion, demanding three stars; Cut the Rope's three collectible stars per level work the same way [unverified]. Budget tuning time for the thresholds, not the layout.
- **Physics variance** [convention]: the same shot varies, so set thresholds with a margin and test the intended skill shot many times. Solvability tools exist for Cut the Rope (Ropossum) and Angry Birds-style generation (Stephenson and Renz) [unverified: capabilities].

## 10. Producing hundreds of levels: templates, data, pruning

- **Levels are data** [convention]: board, goal, move limit, spawn weights, blocker placement and slot type in one file per level, so tuning never touches code.
- **Templates with different mixes** [convention]: reuse board shapes with different goal and blocker combinations; vary at least two of board, goal and blocker set between neighbours.
- **Catch near-duplicates.** For grid boards, run `python3 -I scripts/level_metrics.py new.txt --legend puzzle --compare old1.txt old2.txt`; it flags near-identical layouts (Hamming and structural distance). It does not judge difficulty.
- **Pipeline** [convention]: paper → editor → bot simulation → internal playtest → soft launch → live A/B → retune or prune. Record each level's target and measured metrics side by side.
- **Seed control** [convention]: if starting boards or refills are random, check that no seed is unwinnable at the move limit (bot runs across many seeds), and cap the spread of outcomes per seed.

## 11. Common failures → fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Churn spike at one level | Hard wall, especially early | Ease it; long A/B test on retention, not conversion |
| Players "lose for no reason" | Random seeds unwinnable; blocker state unreadable | Seed checks with bots; show layers and countdowns on tiles |
| Levels blur together | Same goal and board repeated | Vary goal type and board shape; one hook per level |
| Live pass rate far from predicted | Bot not calibrated, or population effects ignored | Fit bot-to-human mapping; model persistence and boredom |
| Star thresholds feel random | Set from one lucky run | Average over a repeatable skill shot; add margin; 5–10 testers |
| Targets nobody can compare | Metric undefined | Use the §4 definitions in every spec |

## Review checklist

- [ ] Level's slot (number, type, neighbours) and target written down; the curve, not the level, is reviewed
- [ ] Four pillars filled in: difficulty target, rhythm contrast, flow/hint, hook
- [ ] Every blocker has a stat line and readable on-tile state (not colour alone)
- [ ] Metrics defined (pass rate, fail share, attempts-per-win, attempts-to-first-win, churn window)
- [ ] Sawtooth spacing set per chapter; relief level after each spike; hard slots labelled
- [ ] Hard slots judged on long-run retention; no hard wall early in the progression
- [ ] New element introduced in a low-pressure level, then tested, twisted and combined
- [ ] Difficulty claims labelled: bot-predicted (with calibration) or designer estimate
- [ ] Physics levels: completion and mastery separated; thresholds from a repeatable skill shot
- [ ] Random seeds checked for unwinnable starts
- [ ] New boards compared with `level_metrics.py --compare` against neighbours
- [ ] Retries instant; loss screen shows how close the player came

## Levels to study

- **Candy Crush Saga:** level 65 as the canonical conversion-vs-churn case; episode structure for mechanic introduction [convention].
- **Candy Crush Soda Saga:** blocker design as enemy design (Chen, GDC 2020) [unverified].
- **Royal Match:** labelled hard and super-hard slots within chapters [unverified].
- **Angry Birds:** early levels for "birds before buildings" and star thresholds.
- **Cut the Rope:** themed boxes with one new object each and three-star mastery [unverified].
