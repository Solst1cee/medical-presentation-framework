---
name: topic-review
description: "Use this skill when the user wants to prepare a medical topic review presentation for any rotation or specialty. Triggers: 'topic review', 'rotation presentation', 'topic review conference', 'prepare slides for topic review', 'make a topic review deck'."
---

# Topic Review — Workflow

A topic review is a didactic presentation on a defined clinical topic, given during a rotation or at an academic conference. Slide count, duration, depth, audience year, and section breakdown vary widely — always confirm with the user during kickoff rather than assuming.

This skill is a **thin wrapper**: it describes what's specific to topic reviews and points at the building blocks for the mechanics. The building blocks are reusable across other presentation types.

---

## What's specific to a topic review

- **Format and length:** confirm during kickoff — no fixed slide count or duration.
- **Sections:** confirm during kickoff — typically follow the natural clinical flow of the topic (see Phase 3 for topic-type structure guidance).
- **Reference style:** Vancouver-numbered master list, per-slide reference line at the bottom.
- **Speaker notes:** in the audience's language with English medical terms preserved. Optional — confirm with the user at Phase 7.
- **Audience:** residents and staff at an academic conference; presenter is usually a resident or fellow.

---

## Building blocks to follow

Load these by `Read` when you reach the matching workflow phase:

- For PPTX mechanics, theme, slide layouts → `framework/building-blocks/deck-build.md`
- For auto-fetching textbook chapters, papers, and guideline PDFs into `Sources/` → `framework/building-blocks/sources-fetch.md`
- For references and PMID verification → `framework/building-blocks/references.md`
- For **automated reference reconciliation** (audit script) → `framework/building-blocks/reference-audit.md` — load and run at slide-removal events, Phase 3→4 transition, Phase 4 start, Phase 6 reconciliation
- For open-access figure sourcing → `framework/building-blocks/images.md`
- For speaker notes format → `framework/building-blocks/speaker-notes.md`
- For visual QA → `framework/building-blocks/visual-qa.md`
- For mock Q&A → `framework/building-blocks/mock-qa.md`

## Content modules to consider

Each content module has its own trigger — load only when the trigger fires:

| Module | Trigger |
|---|---|
| `framework/content-modules/clinical-depth.md` | Every disease-syndrome slide. Apply during Phase 3 outline drafting. |
| `framework/content-modules/disease-comparison.md` | Topic has a recognised clinical mimic (e.g., NTM ↔ TB, gout ↔ CPPD, RA ↔ PsA, SLE ↔ drug-induced lupus, DRESS ↔ SJS). Apply during Phase 3 outline drafting — propose a dedicated comparison slide early in the deck, with per-syndrome inline comparison columns where relevant. If unsure whether a candidate mimic is significant enough to warrant the comparison structure, confirm with the user during Phase 1 outline-proposal. |
| `framework/content-modules/evidence-grading.md` | Every slide that states a clinical recommendation from a named guideline — most often F (Treatment / management / prevention), and central in Type 4 management-focused and Type 5 emergency reviews. Apply during Phase 3 outline drafting: each recommendation in the outline carries its grade (GRADE / ACC-AHA Class + LOE / USPSTF) and the guideline year, on the same line. Flag conflicts between guidelines (or between an international guideline and the local one) explicitly rather than picking one silently. |
| `framework/content-modules/local-guideline.md` | Thai-speaking audience. Apply during Phase 2 (local-context research) and Phase 3 (Local Context slide near treatment). |
| `framework/content-modules/paper-summary.md` | **On user request only** — when the user asks for details on a specific paper (e.g., *"summarise Garrahy 2021"*, *"landmark card for DAPA-HF"*, *"chip for that trial"*). Output goes inline in the outline's `## Build aids — not for slides` section alongside Sources and Figure summaries. Pick the tier from the user's phrasing — chip (Tier 1), compact landmark card (Tier 2), or full summary (Tier 3) — and label the card with its tier. Don't auto-summarise every reference. |

## Discipline (always applies)

- Before any rebuild or post-presentation update → `framework/safe-file-operations.md`

---

## 7-phase workflow

### Phase 1 — Kickoff & scope

**Step 0 — Check the project folder before anything else.**

Before the kickoff questions, check whether the project folder already exists at the expected path (`{Department}/{Topic}/`). Two cases:

- **Folder doesn't exist yet** — offer to create the full standard structure (Sources/, Documents/, Deck/, Build_archive/Backups/, Build_archive/Section_PPTXs/, Build_archive/Old_versions/, and a starter `README.md` with topic + audience + date). Don't ask the user to set it up manually — that introduces typos and missing subfolders. Suggested phrasing: *"You haven't created the project folder yet. Want me to set up `{Department}/{Topic}/` with the standard structure? You'd then drop your textbook PDFs and key papers into `Sources/`, and we'd begin the kickoff questions."*
- **Folder already exists** — confirm with the user that they want to work in it, then list what's already in `Sources/` so the kickoff conversation can reference the actual material on hand.

Only after the folder exists (and the user has had a chance to drop source PDFs into `Sources/`) move into the kickoff questions below.

**Kickoff questions** — ask via `AskUserQuestion` (one question at a time):

1. **Which rotation and topic?** (e.g., "Internal Medicine — Hyponatremia"; "Rheumatology — Gout & CPPD"; "Nephrology — IgA nephropathy")
2. **Slide count and duration?** Confirm both — they're not fixed.
3. **Audience and language?** (resident year, narrative language, English medical terms preserved)
4. **Primary sources?** (textbook + edition + chapter; guideline name + year; user-supplied PDFs in `Sources/`)
5. **Existing PPTX template or colleague's deck to preserve?** This drives `deck-build.md` Step 1 (theme vs. template vs. from scratch). **Always ask explicitly — don't assume a default.** Examples of what to look for: an institutional title slide / section divider style, a colleague's deck whose section dividers the user likes, a `Templates/` folder at the workspace root. If the user mentions liking the design of any prior presentation, treat that as a template lead — ask for the file before building anything.
6. **Specific angles to emphasize?** (e.g., pathophysiology-heavy, treatment-heavy, local-context-heavy)

**Topic type + section weighting.** After the questions, classify the topic into one of the six types in Phase 3 and propose the section weighting (Heavy / Standard / Light / Skip) explicitly. Get user approval before any research — the weighting drives Phase 2 research depth, Phase 3 slide allocation, and the master reference list density.

**Do not research or build until the outline structure and weighting are approved.**

### Phase 2 — Research

Once outline is approved (and the section weighting from Phase 3 has been agreed during Phase 1 kickoff):

**Calibrate research depth per section to the agreed weighting.** Don't research everything to the same depth — see Phase 3 *Weighting meaning* table. Briefly:

- **Heavy** sections: textbook + review articles + primary-literature cohort data (specific frequencies, prevalences, outcome stats). 4–7+ refs.
- **Standard** sections: textbook + 1–2 supporting papers. 2–4 refs.
- **Light** sections: textbook only. 1 ref.
- **Skip** sections: no research time.

Then:

0. **Offer to auto-fetch any missing sources** via `sources-fetch.md` before manual reading begins. List what the kickoff named (textbook chapter, guideline, landmark papers), check what's already in `Sources/`, and offer to fetch the rest via the `sources-fetch.md` ladder (local library → free open-access API → browser → browser with optional auto-VPN; see `sources-fetch.md` and `CLAUDE.md §8–9`). Skip if the user says they'll handle it themselves or everything is already in `Sources/`. The fetched files land in `Sources/`; their citations land in `Sources/_acquisition_log.md`, which step 4 below reads when populating the sources summary table.
1. Read the user-supplied PDFs in `Sources/` — start with the primary textbook chapter, then secondary, then guidelines. Don't infer details from training knowledge.
2. For Heavy sections, find and verify primary-literature PMIDs (key cohort papers, landmark trials). Web-search each PMID before adding to the master reference list — see `references.md`. Any newly-identified paper can be queued for `sources-fetch.md` instead of being downloaded by hand.
3. Build a Vancouver-style master reference list at the **top** of `Documents/{Topic} outline.md`.
4. **Populate the sources summary table at the bottom of the outline**, under a `## Build aids — not for slides` section header. This is a build aid for the outline only — **it never gets copied into a slide**. Format and column definitions live in `references.md`. Its purpose: let the user sync papers they don't yet have on hand, and distinguish what came from `Sources/` vs. what Claude pulled from web search. The same `## Build aids — not for slides` section also hosts the figure summary table (Phase 3; see `images.md`).

5. Report back: surprises in the textbook vs. what was expected; any reference issues caught.

### Phase 3 — Outline drafting

Expand the approved outline into slide-by-slide content in `Documents/{Topic} outline.md`. For each slide:

- Slide number + title
- Bullet content (concise, not paragraphs)
- `Ref:` line with master-list reference numbers
- Cohort prevalence numbers, tables, drug regimens where relevant
- Figure placeholders explicitly marked (see Phase 5)

As you mark figure placeholders, add a row to the **figure summary table** at the bottom of the outline (in the `## Build aids — not for slides` section started in Phase 2). The figure table sits next to the sources summary table; format and column definitions live in `images.md`.

**Annotate the slide-content boundary explicitly.** The outline file mixes deck content with working aids. Add two visible markers so a reader (human or Claude) can see at a glance which parts become slides:

- After the master reference list, before the first section: a `> **▼ SLIDE DECK CONTENT — STARTS BELOW ▼**` blockquote.
- After the last reference slide, before `## Build aids — not for slides`: a `> **▲ END OF SLIDE DECK CONTENT ▲**` blockquote.

See the Example outline structure section below for the exact wording. Everything between these two markers is what the deck-build flow will turn into slides; everything outside them is metadata.

Convention: master reference list at the top of the outline; slide content bracketed by the two boundary markers; both the sources summary table and the figure summary table sit at the bottom under `## Build aids — not for slides`. Build aids never propagate into the slide deck. See `references.md` for the sources table format and `images.md` for the figure table format.

#### Topic-type-specific outline structures

Most resident-level topic reviews fall into one of six types. Each type weights the standard sections differently — what gets deep, extensive coverage vs. a brief mention vs. skipped. **This is guidance, not a script.** Always present the proposed weighting to the user during Phase 1 kickoff, get their confirmation, and let them override per topic before any research begins.

##### Section menu (used across all types)

| Section | What it covers |
|---|---|
| **A. Epidemiology** | Incidence, prevalence, demographics, risk factors at population level |
| **B. Pathophysiology** | Mechanism — why this happens |
| **C. Clinical presentation** | History, examination, natural history, bedside view |
| **D. Differential diagnosis** | Related / mimic conditions, how to distinguish |
| **E. Investigation / diagnosis** | Labs, imaging, biopsy, diagnostic criteria, algorithms |
| **F. Treatment / management / prevention** | Therapy (acute + chronic), evidence, dosing, monitoring, primary / secondary prevention |
| **G. Prognosis / outcomes** | Mortality, complications, follow-up |
| **H. Local context** | Thai / local guideline, drug availability, NHSO coverage |
| **I. Special populations** | Pregnancy, elderly, immunocompromised, specific subgroups |
| **J. Recent updates / controversies** | Guideline updates, ongoing debates, trial-level changes |

##### Weighting meaning

Weighting drives **three things together**: how deep the research goes for that section, how many references back it up, and how many slides it gets. Not just slide count.

| Weight | Research depth | Reference density | Slide allocation |
|---|---|---|---|
| **Heavy** | Textbook **+ review articles + primary-literature cohort data**. Specific numbers — frequency of each symptom in real cohorts, prevalence stats, outcome percentages. The audience hears exact data, not generic "common in patients" language. | 4–7+ refs spread across the section's slides | Multiple slides with sub-sections; the focal point |
| **Standard** | Textbook **+ 1–2 supporting papers** for any non-trivial claim. The audience gets the framework and the headline evidence, not the deep cohort data. | 2–4 refs across 1–2 slides | 1–2 slides with the essentials |
| **Light** | Textbook-level only; brief mention. | 1 ref (often shared with an adjacent slide) | 1 slide, or a single bullet on another slide |
| **Skip** | None — no research time spent here. | 0 | 0 slides |

**Slide allocation is proportional** to deck size — the same weighting applied to a 30-slide deck and a 50-slide deck produces different slide counts but the same relative emphasis. The same is true for reference density: more references on a Heavy section in a 50-slide deck, fewer in a 30-slide deck, but the *ratio* of heavy-section refs to standard-section refs stays the same.

The point of weighting: a "Heavy" section is what separates a good resident topic review from a textbook recitation. Generic textbook coverage of every section reads as a wall of slides. Choosing 2–4 sections to research deeply (with primary literature and cohort numbers) gives the deck a clear point of view.

---

##### Type 1 — Disease entity

A single named disease (e.g., **IgA nephropathy, SLE, sarcoidosis, Crohn's disease, AIH**).

| Heavy | Standard | Light | Skip |
|---|---|---|---|
| B, C, D | E, F, H, J | A, G, I | — |

**Framing notes:**

- The audience should leave understanding *what the disease is* (B) and *how it shows up* (C, D). Investigation (E) and treatment (F) are covered properly but aren't the focal point.
- **Upgrade F to Heavy** if the disease has a complex treatment landscape (e.g., SLE biologics, IgA nephropathy with KDIGO 2024 updates, AIH steroids + azathioprine). Confirm with the user during Phase 1.

---

##### Type 2 — Syndrome / clinical pattern

A pattern with multiple causes (e.g., **hyponatremia, AKI, FUO, pancytopenia, NTM and MSK involvement, pneumonia in immunocompromised host, chemotherapy-induced nausea and vomiting**).

| Heavy | Standard | Light | Skip |
|---|---|---|---|
| B, C, D, E | F | H, J | A, G, I |

**Framing notes:**

- The audience should leave able to *recognise the pattern* and *work out which cause it is*.
- **B** is the pathophys of the syndrome itself (e.g., for hyponatremia: volume status, osmolality, AVP physiology).
- **D** is the causes of *this syndrome* (e.g., for hyponatremia: SIADH, hypovolemic causes, hypervolemic causes).
- **Upgrade F to Standard+ or Heavy** if the syndrome is highly treatment-oriented — e.g., chemo-induced N/V is mostly a treatment story; pneumonia in immunocompromised host needs antimicrobial coverage in detail. Confirm with the user.

---

##### Type 3 — Approach to X (symptom or DDx-finding workup)

Symptom or finding-based workup (e.g., **approach to dyspnea, chest pain, pleural fluid, cancer of unknown origin**).

| Heavy | Standard | Light | Skip |
|---|---|---|---|
| B, C, D, E | H | F, J | A, G, I |

**Framing notes:**

- The audience should leave with *a working algorithm* for the next patient with this presentation.
- **B** is the pathophys of how *each category of cause* produces the finding (e.g., for dyspnea: cardiac vs pulmonary vs metabolic mechanisms).
- **D** is the *categories of cause* themselves, with the framework that organises them.
- **E** is the *investigation algorithm* — what to order in what order, how to interpret pivots.
- **F is Light** because the goal is "get to the right diagnosis"; once you do, treatment is whatever that disease needs.

**Distinction from Type 2.** Types 2 and 3 share the same Heavy sections (B, C, D, E) but frame each differently. Type 2 starts from a defined syndrome and works through its subtypes. Type 3 starts from a symptom or finding and works upstream to categories. Confirm with the user which mode fits before drafting.

---

##### Type 4 — Management-focused (includes recent updates / guideline reviews)

Drug or therapy emphasis, or a guideline / trial update (e.g., **management of psoriatic arthritis, GDMT in HF, latest oncology trial review, new HF guidelines**).

| Heavy | Standard | Light | Skip |
|---|---|---|---|
| B, F | E, G, H, I, J | C, D | A |

**Framing notes:**

- The audience should leave knowing *what to do and why*.
- **B** is brief — just enough mechanism to ground the treatment choices.
- **F** is the talk's focus — drug classes, evidence, dosing, monitoring, special situations, prevention.
- **Upgrade C and D to Standard** if the diagnosis isn't trivially established — e.g., "management of pancytopenia" is both a management talk and a syndrome talk; diagnosis matters. Confirm with the user.

---

##### Type 5 — Emergency / acute management

Time-critical condition (e.g., **DKA, septic shock, status epilepticus, anaphylaxis**).

| Heavy | Standard | Light | Skip |
|---|---|---|---|
| C, E, F, H | B, D, I, J | A, G | — |

**Framing notes:**

- The audience should leave able to *recognise and act fast* on the next case.
- **C** is bedside recognition — what does this look like in real time.
- **E** is the rapid-investigation pivot — what to order in the first 15 minutes.
- **F** is the protocol — fluids, drugs, doses, sequence, monitoring endpoints.
- **H** is critical for emergencies — institutional protocols, what's stocked, who to call (intensivist, anesthesia, cath lab).
- **B and D are Standard**, not Light: the audience still needs to understand the underlying mechanism and the close-mimics that need different action.
- No skips — emergencies need broad coverage even if some parts are light.

---

##### Type 6 — Specific clinical scenario / decision-making

Situational, often diagnostic-test or biomarker focused (e.g., **perioperative cardiac risk, immunosuppression management, novel biomarkers in AKI, when to escalate dialysis**).

| Heavy | Standard | Light | Skip |
|---|---|---|---|
| E, F, H, J | B, G, I | — | A, C, D |

**Framing notes:**

- The audience should leave with *a defensible answer to the operational question* (when to use what, how to decide).
- **E** is the test / biomarker / decision tool itself — characteristics, when it changes management.
- **F** is the action that follows the decision.
- **H** is institutional — what's available locally, what the local protocols are.
- **J** is critical because scenario reviews are usually triggered by new evidence; the audience wants to know "what's changed and should we adopt it".
- A, C, D are skipped because the scenario assumes a defined clinical context — the talk isn't about teaching the disease, it's about the specific decision.

---

##### How to use this table during Phase 1

Before any research, present the proposed weighting to the user:

> *"I'd treat this as a Type N review with the following emphasis: Heavy on [sections], Standard on [sections], Light on [sections], Skip on [sections]. Does that match what you want, or would you like to shift any weights?"*

Capture the agreed weighting in the outline metadata header. The weighting drives **two downstream phases**:

- **Phase 2 (Research)** — depth and reference effort per section follows the weighting. Heavy sections trigger primary-literature search for cohort data; Standard sections add 1–2 supporting papers to textbook coverage; Light sections stay at textbook only; Skip sections get no research time. Don't research everything to the same depth — the point of weighting is to focus effort on what the audience should remember.
- **Phase 3 (Slide allocation)** — Heavy sections get multiple slides with sub-sections; Light sections get 1 slide or a single bullet. Adjust if the user shifts weights.

**Don't apply this table silently** — the value is in the conversation about emphasis *before* any work begins. The user can also adjust later if the talk evolves.

For any disease-syndrome slide, apply `clinical-depth.md` (bedside layer).

For any slide that states a clinical recommendation from a named guideline, apply `evidence-grading.md` (grade + system + guideline year on the recommendation line; flag conflicts between societies or with the local guideline rather than picking one silently).

**Section 3 (Heavy clinical) — apply the "recognition" frame.** For each organ-system slide in a Heavy clinical section, structure content around bedside recognition:

1. **What the patient complains of** — symptoms in the patient's own words
2. **What the examiner finds** — physical exam findings, including bedside tests (e.g., phenylephrine test for scleritis vs episcleritis)
3. **What's specific to this disease vs non-specific** — for each finding, flag whether it points to the named disease or could be many things
4. **How to distinguish from the closest mimic** — name the comparator; never make a "specific" claim without saying compared to what

This frame is non-negotiable for the Heavy clinical section. A bullet list of organ-system findings without the patient/examiner perspective fails the audience's recognition need. See `clinical-depth.md` for the full bedside-layer pattern.

**One slide per major organ system** when the section is Heavy — don't cram eye + skin + nerve + CNS + cardiac onto one consolidated slide. Each organ deserves its own slide with at least one image placeholder.

**Slide-removal trigger** — if at any point during outline drafting the user asks to remove a slide, cut a section, or trim content:

1. Note the cited refs on the to-be-removed slide(s)
2. Edit the outline to remove the slide(s)
3. Run `audit_references.py` (see `reference-audit.md`)
4. Show user the newly-orphaned refs; ask to remove from master list (default yes)
5. Apply confirmed removals to master list and sources summary

Do NOT delete files in `Sources/` as part of this — only the master-list entry. Files persist by `safe-file-operations.md` discipline.

### Phase 4 — Build deck

**Confirm the completed outline with the user before starting to build.** If the user has not approved the slide-by-slide outline from Phase 3, do not begin building.

**Mandatory entry step — run the reference audit BEFORE any python-pptx work.** See `reference-audit.md`:

```bash
python3 framework/building-blocks/audit_references.py \
    "{Department}/{Topic}/Documents/{Topic} outline.md" \
    "{Department}/{Topic}/Sources/"
```

If the audit reports BROKEN citations or other issues, surface them and resolve before proceeding. Don't propagate broken refs into the deck.

Build the deck from `{Topic} outline.md` per `deck-build.md`. The deck-build flow will ask about theme/template upfront (Step 1 of `deck-build.md`) if not already established in Phase 1.

**Naming convention:**

- Outline file: `Documents/{Topic} outline.md` — e.g., `Hyponatremia outline.md`
- Deck working copies: `Deck/{Topic} slide v1.pptx`, `v2.pptx`, ... — e.g., `Hyponatremia slide v1.pptx`
- Final version: the user assigns the `(Final)` label themselves. **Never name a working copy `(Final)`.**

Verify slide count and image count after each build pass.

If a colleague's existing PPTX must be preserved, use the unpack/repack XML mode described in `deck-build.md`.

### Phase 5 — Image sourcing

**Default behaviour: Claude does NOT crop or place images automatically.** Past attempts at automated cropping produced poorly-framed figures and clipped key findings. Instead:

1. For each slide that needs an image, Claude inserts a **labelled placeholder textbox** describing the intended figure: modality, finding to illustrate, candidate source paper, license to verify. The user inserts the actual image themselves during deck review.
2. If the user has already placed image files in `Sources/Figures/`, Claude embeds them at **original aspect ratio (no cropping; resizing is fine)** and positions them simply. The user fine-tunes placement during deck review.
3. Only if the user explicitly asks Claude to source and place images directly, follow the full PMC + license workflow in `images.md`.

Whenever an image is embedded, license + caption discipline still applies (PMC ID, license name, paper-derived caption) — see `images.md`.

> *Note: this default-to-placeholder rule should also be reflected in `images.md` when that building block is next revised.*

### Phase 6 — Visual QA

Apply `visual-qa.md`:

- Render the deck to PDF using LibreOffice.
- Extract PNG thumbnails for representative slides.
- View each thumbnail and check for overflow / overlap / truncation / auto-shrink / theme drift.
- Build a contact sheet for decks of substantial size.
- Don't just trust "it built" — visually verify.

### Phase 7 — Speaker notes + mock Q&A *(optional)*

Ask the user at the start of this phase: *"Do you want me to generate speaker notes and a mock Q&A document?"* The user can request both, one, or neither.

**If speaker notes** — apply `speaker-notes.md`:

- For each slide, draft a few sentences in the audience's language with English medical terminology preserved.
- Save to `Documents/Speaker_notes.md` AND embed in the .pptx notes pane.

**If mock Q&A** — apply `mock-qa.md`:

- Generate anticipated faculty questions across the deck (volume scales with deck size — confirm with the user).
- Difficulty graded ★ (foundation) to ★★★ (advanced).
- Tagged `[in deck — slide N]` or `[beyond deck]`.
- Final "Faculty-feedback gap questions" section for the most valuable items.
- Save to `Documents/Mock_questions.md`.

If the user declines both, end the workflow at Phase 6.

---

## Example outline structure (worked skeleton)

The skeleton below demonstrates how the metadata header, master reference list, slide-by-slide content, and the two build-aid tables coexist inside a single `{Topic} outline.md`. Topic: **Hyponatremia** (illustrative).

````markdown
# Hyponatremia — Topic Review Outline

**Audience:** Internal Medicine residents (2nd–3rd year)
**Duration:** 35 min talk + 10 min Q&A
**Slides:** ~40 planned
**Theme:** Academic navy (Pantone 533 C primary / 1797 C accent)
**Speaker notes:** Thai narrative, English medical terms preserved
**Date:** 2026-06-15

---

## Master reference list (Vancouver style)

### Textbooks
1. Mount DB. Hyponatremia. In: Loscalzo J et al., editors. Harrison's Principles of Internal Medicine. 21st ed. McGraw-Hill; 2022. Ch. 121.
2. Sterns RH. Disorders of plasma sodium. In: Yu ASL et al., editors. Brenner & Rector's The Kidney. 12th ed. Elsevier; 2024. Ch. 16.

### Guidelines
3. Spasovski G, et al. Clinical practice guideline on diagnosis and treatment of hyponatraemia. Eur J Endocrinol. 2014;170(3):G1–47. (PMID 24569125)
4. Verbalis JG, et al. Diagnosis, evaluation, and treatment of hyponatremia: expert panel recommendations. Am J Med. 2013;126(10 Suppl 1):S1–42. (PMID 24074529)

### Primary literature
5. Adrogue HJ, Madias NE. Hyponatremia. N Engl J Med. 2000;342(21):1581–9. (PMID 10816188)
6. Sterns RH, Riggs JE, Schochet SS. Osmotic demyelination syndrome following correction of hyponatremia. N Engl J Med. 1986;314(24):1535–42. (PMID 3713747)
7. Garrahy A, et al. Continuous versus bolus infusion of hypertonic saline in symptomatic hyponatremia. J Clin Endocrinol Metab. 2021;106(8):e3007–18. (PMID 33954787)
... (continue numbered list — typically 20–30 entries in total)

---

> **▼ SLIDE DECK CONTENT — STARTS BELOW ▼**
> Everything from this marker down to "**END OF SLIDE DECK CONTENT**" becomes slides in the .pptx. The metadata block and master reference list above are working aids — they do not appear in the slides.

---

## Section 1 — Introduction & epidemiology

### Slide 1 — Title slide
- Title: Hyponatremia — A Clinical Approach
- Subtitle: A topic review for Internal Medicine residents
- Presenter / date / footer

### Slide 2 — Why this matters
- Most common electrolyte disorder in hospitalised patients (~15–30%)
- Independent predictor of mortality across multiple settings
- Both under-correction and over-correction cause harm
- Ref: 3, 5

### Slide 3 — Section divider: "1. Definition & classification"

### Slide 4 — Definition & severity grading
- Plasma sodium < 135 mmol/L
- Severity grading by serum Na AND symptoms (per Spasovski 2014)
- Acute (<48 hr) vs chronic (>48 hr) — clinical implication
- Ref: 3

... (slides 5–7 continue this section)

## Section 2 — Pathophysiology

### Slide 8 — AVP regulation
- AVP physiology recap
- Effective osmolality vs measured osmolality
- The role of free water intake
- [FIGURE: AVP regulation cascade diagram — to recreate as PowerPoint shapes]
- Ref: 1, 5

... (Sections 3–5 omitted for brevity)

## Section 6 — Treatment & local context

### Slide 28 — Hypertonic saline protocol
- Symptomatic hyponatremia: 150 mL of 3% NaCl over 20 min, repeat ×2 if needed *(Spasovski 2014 — Strong recommendation, low-quality evidence)*
- Target: 4–6 mmol/L rise in serum Na in the first hour *(Spasovski 2014 — Strong recommendation, low-quality evidence)*
- Recheck Na q1h until stable
- [FIGURE: Schema — bolus vs continuous infusion protocols]
- Ref: 3, 7

### Slide 30 — Local context (Thailand)
- 3% NaCl availability — confirm institutional pharmacy stock
- NHSO (สปสช.) coverage considerations for hypertonic saline preparation
- Tolvaptan cost / access: Universal Coverage vs Social Security vs private pay
- Reference labs for serum / urine osmolality if not done in-house
- Ref: 3, 4, local

... (slides 31–38 continue)

## Reference slides (deck-end)

### Slide 39 — References (1/2): Textbooks + Guidelines
- Entries: 1, 2, 3, 4

### Slide 40 — References (2/2): Primary literature
- Entries: 5, 6, 7, 8, 9, 10, ...

---

> **▲ END OF SLIDE DECK CONTENT ▲**
> Everything below this marker is a working aid — none of it gets copied into a slide.

---

## Build aids — not for slides

### Sources summary

| Source | Type | Location | Status |
|---|---|---|---|
| Harrison's IM 21e Ch. 121 (Mount) | textbook chapter | `Sources/` | provided by user |
| Brenner & Rector 12e Ch. 16 (Sterns) | textbook chapter | `Sources/` | provided by user |
| Spasovski 2014 European hyponatremia guideline | guideline | online PDF | not yet in `Sources/` — user to download |
| Verbalis 2013 expert panel | guideline | online PDF | not yet in `Sources/` — user to download |
| Adrogue & Madias 2000 (PMID 10816188) | landmark paper | online — DOI + PMC link | not yet in `Sources/` — user to download |
| Sterns 1986 osmotic demyelination (PMID 3713747) | landmark paper | online — DOI + PMC link | not yet in `Sources/` — user to download |
| Garrahy 2021 hypertonic saline RCT (PMID 33954787) | RCT | online — DOI + PMC link | not yet in `Sources/` — user to download |

### Figure summary

| Slide | Figure description | Status | Source & action for user |
|---|---|---|---|
| 8 | AVP regulation cascade diagram | not yet placed | Recreate as PowerPoint shapes — no suitable open-access version. |
| 14 | Diagnostic algorithm (volume status → osmolality → tonicity) | not yet placed | Recreate as PowerPoint flowchart. |
| 19 | MRI brain T2 FLAIR — central pontine myelinolysis | placeholder | Candidate: PMC9824631 (CC-BY). User to download from PMC. |
| 22 | Plot — sodium correction rates vs. ODS risk | placeholder | Candidate: Sterns 1986 reproduced in Garrahy 2021 supplement (verify license). |
| 28 | Schema — hypertonic saline bolus vs continuous | not yet placed | Recreate as PowerPoint schema. |
| 33 | Photo — tolvaptan tablets (illustrative) | not yet placed | No candidate identified — consider skipping or use generic Rx illustration. |

### Paper summaries

> Added on user request only. Format and content per `framework/content-modules/paper-summary.md`. Example card shown below — in a real outline, you'd have one card per landmark paper the user asked about.

#### Garrahy 2021 — Hypertonic saline RCT

**Citation:** Garrahy A, et al. Continuous versus bolus infusion of hypertonic saline in symptomatic hyponatremia. J Clin Endocrinol Metab. 2021;106(8):e3007–18. (PMID 33954787)

**Design:** Multicentre, prospective, randomised, open-label trial.

**PICO:**
- **P:** Adults with symptomatic hyponatremia (Na ≤ 125 mmol/L + moderate/severe symptoms); n = 22.
- **I:** Continuous infusion of 3% NaCl titrated to target sodium rise.
- **C:** Bolus 150 mL of 3% NaCl over 20 min, repeat up to ×3.
- **O:** Primary — proportion achieving target rise (4–10 mmol/L) at 24 h without overcorrection.

**Key results:**
- Target rise achieved without overcorrection: 73% (bolus) vs 64% (continuous), no significant difference.
- Mean rise at 6 h similar between groups.

**Quality / risk of bias:** Small open-label RCT (n = 22); underpowered for clinical outcomes; pragmatic design.

**Remark:** Both bolus and continuous regimens appear equivalent for short-term targets; institutional preference and overcorrection-monitoring infrastructure should drive the choice. Main caveat: small sample limits firm conclusions on rare events like osmotic demyelination.

**How to use in this deck:**
- Slide 28 (hypertonic saline protocol), Ref #7
- Verbatim quote for that slide pending — user to select from full text once Sources/ has the PDF.

````

### Notes on the structure

- The **metadata header** at the top captures everything `deck-build.md` will need: audience, duration, slide count, theme palette, speaker-note language, date. Update it as those choices are finalised in Phase 1.
- The **master reference list** is grouped (textbooks / guidelines / primary literature) but **numbered continuously** so per-slide `Ref:` lines can reference any entry with a single number.
- The **slide-deck boundary markers** (`▼ SLIDE DECK CONTENT — STARTS BELOW ▼` and `▲ END OF SLIDE DECK CONTENT ▲`) bracket the part of the outline that becomes slides. The user can edit anywhere between them and know it will land in the deck; anything outside them is working metadata.
- **Slides** are listed flat in the order they appear in the deck. `## Section N — Title` headers in the outline are organisational only — each section divider also gets its own slide entry.
- Each slide entry shows title, bullet content, `[FIGURE: ...]` placeholders where needed, and a `Ref:` line.
- Below the end marker and the `## Build aids — not for slides` header is metadata for the build process. Both summary tables live here.

---

## Folder structure

Set up before Phase 2 (also documented in `CLAUDE.md` Section 5):

```
{Department}/                            # e.g., Internal Medicine, Rheumatology
└── {Topic}/
    ├── README.md
    ├── Sources/                         # textbook PDFs, guidelines, primary papers
    │   └── Figures/                     # user-provided images to embed
    ├── Documents/                       # markdown outputs
    │   ├── {Topic} outline.md
    │   ├── Speaker_notes.md             # if Phase 7 done
    │   ├── Mock_questions.md            # if Phase 7 done
    │   └── Faculty_feedback.md          # filled after the talk
    ├── Deck/                            # PPTX + PDF deliverables (live working copies)
    │   ├── {Topic} slide v1.pptx → v2 → ...
    │   └── {Topic} slide (Final).pptx + (Final).pdf
    └── Build_archive/                   # working files (keep, don't delete)
        ├── Section_PPTXs/                # standalone section rebuilds (see deck-build.md Step 7)
        ├── Backups/                      # safety copies before risky edits (see safe-file-operations.md)
        └── Old_versions/                 # superseded full-deck iterations the user no longer edits
```

Tell the user this structure during Phase 1 and create the folders before Phase 2.

---

## Post-presentation update

After the talk, faculty typically identify gaps. To integrate them:

1. **Read `safe-file-operations.md` first.** This is non-negotiable.
2. Capture faculty comments in `Documents/Faculty_feedback.md`.
3. Back up the finalised deck with a dated name BEFORE modifying.
4. Write the modified version to a NEW filename, not the original.
5. Verify file size + slide count + image count + speaker-note count against the backup before reporting done.
6. Update `Documents/Mock_questions.md` with the actual questions asked and which were gaps.

---

## Conventions worth keeping

- **Vancouver-numbered references** — master list at top of outline; per-slide `Ref:` numbers (see `references.md`).
- **Verify every PMID** by web search before adding (see `references.md`).
- **Slide-deck boundary markers** in the outline — `▼ SLIDE DECK CONTENT — STARTS BELOW ▼` after the master reference list and `▲ END OF SLIDE DECK CONTENT ▲` before the build aids. Everything between them becomes slides; everything outside is working metadata. See the example outline section for the exact format.
- **Build-aid sections at the bottom of the outline**, under a `## Build aids — not for slides` section header:
  - **Sources summary table** — papers / textbooks / guidelines; what's in `Sources/` vs. what the user still needs to download (see `references.md`).
  - **Figure summary table** — every planned figure; status (`placeholder` / `in Sources/Figures/` / `not yet placed`), source, action for the user (see `images.md`).
  - **Paper summaries** — PICO-format cards with one-line RoB + 1–2 sentence remark for landmark papers, added **on user request only** (see `paper-summary.md`).
  - Build aids never propagate into the slide deck.
- **Standalone section PPTXs during iteration** — when rebuilding one section, generate it as its own .pptx so the user can integrate without overwriting their edits.
- **Speaker notes in audience's language with English medical terms preserved** (see `speaker-notes.md`).
- **No automated image cropping by default** — use placeholders; let the user insert real images (see Phase 5).
- **Topic-named files** — `{Topic} outline.md` and `{Topic} slide v1.pptx`, not generic names.
- **Confirm outline before building** — Phase 4 does not start until the slide-by-slide outline is signed off.

---

## Safety reminders

The full safety discipline lives in `safe-file-operations.md`; read it before any rebuild that touches a "Final" or "important" file. Backstory and context for these rules live in `framework/retrospective.md`.

---

## Quick-start checklist

- [ ] Decide rotation, topic, audience, slide count, duration, primary sources
- [ ] Create folder structure (`Sources/`, `Documents/`, `Deck/`, `Build_archive/Backups/`, `Build_archive/Section_PPTXs/`, `Build_archive/Old_versions/`)
- [ ] Classify topic type (Types 1–6) and propose section weighting; get user approval before research
- [ ] Drop primary-source PDFs into `Sources/`; auto-fetch the rest via `sources-fetch.md`
- [ ] Read source PDFs; verify every PMID via web search before adding to master reference list
- [ ] Build outline with master reference list (top), slide-by-slide content between `▼`/`▲` markers, and `## Build aids — not for slides` (sources summary + figure summary) at the bottom
- [ ] Run `audit_references.py` at end of Phase 3; resolve any BROKEN / ORPHANED entries before building
- [ ] Confirm outline with user; confirm theme/template (Step 1 of `deck-build.md`)
- [ ] Build deck per `deck-build.md`; visual QA per `visual-qa.md`
- [ ] Speaker notes + mock Q&A per Phase 7 (optional)
- [ ] Apply `safe-file-operations.md` before any rebuild or post-presentation update

---

*Topic-review workflow — thin wrapper over the framework building blocks. Always confirm outline structure and section weighting before research begins.*
