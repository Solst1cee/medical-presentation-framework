---
name: disease-comparison
description: "Optional content module for building a comparison against a clinical mimic. Use when the topic has a related disease that residents are also expected to know (NTM vs TB, gout vs pseudogout, RA vs PsA, etc.). Provides 5 comparison axes and 3 slide layout patterns."
---

# Disease comparison framework

## Why this matters

Faculty often ask comparison questions. "How is NTM septic arthritis different from TB?" is the kind of question where a fragmentary answer ("NTM is more in the hand") falls short. A trained resident should be able to compare across **all clinical axes** — not just one. The trap to avoid: relegating the comparison to a single slide deep in the deck. The contrast should be set up early (dedicated comparison slide immediately after introducing the topic) and reinforced throughout, not buried under a single sub-topic.

See `skills/retrospective.md` for the project history that drove this module.

---

## When to apply this framework

Trigger this skill whenever the topic has a clinical mimic that residents are also expected to know:

| Topic | Common mimic |
|---|---|
| NTM MSK | Tuberculous MSK |
| Gouty arthritis | Pseudogout (CPPD) |
| Rheumatoid arthritis | Psoriatic arthritis, polymyalgia rheumatica |
| Septic arthritis (pyogenic) | Mycobacterial, fungal, crystal |
| Vasculitis (large vessel) | Atherosclerosis, fibromuscular dysplasia |
| Lupus | Mixed connective tissue disease, drug-induced lupus |
| DRESS | Stevens-Johnson syndrome, AGEP |
| Idiopathic inflammatory myopathy | Statin myopathy, mitochondrial myopathy |

If you can identify a comparator before the deep research phase, plan the comparison structure during outline drafting.

---

## Five comparison axes — required for every disease comparison

Compare the disease and its mimic across **all five** of these axes:

### 1. Risk factors / epidemiology
- Age, sex, ethnicity / regional patterns
- Genetic susceptibility (HLA, MSMD)
- Environmental exposures
- Iatrogenic / medication-related risk
- Prevalence and incidence

### 2. Symptoms (history)
- Tempo (acute / subacute / chronic)
- Constitutional symptoms (fever, weight loss, night sweats — with prevalence)
- Joint distribution / target organ
- Pain quality
- Triggering / relieving factors

### 3. Examination findings
- Inspection patterns
- Palpation findings
- Special-test responses
- Skin / extra-articular features
- Lymph node / organ involvement

### 4. Investigation profile
- **Laboratory** — CBC, CRP, ESR, autoantibodies (positive vs negative), specific markers
- **Imaging** — modality of choice, characteristic findings, what's *not* seen
- **Microbiology** — what grows, what stains, on what media, in what time frame
- **Histopathology** — granuloma type, AFB on stain, key features

### 5. Treatment
- First-line drugs
- Duration
- Surgical role
- Special considerations
- Outcomes / prognosis

---

## Slide layout patterns

### Pattern A — Dedicated comparison slide (use for the most important contrast)

Place this slide **early** in the deck, immediately after introducing the topic. Use a **wide table format**:

```
+--------------------------------------------------------------+
| Header: "[Topic] vs [Mimic] — Comparison"                    |
+----------+--------------+----------------+------------------+
| Axis     | [Topic]      | [Mimic]        | Discriminator    |
+----------+--------------+----------------+------------------+
| Risk     | ...          | ...            | ...              |
| Symptoms | ...          | ...            | ...              |
| Exam     | ...          | ...            | ...              |
| Imaging  | ...          | ...            | ...              |
| Micro    | ...          | ...            | ...              |
| Histo    | ...          | ...            | ...              |
| Tx       | ...          | ...            | ...              |
+----------+--------------+----------------+------------------+
```

The **Discriminator** column is the highest-yield: a single feature that, if present, swings the diagnosis decisively.

### Pattern B — Inline comparison columns (use for per-syndrome contrasts)

In each clinical-syndrome slide, add a **two-column table** in a corner showing topic-specific vs mimic-specific findings for that syndrome.

```
+-----------------------------------------------------------+
| Header: "[Syndrome] — Clinical Features"                  |
+----------------------------+------------------------------+
| Pattern, course, fluid      | TB vs NTM contrast (table)  |
| ...                         | ...                          |
+----------------------------+------------------------------+
```

### Pattern C — Two-colour highlighting throughout

If the comparison is central to the topic, pick **two accent colours** — one for the topic, one for the mimic. Use them consistently across every slide where both diseases appear (e.g., topic bullets in `ACCENT_SECONDARY`, mimic bullets in `ACCENT_PRIMARY`). Theme constants live in `deck-build.md` Step 2.

---

## Worked example — NTM vs TB

| Axis | NTM MSK | TB MSK |
|---|---|---|
| **Risk factors** | Aquatic / soil exposure, surgery, biologics, anti-IFN-γ autoantibodies, chronic glucocorticoids | Reactivation of latent TB, immigrant from endemic area, HIV, malnutrition, chronic glucocorticoids |
| **Symptoms** | Indolent monoarthritis or tenosynovitis, often months to years; constitutional symptoms only ~40% | Indolent but more constitutional symptoms; back pain prominent if Pott's |
| **Exam** | Carpal tunnel signs, doughy tenosynovial mass, often hand/wrist; rare fever | Spinal tenderness, kyphosis (Pott's), cold abscess; lymphadenopathy more common |
| **Joint distribution** | Small joints, knee, hand/wrist | Spine 60%, hip, knee |
| **Tenosynovitis** | Common (esp. M. marinum, MAC) | Uncommon |
| **Pulmonary co-disease** | Uncommon in MSK NTM | <50% in osteoarticular TB but more often present |
| **Direct inoculation history** | Common (water, trauma, surgery) | Rare — usually reactivation |
| **Synovial fluid** | WBC 5,000–30,000; lymphocyte-predominant in chronic; AFB ~30% | Variable WBC; AFB 10–20%; tissue often positive |
| **Imaging** | Multilevel skip lesions, sclerotic foci, less disc involvement | Disc-centered, single-level, gibbus deformity |
| **Histopathology** | Granuloma (caseating or non-caseating); fibroblast-like synoviocytes (Park 2014) | Caseating granuloma typical |
| **Culture** | LJ + MGIT, 6–8 wk; species-specific temperature/media | LJ + MGIT, 4–8 wk |
| **Treatment** | Species-specific multidrug ≥6–12 months | RIPE × 2 mo, then RI × 7–10 mo (12 months total typical for MSK) |
| **Discriminator** | Tenosynovitis present, hand/wrist target, direct-inoculation history, slow growth on culture | Spinal involvement, gibbus, lymphadenopathy, classic pulmonary findings, faster growth |

---

## Self-check before declaring the comparison done

- [ ] Have you compared across all 5 axes (risk, symptoms, exam, investigation, treatment)?
- [ ] Is there a "Discriminator" column or row that highlights the most decisive feature?
- [ ] If the comparator has its own treatment, are the regimens distinct enough that mistakes would be clinically meaningful (e.g., RIPE for TB vs species-specific multidrug for NTM)?
- [ ] Is the comparison distributed throughout the deck — or relegated to a single slide?
- [ ] Does the deck visually distinguish the two conditions (e.g., color-coded bullets)?
