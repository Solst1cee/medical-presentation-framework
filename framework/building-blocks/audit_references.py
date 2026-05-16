#!/usr/bin/env python3
"""Reference audit — cross-checks slide citations, master reference list, and Sources/ folder.

USAGE
  python3 audit_references.py "Documents/{Topic} outline.md" [Sources/]

Reports four categories of issues:
  1. ORPHANED   — entry exists in master reference list but not cited on any slide
  2. BROKEN     — citation appears on a slide but no matching master-list entry
  3. STALE row  — sources summary table has a row for a number not in master list
  4. UNMATCHED  — file in Sources/ doesn't match any master-list entry by filename heuristics

Designed to run at these workflow checkpoints (see `reference-audit.md` for full integration):
  - When the user requests slide / section removal     → run BEFORE+AFTER, diff orphans
  - End of Phase 3 — "finalize outline"                → block transition if BROKEN exist
  - Start of Phase 4 — "build deck"                    → run as first step
  - Phase 6 final reconciliation                       → automated alternative to manual walk-through

Output is plain text. Exit code 0 if all reconciled; 1 if any issues found; 2 on error.
"""
from __future__ import annotations
import argparse, os, re, sys
from pathlib import Path


def extract_cited_refs(slide_region: str) -> dict[int, list[str]]:
    """Return {ref_num: [slide titles where cited]} found in **Ref:** lines.

    Robust to false positives like 'Table 90.4' or 'Ch 90' — only counts numbers
    that look like a citation (after **Ref:**, comma-separated, not preceded by
    Ch/Fig/Table/Vol).
    """
    cited: dict[int, list[str]] = {}
    current_slide = "?"
    for line in slide_region.split("\n"):
        m = re.match(r"^### Slide \d+\w?\s*[—–-]\s*(.+)", line)
        if m:
            current_slide = m.group(1).strip()[:60]
            continue
        if "**Ref:**" not in line:
            continue
        after = line.split("**Ref:**", 1)[1]
        # Strip parentheticals
        after = re.sub(r"\([^)]*\)", "", after)
        # Strip italic/bold wrappers
        after = re.sub(r"[*_]+", "", after)
        for seg in re.split(r"[,·•;]", after):
            seg = seg.strip()
            if not seg:
                continue
            m_num = re.match(r"^(\d{1,2})\b", seg)
            if not m_num:
                continue
            n = int(m_num.group(1))
            if 1 <= n <= 99:
                cited.setdefault(n, []).append(current_slide)
    return cited


def extract_master_list(text_before_slides: str) -> dict[int, str]:
    master: dict[int, str] = {}
    for line in text_before_slides.split("\n"):
        m = re.match(r"^(\d{1,3})\.\s+(.+)$", line)
        if not m:
            continue
        n = int(m.group(1))
        if not (1 <= n <= 200):
            continue
        citation = m.group(2).strip()
        citation = re.sub(r"\*+([^*]+)\*+", r"\1", citation).strip()
        # Don't truncate — full citation needed for chapter-number / "Kelley" / "Harrison" tokens
        # that often appear in the second half of long Vancouver-style citations.
        master[n] = citation
    return master


def extract_sources_summary(text: str) -> dict[int, dict]:
    sources: dict[int, dict] = {}
    sec = re.search(r"### Sources summary[\s\S]+?(?=\n### |\n## |\Z)", text)
    if not sec:
        return sources
    for m in re.finditer(
        r"^\|\s*(\d{1,3})\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
        sec.group(),
        re.MULTILINE,
    ):
        sources[int(m.group(1))] = {
            "short_name": m.group(2).strip(),
            "type": m.group(3).strip(),
            "location": m.group(4).strip(),
            "status": m.group(5).strip(),
        }
    return sources


def parse_outline(outline_path: Path):
    text = outline_path.read_text(encoding="utf-8")
    try:
        start_idx = text.index("▼ SLIDE DECK CONTENT")
        end_idx = text.index("▲ END OF SLIDE DECK CONTENT")
    except ValueError:
        return None, None, None, "boundary markers (▼ / ▲) missing"
    slide_region = text[start_idx:end_idx]
    metadata_region = text[:start_idx]

    cited = extract_cited_refs(slide_region)
    master = extract_master_list(metadata_region)
    sources = extract_sources_summary(text)
    return cited, master, sources, None


STOPWORDS = {
    "the", "and", "with", "for", "from", "into", "of",
    "criteria", "guideline", "consensus", "review", "paper",
    "acr", "eular", "ar", "rheum", "rheumatol",
    "vol", "ed", "edition", "ch", "chapter",
}


def _stem(tok: str) -> str:
    """Crude singular-form normalization: 'harrisons' → 'harrison'."""
    if len(tok) > 5 and tok.endswith("s") and not tok.endswith("ss"):
        return tok[:-1]
    return tok


def filename_tokens(filename: str) -> set:
    base = re.sub(r"\.(pdf|docx|epub)$", "", filename, flags=re.IGNORECASE)
    # Detect Ch{N} BEFORE splitting on dashes — preserves the chapter signal
    chapter_toks = {f"ch{m.group(1)}" for m in re.finditer(r"\bCh\.?\s*(\d{1,3})\b", base, re.IGNORECASE)}
    base = re.sub(r"[_\-\(\)\.,]", " ", base)
    tokens = set(chapter_toks)
    for tok in base.split():
        tok_lower = tok.lower()
        if re.match(r"^(19|20)\d{2}$", tok):
            tokens.add(tok)
            continue
        if len(tok) >= 4 and tok[0].isupper() and tok_lower not in STOPWORDS:
            tokens.add(_stem(tok_lower))
    return tokens


def citation_tokens(citation: str) -> set:
    """Author-like (Capitalized 4+), year, and chapter-number tokens.

    Uses non-capturing group `(?:19|20)` for the year so re.findall returns the
    full year match. Detects Ch.N patterns separately to preserve chapter signal.
    """
    tokens = set()
    for tok in re.findall(r"\b[A-Z][a-z]{3,}\b|\b(?:19|20)\d{2}\b", citation):
        tokens.add(_stem(tok.lower()))
    for m in re.finditer(r"\bCh\.?\s*(\d{1,3})\b", citation):
        tokens.add(f"ch{m.group(1)}")
    return tokens


def match_file_to_master(fname: str, master: dict) -> int | None:
    f_toks = filename_tokens(fname)
    if not f_toks:
        return None
    best_n, best_overlap = None, 0
    for n, citation in master.items():
        c_toks = citation_tokens(citation)
        overlap = len(f_toks & c_toks)
        if overlap > best_overlap and overlap >= 2:
            best_n, best_overlap = n, overlap
    return best_n


def file_appears_present(status_str: str) -> bool:
    return "✅" in status_str


def audit(outline_path: Path, sources_dir):
    cited, master, sources, err = parse_outline(outline_path)
    if err:
        print(f"❌ Could not parse outline: {err}")
        return 2

    cited_nums = set(cited.keys())
    master_nums = set(master.keys())

    in_use = cited_nums & master_nums
    orphan_in_master = master_nums - cited_nums
    broken_cite = cited_nums - master_nums

    print("=" * 78)
    print(f"REFERENCE AUDIT — {outline_path}")
    print("=" * 78)
    print(f"  Master list entries:   {len(master)}")
    print(f"  Cited on slides:       {len(cited_nums)}")
    print(f"  In use (matched):      {len(in_use)}")
    print()

    issues = 0

    if orphan_in_master:
        issues += len(orphan_in_master)
        print(f"⚠  ORPHANED — in master list but not cited on any slide ({len(orphan_in_master)}):")
        for n in sorted(orphan_in_master):
            print(f"   [{n:>2}]  {master[n][:130]}")
        print("    → Recommended: remove from master list. Keep PDF in Sources/ if user wants it.")
        print()

    if broken_cite:
        issues += len(broken_cite)
        print(f"❌ BROKEN — cited on a slide but no master-list entry ({len(broken_cite)}):")
        for n in sorted(broken_cite):
            slides = ", ".join(cited[n][:3])
            print(f"   [{n:>2}]  cited on: {slides}")
        print("    → Recommended: add entry to master list, or fix the citation.")
        print()

    if sources:
        print(f"\U0001f4c1 SOURCES SUMMARY ({len(sources)} entries):")
        for n in sorted(sources.keys()):
            entry = sources[n]
            in_master = n in master_nums
            used = n in cited_nums
            file_present = file_appears_present(entry["status"])

            if not in_master:
                tag = "⚠  STALE ROW (not in master list)"
                issues += 1
            elif not used:
                if file_present:
                    tag = "○ unused (file present)"
                    issues += 1
                else:
                    tag = "○ unused (no file)"
            elif file_present:
                tag = "✓ used (file present)"
            else:
                tag = "⏳ used (file pending fetch)"

            print(f"   [{n:>2}] {tag:<37} {entry['short_name'][:55]}")
        print()

    if sources_dir and Path(sources_dir).is_dir():
        files = sorted(
            f for f in os.listdir(sources_dir)
            if f.lower().endswith((".pdf", ".docx", ".epub")) and not f.startswith(".")
        )
        print(f"\U0001f4c2 FILES IN {sources_dir} ({len(files)} files):")
        unmatched_files = []
        for fname in files:
            matched_n = match_file_to_master(fname, master)
            if matched_n is None:
                unmatched_files.append(fname)
                print(f"   ⚠  {fname[:75]:<75}  no master-list match")
            else:
                used_tag = "✓ in use" if matched_n in cited_nums else "○ not cited"
                print(f"      {fname[:75]:<75}  [{matched_n:>2}]  {used_tag}")
        if unmatched_files:
            issues += len(unmatched_files)
            print(f"    → {len(unmatched_files)} file(s) in Sources/ have no matching master-list entry.")
            print(f"      Either add to master list, or move out of Sources/ if no longer needed.")
        print()

    if issues == 0:
        print("✅ All references reconciled.")
        return 0
    print(f"⚠  Total issues to resolve: {issues}")
    return 1


def main():
    ap = argparse.ArgumentParser(description="Reference audit for medical-presentation-framework outlines.")
    ap.add_argument("outline", help="Path to {Topic} outline.md")
    ap.add_argument("sources", nargs="?", default=None, help="Path to Sources/ folder (optional)")
    args = ap.parse_args()

    outline_path = Path(args.outline)
    if not outline_path.is_file():
        print(f"❌ Outline not found: {outline_path}")
        sys.exit(2)
    sources_dir = args.sources

    sys.exit(audit(outline_path, sources_dir))


if __name__ == "__main__":
    main()
