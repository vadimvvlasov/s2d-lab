# Verifier and rework loop

## Overview

S2D Lab implements a bounded producer–verifier–rework loop to ensure quality and auditability of the Conversation Research Recap. The Independent Auditor independently verifies artifacts and the final report, routing defects back to the responsible agent for correction.

![Verifier workflow](assets/verifier-workflow.svg)

## Key principles

1. **Independent verification:** The auditor is read-only and works in a separate context. It reports findings but never edits artifacts.

2. **Bounded cycles:** Maximum 3 rework cycles per artifact. After cycle 3, unresolved findings escalate rather than continuing indefinitely.

3. **Explicit versioning:** Every artifact (Question Map, Research Packet, Final Report) has an explicit version (v1, v2, v3, v4).

4. **Source traceability:** The original conversation is stored in git-ignored run storage and accessible to every auditor invocation.

5. **Structured findings:** Every `BLOCKER` or `MAJOR` finding creates a Change Request with precise defect, evidence, required change, acceptance criteria, and recheck scope.

## Workflow phases

### 1. Source intake
The Research Lead stores the original conversation in `runs/.work/<run-id>/source.md` and records the run ID and timestamp. This source reference is passed to all subagents.

### 2. Question Map v1
The Conversation Analyst extracts questions and produces Question Map v1.

### 3. Research Packet v1
The Quant Researcher answers questions, compares options, and produces Research Packet v1.

### 4. Research audit (cycle 0)
The Independent Auditor reviews the Question Map and Research Packet, checking:
- Question attribution and extraction fidelity
- Source accessibility and verification status
- Calculations and evidence quality
- Option comparison fairness
- Recommendation logic

The auditor produces a Verification Report with verdict:
- `PASS`: no unresolved findings
- `PASS_WITH_LIMITATIONS`: no blocker; limitations explicit and bounded
- `CHANGES_REQUESTED`: `BLOCKER` or `MAJOR` requires fix
- `BLOCKED`: review cannot be completed (e.g., source unavailable)

### 5. Rework loop (max 3 cycles)
For each `BLOCKER` or `MAJOR` finding:
1. Lead creates a Change Request (CR) identifying the defect and routing it to the responsible agent
2. Producer creates a new artifact version (v2, v3, v4) with resolution notes
3. Auditor independently rechecks the affected scope and dependent claims
4. Cycle count increments

After cycle 3, unresolved findings are marked `ESCALATED_TO_OWNER`. No fourth cycle is started.

### 6. Synthesis
After research audit `PASS` or `PASS_WITH_LIMITATIONS` with no unresolved blocker, the Lead writes the Final Report v1.

### 7. Final report audit
The auditor reviews the final report against:
- Original conversation fidelity
- Question Map and Research Packet consistency
- Output contract compliance
- Evidence citations and accessibility
- Unsupported claims introduced during synthesis

### 8. Release gate
The report is released to `runs/YYYY-MM-DD-conversation-research-recap.md` only after:
- Final audit `PASS` or `PASS_WITH_LIMITATIONS`
- No unresolved `BLOCKER`

If the final report has a `BLOCKER` or `MAJOR`, the rework loop applies to the final report (max 3 cycles).

## Severity levels

- **BLOCKER:** Invalidates central conclusion, materially misrepresents source, makes output unreliable. Must fix or remove conclusion. No verified release while unresolved.

- **MAJOR:** Materially weakens evidence, calculations, comparison, recommendation, attribution, or fidelity. Must fix, or narrow the affected claim and disclose the limitation.

- **MINOR:** Localized clarity or completeness issue. Lead records a reasoned disposition (fix or accept with rationale). Does not block release.

## Change Request routing

- **Question attribution, extraction, splitting, omitted/merged questions:** conversation-analyst
- **Evidence, sources, calculations, options, recommendation logic:** quant-researcher
- **Synthesis, report wording, unsupported claims in final report:** research-lead
- **Orchestration, missing auditor inputs:** Lead fixes handoff and reruns auditor (not counted as a cycle)

## Escalation

If a `BLOCKER` or `MAJOR` finding remains unresolved after 3 cycles, it is escalated to the owner (user) with:
- Finding details and severity
- Producer and auditor positions
- Affected scope
- Decision needed

The user can:
- Accept the limitation and release with explicit disclosure (if not a blocker)
- Narrow or remove the affected claim
- Provide additional evidence or clarification
- Decide not to release

An unresolved blocker always prevents verified release.

## State persistence

Run state is maintained in `runs/.work/<run-id>/state.yaml` with:
- Run ID, timestamp, source reference
- Artifact versions and cycle counts
- Open Change Requests and their status
- Verification history
- Final audit status
- Release eligibility
- Current phase and next action

This enables resume after interruption and provides an audit trail.

## User experience

From the user's perspective:
1. Run `/recap` with a conversation
2. Receive one clean, verified Conversation Research Recap
3. Intermediate artifacts, Change Requests, and verification reports remain in `runs/.work/<run-id>/` for transparency but are not shown unless requested

The verifier loop ensures quality without exposing workflow ceremony in the final report.
