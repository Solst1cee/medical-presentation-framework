---
name: images
description: "Building block for medical figure handling in presentations — default placeholder policy, PubMed Central (PMC) sourcing workflow, CC-BY / CC-BY-NC license verification, paper-derived caption format, and embedding mechanics. Loaded by Read path from a presentation-type skill; not intended to auto-trigger on its own."
---

# Medical figures — default policy and sourcing workflow

## Why this matters

A medical presentation without real images is a wall of bullet points. But pulling images at random from the web carries copyright risk, license-violation risk, and reputational risk. This file covers two things: the **default policy** for how images get into the deck (usually as placeholders, with the user inserting the real figures during review), and the **full sourcing workflow** for the cases where Claude is asked to find and place images directly.

---

## Default policy — placeholders first, not automated sourcing

**Default behaviour: Claude does NOT source, crop, or place images automatically.** Past attempts at automated cropping produced poorly-framed figures with clipped key findings. The user typically wants to insert real images themselves during deck review. The default flow is:

1. **Placeholder textboxes on every slide that needs an image.** Each placeholder describes the intended figure (modality, body part, finding, candidate source paper, license to verify). The user inserts the actual image themselves during deck review. See the placeholder format below.
2. **If the user has placed image files in `Sources/Figures/`**, Claude embeds them at **original aspect ratio (no cropping; resizing is fine)** and positions them simply. The user fine-tunes placement when reviewing the deck.
3. **Full PMC sourcing workflow (Phases 1–7 below) runs only when the user explicitly asks** Claude to source and place images directly.

Whenever an image *is* embedded — whether from `Sources/Figures/` or sourced via Phases 1–7 — the license + caption discipline (PMC ID, license name, paper-derived caption) still applies.

This policy is invoked from `topic-review.md` Phase 5 and any other presentation-type skill that handles figures. Keep this file's default behaviour aligned with those.

---

## Placeholder format

On a slide that needs an image, insert a **dashed-border textbox** where the image will go, sized roughly to the intended image area. The textbox content:

```
[FIGURE: {modality} {body part} — {specific finding}]
Candidate: {Author Year, PMC ID, license} (verify license at source)
User to source and insert.
```

Examples of well-formed placeholders:

```
[FIGURE: Axial T2 MRI of the wrist — rice bodies in flexor tenosynovitis]
Candidate: Yang et al. 2016, PMC10323524, CC-BY (verify license at source)
User to source and insert.

[FIGURE: Sagittal T2 MRI lumbar spine — paraspinal abscess in vertebral osteomyelitis]
Candidate: not pre-identified — user to source.

[FIGURE: Clinical photograph — sporotrichoid skin lesions on the forearm]
User to source and insert.
```

Placeholder textbox — structural conventions (styling lives in `deck-build.md`):

- **Border:** dashed thin border so it's visually distinct from real slide content.
- **Position and size:** place at the exact spot and dimensions the final image should occupy.
- **Font, size, colour:** per `deck-build.md` Step 3 (image-placeholder-textbox row of the font-size table). Don't restate sizes or colours here — they're theme-driven.

The placeholder ensures the user knows exactly what to insert, where to insert it, and which paper to credit — without anyone having to remember the slide-by-slide plan later.

---

## Figure summary table — outline.md build aid

At the bottom of `{Topic} outline.md`, maintain a **figure summary table** listing every figure planned for the deck. This is a **build aid for the outline only — it never gets copied into a slide**. Its purpose is to give the user a single view of which figures are sourced, which are placeholders, which still need work, and where each one came from (or should come from).

Place it under an explicit build-aid section header so anyone (human or Claude) reading the outline can see it's not deck content:

```
## Build aids — not for slides

### Figure summary

| Slide | Figure description | Status | Source & action for user |
|---|---|---|---|
| 8 | MRI wrist — rice bodies in flexor tenosynovitis | placeholder | Candidate: Yang 2016, PMC10323524 (CC-BY). User to download from PMC. |
| 12 | Sagittal MRI lumbar spine — paraspinal abscess | placeholder | No open-access candidate identified — user to source manually or recreate. |
| 15 | Clinical photo — sporotrichoid forearm lesions | in `Sources/Figures/` | File: `sporotrichoid_photo.jpg`; embedded at original aspect ratio. |
| 18 | Histopathology H&E — granulomatous inflammation | placeholder | Candidate: Lee 2019, PMC9876543 — **verify CC-BY-NC license at source first**. |
| 22 | Plain film knee AP — chondrocalcinosis | not yet placed | No candidate identified — consider recreating as PowerPoint diagram. |
```

### Column definitions

- **Slide** — slide number from the outline. Update if slide numbers shift.
- **Figure description** — one-line description of what the image must show. Match the placeholder textbox content where possible.
- **Status** — one of:
  - `placeholder` — slide has a labelled placeholder textbox; image not yet inserted
  - `in Sources/Figures/` — user has provided the file; embedded at original aspect ratio
  - `not yet placed` — no candidate identified yet; needs user decision (search, recreate, or drop)
- **Source & action for user** — concrete next step. Who needs to do something, and what.

### Update cadence

- Add a row when a slide gets a figure placeholder during outline drafting.
- Update status to `in Sources/Figures/` once the user supplies the file.
- Revise if a candidate paper is later identified, rejected, or replaced.
- Keep the table in sync with the actual deck through visual QA. The table itself is build metadata; once a slide image is placed and captioned, the slide is the canonical record of that figure, and the table just tracks status. For outline-vs-deck content sync more broadly, see `deck-build.md` Step 7 ("Source-of-truth lifecycle").

### Why this table never goes into the deck

It's working metadata for the build process, not content for the audience. Keeping it under the `## Build aids — not for slides` header — alongside the sources summary table (see `references.md`) — makes the boundary obvious to anyone moving content from `outline.md` into slides.

---

## When the user provides images in `Sources/Figures/`

If the user has already collected image files (downloaded from PMC, scanned from a textbook they own, supplied by a colleague), and put them in `Sources/Figures/`:

1. Inspect the filename — the user typically names files descriptively (e.g., `MRI wrist rice bodies.jpg`).
2. Confirm with the user **which file goes on which slide** before embedding. Don't guess from filenames alone if there's any ambiguity.
3. Embed at **original aspect ratio**. Resize if needed to fit the slide layout; **do not crop**. The user can re-crop during deck review if they want.
4. Add the standard caption + license note below the image (see Caption format below). The user supplies the citation if it isn't in the filename or paper PDF.

If a user-supplied image has no license info, ask before embedding — the user may know it's from a textbook they own (educational fair use considerations) or from a colleague (permission considerations).

---

## Full sourcing workflow — Phases 1 to 7

The phases below apply only when the user explicitly asks Claude to source and place images. Skip if the default placeholder flow is being used.

### Phase 1 — Identify what figure each slide needs

During outline drafting, mark **figure placeholders** explicitly. Each placeholder specifies:

- **Modality** (plain film / MRI / CT / US / clinical photo / histopathology / electron microscopy / gross specimen)
- **Body part** if applicable
- **Specific finding** the image must demonstrate
- **Disease or organism context**

Example placeholders for a few different topics:

```
[FIGURE: Axial T2 MRI of the wrist — rice bodies in flexor tenosynovitis]
[FIGURE: Sagittal T2 MRI lumbar spine — paraspinal abscess in vertebral osteomyelitis]
[FIGURE: Plain film knee AP — chondrocalcinosis in CPPD]
[FIGURE: Light microscopy renal biopsy H&E — crescentic glomerulonephritis]
[FIGURE: CT chest contrast — bilateral pulmonary nodules with cavitation]
[FIGURE: Clinical photograph — palpable purpura of the lower extremities]
```

### Phase 2 — PMC search workflow

Search PubMed Central (PMC) for open-access papers with relevant figures.

#### Search query pattern

```
[disease/organism] [body part/modality] [specific finding] open access PMC case report figure
```

Example queries that work well:

```
"Mycobacterium marinum" tenosynovitis hand wrist MRI rice bodies open access PMC
"chondrocalcinosis" knee plain film calcification open access PMC
"crescentic glomerulonephritis" renal biopsy H&E light microscopy open access PMC
"vertebral osteomyelitis" sagittal MRI paraspinal abscess PMC
"granulomatosis with polyangiitis" CT chest cavitary nodule open access PMC
```

#### Triage candidates

For each candidate paper, check:

1. **Is it open access?** PMC papers are mostly OA, but verify the article page directly.
2. **Does the figure actually show what you need?** Read the paper's figure legend — don't infer from the thumbnail.
3. **Is the clinical context relevant?** A figure from a context matching your case (immune status, age group, disease subtype) is preferred over a generic one.
4. **License?** Look for CC-BY, CC-BY-NC, CC-BY-NC-ND at the article footer.
5. **Quality?** High-resolution panels are better than low-res screenshots.

### Phase 3 — License verification

Open-access doesn't always mean free-to-use. The common licenses:

| License | Allows reproduction | Allows modification | Commercial use | Caveats |
|---|---|---|---|---|
| **CC-BY 4.0** | Yes, with attribution | Yes | Yes | Most permissive — preferred |
| **CC-BY-NC 4.0** | Yes, with attribution | Yes | No (non-commercial only) | Educational presentations qualify as non-commercial |
| **CC-BY-NC-ND 4.0** | Yes, with attribution | **No modification** | No | Cannot crop or annotate substantially |
| **PMC freely available, no CC license** | Variable | Variable | Variable | Check the journal's policy directly |
| **Author's own work, no license stated** | Permission required | Permission required | Permission required | Email the corresponding author |

For an **educational, non-commercial academic conference** presentation (the typical use case for this framework), **CC-BY and CC-BY-NC are both acceptable**. **CC-BY-NC-ND** is acceptable only if you embed the figure unaltered — no cropping, no annotation overlay.

### Phase 4 — Caption format

Every embedded image gets a **paper-derived caption** plus **source attribution and license** rendered below the figure (styling per `deck-build.md` Step 3, image-caption row):

```
[Image]
Axial T2 MRI: large fluid collection with multiple rice bodies along the
flexor tendon of the 3rd finger, with diffuse synovial thickening and
enhancement. M. intracellulare tenosynovitis. (PMC10323524, CC-BY)
```

#### Caption content rules

1. **Describe what the figure shows** — not what the disease is. ("Sagittal T2 with paraspinal abscess" rather than "MAC vertebral osteomyelitis")
2. **Add the diagnostic context briefly** — one phrase
3. **Include source attribution** — `(Author Year, PMC ID, license)` or `(Source paper citation)`
4. **Keep it short** — 2–3 lines max

#### Caption placement (structural — styling lives in `deck-build.md`)

- **Position:** directly below the image, inside the body content area.
- **Width:** matches the image width.
- **Alignment:** centred for a single-line caption; left-aligned for multi-line.
- **Font, size, colour:** per `deck-build.md` Step 3 (image-caption row of the font-size table). Don't restate sizes or colours here — they're theme-driven.

### Phase 5 — Build-time embedding

In python-pptx (assumes theme constants and helpers from `deck-build.md`):

```python
def add_figure_with_caption(slide, image_path, x, y, w, h, caption):
    """Embed image at original aspect ratio (resized to w×h) and add caption below.
    Caption size / colour come from the theme — see deck-build.md Step 3."""
    slide.shapes.add_picture(image_path, x, y, width=w, height=h)
    cap_y = y + h
    cap_box = slide.shapes.add_textbox(x, cap_y, w, Inches(0.55))
    tf = cap_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    # CAPTION_SIZE and GRAY_MED come from the theme constants block at the top
    # of the build script (see deck-build.md Step 2 / Step 3).
    set_run(p.add_run(), caption, size=CAPTION_SIZE, italic=True, color=GRAY_MED)
```

Place captions **inside the body content area, above the reference line at y≈6.50 in**. Keep image height ≤ 5 in if a caption is needed below.

Note: do not pass cropping parameters to `add_picture` — pass `width` and `height` such that the original aspect ratio is preserved. If the layout requires a specific aspect ratio, leave a placeholder instead and let the user resolve the framing during deck review.

### Phase 6 — Reference list integration

Add the source paper to the master Vancouver reference list (see `references.md`):

```
20. Yang J, Park MJ, Kim CW, Lee HS, Yoon SR. Calcaneal osteomyelitis due
    to non-tuberculous mycobacteria: a case report. Ann Rehabil Med.
    2016;40(1):178–82.
```

The reference line on the slide bottom then includes the figure source's number alongside the body-content sources:

```
Refs: 1, 5, 12, 14, 18, 20   ← image source as ref #20
```

### Phase 7 — File management

User-side workflow when Claude is sourcing images:

1. Recommend the candidate PMC paper(s) to the user with a one-line description of what each figure shows.
2. User downloads the figure(s) and places them in `Sources/Figures/` with descriptive filenames (e.g., `MRI wrist rice bodies.jpg`).
3. User confirms filename.
4. Build script references the file path and embeds the image.

Don't try to download images yourself — PMC and most journal hosts are typically blocked from your network. Always go through the user.

---

## When you can't find an open-access image

If after a thorough search no suitable open-access image exists:

1. **Use a placeholder** — the default behaviour anyway; let the user source it manually from a textbook they own.
2. **Suggest a recreation** — if the figure is a cascade diagram, classification table, or simple anatomical schematic, recreate it as native PowerPoint shapes.
3. **Suggest a textbook screenshot** — for figures from a textbook the user already owns, the user can crop their own scan; document the source in the caption.
4. **Suggest a stock illustration** — generic anatomical diagrams from open-access anatomy resources (AnatomyTOOL, OpenStax Anatomy) are sometimes acceptable for non-clinical illustrative content.

---

## Source recommendations by image type

| Image type | First-line source |
|---|---|
| Plain film / radiograph | PMC case reports of the specific disease |
| MRI (musculoskeletal, neuroradiology) | Skeletal Radiology, IDCases, Neuroradiology articles in PMC |
| CT (chest, abdomen) | Respirology Case Reports, BMC Pulmonary Medicine, Radiology Case Reports |
| Ultrasound | Journal of Medical Ultrasound, J Ultrasound Med |
| Clinical photographs | Cleveland Clinic Journal of Medicine; NEJM Image Challenges (often OA); BMJ Case Reports |
| Histopathology (H&E) | Internal Medicine (Japan), Diagnostic Pathology, Case Reports in Pathology |
| Special stains / microbiology | Journal of Clinical Microbiology, Infection and Immunity |
| Anatomical schematics | Open-access anatomy textbooks (AnatomyTOOL, OpenStax Anatomy) |

---

## Self-check before declaring images done

- [ ] Default policy followed: placeholders unless the user explicitly asked for direct sourcing
- [ ] User-supplied images embedded at original aspect ratio (no cropping)
- [ ] Every embedded image has a paper-derived caption describing what's shown
- [ ] Every embedded image has source attribution (Author Year, PMC ID, license)
- [ ] License verified at the source paper's footer (not assumed)
- [ ] Source paper is in the master reference list
- [ ] Reference number for the source appears in the slide's Ref line
- [ ] Image height + caption fits within the body area (above the reference line at y≈6.50 in)
- [ ] No CC-BY-NC-ND images have been cropped or annotated
- [ ] Filename in `Sources/Figures/` matches what the build script expects
