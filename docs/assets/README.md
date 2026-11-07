# S2D Lab Diagrams

## User Flow Diagram
**File:** `user-flow.svg`  
**Purpose:** Shows the user experience — what the participant sees  
**Scope:** High-level, simplified workflow from input to output

The user flow emphasizes that S2D Lab has:
- One input: conversation history
- One command: `/recap`
- One output: clean, verified Conversation Research Recap

This diagram is user-facing and intentionally hides internal complexity.

---

## Verifier Workflow Diagram
**File:** `verifier-workflow.svg`  
**Purpose:** Shows the technical implementation with bounded producer-verifier-rework loop  
**Scope:** Complete internal workflow with quality control mechanisms

The verifier workflow shows:
1. **Source intake** — conversation stored in git-ignored workspace
2. **Question Map v1** — Conversation Analyst extraction
3. **Research Packet v1** — Quant Researcher answers + options + recommendation
4. **Research audit (cycle 0)** — Independent Auditor review with verdict
5. **Rework loop** — Change Requests, producer revisions (v2, v3, v4), auditor rechecks (max 3 cycles)
6. **Synthesis** — Research Lead writes Final Report v1
7. **Final report audit** — Independent Auditor checks participant-facing report
8. **Release gate** — Copy to public location only after PASS with no unresolved blockers

**Key features:**
- Explicit artifact versioning (v1→v2→v3→v4)
- Bounded cycles (maximum 3, then escalate)
- Independent verification at every stage
- Release gate preventing unverified output
- Source traceability throughout

This diagram is technical documentation for understanding the quality assurance process.

---

## When to use each diagram

**Use user-flow.svg when:**
- Explaining S2D Lab to new users
- Showing the simplicity of the interface
- Demonstrating "one command, one output" design

**Use verifier-workflow.svg when:**
- Documenting the internal quality process
- Explaining how verification works
- Debugging or troubleshooting workflow issues
- Training on the bounded rework loop
- Discussing architecture or methodology

Both diagrams are accurate — they show different perspectives of the same system.
