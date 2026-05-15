---
name: references
description: "Building block for managing references and citations in medical presentations — Vancouver-numbered master list, per-slide reference lines, PMID verification before adding, the sources summary build-aid table, and reference-slide assembly. Loaded by Read path from a presentation-type skill; not intended to auto-trigger on its own."
---

# Research & references workflow

## Why this matters

A medical presentation's credibility lives in its references. Two failure modes are devastating:

1. **Misattributed claims** — citing a guideline for content it doesn't actually contain (e.g., citing the 2020 ATS/IDSA pulmonary NTM guideline for an extrapulmonary regimen).
2. **Wrong PMIDs, page numbers, chapter numbers** — discoverable in seconds during faculty Q&A; instantly destroys trust.

This workflow exists to prevent both.

---

## Phase 1 — Source preference clarification (during outline drafting)

Ask the user up front:

> "What evidence base should this presentation prioritise?
> A) Textbook-based — core concepts from the standard textbooks
> B) Mixed — textbook for mechanisms; guideline + landmark trials for management
> C) Guideline + recent publication-based — current major guideline as backbone, supported by key RCTs and recent updates
> D) I'll provide the sources myself"

Record the answer. The reference style differs:

| Mode | Pathophysiology | Management | Citations |
|---|---|---|---|
| Textbook | Textbook chapters | Textbook algorithms | Author, book, edition |
| Mixed | Textbook + landmark paper | Guideline for management | Textbook + PMID |
| Guideline / Publication | Review articles + RCTs | Current guideline version | PMID throughout |

---

## Phase 2 — Source PDF management

Ask the user to drop reference PDFs into a `Sources/` folder. This is the **single most reliable** way to ground the content.

For every textbook chapter or major paper used:

1. Extract text with `pdftotext -layout`.
2. Read the actual chapter, not what you think the chapter says.
3. Note the chapter number, page range, and key direct quotes.
4. Add to the master reference list with verified bibliographic data.

Without reading the PDFs directly, chapter numbers, page ranges, and which guideline a chapter actually cites are all wrong-or-unverifiable.

---

## Sources summary table — outline.md build aid

At the bottom of `{Topic} outline.md`, maintain a **sources summary table** listing every textbook, guideline, and paper used in the deck. This is a **build aid for the outline only — it never gets copied into a slide**. Its purpose: give the user a single view of which sources are already on hand vs. which they still need to download to verify Claude's claims independently.

Place it under the `## Build aids — not for slides` section header (alongside the figure summary table from `images.md`):

```markdown
## Build aids — not for slides

### Sources summary

| Source | Type | Location | Status |
|---|---|---|---|
| Harrison's IM 21e Ch. 121 (Mount) | textbook chapter | `Sources/` | provided by user |
| Brenner & Rector 12e Ch. 16 (Sterns) | textbook chapter | `Sources/` | provided by user |
| Spasovski 2014 European hyponatremia guideline | guideline | online PDF | not yet in `Sources/` — user to download |
| Verbalis 2013 expert panel | guideline | online PDF | not yet in `Sources/` — user to download |
| Adrogue & Madias 2000 (PMID 10816188) | landmark paper | online — DOI + PMC link | not yet in `Sources/` — user to download |
```

### Column definitions

- **Source** — abbreviated citation (textbook + edition + chapter; guideline name + year; or first-author + journal + year + PMID for papers).
- **Type** — `textbook chapter` / `guideline` / `landmark paper` / `RCT` / `cohort study` / `review article` / `case series` / `meta-analysis`.
- **Location** — `Sources/` (user-supplied PDF folder); `online — DOI + PMC link`; `online PDF` (link only); `paywalled — needs library access`; etc.
- **Status** — `provided by user` (PDF is in `Sources/`) or `not yet in Sources/ — user to download` (Claude pulled from web search only).

### Update cadence

- Add a row to the table when each source enters the deck.
- Update `Status` from `not yet in Sources/` to `provided by user` once the user drops the PDF in.
- Keep the table in sync with the master reference list (at the top of the outline) through Phase 6 (final reconciliation).

### Why this table never goes into the deck

It's working metadata for the build process. Keeping it under the `## Build aids — not for slides` header — alongside the figure summary table — makes the boundary obvious to anyone moving content from `outline.md` into slides.

---

## Phase 3 — PMID verification

For every primary literature citation, **verify the PMID** before adding it to the reference list.

Quickest method: web search

> `[first author] [topic keywords] [year] pubmed`

The PubMed result page gives the canonical PMID and canonical citation format. PMID verification is non-negotiable.

---

## Phase 4 — Vancouver-style numbered reference list

Use Vancouver style (NLM citation format) throughout. Maintain a **single master numbered list at the top of the outline document**. The deck-end reference slides reproduce this list in numerical order for the audience.

### Format

```
1. Author1 LM, Author2 NO, Author3 PQ, et al. Title of article in sentence case. Journal Abbrev. Year;Volume(Issue):Pages.
```

For 6 or fewer authors: list all. For 7 or more: list the first 6 then `et al.`

For book chapters:

```
N. Author LM, Author NO. Chapter title. In: Editor LM, Editor NO, editors. Book Title. Edition. Publisher; Year. p. Pages.
```

### Numbering rules

- Number references in the order they first appear in the deck.
- Once a number is assigned, never renumber — append new ones at the end.
- Use the same numbers consistently across outline and deck.
- The deck-end reference slides display the master list in numerical order.

### On-slide reference rendering — structural conventions

The visual styling (font size, colour, separator weight) lives in `deck-build.md` Step 3. The structural conventions specific to references:

- **Position:** bottom of every content slide, above the footer.
- **Content:** full Vancouver citation for each cited reference, with the reference number leading.
- **Separator:** thin horizontal rule between body content and the reference block.
- **Layout:** one reference per line, stacked.
- **Maximum 4 references per slide.** If more is tempting, prefer 3 — slide density loses readability fast above 4.

Example bottom-of-slide reference block (rendered styling per `deck-build.md`):

```
1. AuthorA LM, AuthorB NO. Disease overview. In: Editor LM et al., editors. Standard Textbook. 21st ed. Publisher; 2024. p. 1015–25.
14. AuthorC LM, AuthorD EF, AuthorE GH, AuthorF IJ. Pivotal RCT on therapy X. N Engl J Med. 2023;390(8):e3007–18.
```

### Outline file rendering

Each slide section in the outline ends with a `Ref:` line listing reference numbers only:

```
**Ref:** 1, 5, 12, 14, 18
```

The full citations live only in the master list at the top of the outline.

---

## Phase 5 — Use exact wording from sources

For every claim written into the outline or deck:

1. Identify which reference(s) support the claim.
2. **Use the exact wording from the source — do not paraphrase.** Paraphrasing can introduce subtle distortions: shifted percentages, dropped qualifiers, changed clinical meaning. The defence at faculty Q&A is "this is what the paper says"; that defence only works when the wording is verbatim.
3. If the source's wording is too long for a slide, **trim with ellipsis** rather than rewording — the audience sees what the paper says, just abbreviated.
4. Tag the claim with the reference number in the outline.

Example workflow:

```
Source — Lee JH et al. Endocr J 2022;69(8):987–95:
"23.4% had SIADH as the primary cause."
"82.1% achieved sodium normalisation by 72 hours on fluid restriction."

Outline (verbatim from source):
- "23.4% had SIADH as the primary cause" (Lee 2022)
- "82.1% achieved sodium normalisation by 72 hours on fluid restriction" (Lee 2022)
Ref: 14

Slide rendering (same wording — fits at body-bullet size):
- 23.4% had SIADH as the primary cause
- 82.1% achieved sodium normalisation by 72 hours on fluid restriction
References at slide bottom: 14
```

If a source quote is too long to fit at body-text size, **split it across two bullets**, **trim with ellipsis**, or **promote it to its own slide** — but do not rewrite it. Always keep the exact phrasing.

---

## Phase 6 — Final reference reconciliation

Before declaring the deck finalised:

1. **Walk through every slide** and check that the `Ref:` line matches the actual content.
2. **Walk through the master list** and confirm every reference number is used at least once.
3. **Walk through the master list** and confirm no reference appears that isn't cited anywhere.
4. Resolve any "Ref [N] not found" errors in the build script.
5. **Cross-check the sources summary table (build aid)** against the master list — every cited reference should appear in the table; every table row should appear in the master list.

---

## Common citation errors to watch for

| Error | How to catch |
|---|---|
| Citing the 2020 ATS/IDSA pulmonary NTM guideline for extrapulmonary regimens | Check that the cited guideline actually addresses the body site you're discussing. The 2020 update is **pulmonary only** — extrapulmonary regimens are in the 2007 statement. |
| Citing the ACR 2021 RA guideline for MSK NTM | The guideline addresses NTM **lung disease** only — extrapolation needs a different citation. |
| Citing a textbook chapter without checking the latest edition's numbering | Re-verify chapter numbers against the actual edition's table of contents — chapter numbering changes between editions. |
| Citing a textbook from an older edition than what's currently in print | Confirm the edition the user owns / the audience expects. Citing Harrison's 19e when 21e is current can be a faculty red flag — match the latest edition unless the user has a specific reason. |
| Citing a conference abstract as if it were a peer-reviewed paper | Note `[abstract]` in the citation when the source is a conference abstract (IDWeek poster, etc.); the audience should know the evidence weight. |
| Citing a guideline before checking which population it covers | A guideline written for one population (immunocompromised, paediatric, ICU-only) may not apply to your case — match the guideline's scope to the slide's scope. |

---

## Self-check before finalising references

- [ ] Every PMID has been verified against PubMed.
- [ ] Every textbook chapter number has been verified against the actual edition.
- [ ] Every guideline citation matches the actual scope of the guideline.
- [ ] On-slide reference styling per `deck-build.md` Step 3 — references are intentionally smaller than body text; the styling is theme-driven.
- [ ] Master list at the top of the outline is complete, ordered, contains no duplicates.
- [ ] Every slide's `Ref:` line lists numbers only, not full citations.
- [ ] Outline.md and the deck-end reference slides match exactly.
- [ ] Sources summary table at the bottom of `outline.md` (build aid) is up to date and reflects what's actually in `Sources/`.
