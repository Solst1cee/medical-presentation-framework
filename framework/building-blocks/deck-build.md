---
name: deck-build
description: "Building block for assembling PPTX decks — theme-selection flow, 9 reusable slide layouts, font/density conventions, and python-pptx + unpack/repack XML mechanics. Loaded by Read path from a presentation-type skill; not intended to auto-trigger on its own."
---

# Deck-build — flow for assembling a PPTX from an outline

## When this loads

Loaded by a presentation-type skill (`topic-review.md`, `journal-club.md`, `case-discussion.md`) at the build phase. The caller already has `Documents/Outline.md` finalised and is about to produce the first PPTX from it. This file describes the **flow** the caller runs through — theme selection, layout choice, build mode, QA — not a fixed institutional look.

---

## Step 1 — Ask the user about theme before generating anything

**Step 1a — Check the workspace's saved theme and template folders first.**

Before asking the user from scratch, look at what's already saved at the workspace root:

- `theme/` — markdown files defining the user's named palettes (one file per theme). See `theme/README.md` for format.
- `templates/` — institutional or personal PPTX templates the user has dropped in. See `templates/README.md`.

If either folder contains files, **list them to the user** and ask whether to use one before going through fresh kickoff questions. Suggested phrasing:

> *"I see `theme/Academic-Navy.md` saved at the workspace root. Want me to use it for this deck, or pick something else?"*

This saves time and keeps the user's preferred palettes / templates reusable across projects.

**Step 1b — If nothing's saved (or user wants something different), ask:**

1. **Do you have an existing PPTX template, brand palette, or institutional slide template you want to use?**
   - Yes, a `.pptx` template → use unpack/repack XML mode against that template (see Step 5). Match its existing colours, fonts, and footer. Don't reinvent them. Offer to save it to `templates/` for future re-use.
   - Yes, a colour palette → ask for the values (or whether to read them from a file). Offer to save to `theme/` for future re-use.
   - No → apply the academic default theme (Step 2).

2. **Is there an existing slide example (one you've made before, or a colleague's deck) you want me to mimic?**
   - Yes → ask for the file path. Read its theme constants (colours, font, header style) and apply them to the new deck.
   - No → continue to Step 2.

Never assume an institutional theme. Always ask, even after checking `theme/` and `templates/`.

---

## Step 2 — If using the academic default theme, confirm preferences

If the user has no existing template, apply the academic default and confirm three points:

### 2a. Primary accent colour

Ask: *"What primary accent colour would you like? I can suggest a few Pantone palettes commonly used in academic medicine, or you can give me a hex code if you have something in mind."*

Suggested palettes (offer the table; let the user pick one):

| Palette | Primary accent | Secondary accent | Feel |
|---|---|---|---|
| Academic navy | Pantone 533 C (deep navy, ~#1F3864) | Pantone 1797 C (warm red, ~#C04125) | Classic medicine-school |
| Forest | Pantone 5535 C (forest green, ~#1B4332) | Pantone 7411 C (amber, ~#D89F2A) | Surgical / oncology |
| Slate-blue | Pantone 540 C (deep blue, ~#003057) | Pantone 158 C (warm orange, ~#E87722) | Cardiology / ICU |
| Burgundy | Pantone 188 C (burgundy, ~#76232F) | Pantone 7501 C (cream, ~#DFCFB3) | Internal medicine, traditional |

Hex values above are approximations of the Pantone spot colours; verify against the live Pantone reference if exact brand-match matters.

### 2b. Background

Default to **white**. Only change if the user explicitly asks (e.g., light grey, off-white, or a dark theme for a research-only deck). Avoid black backgrounds for clinical content — projector contrast at the back of a lecture hall is unreliable.

### 2c. Font face

Default to **Calibri** — high readability on projectors, available on every Office install. Only change if the user supplies a brand font.

Once these three choices are confirmed, build the theme-constants block. **This block sits at the very top of every build script** — once filled in, every helper (`set_run`, `add_para`, `add_figure_with_caption`, etc.) pulls colours and font sizes from these names. Don't put inline hex codes or pt numbers anywhere else in the build code.

```python
# ===========================================================================
# FIRST-TIME SETUP — fill in once per project, then use these names everywhere.
#
# How to use this block:
#   1. Confirm theme palette with the user (Step 2a). Convert hex / Pantone
#      picks to RGBColor: e.g., navy #1F3864 → RGBColor(0x1F, 0x38, 0x64).
#      Fill in ACCENT_PRIMARY, ACCENT_SECONDARY, HIGHLIGHT_BG.
#   2. Confirm background (Step 2b). White is the default — change only if
#      the user explicitly requests a different background.
#   3. Confirm font face (Step 2c). Calibri is the default — change only if
#      a brand font is supplied. (Set inside set_run() helper below.)
#   4. Font sizes default to the Step 3 table values. Adjust only with a
#      specific reason — and update the Step 3 table comment so future
#      slides stay consistent.
# ===========================================================================

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# ── Slide geometry ─────────────────────────────────────────────────────────
# Widescreen 16:9 — universal for academic conferences.
SLIDE_W  = Inches(13.333)
SLIDE_H  = Inches(7.5)
HEADER_H = Inches(0.85)

# ── Theme colours (Step 2a + 2b) ───────────────────────────────────────────
# Fill in from the agreed palette. RGBColor takes hex bytes:
#   RGBColor(0x1F, 0x38, 0x64) for #1F3864 (a deep navy).
ACCENT_PRIMARY   = RGBColor(...)               # section dividers, body-text headings
ACCENT_SECONDARY = RGBColor(...)               # content-slide headers, key accents
HIGHLIGHT_BG     = RGBColor(...)               # pearl box fill — pick a light tint of ACCENT_SECONDARY

# Fixed defaults — leave alone unless the user has a specific reason.
BACKGROUND       = RGBColor(0xFF, 0xFF, 0xFF)  # slide background; white default
WHITE            = RGBColor(0xFF, 0xFF, 0xFF)  # for white text on dark fills
GRAY_DARK        = RGBColor(0x33, 0x33, 0x33)  # body text
GRAY_MED         = RGBColor(0x66, 0x66, 0x66)  # captions, references, footer
GRAY_LIGHT       = RGBColor(0xE0, 0xE0, 0xE0)  # separator lines

# ── Font sizes (Step 3 table values) ───────────────────────────────────────
# Integer pt values. Pt() conversion is applied by set_run() — pass these
# constants directly: e.g., size=BODY_SIZE, NOT size=Pt(BODY_SIZE).
TITLE_SIZE        = 44   # title slide topic
TITLE_SUBTITLE    = 24   # title slide subtitle (italic)
TITLE_FOOTER      = 15   # title slide presenter / date / institution
SECTION_SIZE      = 46   # section divider title
SECTION_SUBTITLE  = 20   # section divider subtitle (italic)
HEADER_SIZE       = 26   # content-slide header bar (bold white) — projection-ready
SUBTITLE_SIZE     = 16   # content-slide italic subtitle (16 floor)
BODY_SIZE         = 18   # content-slide bullets — **projection floor; do not drop below 16**
SUBSECTION_SIZE   = 19   # bold subsection labels
TABLE_HEADER_SIZE = 18   # table header row
TABLE_BODY_SIZE   = 16   # table body cells (14–16 range; 14 is the floor for dense tables)
QUADRANT_SIZE     = 15   # 4-quadrant bullets (14–16 range)
STAT_BIG_SIZE     = 40   # stat callout big numbers (34–50 range)
STAT_CAPTION_SIZE = 13   # stat callout caption (12–13 range)
PEARL_SIZE        = 16   # pearl box body (italic)
CAPTION_SIZE      = 10   # image caption (10–11 range)
PLACEHOLDER_SIZE  = 14   # image placeholder textbox (build aid)
REF_SIZE          = 10   # on-slide reference line (intentionally small)
FOOTER_SIZE       = 10   # bottom-of-slide footer
```

**Setup checklist** (before generating any slides, confirm):

- [ ] `ACCENT_PRIMARY` filled in from the agreed palette (Step 2a)
- [ ] `ACCENT_SECONDARY` filled in
- [ ] `HIGHLIGHT_BG` filled in — a light tint of `ACCENT_SECONDARY` (e.g., for a red accent, a cream-pink such as `RGBColor(0xFA, 0xF0, 0xEC)`)
- [ ] `BACKGROUND` confirmed (white default; change only if requested in Step 2b)
- [ ] Font face confirmed in `set_run()` default (Calibri default; change only for a brand font in Step 2c)
- [ ] Font sizes left at the Step 3 defaults unless the user has a specific reason to deviate

Once this block is filled in, downstream code uses **names only** — never inline RGB or pt values. If a slide later needs a colour or size you didn't declare, add it here, then reference it by name.

---

## Step 3 — Font sizes (intentionally larger than typical defaults)

Past presentations used sizes that turned out to be too small to read from the back of a real lecture hall. The defaults below are bigger by ~2 pt across the board, except references — which can stay small because they're long text and not constantly viewed during the talk.

| Slide element | Size | Notes |
|---|---|---|
| Title slide title | **44 pt bold** | Two lines max |
| Title slide subtitle | **24 pt italic** | E.g., "A [Department] Topic Review" |
| Title slide footer (presenter/date) | **15 pt** | Two lines if needed |
| Section divider title | **46 pt bold** | "SECTION N" line + topic line |
| Section divider subtitle | **20 pt italic** | |
| Content slide header | **26 pt bold white** | Inside the accent header bar — projection-ready |
| Content slide subtitle | **16 pt italic** | Optional |
| Content slide body bullets | **18 pt (16 pt floor)** | 6–10 bullets per slide; do not drop below 16 |
| Content slide subsection labels | **19 pt bold** | In ACCENT_PRIMARY |
| Table header row | **18 pt bold white** | On ACCENT_PRIMARY fill |
| Table body rows | **16 pt (14 pt floor for dense tables)** | Alternate white / faint tint |
| 4-quadrant body bullets | **15 pt (14 pt floor)** | Higher density allowed |
| Stat callout big number | **34–50 pt bold** | On a contrasting fill |
| Stat callout caption | **12–13 pt italic** | Below the number |
| Pearl box body | **16 pt italic** | Bold "Pearl:" prefix |
| Image caption | **10–11 pt italic gray-med** | Author + year + PMC ID + license |
| Image placeholder textbox (build aid) | **14 pt italic gray-med** | Dashed thin border; readable from slide-sorter view; replaced by real image during user review (see `images.md`) |
| **References** | **10 pt** | Intentionally small — long, dense text, not for reading during the talk |
| Footer | **10 pt gray-med** | Institution name or course title |

Body content area: `y` from ~1.15 in to ~6.45 in. Reference area: `y` from ~6.50 in to ~7.15 in. Footer: `y` ~7.22 in.

---

## Step 4 — The 9 reusable slide layouts

These nine patterns cover every kind of slide a topic review / journal club / case discussion needs. Each is described in theme-agnostic terms — drop in the user's `ACCENT_PRIMARY` / `ACCENT_SECONDARY` from Step 2.

### Pattern 1 — Title slide

```
+----------------------------------------------------------+
| [ACCENT_PRIMARY band — top 2.3 in, full width]            |
+----------------------------------------------------------+
| [Thin ACCENT_SECONDARY accent line]                       |
+----------------------------------------------------------+
|  Topic Title — Line 1                  (44 pt bold,       |
|  Topic Title — Line 2                   ACCENT_PRIMARY)   |
|                                                           |
|  A [Department] Topic Review           (24 pt italic,     |
|                                         ACCENT_SECONDARY) |
|                                                           |
|  Footer: institution / division        (15 pt gray-dark)  |
|                                                           |
|  Presenter: [name]    Date: [date]     (15 pt gray-med)   |
+----------------------------------------------------------+
```

### Pattern 2 — Section divider

```
+----------------------------------------------------------+
| [Full ACCENT_PRIMARY background]                          |
|                                                           |
|  SECTION N                              (46 pt bold white)|
|  ─────                                  (ACCENT_SECONDARY |
|  [Section topic]                         decorative bar)  |
|                                         (20 pt italic     |
|                                          accent-tint)     |
+----------------------------------------------------------+
```

One section divider per major section. **5–7 sections** is a healthy upper bound for a topic review.

### Pattern 3 — Standard content slide

```
+----------------------------------------------------------+
| [ACCENT_SECONDARY header bar — full width, 0.85 in tall]  |
| Slide title (26 pt bold white, left-aligned)              |
+----------------------------------------------------------+
| Optional italic subtitle (16 pt gray-med)                 |
|                                                           |
| Subsection label (19 pt bold, ACCENT_PRIMARY)             |
| - bullet (18 pt, gray-dark; 16 pt floor)                  |
| - bullet                                                  |
|                                                           |
| Subsection label                                          |
| - bullet                                                  |
| - bullet with [bold ACCENT_SECONDARY] keyword             |
|                                                           |
| [Optional pearl box at bottom]                            |
+--- thin GRAY_LIGHT rule ----------------------------------+
| Refs: 1. [Vancouver citation] (10 pt italic gray-med)     |
|       5. [...]                                             |
+----------------------------------------------------------+
| Footer (10 pt gray-med)                                   |
+----------------------------------------------------------+
```

### Pattern 4 — Table slide

Tables built as native PPTX shapes (not text-frame "tables") render more cleanly:

- Header row: **ACCENT_PRIMARY fill, white 18 pt bold**
- Body rows alternate **white** and **light tint** of ACCENT_PRIMARY (use the colour at ~5% saturation, e.g. `#F5F7FB` for a navy palette)
- First column **bold ACCENT_PRIMARY italic** when it's a category label
- Other columns gray-dark, regular
- Cell padding ~0.1 in left/right; vertical anchor middle

**python-pptx gotcha — vertical anchor on table cells:**

```python
# WRONG — silently no-op. Writes <a:bodyPr anchor="ctr"/> into the text frame,
# but PowerPoint reads cell vertical alignment from <a:tcPr anchor="ctr"/>.
cell.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

# RIGHT — sets the cell's tcPr/@anchor attribute, which PowerPoint honors.
cell.vertical_anchor = MSO_ANCHOR.MIDDLE
```

Apply `cell.vertical_anchor = MSO_ANCHOR.MIDDLE` to **every** cell (header + body) in the table-building helper. This is a recurring confusion because shape text frames DO honor `text_frame.vertical_anchor`; only table cells need the cell-level attribute.

### Reference-line textbox — dynamic sizing anchored to slide bottom

Don't use a fixed-height ref textbox. A 1-ref slide and a 6-ref slide need very different vertical space; a fixed-tall textbox wastes space on the former and crowds body content on every slide.

Pattern: **calculate height from ref count + wrap estimate, then anchor to slide bottom.**

```python
def ref_line(slide, ref_nums, prefix=""):
    sorted_refs = sorted(set(ref_nums))
    lines = ([prefix] if prefix else []) + [CITES[n] for n in sorted_refs if n in CITES]

    # At 9 pt italic Calibri across ~12.5" usable width, ~110 chars fit per line.
    CHARS_PER_LINE = 110
    LINE_H_IN = 0.18
    SPACE_BETWEEN_PARAS_IN = 0.02

    total_lines = 0
    for text in lines:
        wraps = max(1, -(-len(text) // CHARS_PER_LINE))  # ceil division
        total_lines += wraps
    h_in = total_lines * LINE_H_IN + max(0, len(lines) - 1) * SPACE_BETWEEN_PARAS_IN + 0.04
    h_in = max(0.22, h_in)  # floor for single-line case

    BOTTOM_MARGIN_IN = 0.08
    ref_h = Inches(h_in)
    ref_y = SLIDE_H - ref_h - Inches(BOTTOM_MARGIN_IN)

    tb = slide.shapes.add_textbox(Inches(0.4), ref_y, SLIDE_W - Inches(0.8), ref_h)
    tf = tb.text_frame
    tf.margin_top = Emu(0); tf.margin_bottom = Emu(0)
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.BOTTOM  # text flush with bottom of textbox

    for i, text in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if i > 0: p.space_before = Pt(1)
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        set_run(r, text, size=9, italic=True, color=GRAY_MED)
```

The body of each slide's build function uses fixed y-positions for content as before — but doesn't need to reserve a fixed bottom margin for refs. The dynamic ref box only grows upward into the body area when there are many refs.

### Pattern 5 — 4-quadrant Diagnosis & Treatment (workhorse)

For any disease syndrome with substantial diagnostic and treatment content:

```
+----------------------------------------------------------+
| Header: "[Syndrome] — Diagnosis & Treatment"              |
+----------------------------------------------------------+
| Optional subtitle / cross-references                      |
+--------------------------+-------------------------------+
| Imaging                  | Microbiology                  |
| (ACCENT_PRIMARY strip)   | (ACCENT_PRIMARY strip)        |
| - findings 1             | - specimen 1                  |
| - findings 2             | - yield numbers               |
| - findings 3             | - special conditions          |
+--------------------------+-------------------------------+
| Histopathology           | Treatment                     |
| (ACCENT_PRIMARY strip)   | (ACCENT_SECONDARY strip)      |
| - granuloma type         | - surgical role               |
| - special stains         | - drug regimen 1              |
| - caveats                | - drug regimen 2              |
+--------------------------+-------------------------------+
| Refs: 1, 5, 12, 14 (Vancouver-numbered)                   |
+----------------------------------------------------------+
```

Each quadrant ~6 in × 2.55 in. **15 pt bullets (14 pt floor)**. The Treatment quadrant uses the **secondary accent** for its header strip to visually separate it from the diagnostic quadrants.

### Pattern 6 — Stat callouts

For high-impact numbers (cohort outcomes, prevalence stats):

```
Single big stat:
+--------------------------------+
|         36.4%                  |  (34–50 pt bold, white on ACCENT_PRIMARY)
|  of cases were culture-        |  (12–13 pt italic, white)
|  negative on routine workup    |
+--------------------------------+

Triple stat row (outcomes):
+----------+----------+----------+
|   46%    |   29%    |   3.6%   |  (34–40 pt bold)
| Complete | Residual | Mortality|  (12 pt italic)
| recovery | disability|         |
+----------+----------+----------+
  green      amber       red       ← 2.5 pt border, valence-coded
```

For outcome triples: green = good, amber = partial, red = bad. Use sparingly — at most one stat-callout slide per major section.

### Pattern 7 — Pearl box

```
+--------------------------------------------+
| Pearl: [single-sentence clinical rule]     |
|        HIGHLIGHT_BG fill, ACCENT_SECONDARY |
|        border, 16 pt italic body,          |
|        bold "Pearl:" prefix                |
+--------------------------------------------+
```

Use sparingly — **at most one per slide**. If the pearl is a warning, use a dark red border instead of the normal accent border and prefix with `⚠ Pearl:`.

### Pattern 8 — Image slide with caption

```
+----------------------------------------------------------+
| Header: "[Modality] — [Specific finding]"                 |
+----------------------------------------------------------+
| Body text on left side (50% width)             [Image]   |
| - finding 1                                    [       ] |
| - finding 2                                    [       ] |
| - finding 3                                    [       ] |
|                                                           |
|                            Caption: brief italic          |
|                            description from source paper, |
|                            10–11 pt gray-med              |
|                            (Author Year, PMC ID, license) |
+----------------------------------------------------------+
| Refs                                                      |
+----------------------------------------------------------+
```

For a 2×2 image gallery, drop the body text and use a **2-column × 2-row grid**, each image ~5.88 in × 1.85 in with a 0.55 in caption strip below.

### Pattern 9 — References slides

For decks with 25+ references, split across 2 slides. Simple list, no decoration:

```
+----------------------------------------------------------+
| Header: "References (1/2) — Vancouver Style"              |
+----------------------------------------------------------+
| Textbooks (15 pt bold ACCENT_PRIMARY)                     |
| 1. [full Vancouver citation, 10 pt gray-dark]             |
| 2. [...]                                                  |
|                                                           |
| Guidelines (15 pt bold ACCENT_PRIMARY)                    |
| 5. [...]                                                  |
|                                                           |
| Primary literature (1/2) (15 pt bold ACCENT_PRIMARY)      |
| 8. [...]                                                  |
+----------------------------------------------------------+
```

References at 10 pt is deliberate — they're long, they're for the audience to consult after the talk, and shrinking them keeps the slide uncluttered.

---

## Step 5 — Build modes

Two build modes are supported. Pick based on what input you have:

| Input | Mode | Approach |
|---|---|---|
| No existing template — building from scratch | **python-pptx mode** | Open a new `Presentation()`, add slides with `slide_layouts[]`, build shapes with helpers. Save with `prs.save()`. |
| Existing PPTX (user's template, colleague's deck) — must preserve their slides | **unpack/repack XML mode** | `unpack.py` → write raw slide XML strings → `pack.py`. Append new slides without disturbing existing slide IDs. |

### python-pptx mode — primary

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

def set_run(run, text, *, size=BODY_SIZE, bold=False, italic=False, color=None, font="Calibri"):
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color

def add_textbox(slide, x, y, w, h, *, anchor="t"):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    return tf

def add_para(tf, text, *, size=BODY_SIZE, bold=False, italic=False, color=None, align=None, indent=0):
    p = tf.paragraphs[0] if not tf.paragraphs[0].text else tf.add_paragraph()
    if align: p.alignment = align
    if indent: p.level = indent
    set_run(p.add_run(), text, size=size, bold=bold, italic=italic, color=color)
    return p

def add_figure_with_caption(slide, image_path, x, y, w, h, caption):
    """Embed image at original aspect ratio (resized to w×h) and add caption below."""
    slide.shapes.add_picture(image_path, x, y, width=w, height=h)
    cap_y = y + h
    cap_box = slide.shapes.add_textbox(x, cap_y, w, Inches(0.55))
    tf = cap_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    set_run(p.add_run(), caption, size=CAPTION_SIZE, italic=True, color=GRAY_MED)
```

Note: helper defaults like `size=BODY_SIZE` reflect the Step 3 font-size constants. Pass any of the named size constants from Step 2 (TITLE_SIZE, HEADER_SIZE, CAPTION_SIZE, REF_SIZE, etc.) instead of inline integers.

### unpack/repack XML mode — for shared / institutional templates

For inserting new slides into a user-provided template without touching their existing slides:

```bash
python mnt/.claude/framework/pptx/scripts/office/unpack.py "Main/file.pptx" unpacked/
# Find insertion point in presentation.xml → <p:sldIdLst>
# START_SLIDE_NUM = [last slide file number] + 1
# START_SLIDE_ID  = [last sldId number] + 1
# START_RID       = [last rId in presentation.xml.rels] + 1
```

Measure the template's EMU constants (logo position, header bar height) from one of its existing slides before generating XML — never assume; institutional templates vary.

Core XML helpers (literal XML strings, not python-pptx objects):

```python
def X(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def hdr(title, eid=2, bar_h=763995, slide_w=12192000):
    return f'''  <p:sp><p:nvSpPr><p:cNvPr id="{eid}" name="hdr"/><p:cNvSpPr>
      <a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>
    <p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{slide_w}" cy="{bar_h}"/></a:xfrm>
      <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
      <a:solidFill><a:schemeClr val="accent1"><a:lumMod val="50000"/></a:schemeClr></a:solidFill>
    </p:spPr>
    <p:txBody><a:bodyPr anchor="ctr"/><a:lstStyle/>
      <a:p><a:pPr algn="ctr"/><a:r><a:rPr lang="en-US" sz="2800" b="1" dirty="0">
        <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:rPr>
        <a:t>{X(title)}</a:t></a:r></a:p></p:txBody></p:sp>'''
# sz="2800" = 28 pt (XML uses hundredths of a point); adjust per template.

def wrap_slide(body, notes=None):
    NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
          'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')
    notes_xml = ""
    if notes:
        notes_xml = f'''  <p:notes><p:cSld><p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>
        <a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      <p:sp><p:nvSpPr><p:cNvPr id="2" name="Notes"/><p:cNvSpPr>
        <a:spLocks noGrp="1"/></p:cNvSpPr>
        <p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr>
        <p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>
          <a:p><a:r><a:rPr lang="en-US" dirty="0"/>
            <a:t>{X(notes)}</a:t></a:r></a:p>
        </p:txBody></p:sp>
    </p:spTree></p:cSld></p:notes>'''
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld {NS}>
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>
      <a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
{body}
  </p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>{notes_xml}
</p:sld>'''
```

Pack with the standard helper:

```bash
python mnt/.claude/framework/pptx/scripts/clean.py unpacked/
python mnt/.claude/framework/pptx/scripts/office/pack.py \
    unpacked/ "Main/Topic review_[TOPIC].pptx" \
    --original "Main/Topic review.pptx"
```

### XML mode pitfalls

| Pitfall | Fix |
|---|---|
| Multiple bullets in one `<a:p>` | One `<a:p>` per bullet |
| Leading/trailing spaces vanish | `xml:space="preserve"` on `<a:t>` |
| Raw bullet character `•` | `<a:buChar char="&#x2022;"/>` in `<a:pPr>` |
| Smart quotes break XML | `&#x201C;` `&#x201D;` `&#x2018;` `&#x2019;` |
| Namespace corruption | Use `defusedxml.minidom`, not `xml.etree.ElementTree` |
| Missing `[Content_Types].xml` entry | PPTX fails to open |
| rId conflicts | Inspect existing `presentation.xml.rels` first; rId order varies per template |
| PNG not registered | Add `<Default Extension="png" ContentType="image/png"/>` |

---

## Step 6 — QA + safety

After the first build pass, before showing the user:

- Visual QA — see `visual-qa.md`. Render to PDF, convert to PNG thumbnails, inspect 4–6 representative slides for overflow, overlap, contrast.
- Before any rebuild that touches an existing finalised deck — see `safe-file-operations.md`. Backup first; never overwrite a "Final" file.

---

## Step 7 — Post-review iteration

After the first deck is built and the user has reviewed it, expect edit requests. Two distinct scenarios — handle them differently. **Default behaviour: never rebuild the whole deck unless the user explicitly asks for it.** Once the user has the deck in hand, they may have started editing slides directly; a full rebuild would silently overwrite that work.

### Source-of-truth lifecycle

Outline and deck are both live working files, but only one is canonical at any moment. The transition is driven by user action, never inferred automatically:

- **Phase A — outline drafting:** outline is the sole source of truth; the deck does not yet exist.
- **Phase B — first build:** outline drives the deck. If they disagree, the outline wins; the deck is regenerated.
- **Phase C — user reviewing or hand-editing the deck:** both files are live. Every slide-level edit triggers the Scenario B prompt below ("should I update the outline to match?"). If the user declines, the divergence is noted explicitly — either on the slide's `Ref:` comment or in a short "outline-deck divergences" block at the bottom of the outline — so a later rebuild does not silently revert the edit.
- **Phase D — finalised:** the deck is the delivered artifact. The outline is either kept in sync (for archival or future rebuild) or explicitly marked "historical — superseded by deck v Final."

Reconciliation between outline and deck is always an explicit, user-confirmed step. There is no automatic switchover at visual QA or at any other build stage.

### Scenario A — User edited `outline.md` after the deck was built

The outline changed; the deck hasn't been regenerated yet. The user wants the new outline content reflected in the deck, but they likely have direct-in-deck edits on other sections they want to keep.

**Default workflow: build standalone section PPTXs for only the edited sections** — do not rebuild the whole deck.

1. Ask: *"Which sections did you edit in the outline? I'll rebuild just those."* If the user can't list them, ask them to point to the section headers in `{Topic} outline.md` (e.g., "Section 3 — Diagnostic algorithm").
2. Generate a standalone PPTX for each edited section. Naming convention: `{Topic} {section short name} v{N}.pptx` — e.g., `Hyponatremia treatment v2.pptx`, `Hyponatremia diagnostic-algorithm v2.pptx`. Save into `Build_archive/Section_PPTXs/`.
3. Each standalone section PPTX contains only the slides for that section, theme-matched to the master deck.
4. The user imports the section slides into their working master deck themselves (drag-drop in PowerPoint or "Reuse Slides").
5. **Do not modify the master deck file.** That's the user's working copy with their direct edits.

Token-efficiency benefit: only the changed sections are rebuilt, not the whole deck.

### Scenario B — User asks to edit a slide directly in the deck

The user says something like *"change slide 14 to say X"* or *"swap the figure on slide 22"*. They want a direct slide-level edit.

1. Apply `safe-file-operations.md` if the deck filename includes "Final" / "finalised" / "presented" / "important" — backup first; write the new version to a different filename for the user to verify.
2. Make the slide-level edit.
3. **Ask: *"Should I also update `{Topic} outline.md` to match?"*** The outline is the source of truth for any future rebuild — leaving it stale means the next regeneration will silently revert the user's slide-level edit.
4. If the user says yes, update the corresponding entry in `outline.md` (bullets, `Ref:` line, figure placeholder) to mirror the slide change. Both stay in sync.
5. If the user says no, note the divergence explicitly: *"Heads up — your outline still says X for slide 14; the deck now says Y. Any future rebuild from outline will revert this change."*

### When a full rebuild is appropriate

Replace the whole deck only when:

- The user **explicitly asks** for a from-scratch rebuild.
- The deck has not yet been finalised AND the user confirms they have no direct-in-deck edits to preserve.
- A build-script-level change affects every slide (theme migration, font-size update, layout-pattern overhaul) — and the user has been told what will change.

In every other case, prefer Scenario A's section-PPTX approach.

---

## Layout density guidelines (quick reference)

| Slide type | Body text size | Bullets | Notes |
|---|---|---|---|
| Title | 44 pt | n/a | Uncluttered |
| Section divider | 46 pt | n/a | Just title + subtitle |
| Standard content | 18 pt (16 floor) | 6–10 bullets | Use bold subsections |
| 4-quadrant dx/tx | 15 pt (14 floor) | 4–6 per quadrant | Higher density allowed |
| Table | 16 pt (14 floor) | 4–7 rows | Header in ACCENT_PRIMARY |
| Image | 15–16 pt | 4–6 bullets | Image ~5 in wide |
| References | 10 pt | 12–14 entries per slide | Simple list |

---

## Anti-patterns to avoid

- **Inline references in every sentence** — put a single reference line at the bottom of the slide instead.
- **Over-using pearl boxes** — one per slide maximum; otherwise they lose impact.
- **Inconsistent table styling** — pick one header colour, one row-stripe pattern, stick with it.
- **Different fonts on different slides** — one font (Calibri by default), one weight scheme.
- **Over-bolding** — bold should mark *the* key term in a sentence, not multiple terms.
- **Long captions** — image captions stay 2–3 lines max; longer text goes in the body.
- **Missing license info on figures** — every embedded image shows source paper + license. See `images.md`.
- **Slipping to smaller fonts to fit more content** — if it doesn't fit at the Step 3 sizes, split the slide. Don't shrink to compensate.

---

## Build-process notes

When generating slides programmatically:

1. **Define theme constants once at the top** of the build script. Don't sprinkle hex codes through the file.
2. **Build helper functions** — `add_header`, `add_textbox`, `add_para`, `add_slide_refs`, `add_image_caption`. Don't inline the same XML or python-pptx call 50 times.
3. **Watch for null-byte truncation** — large Python build scripts with many string literals occasionally truncate during concurrent edits. Verify file integrity (`hexdump -C | grep "00 00"`) before running. Append the missing tail if needed.
4. **Visual QA every build** — render to PDF, convert to PNG thumbnails, inspect 4–6 representative slides. See `visual-qa.md`.
5. **Standalone section PPTXs for post-review edits** — when the user is iterating on a built deck and asks for an updated section, build a standalone section PPTX they can import; don't rebuild the whole master deck. Full workflow in Step 7 above.
6. **Apply `safe-file-operations.md` before any rebuild that touches an existing finalised deck.**

---

## Self-check before declaring the deck visually consistent

- [ ] One title slide, one or more section dividers, consistent content-slide headers throughout
- [ ] One font face across every slide (Calibri or the user-supplied brand font)
- [ ] Step 3 font sizes applied — body bullets at 16–18 pt, not shrunk to fit
- [ ] Reference line at the bottom of every content slide (10 pt italic gray-med)
- [ ] Image captions include paper-derived description + source attribution + license
- [ ] Pearl boxes used sparingly (≤ 1 per slide)
- [ ] No slide is more than ~90% full of text (leave breathing room)
- [ ] Theme constants matched across all slides — no slide drifts to a differen