# Claude Toolkit

A Claude Code **plugin**: 65 skills for design, planning, review, quality and ops, plus one
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
| Design and front-end | design-review, design-craft-check, motion-check, style-check, a11y-audit, mobile-audit, responsive-design, visual-mock, component-design, ui-diff, brand-identity, motion-pipeline |
| Planning and architecture | feature-design, api-design, schema-design, arch-review, arch-lesson, decision-record, threat-model, spike, seams |
| Review and quality | code-quality, complexity, refactor, tdd, test-coverage, diff-review, review-pr, type-check, format, perf |
| Security | security-check, secrets-scan, deps-audit, leak-audit, scale-audit |
| Ops and session | wrap-up, status, workspace-status, worktree, checkpoint-all, compact-context, pre-commit, pre-deploy, pre-approve, commit-status, add-cicd, hooks, memory-review, retrospective, postmortem |
| Research and authoring | strategize, learn, explain, fact-check, subagent-task, mcp-scaffold, mcp-audit, build-mode, add-tasks, agents, skills, stack-detect, fetch-fallback, ux-psych-audit |

## Two surfaces, two artifacts

This repo produces **two different things**, because Claude Code and claude.ai chat consume
skills in incompatible ways.

| | For Claude Code | For claude.ai chat |
|---|---|---|
| Unit | the plugin | one `.zip` per skill |
| How it arrives | `/plugin install` from the marketplace | Settings -> Capabilities -> Upload skill |
| Gets | all 65 skills, 7 agents | the 38 that work without a checkout |
| Invocation | `/claude-toolkit:name`, or auto by description | enabled per conversation from the Skills menu |
| Can use | git, your repos, hooks, agents | code execution, bundled files, connectors |

27 skills are tagged **[CLI-only]** in their description. They need a local checkout, git or
local hooks, and are excluded from the chat bundle rather than shipped as skills that cannot
do their job.

Build the chat bundle:

```bash
python3 scripts/package-for-chat.py     # 38 zips + INDEX.md in dist/chat-skills/
```

`INDEX.md` is the upload list: what each skill does, its context cost, and how much sits on
disk as bundled references. Upload one zip at a time; chat has no bulk import.

**The numeric design floor does not travel from this repo.** It needs the private
`design-system` CSS. `claude-toolkit-private` ships `/craft-floor`, which carries the scales
and runs the same measurement on a pasted file.

`data-story-check` used to live here. It moved to the private companion plugin
[`claude-toolkit-private`](https://github.com/jersgcodes/claude-toolkit-private), because its
rubric quotes a private project's findings verbatim and a skill without its bar judges by taste.

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
