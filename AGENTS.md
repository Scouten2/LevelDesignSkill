# Contributor guide (for any coding agent working in this repo)

This repo packages one Agent Skill, `skills/level-design/`, for Claude Code, OpenAI Codex and Gemini CLI. This file is for working *on* the skill; it is not loaded by people who install it.

## Layout

- `skills/level-design/`: the skill itself (open [Agent Skills](https://agentskills.io/specification) format). `SKILL.md` is the single source of truth for every tool.
- Package manifests, one set per tool, all pointing at the same `skills/` folder:
  - Claude Code: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
  - Codex: `plugin.json`, `.agents/plugins/marketplace.json`, `skills/level-design/agents/openai.yaml`
  - Gemini CLI: `gemini-extension.json`
- `dist/level-design.skill` (built locally, git-ignored): zip of `skills/level-design/` for claude.ai upload and `gemini skills install`. Attach it to a GitHub Release instead of committing it.

## Rules

- **Keep the skill model-neutral.** In `SKILL.md`, `references/` and `assets/`, address the model as "you" and don't name a specific model or product. Refer to "the project's instruction file (CLAUDE.md, AGENTS.md, GEMINI.md)", not one of them alone.
- Keep `SKILL.md` under 500 lines and its `description` under 1024 characters; `name` must stay `level-design` (matches the folder).
- Scripts are Python 3.8+ standard library only, run as `python3 -I scripts/<name>.py`.
- **Version bumps:** change the version in all of `skills/level-design/SKILL.md` (`metadata.version`), `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `plugin.json` and `gemini-extension.json` together.
- Don't add a root `GEMINI.md`: Gemini CLI would load it into every session of anyone who installs the extension.

## Checks before committing

```bash
cd skills/level-design && python3 -I -m unittest discover -s scripts/tests
claude plugin validate .                      # Claude Code manifest (from the repo root)
gemini extensions link . && gemini skills list  # Gemini CLI picks up the skill
codex plugin marketplace add . && codex plugin list   # Codex sees level-design@level-design
```

Build the release zip (from the repo root):

```bash
rm -f dist/level-design.skill
(cd skills && zip -rqD ../dist/level-design.skill level-design -x 'level-design/evals/*' '*__pycache__*' '*.pyc')
```
