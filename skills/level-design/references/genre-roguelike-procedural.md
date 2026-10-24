# Roguelike & Procedural Levels

## Contents
1. Universal rules: design the rules, not the level
2. Grid + guaranteed path + role templates (Spelunky)
3. Authored skeleton, generated fill (Dead Cells)
4. Floorplan → special rooms → fill (Binding of Isaac)
5. Cycles instead of branches (Unexplored)
6. Chamber-based runs and reward signposting (Hades)
7. Other techniques: flow graphs, attach-and-loop, WFC
8. Validating generated levels
9. Survivors-like arenas
10. Review checklist
11. Games to study

> Confidence tags: untagged claims come from developer statements, primary sources or well-documented analyses, including Boris the Brave's reverse-engineering write-ups (see `SOURCES.md`). **[convention]** = practitioner practice or a tunable default with no source behind the number. **[contested]** = sources disagree. **[unverified]** = could not be checked; don't quote it as fact. Fan-wiki numbers are flagged as such.

Core refs: pacing and teaching in `principles.md`; loops, lock-and-key and critical paths in `layout-and-flow.md`; room dimensions in `metrics.md`; ability gating and `graph_check.py` in `genre-dungeon-metroidvania.md`; Spelunky's generator as a hand-authoring order in `platformer-craft.md`; DRG's hand-made room templates in `genre-coop-pve.md`; LLM generate-and-verify loops in `SKILL.md`; playtest protocol in `playtesting-and-critique.md`.

---

## 1. Universal rules: design the rules, not the level

- **The hybrid wins.** The dominant successful pattern: designers author the building blocks (room templates, chunks) and the high-level skeleton (critical path, lock/key placement, pacing peaks); the algorithm only arranges and fills them. Steve Filby (Dead Cells): too much procedural generation leads to bland, messy, inconsistent levels.
- **Pipeline order.** Build generators in this order and test each stage alone:
  1. **Guaranteed critical path** from entrance to exit.
  2. **Role-typed, hand-authored rooms or chunks** fitted to the path.
  3. **Special rooms placed by graph rules** (boss at max distance, secret adjacent to many rooms, shop or rest before the boss).
  4. **Content filled by weighted rolls** (enemies, treasure, hazards).
  5. **Validation**: reject and re-roll seeds that fail checks (§8).
- **Write the constraint, not the instance.** Every "this level should…" statement from a design review becomes a generator rule or validator check. If you can't express it as a rule, author it as a hand-made set piece.
- **Hide the template.** Players learn templates fast. Counter with sub-chunk randomization inside templates (Spelunky), many variants per role, and rare set pieces.
- **Keep rest beats.** Randomness flattens rhythm unless you schedule calm rooms before peaks (Hades, Dead Cells). Pacing has to be a rule.

## 2. Grid + guaranteed path + role templates (Spelunky, Derek Yu)

- **4×4 room grid.** A random path walks room to room from the top row to the bottom. The path's shape decides each room's type: corridor (left–right exits), drop-down (exit at the bottom), landing (entrance from above).
- **The path is guaranteed traversable without ropes or bombs.** Off-path rooms may be open or walled off; they hold optional risk and reward. Yu's top priority was a guaranteed entrance-to-exit route.
- **Templates by role.** Each room type has many hand-made templates, and each template has randomized sub-chunks (small tile blocks rolled from sets), so the same template reads differently each time.
- **Content pass last.** A later pass places monsters and treasure tile by tile using probability rolls.
- **Yu's framing:** the designer builds the blocks and lets the generator do the rest.
- **Apply it:** define room roles by their exits *first* (which sides are open), then author templates per role, so any path the walker produces can be dressed from the pool.
- **Verified generator order** (Kazemi's interactive Spelunky generator write-up): a guaranteed solution path across the 4×4 room grid, then rooms filled from templates that guarantee the exits the path needs. The same order works for hand design: **path graph → room contracts (required exits) → room fill → hazard pass**. `platformer-craft.md` applies it to hand-authored platformer chunks; check each filled chunk with `platformer_reach.py`.

## 3. Authored skeleton, generated fill (Dead Cells, Sébastien Bénard)

- **Origin.** The team first hand-made levels, ran short of time, and switched to a hybrid. The guiding principle was to keep the algorithm involved in as limited a role as possible.
- **Skeleton by hand.** A human-planned skeleton places keys and locked doors, and the algorithm fills the gaps with handmade tiles (rooms). Runs are "a mashup of carefully designed chunks". Spelunky was the model.
- **Planned pacing.** Dramatic peaks and relaxing breaks are planned into the skeleton. The idea started as an "AI Director" that was later scaled back.
- **The hardest problem:** keeping runs different while players can still remember what they can and cannot cross yet. Metroidvania gating under randomization only works if gates look the same every run and the skeleton keeps their order stable.
- **Apply it:** fix per biome the things players should learn (gate types, exits to other biomes, the biome's signature mechanic); randomize the rest.

## 4. Floorplan → special rooms → fill (Binding of Isaac)

Source: Boris the Brave's analysis and community wikis.

- **Stage 1: floorplan.** The floor grows outward from the start room on a grid. Room count rises with floor depth; one widely cited formula is about random(2) + 5 + floor × 2.6, but sources vary.
- **Stage 2: special rooms by graph rule.**
  - Boss room: the farthest dead end from the start.
  - Item room, shop and the like: other dead ends. Fan wikis say at least 5 dead ends per floor are required for these, though exact numbers conflict between sources.
  - Secret room: a cell that touches several existing rooms, so exploring with bombs is rewarded by deduction ("which wall touches the most rooms?").
- **Stage 3: fill from pools.** Each room's interior is picked from a pool of hand-made layouts for its type.
- **Apply it:** placement rules can create a puzzle on their own. Isaac's secret-room rule teaches a heuristic that skilled players exploit. Pick rules the player can learn and reason about.

## 5. Cycles instead of branches (Unexplored, Joris Dormans)

- **Loops, not trees.** Most generators build a start-to-goal path and hang branches off it. Dormans replaces branches with *loops*: several ways to the goal and shortcuts back, fewer dead ends, less backtracking, and layouts that look hand-made.
- **How it works.** The algorithm draws a large loop with the entrance and goal attached. The two arcs between them are shaped by one of several predefined **cycle types** (e.g. lock-and-key, hidden shortcut), and the cycle type sets the level's pacing. The process recurses with smaller sub-cycles and is built on graph grammars.
- **Caveat.** Much of Unexplored's variety comes from many hand-coded special cases, not the cycle idea alone. Budget for authored special cases.
- **Cheaper version.** Graph grammars are hard to implement. Simpler alternatives grow a cycle out from a chosen node.
- **Apply it:** give each loop a job (a lock-and-key, a one-way shortcut, a risky short arc versus a safe long arc) so pacing has shape. A loop with no job is just an alternate corridor. Loop design is covered in `layout-and-flow.md`.

## 6. Chamber-based runs and reward signposting (Hades, Supergiant)

- **The reward is on the door.** Each exit door shows its chamber's reward before the player chooses, turning route choice into reward choice. Layout becomes a meaningful decision without the player seeing the map.
- **Risk is flagged.** A skull under a reward symbol marks a harder encounter with a bigger payoff.
- **Two currencies, two colours.** Gold laurels mark rewards for the current run; blue laurels mark persistent meta-currency. Colour-code reward classes so players read them at a glance.
- **Calm before the boss.** The chamber before a boss is usually combat-free, with a shop or a free boon.
- **Scale.** A run has up to about 73 chambers (fan wiki). Plan pacing over the whole run, not per chamber.
- **Apply it:** show the reward before the commitment, show the risk next to it, and schedule a breather before each peak.

## 7. Other techniques

- **Flow graphs.** [convention] Enter the Gungeon places hand-made rooms via pre-authored "flow" graphs per floor. Each graph specifies the order and branching of room categories (entrance, combat, chest, shop, boss foyer, boss), and rooms are fitted to it. This is a good default when you want authored pacing with varied rooms.
- **Attach-and-loop (Brogue).** [convention] Brogue attaches room shapes (cross rooms, caves, circles) to existing walls via doors, then adds loops by cutting secret doors or openings where two areas are close in grid space but far apart along paths. It also places "machines" (vaults and key puzzles) as constraint-checked blueprints.
- **Wave Function Collapse (Maxim Gumin, 2016).** [convention] WFC builds output from local adjacency constraints learned from example tiles. It is good at local coherence and poor at global structure (no guaranteed path or pacing), so pair it with a graph or critical-path pass. Townscaper and Bad North use it for local tiling.
- **Hand-made rooms with exit sockets (Deep Rock Galactic).** Ghost Ship strings 100+ hand-crafted room templates "like pearls on a string" with generated tunnels; half-domes on each room's perimeter mark potential exits, and each room is playtested with every class. Details in `genre-coop-pve.md`.
- **Tile-and-vault.** [convention] Diablo-style: tiles and set pieces with hand-made vaults or quest rooms placed into procedural layouts.
- **Jigsaw structures.** [convention] Minecraft joins structure templates at connector points over noise terrain.
- **Choosing.** [convention] Use a grid walker for compact action levels, a flow graph or cyclic generator for dungeons with pacing, WFC for local texture inside a known structure, and attach-and-loop for organic roguelike caves.

## 8. Validating generated levels

You can't playtest every seed, so test the generator. [convention] throughout, apart from the source-backed guarantees noted above.

- **Solvability.** Run a pathfinder with the player's real movement metrics (jump height, gap width from `metrics.md`) from entrance to exit on every generated level. If there are locks, run a key-before-lock check: every key reachable without its own lock. Reject and re-roll failures; log the seed.
- **Bundled checkers for sample levels.** When designing a generator on paper, hand-make or emit a few sample outputs and run the skill's scripts on them, reporting numbers verbatim: `graph_check.py` for lock-and-key floor graphs (reachability, key-before-door order, consumed-key softlocks, dead ends, cycle count); `platformer_reach.py` for side-view chunks against the movement kit; `grid_puzzle_solve.py` for push-puzzle rooms; `level_metrics.py --compare` to show sampled outputs are genuinely different (tile and structural distance; it flags near-duplicates). These check samples, not the generator: say so.
- **Guarantees as assertions.** Encode each design promise as an automated check: "critical path needs no consumables" (Spelunky), "boss at max graph distance", "rest room before boss", "no metroidvania gate before its ability can exist".
- **Expressive range analysis.** Generate thousands of levels and plot them on two or more metrics (e.g. path length, linearity, enemy density, loop count, dead-end count). Look for clusters that are too tight (sameness), outliers (broken levels) and unreachable regions of the design space you wanted. Re-run after every rule or template change.
- **Seed review.** Keep a library of seeds: a random sample, the extremes from expressive-range plots, and every seed a tester flagged. Review them by eye and in play. Fix the rule that produced a bad one, not the level.
- **Template wear.** Track how often each template appears per run and across runs. Retire or vary templates that players recognize too fast.
- **Pacing trace.** Plot intensity per room along the critical path for sampled seeds and compare it to the intended beat chart (`process.md`). Missing rest beats show up as flat high lines.
- **Playtests still matter.** Watch players on fixed seeds so sessions can be compared, then on random ones (`playtesting-and-critique.md`).

## 9. Survivors-like arenas

The level is a **timeline over an arena**: the space is simple, and difficulty lives in the spawn schedule. Primary developer sources are missing; the spawn numbers below come only from a fan wiki, so everything here is **[convention]**.
- **Spawn schedule.** [convention] Vampire Survivors' fan wiki describes one wave definition per minute (minimum enemy count and spawn interval), periodic spawning that pauses above ~300 live enemies, and map events at fixed seconds. Treat these as a starting template: write a minute-by-minute table (composition, minimum count, interval, events, elite or boss drops) and a live-enemy cap.
- **Arena shapes.** [convention] Open field (free kiting, pressure from all sides), corridor (Inlaid Library-style: enemies come from two ends, kiting is linear), and ring or rooms (choke points). Choose the shape for the kiting pattern you want; one stage per shape.
- **Obstacles make kiting lanes, not traps.** [convention] Scatter obstacles so they split hordes and create lanes, but leave no pocket the player can be pinned in; dead ends are deaths. Check every obstacle cluster has at least two exits at the player's speed.
- **Pulls across the arena.** [convention] Chests, healing and pickups away from the start, so the player must cross the horde; elites drop them to give each wave a target.
- **Spawn ring.** [convention] Enemies spawn just off-screen around the player; never on-screen without a telegraph.
- **Readability at density.** [convention] Hundreds of sprites: hazards and elite enemies need distinct silhouettes and colours; projectiles and pickups must not blend into the floor; offer effect-opacity options (`accessibility.md`).
- **Session arc.** [convention] Vampire Survivors stages run about 30 minutes and end with an unbeatable reaper; whatever the length, chart intensity per minute and schedule short lulls before boss minutes (beat chart, `beat_lint.py`).

## Review checklist

- [ ] Pipeline written down: path → roles → special rooms → fill → validate
- [ ] Critical path guaranteed traversable with base abilities only (no consumables)
- [ ] Room/chunk templates authored per role (defined by exits); sub-chunk variation inside templates
- [ ] Special-room placement rules stated (boss distance, secret adjacency, shop/rest before boss) and learnable
- [ ] Loops have jobs (lock-and-key, shortcut, risk/safe arcs); dead ends pay off
- [ ] Pacing is a rule: peaks and calm rooms scheduled, calm room before every boss
- [ ] Rewards and risk shown before commitment (door icons, risk markers, colour-coded currencies)
- [ ] Learnable constants fixed across runs (gate looks, biome signatures, gate order)
- [ ] Validator: solvability, key-before-lock, design assertions; failing seeds re-rolled and logged
- [ ] Expressive range plotted; outliers and sameness reviewed after every rule change
- [ ] Sample outputs checked with the bundled scripts (graph, reach, solve, `--compare` diversity); results reported verbatim
- [ ] Seed library kept (random, extremes, tester-flagged); template frequency tracked
- [ ] Survivors-like: minute-by-minute spawn table with a live-enemy cap; arena shape chosen for its kiting pattern; no obstacle pockets; pickups pull across the horde

## Games to study

- **Grid + templates:** Spelunky, Spelunky 2.
- **Hybrid skeleton:** Dead Cells.
- **Floorplan and special-room rules:** The Binding of Isaac: Rebirth/Repentance.
- **Cyclic generation:** Unexplored.
- **Chamber runs and signposting:** Hades, Hades II.
- **Flow graphs and vaults:** Enter the Gungeon; Brogue; Diablo.
- **Constraint tiling:** Townscaper, Bad North.
- **Survivors-like:** Vampire Survivors (Mad Forest open field vs. Inlaid Library corridor); Deep Rock Galactic (room templates).

Key sources (full list in `SOURCES.md`): GMTK, "How and Why Spelunky Makes its Own Levels"; Kazemi, Spelunky generator; Game Developer and Deepnight (Bénard, Dead Cells); Boris the Brave on Isaac and Unexplored; Hades Wiki; DRG "Below Decks" cave-generation blog; Vampire Survivors Wiki (unverified, bot-blocked).
