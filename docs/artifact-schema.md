# S2D Lab Artifact Schemas

This document defines the structure and required fields for all handoff artifacts in the S2D Lab workflow.

## Purpose

Standardized artifact schemas enable:
- Version tracking and integrity verification
- Automated validation before processing
- Clear dependency chains (which artifacts depend on which)
- Efficient selective loading (don't include full artifacts if only metadata needed)
- Resume protocol (verify expected files exist with correct versions)

## Common Frontmatter Fields

All artifacts use YAML frontmatter + Markdown body format:

```yaml
---
artifact_type: "question_map" | "research_packet" | "verification_report" | "final_report"
version: "v1" | "v2" | "v3" | "v4"
run_id: "<YYYY-MM-DD-short-slug>"
created_by: "conversation-analyst" | "quant-researcher" | "independent-auditor" | "research-lead"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
source_refs:
  - path: "runs/.work/<run-id>/source.md"
    type: "conversation"
  - path: "runs/.work/<run-id>/01-question-map-v1.md"  # if applicable
    type: "question_map"
    version: "v1"
---
```

### Field Descriptions

- **artifact_type** (required): Type discriminator for validation
- **version** (required): Explicit version (v1, v2, v3, v4). Max v4 per cycle limit.
- **run_id** (required): Unique run identifier for grouping artifacts
- **created_by** (required): Agent that produced this artifact
- **created_at** (required): ISO 8601 timestamp
- **source_refs** (required): List of input artifacts/sources used to create this artifact
  - Each ref: `path`, `type`, optionally `version`

## Question Map Schema

```yaml
---
artifact_type: "question_map"
version: "v1"  # or v2, v3, v4
run_id: "2026-11-08-example"
created_by: "conversation-analyst"
created_at: "2026-11-08T10:00:00Z"
source_refs:
  - path: "runs/.work/2026-11-08-example/source.md"
    type: "conversation"

# If revision (v2+):
revision_of: "v1"
change_requests_addressed:
  - cr_id: "CR-001"
    status: "resolved"
    summary: "Added omitted explicit question Q3"
resolution_notes: |
  CR-001: Added Q3 (gold-equity correlation) raised by Eric (line 14).
  Q3 classified as EXPLICIT_QUESTION, attributed to Eric, sourced line 14.
  All acceptance criteria met.
---

# Question Map v1

## Questions Extracted

### Q1 — [Question text]
- **ID:** Q1
- **Class:** EXPLICIT_QUESTION | IMPLIED_QUESTION | PARTICIPANT_CONCERN | RESEARCHER_ADDED_CONTEXT
- **Raised by:** [Participant name]
- **Decision owner:** [Participant or "unknown"]
- **Source span:** lines X-Y OR "turn at HH:MM"
- **Source quote:** "[exact quote]"
- **What they need:** [Decision/information need]
- **Confidence:** HIGH | MEDIUM | LOW
- **Ambiguities:** [If any]
- **Priority:** HIGH | MEDIUM | LOW
- **Reason:** [Why this priority]

[Repeat for each question]

## Questions Not Researchable

### Q4 — [Question text]
- **Reason:** NOT_RESEARCHABLE_INSUFFICIENT_CONTEXT | RHETORICAL | [other]

## Participant Positions and Disagreements

[If applicable]

## Explicit Constraints and Preferences

[With provenance: participant-stated, inferred, or unknown]

## Missing Inputs

[What information is needed but not available]
```

### Required Question Fields

Each question must have:
- ID (Q1, Q2, ...) — stable across versions
- Class (one of 4 types)
- Raised by (participant attribution)
- Source span (line numbers or time)
- What they need (interpretation of intent)
- Confidence (in interpretation)
- Priority (with brief reason)

## Research Packet Schema

```yaml
---
artifact_type: "research_packet"
version: "v1"
run_id: "2026-11-08-example"
created_by: "quant-researcher"
created_at: "2026-11-08T11:00:00Z"
source_refs:
  - path: "runs/.work/2026-11-08-example/source.md"
    type: "conversation"
  - path: "runs/.work/2026-11-08-example/01-question-map-v1.md"
    type: "question_map"
    version: "v1"

# If revision (v2+):
revision_of: "v1"
change_requests_addressed:
  - cr_id: "CR-001"
    status: "resolved"
resolution_notes: |
  CR-001: Corrected calculation Q1 from simple to compound interest.
  Arithmetic verified: $100,000 × 1.08^5 = $146,932.81.
  All acceptance criteria met.
---

# Research Packet v1

## Q1 — [Question text]

### Answer
[Direct answer to the question]

### Options Considered

| Option | Fit | Benefits | Trade-offs | Evidence |
|---|---|---|---|---|

### Best-Supported Option
**Option:** [name]  
**Criteria:** [traceable to participant/inferred/proposed]  
**Why it wins:** [explanation]  
**Main compromise:** [trade-off]  
**When another option is better:** [conditions]  
**What could change this:** [new evidence/criteria]

### Claims

**Claim C1.1** — [Claim statement]
- **Claim ID:** C1.1
- **Type:** FACT | INTERPRETATION | HYPOTHESIS | RECOMMENDATION
- **Evidence:** [Source + access status]
- **Confidence:** HIGH | MEDIUM | LOW
- **Depends on:** [] (list of claim IDs this claim relies on, empty if independent)

**Claim C1.2** — [Another claim]
- **Claim ID:** C1.2
- **Depends on:** ["C1.1"] (this recommendation depends on fact C1.1)

[Continue for all material claims]

### Calculations

**Calculation:** [Name]
- **Inputs:** [List with units and sources]
- **Formula:** [Explicit formula]
- **Steps:** [Intermediate steps]
- **Result:** [Value with units]
- **Timestamp:** [When calculated / data date]
- **Assumptions:** [Stated assumptions]

### Sources

**Source 1:** [Title/Description]
- **URL/Reference:** [if applicable]
- **Access status:** FULL_TEXT_OPENED | OFFICIAL_DATA_OR_API_RETRIEVED | SEARCH_SNIPPET_ONLY | METADATA_ONLY | INACCESSIBLE | USER_SUPPLIED
- **Claims supported:** [List of claim IDs]
- **Date accessed:** [ISO date]

### Confidence and Limitations

[What's uncertain, missing data, verification limits]

[Repeat structure for each question]
```

### Required Research Packet Elements

Per question:
- Direct answer
- Options (if decision question, 2-4 when feasible)
- Best-supported option with criteria provenance
- **Claims with stable claim_ids** (NEW in C1)
- **Claim dependencies** (NEW in C1)
- Evidence with access status
- Calculations with shown work
- Confidence and limitations

### Claim ID Convention

Format: `Q{question_number}.{claim_number}`

Examples:
- C1.1 — First claim for Q1
- C1.2 — Second claim for Q1
- C2.1 — First claim for Q2

Claim IDs are **stable**: If Q1 has claims C1.1, C1.2, C1.3 in v1, and v2 adds C1.4, the original IDs don't change.

## Verification Report Schema

```yaml
---
artifact_type: "verification_report"
version: "v1"  # increments with each recheck
run_id: "2026-11-08-example"
created_by: "independent-auditor"
created_at: "2026-11-08T12:00:00Z"
audit_mode: "baseline" | "differential"
artifact_under_review:
  type: "research_packet"
  path: "runs/.work/2026-11-08-example/02-research-packet-v1.md"
  version: "v1"
source_refs:
  - path: "runs/.work/2026-11-08-example/source.md"
    type: "conversation"
    accessible: true  # or false if BLOCKED
  - path: "runs/.work/2026-11-08-example/01-question-map-v1.md"
    type: "question_map"
    version: "v1"

# For differential audits only:
change_requests_under_review:
  - cr_id: "CR-001"
    finding_id: "F-001"
    severity: "MAJOR"

cycle_number: 0  # 0 = baseline, 1-3 for rechecks

verdict: "PASS" | "PASS_WITH_LIMITATIONS" | "CHANGES_REQUESTED" | "BLOCKED"
---

# Verification Report

[See templates/VERIFICATION-REPORT.md for full body structure]

## Findings

### Finding F-001
[Full finding structure with claim_ids in recheck scope]
```

## Final Report Schema

```yaml
---
artifact_type: "final_report"
version: "v1"
run_id: "2026-11-08-example"
created_by: "research-lead"
created_at: "2026-11-08T13:00:00Z"
source_refs:
  - path: "runs/.work/2026-11-08-example/source.md"
    type: "conversation"
  - path: "runs/.work/2026-11-08-example/01-question-map-v2.md"
    type: "question_map"
    version: "v2"
  - path: "runs/.work/2026-11-08-example/02-research-packet-v2.md"
    type: "research_packet"
    version: "v2"
  - path: "runs/.work/2026-11-08-example/03-verification-research-v2.md"
    type: "verification_report"
    version: "v2"

# If revision (v2+):
revision_of: "v1"
change_requests_addressed:
  - cr_id: "CR-005"
    status: "resolved"
resolution_notes: |
  CR-005: Removed unsupported claim introduced during synthesis.
---

# [Report Title]

[See templates/conversation-research-recap.md for structure]
```

## State Schema (Enhanced)

See `templates/run-state.yaml` for full structure. Key additions for C1:

```yaml
artifacts:
  question_map:
    current_version: "v2"
    path: "runs/.work/<run-id>/01-question-map-v2.md"
    sha256: "<hash>"  # optional integrity check
    cycle_count: 1
    status: "pass"
  
  research_packet:
    current_version: "v2"
    path: "runs/.work/<run-id>/02-research-packet-v2.md"
    sha256: "<hash>"
    cycle_count: 1
    status: "pass"
    claim_ids: ["C1.1", "C1.2", "C2.1", "C2.2", "C2.3"]  # all claims in current version
```

## Validation Rules

### Version Rules
- Version must be v1, v2, v3, or v4
- Version cannot skip (v1 → v3 without v2 is invalid)
- Max version is v4 (cycle limit)

### Revision Rules
- If version > v1: must have `revision_of` and `change_requests_addressed`
- `revision_of` must be previous version (v2 revises v1, v3 revises v2, etc.)

### Source Reference Rules
- All artifacts must reference original conversation source
- Derived artifacts must reference their inputs (e.g., Research Packet references Question Map)
- Source paths must be resolvable at validation time

### Claim ID Rules
- Claim IDs must be stable across versions (don't renumber existing claims)
- New claims get next available number
- Removed claims: ID retired (not reused)
- `depends_on` must reference valid claim IDs from same or prior version

## Implementation Notes

### Frontmatter Parsing
- Use YAML parser (Python: `yaml.safe_load`, JS: `js-yaml`)
- Split on `---` markers (first occurrence after optional initial `---`)
- Markdown body follows closing `---`

### Validation Script (Placeholder)
```bash
# Planned: scripts/validate-artifact.py
python scripts/validate-artifact.py runs/.work/<run-id>/02-research-packet-v1.md
# Checks: required fields, version sequence, source refs, claim ID format
```

### Backward Compatibility
Existing artifacts without frontmatter are grandfathered. New artifacts created after C1 implementation must include frontmatter.

---

**Created:** 2026-11-08 (Task C1)  
**Status:** Schema defined, implementation in progress  
**Next:** Update agent prompts to produce compliant artifacts
