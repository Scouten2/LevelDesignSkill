# Puzzle Craft: Designing One Puzzle

## Contents
1. What a puzzle is
2. Choose the stance: showcase or revelation
3. Explore the system, then prune
4. Idea generators
5. The insight card workflow
6. Reverse-engineer from the key move
7. The deletion test
8. Misdirection and the false assumption
9. Readability
10. Fairness lint
11. Subgenre notes
12. Worked example: "Unstack"
13. Review checklist
14. Levels to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact.

Sequencing puzzles into a game: `puzzle-sequencing.md`. Solver protocol, difficulty metrics and playtests: `puzzle-verification.md`. Grid format: `grid-conventions.md`. Card template: `assets/insight-card.md`.

---

## 1. What a puzzle is

- **A puzzle is a compact demonstration of a true, non-obvious consequence of the rules.** Blow and ten Bosch: "1) know and understand the truth, 2) illustrate the truth as a solvable puzzle, and 3) remove anything that isn't the truth" (IndieCade, 2011). If you can't state the truth in one sentence, the puzzle isn't designed yet.
- **Surprise is the payload.** Blow: a solution that is exactly what the player expected carries no information. A puzzle whose first idea works is a chore, not a puzzle.
- **Goal obvious, method hidden.** Kim: "A puzzle is fun, and it has a right answer"; "first build a good toy" so manipulating the pieces is pleasant before any solve. The challenge must come "by the puzzle itself, not the controls" (Kim, *What is a Puzzle?*).
- **Two difficulty sources.** Kim: puzzles draw on ingenuity and patience in different proportions; Pelánek's Sudoku work splits difficulty into step complexity and the dependency structure among steps. Thinky-game designers prize ingenuity: SSR is "epiphany after epiphany with no unnecessary labor in between" (Northway). Say which source each puzzle uses.

## 2. Choose the stance: showcase or revelation

Practitioners genuinely differ. Pick per project (or per optional layer) and write it on every insight card, because it sets board size, slack and step count.

| | Showcase (Traynor, *Patrick's Parabox*) | Revelation (Blow; Lavelle's *Stephen's Sausage Roll*) |
|---|---|---|
| Aim | "To showcase/communicate, not challenge/stump"; "the easiest possible version of a puzzle that still features the interesting idea" | Make the player "certain that the puzzle is impossible", then reveal "some deep fact about the system" (Foddy on SSR) |
| Board | Trimmed possibility space, removed solution steps, "extra space in each level so there could be errors" | Tight; every cell matters; one sausage in a 3×3 room has "enough possibilities to baffle you" (Brough) |
| Volume | Many small puzzles (364 shipped, >600 drafts cut) | Fewer, harder puzzles; some players won't finish (The Witness has a puzzle Blow guessed <1% would solve) |
| Accidental solve | Fine if "the immediately following puzzles" force the same concept | Close it; the insight is the point |

Portal sits between them: training-first and linear, with rare protected leaps. Default to **showcase** for mandatory content and put revelation puzzles on optional paths (see `fun-checks.md`: mandatory content should be easier than designers expect).

## 3. Explore the system, then prune

Design puzzles from a system, not from a wish list. Blow: "completely explore all possible consequences and combinations", then "draw a strong boundary around the richest aspects" and trim anything "unfocused, contrived… or [that] does not provide enough surprise".

1. **Mechanic-pair matrix.** Rows and columns = mechanics/objects; each cell = the interaction, a surprise rating 0–2, candidate puzzle IDs. Empty rows: prune or extend that mechanic.
2. **Completeness matrix.** Does every rule apply to every object type? Blow: test immunity to time "with everything in your world: what happens if monsters are immune, what happens if doors are." Braid marks every time-immune object with a green glow, so the one exception puzzle still follows the system.
3. **Action sequences.** Enumerate A then B, B then A, AAB, ABA (Traynor). Each ordering that behaves differently is a candidate.
4. **Rule decisions.** Traynor's order: natural behaviour over arbitrary simplification, then the behaviour that makes more interesting puzzles, then intuitive behaviour, then cost. He replaced Parabox's "enter at any free edge tile" with centre-only entry because the original made "awkward puzzles… awkward rule to learn". Teikari dropped intrinsic object properties so "the only meaning in the levels came from the interactable rules".
5. **Prototype first.** Hazelden prototyped *A Good Snowman Is Hard to Build* in PuzzleScript "before writing any code at all" to test that the mechanics "allowed for interesting puzzles", made most of its puzzles "in just a couple of days", and kept the prototype as his level editor.
6. **Health metric.** Traynor: "Number of puzzles you can make in it." If you can't list 10 candidate truths for a mechanic [convention], it is too thin to carry a world.

## 4. Idea generators

Traynor's crowd-sourced "Puzzle Level Idea Strategies" (2022) as a generator list. Run several per mechanic; each output is a candidate truth for an insight card.

| Generator | How to apply it |
|---|---|
| Force an interaction | Pick a matrix cell; build the smallest room where it is the only way through |
| Force a deduction | Pick a fact the player can infer; make progress depend on inferring it |
| Forward design chain | Place objects so the player follows your exact sequence of deductions |
| Impossible → possible | Build a paradox, find a loophole in the rules, then camouflage the loophole |
| Possible → impossible → undo | Tighten until unsolvable, then undo the last change: the tightest solvable version |
| Extremes and geometry | A level 2 cells wide, symmetric, no walls, one object, maximum objects |
| Invariants and emergence | Parity, loops, reversibility; gadgets (one-way tunnel, binary counter, combination lock) |
| Things almost happen | A setup where the obvious move nearly works; the gap is the lesson |
| Tell a joke | A useful object becomes a hindrance; a puzzle that looks hard but is easy |
| Clarify a misunderstanding | Take a wrong model playtesters voiced; build the room that refutes it |
| Alternate solution → new level | When a draft has a second solution, make a puzzle that forces it |
| Bisect / back-design | Merge two levels' ideas; strip a hard puzzle down to an easy teaching one |

Expect to discard most drafts: Parabox shipped 364 puzzles and left over 600 drafts unused. Generate 2–3× the puzzles you need [convention]. Studying other games' levels is a legitimate generator; copying them is not (see SKILL.md gotchas).

## 5. The insight card workflow

Fill `assets/insight-card.md` before drawing any grid:
1. **Truth** (one sentence) and **false assumption** it overturns.
2. **Tempting wrong move** and the **visible rule** that defeats it.
3. **Prerequisites** (puzzle IDs) and **slot** in the curriculum (`puzzle-sequencing.md` §3).
4. **Stance** and difficulty source (ingenuity or patience).
5. **Key move**, then build (§6), strip (§7), verify (`puzzle-verification.md`).
6. **Post-solve sentence**: "Of course… !" Gilbert's fairness test: solutions "don't have to be obvious, just make sense". If you can't write it, the puzzle is arbitrary.

## 6. Reverse-engineer from the key move

Teikari: think of interactions "until I run into something that seems like it might be 'cool'… Once that happens, I try to reverse-engineer a level that requires said interaction." Procedure:
1. Place the key move's before/after states (the box that must step back, the word that must be broken).
2. Add the minimal context that makes the key move *necessary*: the goal, and the one constraint that forbids the obvious route.
3. Block every cheaper route; run the solver after each block.
4. Only then choose the start state, positioned so the tempting wrong move is the nearest one.
5. Gilbert works the same way for chains: start from "the player needs to get into the basement", not "where should I hide a key" (dependency charts: `puzzle-sequencing.md` §8).

## 7. The deletion test

For every element (wall, box, cell, object, rule word): delete it and re-solve. Keep it only if its removal (a) makes the puzzle unsolvable, (b) opens a route that skips the truth, or (c) costs readability or the tempting wrong move. Everything else is noise; "remove anything that isn't the truth".
- Prefer chunked complexity: few objects with rich behaviour. Brough: each sausage "adds the complexity of maybe four Sokoban blocks… chunked in an intuitive way."
- Showcase stance keeps deliberate slack; revelation trims to the bone. Record which slack is deliberate.
- "Every object must be necessary" is a Sokoban-like rule of thumb [convention]; slack floor for recovering from mistakes is not an object.

## 8. Misdirection and the false assumption

- **Misdirect with the rules, not noise.** The tempting wrong move must be a real move that fails for a rule the player can see; "each failed attempt… should reveal information" (Blow). Teikari stopped using red herrings "just for their own sake" because they "don't usually create very interesting problem-solving situations".
- **Name the false assumption** ("boxes only move toward goals", "keys always rewind", "orange portals are exits"). The truth must overturn something players actually believe; Braid World 4's non-exempt key was a surprise that "made sense".
- **Kill accidental associations.** Portal testers "so strongly associated boxes with buttons" that they hunted for a missing box, so Valve swapped in a pedestal button and a ticking timer. Audit every object for what it suggests.
- **Use associations on purpose.** Momentum was Portal's hardest concept; a repeated pushed-out slab over a checkerboard landing taught "slab means fling" like "cubes with buttons".
- **Decorative interactables are lies.** An unused lever teaches players to distrust your space.

## 9. Readability

- **Interactive vs décor.** Portal's cluttered early art "interfered with the portal training process"; the final style uses round shapes for points of interest and sharp shapes for background. Decide this before the art pass; re-verify after (`puzzle-verification.md` §10).
- **The needed observation must be unmissable.** In a Portal 2 fizzler room "almost none of our playtesters could solve" the original; the fix was "a single hole through the glass, moved down to the eye level of the player", which also made both sides valid. Fix with geometry before text. Valve: "Players very rarely look up, and they almost never look at the things that are obvious to us as designers" (Game Informer, *Making a Test Chamber*, 2010).
- **State is readable** at a glance: what is solved, what is powered, which way each object faces. Multi-step rooms: `genre-dungeon-metroidvania.md`.
- **Quiet while thinking.** Portal 2 kept GLaDOS to the start and end of chambers; players "really, really don't want to listen" mid-solve.
- **Cheap undo and reset** (Baba Is You, SSR) turn experiments into thinking. Without undo, every reachable dead state must be visibly dead and one key from a reset.

## 10. Fairness lint

Run on every puzzle. Gilbert's rules are from "Why Adventure Games Suck" (1989); his verified twelve are: clear end objective; obvious sub-goals; live and learn; backwards puzzles; I forgot to pick it up; advance the story; real time is bad drama; incremental reward; arbitrary puzzles; reward intent; unconnected events; give the player options.

| Check | Question | Basis |
|---|---|---|
| Information | Is everything needed perceivable in-world, from where it's needed, in the default view? | Escape rooms: specialised knowledge "obtainable within the room itself" |
| Completeness | Does each rule behave the same for every object type? Any exception visibly marked? | Blow (doors immune?); Braid's green glow |
| Connection | Would a player guess why this key opens this lock? Do "those six objects" plausibly affect the door? | Gilbert: unconnected events, arbitrary puzzles |
| Order | Is the problem met before its solution, ideally the crevice before the rope? | Gilbert: backwards puzzles |
| Recoverability | No die-to-learn; no missable required item; no silent soft-lock | Gilbert: live and learn, "I forgot to pick it up"; Portal's box-delivery tubes |
| Intent | If the player is right next to the object and trying, does the game accept it? Accept any plausible tool by attribute | Gilbert: reward intent; Fox's attribute matching (Zak McKracken) |
| Anti-guessing | Is the answer space too big to brute force, or is feedback batched? | Obra Dinn: 60 crew, fates confirmed only in sets of three. Throttle when <~20 options [convention] |
| Timing | Timed puzzles: ~10% finish with time to spare, ~80% just make it, ~10% fail | Gilbert's 10/80/10 |
| Controls | Could a player who has the insight fail on execution? | Kim |
| Skip | Is there a skip/completion state? | TLOU Part II "SKIP PUZZLE"; `accessibility.md` |

## 11. Subgenre notes

- **Sokoban and block-pushers.** Pushing is irreversible: a box in a non-goal corner is dead. Keep boards small and grow entanglement, not area (`puzzle-verification.md` §8). Verify with `grid_puzzle_solve.py`; its legend also covers ice, keys/doors, pits and switches (`grid-conventions.md` §3). Undo is mandatory.
- **Rule-change (Baba Is You).** Each area puts a "new rule/word in the spotlight" with basic words as "supporting cast" [unverified, secondhand]; testing was largely "eliminating alternative solutions that aren't interesting enough" [unverified]. Run the completeness matrix over every noun × property. The bundled solver doesn't model rule rewriting: prototype in PuzzleScript or hand-trace (`puzzle-verification.md` §11).
- **Line/panel (The Witness).** Blow's rules came from exploration (grooves; no self-crossing turned panels into partition puzzles). Clustered panels teach one rule; complexity rises by grid size, refined rules, then new rules; never explain in words, because explaining immediately "kills epiphany". Enumerate all solution paths per panel to check the intended rule is required.
- **Physics.** Outcomes vary run to run, so verify over many trials and design tolerance into targets. Separate *completable* from *mastered* (stars); Rovio picks birds before buildings and spends longer tuning star thresholds than building. Detail: `genre-casual-mobile.md`.
- **Adventure/inventory.** Gilbert's twelve plus dependency charts (`puzzle-sequencing.md` §8). Each solve opens 2–3 more; every item use must "make sense" in-world.
- **Deduction and knowledge games.** Obra Dinn: break the story into "discrete disasters" the player can "compartmentalize"; plan every fact on two axes, chronology and discovery order, in "a huge spreadsheet"; put characters in "enough different situations" that clues have room; "overwhelm the player initially, then give them time to get comfortable". Outer Wilds: players can't be curious about something specific "unless they're already familiar with everything in their immediate vicinity"; knowledge is the only progression. Metapuzzles (Fez, Tunic) stay optional; Tunic drew criticism for players feeling stuck.
- **Escape rooms.** 45–60 minute sessions; all knowledge in the room; hints from a gamemaster, sometimes limited or penalised. Run 2–3 parallel threads so a group can split [convention].
- **Puzzle rooms in other genres.** One truth per room; readable reset; no combat pressure while the player is thinking [convention]; author a skip state. Teach the verb elsewhere first (Portal 2 taught boss mechanics "a level earlier… without any time pressure").
- **Puzzle-platformers (Limbo, Inside).** The insight is the challenge; execution should be easy once the insight lands [convention]. Playdead's key playtest question: "Did they get stuck in frustration loop: yes or no." Show a hazard working on something else first, checkpoint right before each puzzle, keep one or two interacting elements, and reuse one mechanic with escalation [convention]. Check jumps with `platformer_reach.py` (`platformer-checks.md`).

## 12. Worked example: "Unstack"

Insight card (short): **Truth:** a box must first step *away* from its goal to free the box beneath it. **False assumption:** good pushes move boxes toward goals. **Tempting wrong move:** push the top box left from the side you reach first; the visible rule (no pulling, a wall behind it) leaves it stuck. **Prereqs:** pushing, corners are fatal. **Stance:** showcase, develop slot. **Post-solve:** "Of course: the top box had to get out of the way, then come back."

Draft 1 had floor at (1,1) and (1,2): the solver found 2 push-optimal solutions, mirror images (top box left or right). Deletion test, reversed: walling (1,1) and (1,2) turns the left push into a visible trap and leaves one class.

```
   0123456
00|#######
01|##-.--#
02|##-$--#
03|###$#-#
04|###@--#
05|###.###
06|#######
```
Player (3,4); boxes (3,2) (3,3); goals (3,1) (3,5). `(col,row)`, origin top-left.

```
python3 -I scripts/grid_lint.py unstack.txt --legend puzzle --expect @=1 --expect '$=2' --closed
python3 -I scripts/grid_puzzle_solve.py unstack.txt --metrics --classes
python3 -I scripts/grid_puzzle_solve.py unstack.txt --intended rruuullldRDDrruuLrddlluU
```

Real output from the bundled `grid_puzzle_solve.py --metrics --classes` (the level ships as `scripts/tests/fixtures/puzzle/unstack.txt`): SOLVABLE, 5 pushes / 24 moves (`rruuullldRDDrruuLrddlluU`), push-optimal; 1 solution class up to reordering (draft: 2); first-move traps 1 of 2 first pushes (draft: 0); counter-intuitive pushes 1 (the `R` at move 10, distance to goal 1 → 2); box changes 2 (minimum over all solutions), entanglement excess 1 (the boxes must interleave); dead-end ratio 0.69 (undo need, not difficulty); 0.00 s. `--intended` reports no shortcut. No bypass test is needed beyond the first-push count: the lower box can't move until the top box leaves the column, so every solution contains the key move. Khalifa prior: 24 moves / 49 cells ≈ 0.49, low against 1.22 ± 0.46, as expected for a small teaching room.

## 13. Review checklist

- [ ] Stance chosen (showcase / revelation) and written on the card; difficulty source named
- [ ] Insight card complete before the grid: truth, false assumption, tempting move + visible rule, prereqs, key move
- [ ] Puzzle reverse-engineered from the key move; cheaper routes blocked one by one with a re-solve each
- [ ] Deletion test run on every element; deliberate slack recorded
- [ ] Every failed attempt fails for a visible rule; no decorative interactables or arbitrary red herrings
- [ ] No accidental associations (box-hunt buttons); learned cues used deliberately
- [ ] Key observation in default view at eye level; state readable; quiet during solving
- [ ] Fairness lint table passes (information, completeness, connection, order, recoverability, intent, anti-guessing, timing, controls, skip)
- [ ] Post-solve "Of course…" sentence written
- [ ] Verification protocol run and quoted (`puzzle-verification.md`); grid lint-clean and ruled

## 14. Levels to study

- **Portal / Portal 2** with developer commentary: Chambers 01–13 (gating, glass barrier, fling slab, pedestal button); the Portal 2 fizzler room and co-op courses.
- **Stephen's Sausage Roll:** the first island (tiny boards, total necessity). **Baba Is You:** world 1, one trick per level.
- **The Witness:** the opening area and any region's first panel cluster. **Braid:** World 4 (green-glow exemption and its exception).
- **Patrick's Parabox:** World 1 levels 1–9. **Return of the Obra Dinn:** the first two disasters. **Outer Wilds:** the opening loop on Timber Hearth.
