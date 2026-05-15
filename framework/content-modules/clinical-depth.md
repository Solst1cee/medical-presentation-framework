---
name: clinical-depth
description: "Optional content module for any clinical-syndrome slide that needs a bedside layer — history, examination findings, and cohort symptom-prevalence numbers. Use when a presentation describes a disease syndrome a resident must recognize at first encounter."
---

# Clinical-presentation depth in medical slides

## Why this matters

Medical presentations tend to skew toward imaging, microbiology, and treatment because those are concrete and citation-rich. The **bedside encounter layer** — what the patient says, what the patient looks like, what the examining clinician notices — is often thin. A deck that lists risk factors, imaging features, and antibiotic regimens but says little about *how a patient with this syndrome would actually present at first encounter* fails the most important test: could a resident reading this deck recognise the disease in clinic next week?

See `framework/retrospective.md` for the project history that drove this module.

---

## Required structure for every clinical-syndrome slide

For each named syndrome (e.g., "Tenosynovitis", "Septic arthritis", "Bursitis"), build a **clinical-presentation block** with three layers:

### 1. History — what the patient tells you

- **Duration / tempo** — acute (hours-days) vs subacute (weeks) vs chronic (months)
- **Pain quality** — sharp, dull, aching; constant or movement-related
- **Functional impact** — what activities the patient can no longer do
- **Constitutional symptoms** — fever, night sweats, weight loss, fatigue (with prevalence numbers from a cited cohort)
- **Exposure history** — environmental, occupational, surgical, medication, sexual, travel
- **Previous treatments tried** — antibiotics, steroids, NSAIDs, surgery — and the response

### 2. Examination — what you find at the bedside

- **Inspection** — swelling pattern, erythema, deformity, skin changes
- **Palpation** — temperature, fluctuance, tenderness location, mass character (firm/doughy/fluctuant)
- **Range of motion** — active vs passive limitation
- **Special tests** — Tinel's, Phalen's, anterior drawer, McMurray's, ballottement, etc. — name them by their eponym
- **Distinguishing physical findings** — what makes this look like *this* and not the mimic

### 3. Cohort prevalence — what the literature says

- For each symptom listed, give a **percentage from a cohort study**: "fever in 40%", "constitutional symptoms in 36%", "median dx delay 16 weeks"
- Cite the source paper (Vancouver-numbered)
- Distinguish symptoms that are **sensitive** (present in most cases) from those that are **specific** (rare but pointing strongly to the diagnosis)

---

## Anti-patterns to avoid

- **"Chronic painless swelling"** as the entire clinical description — too thin
- **Pasted differential diagnosis list** without saying *why* the syndrome looks different from each item
- **Imaging-first descriptions** ("MRI shows...") without saying what brought the patient to MRI in the first place
- **Treatment-heavy slides** that imply diagnosis is already obvious

---

## Sourcing the clinical layer

Two complementary sources:

| Source type | What to extract | Example |
|---|---|---|
| **Textbook** (K&F, Harrison's, Hochberg) | Editor-curated symptom list + classic exam pearls | "K&F 12e: 'NTM tenosynovitis presents as chronic unilateral hand/wrist swelling with carpal tunnel signs from median nerve compression by tenosynovial mass.'" |
| **Cohort study** (single-institution series, multicenter reviews) | Symptom prevalence numbers | "Napaumpaiporn 2019 (Thai cohort, n=28): pain 93%, restricted movement 89%, swelling 86%, constitutional symptoms 43%." |

Search PubMed for "[disease] clinical features cohort" or "[disease] case series presentation" to find prevalence data.

---

## Slide layout pattern (one syndrome, one clinical slide)

**Layout: 2-column, with a pearl box at the bottom.**

```
+-----------------------------------------------------------+
| Header: "[Syndrome name] — Clinical Features"             |
+-----------------------------------+-----------------------+
| HISTORY                           | EXAMINATION           |
| - Duration                        | - Inspection          |
| - Pain pattern                    | - Palpation           |
| - Constitutional sx               | - ROM                 |
| - Exposure / risk events          | - Special tests       |
| - Prior treatments                | - Distinguishing exam |
+-----------------------------------+-----------------------+
| Cohort prevalence:                                        |
|   "X cohort (Author year, n=N): Sx-A %, Sx-B %, ..."      |
+-----------------------------------------------------------+
| Pearl: [a single clinical decision rule or trap]          |
+-----------------------------------------------------------+
| Refs at bottom (Vancouver-numbered)                       |
+-----------------------------------------------------------+
```

If the deck has separate "Clinical features" and "Diagnosis & Treatment" slides per syndrome, the clinical-features slide should follow this pattern. The dx/tx slide can then focus on syndrome-specific imaging, microbiology, histopathology, and treatment.

---

## Self-check before declaring a clinical-syndrome slide done

- [ ] Could a junior resident, reading only this slide, decide to test for the disease in a real patient?
- [ ] Are there at least 3 examination findings the resident would actually look for?
- [ ] Is there at least one cohort prevalence number for symptom frequency?
- [ ] Is the contrast with the most common mimic explicit (e.g., "vs RA flare", "vs gout", "vs pyogenic septic arthritis")?
- [ ] Is the pearl box pointing at a *clinical* decision rule, not just a microbiology fact?
