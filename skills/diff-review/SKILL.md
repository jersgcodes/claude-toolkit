---
name: diff-review
description: [CLI-only] Review staged git changes for bugs, privacy issues, debug leftovers, and missing tests before committing. Use before /pre-commit or when asked to review a diff.
allowed-tools: [Read, Grep, Bash]
version: 0.1.0
---



Review staged changes before running pre-commit checks. Do the following steps in order:

**1. Get staged diff**

```bash
git diff --staged
git diff --staged --stat
```

If nothing is staged, print "Nothing staged — run `git add` first." and stop.

**2. Review for obvious issues**

Scan the diff for:

**Bugs:**
- Array/object mutations on state variables (`state.push(`, `state[i] =`)
- Missing `await` on async calls
- Off-by-one errors in loops or slice indices
- Returning inside a loop when the intent looks like it should continue
- Conditional that will always be true or always false

**Privacy (project-specific):**
- Free-text fields (company name, URL, product names, workflow descriptions) being passed to `localStorage.setItem` or storage wrappers
- Any new field added to a session/library save object — flag for privacy review

**Debug leftovers:**
- `console.log(`, `console.error(`, `debugger`
- Commented-out code blocks (more than 2 lines)
- TODO/FIXME comments introduced in this diff

**Test coverage:**
- Source files changed but no corresponding test file in the diff
- Flag each untested source file by name

**3. Report**

```
Diff Review — <N> files changed, <+X/-Y> lines

Bugs: N found
  - <file>:<line> — <description>

Privacy flags: N found
  - <field> added to <storage key> — verify against allowed-fields list

Debug leftovers: N found
  - <file>:<line> — <type>

Missing test updates: N files
  - <filename> changed but no test file in diff

Verdict: CLEAN / WARN / BLOCK
```

- `CLEAN` — nothing found
- `WARN` — debug leftovers or missing tests only (non-blocking)
- `BLOCK` — bugs or privacy violations found

**4. If BLOCK**

List the specific lines to fix. Do not proceed to `/pre-commit` until the blocking issues are resolved.

**5. If CLEAN or WARN**

Print: "Ready for /pre-commit"
