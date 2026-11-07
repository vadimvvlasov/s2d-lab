---
description: Turn the supplied conversation into a question-driven research recap with compared options and a justified recommendation
agent: research-lead
---

Analyze the conversation history supplied in this session and produce one **Conversation Research Recap**.

Follow the bounded producer–verifier–rework workflow:

1. **Source intake:** Store the full original conversation in `runs/.work/<run-id>/source.md`. Record run ID and timestamp.

2. **Question Map v1:** Extract explicit questions, implied questions, participant concerns, and disagreements via `conversation-analyst`. Keep researcher-added context separate. Save as `runs/.work/<run-id>/01-question-map-v1.md`.

3. **Research Packet v1:** Research the most important questions via `quant-researcher`, splitting compound questions where they require different concepts or decision rules. Compare 2–4 realistic options when available, using criteria whose origin is explicit. Save as `runs/.work/<run-id>/02-research-packet-v1.md`.

4. **Research audit (cycle 0):** Have `independent-auditor` independently review question attribution, source accessibility, calculations, conceptual reasoning, and recommendation logic. The auditor must receive the original conversation source path. Save verification report as `runs/.work/<run-id>/03-verification-research-v1.md`.

5. **Rework (max 3 cycles per artifact):** For each `BLOCKER`/`MAJOR` finding, create a Change Request, route to responsible agent, obtain new version, and have auditor recheck. Track cycle count. After cycle 3, unresolved findings escalate; no fourth cycle.

6. **Final report v1:** After research audit `PASS` or `PASS_WITH_LIMITATIONS` (no unresolved blocker), write one readable report for the participants. Save as `runs/.work/<run-id>/04-final-report-v1.md`.

7. **Final report audit:** Have `independent-auditor` audit the final report against original conversation, Question Map, Research Packet, and output contract. Save as `runs/.work/<run-id>/05-verification-final-report-v1.md`.

8. **Release gate:** Only release to `runs/YYYY-MM-DD-conversation-research-recap.md` after final audit `PASS` or `PASS_WITH_LIMITATIONS` with no unresolved blocker. Apply rework loop to final report if needed (max 3 cycles).

9. **Presentation:** Present only the released final report. Keep intermediate packets, Change Requests, and verification reports internal in `runs/.work/<run-id>/`.

Do not invent trading levels or executable trade signals. Do not claim snippet-only or inaccessible sources were fully verified. If the original chat or relevant images are unavailable, the auditor will set verdict to `BLOCKED`.
