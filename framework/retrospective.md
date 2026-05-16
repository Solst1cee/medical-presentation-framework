---
name: retrospective
description: Rolling log of presentations built with this framework — what worked, what got codified, project backstory behind the rules in safe-file-operations.md and the content modules. Read once at the start of a new project; appended to after each new presentation. Not intended to auto-trigger; loaded by reference from CLAUDE.md and other framework files.
---

# Retrospective — Medical Presentation Framework

A rolling log of presentations built with this framework. Each entry captures one real project: what worked, what the audience flagged, what got codified into the framework as a result.

**Purpose**

- The skill files in `framework/` state each rule and convention without backstory (by design). This file is where the backstory lives — *why* a given building block, content module, or safety rule exists in the first place.
- Each new presentation built with the framework should add a new case section. Over time the log becomes a worked-example library that a contributor can read to understand both the framework and the kinds of problems it was shaped to handle.
- Read the existing cases once at the start of a new presentation to remember patterns that have already been validated.

**How to add a new case**

Append a new section under "Cases", using the Case 1 entry as a template:

1. **Header** — project name, format (topic review / journal club / case discussion / etc.), and rotation or context.
2. **Outcome** — one line.
3. **What worked — keep doing** — patterns to preserve.
4. **What to fix next time** — feedback received, with each item ending in `**Codified as:** {skill file path}` if it produced a new rule.
5. **Critical lessons** — only if a process failure happened; describe what went wrong and which safety rule it produced.
6. **Process improvements** — anything you want to remember to apply earlier next time.

---

## Cases

### Case 1 — NTM and Musculoskeletal Involvement (Topic review, Rheumatology, May 2026)

**Outcome:** Successfully presented; archived 5 May 2026. This was the founding project — most of the framework's current building blocks, content modules, and the safety discipline were derived from what worked and what failed here.

#### What worked — keep doing

1. **Structured workflow** — clarify rotation/source/file → propose outline → research from PDFs → build → visual QA → finalize. Each gate prevented wasted effort.
2. **Reading actual textbook PDFs**, not inferring from training knowledge. The K&F 12e Ch. 114 chapter changed details we'd otherwise have gotten wrong (chapter number, exact page references, specific phrasing).
3. **Verification of every PMID** via web search before adding to the reference list. Caught Winthrop PMID error (19861050 → 19861045).
4. **Standalone section PPTXs** for incremental delivery. When the user edited the master deck, building standalone "Osteomyelitis only", "Bursitis only", "MSK Syndromes section v2", "Diagnosis section only", "Master References only" PPTXs let them integrate piecemeal without overwriting their edits.
5. **Vancouver-numbered references** with a master list. Gave consistent numbering across the deck and outline; easy to add new refs (e.g., #25 Fujieda was added cleanly).
6. **Speaker notes in Thai with English medical terminology** — natural for Thai medical-resident audiences; preserves terms exactly as taught at the home institution.
7. **Open-access image sourcing with explicit license + caption from source paper** — every figure on a slide had a paper-derived caption + PMC ID + license, ready for archive.
8. **Mock Q&A document** as an additional pre-presentation artifact — directly anticipated faculty questions.

#### What to fix next time — feedback received

**1. More clinical presentation depth in each MSK syndrome.** The deck had risk factors, imaging, microbiology, treatment — but the **patient encounter** layer was thin. The professor wanted the bedside view: history (duration, pain quality, exposures), examination (e.g., for NTM tenosynovitis: nodular swelling along flexor sheath, reproducible Tinel's sign, *absence* of erythema in chronic disease, firm/doughy mass vs the soft fluctuant feel of acute pyogenic infection), and cohort prevalence numbers per symptom (e.g., "constitutional symptoms in only 40% of a Thai tertiary-centre cohort, fever 36%"). Use both **textbook** (clinical features the editors emphasize) and **research data** (cohort symptom prevalence).
**Codified as:** `framework/content-modules/clinical-depth.md`

**2. Comparison with TB across all axes — not just one slide.** The TB-vs-NTM contrast existed on a single septic-arthritis slide. The professor wanted comparison across **risk factors, symptoms, examination, investigation profile, and treatment** — distributed throughout the deck or on a dedicated comparison page early on. Pattern: a dedicated comparison slide immediately after introducing the topic, per-syndrome inline comparison columns in tables, or a two-colour highlight throughout the deck. Applies whenever the topic has a clinical mimic (NTM↔TB, gout↔pseudogout, RA↔PsA, etc.).
**Codified as:** `framework/content-modules/disease-comparison.md`

**3. Local (Thai) guideline / drug availability.** International guidelines (ATS/IDSA, ACR) were cited but practical availability in Thailand was not. Every drug-related slide should pair the international regimen with a "Available in Thailand?" footnote covering: Royal College of Physicians of Thailand / specialty-society guidance, hospital pharmacy stock, NHSO (สปสช.) coverage, cost (private pay vs Universal Coverage vs Social Security), reference labs for specialised tests (e.g., anti-IFN-γ ELISA available only at select tertiary referral centres in Bangkok), and common substitutions (e.g., rifampin in place of rifabutin, with caveats).
**Codified as:** `framework/content-modules/local-guideline.md`

#### Critical lesson — backup before destructive operations (8 May 2026)

During a post-presentation update to the NTM deck, a "rebuild + replace finalized PPTX" task was delegated to a subagent. The subagent reported success but actually delivered a file with 50 of 57 slides as empty placeholders, zero embedded images, and only 15 of 55 speaker notes preserved. The original 6 MB finalized deck had already been overwritten by the time the failure was detected. The only surviving copy was a backup the user had made independently on their own machine.

This was a process failure, not a content failure. The three rules broken:

1. **Don't overwrite a finalized file** — write the new version to a different filename first; let the user verify before renaming.
2. **Don't delegate destructive work to a subagent without making the backup yourself** — subagents can misreport success.
3. **Don't trust subagent "success" reports** without independent verification (file size, slide count, image count, content spot-check).

**Codified as:** `framework/safe-file-operations.md`

#### Process improvements that came out of this project

1. **Ask about local guidelines as part of the initial clarification** — should be a default question for any non-US/non-UK audience, not an afterthought.
2. **Default to including a clinical-presentation block** in any disease-syndrome slide. The "what does the patient look like" layer was systematically thin.
3. **Default to building a comparison slide** when the disease has a clinical mimic.
4. **Reduce file truncation** — multiple times during this project, large Python build scripts ended with truncated text on disk. Keep individual edits smaller, verify file integrity after each Edit, and prefer Write over multiple Edits when restructuring large blocks.
5. **Faster image sourcing** — batch search early in the build phase, present all candidates at once, and lock in licensing decisions before any embedding.
6. **Earlier mock Q&A** — generate the mock Q&A document around the time the deck reaches v2/v3, not just at the very end. The user can then prepare alongside continued slide refinement.

---

### Case 2 — Granulomatosis with Polyangiitis (Topic review, Rheumatology, May 2026)

**Outcome:** v3 deck delivered; v4 rebuild in progress with vertical-cell-anchor bug fix and projection font defaults applied. Three full rebuilds (v1 burgundy small-fonts → v2 navy template-matched → v3 burgundy template-matched + projection fonts) were needed because the initial defaults didn't match a conference-room audience's needs.

#### What worked — keep doing

1. **Phase-by-phase check-ins** — kickoff → research → outline → build → QA. The user could course-correct between phases instead of waiting until the end to flag issues.
2. **Library + sources-fetch workflow** — the user's library root (configured in `CLAUDE.md` Section 7) with `library-index.md` made Firestein/Harrison extraction fast once the library entry was added. The librarian skill handled renaming + index updates cleanly when the user dropped `nrrheum.2017.140.pdf` (Bossuyt 2017).
3. **Outline as source of truth with boundary markers** — `Documents/{Topic} outline.md` with `▼ SLIDE DECK CONTENT — STARTS BELOW ▼` / `▲ END OF SLIDE DECK CONTENT ▲` markers made it possible to rebuild the deck three times without re-doing the research or losing references.
4. **PDF render + thumbnail extraction for visual QA** — `soffice → pdftoppm → JPEG` caught font-size and layout issues immediately after every build.
5. **Subagent for citation verification** — research subagent verifying 30+ PMIDs in its own context kept the main conversation lean. (Failed for Chrome MCP fetches, but worked well for PubMed verification.)
6. **Saving intermediate deck versions** — `v1.pptx`, `v2.pptx`, `v3.pptx` all kept in `Deck/` so the user could compare design directions side-by-side instead of relying on memory.

#### What to fix next time — feedback received

**1. Default font sizes were screen-reader, not projection-reader.** v1 used 11–14 pt body and 9–11 pt table cells — readable on a laptop but unreadable from row 5 of a 30-seat conference room. The framework's stated 16–18 pt body floor wasn't actually honored. v3 corrected to 18 pt body floor (16 pt for italic/grey/dense table content); section divider title 46 pt; header bar 26 pt.
**Codified as:** `framework/building-blocks/deck-build.md` Step 3 — projection-ready defaults (BODY_SIZE=18, HEADER_SIZE=26, TABLE_BODY_SIZE=15 with 14 as the floor).

**2. Slide-bottom reference lines need both a number AND the full citation, in a dynamically-sized textbox.** This rule took three iterations to settle.

- v1–v4 used **number-only** lines (`Ref: 1, 2, 14`). User feedback: hostile to the audience — forces them to flip to the deck-end reference slides to know what's cited.
- v5 switched to **compact Vancouver joined with ·** (`Hoffman GS et al. Ann Intern Med 1992;116:488 · Langford CA, Fauci AS. Harrison's IM 21e Ch 363`). User feedback: still missing the master-list number, so audience can't cross-reference back to the reference slides.
- Final convention (v5b–v6): **numbered full Vancouver, one per line, sorted ascending by number**:

  ```
  1. Langford CA, Fauci AS. The vasculitis syndromes. In: Harrison's Principles of Internal Medicine. 21st ed. McGraw-Hill; 2022. Ch. 363.
  15. Hoffman GS, et al. Wegener granulomatosis: an analysis of 158 patients. Ann Intern Med. 1992;116(6):488–98.
  23. Bossuyt X, et al. Revised 2017 international consensus on testing of ANCAs in GPA and MPA. Nat Rev Rheumatol. 2017;13(11):683–92.
  ```

- v5 had a layout regression: the fixed-tall ref textbox (1.15") wasted space on slides with 1–2 refs and overlapped body content on slides with bottom-anchored italic notes (e.g., the "Thai context" note on slide 32). **v6 fix: dynamically size the ref textbox** — calculate height from ref count + wrap estimate (110 chars/line at 9pt italic, 0.18" per visual line), then anchor the box to slide bottom (`y = SLIDE_H - calculated_h - 0.08"`). Vertical anchor inside the textbox = bottom (text flush with bottom edge). Slides with 1 ref get a small box hugging the slide bottom; slides with 6 refs get a taller box that grows upward as needed.

**Codified as:**
- `framework/building-blocks/references.md` — on-slide ref format = numbered full Vancouver, stacked, dynamic-sized textbox bottom-anchored. Anti-pattern examples flag BOTH "Ref: 1, 5, 23" (number-only) AND "Hoffman 1992 · Bossuyt 2017" (compact-without-number).
- `framework/building-blocks/deck-build.md` — Pattern 4 includes the full `ref_line()` helper code template with the wrap-estimate constants and bottom-anchor logic.

**3. Tables need vertical-center cells by default.** python-pptx defaults cells to top-anchored, which looks ragged when cell content varies in line count. Also surfaced a recurring python-pptx gotcha: `cell.text_frame.vertical_anchor = MIDDLE` is silently no-op; the correct API is `cell.vertical_anchor = MIDDLE` (writes to `tcPr/@anchor`, which PowerPoint actually reads).
**Codified as:** `framework/building-blocks/deck-build.md` Pattern 4 — explicit code snippet showing the right vs wrong API.

**4. After every content trim, orphaned references accumulate in the master list.** When the user trimmed Section 6 in this project, 12 trial references were left orphaned. The user noticed and pushed back (×4 messages, emphatically). Manual `references.md` Phase 6 reconciliation gets skipped during fast iteration.
**Codified as:** `framework/building-blocks/reference-audit.md` + `audit_references.py` — automated audit script with triggers at slide-removal, Phase 3→4 transition, Phase 4 build start, and Phase 6 final reconciliation.

**5. Slide titles in marketing-tone are unwelcome in academic medical talks.** "Why this matters" was rejected; "Introduction" was the requested register.
**Codified as:** `framework/presentation-types/topic-review.md` — example outline structure now uses neutral journal-article phrasing for slide titles.

**6. Heavy clinical sections need a "recognition" frame, not a feature list.** For each organ system, the audience needs to know **(a) what the patient complains of**, **(b) what the examiner finds**, **(c) what's specific vs non-specific**, **(d) how to distinguish from the closest mimic**. A bullet list of features doesn't serve the audience's recognition need.
**Codified as:** `framework/presentation-types/topic-review.md` Phase 3 — added explicit "recognition frame" requirement for Heavy clinical sections. Each organ deserves its own slide.

**7. Comparative claims need explicit comparators.** "Migratory large-joint pattern is relatively GPA-specific" begs the question "compared to what?". The fix was a comparison table against RA, PMR, gout, SLE, spondyloarthritis explicitly.
**Codified as:** Strengthening in `framework/content-modules/clinical-depth.md` — any disease-specificity claim must name comparators or include a comparison table.

**8. Scope discipline — stay on the named disease.** For a GPA-focused talk, treatment overview tables shouldn't be pan-AAV; EGPA-specific triggers don't belong; resident-level audience doesn't need RAVE-vs-RITUXVAS-vs-CYCLOPS trial detail.
**Codified as:** `framework/presentation-types/topic-review.md` Phase 3 — added scope-discipline reminder; outside of differential section, MPA/EGPA content is out of scope.

**9. Ask about templates explicitly at Phase 1.** The user had a `templates/CINV.pptx` they wanted to match, but I didn't surface this question early enough — built v1 from defaults, then v2 after the user pointed at the template. Cost a full rebuild.
**Codified as:** `framework/presentation-types/topic-review.md` Phase 1 — Question 5 now explicitly tells Claude "always ask, don't assume; if the user mentions liking any prior presentation's design, treat as a template lead."

**10. Bedside-relevant detail beats abstract risk factors.** For occupational silica exposure (a GPA risk factor), "occupational silica" wasn't enough — the user wanted the actual questions to ask during history-taking (mining, quarrying, sandblasting, stonecutting, foundry, ceramics, dental laboratory).
**Codified as:** `framework/content-modules/clinical-depth.md` (next revision) — bedside layer should include exposure-history questions for risk-factor bullets, not just the abstract risk factor.

#### Critical lesson — verify what your tool actually writes (vertical anchor)

Three rebuilds in, the user asked "why aren't the tables vertically centered?" — I'd been setting `cell.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE` in good faith for every cell. Diagnostic XML inspection showed that this writes `<a:bodyPr anchor="ctr"/>` inside the cell's text frame — which PowerPoint ignores for table cells. The correct API is `cell.vertical_anchor = MSO_ANCHOR.MIDDLE`, which writes `<a:tcPr anchor="ctr"/>` on the cell properties.

**Rule generalised:** when a python-pptx visual change isn't taking effect despite the API call returning normally, unpack the produced `.pptx` and inspect the slide XML. PowerPoint's rendering follows the XML, not the library API surface. python-pptx has several silent-no-op gotchas where the wrong attribute path returns success but writes nothing useful.

**Codified as:** `framework/building-blocks/deck-build.md` Pattern 4 — explicit gotcha section showing both APIs and which one PowerPoint actually honors.

#### Process improvements

1. **Run the reference audit at every content-trim event** — don't wait until Phase 6. Three times in this project, orphaned references survived a trim and required the user to flag them. The audit script makes this automatic.
2. **Build small, render to PDF, check, iterate.** **Six full rebuilds were needed (v1 → v6)** in this project, each driven by specific user feedback that the prior defaults didn't honor: small fonts (v1), wrong color (v2), missing template (v2→v3 → wrong-after-all → v5), broken table vertical centering (v3→v4), number-only refs (v4→v5 short), refs without number (v5 compact→v5b numbered full), fixed-tall ref box overlap (v5b→v6 dynamic). Iterating in small visible steps was faster than trying to get it right in one giant pass. Visual QA after every build pass is non-negotiable.
3. **Ask about templates and color palette at Phase 1, not Phase 4.** The user revealed mid-project that they had a template they liked. If asked earlier, would have saved at least one full rebuild.
4. **For slide-bottom elements (refs, footers): use dynamic sizing, not fixed-height reserves.** A fixed-tall ref textbox wastes space on slides with few refs and crowds body content on slides with many. The framework now specifies dynamic sizing anchored to slide bottom — calculate height from content and anchor `top = SLIDE_H - calculated_h - margin`. This same pattern should be applied to any other slide-bottom element (footer, source attribution strip) for the same reason.
5. **Save audit output to a temp file before destructive operations** — when removing slides, the audit run BEFORE the cut is what identifies what becomes newly orphaned. Diffing pre/post audits is more reliable than scanning the post-cut state alone.
6. **For Pro / token-constrained users, build incrementally with state-save points** — `Documents/{Topic} outline.md` and `Deck/{Topic} slide vN.pptx` are the resume points. Don't try to do everything in one long subagent run; the GPA project hit a Pro session limit mid-Chrome-fetch and was only recoverable because the outline state was on disk.
7. **Chrome MCP downloads: verify file size after every operation.** A subagent reported "fetch succeeded" but the file never landed in `Downloads/` (silent state-issue in the browser). Trusting "success" cost a full subagent run.
8. **When using a subagent that the user can interrupt, save intermediate state on the side.** The acquisition log + outline + master reference list all live in committed files, so a subagent that exits abnormally doesn't lose work — only the trailing partial step needs replay.
9. **`Edit` tool truncation watch.** Twice in this project, `Edit` operations against medium-sized files (outline.md, audit_references.py) produced silently-truncated outputs. Always `wc -l` and `tail` after editing a script or long markdown file; if truncation is detected, fall back to `Write` (full-rewrite) rather than another Edit.

---

### Case 3 — (next presentation goes here)

> Template — copy the Case 1/2 structure: **Outcome → What worked → What to fix → Critical lessons → Process improvements**. Each "What to fix" item should end with a `**Codified as:**` line if it generalised into a new rule in `framework/`. If the lesson is project-specific, omit the codification line.

---

*This file grows over time. The framework files in `framework/` stay tight and prescriptive; the messy 