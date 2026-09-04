#!/usr/bin/env python3
"""Plot candidate colours and real brand colours on one hue axis.

Choosing a brand colour is a question about OCCUPANCY, and occupancy is spatial.
A list of names cannot show you that petrol sits in a gap; a hue axis can.

IMPORTANT, and stated on the page too: the reference hex values are from memory
and are APPROXIMATE. The maths converting them to a hue is exact, but the input
is not, so use this to see roughly where the crowds are, never to match a colour.
"""
from __future__ import annotations
import math, json
from pathlib import Path

def srgb_to_oklch(hexs: str):
    h = hexs.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    def lin(v): return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    l = 0.4122214708*r + 0.5363325363*g + 0.0514459929*b
    m = 0.2119034982*r + 0.6806995451*g + 0.1073969566*b
    s = 0.0883024619*r + 0.2817188376*g + 0.6299787005*b
    l_, m_, s_ = l ** (1/3), m ** (1/3), s ** (1/3)
    L = 0.2104542553*l_ + 0.7936177850*m_ - 0.0040720468*s_
    A = 1.9779984951*l_ - 2.4285922050*m_ + 0.4505937099*s_
    B = 0.0259040371*l_ + 0.7827717662*m_ - 0.8086757660*s_
    C = math.hypot(A, B)
    H = math.degrees(math.atan2(B, A)) % 360
    return round(L, 3), round(C, 4), round(H, 1)

# Approximate, from memory. Verify before relying on any of these.
REFS = [
    ("Grab",        "#00B14F", "SEA super-app"),
    ("Gojek",       "#00AA13", "SEA super-app"),
    ("OpenAI",      "#10A37F", "AI"),
    ("Shopee",      "#EE4D2D", "SEA marketplace"),
    ("Anthropic",   "#D97757", "AI"),
    ("Singtel",     "#EE1C25", "SG telco"),
    ("SG flag",     "#EF3340", "national"),
    ("DBS",         "#E4002B", "SG bank"),
    ("OCBC",        "#E4002B", "SG bank"),
    ("Xero",        "#13B5EA", "SME accounting"),
    ("UOB",         "#0B3B75", "SG bank"),
    ("Lazada",      "#0F146D", "SEA marketplace"),
    ("Google",      "#4285F4", "big tech"),
    ("Stripe",      "#635BFF", "payments"),
    ("Slack",       "#611F69", "SaaS"),
]

CANDS = [l.split("|") for l in Path("brandcolour.txt").read_text().splitlines()]

refs = []
for name, hexv, cat in REFS:
    L, C, H = srgb_to_oklch(hexv)
    refs.append({"name": name, "hex": hexv, "cat": cat, "hue": H, "chroma": C})

cands = []
for name, hue, solid, dark, what, who, knock in CANDS:
    cands.append({"name": name, "hue": float(hue), "solid": solid, "dark": dark,
                  "what": what, "who": who})

# How close is each candidate to its nearest real brand colour?
for c in cands:
    if c["name"] == "Graphite":
        c["near"], c["gap"] = "-", 999
        continue
    best = min(refs, key=lambda r: min(abs(c["hue"] - r["hue"]), 360 - abs(c["hue"] - r["hue"])))
    c["near"] = best["name"]
    c["gap"] = round(min(abs(c["hue"] - best["hue"]), 360 - abs(c["hue"] - best["hue"])))

Path("huemap.json").write_text(json.dumps({"refs": refs, "cands": cands}, indent=1))
print(f"{'candidate':11} {'hue':>5}   nearest real brand")
for c in sorted(cands, key=lambda x: -x["gap"]):
    if c["gap"] == 999:
        print(f"{c['name']:11} {c['hue']:>5}   (neutral)")
    else:
        flag = "  <- crowded" if c["gap"] < 18 else ""
        print(f"{c['name']:11} {c['hue']:>5}   {c['gap']:>3} deg from {c['near']}{flag}")
