---
name: local-guideline
description: "Optional content module for adding local/national guideline and drug-availability context to a medical presentation. Scope: Thailand (NLEM, NHSO, MoPH reference labs, RCPT and specialty society guidelines). Use whenever the audience is Thai-speaking residents or clinicians."
---

# Local guideline & drug-availability integration

> **Scope: Thailand** — NLEM (บัญชียาหลักแห่งชาติ), NHSO (สปสช.), MoPH reference labs, Royal College of Physicians of Thailand (RCPT), and Thai specialty societies. If you ever need a different country, copy this file to `local-guideline-{country}.md` and adapt; do not delete this one.

## Why this matters

International guidelines (ATS/IDSA, ACR, EULAR, NICE) drive the academic content of most presentations. But for residents practising in Thailand, the practical question is *"what can I actually do for my patient at this hospital, with this formulary, under this insurance scheme?"*

A deck that cites international guidelines without addressing Thai-side reality leaves real gaps:

- Whether the drugs in the recommended regimen are **routinely available in Thailand** (and which need named-patient access)
- Whether **NHSO (สปสช.) coverage** includes the proposed regimen, or whether prior authorisation / quota constraints apply
- Where **specialised assays** (autoantibody testing, NGS, species-specific cultures) can be ordered domestically
- What the **Royal College of Physicians of Thailand** or the relevant Thai specialty society recommends
- Realistic substitutions when the recommended drug isn't on the hospital formulary

The result of skipping these: a deck with technically correct international content but limited bedside utility. See `framework/retrospective.md` for the project history that drove this module.

---

## When to apply this module

Trigger this module **automatically** for every presentation where the audience is Thai-speaking residents, even if the primary guideline source is American or European. Specifically:

- Any Thai audience reading ACR / IDSA / ATS guidelines
- Any Thai audience reading EULAR / ESCMID guidelines
- Any Thai audience reading NICE / BNF guidelines
- Any presentation citing a regimen whose drugs may not be on Thai hospital formularies

---

## What to add — the "Local Context" structure

Add a dedicated **"Local Context"** or **"Practical Considerations in Thailand"** slide near the treatment section, plus inline footnotes on individual drug slides.

### Dedicated Local Context slide — required content

#### 1. National / society guidelines
- **Royal College of Physicians of Thailand (RCPT)** — search for topic-specific position papers
- **Thai Society of [specialty]** — Thai Rheumatology Association, Thai Endocrine Society, Infectious Disease Association of Thailand, etc.
- Hospital-specific protocols (e.g., your home-institution ID guidelines, tertiary-hospital treatment pathways) — ask the user if such a document exists

#### 2. Drug availability — what the hospital pharmacy stocks
- Cross-reference each drug in the international regimen against:
  - **National Essential Medicines List (NEML)** — บัญชียาหลักแห่งชาติ
  - **Hospital formulary** — the user's home institution (ask for the formulary if needed)
- For drugs **not on formulary**, note:
  - Alternate substitutions accepted in practice
  - "Special access" or named-patient routes
  - Cost if procured privately

#### 3. NHSO (สปสช.) / Universal Coverage / Social Security coverage
- Is the regimen covered under the patient's scheme?
- Are there **prior-authorization requirements** (e.g., quota for bedaquiline, biologics requiring criteria)?
- Approximate out-of-pocket cost if not covered

#### 4. Reference labs for specialised tests
- For each non-routine assay mentioned, note where it can be ordered:
  - University reference labs (the major Bangkok academic medical centres)
  - Department of Medical Sciences (กรมวิทยาศาสตร์การแพทย์)
  - Private reference labs (major private-hospital pathology departments)
- Turnaround time and approximate cost

#### 5. Local epidemiology adjustments
- If your national prevalence differs from the guideline source, mention it
- Specific risk factors more common in your population (e.g., anti-IFN-γ autoantibodies in Southeast Asians, HBV in Asia, melioidosis in NE Thailand)

---

## Inline footnotes on drug slides

For every drug-specific slide (e.g., "M. abscessus regimen"), add a small italic note for each non-routine drug:

> **Bedaquiline** — restricted to MDR-TB in Thailand; named-patient access via Bureau of TB; not routinely available for NTM.

> **Clofazimine** — limited availability; Compassionate access via Department of Medical Sciences; alternate: omit and rely on amikacin + cefoxitin + macrolide combination.

> **Linezolid** — available in major tertiary hospitals; expensive; Universal Coverage usually requires ID approval.

> **Tigecycline** — available; check formulary; high cost; reserve for refractory cases.

This way, a resident reading a treatment slide knows immediately whether the named drug is achievable.

---

## Workflow — how to find local guidelines

When researching, dedicate a **specific research pass** to local guidelines. Suggested searches:

1. **Royal College of Physicians of Thailand** [topic] guideline — RCPT publishes topic-specific position papers via their journal
2. **Thai Society of [specialty]** [topic] — local society guidelines
3. **National Essential Medicines List Thailand** [drug name] — check formulary status
4. **NHSO benefit package** [drug name] — coverage and prior-authorisation requirements
5. PubMed search: `[topic] AND (Thailand OR "Thai") AND guideline OR consensus`
6. Ask the user directly: "Is there a hospital-specific or department protocol for this?"

---

## Worked example — what a "Local context" slide for NTM might have looked like

```
LOCAL CONTEXT — NTM in Thailand
+----------------------------------------------------------+
| 1. Available drugs (Thailand / home-institution formulary)|
|   - Macrolides (azithromycin, clarithromycin) — formulary |
|   - Ethambutol, rifampin, isoniazid — formulary           |
|   - Amikacin — formulary                                  |
|   - Linezolid — restricted, ID approval required          |
|   - Bedaquiline — MDR-TB only; not routine for NTM        |
|   - Clofazimine — limited; via DMS named-patient access   |
|   - Cefoxitin, imipenem — formulary                       |
+----------------------------------------------------------+
| 2. NHSO / UC coverage                                    |
|   - 12-month antimycobacterial therapy: covered for      |
|     confirmed disease with ID consultation               |
|   - DST at reference lab: covered                        |
|   - Anti-IFN-γ autoantibody testing: not in UC; via      |
|     research / out-of-pocket at select university labs   |
+----------------------------------------------------------+
| 3. Reference labs for specialised testing               |
|   - Mycobacterial culture: most tertiary hospitals have   |
|     LJ + MGIT; species ID via university reference labs   |
|     or DMS                                                |
|   - Anti-IFN-γ ELISA: select university immunology labs   |
|   - NGS for culture-negative PJI: limited; major private  |
|     hospitals may refer abroad if needed                  |
+----------------------------------------------------------+
| 4. Practical adjustments for M. abscessus regimen        |
|   - Standard: amikacin IV + imipenem + macrolide, then   |
|     macrolide + 2-3 of (clofazimine, linezolid, moxi)    |
|   - In Thailand: macrolide + amikacin + linezolid +      |
|     moxifloxacin most commonly used (clofazimine often   |
|     omitted)                                             |
+----------------------------------------------------------+
```

---

## Self-check before declaring treatment slides done

- [ ] Have I added a dedicated "Local Context" slide near the treatment section?
- [ ] For every drug named in the international regimen, have I checked formulary status and noted substitutions inline?
- [ ] Have I cited any **national society guidelines** (RCPT, Thai Society of X, etc.)?
- [ ] Have I named the **reference lab** for each non-routine assay?
- [ ] Are NHSO / Universal Coverage / Social Security coverage notes present where relevant?
- [ ] Could a resident leave the room and order this regimen tomorrow, on a real patient, without further research?
