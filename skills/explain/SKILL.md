---
name: explain
description: Explain a file, function, or concept for a non-technical audience.
version: 0.1.0
---


Explain a file, function, or concept for a non-technical audience. Do the following steps in order:

**1. Identify the target**
Use `$ARGUMENTS` if provided (e.g. `/explain ai.py` or `/explain analyze_theme_responses`).
If no argument, ask what to explain.

**2. Read the target**
Read the file or locate the function. Understand what it does before writing the explanation.

**3. Write the explanation**
Tailor to a non-technical reader:
- No jargon without definition
- Use analogies where helpful
- Focus on *what it does* and *why it exists*, not *how* the code works
- If there are risks or limitations, mention them plainly

Structure:
- **What it is**: one sentence
- **What it does**: 2–4 sentences, plain language
- **Why it matters**: how it affects users or the product
- **Limitations or risks** (if any): what could go wrong or what it doesn't cover

**4. Optional: technical addendum**
If the user seems technical (based on conversation context), add a brief technical note at the end covering implementation details.

Keep the explanation under 200 words for the non-technical section.
