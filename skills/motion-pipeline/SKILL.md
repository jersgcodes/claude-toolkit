---
name: motion-pipeline
description: Plan a motion graphics production pipeline — landing hero, explainer, preview, social shorts, onboarding — from one master asset to many derived outputs. Use before commissioning or producing any motion content.
version: 0.1.0
---


# Motion Pipeline

Plan motion graphics production *before* opening After Effects, Rive, Descript, or paying a studio. The goal is to lock the intent, choose the right tool per layer, and design one **master asset** that derives every surface you need.

Applies to: landing hero animations, explainer videos, App Store / Play Store preview videos, social shorts (Reels / TikTok / LinkedIn), in-product onboarding sequences.

Sources: *Animation at Work* (Rachel Nabors), Disney's 12 principles of animation, Lottiefiles best practices, Apple HIG motion guidelines, Stripe / Linear / Vercel landing-page case studies.

---

## When to use

| Situation | Use? |
|---|---|
| About to commission a studio (Hyperframe-tier) | YES — saves $1–5K in revisions |
| Producing in-house explainer or social content | YES |
| Adding motion to a landing page (hero, scroll-triggered) | YES |
| Designing in-product onboarding with animation | YES |
| Single micro-interaction (button hover, toast slide-in) | NO — use `/motion-brief` instead |
| Bug fix to existing animation | NO |

---

## Stage 1 — Frame the intent

Answer in one sentence each:

1. **What concept does the motion convey?** (Not "looks nice" — name the idea. e.g. "data flowing through a pipeline", "AI assembling a workflow from parts")
2. **What emotion should the viewer feel?** (Curiosity? Confidence? Delight? Urgency?)
3. **What action should follow?** (Sign up? Read more? Try the product?)
4. **What's the one thing they should remember?** (If they only watch 3 seconds.)

If the concept needs a paragraph to explain, the motion will fail. Sharpen until it fits one sentence.

---

## Stage 2 — Pick surfaces

Which of these do you need? Mark each:

| Surface | Format | Duration | Where it plays | Sound? |
|---|---|---|---|---|
| Landing hero | Loop, no audio | 8–15s | Above the fold on homepage | No |
| Full explainer | Linear, VO + music | 60–90s | `/about`, sales page, YouTube | Yes |
| App Store preview | Linear, no VO (captions only) | 15–30s | App Store listing | Optional |
| Social short (vertical) | Linear, hook + payoff | 15–60s | Reels, TikTok, LinkedIn, X | Yes |
| Social short (horizontal) | Linear | 15–60s | YouTube Shorts, LinkedIn | Yes |
| Onboarding sequence | Per-step segments | 5–15s each | In-product, post-signup | No |
| Email GIF | Loop, ≤ 5MB | 3–8s | Marketing emails | No |
| Conference / talk intro | Linear | 5–10s | Keynote bumpers | Yes |

Pick 2–4. More than 4 and you're spreading thin.

---

## Stage 3 — Choose the production pattern

| Pattern | When to use | Pro | Con |
|---|---|---|---|
| **Single master → derive** | You need 3+ surfaces sharing the same concept | One production, many outputs (70% cost saving) | Master must be designed for all crops upfront |
| **Bespoke per surface** | Surfaces tell different stories | Each is optimized | 3–5× the work |
| **Hybrid** | Master for landing + explainer, bespoke for social | Balances quality and effort | Need discipline on what's shared vs. unique |

Default: **Single master → derive**, unless surfaces have genuinely different messages.

---

## Stage 4 — Pick the toolchain (per layer)

A motion piece has up to four layers. Pick one tool per layer.

> **Reference:** tool-comparison tables for all four layers are in `references/motion-pipeline-ref.md` — read it when you reach this step.

Write each chosen tool as a row in your brief. If a layer is empty, that's a gap.

---

## Stage 5 — Script + storyboard the master

### Script first
Write the VO/caption script as plain text **before** any visual work. Constraints:

- **Speed:** ~150 words per minute spoken. A 60s explainer = ~150 words MAX.
- **Hook (first 3s):** state the problem or promise. Not "Hi, we're [brand]."
- **Beats:** 1 idea per 5–10s. Don't cram.
- **CTA (last 5s):** one clear action.

### Then storyboard
Sketch one frame per beat. Doesn't need to be art — boxes and labels are fine.

> **Reference:** storyboard template with example beats is in `references/motion-pipeline-ref.md` — read it when you reach this step.

Lock the storyboard before animating. Animation is expensive; rewrites are cheap on paper.

---

## Stage 6 — Design the master for derivation

The master timeline must be built so cuts are cheap. Two rules:

### Rule 1 — Composition crops
Frame every shot so it works in three aspect ratios:

```
┌────────────────────────────┐  16:9 (landing, explainer, YT)
│       ┌────────────┐       │
│       │            │       │  1:1 (Instagram, LinkedIn feed)
│       │   SAFE     │       │
│       │   AREA     │       │  9:16 (Reels, TikTok, Stories)
│       │            │       │
│       └────────────┘       │
└────────────────────────────┘
```

Keep titles, key visuals, and CTAs in the **safe area** (center vertical strip). Background can extend into the wider crop.

### Rule 2 — Chapter markers
Build the timeline as labeled chapters, not one continuous flow:

```
ch1_hook        (0–3s)
ch2_problem     (3–10s)
ch3_concept     (10–25s)
ch4_feature_a   (25–33s)
ch4_feature_b   (33–41s)
ch4_feature_c   (41–50s)
ch5_cta         (50–60s)
```

Then derivatives become recipes:

| Output | Recipe |
|---|---|
| Landing hero | ch3 only, looped, no audio |
| Full explainer | ch1–ch5 all |
| App Store preview | ch1 + ch4_a + ch4_b + ch5 (skip problem) |
| Social short | ch1 (hook) + best feature + ch5 (CTA), vertical crop |
| Onboarding step 1 | ch4_feature_a only, autoplay on signup |

---

## Stage 7 — Output checklist (per surface)

Before publishing, verify:

### Performance
- [ ] Web hero ≤ 500 KB (Lottie) or ≤ 2 MB (looping video)
- [ ] Use `prefers-reduced-motion` to disable or freeze hero
- [ ] Lazy-load below-fold motion
- [ ] Video uses `poster` attribute (don't show blank frame)
- [ ] 60fps on a mid-range laptop (test on throttled CPU)

### Accessibility
- [ ] Captions on any video with VO (SRT or burned-in for social)
- [ ] `aria-label` describes the animation's purpose for screen readers
- [ ] No critical info conveyed by motion alone
- [ ] Flashing < 3Hz (epilepsy safety)
- [ ] Pause/play control if video is > 5s and autoplaying

### Format / delivery
- [ ] Landing hero: WebM (VP9) + MP4 (H.264) fallback, or Lottie JSON
- [ ] Social: MP4 H.264, 30/60fps, captions burned-in
- [ ] App Store: per Apple/Google spec (15–30s, no narration, captions OK)
- [ ] Email GIF: ≤ 5MB, ≤ 8s, ≤ 20 frames
- [ ] Onboarding: Lottie (vector, scales) or short MP4

### Brand
- [ ] Logo bumper start/end (1–2s)
- [ ] Color palette matches design tokens (`~/claude/design-tokens.yaml`)
- [ ] Typography matches site (or close approximation in motion-safe font)

---

## Stage 8 — Cost + time estimate

Sketch a budget table before starting.

> **Reference:** solo/AI-first and commissioned-tier budget tables are in `references/motion-pipeline-ref.md` — read it when you reach this step.

Decide before starting which tier you can afford.

---

## Stage 9 — Validate before producing

- [ ] Concept fits in one sentence (Stage 1)
- [ ] 2–4 surfaces picked (Stage 2)
- [ ] Single-master pattern OR justified bespoke split (Stage 3)
- [ ] One tool chosen per layer (Stage 4)
- [ ] Script written, ≤ 150 words for a 60s piece
- [ ] Storyboard locked, beats labeled
- [ ] Master designed with safe area + chapter markers (Stage 6)
- [ ] Derivative recipes mapped per surface
- [ ] Output checklist understood (Stage 7)
- [ ] Budget realistic for tier (Stage 8)

If any item is "not yet," do not start production.

---

## Output

Save the brief to `docs/motion/<project-or-feature>.md`.

> **Reference:** the full brief template (all sections) is in `references/motion-pipeline-ref.md` — read it when you reach this step.

---

## Integration

- Pulls from: `/feature-design` (feature → motion need), `/visual-mock` (static UI before motion overlays)
- Pairs with: `/motion-brief` (single-asset deep brief), `/motion-audit` (post-build perf/a11y check)
- Hands off to: `/component-design` (in-product motion components), `/responsive-design` (landing hero responsive behavior)
- Outputs feed: `/decision-record` (capture motion strategy ADR), `/a11y-audit` (verify reduced-motion + captions)

---

## Anti-patterns to flag

- **No script, just vibes** — animation drives the message; without a script, viewers don't know what to feel
- **Building each output from scratch** — 5× the work for negligible quality gain over single-master pattern
- **Ignoring safe-area crops** — master is 16:9-only, then social cuts amputate the logo
- **Hero animation > 2 MB** — kills Lighthouse score, hurts SEO
- **Ignoring `prefers-reduced-motion`** — fails WCAG 2.3.3, can trigger vestibular disorders
- **VO without captions** — fails WCAG 1.2.2, also fails on muted autoplay (default on most platforms)
- **Studio commission without locked storyboard** — every revision costs $; lock concept on paper first
- **"We'll add motion later"** — landing without motion in 2026 reads as dated; bake into design phase, not after
- **Tool-driven instead of intent-driven** — "We have Lottie so let's use it" → ends up with unnecessary motion
- **Overproducing onboarding** — in-product motion should be < 1s per step; 10s explainers belong on the landing page, not in the app
