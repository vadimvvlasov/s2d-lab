# Verifier/rework loop synthetic tests

These are lightweight prompt-based tests to verify the verifier/rework loop implementation.

## Test 1: Clean run with final audit pass
**Setup:** Conversation with clear participant questions, good evidence, proper attribution.
**Expected:**
- [ ] Question Map v1 created
- [ ] Research Packet v1 created
- [ ] Research audit (cycle 0) returns `PASS`
- [ ] Final report v1 created
- [ ] Final report audit returns `PASS`
- [ ] Report released to `runs/YYYY-MM-DD-conversation-research-recap.md`
- [ ] Intermediate artifacts remain in `runs/.work/<run-id>/`

## Test 2: Omitted question routes CR to Analyst
**Setup:** Conversation has explicit question that Analyst missed in v1.
**Expected:**
- [ ] Research audit identifies finding F-001, severity MAJOR, category question_attribution, owner conversation-analyst
- [ ] Research audit verdict: `CHANGES_REQUESTED`
- [ ] Lead creates CR-001 targeting Question Map v1 → v2
- [ ] CR routed to conversation-analyst
- [ ] Analyst produces Question Map v2 with resolution notes
- [ ] Auditor rechecks, cycle 1
- [ ] Finding resolved, verdict `PASS` or remaining issue documented

## Test 3: Inaccessible source treated as verified
**Setup:** Research Packet v1 cites a source with access_status METADATA_ONLY but claims FULL_TEXT_OPENED verification.
**Expected:**
- [ ] Research audit identifies finding F-001, severity MAJOR, category evidence, owner quant-researcher
- [ ] Research audit verdict: `CHANGES_REQUESTED`
- [ ] Lead creates CR-001 targeting Research Packet v1 → v2
- [ ] CR requires: downgrade claim or remove unsupported statement
- [ ] Researcher produces Research Packet v2 with corrected source status or narrowed claim
- [ ] Auditor rechecks independently, cycle 1
- [ ] Finding resolved or claim properly narrowed

## Test 4: Calculation error corrected and rechecked
**Setup:** Research Packet v1 contains arithmetic error or wrong units.
**Expected:**
- [ ] Research audit identifies finding F-001, severity MAJOR, category calculation, owner quant-researcher
- [ ] Lead creates CR-001 with acceptance criteria: recalculate with correct inputs/formula
- [ ] Researcher produces Research Packet v2 with corrected calculation and shown work
- [ ] Auditor independently verifies calculation in recheck
- [ ] Finding resolved

## Test 5: Unsupported claim introduced by Lead in final report
**Setup:** Final report v1 introduces a claim not supported by Question Map or Research Packet.
**Expected:**
- [ ] Final report audit identifies finding F-001, severity MAJOR, category synthesis, owner research-lead
- [ ] Lead self-corrects: creates Final Report v2 removing unsupported claim or adding proper evidence
- [ ] Auditor rechecks final report v2, cycle 1
- [ ] Finding resolved

## Test 6: Missing original source results in BLOCKED
**Setup:** Auditor invoked without access to original conversation source.
**Expected:**
- [ ] Auditor checks source accessibility
- [ ] Source unavailable → verdict `BLOCKED`
- [ ] Lead fixes: provides source path, reruns audit
- [ ] Not counted as a rework cycle (orchestration fix, not artifact defect)

## Test 7: Defect persists after 3 cycles
**Setup:** Finding requires fix, producer submits v2 (cycle 1), v3 (cycle 2), v4 (cycle 3), but defect remains.
**Expected:**
- [ ] Cycle 1: producer v2, auditor recheck, still `CHANGES_REQUESTED`
- [ ] Cycle 2: producer v3, auditor recheck, still `CHANGES_REQUESTED`
- [ ] Cycle 3: producer v4, auditor recheck, finding unresolved
- [ ] Lead marks finding as `ESCALATED_TO_OWNER`
- [ ] No cycle 4 started
- [ ] If BLOCKER: no verified release
- [ ] If MAJOR: affected claim must be narrowed/removed or escalated to owner decision

## Test 8: Minor-only finding receives disposition
**Setup:** Research audit returns single finding, severity MINOR.
**Expected:**
- [ ] Verdict can be `PASS` if Lead accepts minor issue
- [ ] Lead records reasoned disposition (fix or accept with rationale)
- [ ] Auditor report states disposition
- [ ] No CR required (unless Lead chooses to fix)
- [ ] Workflow proceeds to synthesis

## Test 9: Context resume reconstructs state
**Setup:** Run interrupted after Research Packet v2, CR-001 open.
**Expected:**
- [ ] `runs/.work/<run-id>/state.yaml` exists
- [ ] State shows: research_packet current_version v2, cycle_count 1, CR-001 status, next_action
- [ ] Lead can resume: dispatch recheck or continue workflow
- [ ] No duplicate v2 creation

## Test 10: Release gate refuses unresolved blocker
**Setup:** Final report audit returns `CHANGES_REQUESTED` with BLOCKER, but after 3 cycles finding remains.
**Expected:**
- [ ] Final report cycle count = 3
- [ ] Finding status: `ESCALATED_TO_OWNER`
- [ ] Release eligibility: false
- [ ] Report NOT copied to `runs/YYYY-MM-DD-conversation-research-recap.md`
- [ ] Lead escalates with findings and status
- [ ] User sees escalation notice, not a released report

## Test execution guidance
These are not automated test harness tests. To validate:
1. For each scenario, simulate by invoking `/recap` with a crafted conversation or intermediate artifacts.
2. Manually verify the expected checkboxes against actual agent behavior and file outputs.
3. Record `PASS` if all checkboxes met, `NOT RUN` if scenario not executed, `FAIL` with details if behavior diverged.
4. A production test harness is out of scope for this update.
