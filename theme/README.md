# Theme files

Put your reusable theme palettes here — one markdown file per named theme.

A theme file describes the **colours, font, font-size deviations, and footer convention** that `framework/building-blocks/deck-build.md` Step 2 (theme-constants block) expects. Saving a theme here means you don't re-specify it from scratch every time you build a deck — Claude reads your saved theme and applies the constants directly.

---

## How to create a theme file

A theme file is a small markdown document with frontmatter and a few sections. Minimum required fields:

````markdown
---
name: Academic Navy
description: Classic medicine-school palette — deep navy primary, warm red accent.
---

# Academic Navy

## Palette
- `ACCENT_PRIMARY`   = `#1F3864`   ← section dividers, body-text headings
- `ACCENT_SECONDARY` = `#C04125`   ← content-slide headers, key accents
- `HIGHLIGHT_BG`     = `#FAF0EC`   ← pearl box fill (light tint of secondary)

## Font
- Calibri

## Footer convention
- *"Division of [specialty] · [Institution]"*

## Font-size deviations (optional)
None — uses the framework defaults from `deck-build.md` Step 3.

## Logo geometry (optional — for unpack/repack XML mode)
None.
````

Add **font-size deviations** only if your audience needs different sizes than the framework defaults (the framework already uses larger-than-typical sizes for lecture-hall readability).

Add **logo geometry** only if you have an institutional master template that places a logo at a specific EMU coordinate.

---

## How Claude uses your theme files

During deck-build Phase 1 (kickoff), Claude asks whether you have a theme. Reply:

> *"Use the theme in `theme/your-theme.md`."*

Claude reads the file, fills in the theme-constants block per `deck-build.md` Step 2, and applies it to every slide in the build. You can keep multiple themes here (e.g., one per institution, one per department, one for journal clubs) and pick per project.

---

## What's tracked in git

Only this README is tracked. Your own theme files (`*.md` inside this folder) are **gitignored** — themes often contain institution-specific branding that shouldn't be in a public repo. Add or remove freely; framework updates won't touch your files.
