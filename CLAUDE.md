# CLAUDE.md — Medical Presentation Framework

A modular framework for medical academic presentations: topic reviews, journal clubs, case discussions (with M&M and operative-technique slots reserved for later formats). One set of reusable building blocks — deck-build, sources-fetch, librarian, references, reference-audit, images, speaker-notes, visual-qa, mock-qa — that any presentation type can call.

Originally authored by an internal-medicine resident in Thailand. The default conventions (English slides, Thai-narrative speaker notes with English medical terms, a home-institution theme palette, Thai NLEM/NHSO local-context content module) reflect that setting. If you're adopting the framework elsewhere, the conventions in Section 4 and the theme constants in `framework/building-blocks/deck-build.md` are designed to be the points you swap.

**Where to start:** this file describes how the framework is laid out and how to use it. `framework/retrospective.md` is optional reading — it captures the lessons that shaped the defaults.

---

## 0. First-time setup for adopters

This framework is designed to be **opened as a Cowork project**. Most of the workflow (topic-review, journal-club, case-discussion) loads from inside this folder via Read path — Claude reads `CLAUDE.md`, sees the framework, and follows the layered framework files. **Open the framework folder as your Cowork project before asking for a topic review, journal club, or case discussion.**

A small number of skills are also packaged as `.skill` bundles at the project root, for cases where direct triggering from outside the framework folder makes sense.

### What's bundled, what's not — and why

- **Bundled** (`.skill` at project root): **sources-fetch** and **librarian**. Both are useful standalone — `sources-fetch` for ad-hoc chapter / paper / guideline acquisition; `librarian` for renaming PDFs and maintaining `library-index.md` outside any presentation workflow. Both are self-contained enough to trigger cleanly from anywhere on the machine once installed.
- **Not bundled** (folder-only): **topic-review, journal-club, case-discussion**. These are *thin wrappers* that load building blocks via relative paths like `framework/building-blocks/deck-build.md`. Those paths only resolve when the working directory is the framework folder. Bundling them would force a choice between (a) shipping copies of every building block inside each `.skill` (defeating the layered architecture's update-once principle) or (b) shipping broken paths. Folder-only is the honest answer.

### Where this framework runs

The framework runs in **Claude Cowork (desktop)**, **Claude Code (desktop terminal or IDE plugin)**, and **Claude Code Remote Control** (iOS app driving a desktop session) — all with full capability.

In **claude.ai/code on the web or the Claude iOS app** (cloud mode), the framework runs with **reduced capability**: outline drafting and the reference audit work, but deck generation does not (no python-pptx, no LibreOffice, no Chrome MCP for paper acquisition). If a user invokes a deck-build phase (Phase 4 onward) from cloud mode, surface this limitation immediately — do not attempt and fail opaquely. See `README.md` "Pick your path" for the full user-facing comparison.

### Claude — on the first session in a new environment, do this check

1. Look at the current `available_skills` list (in the system reminder).
2. For each `.skill` bundle present at the project root, check whether a matching skill name is already installed.
3. If any are missing, list them to the user and offer to install via `present_files` so they get a one-click install card. Do not install silently — let the user choose.

After install, the user may need to restart Cowork for the new skill to appear in `available_skills`.

---

## 1. Architecture — four layers

```
DISCIPLINE   framework/safe-file-operations.md            (always applies)
    ↑
PRESENTATION TYPES   framework/presentation-types/
                       ├── topic-review.md
                       ├── journal-club.md
                       └── case-discussion.md
    ↑ thin wrappers; reference building blocks by Read path
BUILDING BLOCKS   framework/building-blocks/
                       ├── deck-build.md         (theme + layouts + python-pptx + unpack/repack)
                       ├── sources-fetch.md      (4-rung ladder: local library → free OA API → browser → browser+optional auto-VPN → Sources/)
                       ├── librarian.md          (rename PDFs, maintain library-index.md, classify whole vs partial)
                       ├── references.md         (Vancouver + PMID verification)
                       ├── reference-audit.md +  (automated orphan/broken-citation check;
                       │   audit_references.py    triggered on slide-removal, end-Phase-3, start-Phase-4, final)
                       ├── images.md             (PMC open-access + license + caption)
                       ├── speaker-notes.md      (audience-language narrative + English medical terms)
                       ├── visual-qa.md          (PDF render + PNG checks)
                       └── mock-qa.md            (anticipated Q&A, in/beyond deck)
    ↑ optionally enriched by
CONTENT MODULES   framework/content-modules/
                       ├── clinical-depth.md       (bedside Hx + exam + cohort %)
                       ├── disease-comparison.md   (mimic-comparison framework)
                       ├── evidence-grading.md     (GRADE / ACC-AHA / USPSTF on recommendations)
                       ├── local-guideline.md      (Thailand: NLEM, NHSO, RCPT — adapt per setting)
                       └── paper-summary.md        (3-tier: chip / landmark card / full summary — on request)
```

**Why this matters:** update a building block once → every presentation type that calls it gets the new version automatically. No copy-paste, no drift. M&M and operative-technique skill files are deliberately not built yet — add them when a real project for those formats appears.

---

## 2. Quick-start by presentation type

Trigger phrases the user might say, and which skill loads:

| User says | Skill that triggers |
|---|---|
| "topic review", "rotation presentation", "prepare slides for [topic]" | `framework/presentation-types/topic-review.md` |
| "journal club", "critique this paper", "PICO" | `framework/presentation-types/journal-club.md` |
| "case discussion", "case conference", "present a case" | `framework/presentation-types/case-discussion.md` |

Each presentation-type skill has its own workflow phases. They reference the building blocks by `Read` path — when Claude reaches a phase, it loads the relevant building block at that moment. This keeps each presentation-type wrapper thin (~200 lines) and the mechanics in one canonical place.

---

## 3. Safety rules — read before any rebuild

Three rules apply universally and are codified in `framework/safe-file-operations.md`:

1. **NEVER overwrite a file the user calls "Final", "finalized", "presented", or "important".** Write the new version to a different filename. Let the user verify, then rename.
2. **Make your OWN backup before modifying any important file**, using `{file}.backup-YYYYMMDD-HHMM.{ext}`. Don't delegate the backup step.
3. **Don't trust subagent "success" reports without independent verification.** Check file size, slide count, image count, content of 3–5 representative slides.

Read `framework/safe-file-operations.md` before any operation that modifies a finalized artifact.

---

## 4. Conventions — apply to every presentation

These are the defaults. Override them per project as needed.

- **Slides:** English by default. Switch to another language only if the user explicitly requests it for a particular file.
- **Speaker notes:** audience-language narrative with English medical terms preserved exactly as taught (`Mycobacterium marinum`, `Tinel's sign`, `ATS/IDSA`). For a Thai-speaking audience, this means Thai prose with English clinical terms; English-only on explicit request. See `framework/building-blocks/speaker-notes.md`.
- **References:** Vancouver-numbered master list at the top of `Documents/Outline.md`. Per-slide `Ref:` line at the bottom. PMIDs verified by web search before adding. See `framework/building-blocks/references.md`.
- **Images:** Open-access only (PMC, CC-BY / CC-BY-NC), license verified at the source, caption derived from the paper. See `framework/building-blocks/images.md`.
- **Depth:** Fellowship-level by default — mechanisms, edge cases, evidence behind every key recommendation. Only ask to go shallower if the user requests it.
- **Local context:** For any drug-related or test-related slide, pair the international guideline with a local-formulary / availability footnote. The provided `framework/content-modules/local-guideline.md` is Thailand-scoped; copy and adapt for other settings.
- **Source-of-truth lifecycle:** the outline is canonical until the user begins hand-editing the deck; from that point, outline and deck require explicit reconciliation rather than an automatic switchover. See `framework/building-blocks/deck-build.md` Step 7 for the four phases and the reconciliation prompts.

---

## 5. Folder structure per project

Each presentation lives in its own folder under the relevant rotation or format:

```
{Department or Format}/
└── {Topic / Paper / Case}/
    ├── README.md
    ├── Sources/                         # textbook PDFs, guidelines, primary papers
    │   └── Figures/                     # open-access images
    ├── Documents/                       # markdown outputs
    │   ├── {Topic} outline.md
    │   ├── Speaker_notes.md
    │   ├── Mock_questions.md
    │   └── Faculty_feedback.md          # filled after the talk
    ├── Deck/                            # PPTX + PDF deliverables (live working copies)
    │   └── {Topic} slide v1.pptx → v2 → ... → {Topic} slide (Final).pptx + (Final).pdf
    └── Build_archive/                   # working files (keep, don't delete)
        ├── Section_PPTXs/                # standalone section rebuilds (see deck-build.md Step 7)
        ├── Backups/                      # safety copies made before risky edits (see safe-file-operations.md)
        └── Old_versions/                 # superseded full-deck iterations the user no longer actively edits
```

The presentation-type files assume this structure. **At kickoff, the first thing Claude should check is whether the project folder already exists.** If it doesn't, Claude should offer to create the full structure rather than asking the user to set it up manually — this avoids mistyped folder names, missing subfolders, and other setup errors that derail later phases. Only after the folder exists (or the user explicitly says they'll create it themselves) does Claude move into the workflow's kickoff questions.

---

## 6. Where to look for what

| Question | Where |
|---|---|
| Why is the framework structured this way? | Section 1 above (architecture) + `framework/retrospective.md` (the lessons that drove the split) |
| What's the rationale behind the conventions? | `framework/retrospective.md` |
| How do I build a topic review / journal club / case discussion? | `framework/presentation-types/{type}.md` |
| How do I assemble a PPTX? Theme constants? | `framework/building-blocks/deck-build.md` |
| How do I auto-fetch a textbook chapter or paper into `Sources/`? | `framework/building-blocks/sources-fetch.md` (4-rung ladder) |
| How do I resolve a PMID/DOI to a free open-access PDF (no browser/VPN)? | `framework/building-blocks/resolve_oa.py` (sources-fetch Method B); config in §9 |
| How do I auto-connect a VPN only when fetching papers needs it? | §8 below + `framework/building-blocks/vpn-control.ps1` (sources-fetch Method D) |
| How do I rename PDFs / update `library-index.md` / classify a textbook? | `framework/building-blocks/librarian.md` |
| How do I cite papers correctly? | `framework/building-blocks/references.md` |
| How do I check for orphaned / broken citations automatically? | `framework/building-blocks/reference-audit.md` (uses `audit_references.py`) |
| How do I find open-access figures? | `framework/building-blocks/images.md` |
| How do I write speaker notes? | `framework/building-blocks/speaker-notes.md` |
| How do I QA the deck visually? | `framework/building-blocks/visual-qa.md` |
| How do I generate mock Q&A? | `framework/building-blocks/mock-qa.md` |
| How do I add a bedside layer to a syndrome slide? | `framework/content-modules/clinical-depth.md` |
| How do I compare against a clinical mimic? | `framework/content-modules/disease-comparison.md` |
| How do I grade a recommendation (GRADE / ACC-AHA / USPSTF)? | `framework/content-modules/evidence-grading.md` |
| How do I add local formulary / coverage context? | `framework/content-modules/local-guideline.md` |
| How do I summarise a paper (chip / landmark card / full summary)? | `framework/content-modules/paper-summary.md` |
| How do I safely modify a finalized file? | `framework/safe-file-operations.md` |

---

## 7. Library configuration (sources-fetch Method A)

For local-library extraction (textbook chapters from a digital collection on your own machine):

- **Library root:** *(set to your local path, e.g., `D:\MEDICINE\TEXTBOOK` on Windows or `~/Medical Library/` on macOS)*
- **Index file:** `library-index.md` at the library root

`sources-fetch.md` reads the index from this location on every Method A fetch. Set the library root to wherever you keep your digital textbook collection on this machine, then create `library-index.md` listing each book's filename and chapters. Update the index via `librarian.md` whenever you add or remove books.

---

## 8. VPN configuration (sources-fetch Method D) — opt-in, default OFF

Off by default. The framework does **not** touch any VPN unless you explicitly turn this on. Other adopters use different VPN clients (or none), so this stays opt-in and is never a tracked always-on hook.

- **Auto-connect:** off            *(set to `on` to enable demand-driven connect/disconnect)*
- **VPN client:** Cisco Secure Client / AnyConnect (`vpncli.exe`)
- **vpncli.exe path:** *(e.g. `C:\Program Files (x86)\Cisco\Cisco Secure Client\vpncli.exe` — legacy AnyConnect uses `...\Cisco AnyConnect Secure Mobility Client\vpncli.exe`. If unset, `vpn-control.ps1` probes both; set explicitly if probing fails.)*
- **VPN profile / host name:** *(the connection name as it appears in the Cisco client, e.g. `vpn.university.edu` — name only)*
- **Fallback client (if IT blocks vpncli.exe):** *(optional path to an `openconnect` wrapper exposing the same `status|connect|disconnect` verbs and exit-code contract)*

**Security model:** no credentials are stored here or anywhere in the repo — only the executable path and the profile *name*. Authentication uses Cisco's own saved profile / Windows credential store (cert or saved creds, no MFA prompt). Connect is scoped to **Method D only** and only after a real access wall; the lower rungs (A local, B API, C free browser) never touch the VPN. Disconnect is ownership-gated by a per-user marker file in `%TEMP%` — the framework never tears down a tunnel you opened yourself. If auto-connect is off or fails, sources-fetch falls back to asking you manually.

Mechanics live in `framework/building-blocks/vpn-control.ps1` (`status` / `connect` / `disconnect`).

**Optional safety-net hook (you create this on opt-in).** So a tunnel we opened is always released even if a session ends mid-fetch, create `.claude/settings.json` (it is gitignored — per-machine, not shipped) with:

```json
{ "hooks": { "SessionEnd": [ { "hooks": [ {
  "type": "command", "shell": "powershell",
  "command": "powershell -ExecutionPolicy Bypass -File framework\\building-blocks\\vpn-control.ps1 -Action disconnect",
  "timeout": 60, "async": true,
  "statusMessage": "Releasing framework-owned VPN tunnel (if any)..." } ] } ] } }
```

This is a marker-gated no-op unless `vpn-control.ps1 connect` left a tunnel up; it can never drop a tunnel you opened. (Only `SessionEnd` — not `Stop`, which fires every turn and would tear the tunnel down mid-fetch.)

---

## 9. API resolver configuration (sources-fetch Method B)

Used by `resolve_oa.py` to turn a PMID/DOI/title into a *legal* open-access PDF with no browser and no VPN.

- **Contact email:** *(e.g. `you@example.org` — required by Unpaywall, requested by NCBI for politeness. A role or throwaway address is fine. Note: if you commit `CLAUDE.md`, this email lands in the repo; keep it generic or set it locally only.)*
- **NCBI API key:** set via the `NCBI_API_KEY` environment variable **only — never in the repo** (it merely raises the rate limit and is not required).

If no email is configured the resolver still runs the Europe PMC / PMC PMID path, but Unpaywall (DOI-keyed) is skipped and those sources fall through to Method C/D. The resolver emits only openly-licensed / author-deposited URLs — it never returns a paywalled link.