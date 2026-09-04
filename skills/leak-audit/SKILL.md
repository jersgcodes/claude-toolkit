---
name: leak-audit
description: [CLI-only] Audit a repo for private context before it is made public: internal notes, client and codenames, unshipped plans, private references, and the same leaks buried in git history across every branch, not just main. Use before open-sourcing a repo, flipping it public, or sharing a clone.
allowed-tools: [Read, Grep, Glob, Bash]
version: 0.1.0
---

# Leak Audit — is this repo safe to make public?

The private→public boundary is a **leak boundary**: you build with context you can't
share (internal rationale, client names, unshipped plans), and a public repo exposes
**every branch and all commit history, not just `main`.** This checks that none of it
leaked into what people would be able to read.

Different from `/secrets-scan` (credentials) — this is about *context*: names, notes,
and rationale that are fine internally but must not ship.

## Steps

1. **Run the engine** (scans tracked file contents + commit messages + branch names):
   ```bash
   python3 ~/.claude/scripts/leak_audit.py <path>
   ```
   (Installed copy; source is `claude-config/scripts/leak_audit.py`.) It uses the built-in
   markers plus your private denylist at `~/.claude/leak-denylist.txt` (copy it from
   `claude-config/leak-denylist.txt.example` and fill in client/codenames/private slugs).

2. **Triage each finding** — for every hit, decide:
   - **Real leak** → must be scrubbed before publishing (edit the file; if it's in a
     commit message or branch, the history itself carries it — see step 4).
   - **False positive** → note why it's safe (e.g. a public product name that happens to
     match a denylist word). Suggest tightening the denylist term.

3. **Check the git surface specifically.** File edits don't remove leaks already in
   history. If a finding is in a **commit message** or a **branch name**, flag that the
   *public repo must not carry this history* — the safe pattern is a **fresh, generated
   export** (clean history containing only the scrubbed content), never a fork/mirror of
   the private repo.

4. **Report**: list confirmed leaks (file/commit/branch + term), separate the false
   positives, and state clearly whether the repo is **safe to publish** or **must be
   scrubbed first**. If any confirmed leak lives in history, the recommendation is a clean
   re-export, not an in-place edit.

## Notes
- Exit code is non-zero when anything is found — wire it into a pre-push hook on public
  repos, or the private→public export step, to gate publishing.
- Keep the denylist current: every time you add a client/codename internally, add it here.
