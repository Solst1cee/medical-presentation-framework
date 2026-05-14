# CLAUDE.md — Medical Presentation Framework

A modular framework for medical academic presentations: topic reviews, journal clubs, case discussions (with M&M and operative-technique slots reserved for later formats). One set of reusable building blocks — deck-build, references, images, speaker-notes, visual-qa, mock-qa — that any presentation type can call.

Originally authored by an internal-medicine resident in Thailand. The default conventions (English slides, Thai-narrative speaker notes with English medical terms, a home-institution theme palette, Thai NLEM/NHSO local-context content module) reflect that setting. If you're adopting the framework elsewhere, the conventions in Section 4 and the theme constants in `skills/building-blocks/deck-build.md` are designed to be the points you swap.

**Where to start:** this file describes how the framework is laid out and how to use it. `skills/retrospective.md` is optional reading — it captures the lessons that shaped the defaults.

**Ignore `not-used/`.** It holds old backups and superseded drafts from framework development, not current framework files. Don't read, grep, or research inside `not-used/` when working on the framework — current canonical files live in `skills/` and at the project root. (It is also excluded from version control via `.gitignore`.)

---

## 1. Architecture — four layers

```
DISCIPLINE   skills/safe-file-operations.md            (always applies)
    ↑
PRESENTATION TYPES   skills/presentation-types/
                       ├── topic-review.md
                       ├── journal-club.md
                       └── case-discussion.md
    ↑ thin wrappers; reference building blocks by Read path
BUILDING BLOCKS   skills/building-blocks/
                       ├── deck-build.md      (theme + layouts + python-pptx + unpack/repack)
                       ├── references.md      (Vancouver + PMID verification)
                       ├── images.md          (PMC open-access + license + caption)
                       ├── speaker-notes.md   (audience-language narrative + English medical terms)
                       ├── visual-qa.md       (PDF render + PNG checks)
                       └── mock-qa.md         (anticipated Q&A, in/beyond deck)
    ↑ optionally enriched by
CONTENT MODULES   skills/content-modules/
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
| "topic review", "rotation presentation", "prepare slides for [topic]" | `skills/presentation-types/topic-review.md` |
| "journal club", "critique this paper", "PICO" | `skills/presentation-types/journal-club.md` |
| "case discussion", "case conference", "present a case" | `skills/presentation-types/case-discussion.md` |

Each presentation-type skill has its own workflow phases. They reference the building blocks by `Read` path — when Claude reaches a phase, it loads the relevant building block at that moment. This keeps each presentation-type wrapper thin (~200 lines) and the mechanics in one canonical place.

---

## 3. Safety rules — read before any rebuild

Three rules apply universally and are codified in `skills/safe-file-operations.md`:

1. **NEVER overwrite a file the user calls "Final", "finalized", "presented", or "important".** Write the new version to a different filename. Let the user verify, then rename.
2. **Make your OWN backup before modifying any important file**, using `{file}.backup-YYYYMMDD-HHMM.{ext}`. Don't delegate the backup step.
3. **Don't trust subagent "success" reports without independent verification.** Check file size, slide count, image count, content of 3–5 representative slides.

Read `skills/safe-file-operations.md` before any operation that modifies a finalized artifact.

---

## 4. Conventions — apply to every presentation

These are the defaults. Override them per project as needed.

- **Slides:** English by default. Switch to another language only if the user explicitly requests it for a particular file.
- **Speaker notes:** audience-language narrative with English medical terms preserved exactly as taught (`Mycobacterium marinum`, `Tinel's sign`, `ATS/IDSA`). For a Thai-speaking audience, this means Thai prose with English clinical terms; English-only on explicit request. See `skills/building-blocks/speaker-notes.md`.
- **References:** Vancouver-numbered master list at the top of `Documents/Outline.md`. Per-slide `Ref:` line at the bottom. PMIDs verified by web search before adding. See `skills/building-blocks/references.md`.
- **Images:** Open-access only (PMC, CC-BY / CC-BY-NC), license verified at the source, caption derived from the paper. See `skills/building-blocks/images.md`.
- **Depth:** Fellowship-level by default — mechanisms, edge cases, evidence behind every key recommendation. Only ask to go shallower if the user requests it.
- **Local context:** For any drug-related or test-related slide, pair the international guideline with a local-formulary / availability footnote. The provided `skills/content-modules/local-guideline.md` is Thailand-scoped; copy and adapt for other settings.
- **Source-of-truth lifecycle:** the outline is canonical until the user begins hand-editing the deck; from that point, outline and deck require explicit reconciliation rather than an automatic switchover. See `skills/building-blocks/deck-build.md` Step 7 for the four phases and the reconciliation prompts.

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

The presentation-type skills assume this structure. **At kickoff, the first thing Claude should check is whether the project folder already exists.** If it doesn't, Claude should offer to create the full structure rather than asking the user to set it up manually — this avoids mistyped folder names, missing subfolders, and other setup errors that derail later phases. Only after the folder exists (or the user explicitly says they'll create it themselves) does Claude move into the workflow's kickoff questions.

---

## 6. Where to look for what

| Question | Where |
|---|---|
| Why is the framework structured this way? | Section 1 above (architecture) + `skills/retrospective.md` (the lessons that drove the split) |
| What's the rationale behind the conventions? | `skills/retrospective.md` |
| How do I build a topic review / journal club / case discussion? | `skills/presentation-types/{type}.md` |
| How do I assemble a PPTX? Theme constants? | `skills/building-blocks/deck-build.md` |
| How do I cite papers correctly? | `skills/building-blocks/references.md` |
| How do I find open-access figures? | `skills/building-blocks/images.md` |
| How do I write speaker notes? | `skills/building-blocks/speaker-notes.md` |
| How do I QA the deck visually? | `skills/building-blocks/visual-qa.md` |
| How do I generate mock Q&A? | `skills/building-blocks/mock-qa.md` |
| How do I add a bedside layer to a syndrome slide? | `skills/content-modules/clinical-depth.md` |
| How do I compare against a clinical mimic? | `skills/content-modules/disease-comparison.md` |
| How do I grade a recommendation (GRADE / ACC-AHA / USPSTF)? | `skills/content-modules/evidence-grading.md` |
| How do I add local formulary / coverage context? | `skills/content-modules/local-guideline.md` |
| How do I summarise a paper (chip / landmark card / full summary)? | `skills/content-modules/paper-summary.md` |
| How do I safely modify a finalized file? | `skills/safe-file-operations.md` |

---

*Medical Presentation Framework — layered architecture. Update a building block once; every presentation type that uses it gets the new version on the next session.*
