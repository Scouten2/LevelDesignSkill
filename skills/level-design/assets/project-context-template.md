# Project Context Template

Paste this block into the project's instruction file so the skill can use real numbers instead of assumed ones: `CLAUDE.md` (Claude Code), `AGENTS.md` (OpenAI Codex) or `GEMINI.md` (Gemini CLI). Write "assumed" next to any number not read from code or measured in-engine. For platformers, also fill [movement-kit.md](movement-kit.md).

```markdown
## Level design context
- Engine and version: <e.g. Unreal Engine 5.x>
- Units and axes: <e.g. 1 uu = 1 cm, Z-up>
- Player collision: <e.g. capsule radius 42 / half-height 96>
- Movement: <walk / sprint / crouch speeds, jump height or JumpZVelocity, gravity scale, max safe fall>
- Camera: <first- or third-person, FOV, boom length>
- AI navigation: <agent radius and height, nav links for drops, ladders, jumps>
- Grid or tile size (if any): <e.g. 1 tile = 16 px, or 4 m modular kit>
- Editor tools: <MCP server, editor scripting, how to spawn or move actors>
- Level file formats: <tile map format, glyph legend, where level files live>
- Constraints: <platform, performance budgets, accessibility requirements>
```
