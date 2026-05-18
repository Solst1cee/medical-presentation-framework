# Roadmap — parked ideas

Ideas considered during framework development but deliberately deferred. Capture here so they survive across sessions and tools rather than getting re-discovered every time.

---

## Deferred — revisit when conditions change

- **`.claude-plugin/marketplace.json` for plugin discoverability.** Deferred until Claude Code plugin-update bug ([anthropics/claude-code#19197](https://github.com/anthropics/claude-code/issues/19197)) is resolved — currently, plugin installs are pinned to a commit SHA and users have to force-reinstall to get updates. Revisit when the bug ships a fix.

- **Wave 1 ad-hoc utility skills.** Considered promoting content modules (`evidence-grading`, `clinical-depth`, `disease-comparison`, `local-guideline`, `paper-summary`) to standalone installable skills so they can be invoked from plain Claude chat or the iOS app for non-framework micro-tasks. Deferred — would dilute the workflow discipline that gives the framework its quality, and split the framework's mission. Revisit if real demand surfaces from users.

- **Sibling project "Medical Assistant Skills".** If ad-hoc skill demand grows, spin off as a separate repo with separate scope rather than blurring into the presentation framework. Different audience, different update cadence.

- **Rename `MAINTAINER.md` to `CLAUDE.local.md`.** Anthropic has an official convention where Claude Code auto-loads `CLAUDE.local.md` after `CLAUDE.md`, and `.local.*` files are auto-gitignored. Adopting this would replace the bespoke `MAINTAINER.md` presence-check with an established Anthropic convention. Defer until either Anthropic strengthens documentation around it or until the bespoke pattern shows wear.

---

## Distribution / discovery — once the framework feels stable

- **[awesome-claude-code issue #1389](https://github.com/hesreallyhim/awesome-claude-code/issues/1389)** ("Medical Research Skills") is an open demand signal in the canonical Claude-skill curated list — post a link to the framework once it has been used through several real presentations and the workflow has settled.

- **Public release** — currently the framework is GitHub-public but not promoted. Once a few external users have walked through the install path successfully, consider announcing more widely (residency-program channels, medical-education forums).

---

## Comparable projects worth periodically checking

All similar in topology, useful for cross-referencing design decisions:

- [`Galaxy-Dawn/claude-scholar`](https://github.com/Galaxy-Dawn/claude-scholar) — academic research framework, ~25 skills + setup script with full/minimal/selective install modes; chose plain git over plugin packaging.
- [`K-Dense-AI/claude-scientific-writer`](https://github.com/K-Dense-AI/claude-scientific-writer) — scientific writing framework; chose hybrid (Claude Code plugin OR `git clone` + `uv sync`).
- [`levnikolaevich/claude-code-skills`](https://github.com/levnikolaevich/claude-code-skills) — explicit L0–L3 layered architecture; closest architectural twin to this framework.

---

## Operational watch items

- **Edit-tool truncation watch.** Bug is recurring on medium-sized files in both Cowork and Claude Code. Workaround: write or rewrite via Python heredoc through bash rather than the Edit tool. Documented in `framework/retrospective.md` Case 2 #9.

---

*Ideas that mature into action should move out of this file — either into the appropriate framework file, or into a commit/PR. Stale ideas get pruned, not preserved indefinitely.*
