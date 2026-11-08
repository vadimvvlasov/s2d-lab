# Fixture 07: Cycle Limit and Escalation

**Type:** Workflow control test  
**Purpose:** Verify max 3 cycles enforced, escalation after cycle 3  
**Expected:** Escalation without cycle 4 or silent PASS

## Conversation

**Date:** 2026-11-08  
**Participants:** Ivan

---

**Ivan [16:00]:** Какие основные риски у высокодоходных облигаций (junk bonds)?

---

## Expected Question Map v1

**Q1 — Какие основные риски у высокодоходных облигаций?**
- Class: `EXPLICIT_QUESTION`
- Raised by: Ivan
- Source: line 10
- Priority: HIGH

## Scenario

This fixture tests workflow control, not content quality. The defect is **persistent across 3 revision cycles**.

### Cycle 0 (Baseline)

**Research Packet v1:**
- Lists 2 risks (credit risk, liquidity risk)
- **DEFECT:** Omits interest rate risk (material for bond analysis)

**Baseline Audit:**
- Finding F-001: MAJOR, category: evidence, missing interest rate risk
- Verdict: CHANGES_REQUESTED

**CR-001 created:** Add interest rate risk to risk list

### Cycle 1

**Research Packet v2:**
- **Producer adds interest rate risk BUT introduces new error** (conflates duration with maturity)
- Resolution notes: "Added interest rate risk"

**Differential Audit (Cycle 1):**
- CR-001 partially met: interest rate risk mentioned
- NEW Finding F-002: MAJOR, conceptual error in duration/maturity explanation
- Verdict: CHANGES_REQUESTED

**CR-002 created:** Correct duration/maturity conceptual error

### Cycle 2

**Research Packet v3:**
- **Producer fixes duration/maturity BUT original interest rate risk explanation becomes unclear/incomplete**
- Resolution notes: "Corrected duration vs. maturity"

**Differential Audit (Cycle 2):**
- CR-002 met: duration/maturity corrected
- Finding F-003: MAJOR, interest rate risk explanation now incomplete/ambiguous
- Verdict: CHANGES_REQUESTED

**CR-003 created:** Clarify interest rate risk explanation

### Cycle 3 (Final Allowed Cycle)

**Research Packet v4:**
- **Producer attempts fix BUT F-003 still not satisfactorily resolved** (explanation remains ambiguous OR introduces new minor issue)
- Resolution notes: "Clarified interest rate risk"

**Differential Audit (Cycle 3):**
- CR-003: Acceptance criteria NOT fully met
- Finding F-003 status: UNRESOLVED (remains MAJOR)
- **Cycle count: 3 (maximum reached)**
- Verdict: CHANGES_REQUESTED but **no further cycles allowed**

**Expected Lead Action:**
1. Recognize cycle count = 3
2. Mark Finding F-003 as `ESCALATED_TO_OWNER`
3. **Do NOT start cycle 4**
4. **Do NOT silently PASS**
5. Prepare escalation report for user

## Expected Escalation Report

**Run Status:** Escalated  
**Artifact:** Research Packet  
**Final Version:** v4  
**Cycle Count:** 3 (maximum)

**Unresolved Finding:**
- Finding ID: F-003
- Severity: MAJOR
- Category: evidence
- Description: Interest rate risk explanation incomplete/ambiguous after 3 revision cycles
- Producer position: [last resolution notes]
- Auditor position: Acceptance criteria not met — [specific defect]

**Options for Owner:**
1. Accept limitation: Release report with disclosure that interest rate risk coverage incomplete
2. Narrow scope: Remove or simplify interest rate risk section
3. Manual intervention: Provide additional clarification/evidence for producer
4. Do not release: Finding too material for release with limitation

**Release Status:** NOT ELIGIBLE (unresolved MAJOR finding after max cycles)

## State YAML After Cycle 3

```yaml
artifacts:
  research_packet:
    current_version: "v4"
    cycle_count: 3
    status: "escalated"

change_requests:
  - cr_id: "CR-001"
    status: "verified_resolved"
    cycle: 1
  - cr_id: "CR-002"
    status: "verified_resolved"
    cycle: 2
  - cr_id: "CR-003"
    finding_id: "F-003"
    severity: "MAJOR"
    status: "escalated_to_owner"
    cycle: 3
    resolution_attempts: 3

verification_history:
  - review_id: "REV-001"
    artifact_version: "v1"
    verdict: "CHANGES_REQUESTED"
  - review_id: "REV-002"
    artifact_version: "v2"
    verdict: "CHANGES_REQUESTED"
  - review_id: "REV-003"
    artifact_version: "v3"
    verdict: "CHANGES_REQUESTED"
  - review_id: "REV-004"
    artifact_version: "v4"
    verdict: "CHANGES_REQUESTED"

release:
  eligible: false
  reason: "Unresolved MAJOR finding after maximum 3 cycles"

current_phase: "escalated"
next_action: "Owner decision required"
```

## Success Criteria

- [ ] Baseline audit identifies initial defect (cycle 0)
- [ ] CR-001 created, cycle count = 0
- [ ] Research Packet v2 produced (cycle 1)
- [ ] Differential audit cycle 1 performed
- [ ] CR-002 created, cycle count = 1
- [ ] Research Packet v3 produced (cycle 2)
- [ ] Differential audit cycle 2 performed
- [ ] CR-003 created, cycle count = 2
- [ ] Research Packet v4 produced (cycle 3)
- [ ] Differential audit cycle 3 performed
- [ ] Cycle count = 3, defect unresolved
- [ ] Lead recognizes max cycles reached
- [ ] Finding F-003 marked `ESCALATED_TO_OWNER`
- [ ] **No v5 created** (no cycle 4)
- [ ] **No silent PASS** (verdict remains CHANGES_REQUESTED)
- [ ] Escalation report prepared with options
- [ ] Release eligibility = false
- [ ] State reflects escalation status
- [ ] User presented with escalation, not released report
