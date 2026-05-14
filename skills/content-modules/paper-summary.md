---
name: paper-summary
description: "Optional content module for producing a structured summary card of a single research paper at one of three detail tiers — Tier 1 chip (one-line citation), Tier 2 compact landmark card (~8–10 lines), Tier 3 full paper summary (background + PICO + primary / secondary outcomes + safety + subgroups + authors' limitations + critical remark). Use ONLY when the user explicitly asks for a paper summary; choose the tier from the user's phrasing or ask if ambiguous."
---

# Paper summary — three-tier card with critical remark

## When to use this module

Trigger this module **only when the user explicitly asks** for a structured summary of a specific paper. Typical phrasings:

- *"Summarise [Author Year]."* / *"Summarise [paper] in detail."*
- *"Landmark card for [paper]."* / *"Brief PICO for [paper]."*
- *"One-line cite of [paper]."* / *"Chip for [paper]."*
- *"What does [paper] actually show?"* / *"PICO for [paper]."*

Do **not** auto-summarise every paper added to the master reference list. The point is to surface detail on demand — auto-generating cards for every reference clutters the outline and wastes effort on papers the user doesn't need detail on.

Use cases:

- **Research phase** — deciding whether a candidate paper supports the claim you want to make.
- **Outline drafting** — confirming what claim a cited paper actually supports.
- **Slide review** — checking that an on-slide claim matches the paper's actual findings.
- **Faculty Q&A prep** — anticipating *"what did that paper actually show?"* questions.

This is **not** a full critical-appraisal exercise. For a full critique (full risk-of-bias assessment, applicability analysis, GRADE rating), use the journal-club workflow — see `skills/presentation-types/journal-club.md`.

---

## Detail tiers — pick one before building the card

A paper summary can be useful at three different depths. Pick the tier that matches the moment: an inline citation in a topic-review slide needs a chip; a landmark trial cited as the foundation for a recommendation needs a compact card; a paper that is itself the subject of the discussion needs the full summary.

| Tier | Length | Trigger phrasing | When to use |
|---|---|---|---|
| **1 — Chip** | Single sentence | *"one-line cite of X"*, *"chip for X"* | Inline citation in passing — e.g., a topic-review slide that names the trial supporting a recommendation |
| **2 — Compact landmark card** | ~8–10 lines | *"landmark card for X"*, *"brief PICO for X"*, *"what does X actually show?"* | Topic review where a landmark trial is the foundation of a recommendation and deserves its own callout |
| **3 — Full paper summary** | ~60–90 lines | *"summarise X"*, *"summarise X in detail"*, *"full PICO for X"*, *"full summary of X"* | Journal-club prep, deep Q&A prep, or research-phase decision about whether to cite the paper at all |

**Default behaviour when the user's phrasing is ambiguous:**

- In **journal-club** context → default to Tier 3 (full summary).
- In **topic-review** context → ask *"compact card (Tier 2) or full summary (Tier 3)?"* before generating. Default to Tier 2 if no answer.
- For passing references in any context → Tier 1, no need to ask.

Whichever tier is chosen, label the card with its tier in a small footer line (e.g., `*Tier 2 — compact landmark card.*`) so future iterations of the outline know what they are working with. The tiers are a strict superset — Tier 2 fields are a subset of Tier 3 — so a Tier 2 card can be expanded in place to Tier 3 without rewriting what is already there.

---

## Tier 1 — chip (single sentence)

Format for inline citation:

```
{Author Year} — {trial name}, {design}, n={N}. {Primary result: effect size, 95% CI, p}.
```

Use cases:

- A topic-review slide naming the trial that supports a recommendation in passing.
- A Sources-summary table entry where the deck-level claim and the primary result fit in one row.

Rules:

- Numbers, not narrative — effect size, CI, and p are mandatory.
- No remark, no caveat — those start at Tier 2.
- If the trial has no memorable name, drop the trial-name slot and use just *"{Author Year} — {design}, n={N}. {result}."*

---

## Tier 2 — compact landmark card (~8–10 lines)

Format:

```
### {Author Year} — {short paper identifier}

**Citation:** {short Vancouver, PMID}.
**Design:** {one line}.
**PICO:** (flat — one line per element, no sub-bullets)
- P: {population}; n = {N}.
- I: {intervention}.
- C: {comparator}.
- O: {primary outcome, time horizon}.
**Key result:** {primary-outcome effect size, 95% CI, p; NNT if available}.
**Remark:** {one sentence — what the paper supports, plus the most important single caveat}.
```

Rules:

- PICO is flat — one line per element, no nested bullets.
- *Key result* is **one** line — primary outcome only. Secondary results, safety, and subgroups all live in Tier 3.
- *Remark* is **one** sentence, following the pattern *"Supports X; main caveat Y."*
- No background, no quality / risk-of-bias line, no author-limitation list at this tier — that all lives in Tier 3.
- If used in a deck, add a single *"Use:"* line under the card with slide number and reference number (do not expand into the full Tier-3 "How to use in this deck" block).

Use cases:

- Landmark trial that anchors a recommendation in a topic-review slide.
- Build-aids section of an outline when the paper is one of 2–5 foundational trials for the topic.

---

## Tier 3 — full paper summary (default for journal-club work)

A complete summary of a single paper. Build the thirteen sections in order: background before methods, methods before results, results before interpretation. The audience should be able to read the card and answer *"what was known before, what did this paper add, and what should I do differently on Monday?"* without going back to the PDF.

### 1. Heading

`### {Author Year} — {short paper identifier}`

Example: `### McMurray 2019 — DAPA-HF`

### 2. Citation

Full Vancouver-style citation with PMID (per `references.md`).

### 3. Design — one line

Study type. Examples:

- *Multicentre, double-blind, randomised, placebo-controlled trial.*
- *Prospective cohort study (single tertiary centre).*
- *Retrospective case-control study.*
- *Systematic review and meta-analysis of RCTs.*
- *Diagnostic-accuracy study (cross-sectional).*

### 4. Background — what the trial was asking

Two to four sentences covering:

- The clinical question the trial was designed to answer.
- What was already known at the time of the trial — name the prior key evidence (earlier trials, registries, mechanistic data).
- Why a new trial was needed — gap, contradiction, or new population.

This is the *"why this trial exists"* section. Faculty will ask *"what did we know before this paper came out?"* — answer it here.

### 5. Structured framework

Use the format that matches the study type:

**Interventional studies — PICO**
- **P (Population):** who, n, key inclusion / exclusion criteria
- **I (Intervention):** what was given or done; dose, route, duration
- **C (Comparator):** vs what (placebo, active control, usual care)
- **O (Outcome):** primary endpoint, definition, time horizon

**Observational studies — PECOT**
- **P (Population):** cohort description
- **E (Exposure):** risk factor or condition under study
- **C (Comparator):** unexposed or alternative-exposure group
- **O (Outcome):** outcome measured
- **T (Time):** follow-up duration

**Diagnostic-accuracy studies**
- **Target condition:** what disease the test is meant to detect
- **Index test:** the test being evaluated
- **Reference standard:** the gold standard for comparison
- **Setting:** where the test would be applied (primary care, ED, specialty clinic)

**Systematic reviews / meta-analyses**
- Use PICO for the clinical question, then add **search dates · databases · number of studies included · total n pooled**.

### 6. Primary outcome — numbers

Numbers, not narrative. Include:

- Effect size + 95% CI + p
- Event rates in each arm (e.g., *16.3% vs 21.2%*) where applicable
- NNT / NNH if calculated or easily derivable
- Time horizon

### 7. Secondary outcomes

List the pre-specified secondary endpoints in the order the paper presents them. For each: effect size + 95% CI. Distinguish hierarchical (alpha-protected) secondaries from exploratory ones. If a key secondary was statistically positive in one direction but the absolute effect is small, say so.

### 8. Safety / adverse events

The safety signals that matter:

- Total AE / SAE / discontinuation-due-to-AE rates in each arm
- Drug-class-specific AEs (e.g., DKA for SGLT2 inhibitors, bleeding for anticoagulants, hyperkalaemia for MRAs, infection for biologics)
- Any signal that the FDA / EMA / authors specifically flagged
- Deaths attributable to study drug

Even an *"unremarkable"* safety profile deserves an explicit line — the audience needs to know you checked.

### 9. Subgroup analyses

The two to four most clinically relevant pre-specified subgroups. For each: HR / RR + 95% CI + P-interaction. Note any subgroup with a meaningfully different signal — and flag whether the analysis was pre-specified or post-hoc.

### 10. Author discussion / limitations they note

What the authors themselves identify as limitations or caveats in their Discussion section. Be faithful to their wording, not your own — list what they said. Authors often soft-pedal their own limitations; your independent appraisal (Section 11) is where you state any limitation they downplayed or omitted.

### 11. Quality / risk of bias — your independent appraisal (one line)

Single sentence, your own assessment, beyond what the authors say. Examples:

- *Well-conducted double-blind RCT, low risk of bias overall. Main caveat for application: excluded patients with eGFR < 30 mL/min/1.73 m² and type 1 diabetes.*
- *Open-label observational cohort; selection bias likely (referral pattern to a tertiary centre).*
- *Small single-centre RCT (n = 84); underpowered for the secondary mortality endpoint.*

This is intentionally short — a full GRADE-style appraisal lives in `journal-club.md`.

### 12. Remark — your bottom line (1–2 sentences)

Pattern: *"This paper says X; the strongest claim it supports is Y; the most important caveat is Z."*

- Does this change practice?
- For whom?
- With what caveat?

### 13. How to use in this deck *(only if a deck is being built)*

- Slide N (where the paper's content goes)
- Reference number in the master Vancouver list
- Exact-wording quote(s) being lifted (per `references.md` Phase 5 — verbatim, no paraphrasing)

---

## Where the card lives in the outline

Inline in `{Topic} outline.md`, as a **third build-aid sub-section** alongside Sources summary and Figure summary:

```
## Build aids — not for slides

### Sources summary
[table — papers/textbooks/guidelines used in deck]

### Figure summary
[table — images planned for slides]

### Paper summaries
[one card per landmark paper — added on user request, NOT auto-generated]
```

This keeps everything for the deck in one file. The card lives in the build-aids zone, so it never gets copied into a slide (per the `## Build aids — not for slides` boundary marker established in `references.md` and `images.md`).

If a topic requires summaries for many papers (e.g., a 20-paper systematic-review topic) and the inline cards become unwieldy, consider moving them to a `Documents/Paper_summaries/{Author Year}.md` folder — but confirm with the user first.

---

## Worked examples — the same paper at all three tiers

The three cards below summarise the **same paper** (DAPA-HF). Read them side by side. If Tier 2 feels too thin for how you would actually cite the trial in your deck, that's the signal to bump up to Tier 3.

### Tier 1 — chip

```
McMurray 2019 — DAPA-HF: multicentre double-blind RCT, n = 4744. Dapagliflozin
vs placebo reduced the composite of worsening HF event or CV death — HR 0.74
(95% CI 0.65–0.85), p < 0.001.
```

*Tier 1 — chip.*

### Tier 2 — compact landmark card

```
### McMurray 2019 — DAPA-HF

**Citation:** McMurray JJV, et al. N Engl J Med. 2019;381(21):1995–2008. (PMID 31535829)
**Design:** Multicentre, double-blind, randomised, placebo-controlled trial.
**PICO:**
- P: HFrEF (LVEF ≤ 40%), NYHA II–IV, on standard HF therapy; n = 4744.
- I: Dapagliflozin 10 mg PO once daily.
- C: Placebo.
- O: Composite of worsening HF event or CV death; median follow-up 18.2 months.
**Key result:** HR 0.74 (95% CI 0.65–0.85), p < 0.001. NNT ≈ 21 over 18 months.
**Remark:** Established SGLT2 inhibitors as foundational HF therapy in HFrEF
regardless of diabetes status. Main caveat: eGFR < 30 not studied.

Use: Slide 18 (GDMT pillars — SGLT2 inhibitors), Ref #7.
```

*Tier 2 — compact landmark card.*

### Tier 3 — full paper summary

```
### McMurray 2019 — DAPA-HF

**Citation:** McMurray JJV, et al. Dapagliflozin in Patients with Heart Failure and
Reduced Ejection Fraction. N Engl J Med. 2019;381(21):1995–2008. (PMID 31535829)

**Design:** Multicentre, double-blind, randomised, placebo-controlled trial.

**Background:** SGLT2 inhibitors were licensed as glucose-lowering drugs for type 2
diabetes. CV-outcomes trials in diabetes (EMPA-REG OUTCOME 2015, CANVAS 2017,
DECLARE-TIMI 58 2018) had shown reductions in heart-failure hospitalisation, but
these trials enrolled only small HF subgroups and were not designed to test HF
outcomes. The clinical question DAPA-HF asked was: in patients with established
HFrEF — with or without diabetes — does dapagliflozin reduce worsening HF events or
cardiovascular death on top of guideline-directed medical therapy?

**PICO:**
- **P:** Adults with HFrEF (LVEF ≤ 40%), NYHA II–IV, NT-proBNP ≥ 600 pg/mL (or
  ≥ 400 pg/mL if hospitalised for HF within the prior 12 months), on standard HF
  therapy (ACEi / ARB / ARNI + beta-blocker + MRA as tolerated). Excluded: eGFR
  < 30 mL/min/1.73 m², type 1 diabetes, recent symptomatic hypotension. n = 4744
  (2373 dapagliflozin / 2371 placebo).
- **I:** Dapagliflozin 10 mg orally once daily.
- **C:** Placebo.
- **O:** Primary — composite of worsening HF event (HF hospitalisation or urgent IV
  therapy for HF) or death from cardiovascular causes. Median follow-up 18.2 months.

**Primary outcome:**
- 16.3% (dapagliflozin, 386/2373) vs 21.2% (placebo, 502/2371). HR 0.74
  (95% CI 0.65–0.85), p < 0.001. NNT ≈ 21 over 18 months.

**Secondary outcomes** *(hierarchically tested, alpha-protected unless noted):*
- Worsening HF event alone (HF hosp or urgent IV): HR 0.70 (0.59–0.83).
- CV death alone: HR 0.82 (0.69–0.98).
- KCCQ-TSS at 8 months — proportion with ≥ 5-point improvement: 58.3% vs 50.9%
  (OR 1.15, 95% CI 1.08–1.23).
- All-cause death: HR 0.83 (0.71–0.97).
- Composite renal endpoint (≥ 50% sustained decline in eGFR, ESRD, or renal death):
  HR 0.71 (0.44–1.16) — numerically lower, not statistically significant.

**Safety:**
- Discontinuation due to AE: 4.7% (dapagliflozin) vs 4.9% (placebo) — comparable.
- Volume depletion: 7.5% vs 6.8%; symptomatic hypotension: 1.2% vs 1.7%.
- Major hypoglycaemia: 4 events vs 4 events — no excess.
- DKA: 3 cases (dapagliflozin) vs 0 (placebo) — rare but a known SGLT2-class signal.
- Fournier's gangrene: 0 events.
- Amputation: 0.5% vs 0.5%; fracture: 2.1% vs 2.1% — no excess.
- Renal AE: 6.5% vs 7.2% — slightly fewer in dapagliflozin arm.

**Subgroup analyses (pre-specified):**
- Type 2 diabetes vs no diabetes — HR 0.75 vs 0.73, P-interaction = 0.80. Benefit
  independent of diabetes status (a defining finding of the trial).
- NYHA II vs III–IV — HR 0.63 vs 0.90, P-interaction = 0.02. Numerically greater
  effect in less symptomatic patients — hypothesis-generating, not practice-changing.
- Age < 65 vs ≥ 65 — consistent.
- Background sacubitril/valsartan use (~ 11% of cohort) — benefit consistent.

**Author-identified limitations:**
- Excluded patients with eGFR < 30 mL/min/1.73 m² — most severe CKD not studied.
- Excluded type 1 diabetes — efficacy and safety in T1DM unknown.
- Median follow-up of 18.2 months — long-term durability of benefit and safety
  not addressed.
- Enrolled predominantly clinically stable outpatients — sicker decompensated HF
  population not directly studied.
- Limited racial diversity (Black participants 5%).
- KCCQ-TSS is patient-reported and may be susceptible to unblinding via
  known SGLT2-class effects (osmotic diuresis, weight loss).

**Quality / risk of bias (independent appraisal):** Well-conducted double-blind,
event-driven multicentre RCT with central adjudication and low loss to follow-up
— overall low risk of bias. Beyond the authors' stated caveats, the NYHA II vs
III–IV heterogeneity (P-interaction = 0.02) is worth noting but should be treated
as hypothesis-generating, not as a reason to withhold treatment in advanced HF.

**Remark:** DAPA-HF established that dapagliflozin reduces composite HF events and
CV death in HFrEF independent of diabetes status, extending SGLT2 inhibitors from
a glucose-lowering indication to a foundational HF therapy alongside ACEi / ARB /
ARNI + beta-blocker + MRA. The strongest claim it supports is benefit in stable
HFrEF with LVEF ≤ 40% and eGFR ≥ 30; EMPEROR-Reduced (2020) replicated the
finding in a similar HFrEF population, and DELIVER (2022) extended the indication
to HFpEF / HFmrEF. Main caveats for bedside application: eGFR < 30 not studied,
type 1 diabetes not studied, advanced decompensated HF not directly tested.

**How to use in this deck:**
- Slide 18 (GDMT pillars — SGLT2 inhibitors), Ref #7
- Exact-wording quote: *"Among patients with heart failure and a reduced ejection
  fraction, the risk of worsening heart failure or death from cardiovascular causes
  was lower among those who received dapagliflozin"* (NEJM abstract conclusion)
```

*Tier 3 — full paper summary.*

---

## How to decide between tiers — quick test

Ask yourself, *"if I had to explain why this paper supports the slide, how much would I need to say?"*

- **One sentence (*"the trial showed X"*)** → Tier 1.
- **A short paragraph that names population, intervention, primary outcome, and one caveat** → Tier 2.
- **A full discussion that needs background, secondaries, safety, subgroups, the authors' own caveats, and an independent appraisal** → Tier 3.

When in doubt, build Tier 2 first. If during outline review the card feels thin, expand it in place — Tier 2 fields are a strict subset of Tier 3, so nothing already written is lost.

---

## Self-check before declaring a summary card done

**All tiers:**
- [ ] The tier is named on the card (footer line: *"Tier 1/2/3 — ..."*).
- [ ] Key results contain numbers (effect size + CI + p), not narrative.
- [ ] The structured framework matches the design (PICO for RCT, PECOT for cohort, etc.) — applies at Tier 2 and Tier 3.
- [ ] Tier 1 fits in one sentence; Tier 2 fits in ~8–10 lines.

**Tier 3 only:**
- [ ] Background section names the prior key evidence and the clinical question.
- [ ] Secondary outcomes are listed in the order the paper presents them, each with effect size + 95% CI.
- [ ] Safety section lists discontinuation rates **and** drug-class-specific signals, even if "unremarkable".
- [ ] Subgroup analyses include P-interaction values and flag pre-specified vs post-hoc.
- [ ] Author-identified limitations are listed faithfully **before** the independent appraisal.
- [ ] Independent appraisal (Section 11) goes beyond what authors say — name at least one limitation they downplayed if there is one.
- [ ] Remark follows the *"says X / supports Y / caveat Z"* pattern in 1–2 sentences.

**If a deck is being built (Tier 2 or 3):**
- [ ] Slide number and reference number are listed.
- [ ] The card lives in the `## Build aids — not for slides` section of the outline.
- [ ] Any exact-wording quote is verbatim from the source per `references.md` Phase 5.
