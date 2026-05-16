---
name: reference-audit
description: "Building block for automated reference reconciliation — cross-checks slide citations against the master reference list and Sources/ folder. Loaded by Read path from topic-review.md (and other presentation-types) at slide-removal events, Phase 3→4 transition, Phase 4 build entry, and Phase 6 final reconciliation. Companion to references.md."
---

# Reference audit — automated reconciliation

## Why this matters

The framework's `references.md` Phase 6 specifies a manual walk-through of every slide's `Ref:` line against the master list. In practice that step gets skipped during fast iteration — and the most common downstream bug is **orphaned master-list entries left behind after content trims**, followed by **broken citations** when references are renumbered without updating slide references.

`audit_references.py` automates this check. It runs in 1–2 seconds, takes the outline file as input, and reports four categories of issues:

| Category | Meaning | Recommended action |
|---|---|---|
| **ORPHANED** | Entry in master list but cited on no slide | Remove from master list. Keep the PDF in `Sources/` if user wants it for personal reference. |
| **BROKEN** | Citation appears on a slide but no master-list entry with that number | Add the missing entry, or correct the slide's `Ref:` line. |
| **STALE row** | Sources summary table has a row for a number that's no longer in the master list | Remove the table row. |
| **UNUSED file (file present)** | Master entry not cited on any slide, but the PDF is sitting in `Sources/` | Decide: remove the master entry, or add a citation, or move the file out of `Sources/`. |
| **MISSING file (used, pending)** | Cited on slides and in master list, but no file on disk | Fetch the PDF (see `sources-fetch.md`). |
| **UNMATCHED file** | File in `Sources/` doesn't match any master-list entry by filename heuristics | Either add to master list or rename the file so the audit can match it. |

A clean audit is the entry condition for finalizing the outline and starting deck build.

---

## When to run

Five trigger points. The first three are mandatory; the others are on-demand.

### 1. User requests slide / section removal (MANDATORY)

When the user says any of:
- "Remove slide N"
- "Cut section X"
- "Trim {section}"
- "Delete the {description} slide"

Run the audit **before** the removal, then again **after**. Show the user:
- Which refs become newly orphaned by this removal
- Whether any *other* slide still cites them (in which case they're NOT orphaned)

Ask the user whether to remove the now-orphaned entries from the master list as part of the same operation. Default to yes; user can override.

### 2. End of Phase 3 — "finalize outline" (MANDATORY)

Before transitioning from Phase 3 to Phase 4, run the audit. Block the transition if any `BROKEN` citations exist — Phase 4 build would propagate broken refs into the deck.

### 3. Start of Phase 4 — "build deck" (MANDATORY)

As the first step of the build process, run the audit. Surface any issues before committing tokens to python-pptx work.

### 4. Phase 6 — final reconciliation (RECOMMENDED)

Replace the manual Phase 6 walk-through described in `references.md` with the audit. If the audit returns 0 issues, the reconciliation is done.

### 5. On user request — "audit references" / "check references" (ON-DEMAND)

Any time the user explicitly asks. Common phrasing:
- "Audit references"
- "Check references"
- "Are all references used"
- "What's orphaned"

---

## How to run

From the project root:

```bash
python3 framework/building-blocks/audit_references.py \
    "{Department}/{Topic}/Documents/{Topic} outline.md" \
    "{Department}/{Topic}/Sources/"
```

Exit codes:
- `0` — all references reconciled, no action needed
- `1` — issues found (orphaned / broken / unmatched / unused)
- `2` — script error (outline not found, boundary markers missing)

The script reads only; it does not modify files. The audit reports what to fix; Claude applies the fixes in a follow-up Edit operation after user confirmation.

---

## Workflow integration — pseudocode

When the user says "remove slide N":

```
1. Read outline; identify slide N's content and current Ref: line citations
2. Run audit BEFORE removal → save output
3. Edit outline to remove slide N
4. Run audit AFTER removal → diff against BEFORE output
5. Newly-orphaned refs = ORPHANED_AFTER \ ORPHANED_BEFORE
6. Show user:
   - The newly-orphaned references (with full citations)
   - Note any of those refs that the user might want to keep in Sources/ (PDF retention)
7. Ask user: "Remove these N references from the master list?"
8. On confirmation, Edit outline to remove those entries from master list
9. Update Sources summary table to reflect new orphan status
```

When the user says "finalize outline" or "build deck":

```
1. Run audit
2. If exit code 0 → proceed
3. If exit code 1 → show audit output → ask: "Resolve these issues now, or proceed anyway?"
4. If user wants to resolve → apply fixes in order:
   a. BROKEN citations: add master-list entries OR correct slide refs
   b. ORPHANED master entries: remove from master list (with confirmation)
   c. UNMATCHED Sources/ files: prompt for action (add to master, or ignore)
5. Re-run audit to verify zero issues
```

---

## Output format

The audit prints a structured report. Each category is clearly delimited:

```
==============================================================================
REFERENCE AUDIT — Documents/GPA outline.md
==============================================================================
  Master list entries:   23
  Cited on slides:       23
  In use (matched):      22

⚠  ORPHANED — in master list but not cited on any slide (1):
   [17]  Cordier JF et al. Pulmonary Wegener's granulomatosis: a clinical and imaging study of 77 cases. Chest. 1990;97(4):906–12.
    → Recommended: remove from master list. Keep PDF in Sources/ if user wants it.

📁 SOURCES SUMMARY (23 entries):
   [ 1] ✓ used (file present)              Harrison's IM 21e Ch 363 — Vasculitis Syndromes
   [17] ○ unused (no file)                 Cordier 1990 pulmonary Wegener's 77 cases
   ...

📂 FILES IN Sources/ (7 files):
      Bossuyt 2017 ANCA testing consensus.pdf                          [23]  ✓ in use
      Firestein Kelley 12e Ch90 ANCA-Associated Vasculitis.pdf         [ 2]  ✓ in use
      ...

⚠  Total issues to resolve: 1
```

The clean state — zero issues — looks like:

```
==============================================================================
REFERENCE AUDIT — Documents/{Topic} outline.md
==============================================================================
  Master list entries:   23
  Cited on slides:       23
  In use (matched):      23

✅ All references reconciled.
```

---

## Adding the Usage column to the Sources summary table

The default Sources summary table in `references.md` has columns: `# | Source | Type | Location | Status`. Add a sixth column — **Usage** — populated from the audit:

| # | Source | Type | Location | File status | Usage |
|---|---|---|---|---|---|
| 1 | Harrison's IM 21e Ch 363 | textbook | `Sources/` | ✅ on disk | ✓ used (slides 2, 9, 22, 29, ...) |
| 17 | Cordier 1990 pulmonary | clinical cohort | paywalled | ✗ not fetched | ○ orphaned |

The Usage column makes orphans visible at a glance and lists which slides cite each entry. Auto-populated by the audit script on every trigger.

---

## Self-check before declaring an audit operation done

- [ ] Audit ran without errors (exit code 0 or 1, not 2)
- [ ] Every ORPHANED entry was either re-cited, removed, or explicitly retained by user
- [ ] Every BROKEN citation was resolved (entry added or slide ref corrected)
- [ ] Sources summary `Usage` column reflects current state
- [ ] No file deletions occurred — PDFs in `Sources/` are preserved even when their master-list entries are removed (`safe-file-operations.md` discipline)
- [ ] Final audit run reports exit code 0

---

## Anti-patterns

| Anti-pattern | Why it fails | What to do instead |
|---|---|---|
| Removing orphaned entries silently | User may have intentionally retained a reference for future use | Always show what's being removed; ask for confirmation |
| Deleting PDFs from `Sources/` when removing master-list entry | Loses user's working copy; PDF may be useful for future projects | Master-list and `Sources/` are decoupled — only modify the master list, leave files |
| Trusting the audit script's filename → master matching as authoritative | Heuristic is fuzzy; can miss textbook chapters with non-author filenames | Report UNMATCHED files to the user rather than auto-classifying |
| Running audit only at Phase 6 | Issues compound across iterations; faster to catch during outline edits | Trigger on every slide removal and every phase transition |
| Auto-resolving BROKEN citations by guessing the intended ref number | Easy to silently introduce wrong citations | Always ask the user which entry was intended |

---

*Reference-audit building block. Loaded by Read path from `topic-review.md` and other presentation-type skills at the trigger points above. Companion to `references.md` (Phase 6 reconciliation is now automated).*
