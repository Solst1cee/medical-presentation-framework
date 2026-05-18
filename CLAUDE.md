# CLAUDE.md — Medical Presentation Framework

The framework's instructions live in **`AGENTS.md`** at the workspace root.
Read that file first — it has the full architecture, conventions, workflows,
folder structure, library configuration, and the "for maintainers" guidance.

This file exists so Claude tools that auto-load `CLAUDE.md` (Claude Cowork,
Claude Code) find the pointer. The substantive content lives in `AGENTS.md`
so other agentic coding tools that read the `AGENTS.md` convention (OpenAI
Codex, Aider, Ollama wrappers, etc.) work too.

---

## Claude-specific notes

### Cowork: install the `.skill` bundles when prompted

The workspace root contains two `.skill` bundles: `sources-fetch.skill` and
`librarian.skill`. When Cowork prompts to install them on first open, accept.
They enable ad-hoc paper acquisition and library organization outside of a
presentation workflow.

### Claude Code: no extra setup

Claude Code (CLI or IDE plugin) auto-loads both `CLAUDE.md` and `AGENTS.md`.
No additional configuration needed beyond opening the folder.

### Claude — on the first session in a new environment, do this check

1. Look at the current `available_skills` list (in the system reminder).
2. For each `.skill` bundle present at the project root, check whether a
   matching skill name is already installed.
3. If any are missing, list them to the user and offer to install via
   `present_files` so they get a one-click install card. Do not install
   silently — let the user choose.

After install, the user may need to restart Cowork for the new skill to
appear in `available_skills`.
