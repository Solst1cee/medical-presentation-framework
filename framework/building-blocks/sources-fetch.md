---
name: sources-fetch
description: "Use this skill when the user wants to acquire a textbook chapter, journal article, or guideline PDF and place it into a `Sources/` folder. Two methods: browser-driven download (Chrome MCP on publisher sites — requires user has campus network or VPN access) and local-library extraction (read `library-index.md`, copy or extract a chapter from a digital textbook collection — read-only on the original). Triggers: 'find me [chapter/paper] from [textbook/journal]', 'get [chapter] from [Harrison/Goldman/Brenner/etc.]', 'download [chapter/paper/guideline]', 'fetch [chapter/paper]', 'extract [chapter] from [book]', 'pull [chapter/paper] for me', 'I need the chapter on [topic] from [textbook]', 'grab [paper/PMID] into Sources'. Also loaded by Read path from topic-review, journal-club, and case-discussion during their research phase — those workflows drive the call directly without needing a separate trigger."
---

# Source acquisition — automated chapters, articles, and guidelines

## Why this matters

`references.md` Phase 2 assumes the user has already dropped textbook PDFs and key papers into `Sources/`. In practice, that step is the slowest part of kickoff — the user has to find each chapter in their library, download each paper from a publisher site, and rename files. This building block automates the fetch when the user wants it: pick a method (online or local-library), confirm the source list, and let Claude populate `Sources/` with correctly named files and a parallel acquisition log that flows into `references.md`.

This is the **fetch step** only. License handling, citation formatting, and master-list maintenance still live in `references.md`. Image-specific sourcing still lives in `images.md` (figures inside Sources/Figures/). This skill puts whole textbook chapters and full-text articles into the project's working set.

---

## How this skill is triggered — a deliberate exception

The framework convention is that building blocks have *neutral* descriptions so they don't compete with presentation-type auto-triggers. **This skill is the one carve-out.** The frontmatter description includes direct triggers ("find me [chapter] from [textbook]", "download [paper]", "fetch [PMID]", etc.) because users frequently want to fetch a chapter or paper *outside* a presentation workflow — for personal study, ad-hoc reference, or to seed a project's `Sources/` before the kickoff conversation.

Two activation paths:

1. **Direct trigger** — user types a fetch phrase. The skill auto-loads and runs the workflow standalone, asking which method (browser or local library) and where to put the output. If no project context exists, the default destination is the user's working directory.
2. **Loaded by Read path** — a presentation-type skill (topic-review, journal-club, case-discussion) calls this skill during its research phase. The presentation-type workflow drives the call; this skill's triggers are not consulted.

Future maintainers: do not "fix" the triggers back to neutral. The carve-out is intentional and documented here.

---

## Workflow — library first, then browser

The skill always tries the local library before reaching for the browser. Library extraction is fast, free, and works offline; browser download requires the user to have live VPN / campus access. The fall-through logic per source:

```
For each requested source:
  1. Read library-index.md → look for the book / paper.
     ├─ Found     → Method B (extract or copy from local library) → done.
     └─ Not found → continue to step 2.
  2. Ask the user once for the whole missing-items batch:
     "Source(s) not in your library. Do you have campus / VPN access right now?"
     ├─ Yes → Method A (browser via Chrome MCP) for the missing items.
     └─ No  → log the missing items in the report; user fetches manually later.
  3. Append a row to Sources/_acquisition_log.md for every successfully fetched file.
```

Two methods, one sequence. Don't ask the user up front which method to use — let the library answer, fall through to browser only on a miss.

| Method | When it runs | Inputs needed | Output |
|---|---|---|---|
| **B. Local library extraction** (tried first) | A `library-index.md` is present at the configured library root | Book + chapter request, or paper title | PDF in `{Project}/Sources/`, original library file untouched |
| **A. Browser download** (fallback) | Library miss + user confirms live VPN / campus access | Platform, citation/PMID/DOI, live publisher access | PDF (or saved-as-PDF) in `{Project}/Sources/` |

---

## Pre-flight — confirm the source list once

Before starting the fetch loop, restate the source list and ask for sign-off. The list is usually drawn from the kickoff conversation — Phase 1 of the presentation-type workflow has already named the textbook + chapter, the guideline, the landmark papers. You can mark each entry with the *expected* method (textbooks → likely library; recent papers/guidelines → likely browser), but the workflow above will fall through automatically if the library doesn't have something:

> *"I'll fetch the following into `Sources/`. Confirm or edit before I start:*
> *1. Harrison's IM 21e Ch. 121 (Hyponatremia) — try local library first*
> *2. Brenner & Rector 12e Ch. 16 — try local library first*
> *3. Spasovski 2014 European hyponatremia guideline (PMID 24569125) — browser (likely not in library)*
> *4. Garrahy 2021 hypertonic saline RCT (PMID 33954787) — browser (likely not in library)"*

Confirm list → run the per-source flow above → report at the end with a summary table noting which method each source was actually fetched by.

---

## Method A — Browser download (online access)

### Pre-flight access check

This check runs **only after the library has been tried** and at least one source is still missing. Ask the user once for the whole fall-through batch:

> *"I couldn't find these in your library: [list of missing items]. Do you have campus network or VPN access right now? I'll attempt the downloads via the Chrome extension; if a login wall appears, I'll stop and report."*

Claude cannot independently verify VPN state — the only reliable check is to attempt navigation and observe what loads. If the first download hits a paywall or login wall, stop the loop and report to the user; don't keep retrying every other source. If the user says no, skip Method A entirely and log the missing items as user-to-fetch — they can re-run the skill later when access is available.

### Tooling

Use the Chrome MCP (`mcp__Claude_in_Chrome__*`). Native browser automation is required because most publisher chapter-PDF buttons are SPA-rendered and not accessible via plain HTTP fetch. Bash `curl` / `wget` will not work for authenticated publisher sites.

The `web_fetch` tool may work for fully open-access targets (PMC article landing pages, EQUATOR-network reporting checklists). Try `web_fetch` first for those — if it returns the article HTML, the PDF link is usually one click away and a direct PDF URL can be captured for `download` rather than going through Chrome.

### Workflow per source

1. **Identify the platform** from the source type (table below).
2. **Navigate** to the search box of the right platform via Chrome MCP; search by title or DOI.
3. **Open the article / chapter page** and locate the PDF download control.
4. **Trigger the download** to the user's default download folder.
5. **Move the file** into `{Project}/Sources/` and rename per the filename convention.
6. **Append a row** to `Sources/_acquisition_log.md` (citation, source URL, access date).
7. **Report back** at the end of the loop with one line per fetched source.

### Platform crib sheet

| Platform | Chapter / article format | Where the download control sits | Notes |
|---|---|---|---|
| **PMC (PubMed Central)** | PDF (free, open access) | "PDF" button on the article landing page; or direct URL `…/pdf/{pmcid}.pdf` | Always free; `web_fetch` may work for the landing page. |
| **PubMed** | Abstract only — follow the "Free PMC article" or publisher link out | Right sidebar | Use as a discovery layer, not a download target. |
| **Journal publisher sites** (NEJM, JAMA, Lancet, Elsevier journals) | PDF | "Download PDF" / "PDF" button on article page | Requires institutional access; check VPN. |
| **ClinicalKey** | PDF, per chapter | Chapter page → right sidebar → "PDF" or "Save as PDF" | Login required; PDF preserves figures + page numbers. |
| **AccessMedicine** (McGraw-Hill) | HTML chapter; PDF for some content | Top toolbar → "Print" → save as PDF; some chapters have a direct PDF link | Many chapters are HTML-only — saved-as-PDF preserves text but not always figures cleanly. |
| **UpToDate** | HTML topic article (not chapters) | "Print" → save as PDF | Articles are reviews, not textbook chapters; useful for guideline-style summaries. |
| **EQUATOR Network** | PDF reporting checklists (CONSORT, PRISMA, STARD, STROBE, etc.) | Direct PDF link on each guideline page | Open access; `web_fetch` works. |

### Filename convention

Consistent names downstream make `references.md` Phase 2 reconciliation cleaner.

- **Textbook chapter:** `{Book short name} {Edition} Ch{N} {Chapter title}.pdf`
  - `Harrisons IM 21e Ch121 Hyponatremia.pdf`
  - `Brenner Rector 12e Ch16 Disorders of plasma sodium.pdf`
- **Journal article:** `{First author} {Year} {Short title}.pdf`
  - `Garrahy 2021 Hypertonic saline RCT.pdf`
  - `Spasovski 2014 European hyponatremia guideline.pdf`
- **Guideline document:** `{Society} {Year} {Topic}.pdf`
  - `KDIGO 2024 Glomerular diseases.pdf`

Avoid spaces in filenames if the project uses scripts that shell-pipe paths; otherwise spaces are fine.

### When access fails

| Failure | Recovery |
|---|---|
| Login wall appears | Stop the loop. Report the platform and the source. Ask the user to verify VPN / login status and resume. |
| Paywall (no institutional access) | Report to user. Suggest alternatives: PMC version, preprint server (medRxiv, bioRxiv), interlibrary loan. Do not bypass paywalls. |
| Geo-restriction | Report. Cannot proceed without VPN to an authorised region. |
| Anti-bot challenge (CAPTCHA) | Report. User has to complete the CAPTCHA and re-attempt. |
| File downloads but is corrupt / 0-byte | Re-attempt once, then report. |

Don't retry a failed source more than once silently — failures usually indicate an access problem the user has to resolve.

---

## Method B — Local library extraction (offline)

### Pre-flight: locate `library-index.md`

The skill expects a maintained index file at the user's library root. Two cases:

- **Index exists** — read it and proceed.
- **Index doesn't exist** — offer to scaffold one (one-time setup, see below).

The library root path is recorded in the project's `CLAUDE.md` under a small `## Library configuration` section the first time the skill is used:

```markdown
## Library configuration (sources-fetch Method B)
- **Library root:** `C:\Users\{user}\Documents\Medical Library`
- **Index file:** `library-index.md` at the library root
```

If the path isn't recorded yet, ask the user once and append it to `CLAUDE.md`. Subsequent sessions read it from there.

### `library-index.md` format

Maintained by the user (with Claude's help on first scaffold). Lives at the library root. Format:

````markdown
# Medical Library Index

**Library root:** C:\Users\{user}\Documents\Medical Library
**Last updated:** 2026-05-15

---

## Internal Medicine

### Harrison's Principles of Internal Medicine — 21st edition (2022)
- **Editors:** Loscalzo J, Fauci A, Kasper D, Hauser S, Longo D, Jameson JL.
- **Publisher:** McGraw-Hill
- **Layout:** single PDF with bookmarks
- **Path:** `Internal Medicine/Harrisons IM 21e/Harrisons-IM-21e.pdf`
- **TOC source:** PDF bookmarks (chapter-level)
- **Notes:** ~5000 pages; chapter extraction by bookmark page range.

### Goldman-Cecil Medicine — 26th edition (2020)
- **Editors:** Goldman L, Schafer AI.
- **Publisher:** Elsevier
- **Layout:** folder of per-chapter PDFs
- **Path:** `Internal Medicine/Goldman-Cecil 26e/`
- **TOC source:** filenames match chapter numbers (e.g., `Ch_121_Hyponatremia.pdf`).

---

## Nephrology

### Brenner & Rector's The Kidney — 12th edition (2024)
- **Editors:** Yu ASL, Chertow GM, Luyckx VA, Marsden PA, Skorecki K, Taal MW.
- **Publisher:** Elsevier
- **Layout:** single PDF with bookmarks
- **Path:** `Nephrology/Brenner-Rector 12e/Brenner-Rector-12e.pdf`
- **TOC source:** PDF bookmarks.
````

### Field definitions

- **Editors / Publisher:** for citation construction without re-opening the PDF.
- **Layout:** `single PDF with bookmarks` or `folder of per-chapter PDFs`. Determines extraction code path.
- **Path:** relative to **Library root**.
- **TOC source:** how Claude finds the chapter — `PDF bookmarks`, `filenames match chapter numbers`, or `separate TOC at {path}`.

### Workflow per source

1. **Read** `library-index.md`.
2. **Match** the request (book + edition + chapter) to an index entry. Fuzzy match on book name + edition acceptable; **confirm with the user before extraction** if multiple candidates or unclear match.
3. **Branch on layout:**
   - **Folder of per-chapter PDFs** → find the matching file by chapter number or title; `shutil.copy` to `{Project}/Sources/`.
   - **Single PDF with bookmarks** → use `pypdf` to walk the bookmark tree, find the target chapter's bookmark, compute its page range (start = bookmark page; end = next sibling bookmark's page − 1, or last page of book), extract pages, write a new PDF to `{Project}/Sources/`.
4. **Never modify the source PDF.** Open in read-only mode. Write only to `Sources/`.
5. **Append a row** to `Sources/_acquisition_log.md`.

### Bookmark-driven extraction (single-PDF case)

```python
from pypdf import PdfReader, PdfWriter
from pathlib import Path

def extract_chapter_by_bookmark(library_pdf, chapter_query, out_path):
    """Extract a chapter by fuzzy bookmark match. Read-only on library_pdf."""
    reader = PdfReader(str(library_pdf))

    # Flatten bookmark tree to (title, page_index) pairs
    def walk(outline, acc):
        for item in outline:
            if isinstance(item, list):
                walk(item, acc)
            else:
                acc.append((item.title, reader.get_destination_page_number(item)))
        return acc
    bookmarks = walk(reader.outline, [])

    # Fuzzy match on chapter_query
    matches = [(t, p) for t, p in bookmarks if chapter_query.lower() in t.lower()]
    if not matches:
        raise ValueError(f"No bookmark matched '{chapter_query}'. Candidates: {[t for t,_ in bookmarks[:20]]}")
    if len(matches) > 1:
        raise ValueError(f"Ambiguous match for '{chapter_query}': {[t for t,_ in matches]} — confirm with user")

    title, start = matches[0]
    # End page = next bookmark's start - 1, or last page if final chapter
    pages_after = [p for _, p in bookmarks if p > start]
    end = (min(pages_after) - 1) if pages_after else len(reader.pages) - 1

    writer = PdfWriter()
    for i in range(start, end + 1):
        writer.add_page(reader.pages[i])
    with open(out_path, "wb") as f:
        writer.write(f)
    return title, start, end
```

### When the index is missing or stale

- **Index doesn't exist** — offer to create one. Walk the library root, list every PDF/folder, propose entries grouped by parent folder. The user reviews and edits before saving as `library-index.md`. One-time setup; subsequent fetches just read.
- **Book in user's request not in the index** — ask the user, then add an entry.
- **Chapter not found by bookmark match** — list the bookmarks that ARE in the book (top 20) so the user can pick or correct the title.
- **Layout mismatch** (index says single-PDF, but file is actually a folder, or vice versa) — stop and ask; don't guess.

---

## Common to both methods

### Destination

All fetched files land in `{Project}/Sources/`. Originals are never modified — Method A writes only to the project's `Sources/`; Method B opens library files read-only.

### Acquisition log — hand-off to `references.md`

During the fetch loop, maintain `Sources/_acquisition_log.md`:

```markdown
# Sources acquisition log

| File | Citation (Vancouver-ready) | Method / source | Date |
|---|---|---|---|
| Harrisons IM 21e Ch121 Hyponatremia.pdf | Mount DB. Hyponatremia. In: Loscalzo J et al., editors. Harrison's PIM. 21st ed. McGraw-Hill; 2022. Ch. 121. | Local library extraction (`Harrisons-IM-21e.pdf`, p. 1015–1025) | 2026-05-15 |
| Spasovski 2014 European hyponatremia guideline.pdf | Spasovski G, et al. Clinical practice guideline on diagnosis and treatment of hyponatraemia. Eur J Endocrinol. 2014;170(3):G1–47. (PMID 24569125) | Browser download (PMC) | 2026-05-15 |
| Garrahy 2021 Hypertonic saline RCT.pdf | Garrahy A, et al. Continuous versus bolus infusion of hypertonic saline in symptomatic hyponatremia. J Clin Endocrinol Metab. 2021;106(8):e3007–18. (PMID 33954787) | Browser download (journal site, via VPN) | 2026-05-15 |
```

This is a build aid — `references.md` Phase 2 reads it to:

- Populate the master Vancouver reference list at the top of `{Topic} outline.md`.
- Populate the sources summary table at the bottom of the outline (under `## Build aids — not for slides`), using the citations and method strings here.

The log file does not propagate into the deck. Once the master list and the sources summary table are populated, the log can be deleted or kept for audit.

### License sanity check (pass-through, not the primary check)

This skill does not replace `references.md` and `images.md` license discipline. But at fetch time, two quick checks are worth doing:

- **Method A from PMC:** confirm the article page shows a CC license (CC-BY, CC-BY-NC); flag if the journal is "free to read" but not openly licensed.
- **Method A from publisher sites behind a paywall:** the user's institutional access permits read-and-cite for educational use; do not redistribute the PDF outside the user's project.
- **Method B (textbooks the user owns):** local extraction for personal study and educational presentation is the user's call. The acquisition log records the source PDF for audit.

If a paper turns out to be unsuitable for the planned use (e.g., CC-BY-ND chapter that the user wants to crop figures from), surface it during `images.md` figure planning, not at fetch time.

---

## Anti-patterns

| Anti-pattern | Why it fails | What to do instead |
|---|---|---|
| Mass-fetching without confirming the source list | User ends up with files they didn't want; wastes VPN session | Confirm the list once at top of the loop; fetch in sequence |
| Modifying the original library PDF | Destroys the user's reference copy | Open library files read-only; write only to project `Sources/` |
| Silently overwriting an existing `Sources/{file}.pdf` | Loses prior version (may have been hand-annotated) | If file exists, ask before overwriting; offer `{file} (v2).pdf` |
| Cropping pages out of an extracted chapter | Loses figures and tables the user may need later | Extract the *whole* chapter (bookmark start to next-bookmark-end-1) |
| Retrying a paywalled source repeatedly | Wastes time; doesn