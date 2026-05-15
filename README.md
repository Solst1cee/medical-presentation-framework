# Medical Presentation Framework

A modular framework for **medical academic presentations** — topic reviews, journal clubs, and case discussions — designed to be used with **Claude Cowork** (Anthropic's desktop AI assistant). The framework gives Claude a structured way to help you research, outline, build, QA, and refine medical decks while keeping clinical accuracy and proper citation discipline.

Originally built by an internal-medicine resident in Thailand. The defaults assume a Thai-speaking academic audience with English medical terminology, but every default is designed to be swapped — see *Adapting the framework* below.

---

## What this framework does

When connected to Claude Cowork, it lets you say things like:

- *"Make a topic review on hyponatremia for our IM conference, 40 slides, Thai narrative."*
- *"Build a journal-club deck on the EMPEROR-Reduced trial."*
- *"Help me present this case I admitted last week."*

…and Claude will guide you through a structured workflow: clarifying scope, proposing an outline, researching from your PDFs, generating slides, doing visual QA, and (optionally) writing speaker notes + mock Q&A.

It is **not** an autopilot. The framework prioritises clinical accuracy, exact-wording from sources, and the user's editorial control over every decision.

---

## Designed for Claude Cowork

This framework expects to be loaded by Claude Cowork. If you're not using Claude Cowork, you can still read the markdown files as workflow documentation — but the auto-loading and skill triggers won't work.

**To use:**

1. Install Claude Cowork on your computer (see Anthropic's documentation).
2. Clone or download this repository to wherever you want it on your computer.
3. Connect Claude Cowork to the `Medical Presentation Framework/` folder — that becomes your workspace.
4. Tell Claude what you want to build (e.g., *"Make a topic review on AKI"*). Claude reads `CLAUDE.md` first to learn the framework, then loads the relevant framework files as it progresses through the workflow.

---

## Folder placement — what the workspace looks like

The `Medical Presentation Framework/` folder is **the Cowork workspace**. Both the framework's instruction files (`CLAUDE.md`, `README.md`, `framework/`, `sources-fetch.skill`) and your topic folders (Internal Medicine, Rheumatology, etc.) live inside it. Topic folders are created and edited next to the framework files — they're siblings.

```
Medical Presentation Framework/           ← Cowork workspace; point Cowork here
├── CLAUDE.md                              ← Cowork auto-reads this first
├── README.md                              ← this file (human-facing intro)
├── sources-fetch.skill                    ← Cowork auto-installs .skill bundles from root
├── (any other .skill bundles)
│
├── framework/                             ← the framework's instruction files
│   ├── retrospective.md
│   ├── safe-file-operations.md
│   ├── building-blocks/
│   ├── content-modules/
│   └── presentation-types/
│
├── theme/                                 ← your reusable theme palettes (markdown) — see theme/README.md
├── templates/                             ← your institutional or personal PPTX templates — see templates/README.md
│
├── Internal Medicine/                     ← your topic folders, organised by rotation
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

**About `theme/` and `templates/`:**

- `theme/` is where you save reusable palette files — colour values, fonts, footer convention. Drop one `*.md` file per named theme (e.g., `theme/Academic-Navy.md`). The framework reads from this folder when you build a deck, so a saved theme can be reused across projects. See `theme/README.md` for the file format.
- `templates/` is for institutional PPTX templates (`*.pptx` files). If your hospital has a branded master deck, drop it here and Claude uses it as the base for the unpack/repack build mode (`deck-build.md` Step 5). See `templates/README.md`.
- Both folders are gitignored except for their `README.md` — your saved themes and templates stay on your machine and aren't pushed to the public repo.

**Why this layout works:**

- Cowork auto-reads `CLAUDE.md` from the workspace root (the `Medical Presentation Framework/` folder).
- `.skill` bundles at the workspace root (like `sources-fetch.skill`) get auto-installed by Cowork.
- The framework's instruction set lives in the `framework/` subfolder — separate from anything Cowork treats as a skill, so there's no naming collision.
- Topic folders live as siblings of `framework/`, not inside it — your real work stays neatly separated from the framework's machinery.

---

## How to start a new presentation

Each presentation lives in its own folder under the relevant rotation. You have **two ways** to set this up.

### Option A — Let Claude create the folder structure (recommended for most users)

If you haven't created the project folder yet, just tell Claude what you want and where it should live:

> *"I want to make a topic review on hyponatremia for IM residents, around 40 slides. I haven't created the project folder yet — please set it up under `Internal Medicine/`."*

Claude will:

1. Create `Internal Medicine/Hyponatremia/` with the full subfolder structure (Sources/, Documents/, Deck/, Build_archive/Backups/, etc. — exactly as shown in Option B below).
2. Drop a starter `README.md` inside the project folder with the topic, audience, and date.
3. Tell you what to do next — typically:
   - *"Place your textbook PDFs and any key papers into `Sources/`."*
   - *"If you've already collected any figures, place them in `Sources/Figures/`."*
   - *"When ready, tell me what's in Sources and we'll begin Phase 1 (kickoff)."*

Letting Claude create the structure avoids the small mistakes that derail later phases (mistyped folder names, missing `Build_archive/Backups/`, wrong capitalisation). Once the folder exists and you've added your source PDFs, just say *"sources are in place — let's start"* and Claude moves into Phase 1.

### Option B — Create the folder structure yourself

If you prefer to set up the folder manually (e.g., you already have a project layout you like), build it with this structure:

```
Internal Medicine/
└── Hyponatremia/
    ├── README.md                        ← brief note: topic, audience, date
    ├── Sources/                         ← drop textbook PDFs, guidelines, primary papers here
    │   └── Figures/                     ← any images you've already collected
    ├── Documents/                       ← markdown outputs (Claude populates these)
    │   ├── Hyponatremia outline.md      ← created in Phase 3
    │   ├── Speaker_notes.md             ← if you opt into Phase 7
    │   ├── Mock_questions.md            ← if you opt into Phase 7
    │   └── Faculty_feedback.md          ← fill in after the talk
    ├── Deck/                            ← PPTX + PDF deliverables
    │   ├── Hyponatremia slide v1.pptx   ← Claude saves working versions here
    │   └── (later) Hyponatremia slide (Final).pptx + (Final).pdf
    └── Build_archive/                   ← working files Claude keeps; don't delete
        ├── Section_PPTXs/                ← standalone section rebuilds during iteration
        ├── Backups/                      ← safety copies made before risky edits
        └── Old_versions/                 ← superseded full-deck iterations
```

Then tell Claude where to find it:

> *"I want to make a topic review on hyponatremia in `Internal Medicine/Hyponatremia/`. I've put Harrison's Ch. 121 and the 2014 European hyponatremia guideline in `Sources/`."*

---

### The 7-phase workflow Claude runs

Whichever option you chose, Claude then runs through:

1. **Phase 1 (kickoff)** — ask about audience, duration, depth, theme preferences, and which sections to weight Heavy vs Standard vs Light.
2. **Phase 2 (research)** — read your PDFs, verify PMIDs, build a Vancouver reference list, fill in a sources-summary table.
3. **Phase 3 (outline)** — draft a slide-by-slide outline with figure placeholders; show you what's covered, ask you to confirm before building.
4. **Phase 4 (build)** — generate the PPTX with the agreed theme.
5. **Phase 5 (images)** — by default, insert placeholders for figures (so you control image quality) rather than auto-cropping.
6. **Phase 6 (visual QA)** — render to PDF, inspect for overflow / overlap / drift.
7. **Phase 7 (optional)** — speaker notes (in your audience's language) + mock Q&A for rehearsal.

Once you start editing slides directly in PowerPoint, Claude will ask whether to mirror each change back into the outline. Keeping both in sync prevents a future rebuild from silently reverting your hand edits — see `deck-build.md` Step 7 for the full lifecycle.

After the talk, Claude can help integrate faculty feedback safely (always with a backup first).

---

## What's inside the framework

```
Medical Presentation Framework/
├── CLAUDE.md                       Entry point. Claude reads this first to learn the framework.
├── README.md                       This file.
└── framework/
    ├── retrospective.md             Rolling log of presentations built with the framework — the "why" behind each rule. Append new cases over time.
    ├── safe-file-operations.md      Discipline. How to handle "Final" files without overwriting them. Always loaded.
    ├── presentation-types/          One file per presentation format (the entry points users invoke):
    │   ├── topic-review.md          7-phase workflow for rotation topic reviews
    │   ├── journal-club.md          Paper critique workflow (PICO, study design, validity)
    │   └── case-discussion.md       Case-presentation workflow
    ├── building-blocks/             Reusable mechanics, called by the presentation types:
    │   ├── deck-build.md            Theme selection, font sizes, 9 slide layouts, python-pptx + XML build modes
    │   ├── references.md            Vancouver citations, PMID verification, sources summary table
    │   ├── images.md                Open-access sourcing, license verification, figure summary table, placeholder default
    │   ├── speaker-notes.md         Audience-language narrative with English medical terms preserved
    │   ├── visual-qa.md             PDF render + PNG inspection workflow
    │   └── mock-qa.md               Anticipated faculty Q&A generation
    └── content-modules/             Optional content depth modules:
        ├── clinical-depth.md        Bedside layer (history + exam + cohort frequencies) for syndrome slides
        ├── disease-comparison.md    Mimic-comparison framework (e.g., NTM ↔ TB)
        ├── evidence-grading.md      Annotate guideline recommendations with their grade (GRADE / ACC-AHA / USPSTF)
        ├── local-guideline.md       Thai NLEM / NHSO / RCPT local-context integration
        └── paper-summary.md         Three-tier paper summary card (chip / compact landmark / full summary)
```

The **layered architecture** means: update a building block once → every presentation type that calls it gets the new version automatically. No copy-paste, no drift.

---

## Adapting the framework

The defaults reflect a Thai academic medical setting. Three places where adaptation is most likely:

1. **Theme palette.** `framework/building-blocks/deck-build.md` Step 1 asks the user about theme before generating slides — you can specify your institution's brand colours, hand Claude an existing PowerPoint template, or accept the academic default with a Pantone palette. The font-size constants in Step 2 are tuned for readability in a real lecture hall (~+2 pt over typical defaults).

2. **Language.** Speaker notes default to Thai narrative with English medical terms preserved. To switch to English-only or another audience language, say so at Phase 1 kickoff (`speaker-notes.md` describes the convention).

3. **Local-context content module.** `framework/content-modules/local-guideline.md` is Thailand-scoped (NHSO, RCPT, Thai formulary). For other countries, fork this file and substitute your national formulary / coverage system / specialty society references.

---

## Safety — non-negotiable

Before any operation that touches a "Final" or "important" file, the framework requires:

1. **Backup first** — a dated `.backup-YYYYMMDD-HHMM.pptx` copy in `Build_archive/Backups/`.
2. **Write to a new filename** — never overwrite the original; let the user verify and rename.
3. **Independent verification** — slide count, image count, speaker-note count, and content of 3–5 representative slides must match expectations before reporting done.

These rules are codified in `framework/safe-file-operations.md` and are read before any rebuild or post-feedback update. The background that led to these rules lives in `framework/retrospective.md`.

---

## Defaults at a glance

| Element | Default | Where to change |
|---|---|---|
| Slide language | English | Phase 1 kickoff, per project |
| Speaker-note language | Audience language + English medical terms (Thai narrative for Thai audiences) | Phase 1 kickoff |
| Theme | Academic-default Pantone palette; white background; Calibri font | `deck-build.md` Step 1 |
| Body bullet size | 16–18 pt (deliberately larger than typical) | `deck-build.md` Step 3 |
| Reference size | 10 pt italic (small by design — long text, not read during talk) | `deck-build.md` Step 3 |
| Image policy | Placeholders by default; user inserts real images | `images.md` |
| Source paraphrasing | Use exact wording from sources; no paraphrasing | `references.md` Phase 5 |
| Local context | Thailand-scoped (NHSO / RCPT / Thai formulary) | `local-guideline.md` |
| Source-of-truth lifecycle | Outline canonical until deck hand-editing begins; reconciliation between outline and deck is explicit, not automatic | `deck-build.md` Step 7 |

---

## License & contribution

This framework is offered as-is for use by medical residents, fellows, and faculty preparing academic presentations. If you adapt it for your country or institution, you're welcome to share back your local-guideline variant or any new presentation types you add.

The framework's design and the rationale behind each convention are captured in `framework/retrospective.md` — read once at the start of a new project, append to after each new presentation.
