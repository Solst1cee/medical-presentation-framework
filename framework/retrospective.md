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

### Case 2 — (next presentation goes here)

> Template — copy the Case 1 structure: **Outcome → What worked → What to fix → Critical lessons → Process improvements**. Each "What to fix" item should end with a `**Codified as:**` line if it generalised into a new rule in `framework/`. If the lesson is project-specific, omit the codification line.

---

*This file grows over time. The framework files in `framework/` stay tight and prescriptive; the messy reality of each project lives here.*
