---
description: Turn the supplied conversation into a question-driven research recap with compared options and a justified recommendation
agent: research-lead
---

Analyze the conversation and produce one **Conversation Research Recap**.

Input (`$ARGUMENTS`): optional path to a Telegram Desktop HTML export folder (`ChatExport_*`) and/or `--chat "<title>"`. Without arguments, the newest export of `investment-decisions-with-ml` in `~/Downloads/Telegram Desktop` is used — all messages and photos in the export. A conversation pasted into the session takes precedence.

Source intake: unless a conversation was pasted, run exactly `uv run scripts/tg_export_to_source.py $ARGUMENTS` (nothing before or after it). If the arguments are `--resume <run-id>`, skip intake and resume that run as your Workflow describes.

Then follow your Workflow: Question Map and its audit, one research packet and audit per research task with bounded rework (max 3 cycles per artifact), final report, final audit, release gate. Present only the released final report; intermediate artifacts stay in `runs/.work/<run-id>/`.

Do not invent trading levels or executable trade signals. Do not claim snippet-only or inaccessible sources were fully verified.
