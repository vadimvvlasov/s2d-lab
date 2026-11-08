#!/usr/bin/env python3
"""
Extract ground truth from fixture markdown files for E2 evaluation.

Usage:
    uv run --with pyyaml scripts/extract-ground-truth.py tests/fixtures/01-short-simple.md

Output:
    tests/ground-truth/fx01.json
"""

import argparse
import json
import re
from pathlib import Path
from typing import Any


def parse_fixture_markdown(content: str) -> dict[str, Any]:
    """
    Parse fixture markdown and extract expected outputs.

    Returns dict with:
    - fixture_id
    - expected_questions: list of {id, text, type, raised_by}
    - expected_claims: list of {id, statement, evidence_refs}
    - seeded_defects: list of {severity, category, artifact}
    - expected_verdicts: dict artifact -> verdict
    - success_criteria: list of strings
    """
    result = {
        "fixture_id": None,
        "expected_questions": [],
        "expected_claims": [],
        "expected_evidence": [],
        "seeded_defects": [],
        "expected_verdicts": {},
        "success_criteria": [],
        "conversation": "",
    }

    # Extract fixture ID from title
    if m := re.search(r"# Fixture (\d+):", content):
        result["fixture_id"] = f"fx{m.group(1).zfill(2)}"

    # Extract conversation section
    conv_match = re.search(
        r"## Conversation\s+\*\*Date:\*\*.*?\n\*\*Participants:\*\*.*?\n+---+(.*?)(?=\n## |$)",
        content,
        re.DOTALL,
    )
    if conv_match:
        result["conversation"] = conv_match.group(1).strip()

    # Extract expected questions from "Expected Question Map" section
    questions_section = re.search(
        r"## Expected Question Map.*?(?:### Questions Extracted|###)(.*?)(?=### |## |$)",
        content,
        re.DOTALL,
    )
    if questions_section:
        question_blocks = re.finditer(
            r"\*\*Q(\d+) — (.*?)\*\*\s*\n- Class: `([^`]+)`\s*\n- Raised by: (\w+)",
            questions_section.group(1),
            re.DOTALL,
        )
        for qmatch in question_blocks:
            qnum, qtext, qclass, raised_by = qmatch.groups()
            result["expected_questions"].append(
                {
                    "id": f"Q{qnum}",
                    "text": qtext.strip(),
                    "type": qclass,
                    "raised_by": raised_by,
                }
            )

    # Extract seeded defects from "Seeded Defect" section
    defect_section = re.search(r"## Seeded Defect\s+(.*?)(?=## |$)", content, re.DOTALL)
    if defect_section:
        # Look for defect description
        defect_text = defect_section.group(1).strip()
        if "invents" in defect_text.lower() or "defect" in defect_text.lower():
            # Parse from "Expected Baseline Audit" section for details
            audit_section = re.search(
                r"## Expected Baseline Audit.*?\*\*Finding F-\d+:\*\*\s+- \*\*Severity:\*\* (\w+)\s+- \*\*Category:\*\* ([\w_]+)",
                content,
                re.DOTALL,
            )
            if audit_section:
                severity, category = audit_section.groups()
                result["seeded_defects"].append(
                    {
                        "severity": severity,
                        "category": category,
                        "artifact": "research_packet_v1",  # Common pattern
                        "description": defect_text[:200],
                    }
                )

    # Extract expected verdicts from audit sections
    # Pattern: "**Expected Verdict:** PASS" or "**Verdict:** CHANGES_REQUESTED"
    verdict_matches = re.finditer(r"\*\*(?:Expected )?Verdict:\*\* ([\w_]+)", content)
    for i, vmatch in enumerate(verdict_matches):
        verdict = vmatch.group(1)
        # Try to determine which artifact this is for
        # Simple heuristic: first verdict is baseline audit v1
        artifact_key = f"baseline_audit_v{i + 1}"
        result["expected_verdicts"][artifact_key] = verdict

    # Extract success criteria from "Success Criteria" section
    criteria_section = re.search(
        r"## Success Criteria\s+(.*?)(?=##|$)", content, re.DOTALL
    )
    if criteria_section:
        criteria_lines = re.findall(
            r"- \[[ x]\] (.+?)(?:\n|$)", criteria_section.group(1)
        )
        result["success_criteria"] = [c.strip() for c in criteria_lines]

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Extract ground truth from fixture markdown files"
    )
    parser.add_argument("fixture_file", type=Path, help="Path to fixture .md file")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("tests/ground-truth"),
        help="Output directory for JSON files",
    )
    args = parser.parse_args()

    # Read fixture file
    content = args.fixture_file.read_text(encoding="utf-8")

    # Parse ground truth
    ground_truth = parse_fixture_markdown(content)

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Write JSON
    fixture_id = ground_truth["fixture_id"]
    if not fixture_id:
        # Fallback: extract from filename
        fixture_id = f"fx{args.fixture_file.stem.split('-')[0].zfill(2)}"
        ground_truth["fixture_id"] = fixture_id

    output_file = args.output_dir / f"{fixture_id}.json"
    output_file.write_text(
        json.dumps(ground_truth, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"✅ Ground truth extracted: {output_file}")
    print(f"   - Questions: {len(ground_truth['expected_questions'])}")
    print(f"   - Seeded defects: {len(ground_truth['seeded_defects'])}")
    print(f"   - Success criteria: {len(ground_truth['success_criteria'])}")


if __name__ == "__main__":
    main()
