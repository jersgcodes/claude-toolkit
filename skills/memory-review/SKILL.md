---
name: memory-review
description: [CLI-only] Audit and clean stale memory files across all projects.
version: 0.1.0
---


Audit and clean stale memory files across all projects. Do the following steps in order:

**1. Find all memory directories**

```bash
find ~/.claude/projects -name "MEMORY.md" | sort
```

For each, note the project path it belongs to.

---

**2. For each project memory**

Read `MEMORY.md` and all linked memory files in the same directory.

For each memory entry assess:

**Is it still accurate?**
- `project` type memories decay fast — check if the described state still matches reality (e.g. a feature listed as "not yet built" may now be built)
- `feedback` type memories should persist unless the user's preference has clearly changed
- `user` type memories should persist unless the described role/knowledge has changed
- `reference` type memories — check if the referenced system/URL is still relevant

**Is it still load-bearing?**
- Would losing this memory cause Claude to repeat a mistake or miss important context?
- If it describes something already obvious from the current codebase, it's redundant

**Is it specific enough to be useful?**
- Vague memories like "user prefers simple solutions" are already in CLAUDE.md — redundant here
- Useful memories are specific: "don't mock the database", "land on Step 4 after archetype load"

---

**3. Categorise each memory**

- `KEEP` — accurate, specific, load-bearing
- `UPDATE` — mostly accurate but needs a small edit
- `STALE` — describes a state that no longer exists
- `REDUNDANT` — already covered by CLAUDE.md or obvious from the codebase

---

**4. Apply changes**

- For `UPDATE`: edit the memory file with the correction
- For `STALE` or `REDUNDANT`: remove the entry from `MEMORY.md` and delete the file
- For `KEEP`: no action

---

**5. Report**

```
Memory Review

Project: <project-name>
  KEEP:       N memories
  UPDATED:    N memories — <list of what changed>
  REMOVED:    N memories — <list of what was removed and why>

Project: <project-name>
  ...

Total: N kept, N updated, N removed
```

If no changes were needed: "All memories current — no action taken."
