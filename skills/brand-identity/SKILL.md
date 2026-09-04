---
name: brand-identity
description: Build a brand identity from scratch — positioning brief, colour occupancy audit against real competitors, logo construction and the seven tests, wordmark typography, and the full asset system. Use when a project needs a logo, a brand colour, or a wordmark, or when an existing identity reads generic.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
version: 0.1.0
---

# Brand Identity

Turns "make us a logo" into a sequence of decisions with evidence behind each one.

**The failure this exists to prevent:** generating variants until something looks nice. That is one step
of an eight-step process, and doing it alone produces marks that are competent and forgettable. It is
also exactly what an AI does by default, which is why the output reads as machine-made.

## Run in this order. Do not skip 2, 5 or 6.

### 1 · Brief
Three sentences, written down before anything visual:
- What it must **say**, to whom
- What it must **not** say
- The **tension** it has to hold (almost every brand has one: warm *and* credible, cheap *and* trustworthy)

Ask the user for these. Do not infer them. If the name means something — especially in another language
or a local vernacular — that meaning is usually the brief.

### 2 · Occupancy audit  ← the step that changes the answer
Differentiation, not harmony, decides a brand colour. Plot candidate hues **and real competitor hues** on
one axis, plus the hues already reserved for error, warning and success.

Use `references/hue_audit.py`. It converts competitor hex values to OKLCH hue and reports the nearest
neighbour for each candidate. Under ~18 degrees from a real brand in the same category is dead.

**State clearly that competitor hex values are approximate** unless the user supplies them. Never present
a remembered brand colour as fact.

### 3 · Divergence
Many rough marks, fast, ugly, no refinement. Vary **one axis at a time** — structure, then weight, then
fill — so the user can see what each move does. Mixing axes makes comparison impossible, which is the
most common way this step is wasted.

Ground every concept in **what the product does**, not in a pun on the name. Puns are the first thing a
client rejects and they are right to.

### 4 · Reduction
Kill anything that needs a sentence to explain. **A mark that means three things means none.**
Distinctiveness beats description: a logo does not have to depict the business.

### 5 · Construction
Rebuild survivors on a stated grid: strokes of one weight, radii as ratios, angles from a small set.
This is what separates a sketch from a mark. Record the geometry so it can be rebuilt by anyone.

### 6 · Optical correction
Then break the maths where the eye demands it:
- Circles **overshoot** flat edges or they read small
- **Horizontals** are drawn thinner than verticals or they look heavy
- Numerically equal gaps look unequal — space by eye
- At small sizes the stroke **thickens disproportionately**: a separate cut, not a scale

### 7 · Application — the seven tests
Run `references/logo_kit.py`. Generates a contact sheet: reduction at six sizes, one colour, silhouette,
memory, reversal on brand and on a busy ground, rotation and mirror, clear space.

Most marks die on **reduction** and **silhouette**. Run these early.

### 8 · System
Lockups, clear space **as a ratio never in pixels**, minimum size, colour variants, and a forbidden list.

## Wordmark

For a small brand the wordmark does ~80% of the work. It deserves more time than the symbol.

- **Case:** caps give a clean rectangle that locks up predictably and reads as signage. Mixed case keeps
  ascenders and descenders, so the silhouette is distinctive and friendlier. Decide from the *name*: a
  colloquial or slang name in caps shouts; a formal name in lowercase undercuts itself
- **Tracking** is the highest-leverage adjustment. Capitals were never drawn to sit together and always
  need positive tracking; lowercase needs almost none
- **Match the mark to cap height**, not to the line box. Sizing to the line makes the mark tower over the word
- **Two-word names** can carry hierarchy: one word heavier, smaller, or in the brand colour
- Set it in a licensed face, then kern **optically**. A wordmark is a drawing, not a text box

## Type sourcing

Anything on the front page of a free CDN is in the pool every template and generator draws from — that is
what makes type read as machine-made. Look at libre foundries that need self-hosting for genuinely
un-generic faces, or commit to a **system stack**, which loads instantly and reads native rather than
templated. Both are better answers than the twentieth most popular Google font.

## Before committing

Tell the user to check, because these cannot be checked from here:
- Trademark register, for their classes and jurisdiction
- Reverse image search for near-identical marks
- Unintended meaning in every language the audience reads
- Domain and handle availability

## Outputs

```
brand/<name>/
├── BRIEF.md          positioning, tension, what it must not say
├── hue_audit.txt     candidates vs real competitors
├── explore.html      one page per decision, one variable per page
├── kit/<mark>/       tests.html + favicon.svg + icon-app.svg + colour variants
└── SYSTEM.md         lockups, clear space, min size, forbidden list
```

## Honesty rules

- Never present a remembered competitor colour, font or logo as verified fact
- Never reproduce another company's logotype. Show **the user's mark in that structural pattern** instead
- Say when a step has been skipped. "These are sketches, not constructed marks" is useful; pretending
  otherwise wastes the user's judgement on the wrong question
