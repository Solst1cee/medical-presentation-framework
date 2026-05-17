---
name: sources-fetch
description: "Use this skill when the user wants to acquire a textbook chapter, journal article, or guideline PDF and place it into a `Sources/` folder. A four-rung fetch ladder, tried in order per source: Method A local-library extraction (read `library-index.md`, copy or extract a chapter, read-only on the original), Method B free open-access API resolver (PMID/DOI/title → legal OA PDF via PMC/Unpaywall/Europe PMC, no browser, no VPN), Method C browser via Chrome MCP without VPN (free/open targets that still need a real browser), Method D browser via Chrome MCP with optional demand-driven VPN auto-connect (entitled publisher content). Triggers: 'find me [chapter/paper] from [textbook/journal]', 'get [chapter] from [Harrison/Goldman/Brenner/etc.]', 'download [chapter/paper/guideline]', 'fetch [chapter/paper]', 'extract [chapter] from [book]', 'pull [chapter/paper] for me', 'I need the chapter on [topic] from [textbook]', 'grab [paper/PMID] into Sources'. Also loaded by Read path from topic-review, journal-club, and case-discussion during their research phase — those workflows drive the call directly without needing a separate trigger."
---

# Source acquisition — automated chapters, articles, and guidelines

## Why this matters

`references.md` Phase 2 assumes the user has already dropped textbook PDFs and key papers into `Sources/`. In practice, that step is the slowest part of kickoff — the user has to find each chapter in their library, download each paper from a publisher site, and rename files. This building block automates the fetch when the user wants it: confirm the source list, then let Claude walk a four-rung ladder per source (cheapest/safest rung first) and populate `Sources/` with correctly named files and a parallel acquisition log that flows into `references.md`.

This is the **fetch step** only. License handling, citation formatting, and master-list maintenance still live in `references.md`. Image-specific sourcing still lives in `images.md` (figures inside Sources/Figures/). This skill puts whole textbook chapters and full-text articles into the project's working set.

---

## How this skill is triggered — a deliberate exception

The framework convention is that building blocks have *neutral* descriptions so they don't compete with presentation-type auto-triggers. **This skill is the one carve-out.** The frontmatter description includes direct triggers ("find me [chapter] from [textbook]", "download [paper]", "fetch [PMID]", etc.) because users frequently want to fetch a chapter or paper *outside* a presentation workflow — for personal study, ad-hoc reference, or to seed a project's `Sources/` before the kickoff conversation.

Two activation paths:

1. **Direct trigger** — user types a fetch phrase. The skill auto-loads and runs the ladder standalone, asking only *where* to put the output (it does **not** ask which method up front — the ladder falls through automatically). If no project context exists, the default destination is the user's working directory.
2. **Loaded by Read path** — a presentation-type skill (topic-review, journal-club, case-discussion) calls this skill during its research phase. The presentation-type workflow drives the call; this skill's triggers are not consulted.

Future maintainers: do not "fix" the triggers back to neutral. The carve-out is intentional and documented here.

---

## Workflow — the four-rung ladder

For **each** requested source, try the rungs in order. Stop at the first rung that succeeds. Drop to the next rung only on a miss or an access wall. The VPN is touched **only at Method D**, and only if the user has opted in.

```
For each requested source:
  A. Local library  — read library-index.md; book/chapter found → extract or
                       copy (offline, original read-only) → DONE
       └─ miss → B
  B. Free API        — paper/guideline with a DOI / PMID / title (NOT a textbook
                       chapter): resolve_oa.py → a legal open-access PDF
                       (Europe PMC / PMC / Unpaywall) → download → DONE
       └─ no legal free copy, or it is a textbook chapter → C
  C. Browser, no VPN — open/free target that needs a real browser (PMC SPA
                       landing page, EQUATOR checklist, open-access publisher
                       page); loads with no auth wall → download → DONE
       └─ hits a paywall / login / SSO wall → D
  D. Browser + VPN   — entitled content (subscription journals, ClinicalKey,
                       AccessMedicine, UpToDate). If VPN auto-connect is opted
                       in: bring the tunnel up, run the Method C workflow,
                       release the tunnel. Wall persists → log as user-to-fetch.
  E. Append a row to Sources/_acquisition_log.md for every fetched file.
```

Don't ask the user up front which method to use — let each rung answer and fall through on a miss.

Per source-type applicability:

- **Papers / guidelines (have a DOI / PMID / title):** A → B → C → D.
- **Textbook chapters (no API; the online platforms are login-walled):** A → D (B and C are skipped).
- **Open-access figures:** out of scope — handled by `images.md`.

| Method | When it runs | Inputs needed | Output |
|---|---|---|---|
| **A. Local library extraction** (tried first) | A `library-index.md` is present at the configured library root | Book + chapter request, or paper title | PDF in `{Project}/Sources/`, original library file untouched |
| **B. Free API resolver** | Library miss + the item is a paper/guideline with a DOI/PMID/title | DOI / PMID / title, contact email | PDF in `{Project}/Sources/`, no browser, no VPN |
| **C. Browser, no VPN** | API miss (or a non-paper) + target is free/open but needs a browser | Platform, citation/PMID/DOI | PDF (or saved-as-PDF) in `{Project}/Sources/` |
| **D. Browser + VPN** | Method C hit a paywall/login/SSO wall on entitled content | Platform, citation, institutional access (auto or manual) | PDF (or saved-as-PDF) in `{Project}/Sources/` |

---

## Pre-flight — confirm the source list once

Before starting the fetch loop, restate the source list and ask for sign-off. The list is usually drawn from the kickoff conversation — Phase 1 of the presentation-type workflow has already named the textbook + chapter, the guideline, the landmark papers. You can mark each entry with the *expected* entry rung (textbooks → likely Method A library; papers/guidelines → likely Method B API, else C/D), but the ladder will fall through automatically regardless:

> *"I'll fetch the following into `Sources/`. Confirm or edit before I start:*
> *1. Harrison's IM 21e Ch. 121 (Hyponatremia) — try local library first*
> *2. Brenner & Rector 12e Ch. 16 — try local library first*
> *3. Spasovski 2014 European hyponatremia guideline (PMID 24569125) — try open-access API, then browser*
> *4. Garrahy 2021 hypertonic saline RCT (PMID 33954787) — try open-access API, then browser"*

Confirm list → run the per-source ladder above → report at the end with a summary table noting which rung each source was actually fetched by.

---

## Method A — Local library extraction (offline, tried first)

### Pre-flight: locate `library-index.md`

The skill expects a maintained index file at the user's library root. Two cases:

- **Index exists** — read it and proceed.
- **Index doesn't exist** — offer to scaffold one (one-time setup, see below).

The library root path is recorded in the project's `CLAUDE.md` under the `## 7. Library configuration` section the first time the skill is used:

```markdown
## 7. Library configuration (sources-fetch Method A)
- **Library root:** `C:\Users\{user}\Documents\Medical Library`
- **Index file:** `library-index.md` at the library root
```

If the path isn't recorded yet, ask the user once and append it to `CLAUDE.md`. Subsequent sessions read it from there.

### `library-index.md` format

The canonical format spec — including the **`Coverage`** field that distinguishes complete textbooks from partial chapter collections — lives in **`librarian.md`**. Method A reads the index for lookups; any *update* to the index goes through `librarian` so the spec stays single-source.

For a Method A lookup, the fields you need are: `Layout`, `Path`, `TOC source`, and `Coverage`. See `librarian.md` for the full schema, field definitions, and worked examples.

### Workflow per source

1. **Read** `library-index.md`.
2. **Match** the request (book + edition + chapter) to an index entry. Fuzzy match on book name + edition acceptable; **confirm with the user before extraction** if multiple candidates or unclear match. Also check the entry's **`Coverage`** field — if it is `partial — chapters: ...` and the requested chapter is **not** in that list, treat this as a library miss and fall through to the next applicable rung (**Method B** for papers/guidelines; **Method D** for textbook chapters).
3. **Branch on layout:**
   - **Folder of per-chapter PDFs** → find the matching file by chapter number or title; `shutil.copy` to `{Project}/Sources/`.
   - **Single PDF with bookmarks** → use `pypdf` to walk the bookmark tree, find the target chapter's bookmark, compute its page range (start = bookmark page; end = next sibling bookmark's page − 1, or last page of book), extract pages, write a new PDF to `{Project}/Sources/`.
4. **Never modify the source PDF.** Open in read-only mode. Write only to `Sources/`.
5. **Hand the extracted file to `librarian.md`** to apply the canonical filename (textbook chapter pattern), then append a row to `Sources/_acquisition_log.md` using the canonical filename, source noted as `"Local library extraction from {book}, p. {start}–{end}"`, and date.

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

## Method B — Free open-access API resolver (no browser, no VPN)

Runs after a Method A miss, **only for papers/guidelines that have a DOI, PMID, or title**. Textbook chapters skip this rung (no API exposes textbook chapters). Pure HTTP/JSON, so it is fast and robust where Chrome MCP is brittle, and it never needs campus access or a VPN.

### Pre-flight: contact email

The resolver uses NCBI E-utilities + Europe PMC (PMID-keyed, no key needed) and Unpaywall (DOI-keyed, requires a contact `email`). The email is recorded in `CLAUDE.md` under `## 9. API resolver configuration`:

```markdown
## 9. API resolver configuration (sources-fetch Method B)
- **Contact email:** `you@example.org`   (NCBI politeness + Unpaywall required param)
- **NCBI API key:** set via the `NCBI_API_KEY` environment variable only — never in the repo
```

If no email is configured, the resolver still runs (Europe PMC / PMC PMID path works) but **Unpaywall is skipped** — the DOI-only open-access copies it would have found are missed, and those sources simply fall through to Method C/D. Ask the user once for an email and append it to `CLAUDE.md §9`; a role or throwaway address is fine.

### Legality guardrail

`resolve_oa.py` emits **only** PDF URLs the open-access services themselves report as openly licensed or author/repository-deposited (Europe PMC `isOpenAccess`, NCBI PMC OA subset, Unpaywall `best_oa_location`). It never emits a paywalled publisher URL. Do not second-guess a `resolved:false` into reaching for a paywalled link — that is exactly what Method D's institutional access is for. No paywall bypass, ever.

### Workflow per source

1. **Invoke the resolver** with whatever identifier you have:

   ```
   python framework/building-blocks/resolve_oa.py --pmid 33954787 --email you@example.org
   python framework/building-blocks/resolve_oa.py --doi 10.1210/clinem/dgab321 --email you@example.org
   python framework/building-blocks/resolve_oa.py --title "Continuous versus bolus hypertonic saline" --email you@example.org
   ```

2. **Parse the single-line JSON on stdout and branch on the exit code:**
   - **exit 0** (`"resolved": true`) → a legal OA PDF was found. Download `pdf_url` — try `web_fetch` first; if it does not yield the PDF bytes, `curl -L` the URL. Save into `{Project}/Sources/`. Verify: present, non-zero bytes, opens cleanly. If verification fails, do **not** append to the acquisition log — fall through to Method C.
   - **exit 1** (`"resolved": false`) → no legal free copy. Fall through to **Method C**. This is not an error; it is the expected signal.
3. **Hand the file to `librarian.md`** for the canonical filename (journal-article / guideline pattern).
4. **Append a row** to `Sources/_acquisition_log.md` using the canonical filename, method string `"API (<source>, open access)"` (e.g. `API (EuropePMC, open access)`), the `pdf_url`, the `license` from the resolver output when present, and the date.

---

## Method C — Browser via Chrome MCP, no VPN (free/open targets)

Runs after a Method B miss, or for non-paper items a library miss sends straight here. Method C is the **attempt the browser download *without* a VPN** rung — for content that is free/open but rendered such that an API/`web_fetch` cannot grab the PDF directly (SPA-rendered PMC pages, EQUATOR checklist pages, open-access publisher article pages).

If a target loads behind a **paywall / login / SSO wall** with no VPN, that is the signal to escalate to **Method D** — do not keep retrying it here.

### Tooling

Use the Chrome MCP (`mcp__Claude_in_Chrome__*`). Native browser automation is required because most publisher chapter-PDF buttons are SPA-rendered and not accessible via plain HTTP fetch. Bash `curl` / `wget` will not work for authenticated publisher sites.

The `web_fetch` tool may work for fully open-access targets (PMC article landing pages, EQUATOR-network reporting checklists). Try `web_fetch` first for those — if it returns the article HTML, the PDF link is usually one click away and a direct PDF URL can be captured for `download` rather than going through Chrome. (For papers, Method B should already have caught most of these — Method C is the fallback when the resolver missed but the content is still free.)

### Workflow per source (shared with Method D)

1. **Identify the platform** from the source type (table below).
2. **Navigate** to the search box of the right platform via Chrome MCP; search by title or DOI.
3. **Open the article / chapter page** and locate the PDF download control.
4. **Trigger the download.** The browser saves to the user's default Downloads folder, not to `{Project}/Sources/`. That's expected — the move happens in the next step.
5. **Move from Downloads to `{Project}/Sources/` — non-skippable.** The browser does not save directly to the project folder; without this move the file lives in the wrong place and `_acquisition_log.md` will reference a path that does not exist. After the move, verify: file present in `Sources/`, non-zero bytes, opens cleanly. If verification fails, do not append to the acquisition log — re-attempt the move or report a failure.
6. **Hand the file to `librarian.md`** for naming. Pass the citation / title / author context; `librarian` renames per the canonical convention (textbook chapter / article / guideline patterns) and returns the canonical filename. Don't invent ad-hoc names — `librarian` owns this convention so all framework files agree on it.
7. **Append a row** to `Sources/_acquisition_log.md` using the canonical filename returned by `librarian` (citation, source URL, access date), method string `"Browser download, no VPN (<platform>)"` for Method C or `"Browser download, via VPN (<platform>)"` for Method D.
8. **Ask "save to library too?"** for textbook-chapter fetches via the browser. Once the project copy is safe in `Sources/`, prompt the user:

   > *"You just downloaded {Book Ch N — Title} from {publisher}. Want to add it to your local library so a future fetch can use it offline?*
   > *(a) Just this chapter — `librarian` will save a copy to the library root and append a `partial` chapter entry to `library-index.md`*
   > *(b) The whole textbook PDF — if you have it on hand or can grab it now, `librarian` will add a `complete` entry*
   > *(c) Nothing — the project `Sources/` copy is enough"*

   On (a) or (b), call `librarian.md` to handle the file copy and index update. On (c), continue. Skip this prompt for one-off papers and guidelines that aren't part of a textbook — they rarely belong in the long-term library.
9. **Report back** at the end of the loop with one line per fetched source: filename, source URL, rung used, library-status (added / not added).

### Platform crib sheet

| Platform | Format | Where the download control sits | Rung |
|---|---|---|---|
| **PMC (PubMed Central)** | PDF (free, open access) | "PDF" button on the article landing page; or direct URL `…/pdf/{pmcid}.pdf` | Usually **Method B**; **Method C** if the SPA page blocks the resolver. Always free — no VPN. |
| **PubMed** | Abstract only — follow the "Free PMC article" or publisher link out | Right sidebar | Discovery layer feeding **Method B**, not a download target. |
| **EQUATOR Network** | PDF reporting checklists (CONSORT, PRISMA, STARD, STROBE, etc.) | Direct PDF link on each guideline page | **Method C** — open access; `web_fetch` works. No VPN. |
| **Open-access publisher article pages** | PDF | "Download PDF" on the article page | **Method C** — no auth wall. No VPN. |
| **Journal publisher sites** (NEJM, JAMA, Lancet, Elsevier journals) | PDF | "Download PDF" / "PDF" button on article page | **Method D** — requires institutional access. |
| **ClinicalKey** | PDF, per chapter | Chapter page → right sidebar → "PDF" or "Save as PDF" | **Method D** — login required; PDF preserves figures + page numbers. |
| **AccessMedicine** (McGraw-Hill) | HTML chapter; PDF for some content | Top toolbar → "Print" → save as PDF; some chapters have a direct PDF link | **Method D** — login required; many chapters HTML-only, saved-as-PDF preserves text but not always figures cleanly. |
| **UpToDate** | HTML topic article (not chapters) | "Print" → save as PDF | **Method D** — login required; articles are reviews, useful for guideline-style summaries. |

### Filename convention (shared with Method D)

The canonical naming conventions live in **`librarian.md`**. Sources-fetch delegates the rename in step 6 of the workflow above — don't duplicate the convention here. Brief reminder of the patterns:

- **Textbook chapter:** `{Book short name} {Edition} Ch{N} {Chapter title}.pdf`
- **Journal article:** `{First author} {Year} {Short title}.pdf`
- **Guideline document:** `{Society} {Year} {Topic}.pdf`

For full conventions, edge cases, and PDF-metadata-driven name inference, see `librarian.md`.

### When access fails — and the pause-and-resume pattern (shared with Method D)

Some walls clear in <30 seconds if the user steps into the live browser tab and handles them manually. Others are hard failures. Treat them differently.

#### Pause-and-resume (recoverable in-session)

Chrome MCP keeps the browser tab open between operations, and the user is at their machine. When you hit a wall the user can clear quickly, **pause the automation and ask them to handle it in the live tab**, then resume:

> *"I hit a [CAPTCHA / publisher account login / SSO redirect] on {platform} for {source}. The tab is open in your browser. Please complete it there, then tell me to continue."*

After the user signals "continue," retry the download — the session cookie usually persists, so the second attempt succeeds. This pattern applies to:

- **CAPTCHA challenges** (reCAPTCHA, hCaptcha, "verify you're human" puzzles)
- **Publisher-level account login on top of campus IP.** Some publishers (Wiley, Elsevier on certain titles) require a one-time interactive login even when the user is already on the institutional network. The login persists for the session.
- **SSO institutional login redirects** (Shibboleth, OpenAthens) — same pattern; user signs in once, automation resumes.

Do not try to solve CAPTCHAs programmatically — it violates publisher ToS and is not reliable in any case.

#### Hard failures (cannot be cleared in-session)

| Failure | Recovery |
|---|---|
| Paywall, no institutional access at all | Report to user. Suggest alternatives: PMC version, preprint server (medRxiv, bioRxiv), interlibrary loan. Do not bypass paywalls. |
| Geo-restriction | Report. Cannot proceed without VPN to an authorised region. |
| Persistent CAPTCHA after the user paused and tried | Stop the loop. Log as user-to-fetch. |
| File downloads but is corrupt / 0-byte | Re-attempt once, then report. |
| Repeated session expiry mid-batch | Stop the loop. Suggest the user re-authenticate fully and re-run the skill. |
| VPN auto-connect script error / timeout (`vpn-control.ps1` exit 4/5/6) | **Not a hard fail.** Fall through to the manual "Do you have VPN access?" ask (Method D); proceed if the user confirms. Surface the script failure once; do not retry the script in a loop. |

Don't retry a failed source more than once silently — failures usually indicate an access problem the user has to resolve. The pause pattern handles the easy cases; remaining failures need human attention out-of-band.

---

## Method D — Browser via Chrome MCP, with VPN auto-connect (entitled content)

Method D is **Method C with the institutional tunnel up**. It runs when Method C hits a paywall / login / SSO wall on entitled content (subscription journals, ClinicalKey, AccessMedicine, UpToDate), or when a library miss on a textbook chapter sends it straight here. It reuses the Method C **tooling, per-source workflow (steps 1–9), filename convention, and failure handling** verbatim — the only addition is bringing a VPN up first and releasing it after.

### Pre-flight access check

**Step 0 — read VPN config.** Look for a `## 8. VPN configuration` block in `CLAUDE.md` (format and security model in CLAUDE.md §8).

- **Config absent, or `Auto-connect: off`** → fall straight through to the **manual access ask** (verbatim, the original behaviour, preserved below). This is the default.
- **Config present and `Auto-connect: on`** → attempt scoped auto-connect (Step A) before the manual ask.

**Step A — scoped auto-connect.** Run only when ≥1 source has reached Method D:

```
powershell -ExecutionPolicy Bypass -File framework\building-blocks\vpn-control.ps1 -Action connect -VpnCli "<configured path>" -Profile "<configured profile>"
```

Branch on the exit code:

- **0** — *we* brought the tunnel up. Proceed with the Method C workflow. **Remember we own the tunnel** — the "Post-fetch — release the VPN" step below must run.
- **2** — a tunnel was already up (the user established it). Proceed with the Method C workflow. **Do NOT schedule teardown** (we don't own it).
- **4 / 5 / 6** (vpncli missing / connect failed or timed out / bad args) — **do not hard-fail.** Tell the user auto-connect didn't succeed, then fall through to the manual access ask below exactly as if config were absent.

**Manual access ask (fallback path — unchanged original behaviour):**

> *"I couldn't find these in your library: [list of missing items]. Do you have campus network or VPN access right now? I'll attempt the downloads via the Chrome extension; if a login wall appears, I'll stop and report."*

Claude cannot independently verify VPN state — the only reliable check is to attempt navigation and observe what loads. If the first download hits a paywall or login wall, stop the loop and report to the user; don't keep retrying every other source. If the user says no, skip Method D entirely and log the missing items as user-to-fetch — they can re-run the skill later when access is available.

### Run the fetch

With the tunnel up (auto or manual), run the **Method C "Workflow per source" steps 1–9** exactly as written, using the entitled-platform rows of the crib sheet. Pause-and-resume and the hard-failure table apply unchanged. Log the method string as `"Browser download, via VPN (<platform>)"`.

### Post-fetch — release the VPN if we brought it up

After the per-source loop finishes — **success, partial, or all-failed; teardown runs in every case** — and **only if Step A returned exit 0** (we own the tunnel):

```
powershell -ExecutionPolicy Bypass -File framework\building-blocks\vpn-control.ps1 -Action disconnect
```

- Exit **0** → released cleanly.
- Exit **5 / 7** → tell the user auto-disconnect didn't fully complete; the `SessionEnd` safety-net hook (CLAUDE.md §8) will retry, and the tunnel can be dropped manually. Never block or fail the fetch report on a teardown outcome.

If Step A returned **2** (pre-existing tunnel) or the manual fallback was used, **do not run disconnect** — we don't own the tunnel and must not tear down the user's own session.

---

## Common to all rungs

### Destination

All fetched files land in `{Project}/Sources/`. Originals are never modified — Method A opens library files read-only; Method B downloads only to the project's `Sources/`; Methods C/D move the browser download into `Sources/`.

### Acquisition log — hand-off to `references.md`

During the fetch loop, maintain `Sources/_acquisition_log.md`:

```markdown
# Sources acquisition log

| File | Citation (Vancouver-ready) | Method / source | Date |
|---|---|---|---|
| Harrisons IM 21e Ch121 Hyponatremia.pdf | Mount DB. Hyponatremia. In: Loscalzo J et al., editors. Harrison's PIM. 21st ed. McGraw-Hill; 2022. Ch. 121. | Local library extraction (`Harrisons-IM-21e.pdf`, p. 1015–1025) | 2026-05-15 |
| Spasovski 2014 European hyponatremia guideline.pdf | Spasovski G, et al. Clinical practice guideline on diagnosis and treatment of hyponatraemia. Eur J Endocrinol. 2014;170(3):G1–47. (PMID 24569125) | API (EuropePMC, open access) | 2026-05-15 |
| Garrahy 2021 Hypertonic saline RCT.pdf | Garrahy A, et al. Continuous versus bolus infusion of hypertonic saline in symptomatic hyponatremia. J Clin Endocrinol Metab. 2021;106(8):e3007–18. (PMID 33954787) | Browser download, via VPN (journal site) | 2026-05-15 |
```

This is a build aid — `references.md` Phase 2 reads it to:

- Populate the master Vancouver reference list at the top of `{Topic} outline.md`.
- Populate the sources summary table at the bottom of the outline (under `## Build aids — not for slides`), using the citations and method strings here.

The log file does not propagate into the deck. Once the master list and the sources summary table are populated, the log can be deleted or kept for audit.

### License sanity check (pass-through, not the primary check)

This skill does not replace `references.md` and `images.md` license discipline. But at fetch time, quick checks are worth doing:

- **Method A (textbooks the user owns):** local extraction for personal study and educational presentation is the user's call. The acquisition log records the source PDF for audit.
- **Method B (API resolver):** the resolver emits only open-access / author-deposited copies; record the `license` value it returns alongside the source string for downstream reference discipline.
- **Method C from PMC / open access:** confirm the article page shows a CC license (CC-BY, CC-BY-NC); flag if the journal is "free to read" but not openly licensed.
- **Method D from publisher sites behind a paywall:** the user's institutional access permits read-and-cite for educational use; do not redistribute the PDF outside the user's project.

If a paper turns out to be unsuitable for the planned use (e.g., CC-BY-ND chapter that the user wants to crop figures from), surface it during `images.md` figure planning, not at fetch time.

---

## Anti-patterns

| Anti-pattern | Why it fails | What to do instead |
|---|---|---|
| Asking the user which method to use up front | The ladder exists precisely so they don't have to; wastes a turn | Confirm the source list once, then let the ladder fall through automatically |
| Mass-fetching without confirming the source list | User ends up with files they didn't want; wastes a browser/VPN session | Confirm the list once at top of the loop; fetch in sequence |
| Reaching for the browser/VPN before trying Methods A and B | Wastes an institutional session on content that was free or local | Always try local library, then the API resolver, before any browser rung |
| Connecting the VPN at Method A/B/C, or for a non-paper before a wall | The VPN is only ever needed for entitled content at Method D | Only Method D Step A touches the VPN, and only after a real access wall |
| Tearing down a VPN tunnel the user opened themselves | Kills the user's own session mid-work | Only `disconnect` when the ownership marker proves *we* opened it (Step A exit 0) |
| Hard-failing the fetch when `vpncli.exe` is missing or times out | Blocks a fetch that could proceed via the manual path | Fall through to the manual access ask; never abort the loop on a VPN-script error |
| Modifying the original library PDF | Destroys the user's reference copy | Open library files read-only; write only to project `Sources/` |
| Silently overwriting an existing `Sources/{file}.pdf` | Loses prior version (may have been hand-annotated) | If file exists, ask before overwriting; offer `{file} (v2).pdf` |
| Cropping pages out of an extracted chapter | Loses figures and tables the user may need later | Extract the *whole* chapter (bookmark start to next-bookmark-end-1) |
| Reaching for a paywalled link after the resolver returns `resolved:false` | Bypassing a paywall violates publisher ToS | Fall through to Method D's institutional access; never bypass a paywall |
