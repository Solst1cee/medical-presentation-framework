---
name: visual-qa
description: "Building block for visual quality assurance of a finished deck — render to PDF, extract PNG/JPG thumbnails, and check for overflow, overlap, truncation, font-shrink, and theme drift. Loaded by Read path from a presentation-type skill; not intended to auto-trigger on its own."
---

# Visual QA — render and inspect before finalizing

## Why this matters

A python-pptx build script can produce a structurally valid .pptx that looks broken when actually opened. Common failure modes that the build script will not catch:

- **Text overflow** — bullet runs past the slide edge or into the reference area at the bottom
- **Shape overlap** — pearl box covers a reference line; image overlaps a text frame; two text boxes share pixels
- **Truncation** — long bullet text is cut off mid-sentence with no `…` indicator
- **Font auto-shrink** — PowerPoint auto-reduces font size to fit content, sometimes to 7 pt; the slide builds successfully but is unreadable
- **Theme drift** — a single slide has a slightly different accent colour than the rest; happens when a constant is misspelled in one helper call (e.g., `ACCENT_PRIMARY` typo vs an inline RGB value)
- **Image scaling** — a CC-BY image is stretched or squashed; aspect ratio breaks
- **Caption misalignment** — caption text frame is offset from the image it describes

None of these will trigger a python-pptx error. They only become visible when you *look at* the rendered slides.

---

## The render-and-inspect loop

After every significant build, run this loop:

### Step 1 — Render to PDF

LibreOffice headless is the reliable cross-platform renderer:

```bash
soffice --headless --convert-to pdf "Deck/{Topic} slide v3.pptx" --outdir /tmp/
```

Expected output: `/tmp/{Topic} slide v3.pdf`. The render takes ~10–30 seconds for a 50-slide deck.

If LibreOffice isn't available, use PowerPoint itself on the user's machine — but the headless route is faster for iteration.

### Step 2 — Convert PDF to PNG thumbnails

```bash
pdftoppm -jpeg -r 120 "/tmp/{Topic} slide v3.pdf" /tmp/qa_slide
# Produces /tmp/qa_slide-01.jpg, qa_slide-02.jpg, ...
```

Resolution 120 dpi is enough to spot overflow/overlap. Higher (200+ dpi) for fine-grained font inspection.

### Step 3 — Inspect representative slides

Read 4–6 thumbnails using the `Read` tool (which renders images visually) — pick:

- The **title slide** (theme + footer pattern check)
- A **section divider** (`ACCENT_PRIMARY` fill + accent bar check)
- A **content slide** with dense bullets (overflow check)
- A **4-quadrant slide** (quadrant alignment + density check)
- An **image slide** (image scaling + caption alignment)
- A **references slide** (line spacing + truncation)

If any reveals a problem, fix and re-render. Don't trust a single sample.

### Step 4 — Build a contact-sheet for whole-deck scan

For decks over 30 slides, build a small contact-sheet image to scan the whole deck at once:

```bash
# Resize each thumbnail to 800 wide, then tile 4 across
for f in /tmp/qa_slide-*.jpg; do
  convert "$f" -resize 800x "$f"
done
montage /tmp/qa_slide-*.jpg -tile 4x -geometry +5+5 /tmp/contact_sheet.jpg
```

Read `/tmp/contact_sheet.jpg` — the whole deck appears at-a-glance. Drift between slides becomes visible immediately.

---

## The 5-point QA checklist (apply to every inspected slide)

### 1. Text overflow

- [ ] Does any bullet extend past the right edge of the slide?
- [ ] Does the body content overlap the reference area at the bottom (see `deck-build.md` Step 3 for body / reference y-boundaries)?
- [ ] Are any lines wrapping unexpectedly because of font size?

Fix: shorten the bullet, reduce font size **within the element's range** (see `deck-build.md` Step 3 — e.g., body bullets stay in the 16–18 pt range), or split across two bullets. Don't reduce below the range minimum.

### 2. Shape overlap

- [ ] Do any two text boxes occupy the same pixels?
- [ ] Does the pearl box cover the reference line?
- [ ] Does an image overlap the text frame next to it?

Fix: reduce one of the shapes' dimensions; reposition; or split the slide into two.

### 3. Truncation

- [ ] Is any bullet cut off mid-sentence?
- [ ] Are any reference citations cut off?
- [ ] Is the speaker-notes content in the notes pane truncated?

Fix: increase the text frame height; reduce font; shorten content.

### 4. Font auto-shrink

- [ ] Has python-pptx auto-shrunk any text **below the element's range minimum** in `deck-build.md` Step 3 (body bullets shouldn't drop below 16 pt; 4-quadrant below 13 pt; references below 10 pt; etc.)?
- [ ] If so, is the content actually readable, or has it gone microscopic?

Fix: disable autofit on the offending frame, then either genuinely shorten the content or split the slide. Don't allow autofit to push text below the element's range minimum in `deck-build.md` Step 3.

### 5. Theme drift

- [ ] Is every content-slide header bar the same `ACCENT_SECONDARY`?
- [ ] Is every section-divider fill the same `ACCENT_PRIMARY`?
- [ ] Is the body font consistent on every slide (default Calibri — no Arial or other slip)?
- [ ] Is the footer text the same on every slide?

Fix: trace back to which helper or hard-coded RGB produced the off-theme slide. All colours should come from the theme constants block (`deck-build.md` Step 2).

---

## Whole-deck scans — what to look for on the contact sheet

When you read the contact-sheet thumbnail, you're looking for:

- **Section structure** — section dividers appear at roughly regular intervals; one slide stands out clearly as "Section 4" or whatever
- **Density gradient** — content slides early are denser (epidemiology, pathophysiology) and later are denser again (treatment, outcomes); the gradient should look reasonable, not chaotic
- **Colour consistency** — `ACCENT_SECONDARY` headers throughout content slides; `ACCENT_PRIMARY` on section dividers; no rogue colours from a forgotten test slide or hard-coded RGB
- **Image distribution** — image slides clustered in the disease-description or imaging sections, not scattered randomly
- **Reference slides** at the very end — distinguishable from content slides at a glance

---

## When to apply this

| Trigger | Apply |
|---|---|
| Just rebuilt the whole deck | Yes — full render + sample 6 slides |
| Modified one slide | Render that slide only (PDF page N), inspect |
| Added images to several slides | Re-render and inspect image slides + their neighbors |
| About to declare the deck "Final" | Yes — full render + contact sheet + 8 sample slides |
| Post-feedback rebuild | Yes — full render + careful spot-check of changed slides |

---

## Anti-patterns to avoid

- **Building without visual QA** — "it built without errors so it's fine"
- **Inspecting only the title slide** — the title is the easiest slide; the failures are mid-deck
- **Delegating visual QA to a subagent without verifying** — the subagent can't actually open the file in PowerPoint and may misreport. Verify independently by reading the PDF / PNG thumbnails yourself.
- **Skipping QA on a "small" change** — small changes routinely cause overflow if they touch text length

---

## Self-check before declaring the deck visually complete

- [ ] Full deck has been rendered to PDF without errors
- [ ] PDF was converted to thumbnails at ≥ 120 dpi
- [ ] At least 6 representative slides (across sections, layouts, content types) were inspected
- [ ] A contact-sheet scan was done for decks ≥ 30 slides
- [ ] All five issue types (overflow, overlap, truncation, auto-shrink, drift) have been actively looked for, not just hoped about
- [ ] Any visible issues have been fixed and re-rendered
- [ ] No `???` or `TODO` markers remain anywhere
- [ ] `[FIGURE: ...]` placeholder textboxes are present where expected (per the figure summary table in `outline.md`) — these are intentional build aids, not unfinished content. See `images.md`.
- [ ] All embedded images (i.e., not placeholders) render correctly — no broken-image icons
