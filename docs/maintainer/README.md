# Maintainer guide — Medical Presentation Framework

This guide is for **anyone editing the framework's own files** — the original maintainer, contributors, or your future self on a fresh machine. If you are using the framework to build a presentation deck, read `AGENTS.md` and the project `README.md` instead and skip this folder.

---

## When to load this guide

Load this guide (or have Claude load it) early in any session whose purpose is **editing the framework itself** — for example:

- Updating a building-block file (e.g., `framework/building-blocks/deck-build.md`)
- Adding or refactoring a content module
- Cleaning up cross-references after a rename
- Re-packaging a `.skill` bundle
- Reviewing and bumping the framework's defaults

Do not load it during normal end-user sessions (building a topic review, journal club, case discussion). Those are `AGENTS.md`'s territory.

---

## Writing style for framework files

The framework is publicly shareable on GitHub. Write every framework file so a downloader can use it without context from the maintainer's local environment.

- **Don't include personal names, institution names, or other identifying details.** Acknowledging *"an internal-medicine resident in Thailand"* is fine; nothing more specific.
- **When stating a safety rule or workflow convention, state the rule alone.** Project history / backstory belongs only in `framework/retrospective.md`.
- **Default tone:** instructional and concise. No long "why this exists" explanations outside `framework/retrospective.md`.
- **No emoji** in framework files unless explicitly requested by the user. Bare ASCII glyphs only (`▼`, `★`, `–`) where they earn their place.

If you spot identifying detail or backstory creeping into a framework file during an edit, sanitise it as part of the same change.

---

## Default conventions to preserve

The defaults reflect a Thai academic medical setting. Document them as **adaptable defaults**, not personal facts.

- Slides English by default; speaker notes Thai-narrative with English medical terms preserved.
- `framework/content-modules/local-guideline.md` is Thailand-scoped (NLEM, NHSO, RCPT). Note in its frontmatter that adopters in other countries should fork it.
- Theme constants in `framework/building-blocks/deck-build.md` Step 2 default to an "Academic Navy" palette (or whatever the public default is at time of update). Personal palettes go in the user's `theme/` folder, not into `deck-build.md`.
- Font sizes are deliberately larger than typical PowerPoint defaults (lecture-hall readability). Don't reduce without a documented reason.

---

## Editing safety — backups go outside the repo

The framework's own safety discipline (`framework/safe-file-operations.md`) applies when editing the framework's own files too — but the backup destination is different:

- **For real user projects** built with the framework, backups go to `{Project}/Build_archive/Backups/`.
- **For framework-development work** (editing files inside `framework/`, `AGENTS.md`, `CLAUDE.md`, `README.md`, etc.), backups go to a local dev folder that is **gitignored** — so they don't get pushed to the public repo.

This repo's convention is `not-used/` at the workspace root (gitignored, listed in `.gitignore`). Other contributors can use a sibling folder outside the workspace if they prefer. Either is fine. The non-negotiable rules:

1. Don't put dev backups inside `framework/` — they get confused with canonical files.
2. Don't commit dev backups to git.
3. Don't trust subagents' "success" reports — verify content after any rebuild or batch sweep.

When in doubt, `cp file.md not-used/file.backup-YYYYMMDD-HHMM.md` before editing.

---

## Cross-reference sweep procedure

When you rename a file or move a path inside `framework/`:

1. **Make a backup** of every file that references the old path (`cp` into `not-used/` or sibling dev folder).
2. **Sweep cross-references** with `sed -i 's|old-path|new-path|g' file.md` per file, or for batch:
   ```bash
   grep -rln 'old-path/' . | xargs sed -i 's|old-path/|new-path/|g'
   ```
3. **Verify** with `grep -rn 'old-path/' framework/ AGENTS.md CLAUDE.md README.md docs/` — should return nothing.
4. **Update `README.md`, `AGENTS.md`, and `CLAUDE.md`** if they referenced the old path in user-facing prose (not just paths).
5. **Commit the rename and sweep as a single commit** so `git pull` applies the rename atomically for downstream users.

---

## Re-packaging `.skill` bundles

When `framework/building-blocks/sources-fetch.md` or `framework/building-blocks/librarian.md` changes, re-package the affected `.skill` bundle so the installed skill stays in sync:

```bash
# from any directory
SKILL_DIR=/path/to/Medical\ Presentation\ Framework/framework/building-blocks
mkdir -p /tmp/sources-fetch && cp "$SKILL_DIR/sources-fetch.md" /tmp/sources-fetch/SKILL.md
python -m scripts.package_skill /tmp/sources-fetch /path/to/Medical\ Presentation\ Framework
```

Run from the `skill-creator` skill folder so `scripts.package_skill` is on the path. Adopters who already installed the previous version need to re-install to pick up changes.

If you ever add a third `.skill` bundle to the repo, document its packaging command here too.

---

## On using the framework's own safety rules during edits

`framework/safe-file-operations.md` is written for end users editing finalised decks. The spirit of those rules applies to maintainers editing framework files too:

- Backup before editing important files (just to a different folder per the rule above).
- Write to a new filename for risky rewrites, then verify before replacing.
- Don't trust subagent reports — verify file content after batch operations.

The framework eats its own dog food: when in doubt, treat a framework file like a "finalised" deck.

---

## How the framework is typically maintained — M1 and M2 paths

Maintainers can edit the framework from two contexts. Knowing which one a contributor is on helps when planning edits.

- **M1 — Claude Code on desktop, default for substantive work.** Use the VS Code or JetBrains plugin so markdown editing is side-by-side with the conversation. Watch for the Edit-tool truncation gremlin on files larger than ~500 lines or after several rapid edits in a row — fall back to Write or a Python-via-bash heredoc per `framework/retrospective.md` Case 2 #9.
- **M2 — Web / iOS Claude Code, for typo fixes and tiny edits only.** Open claude.ai/code in a browser or use the Claude iOS app pointed at the connected GitHub repo. Ask for a small change, review the PR on GitHub, merge. Do not try multi-file refactors here — cloud mode has no MCPs, no Python, no shell to your local machine.
- **Switching between M1 and M2 is fine.** Each is its own session; commits push to the same GitHub origin. The repo is the source of truth, not any particular session.
- **Remote Control between machines.** If you start a Claude Code session on your desktop and pick it up from your iPhone via Remote Control, you are still controlling the same session — the desktop runs the work, the iPhone is just a viewport. The PC must stay on for the session to survive.

---

## User contexts to support — U1–U4

End users land on one of four paths. Knowing which one a user is on helps when triaging questions or designing a framework change.

| Path | Where they run | Capability | Common failure mode |
|---|---|---|---|
| **U1 Cowork** | Their PC | Full framework (Phases 1–7), polished UI | Desktop-only — no mobile workflow |
| **U2 Claude Code** | Their PC (terminal or IDE) | Full framework | Heavier setup; `.skill` reinstall needed after `sources-fetch`/`librarian` updates |
| **U3 Web / iOS** | Cloud sandbox via their GitHub fork | **Outline + references only** — no python-pptx, no LibreOffice, no Chrome MCP, no local filesystem | User expects a `.pptx` from cloud mode and gets confused when it does not appear |
| **U4 Remote Control** | Their always-on PC, controlled from iOS | Full framework — runs on their desktop | PC must stay on; 10-minute iOS disconnect timeout |

The user-facing version of this comparison lives in `README.md` "Pick your path" — keep the two in sync when paths change.

---

## Triage cheatsheet when a user reports an issue

- "Build failed" or "no PPTX came out" → check whether they are on U3. Cloud mode cannot run python-pptx or LibreOffice. Not a framework bug.
- "Trigger phrase did nothing" → likely outside the framework folder. `sources-fetch` and `librarian` only auto-trigger when the framework folder is open in Cowork, or when their `.skill` bundle has been installed.
- "I do not have the latest version" → check whether they ran `git pull` AND reinstalled `.skill` bundles (U1/U2) or clicked Sync Fork on GitHub (U3).
- "Audit script crashed" → may be a Python version mismatch in their environment. Confirm `python3 --version` (script targets 3.10+).
- "Visual QA produced no thumbnails" → LibreOffice not installed (`soffice` not on PATH) or `pdftoppm` missing.

---

## What's in the repo (tracked in git)

- `AGENTS.md` — canonical framework instructions (tool-agnostic; primary content file).
- `CLAUDE.md` — thin Claude-specific pointer to `AGENTS.md` plus Claude-tool install notes (Cowork auto-loads this).
- `README.md` — human-facing intro.
- `docs/maintainer/` — this guide and companion files (`architecture.md`, `roadmap.md`).
- `framework/` — the framework's instruction set (one folder per layer).
- `theme/README.md` and `templates/README.md` — placeholder folders for user content; explain the format but contain no user files in the repo.
- `sources-fetch.skill`, `librarian.skill` — bundled standalone skills.
- `.gitignore`.

## What's NOT in the repo (intentionally)

- `MAINTAINER.md` — gitignored, local-only personal overlay (see below).
- `not-used/` — maintainer-local dev backups.
- Topic folders (`Internal Medicine/`, `Rheumatology/`, etc.) — that's user content, not framework content.
- User theme files (`theme/*.md`) and PPTX templates (`templates/*.pptx`) — institution-specific.
- Personal files (`*_personal.md`) at workspace root.
- The maintainer's library configuration (per-machine path; documented in `AGENTS.md` Section 7 as a placeholder).

---

## The optional `MAINTAINER.md` personal overlay

A gitignored `MAINTAINER.md` file at the workspace root is **optional** but useful for the original maintainer. Its purposes:

1. **Signal that the workspace is a maintainer machine** (not a fresh test-clone). Its presence tells the `AGENTS.md` `## For maintainers` block to treat the environment as a source repo. Even an empty file is sufficient for this signal.
2. **Hold truly personal notes** — draft ideas, machine-specific paths, work-in-progress observations. Notes that mature into reusable guidance should graduate into this folder (`docs/maintainer/`) and be committed.

---

## See also

- [`docs/maintainer/architecture.md`](./architecture.md) — deeper architectural notes (4-layer model, frontmatter conventions, file-loading flow)
- [`docs/maintainer/roadmap.md`](./roadmap.md) — parked ideas, deferred work, distribution-channel plans

---

*This guide replaces the older single-file `MAINTAINER.md` at the repo root. The split moves maintainer guidance into the public repo so it is accessible from any tool (including claude.ai/code), while leaving room for a local-only personal overlay.*
