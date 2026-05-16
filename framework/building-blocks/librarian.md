---
name: librarian
description: "Use this skill to organise medical reference files — rename PDFs to a consistent convention, scan a library or project Sources/ folder for new or removed items, and maintain library-index.md (the index of textbooks, articles, and guidelines). Operates on two scopes: the long-term library root (a digital textbook collection), and per-project Sources/ folders (working sets for individual presentations). Triggers: 'rename my pdfs', 'clean up filenames', 'update library index', 'scan my library', 'list my textbooks', 'what's in my library', 'classify this pdf', '/librarian update', '/librarian rename', '/librarian list', '/librarian classify'. Also loaded by Read path from sources-fetch after a successful fetch — sources-fetch hands a freshly-acquired file to librarian for naming and index updates."
---

# Librarian — file naming, library index, and folder scans

## Why this matters

Source acquisition (`sources-fetch.md`) puts files into folders. Keeping those folders organised — consistent names, an up-to-date index, a clear picture of what's whole and what's partial — is a separate job. Without it, the library becomes a pile of `978-0-323-44942-7.pdf` and `EJM2014-G1-G47.pdf` files that nobody can search by topic, and the index drifts out of sync with what's actually on disk. This skill keeps the organisation honest.

This is the **organisation** layer. Acquisition lives in `sources-fetch.md`. Citation formatting lives in `references.md`. Image cropping lives in `images.md`. Librarian's scope is naming, indexing, and classifying.

---

## How this skill is triggered — same exception as sources-fetch

Like `sources-fetch`, this skill has direct triggers in its frontmatter despite the framework convention that building blocks are neutrally described. The reason is the same: users want to organise their library outside any presentation workflow ("I just dropped 5 new PDFs into D:\MEDICINE\TEXTBOOK, please clean them up"). The frontmatter triggers handle that case.

Two activation paths:

1. **Direct trigger** — user types a librarian phrase or `/librarian <subcommand>`. Skill auto-loads and runs the matching workflow.
2. **Loaded by Read path** — `sources-fetch.md` calls this skill after a successful Method A or Method B fetch to rename the acquired file and update the relevant index.

Future maintainers: do not "fix" the triggers back to neutral. The carve-out is intentional and documented here, paralleling `sources-fetch.md`.

---

## Subcommands

| Subcommand | Action |
|---|---|
| `/librarian update` | Walk the library root, compare against `library-index.md`, propose adds for new PDFs and removals for missing ones. Show diff; never write without confirmation. |
| `/librarian rename <folder>` | Walk the folder, identify PDFs with poor names, propose better names per the conventions below. Show before/after; rename only on confirmation. Defaults to the library root if no folder given. |
| `/librarian list` | Compact summary of what's currently in the library, grouped by specialty section. Useful when you're not sure if a book is already indexed. |
| `/librarian classify <file>` | Inspect one PDF — read metadata, scan first few pages — and propose its index entry (book, edition, layout, coverage). Useful for one-off additions. |
| `/librarian` (no args) | Show the subcommand list. |

When loaded by `sources-fetch.md` (not a direct trigger), the entry point is the **post-fetch handoff** flow described below — the skill receives a file path, target folder, and context (textbook chapter? journal article? guideline?), names the file, moves it, and updates the relevant index.

---

## Two scopes — same mechanics

| Scope | Folder | Index file | Purpose |
|---|---|---|---|
| **Library root** | e.g., `D:\MEDICINE\TEXTBOOK` (recorded in `CLAUDE.md` Section 7 / library configuration) | `library-index.md` at the library root | Long-term reference collection across all projects |
| **Project Sources/** | `{Project}/Sources/` for a specific presentation | `_acquisition_log.md` in the same folder (managed by `sources-fetch.md`) | Per-project working set |

Same naming conventions and same rename mechanics apply to both. The difference is only which index file gets updated. When invoked with `/librarian update` and no folder argument, the default scope is the library root. When invoked from `sources-fetch.md` after a project fetch, the scope is that project's `Sources/`.

---

## Naming conventions

These are the canonical conventions for this framework, also referenced by `sources-fetch.md`. Librarian enforces them on rename.

### Textbook chapter

```
{Book short name} {Edition} Ch{N} {Chapter title}.pdf
```

Examples:
```
Harrisons IM 21e Ch121 Hyponatremia.pdf
Brenner Rector 12e Ch16 Disorders of plasma sodium.pdf
Mandell ID 10e Ch268 Sporotrichosis.pdf
```

### Journal article

```
{First author} {Year} {Short title}.pdf
```

Examples:
```
Garrahy 2021 Hypertonic saline RCT.pdf
Adrogue Madias 2000 Hyponatremia review.pdf
Spasovski 2014 European hyponatremia guideline.pdf
```

If the article has only one author or two authors, optionally include both: `Adrogue Madias 2000`. For three or more, use first author only.

### Guideline document

```
{Society} {Year} {Topic}.pdf
```

Examples:
```
KDIGO 2024 Glomerular diseases.pdf
ATS IDSA 2020 NTM pulmonary disease.pdf
ACC AHA 2022 HF guidelines.pdf
```

### General rules

- Spaces are fine; no underscores unless the user prefers them.
- Avoid characters that break shell pipelines on Windows: `< > : " | ? *`.
- Don't include the institution name (e.g., "from John Hopkins library") — it's not part of the citation.
- Don't include "free" / "open access" / "PDF" in the name — these are noise.
- Keep titles short. The full citation lives in `library-index.md` or `_acquisition_log.md`; the filename just needs to be human-recognisable.

---

## library-index.md format (canonical spec)

Lives at the library root. Maintained by librarian — never edited blindly by another skill.

```markdown
# Medical Library Index

**Library root:** {absolute path}
**Last updated:** YYYY-MM-DD

---

## {Specialty section}

### {Book name} — {edition} ({year})
- **Editors:** {Editor1, Editor2, et al.}
- **Publisher:** {Publisher}
- **Layout:** single PDF with bookmarks | folder of per-chapter PDFs
- **Path:** {path relative to library root}
- **TOC source:** PDF bookmarks | filenames match chapter numbers | separate TOC at {path}
- **Coverage:** complete | partial — chapters: {N (title, fetched YYYY-MM-DD), N (title, fetched YYYY-MM-DD), ...}
- **Notes:** {free-form: page count, bookmark count, edition quirks, verification status}
```

### Field definitions

- **Editors / Publisher:** for citation construction without re-opening the PDF.
- **Layout:** determines extraction code path (single-PDF bookmark walk vs folder file copy).
- **Path:** relative to **Library root**. Use forward slashes or backslashes consistent with the host OS.
- **TOC source:** how to find a chapter inside the file.
- **Coverage:**
  - `complete` — whole textbook is present (every chapter reachable).
  - `partial — chapters: ...` — only specific chapters available. Each chapter listed with its number, short title, and fetch date. When `sources-fetch` does a library lookup, partial entries count as hits **only if the requested chapter is in the list**; otherwise the lookup falls through to browser fetch.
- **Notes:** free-form. Things worth recording: page count, bookmark count, "Vol 1+2 combined," verification of whether bookmark extraction works, edition-specific quirks.

### Sectioning

Group entries by specialty (`## Internal Medicine`, `## Nephrology`, `## Infectious Diseases`, etc.). Empty sections can stay as placeholders. Add new sections as the library grows.

### When Coverage is partial — recording chapters

After `sources-fetch` Method A successfully downloads an individual chapter and the user opts to add it to the library, librarian appends to the Coverage line:

```
Before: - **Coverage:** partial — chapters: 121 (Hyponatremia, fetched 2026-05-16)
After:  - **Coverage:** partial — chapters: 121 (Hyponatremia, fetched 2026-05-16), 363 (Sporotrichosis, fetched 2026-05-17)
```

If a partial entry accumulates many chapters and the user later acquires the whole textbook, librarian replaces `partial — chapters: ...` with `complete` and updates the Path to the whole-book file.

---

## Operation: `/librarian update`

Scope: library root by default; pass a folder path to override.

### Workflow

1. **Read** the current `library-index.md` (or note that none exists; offer to scaffold).
2. **Walk** the library root, listing every PDF and every folder of PDFs.
3. **Diff** what's on disk against what's in the index:
   - **In disk, not in index** → propose a new entry (use `/librarian classify` internals to draft the fields).
   - **In index, not on disk** → propose removal or flag as missing. Don't silently delete.
   - **Path mismatch** (file moved) → propose path update.
   - **Coverage drift** (partial entry's listed chapters no longer match what's on disk) → propose update.
4. **Show the diff** as a clear before/after summary. Group by add / remove / update.
5. **Ask the user to approve** before writing. Selective approval is fine ("apply 1, 3, 5 only").
6. **Update** `library-index.md`, including the `Last updated` date.

### Detecting layout

For each PDF or folder candidate:

- **Single PDF with bookmarks:** open with `pypdf`, check `reader.outline` is non-empty and tree-structured.
- **Folder of per-chapter PDFs:** folder containing multiple PDF files whose filenames look chapter-numbered (e.g., `Ch_001.pdf`, `Ch_002.pdf`, or `chapter01_*.pdf`).
- **Single PDF without bookmarks:** flag as `Layout: single PDF (no bookmarks — chapter extraction unreliable)` and note in **Notes** that the user should consider a different source or build a TOC manually.

### Detecting Coverage

- A single PDF with full bookmark tree spanning hundreds of pages → `complete`.
- A folder of per-chapter PDFs with continuous numbering → `complete`.
- A single PDF with only a few pages → likely a `partial` entry (one chapter or one article); don't treat as a textbook.
- Mixed folder (some chapters present, others missing) → `partial — chapters: {list of present ones}`.

When in doubt, propose `partial` and ask the user to confirm.

---

## Operation: `/librarian rename <folder>`

### Workflow

1. **Walk** the folder, listing every PDF.
2. **For each PDF**, decide if the current name follows the conventions above. If not:
   - **Read PDF metadata** with `pypdf` (`/Title`, `/Author`, `/Subject`, `/Keywords`).
   - **Extract first-page text** to find title, author, journal, year, DOI, PMID.
   - **Regex hunt** for: DOI (`10\.\d{4,9}/[-._;()/:A-Za-z0-9]+`), PMID (`PMID:?\s*(\d{6,9})`), year (`\b(19|20)\d{2}\b`).
   - **Classify** the file (textbook chapter / article / guideline) — see `/librarian classify` below.
   - **Construct** the proposed name from the conventions.
3. **Show before/after** as a table. Rename only on user confirmation.
4. **Never silently overwrite.** If the proposed name collides with an existing file, append ` (v2)` or ask.

### Code sketch

```python
from pypdf import PdfReader
import re
from pathlib import Path

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
PMID_RE = re.compile(r"PMID:?\s*(\d{6,9})")
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")

def inspect_pdf(path):
    """Return a dict of inferred fields for one PDF."""
    reader = PdfReader(str(path))
    info = {
        "title_meta": (reader.metadata.title or "").strip() if reader.metadata else "",
        "author_meta": (reader.metadata.author or "").strip() if reader.metadata else "",
        "page_count": len(reader.pages),
        "has_bookmarks": bool(reader.outline),
    }
    # First-page text — often has title/author/journal/DOI for articles
    if reader.pages:
        first = reader.pages[0].extract_text() or ""
        info["doi"] = next(iter(DOI_RE.findall(first)), None)
        info["pmid"] = next(iter(PMID_RE.findall(first)), None)
        info["year"] = next(iter(YEAR_RE.findall(first)), None)
        info["first_page_excerpt"] = first[:500]
    return info
```

The skill uses these inferences to propose a name; the user is the final arbiter.

---

## Operation: `/librarian list`

Read `library-index.md`, render a compact summary:

```
Internal Medicine
  - Harrison's IM 21e (2022) — complete, single PDF
  - Goldman-Cecil 26e (2020) — complete, folder of chapters

Infectious Diseases
  - Mandell ID 10e — complete, single PDF
  - IDSA 2020 NTM guideline — partial (1 chapter)

Nephrology
  (no entries)
```

Plain prose summary; not a table dump. Useful as a quick "do I already have X?" check.

---

## Operation: `/librarian classify <file>`

Inspect one file and propose its index entry. Used standalone or internally by `update` and `rename`.

Output:

```
File: D:\MEDICINE\TEXTBOOK\Mandell ID 10e.pdf
Inferred classification:
  Type: textbook (single PDF, 4500 pages, 712 bookmarks)
  Book: Mandell, Douglas, and Bennett's Principles and Practice of Infectious Diseases
  Edition: 10th
  Year: 2020
  Editors: Bennett JE, Dolin R, Blaser MJ
  Publisher: Elsevier
  Layout: single PDF with bookmarks
  Coverage: complete
  Specialty section: Infectious Diseases

Proposed library-index entry:

### Mandell, Douglas, and Bennett's Principles and Practice of Infectious Diseases — 10th edition (2020)
- **Editors:** Bennett JE, Dolin R, Blaser MJ
- **Publisher:** Elsevier
- **Layout:** single PDF with bookmarks
- **Path:** Mandell ID 10e.pdf
- **TOC source:** PDF bookmarks
- **Coverage:** complete
- **Notes:** 4500 pages, 712 bookmarks.

Apply? [yes / edit / skip]
```

The "edit" branch lets the user fix any field before write.

---

## Integration with sources-fetch

`sources-fetch.md` calls this skill at two points:

1. **After a successful download (Method A or B)** — librarian renames the file to the canonical convention before it's recorded in `_acquisition_log.md`. Sources-fetch passes the file path and known context (citation, source URL); librarian returns the canonical filename.
2. **After the "save to library too?" prompt resolves to yes** — librarian adds (or updates) the relevant `library-index.md` entry. For "just this chapter," it appends to a partial Coverage list. For "the whole textbook," it adds a new complete entry.

These are read-path calls; sources-fetch drives them. No direct trigger involved.

---

## Anti-patterns

| Anti-pattern | Why it fails | What to do instead |
|---|---|---|
| Silently renaming files | The user may have organised some files manually with intentional names | Always show before/after; rename only on confirmation |
| Silently editing `library-index.md` | The user reads this file too — unannounced changes break trust | Show diff; ask before writing |
| Deleting an index entry because the file is missing | The file might be moved, not gone — check first; flag as "missing" rather than removing | Propose removal as a candidate; require user confirmation |
| Treating PDF metadata `/Title` as authoritative | Publisher PDFs often have generic or wrong `/Title` ("untitled-1.pdf"); first-page text is more reliable | Use metadata as a hint, not ground truth; cross-check against first-page text |
| Filling in editor names from training knowledge | Hallucination risk for editions / years; cite from the PDF itself | Extract editors from the PDF's title page or copyright page; if unclear, ask the user |
| Auto-classifying ambiguous files | A "Mandell Ch268" PDF might be a partial chapter or a standalone article — wrong inference cascades into wrong index entries | When ambiguous, ask the user before proposing the entry |
| Renaming files inside a partial chapter folder to look like a complete textbook | Misrepresents what's actually on disk | Coverage stays `partial` until the whole book is present |

---

## Self-check before declaring a librarian operation done

- [ ] Every rename was approved by the user (no silent renames)
- [ ] No file was overwritten (collision → versioned name or skip)
- [ ] `library-index.md` `Last updated` date matches today
- [ ] Diff shown matches what was actually written
- [ ] Coverage field accurately reflects what's on disk for each entry
- [ ] No entry references a file that doesn't exist
- [ ] No on-disk PDF is missing from the index (or, if intentionally excluded, the user confirmed)
- [ ] Naming conventions applied consistently (textbook / article / guideline patterns from sources-fetch.md)

---

*Library and per-project organisation building block. Operates at two scopes: long-term library (D:\MEDICINE\TEXTBOOK or wherever the user's collection lives) and per-project Sources/ folders. Loaded by direct trigger or by Read path from sources-fetch.*
