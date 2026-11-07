# S2D Lab — Question-First Upgrade

This package upgrades S2D from a generic **Decision Brief** into a **participant-centered Conversation Research Recap**.

## Product behavior

User flow remains unchanged: conversation history + `/recap`.

The reasoning chain becomes:

`participant questions → problem formalization → evidence search → option comparison → best-fit recommendation → independent audit → readable group recap`

## Package contents

- `00-CODING-AGENT-INSTRUCTIONS.md` — implementation instructions for OpenCode.
- `proposed/` — replacement/new files with target repository paths.
- `research/FOUNDATIONS.md` — research-based design rationale.
- `proposed/tests/` — small acceptance fixture and expected behavior.

## How to use

1. Open/clone `vadimvvlasov/s2d-lab` in OpenCode.
2. Extract this package into the repository root. It creates `s2d-lab-question-first-upgrade/`.
3. Start the coding agent from the repository root.
4. Give it this instruction:

   > Read `s2d-lab-question-first-upgrade/00-CODING-AGENT-INSTRUCTIONS.md` and implement the upgrade. Treat `proposed/` as the target design, inspect the current repository before editing, preserve unrelated changes, and complete the acceptance review. Do not commit or push.

5. Review the resulting diff and test report before approving a commit.

The proposed files are a reference overlay. The coding agent must reconcile them with the current repository rather than blindly overwrite files.
