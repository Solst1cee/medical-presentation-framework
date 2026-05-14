---
name: speaker-notes
description: "Building block for writing presenter speaker notes in the audience's language with English medical terminology preserved. Covers structure, length per slide, embedding mechanics for .pptx notes pane, and saving to a parallel Speaker_notes.md. Loaded by Read path from a presentation-type skill; not intended to auto-trigger on its own."
---

# Speaker notes — audience-language narrative with English medical terms

## Why this matters

Speaker notes serve two distinct purposes during and after a presentation:

1. **During the talk:** a cognitive scaffold the presenter can glance at — the teaching point that justifies the slide, the cohort number that supports the bullet, the sentence that connects this slide to the next.
2. **After the talk:** documentation. The slide alone is often too compressed for someone (you in 6 months, a colleague catching up) to reconstruct the reasoning. Speaker notes are where the *why* lives.

For Thai medical-resident audiences, the natural style is **Thai prose with English technical terms preserved exactly as taught**. This matches how clinical teaching happens in Thai medical schools and academic centres — Thai connective tissue, English nouns. Translating "tenosynovitis" to "อักเสบของเยื่อหุ้มเอ็น" reads as awkwardly formal and forces the presenter to code-switch on the fly.

> **English-only exception.** Default to Thai narrative + English medical terms. Only write English-only speaker notes if the author explicitly asks for it (e.g., "this is an English-language conference; keep everything English").

---

## Per-slide structure

Each slide gets **4–8 sentences** of speaker notes. Structure:

1. **Opening orientation** (1 sentence) — what this slide is about and why it follows the previous one.
2. **Key teaching point** (1–2 sentences) — the one thing the audience should leave the slide knowing.
3. **Evidence anchor** (1–2 sentences) — the cohort number, guideline reference, or trial that supports the teaching point.
4. **Optional clinical pearl or warning** (1 sentence) — a bedside-relevant cue or trap.
5. **Transition** (1 sentence) — bridges to the next slide.

Total length: ~80–150 words for a content slide. Less for divider slides (just an orientation sentence).

---

## Style — Thai narrative, English medical terms

### What to keep in English

- **Organism names** — *Mycobacterium marinum*, MAC, M. abscessus
- **Drug names** — azithromycin, ethambutol, bedaquiline
- **Lab tests** — anti-IFN-γ ELISA, MGIT culture, beta-D-glucan
- **Eponymous signs / tests** — Tinel's, Phalen's, McMurray's
- **Guideline / society names** — ATS/IDSA, ACR, RCPT
- **Anatomic terms** — flexor tendon sheath, paraspinal abscess
- **Numeric data** — "21% misdiagnosed", "PMID 19861045"
- **Disease names** — tenosynovitis, septic arthritis, Pott's disease

### What to write in Thai

- Sentence connectives — แต่, อย่างไรก็ตาม, นอกจากนี้
- Causal / explanatory framing — เพราะว่า, ทำให้, ต้อง
- Instructional cues — สำคัญที่จะต้อง, ระวัง, ให้คิดถึง
- Clinical reasoning — น่าจะเป็น, ไม่น่าจะเป็น, แยกจาก

### Worked example

> Spasovski 2014 European hyponatremia guideline (PMID 24569125): ใน euvolemic hyponatremia ที่ urine osmolality > 100 mOsm/kg และ urine Na > 30 mmol/L ส่วนใหญ่เป็น SIADH. First-line treatment คือ fluid restriction (< 800 mL/day) — แต่ effect ค่อนข้างช้า บางครั้งต้องใช้ tolvaptan หรือ urea ร่วมด้วยในรายที่ refractory.
>
> Key teaching point: ใน chronic asymptomatic hyponatremia การ correct serum Na เร็วเกิน 8 mmol/L ใน 24 ชั่วโมง เพิ่ม risk ของ osmotic demyelination syndrome อย่างมาก — ต้อง monitor serum Na ทุก 4–6 ชั่วโมง และพร้อม re-lower ด้วย 5% dextrose ถ้า overcorrect.

(Two sentences. Roughly the right density for a content slide. Note: organism / lab / drug / eponym / numeric values stay in English; connective and reasoning tissue in Thai.)

---

## Anti-patterns to avoid

- **Translating technical terms into Thai for "clarity"** — this is actually more confusing. Thai residents learn "tenosynovitis" in English. Don't translate to "อักเสบของปลอกหุ้มเอ็น" unless the author specifically requests it.
- **English-only notes for a Thai audience** — robotic to read aloud. Mixed style is the natural register.
- **Reading-the-slide notes** — speaker notes that just restate the bullet text in prose. The bullet is for the audience to see; the speaker notes are for the *unseen* explanation.
- **Single-line notes** — too thin. If a slide is worth showing, it's worth 4 sentences of context.
- **Pasting the entire paper abstract** — too thick. Notes should be presenter-readable in one glance.
- **Citation-free claims** — every numeric claim in the speaker notes should carry a PMID or guideline reference, just like the slide.

---

## Saving and embedding

Speaker notes live in **two places**:

### 1. `Documents/Speaker_notes.md` — the authored markdown source

Authored as a markdown file with one section per slide. Format:

```markdown
## Slide 14 — SIADH: Diagnostic Criteria

[Thai-narrative notes here, 4–8 sentences]

**Refs:** 1, 5, 14
```

This file is also useful as a study aid for the presenter pre-talk, separate from the deck.

### 2. The .pptx notes pane — embedded during build

When the deck is rebuilt, the speaker-notes are written into the PPTX notes pane so that PowerPoint shows them in Presenter view.

Python-pptx:

```python
def set_speaker_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text  # replaces any existing notes
```

For the unpack/repack XML mode, the `wrap_slide(body, notes=notes_text)` helper in `deck-build.md` writes the notes XML inline. See that file for the XML format.

---

## Length guide by presentation type

| Presentation type | Notes density |
|---|---|
| Topic review | 4–8 sentences/slide on content slides; 1 on dividers |
| Journal club | 6–10 sentences on critical-appraisal slides (more dense — defending methodological choices); 2–3 on background |
| Case discussion | 5–8 sentences per phase (HPI / PE / workup / management); the case-narrative slides deserve more talking time |

Don't over-prepare notes for ceremonial slides (title, dividers, references) — one orientation sentence suffices. Additional rows for reserved presentation types (M&M, operative-technique) will be added when those skills are built.

---

## Workflow — when to write speaker notes

Write speaker notes **after the deck is visually stable** (post visual-QA, ideally same day as presentation rehearsal). Reasons:

- You'll rewrite if the slide content shifts; writing notes against a v3 deck and then re-writing against v5 is wasted effort.
- Writing notes forces you to rehearse the flow. Doing it close to the talk improves recall.

A reasonable middle ground: draft notes at v3, finalise at v5 (post visual-QA). That gives time to refine talking points before rehearsal — generating notes the night before the talk is too late.

---

## Self-check before declaring speaker notes done

- [ ] Every content slide has 4–8 sentences of notes
- [ ] Notes are in Thai prose with English medical terms preserved (unless author requested English-only)
- [ ] Every numeric claim is anchored to a Vancouver reference number
- [ ] Notes don't just restate the bullets — they add the *why*
- [ ] Notes are saved both in `Documents/Speaker_notes.md` AND embedded in the .pptx notes pane
- [ ] Notes don't reveal information that's intentionally suspenseful (case-discussion / M&M)
- [ ] Total length per slide is reasonable for the talk pace (~10–15 sec per slide of speaker monologue)
