---
name: case-discussion
description: "Use this skill when the user wants to prepare a case discussion or case conference presentation — a single patient case walked through chronologically. Triggers: 'case discussion', 'case presentation', 'case conference', 'present a case', 'grand rounds case', 'ward case', 'interesting case'."
---

# Case Discussion — Workflow

A case discussion is a presentation of a single patient case, walked through the way the diagnosis actually unfolded at the bedside: HPI → PE → workup → working diagnosis → management → outcome → discussion. Slide count, duration, and audience vary — always confirm with the user during kickoff. The audience reasons along with the case as it's revealed.

This skill is a **thin wrapper**: it describes what's specific to case discussions and points at the building blocks for the mechanics.

---

## What's specific to a case discussion

- **Format and length:** confirm during kickoff — no fixed slide count or duration.
- **Narrative chronological flow:** the case unfolds the way it did at the bedside — symptoms, exam, workup, dx, management. Suspense is part of the format.
- **Audience reasons with the case:** pause before reveals; ask "what's your differential?" before showing imaging
- **One patient, one timeline:** not a literature review
- **De-identification mandatory:** no names, no MRNs, no dates that would identify; alter demographics if needed
- **Discussion-heavy ending:** the last 30–50% of the talk is teaching points drawn from the case

---

## Building blocks to follow

- For PPTX mechanics, theme, and slide layouts → `framework/building-blocks/deck-build.md`
- For auto-fetching textbook chapters and primary papers cited in the discussion section into `Sources/` → `framework/building-blocks/sources-fetch.md`
- For references and PMID verification → `framework/building-blocks/references.md`
- For open-access figure sourcing if you need stock imaging beyond the patient's own → `framework/building-blocks/images.md`
- For speaker notes format → `framework/building-blocks/speaker-notes.md`
- For visual QA → `framework/building-blocks/visual-qa.md`
- For mock Q&A → `framework/building-blocks/mock-qa.md`

## Content modules to consider

- For the bedside layer — what was on history, what the exam showed → `framework/content-modules/clinical-depth.md`
- For the local-context layer — what drug was available, what test was orderable → `framework/content-modules/local-guideline.md`
- If the final diagnosis has a clinical mimic that was on the differential → `framework/content-modules/disease-comparison.md`
- For the management slide(s) and the discussion section — if the treatment chosen, workup ordered, or take-home points follow a named guideline → `framework/content-modules/evidence-grading.md` (grade + system + year on each recommendation; if the actual case management diverged from the guideline-recommended approach, name the grade of what was recommended and discuss the divergence as a teaching point)

## Discipline (always applies)

- Before any rebuild → `framework/safe-file-operations.md`
- **De-identification check before sharing:** see below

---

## De-identification — non-negotiable

Before any draft leaves the user's machine, verify:

- [ ] No patient name, initials, or MRN anywhere (slides, speaker notes, file names, image metadata)
- [ ] No specific dates of admission/procedure — use "Day 1 / Day 5" or "Month X" relative timeline
- [ ] No identifying demographics (rare occupation, specific village/hospital ward) unless clinically essential; if essential, alter slightly
- [ ] Images cropped to remove name plates, room numbers, hospital logos with identifying info
- [ ] DICOM metadata stripped from imaging (use `gdcmanon` or similar)
- [ ] No verbatim direct quotes if they could identify
- [ ] If the case is unusual enough to be locally recognizable, alter non-clinical details (e.g., flip laterality if not clinically essential, change cohabitant relationships)

If the audience is from the same hospital and the patient was admitted recently, ask the user whether they have institutional approval (IRB or department head) for case presentation.

---

## Deck skeleton (typical proportions)

| Phase | Slides | Content |
|---|---|---|
| 1. Setup | 2–3 | Title; "Why this case" (1 line teaser); learning objectives |
| 2. HPI | 3–5 | Presenting complaint, HPI, PMH, medications, social/exposures, ROS |
| 3. Examination | 2–4 | Vitals, general appearance, focused PE findings (positives + key negatives) |
| 4. Differential at bedside | 1 | What was on the working differential at the moment of admission? |
| 5. Initial workup | 3–5 | CBC/chem/coags + targeted tests; imaging if early; cultures |
| 6. Revised differential | 1 | What stayed on differential? What's newly suspected? |
| 7. Further workup | 2–4 | Confirmatory studies, biopsy, specialised tests |
| 8. Final diagnosis | 1 | The dx, with the single confirmatory study highlighted |
| 9. Management | 2–4 | Treatment chosen, dose, duration, alternatives considered |
| 10. Course & outcome | 2–3 | Hospital course, response to treatment, complications, discharge plan |
| 11. Discussion | 3–6 | Teaching points: pathophysiology, key bedside cues, mimic comparison, local context |
| 12. Take-home | 1 | 3 bullets max |
| 13. References | 1 | Vancouver-numbered |

Total slide count scales with case complexity — confirm the target with the user during kickoff and scale each phase proportionally.

---

## Pause-and-reveal — a case-discussion-specific layout

Case discussions benefit from **"What's your differential?" pause slides** between data reveals. Pattern:

```
+----------------------------------------------------------+
| Header: "What's your differential?"                      |
+----------------------------------------------------------+
| Case data so far (recap, 5–6 bullets)                    |
|                                                          |
| [pause]                                                  |
|                                                          |
| (next slide reveals the next workup result)              |
+----------------------------------------------------------+
```

Use 2–3 of these across the case. They give the audience a moment to reason and let the discussion feel earned when the answer arrives.

---

## Discussion section — the teaching

This is what differentiates a case discussion from a case report. Cover:

1. **Why was the diagnosis difficult?** What were the clinical traps?
2. **Pathophysiology** — brief, only what's needed to understand the case
3. **Bedside cues you wish you'd recognized earlier** — apply `clinical-depth.md` for the syndrome
4. **Clinical mimics** — what else looked like this; what discriminates → apply `disease-comparison.md` if relevant
5. **Local context** — drug availability, test availability, NHSO coverage → apply `local-guideline.md`
6. **Take-home teaching points** — 2–3 max

Avoid: turning the discussion section into a topic review. Stay anchored to *this* case.

---

## 6-phase workflow

### Phase 1 — Kickoff

Confirm via `AskUserQuestion`:

1. What's the case — brief one-liner?
2. Has the case been formally de-identified?
3. Audience, language, length?
4. Why is this case teaching-worthy? (Diagnostic challenge / management dilemma / rare disease / system issue?)
5. Does the diagnosis have a mimic that was on the differential? (For `disease-comparison.md`)

### Phase 2 — Case reconstruction

Build a timeline of the actual case from the user's notes / discharge summary / their memory. This is the **single source of truth** for the deck. Save to `Documents/{Case} timeline.md`:

```markdown
# Case Timeline (de-identified)

## Day 0 (admission)
- Vitals: T 38.4, BP 110/70, HR 102
- HPI: 6 weeks of...
- Exam: ...

## Day 1
- Labs: CBC 12.3 / 11.1 / 270k...
- CT abdomen: ...

## Day 5
- ...
```

Verify de-identification of this file before proceeding.

### Phase 3 — Outline drafting

Build `Documents/{Case} outline.md` following the deck skeleton above. Decide where to place "What's your differential?" pause slides.

As the discussion section takes shape, list the textbook chapters and primary papers it will cite — then offer to fetch them via `sources-fetch.md` so they land in `Sources/Reference_papers/` ready for verbatim quoting. The case material itself (timeline, discharge summary, imaging) is user-supplied and de-identified separately; `sources-fetch.md` is for the *teaching* sources that anchor the discussion.

### Phase 4 — Build deck

Apply `deck-build.md`. Save as `Deck/{Case} slide v1.pptx` (e.g., `65F PUO admitted day 0 slide v1.pptx`) — never name a working copy `(Final)`; the user assigns that label.

If patient imaging is used (chest X-ray, CT slice, etc.), strip DICOM metadata and crop to remove identifiers. Caption with relative date ("Hospital day 3") not absolute.

If stock imaging is needed for the discussion section (e.g., a schematic of a pathway), use `images.md`.

### Phase 5 — Visual QA + speaker notes

Apply `visual-qa.md` and `speaker-notes.md`.

For a case discussion, speaker notes have a particular feature: **don't reveal information on the speaker notes that's intentionally suspenseful on the slide**. If the slide is a pause-and-reveal, the speaker notes for that slide should describe the pause, not the answer.

### Phase 6 — Mock Q&A

Apply `mock-qa.md`. For a case discussion, generate **15–25 questions** distributed:

- ★ Foundation: HPI details, exam findings, basic dx (3–5 questions)
- ★★ Intermediate: differential reasoning, why-not-X (8–12 questions)
- ★★★ Advanced: management trade-offs, alternative paths, what would you do differently (5–8 questions)
- Gap section: 3–5 questions about "what does the literature say about this scenario"

---

## Folder structure

```
{Department}/Case Discussions/
└── {Case short title — de-identified}/
    ├── README.md
    ├── Sources/                            # de-identified source material
    │   ├── Discharge_summary_redacted.pdf  # de-identified version
    │   ├── Imaging/                        # de-identified DICOMs / JPGs
    │   ├── Figures/                        # any open-access figures for the discussion section
    │   └── Reference_papers/               # papers cited in discussion
    ├── Documents/                          # markdown outputs
    │   ├── {Case} timeline.md              # de-identified case reconstruction
    │   ├── {Case} outline.md
    │   ├── Speaker_notes.md
    │   ├── Mock_questions.md
    │   └── Faculty_feedback.md             # filled after the talk
    ├── Deck/                               # PPTX + PDF deliverables (live working copies)
    │   ├── {Case} slide v1.pptx → v2 → ...
    │   └── {Case} slide (Final).pptx + (Final).pdf
    └── Build_archive/                      # working files (keep, don't delete)
        ├── Section_PPTXs/                   # standalone section rebuilds (see deck-build.md Step 7)
        ├── Backups/                         # safety copies before risky edits (see safe-file-operations.md)
        └── Old_versions/                    # superseded full-deck iterations
```

---

## Anti-patterns to avoid

- **Revealing the diagnosis on slide 2** — the audience-reasoning experience is lost
- **Skipping pause slides** — without them the case becomes a chronological list, not a discussion
- **Discussion section that's a mini-topic review** — stay anchored to this case
- **No teaching point at the end** — the case must produce 2–3 take-homes
- **Patient-identifying details surviving in metadata** — always strip DICOM, crop visibly, scrub filenames
- **Citing only textbook chapters** — case discussions need primary literature for the discussion section
- **Including speaker notes that reveal upcoming slide answers** — defeats pause-and-reveal

---

## Quick-start checklist

- [ ] Case is de-identified at every level (slides, notes, files, metadata)
- [ ] Timeline reconstructed from real notes, not training-knowledge inference
- [ ] Outl