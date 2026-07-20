# AGENTS.md

> Template for `AGENTS.md`-based coding agents (OpenAI Codex, Cursor, and other tools that read a
> repo-root `AGENTS.md`). Copy this into a project root and edit the placeholders. It mirrors the
> intent of a Claude Code `CLAUDE.md` in the format those tools expect.

## About this project
<!-- One or two lines: what this repo is, primary language, how to run it. -->
- Language: <e.g. Python 3.12 / TypeScript>
- Run tests: `<command>`
- Build / lint / format: `<commands>`

## Working agreements
- Prefer the simplest solution that meets the requirement; avoid over-engineering.
- Make minimal, focused changes; don't refactor unrelated code unless asked.
- No dead code — remove rather than comment out.
- Write/keep tests alongside new code; tests must pass before a change is "done".
- Never commit secrets. Work on a feature branch, not `main`, unless told otherwise.
- Be concise and direct.

## Skills available
This project's team uses a library of 52 review/design/planning/quality skills (see
`claude-toolkit`). When a task matches one, follow that skill's steps:

- **Design:** api-design, schema-design, component-design, responsive-design, a11y-audit, visual-mock
- **Planning:** feature-design, spike, decision-record, threat-model, arch-review
- **Review & quality:** code-quality, complexity, refactor, seams, tdd, review-pr, diff-review, security-check, secrets-scan, deps-audit, type-check
- **Research & ops:** deep-research, subagent-task, mcp-scaffold, mcp-audit, postmortem, wrap-up

Full skill instructions: install the plugin (`/plugin marketplace add jersgcodes/claude-toolkit`)
or read `chatgpt-knowledge-bundle.md` in this repo's `exports/`.

## Guardrails
<!-- Add project-specific do-not-touch paths, deploy rules, data-handling constraints, etc. -->
