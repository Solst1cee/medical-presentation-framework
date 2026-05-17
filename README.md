# Medical Presentation Framework

A modular framework for **medical academic presentations** — topic reviews, journal clubs, and case discussions — designed to be used with **Claude Cowork** (Anthropic's desktop AI assistant). It gives Claude a structured workflow to help you research, outline, build, QA, and refine medical decks while keeping clinical accuracy and proper citation discipline.

Originally built by an internal-medicine resident in Thailand. Defaults assume a Thai-speaking academic audience with English medical terminology, but every default is swappable — see *Adapting the framework*.

---

## What this framework does

When connected to Claude Cowork, you say things like:

- *"Make a topic review on hyponatremia for our IM conference, 40 slides, Thai narrative."*
- *"Build a journal-club deck on the EMPEROR-Reduced trial."*
- *"Help me present this case I admitted last week."*

…and Claude walks you through a structured **7-phase workflow**: clarifying scope → researching from your PDFs → drafting an outline → generating slides → visual QA → (optionally) speaker notes and mock Q&A.

It is **not** an autopilot. The framework prioritises clinical accuracy, **exact-wording from sources** (no paraphrasing), and the user's editorial control over every decision.

---

## Pick your path before installing

The framework supports four user paths. They differ in setup complexity, capability, and whether you can use them from mobile. Pick the one that fits your work pattern before you install — the steps below assume a path.

| Path | Where you run | Setup | Mobile? | Capability |
|---|---|---|---|---|
| **U1 — Cowork on PC** | Claude Cowork desktop | Easiest | No, desktop only | **Full framework** — outline, build, visual QA, all phases |
| **U2 — Claude Code on PC** | Claude Code CLI or IDE plugin | Medium | No, desktop only | **Full framework** — same as U1 |
| **U3 — Claude on web / iOS** | claude.ai/code in a browser or the Claude iOS app, connected to your fork | Medium (fork + GitHub setup) | Yes, any device | **Outline, references + OA paper fetch** — the open-access API resolver works (network-policy permitting); cannot generate `.pptx`, render PDFs, or browser/VPN-fetch paywalled papers or local-library chapters |
| **U4 — Remote Control** | Always-on PC, controlled from iOS via Claude Code Remote Control | Hardest (U2 setup + Remote Control enable) | Yes, any device | **Full framework** — the work runs on your home PC; your phone is a remote keyboard |

**Quick recommendations:**

- **Only ever at your desk** → U1 (simplest) or U2 (more flexible if you like terminals or VS Code).
- **Want to draft on the train, build at home** → U3 for outlining, then finish on U1 or U2 at your desk.
- **Want full power from your phone** → U4. Requires keeping a PC on and connected, but it is the only mobile path that supports the full deck-build workflow.

The install steps below cover U1 and U2 directly. U3 and U4 setup notes are in *Mobile and remote setup* later in this README.

---

## Installation — 4 steps

### Step 1 — Install Claude Cowork

Download and install Claude Cowork from Anthropic's website. Make sure it's launching correctly on your machine before continuing.

### Step 2 — Download the framework

You have two ways to get the framework files. **Git clone is recommended** because updates become a one-command operation; manual download works fine for first install but updating is more fragile.

**Option A — Clone with git (recommended)**

In a terminal (PowerShell on Windows, Terminal on macOS/Linux), navigate to wherever you want the framework folder to live, then:

```bash
git clone https://github.com/Solst1cee/medical-presentation-framework
```

Git creates a new folder called `medical-presentation-framework/` and puts everything inside it. If you want a different folder name (e.g., `My Presentations`):

```bash
git clone https://github.com/Solst1cee/medical-presentation-framework "My Presentations"
```

**Option B — Manual download (no git required)**

If you don't have git installed, or you'd rather not use a terminal:

1. Go to https://github.com/Solst1cee/medical-presentation-framework in your browser.
2. Click the green **"Code"** button → **"Download ZIP"**.
3. Extract the ZIP file. The extracted folder will be named `medical-presentation-framework-main/` (GitHub adds the `-main` branch suffix).
4. Rename the folder if you like — drop the `-main` to get `medical-presentation-framework/`, or rename to anything else such as `My Presentations`.
5. Move the folder to wherever you want it on your machine.

**Trade-off to know about** if you skip git:

- ✗ **Updates are harder.** With git, `git pull` (or `git reset --hard origin/main`) brings the latest framework files in one command. With manual download, you'll need to re-download the ZIP and carefully overlay the framework files onto your existing folder without disturbing your topic folders, saved themes, and templates. See *Keeping the framework up to date* below for the manual-update procedure.
- ✗ **No version history.** You can't see what changed between versions or roll back if something breaks.
- ✗ **No diff visibility.** With git you can run `git log -p` to see exactly what's new; manually, you'd have to compare folders side-by-side.
- ✓ **No tooling required.** Just a web browser and a ZIP extractor (built into Windows / macOS).

### Step 3 — Point Claude Cowork at the folder

In Cowork, create a new project and select the cloned folder as the workspace root. Cowork will detect `CLAUDE.md` at the root and treat it as the framework's main instruction file.

You should also see `.skill` bundles at the root (`sources-fetch.skill`, `librarian.skill`). When Cowork prompts to install them, accept — they enable ad-hoc paper acquisition and library management outside of a presentation workflow.

### Step 4 — Verify it loaded

Ask Claude something simple like *"What presentation types does this framework support?"*. You should get an answer that mentions **topic review**, **journal club**, and **case discussion** — that confirms Cowork found and read `CLAUDE.md`.

If Claude doesn't recognise the framework, double-check that:
- Cowork is pointed at the folder containing `CLAUDE.md` (not its parent or a subfolder).
- You restarted Cowork after first connecting the workspace.

---

## Folder layout after install

The cloned folder *is* the workspace. Topic folders you create later will live as siblings of `framework/`, inside this same workspace.

```
medical-presentation-framework/                  ← Cowork workspace; point Cowork here
│
├── CLAUDE.md                                     ← Cowork auto-reads this first
├── README.md                                     ← this file
├── sources-fetch.skill                           ← Cowork installs this on first run
├── librarian.skill                               ← Cowork installs this too
│
├── framework/                                    ← the framework's instruction files
│   ├── retrospective.md
│   ├── safe-file-operations.md
│   ├── building-blocks/                           (mechanics — deck-build, references, images, …)
│   ├── content-modules/                           (optional content — clinical-depth, paper-summary, …)
│   └── presentation-types/                        (entry points — topic-review, journal-club, case-discussion)
│
├── theme/                                        ← put your saved theme palettes here (gitignored except README)
├── templates/                                    ← put your institutional PPTX templates here (gitignored except README)
│
├── Internal Medicine/                            ← (you create these later) topic folders, organised by rotation
│   ├── Hyponatremia/
│   ├── Heart Failure GDMT/
│   └── Pneumonia in IC host/
│
├── Rheumatology/
│   ├── Gout & CPPD/
│   └── Psoriatic arthritis management/
│
└── Journal Club/
    └── EMPEROR-Reduced 2020/
```

---

## The 7-phase workflow — what runs when, and which tools are active

Every presentation Claude builds passes through these phases. Tools listed in the right column are the framework files Claude reads (and the `.skill` bundles Claude can call) at that phase.

| # | Phase | What happens | Tools / building blocks active |
|---|---|---|---|
| 1 | **Kickoff** | Claude asks: rotation, topic, audience, slide count, theme, weighting. Proposes outline structure based on topic type. | (none — interview only) |
| 2 | **Research** | Claude reads your PDFs in `Sources/`, verifies PMIDs, builds master reference list, fills a sources-summary table at the bottom of the outline. | `sources-fetch` (acquire chapters/papers), `librarian` (organise PDFs), `references` (Vancouver + PMID verification) |
| 3 | **Outline drafting** | Slide-by-slide outline with figure placeholders, `Ref:` lines, and an optional paper-summary card per landmark trial. `reference-audit` runs automatically before transitioning to Phase 4 — blocks the transition if any orphaned / broken citations exist. You confirm before any deck-build starts. | `references`, `reference-audit` (`audit_references.py`), `images` (figure-summary table), `paper-summary` (PICO cards on request), `clinical-depth`, `disease-comparison`, `local-guideline`, `evidence-grading` (content modules apply per slide as relevant) |
| 4 | **Build deck** | Claude generates the PPTX from the approved outline. Asks about theme/template if not already saved in `theme/` or `templates/`. Re-runs `reference-audit` as the first step — no broken refs propagate into slides. | `deck-build` (theme + layouts + python-pptx mechanics), `reference-audit` |
| 5 | **Image sourcing** | **Default: Claude inserts labelled placeholder textboxes** for each figure. You insert real images yourself. Claude only auto-sources images if you explicitly ask. | `images` (placeholder format + license rules), `sources-fetch` (if downloading figures from PMC) |
| 6 | **Visual QA** | Claude renders the deck to PDF, extracts PNG thumbnails, inspects for overflow / overlap / truncation / font-shrink / theme drift. | `visual-qa` |
| 7 | **Speaker notes + Mock Q&A** *(optional)* | Speaker notes in the audience's language (with English medical terms preserved); 25–40 anticipated faculty questions with difficulty grades. | `speaker-notes`, `mock-qa` |

**Discipline layer (always active):** `framework/safe-file-operations.md` — backup-before-modify rules apply throughout. If a file is called "Final" or "Important", Claude refuses to overwrite it without a fresh backup.

---

## Walkthrough — building a hyponatremia topic review, end to end

Here's what an actual session looks like.

### You say:

> *"I want to make a topic review on hyponatremia for IM residents, around 40 slides. I haven't created the project folder yet — please set it up under `Internal Medicine/`."*

### Claude does:

**Phase 1 (kickoff)** — Creates `Internal Medicine/Hyponatremia/` with full subfolder structure (Sources/, Documents/, Deck/, Build_archive/Backups/, etc.). Asks you:

- Audience? *"IM residents, Y2–Y3"*
- Duration? *"35 min + 10 min Q&A"*
- Theme? *"Use theme/Academic-Navy.md"* (or "academic default")
- Topic type and weighting? Claude classifies this as a **Type 2 (Syndrome / clinical pattern)** review and proposes weighting: Heavy on pathophysiology, clinical presentation, DDx, investigation; Standard on treatment; Light on local context, recent updates; Skip epidemiology, prognosis, special populations. You approve or adjust.

### You then say:

> *"Sources are in place. Harrison's Ch. 121 and the 2014 European hyponatremia guideline are in Sources/. Can you also fetch Adrogue & Madias 2000 (PMID 10816188)?"*

**Phase 2 (research)** — Claude invokes `sources-fetch` to acquire the Adrogue paper. Reads all PDFs in `Sources/`, verifies every PMID, builds the master Vancouver reference list at the top of `Hyponatremia outline.md`, and populates a sources-summary table at the bottom under `## Build aids — not for slides`. Reports back any surprises in the textbook content vs. what was expected.

**Phase 3 (outline)** — Claude expands the outline slide-by-slide between two markers:

```
> ▼ SLIDE DECK CONTENT — STARTS BELOW ▼
[Slide 1 to Slide 40]
> ▲ END OF SLIDE DECK CONTENT ▲
```

Figure placeholders are added as needed (e.g., AVP regulation cascade, MRI brain — central pontine myelinolysis). Build-aid section at the bottom now has Sources summary + Figure summary tables.

You ask: *"Summarise Garrahy 2021 — give me a compact card for slide 28."*

Claude invokes `paper-summary.md` Tier 2 and appends a compact landmark card to the build-aid section.

You confirm the outline. Claude does not build until you confirm.

### You say:

> *"Confirmed. Build it."*

**Phase 4 (build)** — Claude generates `Deck/Hyponatremia slide v1.pptx` using the Academic-Navy theme constants from `theme/Academic-Navy.md`. PPTX is created via python-pptx with all 9 slide layout patterns (title, section dividers, content, 4-quadrant, stat callouts, pearl boxes, images, references).

**Phase 5 (images)** — By default, Claude inserts labelled placeholder textboxes for each figure. You'll later replace these with real images during your review.

**Phase 6 (visual QA)** — Claude renders the deck to PDF (via LibreOffice), extracts PNG thumbnails of representative slides, inspects for overflow, overlap, drift. Reports any issues; offers to fix.

### Claude asks:

> *"Want speaker notes and a mock Q&A document?"*

You say yes.

**Phase 7 (optional)** — Speaker notes saved to `Documents/Speaker_notes.md` and embedded in the .pptx notes pane (Thai narrative with English medical terms preserved). Mock Q&A saved to `Documents/Mock_questions.md` with 25–40 anticipated questions graded ★ to ★★★ and tagged `[in deck — slide N]` or `[beyond deck]`.

### After your talk:

You capture faculty feedback in `Documents/Faculty_feedback.md`. Claude can help integrate gaps into a v2 of the deck — always with a dated backup first (per `safe-file-operations.md`).

---

## The framework's bundled tools (.skill files at the workspace root)

These two skills are installable by Cowork on first connect. They work both inside the 7-phase workflow AND as standalone commands anytime.

### `sources-fetch.skill`

**What it does:** Acquires textbook chapters, journal articles, or guideline PDFs and places them into a project's `Sources/` folder.

**A four-rung ladder, tried in order per source (stops at the first that works):**

1. **Method A — local-library extraction** from your digital textbook collection (reads `library-index.md`, copies or extracts the requested chapter; offline).
2. **Method B — free open-access API resolver** (PMID/DOI/title → a legal open-access PDF via PMC / Unpaywall / Europe PMC; no browser, no VPN).
3. **Method C — browser via Chrome MCP, no VPN** (free/open targets that still need a real browser).
4. **Method D — browser via Chrome MCP, with optional demand-driven VPN auto-connect** (entitled publisher content; requires campus network or VPN access). See *Customising the framework → Optional VPN auto-connect*.

**Trigger from anywhere:**

- *"Find me Harrison's chapter 121 on hyponatremia, put it in Sources/."*
- *"Download Adrogue 2000 PMID 10816188."*
- *"Get the KDIGO 2024 sodium guideline."*

### `librarian.skill`

**What it does:** Organises medical reference files — renames PDFs to a consistent convention, scans folders for new/removed items, maintains `library-index.md`, classifies textbooks as whole vs partial.

**Trigger from anywhere:**

- *"Clean up the filenames in my library."*
- *"Update library-index.md — I just dropped 5 new PDFs in my library folder."*
- *"List my textbooks."*
- *"What's in my Sources/ folder for the Hyponatremia project?"*

---

## Customising the framework

### Saving your theme palette

Put a markdown file in `theme/` describing your colours and fonts. Example: `theme/Academic-Navy.md` with palette `#1F3864` primary, `#C04125` secondary. See `theme/README.md` for the file format.

Once saved, just tell Claude *"Use the theme in theme/Academic-Navy.md"* during Phase 1.

### Saving an institutional PPTX template

Put your branded PPTX in `templates/`. Example: `templates/Institution-master.pptx`. Claude uses it as a base in unpack/repack XML build mode.

Both `theme/` and `templates/` are **gitignored** except their READMEs — your files stay on your machine.

### Faster, VPN-light paper fetching (the 4-rung ladder)

`sources-fetch` walks four rungs per source and stops at the first that works: **A** local library → **B** free open-access API resolver → **C** browser without VPN → **D** browser with VPN. Most papers with a legal free copy (PMC, author manuscripts, repositories) are resolved at rung B by `resolve_oa.py` with no browser and no VPN — so the VPN is only ever reached for genuinely entitled content at rung D. Set a contact email in `CLAUDE.md §9` (required by Unpaywall; a throwaway address is fine) and rung B works with zero further setup.

### Optional VPN auto-connect for paper downloads (Windows, opt-in)

**Off by default.** When you enable it, `sources-fetch` brings your institutional VPN up *only* at rung D (entitled content), and releases it when the fetch is done — so you don't connect/disconnect by hand.

- **Setup:** in `CLAUDE.md §8` set `Auto-connect: on`, your `vpncli.exe` path, and your VPN profile/host name. Built for Windows + Cisco Secure Client / AnyConnect (cert or saved creds, no MFA); an `openconnect` wrapper honouring the same verb contract works as a fallback if IT blocks `vpncli.exe`.
- **Security:** no credentials live in the repo — only the executable path and the profile name. Auth stays in Cisco's saved profile / Windows credential store.
- **Never breaks your own session:** disconnect is gated by a per-user ownership marker, so the framework only ever tears down a tunnel *it* opened — never one you opened yourself. An optional `SessionEnd` hook (snippet in `CLAUDE.md §8`, gitignored/per-machine) guarantees cleanup even if a session ends mid-fetch.
- **Validation:** the tunnel logic can't be exercised from Claude Code on the web (no Windows / no `vpncli.exe`); validate on your own machine with `vpn-control.ps1 -Action status` and the checklist behaviour described in `CLAUDE.md §8`.

---

## Keeping the framework up to date

The update steps differ per path. Pick the one matching the path you installed.

### U1 — Cowork on PC

1. `git pull` in the framework folder (or re-download the ZIP per *Option B* below).
2. If `sources-fetch.skill` or `librarian.skill` changed in that pull, open Cowork's skill manager and reinstall the changed bundle(s).
3. Restart Cowork so the registry picks up the new version.

### U2 — Claude Code on PC

1. `git pull` in the framework folder.
2. If you installed `sources-fetch.skill` or `librarian.skill` to `~/.claude/skills/`, re-copy the changed bundle(s) from the freshly-pulled repo into your skills folder.
3. No restart required — next session sees the new content.

### U3 — Claude on web / iOS

1. On GitHub, open your fork → click **Sync fork** → confirm.
2. Next claude.ai/code or iOS session reads the updated framework.

If you made local edits to framework files in your fork, syncing may produce merge conflicts — resolve on GitHub's web interface, or pull from upstream into a local clone if you have one.

### U4 — Remote Control

Same steps as U2, executed on your always-on PC. You can trigger the `git pull` and the skill re-copy via the Remote Control session from your iOS device — the commands run on the desktop where the session lives.

---

The two installation styles (clone vs ZIP) below back the steps above:

You have two ways to update, matching the two ways you installed. **Git is much cleaner**; manual update is doable but requires care to avoid overwriting your own content.

### Option A — Update with git (recommended)

```bash
cd medical-presentation-framework
git fetch origin
git reset --hard origin/main
```

This force-syncs all framework files to match the latest version on GitHub.

**What this preserves** (your personal content, untouched):

- Theme palettes in `theme/`
- PPTX templates in `templates/`
- Your topic folders (`Internal Medicine/`, `Rheumatology/`, etc.)
- Any local files matching `*_personal.md`
- Anything in `not-used/`

**What this discards:**

- Any modifications you accidentally made to framework files (e.g., if you or Claude touched `CLAUDE.md` or files inside `framework/` during a session).

If you have intentional local edits to framework files that you want to keep, use `git stash` before resetting (advanced workflow; see [git documentation](https://git-scm.com/docs/git-stash)).

### Option B — Update manually (no git required)

If you installed via manual download, updating means: download the latest ZIP, then carefully replace the *framework files* in your existing folder without touching your *personal content*.

**Step-by-step:**

1. **Download the latest ZIP.** Go to https://github.com/Solst1cee/medical-presentation-framework → green **"Code"** button → **"Download ZIP"**. Extract it to a **temporary location** (not your existing workspace folder). Call this temporary location *"NEW"* in the steps below.

2. **Identify your existing workspace folder.** This is the folder Cowork has been pointing at — likely called `medical-presentation-framework/` or `My Presentations/`. Call this *"EXISTING"*.

3. **Delete the old `framework/` subfolder inside EXISTING.** This is the most important single step. Why: a manual file-by-file copy can leave behind old framework files that were renamed or deleted in the update. Deleting the whole `framework/` folder ensures no orphan files remain. **Do not delete EXISTING itself** — only its `framework/` subfolder.

4. **Copy from NEW into EXISTING**, overwriting where files exist:
   - `CLAUDE.md`
   - `README.md`
   - `.gitignore` *(skip this if you've customised it)*
   - `sources-fetch.skill`
   - `librarian.skill`
   - `framework/` *(the whole folder you just deleted from EXISTING)*
   - `theme/README.md` *(only the README — leave the folder itself untouched)*
   - `templates/README.md` *(same)*

5. **Do NOT copy from NEW to EXISTING:**
   - The contents of `theme/` other than `README.md` — these are your saved theme palettes.
   - The contents of `templates/` other than `README.md` — these are your saved PPTX templates.
   - (In practice, NEW won't even have these files inside `theme/` or `templates/` — they're gitignored — so you can copy the whole `theme/` and `templates/` folders without harm, but it's safer to copy only their READMEs.)

6. **Verify nothing personal is missing.** Open EXISTING in your file explorer and confirm:
   - Your topic folders (`Internal Medicine/`, `Rheumatology/`, etc.) are still there.
   - Your saved themes (`theme/your-theme.md`) and templates (`templates/your-template.pptx`) are still there.
   - `framework/` has the expected file count — open the updated `CLAUDE.md` Section 1 (architecture diagram) and confirm every listed file is present in the folder.

7. **Re-open Cowork on the updated workspace.** It should auto-load the new `CLAUDE.md`.

**Concerns to watch for with manual update:**

- ⚠️ **Forgetting to delete the old `framework/` subfolder first.** If you skip step 3 and just copy on top, removed or renamed files from the old version stay around. Claude may then read stale content. **Always delete the old `framework/` folder before copying the new one.**
- ⚠️ **Accidentally deleting your topic folders or saved themes/templates.** Your work is interleaved with framework files at the workspace root. Going *file-by-file* rather than *folder-by-folder* keeps you safe. When in doubt, **back up EXISTING** (zip it) before starting the update.
- ⚠️ **Stale `sources-fetch.skill` or `librarian.skill` in Cowork's installed skills.** The bundle files at the workspace root will be replaced by the copy, but Cowork may have already installed the *previous* version of the skill. After updating, re-install each `.skill` bundle in Cowork to pick up changes.
- ⚠️ **No easy rollback.** If the update breaks something, you can't `git checkout` your way back. Keep a zip of the previous version as your rollback safety net.

**If you ever decide to switch from manual to git later**, you can: delete your existing manual-download folder, `git clone` fresh, then copy your topic folders, saved themes, and saved templates back into the cloned folder. From that point on, updates become `git pull`.

---

## Adapting the framework for non-Thai settings

The defaults reflect a Thai academic medical environment. Three points where adaptation is most likely:

1. **Theme palette.** `framework/building-blocks/deck-build.md` Step 1 asks the user about theme before generating slides — you can specify your institution's brand colours, hand Claude an existing PowerPoint template, or accept the academic default with a Pantone palette. The font-size constants in Step 2 are tuned for lecture-hall readability (~+2 pt over typical PowerPoint defaults).
2. **Language.** Speaker notes default to Thai narrative with English medical terms preserved. To switch to English-only or another audience language, say so at Phase 1 kickoff. See `framework/building-blocks/speaker-notes.md`.
3. **Local-context content module.** `framework/content-modules/local-guideline.md` is Thailand-scoped (NHSO, RCPT, Thai formulary). For other countries, fork this file and substitute your national formulary, coverage system, and specialty-society references.

---

## Safety — non-negotiable

Before any operation that touches a file marked "Final", "finalized", "presented", or "important", the framework requires:

1. **Backup first** — a dated `.backup-YYYYMMDD-HHMM.pptx` copy in `Build_archive/Backups/`.
2. **Write to a new filename** — never overwrite the original; let the user verify before renaming.
3. **Independent verification** — slide count, image count, speaker-note count, and content of 3–5 representative slides must match expectations before Claude reports done.

Codified in `framework/safe-file-operations.md`; background in `framework/retrospective.md`.

---

## Defaults at a glance

| Element | Default | Where to change |
|---|---|---|
| Slide language | English | Phase 1 kickoff, per project |
| Speaker-note language | Audience language + English medical terms (Thai narrative for Thai audiences) | Phase 1 kickoff |
| Theme | Academic-default Pantone palette; white background; Calibri font | `theme/your-theme.md` or `deck-build.md` Step 1 |
| Body bullet size | 18 pt with 16 pt floor (projection-ready; deliberately larger than typical PowerPoint defaults) | `deck-build.md` Step 3 |
| Reference font size | 10 pt italic (intentionally small — long text, not for reading during the talk) | `deck-build.md` Step 3 |
| Image policy | Placeholders by default; user inserts real images | `images.md` |
| Paper fetch ladder | A local library → B free OA API → C browser → D browser+VPN, per source | `sources-fetch.md`; email in `CLAUDE.md §9` |
| VPN auto-connect | Off (opt-in; Windows + Cisco `vpncli.exe`; only at rung D) | `CLAUDE.md §8` + `vpn-control.ps1` |
| Source paraphrasing | Use exact wording from sources — no paraphrasing | `references.md` Phase 5 |
| Local context | Thailand-scoped (NHSO / RCPT / Thai formulary) | `local-guideline.md` |
| Outline ↔ deck sync | Outline canonical until deck hand-editing begins; reconciliation is explicit, not automatic | `deck-build.md` Step 7 |

---

## License & contribution

This framework is offered as-is for medical residents, fellows, and faculty preparing academic presentat