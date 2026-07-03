# Claude Toolkit

A Claude Code **plugin** of design, planning, research, review, and quality skills — usable on the **CLI, web (claude.ai/code), and mobile**.

Skills use the progressive-disclosure pattern: a lean `SKILL.md` body plus on-demand `references/` files, so they stay light in context and load detail only when needed.

## Install

```
/plugin marketplace add jersgcodes/claude-toolkit
/plugin install claude-toolkit
```

Then invoke any skill by name (e.g. `/claude-toolkit:arch-review`) or let Claude auto-invoke by description.

## What's inside

| Family | Skills |
|---|---|
| Design | api-design, schema-design, component-design, responsive-design, a11y-audit, visual-mock, motion-pipeline |
| Planning | feature-design, spike, decision-record, threat-model |
| Review & quality | code-quality, complexity, refactor, seams, tdd, review-pr, arch-review |
| Research & ops | deep-research, subagent-task, mcp-scaffold, mcp-audit, postmortem, wrap-up |

Skills tagged **[CLI-only]** in their description depend on a local terminal (git, local hooks) and are no-ops on web/mobile.

## Platform support

| Component | CLI | Web | Mobile |
|---|---|---|---|
| Skills | ✅ | ✅ | ✅ |
| Agents | ✅ | ✅ | ✅ |
| Remote MCP servers | ✅ | ✅ | ✅ |
| Hooks (local automation) | ✅ | — | — |

## License

MIT
