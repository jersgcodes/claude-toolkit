---
name: retrospective
description: [CLI-only] Run an end-of-sprint retrospective based on git history and task state.
version: 0.1.0
---


Run an end-of-sprint retrospective based on git history and task state. Do the following steps in order:

**1. Get the time range**
If a date range is provided as an argument (`$ARGUMENTS`, e.g. "last 2 weeks"), use it.
Otherwise default to the last 14 days: `git log --since="14 days ago" --oneline`.

**2. What shipped**
Summarise commits into logical features/fixes (group related commits). Focus on user-visible changes.

**3. What didn't ship**
If `docs/tasks.md` exists, list any tasks that were `[in_progress]` or `[pending]` at the start of the period and are still not done.

**4. What slowed us down**
Look for signals in the git log:
- Multiple commits fixing the same thing (reverts, "fix fix", "actually fix")
- Long gaps between commits on the same feature
- Commits with "debug", "temp", "wip" that stayed in for a long time

**5. Format output**

---
**Shipped**
- [bullet list]

**Not shipped / carried over**
- [bullet list or "None"]

**Friction points**
- [patterns that slowed things down]

**One thing to do differently next sprint**
- [single most impactful process change based on the above]
---
