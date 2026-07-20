---
name: skills
description: [CLI-only] List all available slash commands and what they do. Use when asking "what skills exist", "what commands are available", or "what can I run".
allowed-tools: [Read, Glob]
version: 0.1.0
---



List all available skills (slash commands) and what they do. Do the following steps in order:

**1. Read global skills**
List all `.md` files in `~/.claude/commands/` and read the first non-empty line of each as the description.

**2. Read project skills**
List all `.md` files in `.claude/commands/` (relative to current working directory) and read the first non-empty line of each.

**3. Print a formatted table**

**Global skills** (available in all projects):
| Skill | Description |
|---|---|
| /skill-name | first line of the md file |

**Project skills** (this project only):
| Skill | Description |
|---|---|
| /skill-name | first line of the md file |

Strip the `.md` extension for the skill name. Sort alphabetically within each group.

**4. Usage reminder**
Print at the bottom:
> Type `/skill-name` to run a skill. Skills in `.claude/commands/` override global skills with the same name.
