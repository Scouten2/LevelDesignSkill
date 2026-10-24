# Puzzle Sequencing: Curricula, Tiers, Hints and Dependency Charts

## Contents
1. Sequencing is a separate skill
2. Checklisting
3. The per-mechanic curriculum
4. Knowledge tiers: parallel within, linear between
5. Priming leaps from a distance
6. Airlocks, breaks and re-teaching
7. Hint ladders and escape valves
8. Dependency charts
9. Pacing difficulty across a game
10. How many mechanics, how many puzzles
11. Sequence table template
12. Review checklist

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Single-puzzle design: `puzzle-craft.md`. Verifying and playtesting: `puzzle-verification.md`. General teaching theory (Hayashida, Hodent): `principles.md`.

---

## 1. Sequencing is a separate skill

- Valve: Portal "is effectively an extended player training exercise… introducing a series of gameplay tools, then layering these tools into increasingly difficult puzzles."
- Traynor: "I learned to treat puzzle management as a skill." His five tools for smoothing a curve: **insert, modify, delete, reorder, optionalize**. He used them to patch conceptual leaps, give "a second chance to learn" and manage playtime (GDC 2024).
- A good puzzle in the wrong slot is a bad puzzle. Before placing any puzzle, know what each player already knows when they reach it. That is what tiers (§4) and dependency charts (§8) are for.

## 2. Checklisting

Valve's term (Game Informer, 2010): break a mechanic into its core facts and give each one "a very clean room to safely experiment."
1. Write the checklist. Portal example: portals come in pairs; either colour is an entrance and an exit; momentum is conserved through a portal; portals only go on certain surfaces.
2. Give each fact a room where it is the only unknown.
3. **Gate it** so stumbling fails. Portal's Chamber 01: "stumbling around will virtually always lead to a dead end… a minimum of five portals in a specific order."
4. **Block bypasses of the lesson.** When testers skipped Chamber 04's box-and-button lesson, Valve added a glass barrier. "For training purposes, there's generally just one correct solution to these early puzzles."
5. **Make the first one impossible to fail.** Parabox World 1 level 4 makes it "impossible to mess up the solution, ensuring you learn the behaviour" (fan analysis).

## 3. The per-mechanic curriculum

Hayashida's four steps (*Super Mario 3D Land* interview, 2012): introduce → develop → twist ("ten", "a doozy that throws them for a loop") → conclude, with "a clear concept in the beginning, and that's carried through absolutely all the way". Valve's twists "usually involve taking a previously learned rule and turning it on its head." For puzzles, expand to slots:

| Slot | Job | Solution classes | Example signal |
|---|---|---|---|
| Introduce (checklist) | One fact, safe, unfailable | 1 | Player can state the fact afterwards |
| Gate | Fact must be used; stumbling fails | 1 | Bypass test fails (`puzzle-verification.md` §4) |
| Develop | Repeat or vary to make it stick | 1–2 | Parabox level 6 repeats the new move 4 times "to reinforce the idea" |
| Combine | Join with an earlier mechanic | any | Both rules appear in the solver's "rules used" |
| Twist | A learned rule turned on its head | any | Counter-intuitive move present |
| Conclude / side | Show mastery; hardest ideas optional | any | Off the critical path |

- **One new concept per puzzle.** Portal's Chamber 08 "introduced too many new concepts at once", so Valve inserted two chambers before it. Hodent's general cap is at most 3 new items in learning mode; for puzzles, keep it to 1 [convention, consistent with Valve's fix].
- **"Overwhelmed players tend not to digest new information"**: Valve cut a later chamber down to the double fling alone.
- **Accidental solves:** acceptable only if the next puzzle forces the same concept (Traynor). Otherwise tighten the puzzle.
- **Combine before twist** unless the twist is about one mechanic alone. Order the twist after players have *used* the rule several times, or there is nothing to overturn.
- Run the slots per mechanic, then interleave mechanics (§4). You can lint the order: write the sequence as a beat chart with a `New concepts` column and run `python3 -I scripts/beat_lint.py sequence.md`.

## 4. Knowledge tiers: parallel within, linear between

Two verified lessons pull against each other:
- **Parallelism rescues stuck players.** Gilbert: think of "the player as outside the cages, and the puzzles as locked up within… If the solution to one puzzle stumps her, she can go on to another." Falstein: "Make it Bushy." Day of the Tentacle peaks at 13 simultaneously open puzzles.
- **Linearity guarantees prior knowledge.** Valve's Portal 2 co-op hub began flat ("if they got stuck… they could pick another test chamber"), but "this prevented us from doing sufficient training… By going linear, we could guarantee prior knowledge."

**Synthesis: parallel within a knowledge tier, linear between tiers** [convention, derived from both]. A tier is a set of puzzles with the same prerequisite knowledge.
- Within a tier offer 3+ parallel puzzles [convention] and gate the next tier on N of M solved [convention]. Precedents: Talos doors need sets of sigils; Layton opens areas after "a certain number of puzzles"; The Witness runs linear panel chains inside regions while regions are parallel.
- A tier gate must check knowledge, not count: the gating puzzle uses the tier's core fact (§2 step 3).
- SSR is the strict end: each section must be finished before moving on. Choose strictness from the stance (`puzzle-craft.md` §2).

## 5. Priming leaps from a distance

The most counter-intuitive Valve finding. For the Portal 2 co-op's "trickiest logical leap", adding a stepping-stone puzzle right before it "significantly reduced the average solution time… but this almost completely robbed the appeal." Instead Valve placed a teaching puzzle **four chambers earlier** to "subconsciously prime" midair collision, and laid out the leap room "so that players would see the entire space as a symmetrical whole": "By planting shards of the idea in their heads, we allow players to own that exciting dual collision epiphany."

Rules:
- Mark protected leaps on the card (`assets/insight-card.md`) and never put a stepping stone directly before one.
- Prime the component idea several puzzles earlier (Valve used 4; [convention] ≥3), ideally in a different context and without asking the player to use it yet.
- Pre-teach in a different context when players fixate: Portal 2 fixed an excursion-funnel fixation with a destruction event that pre-teaches the floor-to-wall move "in a different context".
- Don't over-explain new ideas. Blow: explaining immediately "kills epiphany and related things like the joy of discovery."

## 6. Airlocks, breaks and re-teaching

- **Airlocks.** When Portal 2 players could move freely between puzzles, "they logically assumed that the individual puzzles were part of one big puzzle. This had bad results." Separate independent puzzles with an airlock, a corridor or a clear visual boundary. If puzzles *do* share state, say so with the space.
- **Breaks.** Testers tired of "solving so many complex test chambers in a row", so Portal 2 added a funnel ride. Insert a non-puzzle beat after 2–3 hard puzzles [convention].
- **Re-teaching.** "Player training doesn't always stick, especially after the introduction of a big, new concept" (Portal Chamber 12 re-introduces flinging). After any big new concept, re-test the critical older skill within the next 1–2 puzzles [convention].
- **No time pressure while learning.** Portal 2 taught boss mechanics "a level earlier… without any time pressure"; Hodent: "DON'T PUNISH WHILE TEACHING".

## 7. Hint ladders and escape valves

Give stuck players somewhere to go. Layer these:
1. **Parallel puzzles** in the tier (§4): the cheapest valve.
2. **Hint ladder.** Layton: "Each puzzle has three hints available… the player must spend one 'hint coin' to see each hint"; the player "starts with ten" and finds more by examining the world (*Curious Village*). Rungs [convention]: restate the goal → point at the relevant element → name the false assumption → (optional) the key move. Never open with the solution.
3. **Unlock all.** Parabox borrowed an "unlock all puzzles" option from Cosmic Express.
4. **Skip / completion state** per puzzle for accessibility (TLOU Part II "SKIP PUZZLE"; `accessibility.md`).
5. **Optional layer.** Put the hardest ideas off the critical path: Parabox side levels, Talos star puzzles, The Witness's sub-1% puzzle.
6. **Live hints** in escape rooms come from a gamemaster, often limited or time-penalised.

Write in each insight card which valves apply.

## 8. Dependency charts

For multi-step puzzles, adventure games, deduction games and hubs. Gilbert's method ("Puzzle Dependency Charts", 2014):
- "I always work backwards… not from the very end of the game, but from the end of puzzle chains." Start from "the player needs to get into the basement", not "where should I hide a key".
- Shape: "Solving one puzzle should open up 2 or 3 new ones, and then those collapses down… to a single solution that then opens up more non-linear puzzles." Acts end in a bottleneck, which gives "a sense of completion" and lets "the inventory… be culled." Avoid "too linear or too unwieldy with choice."
- Use auto-layout, not hand-drawn flowcharts. Expect the chart to change "maybe 20%" over development (Gilbert, 2026). Thimbleweed Park's Act 3 "should be the shortest"; charts don't show true length, so "add a puzzle here and there, or snip a few away."
- Calibration from Day of the Tentacle: short linear intro → one node ("Find Super Battery Plans") opening 15 downstream puzzles → peak layer of 13 open at once → contracting nodes that cut branching by 1–2 → linear finale of 4. 32 cross-character dependencies make up about half the game.

**Run it.** One node per line, `id: label | needs: a, b | gives: x, y` (or JSON):
```
start: Wake in the lighthouse | gives: lobby
oil: Fill the lamp | needs: lobby | gives: lamp_oil
bar: Free the crowbar from the ice | needs: lobby | gives: crowbar
clock: Fix the clock | needs: lobby | gives: dusk
lamp: Light the lamp at dusk | needs: lamp_oil, dusk | gives: lit_lamp
cellar: Open the cellar | needs: crowbar, lit_lamp | gives: cellar
```
`python3 -I scripts/dependency_chart.py act1.txt --mermaid`. It reports cycles (errors), unreachable nodes (needs never given), topological layers with widths (how many puzzles are open at once), critical path length, bottlenecks (layer width 1 mid-chart), expanding nodes (opening ≥3) and a Gilbert check (each solve should open 2–3 [convention]). Hand-computed for this example, not script output: layers 1-3-1-1, critical path 4, `lamp` a mid-chart bottleneck, `start` opens 3.

Read the result: width-1 layers mid-act are where stuck players quit, so make them easy or give them two routes; layers wider than the player can hold in mind need a journal or inventory to track [convention]; every item node needs a reason in the fiction (Gilbert's "unconnected events"). Lock-and-key *spaces* go to `graph_check.py` instead (`grid-conventions.md` §4).

## 9. Pacing difficulty across a game

- **Rising trend with relief.** devtodev: "the majority of game levels should be easy, but after a number of easy levels should follow one or some very difficult levels." King's Candy Crush level 65 was too hard: the highest-converting level and the biggest churn source; making it easier "retained players longer" (GDC 2024). Mandatory spikes cost players; put spikes on optional content where you can.
- **Kim's band:** puzzles "too easy are disappointing; too hard are discouraging."
- **Openings.** Deduction games may "overwhelm the player initially, then give them time to get comfortable with the core loop" (Pope). Outer Wilds needs familiarity before curiosity. Choose one opening on purpose.
- **Endings.** Gilbert keeps final acts short and fast; DOTT ends in a linear run of 4.
- **Order by measured difficulty**, not designer feel: use the solver's entanglement and counter-intuitive counts to order grid puzzles, then playtest medians (`puzzle-verification.md` §7, §14). Gilbert: "It's very easy when designing to become blind to what the player doesn't know."

## 10. How many mechanics, how many puzzles

What exists (calibration, not targets):

| Game | Volume |
|---|---|
| Patrick's Parabox | 364 shipped puzzles, over 600 unused drafts, 4 years |
| The Witness | about 650 puzzles, about 80 hours |
| Baba Is You | 231 base levels |
| A Good Snowman Is Hard to Build (2014 build) | 25 levels, 2–4 hours; Hazelden: better it "doesn't overstay its welcome" than "over 500 levels!" |
| Professor Layton and the Curious Village | 120 puzzles, 3 hints each, 10 starting hint coins |
| Return of the Obra Dinn | 60 crew identities |

- Blow: "be generous with your mechanics" and avoid mechanics "which appear rarely": a mechanic should earn many puzzles or be cut.
- Defaults [convention]: 1 new concept per puzzle; 4–8 puzzles per mechanic on the critical path plus optional side puzzles; generate 2–3× the puzzles you need and cut; a mechanic is worth adding only if pairing it with existing ones yields new truths (`puzzle-craft.md` §3).

## 11. Sequence table template

| ID | Tier | Slot | Truth (1 line) | New concept | Prereqs | Stance | Moves / pushes | Classes | Entanglement excess | CI pushes | Valves | Playtest median | % who can state truth |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Fill the solver columns from script output only (`puzzle-verification.md`). Leave playtest columns blank until there is data.

## 12. Review checklist

- [ ] Each mechanic has a written checklist; every fact has a clean room and a gate where stumbling fails
- [ ] Introduce/gate puzzles have one solution class; bypasses of the lesson blocked
- [ ] ≤1 new concept per puzzle; curriculum slots (introduce → gate → develop → combine → twist → conclude) present per mechanic
- [ ] Puzzles grouped into knowledge tiers: parallel within, gated between, gate checks the tier's core fact
- [ ] Protected leaps primed several puzzles earlier; no stepping stone directly before
- [ ] Airlocks between independent puzzles; break after 2–3 hard puzzles; re-teach after big concepts
- [ ] Hint ladder / parallel options / unlock-all / skip state decided per puzzle; hardest ideas optional
- [ ] Dependency chart run through `dependency_chart.py`; no cycles or unreachable nodes; mid-act bottlenecks easy
- [ ] Difficulty order backed by solver metrics and playtest data, not designer feel
- [ ] Sequence table filled; solver columns from script output only
