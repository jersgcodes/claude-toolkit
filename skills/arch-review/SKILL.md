---
name: arch-review
description: Review the codebase architecture to identify modularisation opportunities and reduce context wastage when working with Claude.
version: 0.1.0
---


Review the codebase architecture to identify modularisation opportunities and reduce context wastage when working with Claude. Do the following steps in order:

**Note:** This skill checks macro-level structure (modules, boundaries, file organization). For micro-level performance optimization (algorithms, data structures, hot paths), run `/optimize` after this.

**0. Detect stack first**

Run `/stack-detect` (or manually detect) to identify the project's tech stack. This determines:
- Which file extensions to scan (`.js`/`.jsx` for Node, `.py` for Python, `.ts`/`.tsx` for TypeScript, etc.)
- Which tools are applicable (eslint vs ruff, vitest vs pytest, tsc vs mypy)
- Which pre-commit hooks make sense (don't add tsc for JSX projects)

Use the detected stack for all subsequent steps.

**1. Find large files**

List all source files (excluding node_modules, dist, .git, migrations, generated files) and their line counts. Flag any file over 300 lines as a modularisation candidate.

Auto-detect the right find command based on stack:
- **Node.js/JSX**: `find . -name "*.js" -o -name "*.jsx" | grep -v "node_modules\|dist\|\.git" | xargs wc -l | sort -rn | head -20`
- **TypeScript**: `find . -name "*.ts" -o -name "*.tsx" | grep -v "node_modules\|dist\|\.git" | xargs wc -l | sort -rn | head -20`
- **Python**: `find . -name "*.py" | grep -v "__pycache__\|\.git\|venv\|\.venv" | xargs wc -l | sort -rn | head -20`
- **Go**: `find . -name "*.go" | grep -v vendor | xargs wc -l | sort -rn | head -20`

**2. Identify agent opportunities**

For each large file, identify which functions/sections are logically independent and could be delegated to a Claude subagent without needing the full file context. Flag these patterns:
- Functions that only read (no writes) — good for Explore agents
- Functions that write to a single output file — good for isolated write agents
- Test suites that are independent of each other — can run in parallel agents
- Data files or content packs — can be audited without full codebase context
- Pure data (no logic) vs data + functions — pure data files rarely need splitting

**3. Map coupling hotspots**

Find files that are imported by many others (high fan-in). These are hardest to refactor but most important to understand.

Auto-detect the right grep based on stack:
- **JS/JSX/TS/TSX**: `grep -rh "from ['\"]" --include="*.js" --include="*.jsx" . | grep -v node_modules | sed "s/.*from ['\"]//;s/['\"].*//" | grep "^\." | sort | uniq -c | sort -rn | head -15`
- **Python**: `grep -rh "from \|import " --include="*.py" . | grep -v __pycache__ | sort | uniq -c | sort -rn | head -15`

**4. Suggest splits**

For each file over 300 lines, suggest a concrete split:
- What logical groupings exist?
- What would each new file's responsibility be (one-sentence description)?
- Which Claude agent type is best suited to work on each part independently?
- For pure data files: is splitting worth it? (Often no — cross-validation tests are more valuable than splitting data)

Generic agent mapping (adapt to project):

| File type | Best agent | Why |
|---|---|---|
| Pure data files (JSON, constants) | content-audit or Explore | Self-contained, read-only |
| UI components (React, Vue) | react-auditor or general-purpose | Isolated per component |
| API routes / handlers | general-purpose | Needs context of data layer |
| Test files | general-purpose (parallel) | Independent per test suite |
| Configuration / scripts | general-purpose | Usually small, rarely split |
| Large view components | general-purpose | Split into sub-components |

**5. Identify what can be parallelised**

List tasks that could be sent to multiple Claude agents simultaneously (no data dependencies between them).

**6. Check pre-commit / CI alignment**

Verify that pre-commit hooks and CI config match the detected stack:
- JSX project should NOT have `tsc --noEmit` hook
- Python project should NOT have eslint
- If `.pre-commit-config.yaml` exists, flag mismatches with detected stack

**7. Print a summary**

Format:
---
**Stack detected:** [e.g., Vite + React (JSX), no TypeScript]

**Files over 300 lines (modularisation candidates):**
- `file.js` (N lines) — suggested split: [description]

**Highest coupling (imported by most files):**
- `file.js` — imported by N files

**Agent parallelisation opportunities:**
- [Task A] + [Task B] can run simultaneously using two agents

**Pre-commit / CI mismatches:**
- [any hooks that don't match the stack]

**Top 3 recommended refactors (highest impact on Claude context efficiency):**
1. [specific refactor with new file names]
2. ...
3. ...
---

**8. Regenerate architecture docs**

If `docs/architecture.md` exists, update the Mermaid diagrams and key files table to reflect any new files found.

If `scripts/gen-architecture.ts` or equivalent exists, flag it for the user to run rather than running automatically.

Note: architecture docs use **Mermaid** (not draw.io). Diagrams render natively in GitHub.

**IMPORTANT: Always branch before executing refactors.** Use `git checkout -b refactor/<name>` before making changes. Verify the split files are valid before replacing the original.

Keep it actionable. Focus on what reduces the number of lines Claude must read to complete a typical task.
