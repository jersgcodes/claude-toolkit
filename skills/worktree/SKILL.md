---
name: worktree
description: [CLI-only] Create or manage isolated git worktrees for parallel feature work without context-switching the main checkout.
allowed-tools: [Bash, Read]
version: 0.1.0
---



# Worktree

Git worktrees let you check out multiple branches simultaneously in separate directories — useful when you want to:

- Try a refactor without dirtying your main branch
- Run two long-running tasks in parallel (one per worktree, one Claude session per worktree)
- Compare two implementations side-by-side
- Review a PR locally without stashing your in-progress work

Inspired by the *Superpowers* framework (using-git-worktrees skill).

---

## Modes

| Argument | Action |
|---|---|
| `<feature-name>` | Create a new worktree at `~/claude/.worktrees/<project>-<feature>/` on a new branch `feature/<feature>` off the current HEAD |
| `list` | Show all worktrees for the current repo |
| `clean` | Show worktrees safe to delete (merged or never-committed) and prompt for removal |
| (none) | Print usage |

---

## Step 1 — Determine current repo

```bash
repo_root=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$repo_root" ]; then
  echo "Not in a git repository. Run /worktree from inside a project."
  exit 1
fi
project_name=$(basename "$repo_root")
```

---

## Step 2 — Handle the argument

### Mode A: Create — `/worktree <feature-name>`

a) Validate `$ARGUMENTS`:
- Must be lowercase alphanumeric + dashes only
- Reject if contains spaces, slashes, or special chars
- Reject if empty

b) Check current branch is clean OR has only safe-to-include changes. Run:
```bash
git status --porcelain
```
If dirty, ask user: "Working tree is dirty. Stash before creating worktree? [y/n]"

c) Create the worktree directory:
```bash
worktree_root="$HOME/claude/.worktrees"
mkdir -p "$worktree_root"
target_dir="$worktree_root/${project_name}-${ARGUMENTS}"
branch_name="feature/${ARGUMENTS}"

git worktree add "$target_dir" -b "$branch_name"
```

d) Confirm and print next steps:
```
Worktree created:
  Path:   $target_dir
  Branch: $branch_name
  Base:   <current HEAD short SHA>

Next:
  cd $target_dir
  # Work normally — commits land on $branch_name
  # When done: git push, merge, then run /worktree clean
```

### Mode B: List — `/worktree list`

```bash
git worktree list
```

Format the output as a table:
```
| Branch | Path | Status |
|---|---|---|
| main | <workspace>/<project> | (current) |
| feature/foo | ~/claude/.worktrees/<project>-foo | dirty (3 files) |
| feature/bar | ~/claude/.worktrees/<project>-bar | clean, 5 commits ahead |
```

To check status per worktree:
```bash
git -C <path> status --porcelain | wc -l   # uncommitted file count
git -C <path> rev-list --count main..HEAD  # commits ahead of main
```

### Mode C: Clean — `/worktree clean`

For each worktree (excluding main):
1. Check if its branch is merged to main: `git branch --merged main | grep <branch>`
2. Check if uncommitted: `git -C <path> status --porcelain`
3. Classify:
   - **Safe to remove** — merged AND clean
   - **Risk** — unmerged commits OR uncommitted changes
   - **Already removed branch but worktree dir exists** — orphaned

Print a table and ask user which to remove. For each confirmed removal:
```bash
git worktree remove <path>
git branch -d <branch>  # optional, only if user wants
```

---

## Step 3 — Standalone worktree pattern

For long-running work, recommend opening a fresh Claude Code session in the worktree directory:

```bash
cd ~/claude/.worktrees/<project>-<feature>
claude   # or: claude -p "..." for headless
```

This keeps each session's context focused on one branch's work — no cross-contamination.

---

## Cost control

- Free skill — only bash commands, no LLM analysis
- Use `model: haiku` (fastest, cheapest tier)

---

## Integration

- Used during: long refactors (`/refactor --apply` for many transformations)
- Used during: experimental spikes (test an idea without committing on main)
- Used during: parallel headless builds (one worktree per `claude -p` session)

---

## Common gotchas

- **Symlinks/`.env` files** — worktrees share the same git history but have separate working directories. If your project relies on local-only files (e.g. `projects.local.yaml`, `.env`), copy them into the new worktree manually.
- **Same branch in two worktrees** — git rejects this. If you need parallel work on the same branch, use stash + create new branch.
- **Disk usage** — each worktree is a full copy of the working tree (not the .git/). For large projects, watch disk space. Run `/worktree clean` regularly.
- **VS Code / IDE** — open the worktree dir as a separate window so it doesn't confuse the file watcher.
