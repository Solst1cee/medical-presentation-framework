# Architecture — deeper maintainer notes

For the high-level architecture diagram, see `AGENTS.md` Section 1. The points below are maintainer-specific.

---

## The 4-layer architecture is deliberate

- **Discipline** (`framework/safe-file-operations.md`) applies always — every workflow loads it.
- **Presentation types** (`framework/presentation-types/`) are thin workflow wrappers — they orchestrate the building blocks but don't implement mechanics.
- **Building blocks** (`framework/building-blocks/`) are reusable mechanics — deck-build, references, images, etc. Each is callable from any presentation type.
- **Content modules** (`framework/content-modules/`) are optional domain content — applied only when their trigger condition matches.

Don't move a building block into a presentation-type file even if "it's only used by one type right now" — that defeats the update-once-propagate-everywhere principle that makes the layered architecture worth having.

---

## Frontmatter conventions

- **Presentation-type files have *auto-trigger* descriptions** (so a user saying "topic review" triggers `topic-review.md`). The description starts with `Use this skill when the user wants to...` and lists trigger phrases.
- **Building blocks and content modules have *neutral* descriptions** so they don't compete with presentation-type triggers. They get loaded by Read path from inside a triggered workflow.
- Preserve this distinction when you edit frontmatter. Promoting a building block to auto-trigger creates trigger collision; demoting a presentation type to neutral breaks its discoverability.

---

## Cross-reference path style

- Cross-references between framework files use **root-relative paths** (`framework/building-blocks/deck-build.md`) when referenced from outside the `framework/` folder, and **plain filename or relative path** when referenced from within `framework/`.
- Don't introduce a different path style. The sweep procedure in `docs/maintainer/README.md` assumes this convention.

---

## Worked-example consistency

- The canonical worked example across the framework is **Hyponatremia / SIADH** — used in `framework/presentation-types/topic-review.md`, `framework/building-blocks/references.md`, `framework/content-modules/paper-summary.md`, and the README walkthrough.
- If you change the canonical topic, change it everywhere in one commit. Inconsistent worked examples confuse adopters.

---

## File-loading flow

Different tools load different files. Knowing the loading order helps when debugging "why didn't Claude see X?"

- **Cowork** auto-loads `CLAUDE.md` (the thin pointer); Claude then Reads `AGENTS.md` for substantive framework content.
- **Claude Code (desktop and web)** auto-loads both `CLAUDE.md` AND `AGENTS.md`.
- **OpenAI Codex, Aider, Ollama wrappers** auto-load `AGENTS.md` directly (they don't read `CLAUDE.md`).
- **In a maintainer session**, the `## For maintainers` block in `AGENTS.md` instructs Claude to also load `docs/maintainer/README.md` (and any local `MAINTAINER.md` if present).

The `CLAUDE.md` ↔ `AGENTS.md` split (with `CLAUDE.md` as the thin pointer) is documented in the project commit history. Search `git log --oneline | grep -i inversion` for the commit that introduced the inversion and the rationale.

---

## Skill packaging — folder-loaded vs `.skill`-bundled

The framework currently uses both forms:

- **Folder-loaded skills** (most building blocks, all presentation types, all content modules): live in `framework/` and load via Read path from inside a workflow. Not installable standalone.
- **`.skill`-bundled skills** (currently `sources-fetch` and `librarian`): live as `.skill` bundles at the workspace root. Installed by Cowork on first run; can be re-installed manually. Useful when the skill needs to be triggerable from outside the framework folder.

The bundling rationale for the two `.skill` items is documented in `AGENTS.md` Section 0 ("What's bundled, what's not — and why"). The trade-off: bundled skills add a second update step for users (re-install after `git pull` if the bundle changed), folder-loaded skills only need `git pull`.

When considering whether a new building block should be bundled, ask: does it need cross-context triggering? If no, keep it folder-loaded.

---

## Sources of truth

- For framework *defaults* (font sizes, palette, etc.): the constants block at the top of `framework/building-blocks/deck-build.md` Step 2 is canonical. Any prose elsewhere that mentions specific values should match it.
- For *workflow phases*: each presentation-type skill defines its own phases. Building blocks describe mechanics, not phases.
- For *user paths*: `README.md` "Pick your path" is canonical for users; `docs/maintainer/README.md` "User contexts" is the maintainer mirror. Keep both in sync.
- For *historical backstory*: `framework/retrospective.md` is the only place project history belongs. Don't let backstory creep into framework files.
