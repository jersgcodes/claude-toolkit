# Exports — use these skills outside Claude Code

The 52 skills in this toolkit are portable markdown. Only **Claude Code auto-invokes** them; in
other tools you load them. This folder packages them for that.

| File | For |
|---|---|
| `chatgpt-knowledge-bundle.md` | Upload as **Knowledge** to a ChatGPT Custom GPT / add to a Project (all 52 skills + references inlined) |
| `chatgpt-system-instructions.md` | Paste into the GPT/Project **Instructions** (role + skill index + how to apply) |
| `AGENTS.md` | Template for Codex / Cursor / other `AGENTS.md`-based tools |

## Set up a ChatGPT "Dev Assistant" (Custom GPT)
1. ChatGPT → **Explore GPTs → Create**.
2. **Instructions:** paste `chatgpt-system-instructions.md`. Edit the *"Your standards"* section at the bottom to add your own coding standards (e.g. from your `CLAUDE.md`).
3. **Knowledge:** upload `chatgpt-knowledge-bundle.md`.
4. Save (private to you, or share within your org). Now ask it to plan/review/design and it follows the skill steps.

## Set up as a ChatGPT Project (simpler, no GPT needed)
1. ChatGPT → **Projects → New**.
2. **Project instructions:** paste `chatgpt-system-instructions.md` (+ your standards).
3. **Files:** add `chatgpt-knowledge-bundle.md`.
4. Chat inside the project.

> **Note:** ChatGPT does **not** auto-invoke skills by description like Claude Code — it retrieves
> from the knowledge file. Naming the skill ("use `/threat-model`") gives the most reliable result.
> `[CLI-only]` skills (git/tests/local tools) become *guidance* in ChatGPT, not executed steps.

## Generic LLM / other tools
- Any chat model: paste `chatgpt-system-instructions.md`, then paste the relevant skill section from `chatgpt-knowledge-bundle.md` when you need it.
- Prefer many files over one bundle? The 52 individual skills live in `../skills/<name>/SKILL.md`.

## Division of labour (if you also use Claude Code)
- **Claude Code** — agentic coding *in your repos*; these skills run natively.
- **ChatGPT (Custom GPT / Project)** — planning, design reviews, threat models, explaining code, and (with Code Interpreter) data/analysis work. It's the complement, not a repo coding agent.
