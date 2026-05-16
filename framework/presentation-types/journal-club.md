---
name: journal-club
description: "Use this skill when the user wants to prepare a journal club presentation — critical appraisal of a single primary paper. Triggers: 'journal club', 'critique a paper', 'PICO', 'critically appraise', 'present a paper', 'JC presentation'."
---

# Journal Club — Workflow

A journal club is a 20–30 minute critical-appraisal presentation of a single primary paper (usually an RCT, cohort study, diagnostic-accuracy study, or systematic review). The deck is typically 15–25 slides. The audience evaluates whether the methodology supports the conclusions and whether the result should change practice.

This skill is a **thin wrapper**: it describes what's specific to journal clubs and points at the building blocks for the mechanics. The appraisal sections below name the validated tool to use for each study design — pick one, apply it, and present its verdict.

---

## What's specific to a journal club

- **Format:** 15–25 slides, 20–30 minutes
- **Single paper focus:** the entire deck appraises ONE study (not a literature review)
- **Required sections:** PICO → background gap → methods → results → critical appraisal → "would this change MY practice?"
- **Tone:** skeptical-but-charitable. The presenter is not a cheerleader for the paper; they're a critical reader.
- **Audience:** residents and staff; presenter is usually a resident
- **Q&A:** dense on methodology (internal validity, external validity, conflicts of interest)

---

## Building blocks to follow

- For PPTX mechanics, theme, and slide layouts → `framework/building-blocks/deck-build.md`
- For auto-fetching the paper PDF, supplementary appendix, protocol, and prior trials into `Sources/` → `framework/building-blocks/sources-fetch.md`
- For references and PMID verification → `framework/building-blocks/references.md`
- For **automated reference reconciliation** (audit script) → `framework/building-blocks/reference-audit.md` — load and run at slide-removal events, end of Phase 3 (outline finalised), start of Phase 4 (build), and Phase 6 reconciliation
- For speaker notes format → `framework/building-blocks/speaker-notes.md`
- For visual QA → `framework/building-blocks/visual-qa.md`
- For mock Q&A → `framework/building-blocks/mock-qa.md`

Image sourcing (`images.md`) is rarely needed — most journal-club slides are tables and forest plots. If the paper provides a figure under CC-BY, use it directly; check the licensing section of the paper.

## Content modules to consider

Most JC decks work directly from the paper. These modules apply only at specific moments:

| Module | When it applies |
|---|---|
| `framework/content-modules/evidence-grading.md` | **Background slides** that cite prior guidelines or trials — annotate each prior recommendation with its grade (GRADE / ACC-AHA Class + LOE / USPSTF) so the audience sees how strong the field's position was before the paper. **Central** if the paper being appraised is itself a guideline, a systematic review with GRADE certainty per outcome, or otherwise issues formal recommendations. **"Would this change my practice?"** slide — name the grade of the existing guideline you would be diverging from. |
| `framework/content-modules/local-guideline.md` | "Would this change my practice in my setting?" slide — pair with local formulary / coverage where drug access matters. |
| `framework/content-modules/paper-summary.md` | Optional, for scaffolding only — a Tier 2 or Tier 3 card of the paper can structure the early outline. Most JC outlines work directly from the paper without this step. |

## Discipline (always applies)

- Before any rebuild → `framework/safe-file-operations.md`

---

## Critical-appraisal toolbox — pick the right instrument for the study design

Every journal-club deck should name the appraisal tool it used. Don't invent ad-hoc criteria — the audience expects a validated instrument. Pick one tool from the table, apply its checklist during outline drafting, and surface its verdict on the appraisal slides.

| Tool | Best for | Year | Where to download |
|---|---|---|---|
| **CASP Checklists** | Plain-English appraisal for any design (RCT, SR, cohort, case-control, diagnostic, qualitative, cohort-prognosis, cross-sectional, economic, clinical-prediction-rule) | 2018–2024 | https://casp-uk.net/casp-tools-checklists/ |
| **Cochrane RoB 2** | RCTs (individual, cluster, crossover) — the current gold standard | v22, Aug 2019 | https://methods.cochrane.org/risk-bias-2 (alt: https://www.riskofbias.info/welcome/rob-2-0-tool) |
| **ROBINS-I** | Non-randomised studies of interventions (cohort/case-control of a treatment) | v1 2016 (v2 in development) | https://www.bristol.ac.uk/population-health-sciences/centres/beam-centre/barr/riskofbias/robins-i/ |
| **AMSTAR-2** | Systematic reviews (of RCTs and/or NRSIs) | 2017 | https://amstar.ca/Amstar-2.php (PDF: https://amstar.ca/docs/AMSTAR-2.pdf) |
| **QUADAS-2** | Diagnostic-accuracy primary studies (QUADAS-3 in development) | 2011 | https://www.bristol.ac.uk/population-health-sciences/projects/quadas/ (PDF: https://www.bristol.ac.uk/media-library/sites/quadas/migrated/documents/quadas2.pdf) |
| **GRADE** | Certainty-of-evidence across a body of evidence (per outcome) | Handbook continually updated | https://www.gradeworkinggroup.org/ (handbook: https://gradepro.org/handbook/) |
| **JBI Critical Appraisal Tools** | Designs without a CASP equivalent (case series, prevalence, text-and-opinion); mixed-methods SRs | 2024 revision | https://jbi.global/critical-appraisal-tools |
| **Newcastle–Ottawa Scale** | Quick star-system appraisal of observational cohort/case-control (widely used; pair with ROBINS-I for rigour) | 2014 (stable) | https://ohri.ca/en/who-we-are/core-facilities-and-platforms/ottawa-methods-centre/newcastle-ottawa-scale (PDF: https://www.ohri.ca/programs/clinical_epidemiology/nosgen.pdf) |

### Reporting guidelines (not appraisal, but pair with the tool above)

- **PRISMA 2020** — SR/MA reporting checklist — https://www.prisma-statement.org/prisma-2020-checklist
- **STARD 2015** — diagnostic-accuracy reporting checklist — https://www.equator-network.org/reporting-guidelines/stard/
- **CONSORT 2010** — RCT reporting checklist — https://www.equator-network.org/reporting-guidelines/consort/
- **STROBE** — observational-study reporting checklist — https://www.equator-network.org/reporting-guidelines/strobe/

**Rule of thumb:** RoB-family tools answer *"is this study at low risk of bias?"*; reporting guidelines answer *"did the authors disclose enough for me to judge?"* A well-reported study can still be at high risk of bias — use both lenses.

---

## Deck skeleton (15–25 slides)

| # | Section | Slides | Content |
|---|---|---|---|
| 1 | Title | 1 | Paper title + citation + presenter |
| 2 | Why this paper | 1–2 | Clinical question that motivated the choice; current standard of care; the gap |
| 3 | PICO | 1 | Population / Intervention / Comparator / Outcome — concise, single slide |
| 4 | Background | 1–2 | Prior evidence (cite 2–3 most relevant prior trials or guidelines) |
| 5 | Methods | 3–5 | Design, randomization/blinding, inclusion/exclusion, intervention details, outcomes, statistical plan |
| 6 | Results | 3–5 | Baseline characteristics, primary outcome, key secondary outcomes, subgroup if relevant, safety |
| 7 | Critical appraisal | 3–5 | Internal validity, external validity, statistical considerations, conflict of interest |
| 8 | Bottom line | 1 | "Would this change my practice?" answer with reasoning |
| 9 | References | 1 | Vancouver-numbered |

Total: 15–25 slides typically.

---

## PICO — required first content slide

Build a single slide with PICO laid out clearly:

```
+---------------------------------------------------------+
| PICO                                                    |
+---------------------------------------------------------+
| Population   : [age, condition, severity, setting]      |
| Intervention : [drug + dose + duration, or procedure]   |
| Comparator   : [placebo, standard of care, active]      |
| Outcome      : [primary]                                |
|                [key secondary]                          |
+---------------------------------------------------------+
```

If the paper's PICO is unclear or shifted between protocol and publication, flag that — it's a critical-appraisal point.

For diagnostic studies the analogue is **PIRT**: Population, Index test, Reference standard, Target condition. For prognostic studies it's **PEO**: Population, Exposure, Outcome.

---

## Critical appraisal — generic four axes

Every JC appraisal slide covers these four axes regardless of design. The study-type sections below add the design-specific items.

### 1. Internal validity
Could the study design produce the observed result by something other than the intervention effect? Randomisation, blinding, loss to follow-up, outcome adjudication, analysis population.

### 2. External validity (generalisability)
Would the result apply to my patient, in my setting, on my background therapy? Inclusion/exclusion, single- vs multi-centre, country, health-system context, run-in periods.

### 3. Statistical considerations
Was the study powered for the question it answered? Pre-specified vs post-hoc, multiple comparisons, effect size vs significance, NNT/NNH.

### 4. Conflicts of interest & funding
Industry-funded, industry-designed, author conflicts, trial-registration match.

---

## Critical appraisal by study design — apply during outline drafting

Apply the matching tool from the toolbox above, and walk through the checklist below. CRITICAL-flagged items are the ones that, if failed, materially change the verdict.

### RCT — use Cochrane RoB 2

- **Allocation concealment** — central/web randomisation or sealed, opaque, sequentially-numbered envelopes (SNOSE)
- **Blinding hierarchy** — patient / clinician / outcome-assessor / data-analyst; the lowest tier wins
- **ITT vs per-protocol** — primary analysis must be intention-to-treat; per-protocol is supportive only (**CRITICAL**)
- **Primary outcome pre-specification** — registry (ClinicalTrials.gov, EU-CTR, ANZCTR, TCTR) must match publication for definition, timepoint, and analysis population (**CRITICAL**)
- **Sample size & power** — a-priori calculation with stated effect, alpha, beta, expected event rate
- **Stopping rules** — pre-specified interim analyses with alpha-spending (O'Brien–Fleming, Pocock); early stopping for benefit inflates the effect (truncation bias)
- **Non-inferiority margin** — clinically justified, pre-specified, ideally <50% of the expected superiority effect; report results on both ITT and per-protocol populations
- **Loss to follow-up** — <5% reassuring; >20% serious; *differential* loss across arms is the killer
- **Adverse-event reporting** — CONSORT-Harms extension; pre-specified vs collected verbatim
- **Fragility index** — number of event-status flips needed to lose p<0.05. Treat it as an *intuition* about how close-to-the-threshold a binary-outcome result sits, not as a quality verdict. Modern critique (Cote 2024; Andrade 2020) notes that a low FI in a properly-powered trial is mathematically expected. Do not apply to non-binary or time-to-event outcomes.

### Cohort / case-control — use ROBINS-I (and/or Newcastle–Ottawa)

- **Confounders identified and adjusted** — DAG-driven covariate choice, not stepwise selection; both unadjusted and adjusted estimates reported (**CRITICAL**)
- **Exposure ascertainment** — measured *before* the outcome, validated source (registry, EHR > self-report)
- **Outcome ascertainment** — blinded adjudication; standardised definition
- **Selection bias** — case-control: cases and controls drawn from the same source population; cohort: full inception cohort
- **Immortal time bias** — exposure status assigned at time-zero (use landmark analysis or time-dependent Cox), not after exposure begins. Classic example: statin–diabetes association flipping from HR 0.74 to HR 1.97 once immortal time is corrected (**CRITICAL**)
- **Lost to follow-up** — differential between groups is what matters
- **Propensity scoring** — covariate balance reported after matching/weighting (standardised mean difference <0.1); positivity assumption checked
- **Bradford Hill viewpoints** — strength, consistency, temporality, biological gradient, plausibility, coherence, experiment, analogy. Viewpoints, not checkboxes
- **E-value** — quantifies the unmeasured confounding strength that would explain away the result; modern expectation for observational claims

### Systematic review / meta-analysis — use AMSTAR-2; report against PRISMA 2020

- **Protocol pre-registration (PROSPERO)** — registered a-priori (**AMSTAR-2 critical**)
- **PICO and eligibility criteria** — pre-specified and explicit
- **Search strategy** — ≥2 databases, grey literature, no language restriction, reproducible search string (**AMSTAR-2 critical**)
- **Duplicate screening and extraction** — two independent reviewers (**AMSTAR-2 critical**)
- **Risk-of-bias of included studies** — RoB 2 / ROBINS-I / QUADAS-2 applied to each included paper (**AMSTAR-2 critical**)
- **Heterogeneity** — I² *with confidence interval*, τ² (between-study variance); I² interpreted alongside τ², not in isolation
- **Publication bias** — funnel plot when ≥10 studies; Egger's / Begg's tests; trim-and-fill or PEESE for adjustment (**AMSTAR-2 critical**)
- **Subgroup analyses** — pre-specified; test-for-interaction p-value reported (not just within-subgroup p); apply the ICEMAN credibility instrument
- **Network meta-analysis** — transitivity (qualitative comparison of effect modifiers across treatment loops), consistency (statistical: side-/node-splitting, design-by-treatment interaction), network-plot completeness
- **GRADE certainty per outcome** — five downgrading domains (risk of bias, inconsistency, indirectness, imprecision, publication bias) + three upgrading (large effect, dose-response, plausible confounding in wrong direction)
- **Conflicts of interest** — for both authors and included studies (**AMSTAR-2 critical**)

### Diagnostic accuracy — use QUADAS-2; report against STARD 2015

- **Spectrum (case-mix)** — full clinical spectrum representative of intended use; case-control designs (clearly diseased vs clearly healthy) inflate accuracy (**CRITICAL**)
- **Reference-standard quality** — best available; same standard applied to all subjects (or a pre-defined differential standard)
- **Verification / work-up bias** — does the reference standard depend on the index-test result?
- **Partial verification** — if only test-positives receive the reference standard, sensitivity is inflated and specificity is uninterpretable
- **Index-test threshold pre-specified** — not chosen post-hoc from the ROC curve ("data-driven cutoff")
- **Blinded interpretation** — index and reference read blind to each other and to clinical information
- **Sensitivity, specificity, PPV, NPV, LR+, LR-** all reported with 95% CIs; PPV/NPV anchored to a stated prevalence
- **Pre-test probability and Fagan nomogram** — does the LR meaningfully shift post-test probability in your setting?
- **Indeterminate / uninterpretable results** — handled transparently, not silently excluded

---

## Paper red-flags checklist — verify before believing the conclusions

These are common ways a paper's headline overstates its evidence. Walk through this list during Phase 2 (read the paper) — at least 3 of these typically apply to any given paper, and the appraisal slides should name them.

| # | Red flag | How to detect |
|---|---|---|
| 1 | **Spin in conclusions** despite non-significant primary outcome | Read the primary-outcome p-value first; then check whether the conclusion-line foregrounds a secondary, subgroup, or per-protocol result. Catalogued in ~40–60% of nominally-negative RCTs (Boutron 2010, 2014). |
| 2 | **Specific spin phrases** to watch for | "Trend toward", "promising", "favourable", "numerical improvement", "P>0.05 interpreted as equivalence", "non-significant but clinically meaningful", "showed efficacy in subgroup" |
| 3 | **Outcome switching** | Open the trial-registry record → "Outcome Measures" → compare order, timepoint, and exact definitions to the published paper; check protocol-vs-publication dates. The COMPare project found 301 outcomes dropped and 357 added across 58/67 trials in top-5 journals. |
| 4 | **HARKing (Hypothesising After Results Known)** | Hypothesis in the past tense to fit the result; new endpoints introduced in the discussion that are not in methods; absent or post-dated registry |
| 5 | **p-hacking** | Many p-values clustered just under 0.05; flexible covariate sets across tables; reported tests differ from the methods section |
| 6 | **Trial-registration mismatch** | Registry timepoint, scale, analysis population, or responder definition silently swapped between protocol and publication |
| 7 | **Table 1 anomalies (Carlisle test)** | Baseline continuous variables too similar between arms (uniform p-value distribution violated); SD impossible given the reported mean and bounds; integer counts not matching denominators |
| 8 | **Undeclared conflicts** | Cross-check last-author affiliations, declared funding, prior speaker fees on Open Payments / Disclosure.io; medical-writing acknowledgement language hints at industry ghostwriting |
| 9 | **Relative vs absolute risk reduction** | Abstract reports RRR / HR only; calculate ARR and NNT yourself from event rates. RRR 50% can translate to ARR 1% (NNT 100) |
| 10 | **Composite primary endpoint dominated by softest component** | Read the component-by-component breakdown; if the "win" comes from hospitalisation or symptom-score rather than death/MI, the headline overstates |
| 11 | **Surrogate-endpoint reliance** | HbA1c, LDL, tumour-shrinkage standing in for hard outcomes; check whether the surrogate is meta-analytically validated for that disease |
| 12 | **ITT-to-PP switch between protocol and publication** | Protocol pre-specifies ITT primary; paper foregrounds PP because ITT didn't cross the threshold |
| 13 | **Subgroup-driven enthusiasm** | Forest plot of subgroups featured prominently; p-for-interaction absent or non-significant; subgroup not pre-specified; ICEMAN credibility low |
| 14 | **Sample-size moving target** | Power calculation differs between protocol and paper (effect size inflated, alpha relaxed, or interim "re-estimation" without alpha-spending) |
| 15 | **Early stopping for benefit** | Stopped at the first interim with a large effect — known to overestimate the true effect (truncation bias). Check the stopping boundary (O'Brien–Fleming vs Pocock) |
| 16 | **Fragility-index intuition (binary RCT outcomes only)** | If flipping 1–3 events would erase p<0.05, the result sits on the threshold. Use as a gut-check, not a quality verdict — see RCT section above. |
| 17 | **Per-protocol "as-treated" reassignment** | Crossovers analysed in the group they ended up in, not the group they were randomised to — destroys randomisation |
| 18 | **Missing or post-hoc trial registration** | Registry date is *after* the first-patient-enrolled date — common in older trials, still appears today |

---

## "Would this change my practice?" — the bottom-line slide

This is the slide faculty will ask about most. Structure:

- **Direct answer first:** Yes / No / Yes-with-caveats
- **Reasoning:** 2–3 sentences anchored in the appraisal
- **Local context:** what does this mean in our setting / our patients / under our coverage scheme? (Loop in `local-guideline.md` if drug availability or formulary applies.)
- **Honest about uncertainty:** what would you want to see before changing practice (a confirmatory trial, longer follow-up, a real-world cohort)?

Avoid: "It depends" with no follow-through. Avoid: cheerleading the paper without acknowledging weaknesses.

---

## 6-phase workflow

### Phase 1 — Paper selection & kickoff (10–15 min)

Confirm via `AskUserQuestion`:

1. Which paper? (PMID, title, citation)
2. Why this paper? (Recent? Local relevance? Faculty assigned?)
3. Audience and language?
4. Length (slide count, time)?

Also classify the design (RCT / observational / SR-MA / diagnostic) so the matching appraisal tool from the toolbox can be loaded before Phase 2.

### Phase 2 — Read the paper (30–60 min)

**Before reading, ensure the working set is in `Sources/`.** A journal-club working set is usually: the paper PDF, its supplementary appendix, the trial protocol if available, the trial-registration record (screenshot or text export of the registry's outcome list), and 2–3 prior trials/guidelines cited in the background. Use `sources-fetch.md` to acquire anything not yet on hand — browser download via VPN handles publisher PDFs, supplementary appendices, and registry exports; PMC works for the prior background papers when they're open access.

Read the actual PDF carefully — methods first, then results, then discussion last. Don't infer from the abstract or training knowledge. Walk through the matching study-design checklist above AND the red-flags checklist as you read. Note:

- Pre-specified primary outcome
- Sample-size calculation
- Subgroup analyses (pre-specified or post-hoc?)
- Conflicts disclosed
- Trial-registration ID (look up on ClinicalTrials.gov / EU-CTR / TCTR; compare to the paper)
- For SR/MA: the PROSPERO registration record
- For diagnostic: the reference-standard definition and prevalence in the sample

### Phase 3 — Outline drafting (45 min)

Build `Documents/Outline.md` following the 15–25 slide skeleton. PICO, methods, results — copy the numbers directly from the paper, don't paraphrase. The critical-appraisal section comes from your own reading using the design-specific checklist and the red-flags list. Name the appraisal tool you applied (e.g., "Appraised using Cochrane RoB 2 — overall judgement: Some concerns") on the first appraisal slide.

**Slide-removal trigger** — if the user asks to remove a slide or cut a section, run `audit_references.py` (see `reference-audit.md`) before and after the removal, surface newly-orphaned refs, and ask whether to drop them from the master list. Do not delete files from `Sources/` as part of this — only the master-list entry.

**End-of-Phase-3 audit (mandatory)** — before transitioning to Phase 4, run the reference audit. Block the transition if any BROKEN citations exist.

### Phase 4 — Build deck (45–60 min)

**Mandatory entry step — run the reference audit BEFORE any python-pptx work.** See `reference-audit.md`:

```bash
python3 framework/building-blocks/audit_references.py \
    "{Department}/Journal Club/{Paper short title}/Documents/Outline.md" \
    "{Department}/Journal Club/{Paper short title}/Sources/"
```

If the audit reports BROKEN citations or other issues, surface them and resolve before proceeding.

Apply `deck-build.md`. Save as `JC_v1.pptx`, not `(Final)`.

### Phase 5 — Visual QA + speaker notes (30–45 min)

Apply `visual-qa.md` and `speaker-notes.md`. For a journal club, speaker notes should be denser on the appraisal slides (6–10 sentences) because you may need to defend methodological judgments.

**Final reference reconciliation** — run `audit_references.py` one more time at the end of this phase. If it returns 0 issues, the references are reconciled and the deck is ready for the user's review.

### Phase 6 — Mock Q&A (20–30 min)

Apply `mock-qa.md`. For a journal club, generate **18–28 questions** distributed:

- ★ Foundation: PICO components, primary outcome (3–4 questions)
- ★★ Intermediate: methodology — blinding, ITT, subgroup pre-specification (8–12 questions)
- ★★★ Advanced: alternative explanations for the result, conflicts, applicability (5–8 questions)
- Gap section: 3–5 questions on "what would change my mind" / "what's still unknown"

---

## Folder structure

```
{Department}/Journal Club/
└── {Paper short title}/
    ├── README.md
    ├── Sources/
    │   ├── {Paper}.pdf
    │   ├── Protocol.pdf                  # if available
    │   ├── Supplementary_appendix.pdf    # often where the real methods live
    │   └── Trial_registration.txt        # registry ID + screenshot/notes of outcome list
    ├── Documents/
    │   ├── Outline.md
    │   ├── Appraisal_checklist.md        # the filled-in RoB 2 / AMSTAR-2 / QUADAS-2 worksheet
    │   ├── Speaker_notes.md
    │   ├── Mock_questions.md
    │   └── Faculty_feedback.md           # filled after the talk
    ├── Deck/
    │   └── {Paper} JC (Final).pptx + .pdf
    └── Build_archive/
```

---

## Anti-patterns to avoid

- **Cheerleading the paper** — even excellent papers have limits; identify at least three
- **Trashing the paper** — even flawed papers contribute something; acknowledge it
- **Skipping the COI slide** — funding is part of critical appraisal, not optional
- **Quoting effect size without baseline rate** — "HR 0.7" without context is meaningless
- **Subgroup-driven enthusiasm** — pre-specified subgroups OK; post-hoc subgroups should be flagged
- **Citing only the published paper** — read the trial registration and supplementary appendix; compare planned vs reported outcomes
- **Inventing your own appraisal criteria** — use a validated tool from the toolbox above and name it
- **Treating the fragility index as a quality verdict** — it's an intuition for binary outcomes, not a pass/fail

---

## Quick-start checklist

- [ ] Read the paper PDF carefully (not just the abstract); supplementary appendix opened too
- [ ] Design classified; matching appraisal tool downloaded from the toolbox
- [ ] Trial-registration record opened side-by-side with the paper to compare outcomes
- [ ] Design-specific checklist walked through during reading; red-flags checklist applied
- [ ] PICO laid out clearly on its own slide; numbers copied verbatim from the paper
- [ ] Master reference list built; PMIDs verified by web search
- [ ] `audit_references.py` run at end of Phase 3 and start of Phase 4; no BROKEN / ORPHANED entries
- [ ] Deck built per `deck-build.md`; appraisal tool named on the first appraisal slide
- [ ] Visual QA per `visual-qa.md`; speaker notes dense on appraisal slides per `speaker-notes.md`
- [ ] Final `audit_references.py` run returns 0 issues
- [ ] Mock Q&A generated (18–28 questions weighted toward methodology)
- [ ] "Would this change my practice?" slide answers directly with reasoning anchored in the appraisal
- [ ] `safe-file-operations.md` applied before any rebuild or post-presentation update

---

*Journal-club workflow — thin wrapper over the framework building blocks. Skeptical-but-charitable reading; never trash, never cheerlead.*
