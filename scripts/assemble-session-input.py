#!/usr/bin/env python3
"""
Assemble a writing session input package for a given section.

Usage:
    python scripts/assemble-session-input.py 1.1.1

Reads the Section Brief, extracts relevant files, and produces
a single concatenated session input file.
"""

import sys
import os
import re
from pathlib import Path

# Chapter number to directory name mapping
CHAPTER_DIRS = {
    "0": "00-introduction",
    "1": "01-problem-domain",
    "2": "02-theoretical-foundations",
    "3": "03-methodology",
    "4": "04-experiments",
    "5": "05-validation",
    "6": "06-system-architecture",
    "7": "07-conclusion",
}

def estimate_tokens(text: str) -> int:
    """Rough token estimate: words * 1.3"""
    return int(len(text.split()) * 1.3)

def get_chapter_dir(section_id: str) -> str:
    chapter_num = section_id.split(".")[0]
    return CHAPTER_DIRS.get(chapter_num, f"{chapter_num.zfill(2)}-unknown")

def read_file(path: str) -> str:
    """Read file, return content or empty string with warning."""
    p = Path(path)
    if p.exists():
        return p.read_text(encoding="utf-8")
    else:
        print(f"  WARNING: File not found: {path}")
        return ""

def extract_lit_cards_from_brief(brief_text: str) -> list:
    """Extract literature card filenames from the SOURCE MAPPING table."""
    cards = []
    # Match filenames like word-word-word.md or word-year.md
    for match in re.finditer(r'[a-z][\w-]*\.md', brief_text):
        fname = match.group()
        if fname not in ("brief.md", "input.md", "draft.md", "template.md"):
            cards.append(fname)
    return list(set(cards))

def find_preceding_section(section_id: str) -> str:
    """Compute preceding section ID (simplified: just decrement last number)."""
    parts = section_id.split(".")
    last = int(parts[-1])
    if last > 1:
        parts[-1] = str(last - 1)
        return ".".join(parts)
    return ""

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/assemble-session-input.py <section_id>")
        print("Example: python scripts/assemble-session-input.py 1.1.1")
        sys.exit(1)

    section_id = sys.argv[1]
    chapter_dir = get_chapter_dir(section_id)
    base = Path(".")

    print(f"Assembling session input for §{section_id}")
    print(f"Chapter directory: chapters/{chapter_dir}")
    print()

    parts = []
    total_tokens = 0

    # 1. System prompt
    sp = read_file("prompts/writing-session-system-prompt.md")
    if sp:
        parts.append(("SYSTEM PROMPT", sp))
        print(f"  [1] System prompt: {estimate_tokens(sp)} tokens")

    # 2. INVARIANTS.md (always full)
    inv = read_file("governance/INVARIANTS.md")
    if inv:
        parts.append(("INVARIANTS.md", inv))
        print(f"  [2] INVARIANTS.md: {estimate_tokens(inv)} tokens")

    # 3. Section Brief
    brief_path = f"chapters/{chapter_dir}/briefs/section-{section_id}-brief.md"
    brief = read_file(brief_path)
    if brief:
        parts.append(("SECTION BRIEF", brief))
        print(f"  [3] Section Brief: {estimate_tokens(brief)} tokens")
    else:
        print(f"  ERROR: Section Brief not found at {brief_path}")
        print(f"  Generate it first using the Section Brief template.")
        sys.exit(1)

    # 4. Continuity Note from preceding section
    prev_id = find_preceding_section(section_id)
    if prev_id:
        cont_path = f"chapters/{chapter_dir}/continuity/section-{prev_id}-continuity.md"
        cont = read_file(cont_path)
        if cont:
            parts.append(("CONTINUITY NOTE (preceding section)", cont))
            print(f"  [4] Continuity Note §{prev_id}: {estimate_tokens(cont)} tokens")

        # Also try to get preceding section's last paragraph
        draft_path = f"chapters/{chapter_dir}/drafts/section-{prev_id}-draft.md"
        draft = read_file(draft_path)
        if draft:
            last_para = draft.strip().split("\n\n")[-1]
            parts.append(("PRECEDING SECTION FINAL PARAGRAPH", last_para))
            print(f"  [5] Preceding final paragraph: {estimate_tokens(last_para)} tokens")

    # 5. Literature cards (extracted from brief)
    if brief:
        card_files = extract_lit_cards_from_brief(brief)
        print(f"  [6] Literature cards found in brief: {len(card_files)}")
        for cf in sorted(card_files):
            # Search in external and self directories
            for subdir in ["external", "self", "non-peer-reviewed"]:
                card_path = f"literature/{subdir}/{cf}"
                if Path(card_path).exists():
                    card_text = read_file(card_path)
                    parts.append((f"LITERATURE CARD: {cf}", card_text))
                    print(f"       {cf}: {estimate_tokens(card_text)} tokens")
                    break

    # Assemble output
    output_lines = []
    for title, content in parts:
        output_lines.append(f"\n{'='*60}")
        output_lines.append(f"# {title}")
        output_lines.append(f"{'='*60}\n")
        output_lines.append(content)

    output_text = "\n".join(output_lines)
    total_tokens = estimate_tokens(output_text)

    # Write output
    output_dir = Path(f"chapters/{chapter_dir}/sessions")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"section-{section_id}-input.md"
    output_path.write_text(output_text, encoding="utf-8")

    print()
    print(f"Session input written to: {output_path}")
    print(f"Total estimated tokens: {total_tokens}")
    if total_tokens > 50000:
        print(f"  WARNING: Token count exceeds 50K budget. Consider reducing literature cards.")
    elif total_tokens > 35000:
        print(f"  OK: Within 35K-50K target range.")
    else:
        print(f"  OK: Under 35K — room for additional context if needed.")

if __name__ == "__main__":
    main()
