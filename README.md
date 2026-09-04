# Claude Toolkit

A Claude Code **plugin**: 66 skills for design, planning, review, quality and ops, plus one
agent. Usable on the CLI, on the web (claude.ai/code) and on mobile.

Skills use progressive disclosure — a lean `SKILL.md` body plus `references/` loaded on demand —
so they stay light in context and pull detail only when a run needs it.

## Install

```
/plugin marketplace add jersgcodes/claude-toolkit
/plugin install claude-toolkit
```

Invoke a skill by name (`/claude-toolkit:arch-review`) or let Claude choose it from the
description.

## What's inside

| Family | Skills |
|---|---|
| Design and front-end | design-review, design-craft-check, motion-check, style-check, a11y-audit, mobile-audit, responsive-design, visual-mock, component-design, ui-diff, brand-identity, motion-pipeline, data-story-check |
| Planning and architecture | feature-design, api-design, schema-design, arch-review, arch-lesson, decision-record, threat-model, spike, seams |
| Review and quality | code-quality, complexity, refactor, tdd, test-coverage, diff-review, review-pr, type-check, format, perf |
| Security | security-check, secrets-scan, deps-audit, leak-audit, scale-audit |
| Ops and session | wrap-up, status, workspace-status, worktree, checkpoint-all, compact-context, pre-commit, pre-deploy, pre-approve, commit-status, add-cicd, hooks, memory-review, retrospective, postmortem |
| Research and authoring | strategize, learn, explain, fact-check, subagent-task, mcp-scaffold, mcp-audit, build-mode, add-tasks, agents, skills, stack-detect, fetch-fallback, ux-psych-audit |

27 skills are tagged **[CLI-only]** in their description: they need a local checkout, git, or
local hooks, and do nothing useful on web or mobile.

## The design skills and the private design system

`design-review` and `design-craft-check` are two halves that travel differently.

The **numeric floor** is four programs (`check_contrast.py`, `check_system.py`,
`check_consumers.py`, `check_rendered.py`) that live in a separate, private `design-system`
repo. They measure a checkout, so off-machine there is nothing for them to measure. The skills
say `numeric floor not run: no design-system checkout` and continue rather than reporting a
floor that never ran.

The **bar** is judgement and does travel: `CRAFT-BAR.md` is bundled at
`skills/design-review/references/CRAFT-BAR.md` as a generated snapshot. It is authored only in
`design-system`. Refresh it, never edit it here:

```bash
python3 scripts/sync-design-refs.py           # refresh
python3 scripts/sync-design-refs.py --check   # exit 1 if the snapshot is stale
```

## Platform support

| Component | CLI | Web | Mobile |
|---|---|---|---|
| Skills | yes | yes | yes |
| Agents | yes | yes | yes |
| Remote MCP servers | yes | yes | yes |
| Hooks (local automation) | yes | no | no |

## License

MIT
