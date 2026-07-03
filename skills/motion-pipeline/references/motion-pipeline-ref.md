# motion-pipeline reference material

---

## Stage 4 — Toolchain comparison tables

### Layer 1 — Illustration / hero art
| Tool | Best for | Cost |
|---|---|---|
| **Figma** | Static frames you'll animate later | Free–$15/mo |
| **Procreate / Illustrator** | Hand-drawn or vector illustrations | $10 one-time / $20/mo |
| **AI image** (Midjourney, Recraft) | Style exploration, abstract pieces | $10–30/mo |
| **Spline** | 3D scenes (Stripe-style hero objects) | Free–$15/mo |

### Layer 2 — Animation
| Tool | Best for | Output | Skill |
|---|---|---|---|
| **Framer Motion / GSAP** | Code-native scroll/hover animations | In-repo JSX | Code |
| **Rive** | Interactive state machines, small file | `.riv` runtime | Medium |
| **Lottie** (AE + Bodymovin) | Polished autoplay loops, illustrations | JSON | High (AE) |
| **After Effects** | Linear video output, complex comps | `.mp4` / `.mov` | High |
| **Cavalry** | Code-friendly AE alternative, generative | `.mp4` | Medium |
| **Descript** | Transcript-driven explainer/screencast | `.mp4` | Low (AI-first) |

### Layer 3 — Voice / audio
| Tool | Best for | Cost |
|---|---|---|
| **ElevenLabs** | Broadcast-quality AI VO | $5–22/mo |
| **Your own voice + Descript** | Authentic, fast iteration | included in Descript |
| **Hire VO actor** (Voices.com, Voquent) | Final-tier polish | $100–500 per script |
| **Music: Epidemic Sound / Artlist** | Licensed background music | $12–20/mo |

### Layer 4 — Post / derivative cuts
| Tool | Best for |
|---|---|
| **Descript** | Re-cut explainer into shorts via transcript |
| **Submagic / Opus Clip** | Auto-clip long video → vertical with captions |
| **CapCut** | Manual social-short editing, free |
| **DaVinci Resolve** | Color grading, App Store preview polish |

---

## Stage 5 — Storyboard template

```
[0:00–0:03] Hook
  "Builders ship faster when they can see their entire workflow."
  Visual: zoom out from a single code editor → 5 connected services

[0:03–0:10] Problem
  "But most tools show one slice at a time."
  Visual: highlight one slice, others fade

[0:10–0:25] Concept
  "We unify them into one canvas..."
  Visual: slices animate together into a unified view

[0:25–0:50] How it works
  3 features × ~8s each

[0:50–0:60] CTA
  "Try the demo at example.com"
  Visual: logo + URL hold
```

---

## Stage 8 — Cost and time estimate tables

### Solo / AI-first ballpark

| Item | Time | $ |
|---|---|---|
| Script + storyboard | 2–4 hrs | $0 (you) |
| AI voiceover (ElevenLabs, 150 words) | 30 min | <$1 |
| Music license (Epidemic / Artlist) | 30 min | $15/mo prorated |
| AI B-roll (Runway/Pika, 4–6 clips) | 1–2 hrs | $5–20 |
| Animation in Descript / CapCut | 4–8 hrs | $30/mo prorated |
| Derivative cuts (Submagic, 3 outputs) | 1 hr | $15/mo prorated |
| **Total master** | 10–18 hrs | ~$30–60 |

### Commissioned tier (Hyperframe-style)

| Item | Time | $ |
|---|---|---|
| Brief + storyboard prep | 4–8 hrs | $0 |
| Studio production (master + 3 cuts) | 3–6 weeks | $2,000–15,000 |

---

## Stage 9 — Output brief template

Save the brief to `docs/motion/<project-or-feature>.md`:

```markdown
# Motion brief: <name>

## Intent
- Concept: ...
- Emotion: ...
- CTA: ...
- Memorable beat: ...

## Surfaces
[Stage 2 table, rows checked]

## Pattern
Single master → derive (or: bespoke for X, shared for Y)

## Toolchain
[Stage 4 chosen tools]

## Script
[Final VO/caption text]

## Storyboard
[Stage 5 beats with timing]

## Derivative recipes
[Stage 6 chapter map + per-surface recipe]

## Budget
[Stage 8 numbers]

## Open questions
- ...
```
