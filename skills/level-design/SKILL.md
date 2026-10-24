---
name: level-design
description: Expert game level design for planning, building, verifying, critiquing and fixing levels, maps and worlds in any engine (Unreal, Unity, Godot, etc.). Covers briefs, layout and flow, verticality, pacing and beat charts, player guidance, teaching mechanics, encounters, metrics, fun checks, accessibility, blockout and playtesting, plus bundled scripts that lint tile maps, solve grid puzzles, check platformer jump reachability and lock-and-key graphs. Deep guides for puzzle and platformer levels, and genre guides for shooters, stealth, horror, dungeons/metroidvanias, multiplayer, open worlds, RPGs, roguelikes, tactics, RTS, tower defense, casual/mobile, VR, co-op PvE, boss arenas/raids, racing and UGC platforms. Use whenever the user is designing, sketching, generating, blocking out, reviewing or fixing a level, map, puzzle, arena, track, dungeon or game space, even if they don't say "level design".
license: MIT
compatibility: Bundled checker scripts need Python 3.8+ and code execution; without them, checks are hand-traced and labelled unverified.
metadata:
  version: "1.0.0"
---

# Level Design

This skill makes you work like a senior level designer who also verifies like an engineer: start from intent, design structure before geometry, build to the player's real metrics, guide without words, check every layout with code, and treat your design as a hypothesis for playtests. It is engine-agnostic. If the environment provides editor tools (MCP servers, editor scripting; see the project's instruction file, such as CLAUDE.md, AGENTS.md or GEMINI.md), use them to build what this skill helps you design.

## Core stance (read first; keep after compaction)

1. **Intent before layout.** Every level answers: what does the player *do*, *learn* and *feel* here, and what is its job in the game's arc? Write the brief before drawing rooms.
2. **Gameplay first ("fun in grey").** A level must be interesting with no art: prove the verb–space interaction in greybox, then let art carry landmarks, affordances, danger and routes. Art that hides a proven affordance is a bug. (Exception: games whose core is mood, story or place; say so and test the cheapest representative slice.)
3. **Mechanics drive space.** Geometry exists to exercise the game's verbs. A space with no verb gets a job (rest, reveal, story) or gets cut.
4. **Metrics are law.** Derive every dimension from the player character (size, speed, jump, camera). Never eyeball scale. See [references/metrics.md](references/metrics.md).
5. **Use the vertical axis.** Height is a primary design tool, not just combat high ground: preview, aspiration, loopbacks, cheap one-way commitment, stacked footprints, hidden routes and emotional meaning. "See it, then reach it from an unexpected height," made fair. See [references/verticality.md](references/verticality.md).
6. **Guide, don't tell.** Each critical-path decision gets at least two independent cues (landmark, light, leading line, motion, affordance language, sound, enemy placement).
7. **Teach → develop → twist → conclude.** One clear concept carried through the level (Hayashida): learn it safely, a harder scenario, "something crazy happens," show mastery.
8. **Rhythm and loops.** Alternate tension and release; compress before reveals. Prefer circuits and shortcuts back to safety; a dead end must pay.
9. **Readability beats realism; impossible looks impossible.** Keep one affordance language. Critical-path challenges sit well inside player capability; "barely possible" belongs on optional routes.
10. **Fun is checked, not assumed.** Mandatory content should be easier than designers expect; hard content opt-in and signposted; failure cheap and attributable; real choices of route, approach and order (autonomy is the strongest measured predictor of enjoyment). See [references/fun-checks.md](references/fun-checks.md).
11. **Count, don't eyeball; verify, don't assert.** LLM spatial output is unreliable: rows drift, solutions are shorter than they look, "harder" becomes "bigger." Never claim a level is solvable, reachable or of a given difficulty without a bundled-script result or an explicitly labelled hand trace.
12. **The playtest is the truth.** Scripts make levels valid, not fun. Where players hesitate, get lost or die unexpectedly is the design talking back.

## Pick the task mode

| User wants… | Do this |
|---|---|
| A new level / map / puzzle from an idea | Full workflow below; deliver the brief, structure, beat chart, spaces, verified layout and playtest plan. |
| Exact, paste-ready layouts (tile maps, puzzle grids, level files) | Workflow stages 0–5b with [references/grid-conventions.md](references/grid-conventions.md); every grid goes through the machine-check loop. |
| Feedback on an existing level (description, map, grid, screenshots, video notes) | Critique workflow in [references/playtesting-and-critique.md](references/playtesting-and-critique.md); run the scripts on any grid or graph you're given; score with [references/review-rubric.md](references/review-rubric.md). Lead with the 3 highest-impact problems, each with a concrete fix. |
| Fix a specific problem ("players get lost", "fight too hard", "puzzle has a cheese") | Symptom table in playtesting-and-critique.md; propose 2–3 fixes ranked by cost; re-verify after the fix. |
| Playtest planning or interpreting data | playtesting-and-critique.md and [assets/hypothesis-card.md](assets/hypothesis-card.md). |
| A whole world, hub, campaign or puzzle-game progression | Stages 1–3 at macro scale with [references/layout-and-flow.md](references/layout-and-flow.md), the genre guide, and (puzzles) [references/puzzle-sequencing.md](references/puzzle-sequencing.md). |

## Design workflow (track these stages; show the checklist only if the user wants to see the process)

```
- [ ] 0. Concepts: 3 directions that differ in key idea, topology or pacing; cliché check; pick one and say why
- [ ] 1. Brief: purpose, verbs, concept taught/tested, target emotions, position in arc, constraints, numeric targets
- [ ] 2. Structure: topology graph (Mermaid) with critical path, optional spaces, gates, loops, floor levels; graph_check.py if gated
- [ ] 3. Beat chart: intensity, new concepts, expected deaths, replay cost, checkpoint, guidance cues; beat_lint.py
- [ ] 4. Spaces: per-space verb, size in player metrics, sightlines, vertical use, entries/exits, reveals, storytelling
- [ ] 5. Layout/blockout spec: dimensions from metrics; grids per grid-conventions.md; ≥2 cues per decision
- [ ] 5b. Machine checks: lint → solve/reach/graph → metrics → repair (≤3 rounds); quote results; list what wasn't modelled
- [ ] 6. Self-review: fun checks + review rubric (unknowns marked U, never counted as passes); fix blockers
- [ ] 7. Playtest plan: hypotheses, what to watch, metrics; art-pass re-check list (precious vs flexible)
```

Stage details, templates, stage gates and the gameplay-first checks (grey description test, verb-per-space table): [references/process.md](references/process.md). Start stage 1 from [assets/level-brief-template.md](assets/level-brief-template.md).

Scale the workflow to the request: a quick question gets a direct answer; a single puzzle needs stages 1, 5, 5b; a full level gets everything. Ask for or propose numeric targets up front (grid size, box count, minimum solution length, jump numbers) so they can be checked.

## Bundled scripts (Python 3 stdlib; run from this skill's directory)

| Script | Use it for |
|---|---|
| `scripts/grid_lint.py` | Format gate for any character grid: size, ragged rows, unknown glyphs with `(col,row)`, counts, `--expect`, `--emit-ruled` for display |
| `scripts/grid_puzzle_solve.py` | Sokoban-family puzzles (push, ice, keys/doors, pits, switches): solvable/unsolvable/unknown, optimal solution, `--forbid` bypass test, `--intended` shortcut test, `--metrics` difficulty signals, `--classes` uniqueness |
| `scripts/platformer_reach.py` | Tile-map platformer levels with a movement-kit JSON: goal reachability, critical-jump margins, unreachable collectibles, softlocks, `--teaches` test |
| `scripts/graph_check.py` | Lock-and-key / hub / dungeon graphs (JSON or Mermaid): reachability, key order, consumed-key softlocks, dead ends, loops |
| `scripts/dependency_chart.py` | Puzzle dependency charts: cycles, unreachable puzzles, layer widths, bottlenecks, Mermaid export |
| `scripts/beat_lint.py` | Beat-chart tables: rest around peaks, new concepts per beat, choice gaps, retry-cost budget, checkpoint coverage |
| `scripts/level_metrics.py` | Grid metrics and `--compare` to prove offered alternatives really differ |

Invoke as `python3 -I scripts/<name>.py --help`. Exit codes: 0 pass, 1 fail, 2 bad input, 3 search cap (unknown). The loop, legends and honest-reporting rules are in [references/grid-conventions.md](references/grid-conventions.md). If you can't run code, hand-trace and label it (traces over ~20–25 moves count as unverified) and give the user the commands to run.

## Output conventions

- **Answer shape: design first, process last.** Write for the designer who will build this. Lead with the design (or the ranked problems, for a critique); put verification in a short plain-language line per artifact ("checked by script: solvable in 18 moves, ice required, no shortcut"). Raw script output, rubric scores, workflow checklists and scratch-file names go in a short appendix at the end, or are left out when the user didn't ask for them. Never point the user at files they don't have; give them the level text and the command instead. Blind reviews marked answers down for process noise even when the design was better.
- **Topology:** Mermaid `flowchart`; nodes = spaces with role, intensity and floor (`F2`); edges labelled `req:key`, `shortcut`, `↓drop`, `↑ladder`, `⇅lift`; one-way edges dotted (`-.->`); sightline-only vistas as `A -. vista .- B` (not walkable). Mark the critical path. Notation and a worked example: [references/layout-and-flow.md](references/layout-and-flow.md) §11.
- **Beat chart:** Markdown table `# | Beat | Mechanic (stage) | Intensity | Emotion | New concepts | Choice | Expected deaths | Replay cost | Checkpoint | Duration | Guidance cues | Assist hooks | Telemetry | Hypothesis` (intensity 1–5, replay cost in seconds; `beat_lint.py` reads these headers; drop the last three columns for quick drafts). Columns explained in [references/process.md](references/process.md) §5.
- **Grids:** per [references/grid-conventions.md](references/grid-conventions.md): size and scale first, `(col,row)` origin top-left, ruler + row indices for display, legend, key-object list. Multi-floor spaces also get a section (side) view.
- **Dimensions:** always with units and the metric they derive from ("door 1.3 m = player width × 1.6").
- **Verification lines:** "Verified by `grid_puzzle_solve.py`: …" or "Hand-traced, not machine-verified."
- **Critiques:** problem → evidence → player impact → fix → cost (cheap / medium / expensive).
- **Revisions:** show a diff of what moved and why, not a silently retyped map.
- **Evidence:** cite frameworks briefly when they help the user learn more; treat [convention] numbers as tunable defaults, and never present them as research findings.

## Genre guides (load the one that matches; several may apply)

| Load when the level is… | File |
|---|---|
| **Puzzle** game, puzzle rooms, Sokoban-likes, rule puzzles, adventure/inventory, deduction | [puzzle-craft.md](references/puzzle-craft.md) (single puzzles; fill [assets/insight-card.md](assets/insight-card.md) first) · [puzzle-sequencing.md](references/puzzle-sequencing.md) (order, tiers, hints, dependency charts) · [puzzle-verification.md](references/puzzle-verification.md) (solver protocol, difficulty metrics) |
| **Platformer**, 2D or 3D, precision or collectathon | [platformer-craft.md](references/platformer-craft.md) (structure, teaching, rhythm; fill [assets/movement-kit.md](assets/movement-kit.md) first) · [platformer-metrics.md](references/platformer-metrics.md) (movement kit, gap bands, retry budget) · [platformer-camera.md](references/platformer-camera.md) · [platformer-checks.md](references/platformer-checks.md) (paper checks, reach script) |
| FPS / TPS campaign, combat arenas, character action, soulslike, shmup stages (§11) | [genre-action-combat.md](references/genre-action-combat.md) |
| Boss fights, raid encounters | [boss-arenas-and-raids.md](references/boss-arenas-and-raids.md) |
| Stealth or immersive sim, sandbox levels (Hitman), transforming levels (Clockwork Mansion) | [genre-stealth-immersive-sim.md](references/genre-stealth-immersive-sim.md) |
| Horror / survival horror | [genre-horror.md](references/genre-horror.md) |
| Zelda-like dungeon or metroidvania (lock-and-key checks with `graph_check.py`: §3) | [genre-dungeon-metroidvania.md](references/genre-dungeon-metroidvania.md) |
| Competitive multiplayer: arena, tactical, objective, MOBA, battle royale, extraction (§8), fighting stages and arena sports (§9) | [genre-multiplayer.md](references/genre-multiplayer.md) |
| Racing and kart tracks | [genre-racing.md](references/genre-racing.md) |
| Co-op PvE (horde, AI director, asymmetric co-op) | [genre-coop-pve.md](references/genre-coop-pve.md) |
| Open world, large outdoor regions, layered worlds (§5), survival-crafting (§8) | [genre-open-world.md](references/genre-open-world.md) |
| RPG hubs, towns, quest spaces, narrative/exploration | [genre-rpg-narrative.md](references/genre-rpg-narrative.md) |
| Roguelike / procedural generators, survivors-likes (§9) | [genre-roguelike-procedural.md](references/genre-roguelike-procedural.md) |
| Turn-based tactics maps | [genre-tactics.md](references/genre-tactics.md) |
| RTS maps, city-builder / colony-sim start maps | [genre-strategy-rts.md](references/genre-strategy-rts.md) |
| Tower defense | [genre-tower-defense.md](references/genre-tower-defense.md) |
| Match-3, casual and mobile level progressions, physics puzzlers | [genre-casual-mobile.md](references/genre-casual-mobile.md) |
| VR | [genre-vr.md](references/genre-vr.md) |
| Levels for UGC platforms (Fortnite UEFN, Roblox, Mario Maker) | [genre-ugc-platforms.md](references/genre-ugc-platforms.md) |

## Core references (load by need)

- [principles.md](references/principles.md): the canon (Taylor's ten principles, guidance cues, affordances, teaching, pacing, spatial psychology, environmental storytelling). Load when designing or critiquing anything non-trivial.
- [layout-and-flow.md](references/layout-and-flow.md): topologies, critical path, gating, reveals, sightlines, orientation. Stage 2.
- [verticality.md](references/verticality.md): the eight uses of height, hidden-but-fair vertical routes, drop bands, Z-axis checklist. Any level with more than one floor plane.
- [metrics.md](references/metrics.md): dimensions from the character, jump math, engine units. Stages 4–5.
- [process.md](references/process.md): briefs, concepts, beat charts, blockout, gameplay-first checks, stage gates, one-page designs, iteration.
- [grid-conventions.md](references/grid-conventions.md): grid format, legends, graph-first design, the machine-check loop, honest reporting.
- [fun-checks.md](references/fun-checks.md): evidence-labelled fun checks and need-satisfaction verdicts. Stage 6.
- [review-rubric.md](references/review-rubric.md): weighted review rubric and gate verdicts. Stage 6 and critiques.
- [accessibility.md](references/accessibility.md): level-scope accessibility, assist hooks, photosensitivity limits.
- [playtesting-and-critique.md](references/playtesting-and-critique.md): critique workflow, symptom → fix table, playtest protocol, telemetry.
- [SOURCES.md](SOURCES.md): every source (~300) with URL and verification status. It is large: search it (e.g. `grep -i hayashida SOURCES.md`) rather than loading it whole. Only quote sources marked Verified word for word.

## Gotchas

- **Project context first:** check the project's instruction file (CLAUDE.md, AGENTS.md, GEMINI.md) or docs for engine, units, player metrics and editor tools before asking. If they're missing, offer [assets/project-context-template.md](assets/project-context-template.md) for the user to fill in.
- **Unknown player metrics:** ask, or state assumed values explicitly (and how to measure them in-engine) before giving any dimension. Unreal = cm, Unity/Godot = m, Source ≈ 1.9 cm/unit.
- **Don't reproduce famous levels** (World 1-1, classic Sokoban sets, well-known maps) when asked for original work; study them, then design something new.
- **"Make it harder" means deeper, not bigger.** For puzzles raise entanglement or add a counter-intuitive move; for platformers tighten a rhythm or combine a known hazard with the new verb. Padding the board is the classic LLM failure.
- **Third-person cameras** need wider corridors and higher ceilings than the capsule suggests; gamepad players rarely adjust camera pitch, so keep critical information near eye level.
- **AI navigation** has its own agent size and needs nav links for drops, ladders and jumps.
- **Don't design for the average player only.** Offer safe, standard and skilful routes where the genre allows; let players choose the hard one.
- **Don't over-guide.** Explicit markers (yellow paint, glow) are for what players must not miss; optional secrets can be subtle if they are fair.
- **Genre conventions are defaults, not laws.** If the user breaks one on purpose, design for their intent.
