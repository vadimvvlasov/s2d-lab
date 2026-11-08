---
artifact_type: "research_packet"
version: "v1"
run_id: "test-d2-cycle-2"
created_by: "quant-researcher"
created_at: "2026-11-08T14:00:00Z"
source_refs:
  - path: "source.md"
    type: "conversation"
---

## Q1 — Test Question

**Answer:** Test answer.

**Claims:**

**Claim Q1.C1** — First claim
- **Claim ID:** Q1.C1
- **Type:** FACT
- **Evidence IDs:** []
- **Confidence:** HIGH
- **Depends on:** [Q1.C2]

**Claim Q1.C2** — Second claim
- **Claim ID:** Q1.C2
- **Type:** FACT
- **Evidence IDs:** []
- **Confidence:** HIGH
- **Depends on:** [Q1.C1]

ERROR: Q1.C1 → Q1.C2 → Q1.C1 (cycle)
