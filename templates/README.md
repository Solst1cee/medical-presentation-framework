# PPTX templates

Put your institutional or personal PPTX templates here — one `.pptx` file per template.

A template is a base PowerPoint file with the institution's **master slide layouts, brand fonts, logo placement, and footer**. Claude uses it as a starting point in the unpack/repack XML build mode described in `framework/building-blocks/deck-build.md` Step 5 — generating new slides on top of the template's master without touching it.

---

## When to use a template

Bring one if:

- Your institution has a branded master slide design (logo position, colour scheme, footer line) and you want generated decks to look native.
- You have a colleague's deck whose layout you want to match.
- A conference has a required template (e.g., uniform title and section dividers).

Skip this folder entirely if you're fine with the academic default theme — `deck-build.md` will generate slides from scratch in that case.

---

## How Claude uses your templates

During Phase 1 kickoff, tell Claude:

> *"Use the template at `templates/your-template.pptx` as the base."*

Claude will:

1. Unpack the template into its XML components.
2. Generate new slides on top of the existing master layout.
3. Repack into a final deck.

The template itself stays untouched — the build produces a new file in `Deck/`.

---

## What's tracked in git

Only this README is tracked. Your own PPTX files (`*.pptx` inside this folder) are **gitignored** — templates are often institution-confidential or carry brand-image licensing constraints. Add or remove freely; framework updates won't touch your files.

---

## Naming convention

Use descriptive names so you can pick the right template quickly:

- `templates/Topic-review-master.pptx`
- `templates/Journal-club-master.pptx`
- `templates/Conference-2026-template.pptx`

Avoid filenames with timestamps or version numbers — those go in `Build_archive/Old_versions/` of individual projects, not in this shared templates folder.
