---
name: checkpoint-all
description: [CLI-only] Flush every workspace repo's uncommitted and unpushed work to its remote, so a cloud agent cloning from GitHub sees the latest code rather than stale code. Dry-run by default; pass --go to actually commit and push. Use before dispatching remote agents, before a handoff, or when local and remote have diverged.
allowed-tools: [Bash]
version: 0.1.0
---

# checkpoint-all

Flush all workspace repos' uncommitted / unpushed work to GitHub, so a code agent that
**clones from GitHub sees your latest** — not stale code (an agent's PR based on stale code
is the local↔remote divergence trap).

Run the script — **dry-run by default**; it never commits to `main`/`master`:

```bash
python3 ~/claude/scripts/checkpoint-all.py $ARGUMENTS
```

- **No args → dry-run:** report, per repo, what *would* be committed/pushed. This doubles as a
  one-glance map of workspace git state.
- **`--go` → act:** commit each dirty repo's WIP to its **current branch** (`--no-verify` — it's
  a snapshot, not clean history) and push; repos dirty on `main`/`master` are reported and
  **skipped** for the user to handle by hand.

**Always** run the dry-run first, show the user the output, and get an explicit nod before
running again with `--go`. Force-committing across ~40 repos is powerful and a little dangerous.
