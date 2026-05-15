---
name: evidence-grading
description: "Optional content module for annotating guideline-based recommendations with their evidence grade — GRADE, ACC/AHA Class of Recommendation + Level of Evidence, or USPSTF letter grade. Use whenever a slide states a clinical recommendation that comes from a named guideline, so the audience can see how strong the underlying evidence is."
---

# Evidence grading on recommendation slides

## Why this matters

A slide that says *"start statin therapy"* without telling the audience whether that comes from a Class I, Level A recommendation (multiple RCTs, strong consensus) or a Class IIb, Level C-EO recommendation (expert opinion, no trial data) is hiding the most important piece of information. The audience cannot calibrate how firm the guidance is.

Evidence grading is a one-line annotation that travels with every recommendation. Add it on the slide. Add it in the speaker notes. Faculty will ask what the grade is — having it there pre-empts the question.

---

## The three systems you will meet most often

Different societies use different systems. Name the system on the slide. Do **not** translate one system into another (e.g., "Class I = Grade A") — they are not equivalent and the translation will be wrong somewhere.

### 1. GRADE (Grading of Recommendations, Assessment, Development, and Evaluation)

Used by: WHO, Cochrane, UpToDate, many international and Thai (RCPT) guidelines.

Two axes:

- **Quality of evidence:** High · Moderate · Low · Very Low
- **Strength of recommendation:** Strong · Weak (some guidelines say *Conditional*)

Notation styles you will see:

- *"Strong recommendation, high-quality evidence"* (long form)
- *"1A"* (strong / high), *"1B"* (strong / moderate), *"2A"* (weak / high), *"2C"* (weak / low) — common in CHEST, ACCP guidelines
- *"⊕⊕⊕⊕ High"* or *"⊕⊕⊕⊖ Moderate"* — Cochrane / WHO style

On a slide, write the long form once on the first slide that uses the system, then short codes thereafter.

### 2. ACC/AHA — Class of Recommendation (COR) + Level of Evidence (LOE)

Used by: ACC, AHA, ESC (similar system with slight wording differences), many cardiology and stroke guidelines.

**Class of Recommendation** — what the writers want you to do:

- **Class I** — *Is recommended* / *Should* — benefit >>> risk
- **Class IIa** — *Is reasonable* / *Can be useful* — benefit >> risk
- **Class IIb** — *May be considered* — benefit ≥ risk, less established
- **Class III: No Benefit** — *Is not recommended* — no proven benefit
- **Class III: Harm** — *Should not be performed* — risk > benefit

**Level of Evidence** — how good the underlying data is (2015+ ACC/AHA wording):

- **LOE A** — high-quality evidence from > 1 RCT or meta-analyses of high-quality RCTs
- **LOE B-R** — moderate-quality evidence from > 1 RCT (Randomised)
- **LOE B-NR** — moderate-quality evidence from > 1 well-designed non-randomised study
- **LOE C-LD** — randomised or non-randomised studies with limitations
- **LOE C-EO** — expert opinion based on clinical experience

Notation: *"COR I, LOE A"* or just *"Class I (A)"*.

ESC uses the same Class structure but writes LOE simply as A / B / C without the R/NR/LD/EO suffixes.

### 3. USPSTF (US Preventive Services Task Force)

Used by: screening and primary-prevention recommendations.

- **A** — Recommend; high certainty of substantial net benefit
- **B** — Recommend; high certainty of moderate net benefit, or moderate certainty of moderate-to-substantial benefit
- **C** — Offer selectively based on professional judgement and patient preferences
- **D** — Recommend against; no net benefit or harms outweigh benefits
- **I** — Insufficient evidence to assess

Notation: *"USPSTF Grade B"* — no need for a second axis.

### 4. Society-specific systems you will sometimes see

- **IDSA / ATS** — strength (Strong / Weak) + quality (High / Moderate / Low / Very Low) — GRADE-based.
- **ACG (gastroenterology)** — GRADE-based.
- **ESMO Clinical Practice Guidelines** — own letter / Roman-numeral system (I–V for evidence level, A–E for strength).
- **NCCN** — Category 1 / 2A / 2B / 3 — quality + consensus axis combined.

When citing a society guideline, use **that society's** system. Do not re-grade.

---

## How to annotate on the slide

### One recommendation per line, grade at the end in brackets

> *"Anticoagulate all patients with CHA₂DS₂-VASc ≥ 2 (ACC/AHA COR I, LOE A)."*

> *"Annual mammography in women 50–74 (USPSTF Grade B)."*

> *"Initial dialysis vs medical management — shared decision making in stage 5 CKD (KDIGO 2B)."*

### When multiple grades are present on one slide, label each

If a slide contains recommendations from different societies, name the system on every line:

```
- Aspirin for primary prevention in adults 40–70 with elevated CV risk and low
  bleeding risk: may consider (ACC/AHA COR IIb, LOE A)
- Aspirin for primary prevention in adults > 60: recommend against
  (USPSTF Grade D)
```

A short legend on the slide (*"COR = Class of Recommendation; LOE = Level of Evidence"*) is appropriate if the abbreviations have not been introduced in the deck yet.

### Speaker notes — say the grade out loud

In the speaker-notes narrative (per `framework/building-blocks/speaker-notes.md`), say the grade in words, not just the code. Example: *"นี่เป็นคำแนะนำ Class I, Level A ซึ่งแปลว่า…"* — say what the grade means, not just the letter.

---

## Handling conflicts between guidelines

Conflicts are common and often the most teachable part of a slide. Don't hide them.

### Pattern: list both, note the disagreement, give the rationale

```
- ACC/AHA 2019 — aspirin in primary prevention (age 40–70, high CV risk, low
  bleed risk): may consider (COR IIb, LOE A)
- USPSTF 2022 — aspirin in primary prevention (age 60+): recommend against
  (Grade D)
- Why the divergence: USPSTF weights more recent trials (ARRIVE, ASPREE, ASCEND)
  showing minimal benefit and rising bleed risk in older adults.
```

This pattern works because it (a) names both sources, (b) gives each its own grade in its own system, and (c) explains *why* they diverged — which is the real teaching point.

### When the divergence is between an international guideline and the local one

If RCPT (or local equivalent) takes a different position from ACC/AHA or ESC — or if the recommended drug is not on the local formulary — pair this section with `framework/content-modules/local-guideline.md`. The two modules are designed to be used together for any drug- or test-related slide.

---

## Anti-patterns to avoid

- **Stating a recommendation without its grade.** *"Start statin therapy"* with no grade leaves the audience unable to tell strong evidence from expert opinion.
- **Translating grades across systems.** *"Class I (= Grade A)"* is wrong. Class I is about strength of recommendation; LOE A is about evidence quality. USPSTF Grade A is a combined judgement. They do not map cleanly.
- **Hiding weak evidence behind strong language.** A *"may be considered"* (Class IIb) recommendation written as *"is given to"* misrepresents the guideline.
- **Citing the highest grade in a chain.** If a Class I recommendation depends on a Class IIb upstream decision, the overall strength is no stronger than the weakest link.
- **Omitting the year of the guideline.** Grades change between editions (e.g., aspirin in primary prevention shifted from Class IIa to IIb to Class III in successive editions). Always include the year: *"ACC/AHA 2019"* not just *"ACC/AHA"*.
- **Citing "the guidelines" without naming which one.** Different societies issue different grades for the same intervention; *"the guidelines recommend"* is meaningless.

---

## Worked examples

### Example 1 — single-system slide

> **Anticoagulation in non-valvular atrial fibrillation**
>
> - CHA₂DS₂-VASc ≥ 2 (men) or ≥ 3 (women) → DOAC preferred over warfarin
>   (ACC/AHA 2019, COR I, LOE A)
> - CHA₂DS₂-VASc = 1 (men) or 2 (women) → DOAC reasonable
>   (ACC/AHA 2019, COR IIa, LOE B-NR)
> - CHA₂DS₂-VASc = 0 (men) or 1 (women) → no antithrombotic
>   (ACC/AHA 2019, COR IIa, LOE B-NR)
>
> *Ref: January CT et al. Circulation. 2019;140(2):e125–e151. (PMID 30686041)*

### Example 2 — conflicting societies + local layer

> **Aspirin for primary prevention — competing recommendations**
>
> - **ACC/AHA 2019** — age 40–70, high CV risk, low bleed risk: *may consider*
>   (COR IIb, LOE A)
> - **USPSTF 2022** — age 60+: *recommend against* (Grade D)
> - **Thai RCPT 2022 CV prevention** — individualised; not routinely recommended
>   in primary prevention
>
> Practical take: in our patient (62 y, ASCVD 10-yr risk 12%, no bleeding
> history), the trend across the most recent guidelines is **against** primary
> prevention aspirin. Reserve for established ASCVD.

### Example 3 — GRADE-style with quality + strength

> **Long-term inhaled corticosteroid in COPD**
>
> - Add ICS to LABA/LAMA in patients with FEV₁ < 50% predicted **and** ≥ 2
>   exacerbations per year **or** blood eosinophils ≥ 300/μL
>   (**GOLD 2024 — Strong recommendation, moderate-quality evidence**)
> - Routine ICS in all COPD: *not recommended*
>   (GOLD 2024 — Strong recommendation, high-quality evidence)
>
> *Ref: GOLD 2024 Global Strategy for Prevention, Diagnosis and Management of
> COPD. www.goldcopd.org*

---

## Where the grade lives in the workflow

- **Outline phase** — when a recommendation is added to the outline, the grade is added on the same line. No ungraded recommendation should reach the slide stage.
- **Slide phase** — grade goes in brackets at the end of the recommendation, on the slide itself (per `framework/building-blocks/deck-build.md` — keep on-slide text minimal but the grade is one of the few things that earns its place).
- **Speaker notes phase** — grade is said in words (per `framework/building-blocks/speaker-notes.md`) — both the code and what it means.
- **Mock Q&A phase** — anticipate *"is that a Class I or Class IIa?"* and *"why does USPSTF disagree?"* (per `framework/building-blocks/mock-qa.md`).

---

## Self-check before declaring a recommendation slide done

- [ ] Every recommendation on the slide has a grade.
- [ ] The system is named explicitly (GRADE / ACC-AHA / USPSTF / society-specific).
- [ ] The guideline year is in the citation (e.g., *ACC/AHA 2019*).
- [ ] Mixed-system slides label the system on every line.
- [ ] Conflicts between societies (or with the local guideline) are flagged, not hidden.
- [ ] Speaker notes say what the grade *means*, not just the code.
- [ ] No translation across systems (no *"Class I = Grade A"*).
