#!/usr/bin/env python3
"""Copy the design rubrics out of the private design-system repo into this plugin.

The rubrics are authored in ~/claude/design-system and nowhere else. A plugin skill,
however, has to work on a machine that has no such checkout -- claude.ai, a phone, a
fresh laptop -- so the judgement half of the design system travels with the skill as a
generated snapshot.

Only the rubrics travel. The programs (check_contrast.py and friends) stay where they
are: they measure a repo, and there is no repo to measure on the chat side.

    python3 scripts/sync-design-refs.py            # refresh the snapshots
    python3 scripts/sync-design-refs.py --check    # exit 1 if any snapshot is stale
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys

SOURCE_REPO = pathlib.Path("~/claude/design-system").expanduser()
PLUGIN = pathlib.Path(__file__).resolve().parent.parent

# source (relative to design-system)  ->  destination (relative to the plugin)
MANIFEST = {
    "CRAFT-BAR.md": "skills/design-review/references/CRAFT-BAR.md",
}

# NOT synced, deliberately. data-story/STORY-BAR.md and its worked example quote a private
# client-side-encrypted project's findings verbatim, and this plugin is public. Either
# genericise the rubric at source or ship /data-story-check from a private plugin. Do not
# add it here without doing one of those first.

HEADER = """<!--
GENERATED SNAPSHOT -- DO NOT EDIT.

Authored in the design-system repo as {src}, copied here so the skill works on a
machine with no design-system checkout. Edit it there, then run:

    python3 scripts/sync-design-refs.py

Synced: {date}
-->

"""


def rendered(src: pathlib.Path, rel: str) -> str:
    return HEADER.format(src=rel, date=dt.date.today().isoformat()) + src.read_text()


def body(text: str) -> str:
    """The snapshot minus its generated header, so a date bump is not drift."""
    return text.split("-->\n\n", 1)[1] if text.startswith("<!--\n") else text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report drift, write nothing")
    args = ap.parse_args()

    if not SOURCE_REPO.exists():
        print(f"design-system not found at {SOURCE_REPO}", file=sys.stderr)
        print("Nothing to sync. The bundled snapshots are left as they are.")
        return 0 if args.check else 1

    stale = []
    for rel, dest_rel in MANIFEST.items():
        src, dest = SOURCE_REPO / rel, PLUGIN / dest_rel
        if not src.exists():
            print(f"MISSING  {rel} is not in design-system any more")
            stale.append(dest_rel)
            continue
        want = rendered(src, rel)
        have = dest.read_text() if dest.exists() else ""
        if body(have) == body(want):
            print(f"ok       {dest_rel}")
            continue
        stale.append(dest_rel)
        if args.check:
            print(f"STALE    {dest_rel}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(want)
            print(f"synced   {dest_rel}")

    if args.check and stale:
        print(f"\n{len(stale)} snapshot(s) stale. Run without --check.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
