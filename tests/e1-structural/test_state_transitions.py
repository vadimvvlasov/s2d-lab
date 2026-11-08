#!/usr/bin/env python3
"""
E1 Structural Tests: State Transition Validation

Tests state validation using D3 validator.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

import pytest


class TestStateTransitions:
    """Test state transition validation (D3 validator)"""

    def test_valid_state_passes(self):
        """Valid state should pass validation"""
        import yaml
        from state_schema import RunState
        
        # Use fx07 as valid example (cycle 3, escalated)
        fixture = Path("runs/.work/2026-11-08-fx07-cycle-limit/state.yaml")
        if not fixture.exists():
            pytest.skip("Fixture not available")
        
        with open(fixture) as f:
            data = yaml.safe_load(f)
        
        # Should not raise ValidationError
        state = RunState(**data)
        assert state.run_id == "2026-11-08-fx07-cycle-limit"
        assert state.artifacts["research_packet"].cycle_count == 3

    def test_cycle_count_exceeds_limit_rejected(self):
        """Cycle count > 3 should be rejected"""
        from state_schema import RunState, ArtifactState, ArtifactStatus, FinalAudit, FinalAuditStatus, Release
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            state = RunState(
                run_id="2026-11-08-test",
                timestamp="2026-11-08T10:00:00Z",
                source_ref="source.md",
                artifacts={
                    "research_packet": ArtifactState(
                        current_version="v4",
                        cycle_count=4,  # Exceeds limit!
                        status=ArtifactStatus.ESCALATED,
                    )
                },
                change_requests=[],
                verification_history=[],
                final_audit=FinalAudit(
                    status=FinalAuditStatus.NOT_STARTED,
                    unresolved_blockers=0,
                ),
                release=Release(eligible=False),
                current_phase="escalated",
                next_action="Fix",
            )
        
        assert "cycle_count" in str(exc_info.value).lower() or "less than or equal to 3" in str(exc_info.value)

    def test_pass_with_unresolved_blocker_rejected(self):
        """PASS status with unresolved BLOCKER should be rejected"""
        from state_schema import (
            RunState, ArtifactState, ArtifactStatus,
            ChangeRequest, CRStatus, Severity,
            FinalAudit, FinalAuditStatus, Release
        )
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            state = RunState(
                run_id="2026-11-08-test",
                timestamp="2026-11-08T10:00:00Z",
                source_ref="source.md",
                artifacts={
                    "research_packet": ArtifactState(
                        current_version="v1",
                        cycle_count=0,
                        status=ArtifactStatus.PASS,  # PASS status
                    )
                },
                change_requests=[
                    ChangeRequest(
                        cr_id="CR-001",
                        finding_id="F-001",
                        artifact="research_packet",
                        reviewed_version="v1",
                        target_version="v2",
                        severity=Severity.BLOCKER,  # Unresolved BLOCKER
                        assigned_to="quant-researcher",
                        cycle=1,
                        status=CRStatus.OPEN,  # Not resolved
                    )
                ],
                verification_history=[],
                final_audit=FinalAudit(
                    status=FinalAuditStatus.NOT_STARTED,
                    unresolved_blockers=1,
                ),
                release=Release(eligible=False),
                current_phase="research_audit",
                next_action="Fix BLOCKER",
            )
        
        assert "pass" in str(exc_info.value).lower() and "blocker" in str(exc_info.value).lower()

    def test_version_cycle_mismatch_rejected(self):
        """Version not matching cycle count should be rejected"""
        from state_schema import RunState, ArtifactState, ArtifactStatus, FinalAudit, FinalAuditStatus, Release
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            state = RunState(
                run_id="2026-11-08-test",
                timestamp="2026-11-08T10:00:00Z",
                source_ref="source.md",
                artifacts={
                    "research_packet": ArtifactState(
                        current_version="v3",  # v3 = cycle 2
                        cycle_count=1,  # But cycle_count = 1 (mismatch!)
                        status=ArtifactStatus.PASS,
                    )
                },
                change_requests=[],
                verification_history=[],
                final_audit=FinalAudit(
                    status=FinalAuditStatus.NOT_STARTED,
                    unresolved_blockers=0,
                ),
                release=Release(eligible=False),
                current_phase="research",
                next_action="Continue",
            )
        
        assert "version" in str(exc_info.value).lower() and "cycle" in str(exc_info.value).lower()

    def test_release_without_final_audit_pass_rejected(self):
        """Release eligible=true without final_audit PASS should be rejected"""
        from state_schema import RunState, ArtifactState, ArtifactStatus, FinalAudit, FinalAuditStatus, Release
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            state = RunState(
                run_id="2026-11-08-test",
                timestamp="2026-11-08T10:00:00Z",
                source_ref="source.md",
                artifacts={
                    "final_report": ArtifactState(
                        current_version="v1",
                        cycle_count=0,
                        status=ArtifactStatus.PASS,
                    )
                },
                change_requests=[],
                verification_history=[],
                final_audit=FinalAudit(
                    status=FinalAuditStatus.CHANGES_REQUESTED,  # Not PASS!
                    report_version_audited="v1",
                    unresolved_blockers=0,
                ),
                release=Release(
                    eligible=True,  # Claiming eligible
                    path="runs/test.md",
                ),
                current_phase="final_rework",
                next_action="Fix report",
            )
        
        assert "release" in str(exc_info.value).lower() and "eligible" in str(exc_info.value).lower()

    def test_release_without_path_rejected(self):
        """Release eligible=true without path should be rejected"""
        from state_schema import RunState, ArtifactState, ArtifactStatus, FinalAudit, FinalAuditStatus, Release
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            state = RunState(
                run_id="2026-11-08-test",
                timestamp="2026-11-08T10:00:00Z",
                source_ref="source.md",
                artifacts={
                    "final_report": ArtifactState(
                        current_version="v1",
                        cycle_count=0,
                        status=ArtifactStatus.PASS,
                    )
                },
                change_requests=[],
                verification_history=[],
                final_audit=FinalAudit(
                    status=FinalAuditStatus.PASS,
                    report_version_audited="v1",
                    unresolved_blockers=0,
                ),
                release=Release(
                    eligible=True,
                    path=None,  # Missing path!
                ),
                current_phase="released",
                next_action="None",
            )
        
        assert "path" in str(exc_info.value).lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
