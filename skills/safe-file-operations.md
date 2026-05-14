---
name: safe-file-operations
description: Safety discipline for any operation that modifies, replaces, or rebuilds a file the user considers "final" or "important". Use this BEFORE any operation that overwrites an existing PPTX, doc, code file, or other artifact the user has invested significant work in.
---

# Safe file operations — backup before modify

## Why this matters

A "rebuild" that's structurally valid can still be content-empty: a small output file with placeholder-only slides and zero embedded images can save without raising any errors, but isn't the deck the user finalised. A subagent can confidently self-report success while the file is broken. Once the original is overwritten, no working state exists to recover from — the user has to find their own off-machine backup.

The rule below is the permanent fix: **never modify a finalised artifact without first making your own backup, even if you trust the operation to succeed.**

See `retrospective.md` for the project history that drove these rules.

---

## The rule

**Before any operation that could modify or replace a file the user has called "final", "important", "finished", or that contains substantial accumulated work:**

1. **Make a backup copy** with a clear name (e.g., `<filename>.backup-YYYYMMDD-HHMM.<ext>` or `<filename>_backup.<ext>`)
2. **Verify the backup exists and is complete** — check size, slide count, key content — before proceeding
3. **Write the modified output to a new filename**, not the original — let the user verify and rename
4. **If overwrite is unavoidable**, at minimum keep your own backup copy in a separate location
5. **Never trust a subagent's "success" report blindly** — verify the actual output yourself before considering the task done

---

## Triggers — when to apply this skill

You should automatically invoke this skill before any of the following:

| Operation | Examples |
|---|---|
| **Overwrite a "final" file** | Replacing a presented PPTX, finalized DOCX, submitted PDF |
| **Rebuild from scratch** | Regenerating a deck/document/codebase from a source-of-truth file |
| **Bulk-modify multiple slides** | Adding new slides + modifying existing slides in one pass |
| **Delegate file modification to a subagent** | Any subagent task that writes to an existing user-owned file |
| **Run a build script that overwrites previous output** | Re-running `build_x.py` whose output path matches a finalized deliverable |
| **Move or rename folders containing important work** | Reorganizing project archives, archive cleanup, "finalize" steps |

User language that should trigger this skill:
- "finalized"
- "this is the final version"
- "I presented this"
- "I shared this"
- "for archive"
- "important"
- "don't break this"
- "before we archive..."

---

## Backup naming conventions

Use one of these patterns:

```
<filename>.backup-YYYYMMDD-HHMM.<ext>
<filename> (backup before <description>).<ext>
<filename>_backup.<ext>
```

For example:
- `{Topic} slide (Final).backup-20260508-1015.pptx`
- `{Topic} outline.md.backup-20260508-1015.md`
- `build_final_deck.py.before-feedback-update.bak`

The naming should make it obvious that it's a backup, not a working file.

---

## Where backups go

Backups belong in a dedicated subfolder so they don't clutter the live working directory. The standard location inside a project is:

```
{Project}/Build_archive/Backups/
```

This sits alongside `Section_PPTXs/` and `Old_versions/` inside `Build_archive/` (see folder structure in `CLAUDE.md` Section 5). Keeping safety backups in their own folder makes it obvious which files are active deliverables (`Deck/`) versus safety copies (`Build_archive/Backups/`).

If a project doesn't yet have `Build_archive/Backups/`, create it before making the first backup. Don't drop backups next to the live file at the project root or inside `Deck/` — they look like working files there and risk being opened by mistake.

---

## Workflow — applying the skill

### Step 1 — identify the artifact at risk

Before starting any potentially destructive operation, list the files that will be touched:
- Inputs (read-only — usually safe)
- Outputs (will be created — usually safe if new filename)
- **Existing files that will be overwritten or modified — the at-risk set**

### Step 2 — back up the at-risk set

Backups go into `{Project}/Build_archive/Backups/` (create the folder if it doesn't exist):

```bash
# Example: before rebuilding a finalised PPTX
mkdir -p "Build_archive/Backups"
TS=$(date +%Y%m%d-%H%M)
cp "Deck/{Topic} slide (Final).pptx" "Build_archive/Backups/{Topic} slide (Final).backup-${TS}.pptx"
ls -la "Build_archive/Backups/" | grep "${TS}"   # verify backup exists
```

In python-pptx scripts, the same applies:

```python
import shutil, os
from datetime import datetime
from pathlib import Path

source = Path("Deck/Hyponatremia slide (Final).pptx")
backup_dir = Path("Build_archive/Backups")
backup_dir.mkdir(parents=True, exist_ok=True)
backup = backup_dir / f"{source.stem}.backup-{datetime.now():%Y%m%d-%H%M}{source.suffix}"
shutil.copy(source, backup)
assert backup.stat().st_size == source.stat().st_size, "Backup verification failed"
```

### Step 3 — write the modified version to a new filename FIRST

Don't overwrite the original. Use a temporary name like `Final v2.pptx`, `Final NEW.pptx`, or `Final (with feedback).pptx`. Let the user verify. Only after they confirm it's correct should the rename happen.

### Step 4 — verify the new output is correct BEFORE removing the original

Quick sanity checks for a PPTX rebuild:
- File size — is it within an order of magnitude of the original?
- Slide count — matches expected?
- Image count — matches expected?
- Speaker notes count — matches expected?
- Spot-check 3–5 representative slides for actual content

```python
from pptx import Presentation
new = Presentation("/path/to/new.pptx")
old = Presentation("/path/to/backup.pptx")

print(f"New slides: {len(new.slides)}")
print(f"Backup slides: {len(old.slides)}")

for prs, label in [(new, "new"), (old, "backup")]:
    images = sum(1 for s in prs.slides for sh in s.shapes if hasattr(sh, 'shape_type') and sh.shape_type == 13)
    notes = sum(1 for s in prs.slides if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip())
    print(f"{label}: {images} images, {notes} notes")
```

### Step 5 — only after verification, do the rename/replacement

Once the user confirms (or verification passes), the new file can replace the original. The backup stays in `Build_archive/Backups/` permanently — don't delete it. (Backups go in `Backups/`; superseded full-deck iterations go in `Old_versions/`.)

---

## Subagent-specific protections

If you must delegate file modification to a subagent:

1. **Make the backup yourself first** — do not delegate the backup step
2. **Tell the subagent in its prompt that there is a backup at `<path>` and they must NOT modify or delete it**
3. **Tell the subagent to write to a new filename, not the original** — even if the user said "replace"
4. **Verify the subagent's output independently** — do not trust the subagent's self-reported success
5. **Run a sanity check on file size, slide count, and image count** before reporting completion to the user

Subagent reports can be misleading. A subagent can write something like *"Verification: ✓ Slide count: 57 confirmed... ✓ All embedded images correctly referenced"* and still have produced a file with zero embedded images — confusing "image paths exist on disk" with "images actually embedded in the deck" is a real failure mode. Independent verification is mandatory.

---

## Recovery from a destructive failure

If a destructive operation has already occurred and you don't have your own backup:

1. **Stop further operations immediately**. Don't try to "fix it" by another modification — you may make recovery harder.
2. **Tell the user honestly**. Don't downplay or hide the failure.
3. **Inventory what's recoverable**:
   - `Build_archive/Backups/` — safety copies made before risky operations (the primary recovery source)
   - `Build_archive/Old_versions/` — superseded iterations
   - User's own off-machine backups (cloud, email, recent items, Recycle Bin)
   - Source-of-truth documents (`{Topic} outline.md`, etc.) that can rebuild content
   - Any cached or temporary files
4. **Propose recovery options with their tradeoffs**, and let the user choose
5. **Capture the failure as a permanent lesson** in the skills folder

---

## Specific anti-patterns to avoid

| Anti-pattern | Why it fails | What to do instead |
|---|---|---|
| "I'll just overwrite, the rebuild should work" | Build scripts can have subtle bugs you discover only after destruction | Always write to new filename first |
| "The subagent will handle it carefully" | Subagents can have any of the same failure modes you do, plus you can't see what they did until after | Make backups yourself; verify subagent output |
| "User said replace, so I'll replace" | Even if the user authorizes overwrite, they're trusting you to do it correctly | Honor the intent (single deck) without sacrificing safety (keep a backup) |
| "I tested similar operations before" | Each operation has unique state | Backup discipline applies regardless |
| "If there's a problem I'll undo it" | Undo doesn't exist for file overwrites in most filesystems | Never count on undo |

---

## When this skill is NOT triggered

You don't need to follow this protocol when:
- Creating a brand-new file that doesn't already exist
- Modifying a file in your own scratch/output directory that the user hasn't seen
- Editing your own working files (Python scripts, intermediate builds)
- Running iteration loops where intermediate outputs are explicitly disposable

The trigger is specifically **user-owned, finalized, or important artifacts**.

---

## Self-check before any potentially destructive operation

- [ ] Have I identified the at-risk file(s)?
- [ ] Have I made a backup copy with a clear, dated name?
- [ ] Have I verified the backup is intact (size, content)?
- [ ] Will my output go to a new filename, or will it overwrite the original?
- [ ] If overwriting is required, do I have a separate backup that won't be overwritten?
- [ ] If I'm delegating to a subagent, have I made the backup myself FIRST and protected it from the subagent?
- [ ] After completion, have I verified the new file independently (not just trusted the success report)?

If any answer is "no", **do not proceed**.

---

*This file should be read before any "rebuild," "replace," "overwrite," or "modify final" operation. Project history behind these rules lives in `retrospective.md`.*
