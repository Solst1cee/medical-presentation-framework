---
name: mock-qa
description: "Building block for generating anticipated faculty Q&A for a presentation. Covers question count, difficulty grading, in-deck vs beyond-deck tagging, evidence-anchored answers, and a final gap-questions section for the most valuable items. Loaded by Read path from a presentation-type skill; not intended to auto-trigger on its own."
---

# Mock Q&A — anticipated faculty questions

## Why this matters

Faculty almost always ask three things the deck didn't have. Even a well-rehearsed deck attracts feedback areas the presenter hadn't anticipated — those gap questions are the highest-yield items to prepare for.

A mock Q&A document does two things:

1. **Pre-talk:** forces the presenter to confront questions they hadn't planned for. The 30 minutes spent generating Q&A is worth 3 hours of post-talk regret.
2. **Post-talk:** becomes the seed for the next iteration of the deck. Faculty-asked questions that weren't already on the deck become the gap analysis for the v2.

Generate mock Q&A around the v2/v3 mark of the deck — not at the very last moment. That gives the presenter time to rehearse, fold gap answers into talking points, and decide whether to add a slide for the most important gaps.

---

## What to produce

A single markdown file at `Documents/Mock_questions.md` containing **25–40 anticipated questions** across the deck.

### Per-question format

Each question has four fields:

```markdown
### Q[N]. [Question text in plain language]

**Difficulty:** ★ / ★★ / ★★★
**Tag:** [in deck — slide N] OR [beyond deck]
**Answer:** [4–8 sentences, anchored to ONE piece of evidence]

**Anchor:** [cohort N, PMID, guideline year, regimen name]
```

### Field semantics

- **Difficulty:**
  - ★ — foundation (covered on the basic clinical-features slide; a junior resident should answer this)
  - ★★ — intermediate (requires synthesis across slides or recall of a cohort number)
  - ★★★ — advanced (requires nuance, a specific PMID, or a known controversy)
- **Tag:**
  - `[in deck — slide N]` — answer is visible on slide N. Useful for rehearsal: presenter knows where to point.
  - `[beyond deck]` — answer is NOT on a slide; presenter must answer from notes or knowledge. These are the most valuable items to prepare.
- **Answer:** 4–8 sentences. Lead with the answer, then the evidence anchor, then nuance/caveat if needed.
- **Anchor:** the single most authoritative reference that grounds the answer. One per question.

### Worked example

```markdown
### Q14. Why use fluid restriction as first-line treatment for SIADH rather than starting with tolvaptan?

**Difficulty:** ★★
**Tag:** [in deck — slide 28]
**Answer:** The 2014 European hyponatremia guideline recommends fluid restriction as first-line for mild-to-moderate chronic SIADH because it's effective in the majority of cases, carries zero pharmacological risk, and avoids the cost and access issues with tolvaptan. The 2013 Verbalis expert panel agrees, reserving tolvaptan for SIADH refractory to fluid restriction after 48–72 hours or in patients who can't tolerate the volume restriction. Tolvaptan also requires inpatient initiation in most centres because of the risk of overly rapid correction.

**Anchor:** Spasovski G et al. Eur J Endocrinol 2014;170(3):G1–47 (PMID 24569125)
```

---

## How many questions, distributed how

For a 50-slide topic review:

| Question type | Count | Where in the file |
|---|---|---|
| Foundation (★) | 8–10 | Spread across sections |
| Intermediate (★★) | 10–14 | Heavier in dx/tx sections |
| Advanced (★★★) | 5–8 | Heavier in controversial / nuanced areas |
| Gap (★★ / ★★★, all `[beyond deck]`) | 3–6 | Final section, separately |

Total: **25–40 questions**. The gap section is the most valuable — keep it distinct.

Adjust for other formats:

| Format | Total | Heavier in |
|---|---|---|
| Topic review | 25–40 | Treatment, controversies |
| Journal club | 18–28 | Internal validity, generalisability, conflict-of-interest |
| Case discussion | 15–25 | Decision points, alternative dx, why-not-X |

Rows for reserved presentation types (M&M, operative-technique) will be added when those presentation types are built.

---

## The "Faculty-feedback gap questions" section — most valuable

At the end of the file, add a separate section:

```markdown
---

## Gap questions — anticipated faculty questions whose answers are NOT on a slide

These are the questions the presenter must be ready to answer **from memory or speaker notes**, because the slide deck doesn't show the answer. These are the highest-yield items for rehearsal.

### G1. [Question]
**Answer:** ...
**Why not on a slide:** [too detailed / too speculative / a follow-up question]
**Where the answer would go if asked to add a slide:** Section N, after slide M
```

This is the section that turns into the next iteration's slide additions. After the talk, mark which gap questions actually came up — that's the feedback signal for v2.

---

## Sourcing questions

Generate questions from four buckets:

### Bucket 1 — Slide-derived (foundation + intermediate)
For each major slide, ask: "What's the obvious follow-up question to this slide?"

### Bucket 2 — Cross-slide (intermediate)
Ask: "What connects slide N and slide M that isn't explicit?" (e.g., "Why is the regimen for M. abscessus longer than for MAC?")

### Bucket 3 — Controversy-driven (advanced)
For every claim that has known controversy in the literature, ask the controversial side: "Why didn't you include [alternative]?", "Is the evidence for X actually as strong as the slide implies?"

### Bucket 4 — Local-context driven (intermediate, often gap)
"What does Thai practice actually do for this?", "Is this drug on the NHSO formulary?", "Where can this lab test be ordered in Bangkok?" These are often `[beyond deck]` because international guidelines don't cover them.

---

## Anti-patterns to avoid

- **Trivia questions** — "What year was M. marinum first described?" — not useful for rehearsal
- **Single-citation answers from training knowledge** — every numeric answer should have a verifiable PMID or guideline year
- **Treating every gap question as a slide-add candidate** — some gaps are genuinely beyond the scope of the deck and just need to be in the presenter's notes
- **Generating Q&A only at the end** — too late to refine talking points; aim for v2/v3
- **Skipping the gap section** — this is the most valuable part; don't elide it

---

## Workflow — when to generate Q&A

| Timing | What to do |
|---|---|
| Deck v2 (rough complete) | Draft 15–20 questions, sketch gap section |
| Deck v3 (post-references) | Bring to 25–35 questions; refine answers with PMIDs |
| Deck v5 (post-visual-QA) | Finalize; lock the gap section |
| Post-presentation | Update with which questions actually came up + faculty comments; archive |

---

## Self-check before declaring mock Q&A done

- [ ] At least 25 questions total
- [ ] Difficulty distribution roughly 30% / 50% / 20% (★/★★/★★★)
- [ ] Every answer has an evidence anchor (PMID / guideline / cohort)
- [ ] In-deck vs beyond-deck tags are present on every question
- [ ] At least 3 questions in the dedicated gap section
- [ ] No question is purely trivia
- [ ] Local-context questions (Thai NHSO / formulary / reference labs) are represented for treatment topics
- [ ] The file is saved to `Documents/Mock_questions.md`
