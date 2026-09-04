#!/usr/bin/env python3
"""Logo construction kit: run the seven tests, export the asset set.

Stdlib only, offline. It does not draw the mark for you -- it makes the tests
cheap enough that you actually run them, which is the part everyone skips.

The tests are from LOGO-METHOD.md. Most marks die on reduction and silhouette,
and finding that out after you have committed is the expensive way.

  python3 logo_kit.py --list
  python3 logo_kit.py --mark blaze --out kit
"""
from __future__ import annotations
import argparse, shutil
from pathlib import Path

BRAND = "#008287"

# Marks as pure geometry. Add one here rather than editing SVG by hand, so the
# construction stays stated rather than drawn.
MARKS: dict[str, dict] = {
    "blaze": {
        "label": "Trail blaze",
        "body": '<rect x="9" y="4" width="7" height="11" rx="3.5"/>'
                '<rect x="16" y="17" width="7" height="11" rx="3.5"/>',
        "stroke": 2.6,
        "note": "Bar 7u x 11u, radius = half width (true semicircle ends). "
                "Second bar offset one bar-width across, 2u down.",
    },
    "cairn": {
        "label": "Cairn",
        "body": '<rect x="10" y="20.5" width="12" height="6" rx="3"/>'
                '<rect x="12" y="13" width="8" height="6" rx="3"/>'
                '<rect x="13.6" y="6" width="4.8" height="5.6" rx="2.4"/>',
        "stroke": 2.4,
        "note": "Three stones, widths 12/8/4.8u, each centred on 16u.",
    },
    "tally": {
        "label": "Tally",
        "body": '<path d="M8 8v16M13.3 8v16M18.6 8v16M24 8v16M6 22 26 10"/>',
        "stroke": 2.6,
        "note": "Four uprights on a 5.3u pitch, one crossbar at 30 degrees.",
    },
    "frame": {
        "label": "Focus brackets",
        "body": '<path d="M6 11V7.5A1.5 1.5 0 0 1 7.5 6H11M21 6h3.5A1.5 1.5 0 0 1 26 7.5V11'
                'M26 21v3.5a1.5 1.5 0 0 1-1.5 1.5H21M11 26H7.5A1.5 1.5 0 0 1 6 24.5V21"/>'
                '<circle cx="16" cy="16" r="4.6"/>',
        "stroke": 2.6,
        "note": "Corners span 5u, inset 6u. Centre circle r=4.6u.",
    },
}


def svg(m: dict, size: int, stroke: float | None = None, colour: str = "currentColor",
        extra: str = "", wrap: str = "") -> str:
    sw = stroke if stroke is not None else m["stroke"]
    inner = f'<g transform="{wrap}">{m["body"]}</g>' if wrap else m["body"]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="{size}" height="{size}" '
            f'fill="none" stroke="{colour}" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" {extra}>{inner}</svg>')


def build(key: str, outdir: Path) -> None:
    m = MARKS[key]
    outdir.mkdir(parents=True, exist_ok=True)

    # ---- asset set. SVG only: it scales, and a favicon.svg is enough today.
    assets = {
        "mark-brand.svg": svg(m, 32, colour=BRAND),
        "mark-black.svg": svg(m, 32, colour="#141516"),
        "mark-white.svg": svg(m, 32, colour="#ffffff"),
        "favicon.svg": svg(m, 32, stroke=m["stroke"] * 1.55, colour=BRAND),
        "icon-app.svg": (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">'
                         f'<rect width="64" height="64" rx="14" fill="{BRAND}"/>'
                         f'<g transform="translate(16 16) scale(1)">'
                         f'{svg(m, 32, stroke=m["stroke"] * 1.15, colour="#ffffff").split(">", 1)[1]}'
                         f'</g></svg>'),
    }
    for name, data in assets.items():
        (outdir / name).write_text(data)

    # ---- the seven tests, as a contact sheet the browser renders
    sizes = [16, 20, 24, 32, 48, 72]
    reduction = "".join(
        f'<figure><div class="s">{svg(m, s, stroke=m["stroke"] * (1 + (48 - s) * 0.018), colour=BRAND)}</div>'
        f'<figcaption>{s}px</figcaption></figure>' for s in sizes)
    # Stroke marks have no true silhouette, so approximate mass with a heavy stroke.
    silhouette = "".join(
        f'<figure><div class="s">{svg(m, 64, stroke=w, colour="#141516")}</div>'
        f'<figcaption>stroke {w}</figcaption></figure>' for w in (2.6, 5, 8, 11))
    rot = "".join(
        f'<figure><div class="s">{svg(m, 56, colour=BRAND, wrap=t)}</div><figcaption>{n}</figcaption></figure>'
        for n, t in (("0°", ""), ("90°", "rotate(90 16 16)"), ("180°", "rotate(180 16 16)"),
                     ("mirror", "translate(32 0) scale(-1 1)")))

    (outdir / "tests.html").write_text(f"""<!doctype html><meta charset=utf-8>
<title>{m['label']} — logo tests</title>
<style>
 body{{font:15px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
   background:#fbfbfa;color:#1a1a19;margin:0;padding:40px 28px 80px}}
 .w{{max-width:900px;margin:0 auto}}
 h1{{font-size:28px;margin:0 0 6px}} .sub{{color:#6a6a68;margin:0 0 32px}}
 h2{{font-size:15px;letter-spacing:.08em;text-transform:uppercase;color:#8a8a88;
   margin:38px 0 12px;padding-bottom:6px;border-bottom:1px solid #e3e3e0}}
 .row{{display:flex;gap:26px;align-items:flex-end;flex-wrap:wrap}}
 figure{{margin:0;text-align:center}} figcaption{{font:11px ui-monospace,Menlo,monospace;color:#8a8a88;margin-top:8px}}
 .s{{display:flex;align-items:center;justify-content:center;min-height:76px}}
 .rev{{background:{BRAND};padding:20px 26px;border-radius:10px;display:inline-flex;gap:26px}}
 .busy{{padding:20px 26px;border-radius:10px;display:inline-flex;gap:26px;
   background:repeating-linear-gradient(45deg,#556 0 12px,#889 12px 24px)}}
 .clear{{position:relative;display:inline-block;outline:1.5px dashed #c3312f;outline-offset:24px;margin:26px}}
 p.n{{color:#4a4a48;max-width:66ch}} code{{font:12px ui-monospace,Menlo,monospace;background:#eee;padding:1px 5px;border-radius:3px}}
</style>
<div class=w>
<h1>{m['label']}</h1>
<p class=sub>{m['note']}</p>

<h2>1 · Reduction — most marks die here</h2>
<div class=row>{reduction}</div>
<p class=n>Stroke thickens as the size drops. A mark that is merely <em>scaled</em> down goes thin and
 muddy; a real small-size cut is a separate drawing. If 16px is unreadable, the mark is finished.</p>

<h2>2 · One colour</h2>
<div class=row><figure><div class=s>{svg(m, 64, colour="#141516")}</div><figcaption>black</figcaption></figure>
<figure><div class="s rev">{svg(m, 64, colour="#ffffff")}</div><figcaption>reversed</figcaption></figure></div>

<h2>3 · Silhouette — mass, not line</h2>
<div class=row>{silhouette}</div>
<p class=n>Approximated by thickening the stroke until the counters close. If the shape stops being
 recognisable before the counters fill, it depends on line weight rather than on form.</p>

<h2>4 · Memory</h2>
<p class=n>Not automatable. Show someone the 72px version for five seconds, take it away, ask them to
 draw it. If they cannot, it is too complex — and that is a fatal result, not a note.</p>

<h2>5 · Reversal and busy ground</h2>
<div class=row><div class=rev>{svg(m, 56, colour="#ffffff")}</div>
 <div class=busy>{svg(m, 56, colour="#ffffff")}</div></div>
<p class=n>On anything busy you ship the solid-tile version, not the bare mark.</p>

<h2>6 · Rotation and mirror</h2>
<div class=row>{rot}</div>
<p class=n>Checking it does not accidentally become something else, or point the wrong way.</p>

<h2>7 · Clear space</h2>
<div class=clear>{svg(m, 72, colour=BRAND)}</div>
<p class=n>Stated as a ratio, never in pixels: here <code>clear space = 0.75 × mark height</code> on every
 side. Nothing enters that box.</p>
</div>""")

    print(f"  {outdir}/")
    for f in sorted(outdir.iterdir()):
        print(f"    {f.name}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mark", choices=sorted(MARKS))
    ap.add_argument("--out", default="kit")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    if a.list or not (a.mark or a.all):
        print("marks:")
        for k, v in MARKS.items():
            print(f"  {k:8} {v['label']:18} {v['note']}")
        return 0

    keys = sorted(MARKS) if a.all else [a.mark]
    root = Path(a.out)
    if root.exists():
        shutil.rmtree(root)
    for k in keys:
        build(k, root / k)
    print(f"\nopen {root}/{keys[0]}/tests.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
