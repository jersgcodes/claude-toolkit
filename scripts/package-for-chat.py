#!/usr/bin/env python3
"""Package skills as individual .zip files for upload to claude.ai chat.

claude.ai chat does not install Claude Code plugins. It takes ONE ZIP PER SKILL, under
Settings -> Capabilities -> Upload skill, and each uploaded skill is off by default until
you enable it from the Skills menu in a conversation.

So the plugin is the right unit for Claude Code (CLI, desktop, claude.ai/code) and the
wrong unit for chat. This produces the chat unit from the same source, so there is still
only one place these skills are authored.

CLI-only skills are skipped: they need a checkout, git, or local hooks, and uploading them
to chat produces a skill that cannot do its job. Pass --all to override.

    python3 scripts/package-for-chat.py           # the skills that work in chat
    python3 scripts/package-for-chat.py --all     # every skill, CLI-only included
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import zipfile

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
DIST = PLUGIN / "dist" / "chat-skills"

# claude.ai's published guidance for a skill's full content. Not a hard limit, but a skill
# well past it crowds the conversation it is meant to help.
TOKEN_GUIDANCE = 5000


def est_tokens(chars: int) -> int:
    return chars // 4


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="include CLI-only skills")
    args = ap.parse_args()

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    packaged, skipped, fat = 0, [], []
    for skill_dir in sorted((PLUGIN / "skills").iterdir()):
        md = skill_dir / "SKILL.md"
        if not skill_dir.is_dir() or not md.exists():
            continue
        text = md.read_text()
        if "[CLI-only]" in text and not args.all:
            skipped.append(skill_dir.name)
            continue

        files = [md] + sorted(p for p in skill_dir.rglob("*") if p.is_file() and p != md)
        total = sum(p.stat().st_size for p in files)
        with zipfile.ZipFile(DIST / f"{skill_dir.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for p in files:
                z.write(p, pathlib.Path(skill_dir.name) / p.relative_to(skill_dir))

        tokens = est_tokens(total)
        if tokens > TOKEN_GUIDANCE:
            fat.append((skill_dir.name, tokens))
        packaged += 1
        print(f"  {skill_dir.name:<22} ~{tokens:>5} tokens")

    print(f"\n{packaged} zip(s) in {DIST.relative_to(PLUGIN)}")
    if skipped:
        print(f"skipped {len(skipped)} CLI-only: {', '.join(skipped)}")
    if fat:
        print(f"\nOver claude.ai's ~{TOKEN_GUIDANCE} token guidance, trim before uploading:")
        for name, t in fat:
            print(f"  {name}: ~{t}")
    print("\nUpload at claude.ai -> Settings -> Capabilities -> Upload skill (one zip each).")
    print("Then enable each one from the Skills menu inside a conversation; they are off by default.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
