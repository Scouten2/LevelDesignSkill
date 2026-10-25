# Level Design Skill

An engine-agnostic [Agent Skill](https://agentskills.io) that makes an AI coding agent (Claude Code, OpenAI Codex or Gemini CLI) work like a senior level designer: brief → structure → beat chart → spaces → blockout spec → playtest, grounded in practitioner theory (Dan Taylor, Nintendo's kishōtenketsu, Valve, Naughty Dog, id, FromSoftware, Arkane, The Level Design Book, Totten, Smith & Worch and more), with a guide for each genre.

It covers design, critique and layout verification (bundled Python checkers), with no engine tooling. Hook up your editor tools (an Unreal MCP server, editor scripting, etc.) yourself in your project's instruction file (`CLAUDE.md`, `AGENTS.md` or `GEMINI.md`). This skill then supplies the design judgment for what to build.

## Highlights

- **Verify, don't assert.** Eight bundled Python scripts (stdlib only) check layouts instead of trusting the model's spatial reasoning: tile-map lint, a Sokoban-family puzzle solver with bypass/shortcut/uniqueness tests and validated difficulty metrics, platformer jump-reachability from a movement kit (including a "does this level actually teach the move?" test), a 3D jump-link checker for traversal routes and jump puzzles (respawns past one-way links, depth-axis jumps, teasers, tier estimate), lock-and-key graph checks, puzzle dependency charts, beat-chart linting and layout comparison.
- **Jump puzzles and 3D traversal**: hidden detours (Elden Ring-style lift step-offs and ledge routes), optional world jumping puzzles (Guild Wars 2, Destiny), challenge chambers (Jedi), puzzle-platforming and ability-gated routes (Supraland), and movement-map difficulty tiers (KZ, obbies, Celeste mods), with a jump-sequence spec template and a worked example.
- **Deep puzzle and platformer guides** (3 + 6 files) built from primary sources: Blow and ten Bosch, Traynor, Teikari, Gilbert, Valve's Portal commentary, Jarušek & Pelánek; Hayashida, Celeste's released code, McMillen, Keren's camera article, World 1-1 measured from its tile map.
- **Gameplay first and verticality** as core stances: grey description test, verb-per-space table, art-pass re-check; eight uses of height, "see it, then reach it from an unexpected height", a fairness rule for hidden vertical routes, drop bands, a Z-axis checklist.
- **Fun checks** with labelled evidence strength, a weighted **review rubric**, and a level-scope **accessibility** guide with photosensitivity limits.
- **18 genre guides**, from shooters, stealth and horror to tactics, RTS, tower defense, casual/mobile, VR, co-op PvE, boss arenas and raids, racing and UGC platforms.
- **Sourced, not invented.** `SOURCES.md` lists ~300 sources with their verification status.
- **Works with Claude Code, OpenAI Codex and Gemini CLI** from one skill folder.

## What's inside

```
skills/level-design/
├── SKILL.md                 # hub: core stance, workflow, scripts, output conventions, routing
├── SOURCES.md               # every source with URL and verification status (search it, don't load it whole)
├── assets/                  # level brief, puzzle insight card, movement kit, jump-sequence spec and
│                            # worked example, playtest hypothesis card, project-context template
├── agents/openai.yaml       # optional Codex / ChatGPT display metadata (other tools ignore it)
├── scripts/                 # grid_lint, grid_puzzle_solve, platformer_reach, jump_links, graph_check,
│   └── tests/               # dependency_chart, beat_lint, level_metrics (+ 93 unit tests)
└── references/
    ├── principles.md  layout-and-flow.md  verticality.md  metrics.md  process.md
    ├── grid-conventions.md  fun-checks.md  review-rubric.md  accessibility.md  playtesting-and-critique.md
    ├── puzzle-craft.md  puzzle-sequencing.md  puzzle-verification.md
    ├── platformer-craft.md  platformer-metrics.md  platformer-camera.md  platformer-checks.md
    ├── platformer-3d.md  jump-puzzles.md
    └── genre-*.md, boss-arenas-and-raids.md   # 18 genre guides
```

The agent loads `SKILL.md` when a task involves level design, and loads a reference or genre file only when that task needs it. The scripts need only Python 3.8+ (`python3 -I scripts/<name>.py --help`); run the tests with `python3 -I -m unittest discover -s scripts/tests` from the skill folder.

## Install

The skill is one folder, `skills/level-design/`, in the open [Agent Skills](https://agentskills.io/specification) format. Each tool below reads that same folder; the repo also carries a package manifest for each tool's plugin or extension system.

| Tool | Manifest in this repo |
|---|---|
| Claude Code | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| OpenAI Codex | `plugin.json`, `.agents/plugins/marketplace.json`, `skills/level-design/agents/openai.yaml` |
| Gemini CLI | `gemini-extension.json` |

### Claude Code

As a plugin (recommended):
```
/plugin marketplace add Scouten2/LevelDesignSkill
/plugin install level-design@level-design
```

Or copy the folder:
```bash
# personal (all projects)
cp -r skills/level-design ~/.claude/skills/
# or project-only (e.g. inside your Unreal project)
cp -r skills/level-design <your-project>/.claude/skills/
```

### claude.ai

Upload a zip of the skill under Settings → Capabilities → Skills: download `level-design.skill` from this repo's [Releases](https://github.com/Scouten2/LevelDesignSkill/releases) page, or zip the `skills/level-design` folder yourself with `level-design/` at the zip root. The bundled scripts need code execution enabled.

### OpenAI Codex

As a plugin:
```bash
codex plugin marketplace add Scouten2/LevelDesignSkill
codex plugin add level-design@level-design
```

Or copy the folder (Codex reads `.agents/skills/` from the working directory up to the repo root, and `~/.agents/skills/`):
```bash
cp -r skills/level-design ~/.agents/skills/                 # personal
cp -r skills/level-design <your-project>/.agents/skills/    # project-only
```

### Gemini CLI

As an extension:
```bash
gemini extensions install https://github.com/Scouten2/LevelDesignSkill
```

Or as a standalone skill:
```bash
gemini skills install https://github.com/Scouten2/LevelDesignSkill --path skills/level-design
# or copy it: Gemini CLI reads .gemini/skills/ and .agents/skills/ (workspace) and ~/.gemini/skills/ (personal)
```

`.agents/skills/` is read by both Codex and Gemini CLI, so one project-level copy serves both.

## Using it

Just ask about level design. For example:
- "Design a 15-minute stealth level in a museum that teaches the disguise mechanic."
- "Here's my arena blockout (screenshot). Why do players keep camping the back corner?"
- "Plan a metroidvania region gated by a grapple hook, with a lock-and-key graph."
- "Critique this multiplayer map layout for 5v5 attack/defense."

The agent picks the skill up from the request. To invoke it explicitly: in Claude Code `/level-design` (manual install) or `/level-design:level-design` (plugin install); in Codex `$level-design` (or `/skills`); in Gemini CLI, `/skills` lists it and the model activates it when the task matches.

## Using it with Unreal (or any engine)

Put engine facts in your project's instruction file (`CLAUDE.md` for Claude Code, `AGENTS.md` for Codex, `GEMINI.md` for Gemini CLI) so the skill can use real numbers. A fuller template is in [`skills/level-design/assets/project-context-template.md`](skills/level-design/assets/project-context-template.md). For example:

```markdown
## Level design context
- Engine: Unreal Engine 5.x (1 uu = 1 cm, Z-up)
- Player: capsule radius 42 / half-height 96, MaxWalkSpeed 500, JumpZVelocity 700, GravityScale 1
- Camera: third-person, FOV 90
- Editor tools: <your MCP server / scripting setup>
```

## Sources

In the skill files, untagged claims come from developer statements or primary sources; **[convention]** marks practitioner defaults and unsourced numbers, **[contested]** and **[unverified]** mark the rest. `SOURCES.md` gives each source's status.

## Credits

Written by Claude (Anthropic) for Scouten2, who maintains it.

## License

MIT
