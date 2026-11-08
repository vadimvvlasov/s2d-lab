#!/usr/bin/env python3
"""
Quick schema test without full state validation.

Tests Pydantic models directly.
"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

try:
    from state_schema import (
        ArtifactState,
        ArtifactStatus,
        ChangeRequest,
        CRStatus,
        FinalAudit,
        FinalAuditStatus,
        Release,
        RunState,
        Severity,
        VerificationRecord,
        Verdict,
    )
    from pydantic import ValidationError
except ImportError as e:
    print(f"Error: {e}")
    print("Install: pip install pydantic")
    sys.exit(1)


def test_artifact_state():
    """Test ArtifactState validation"""
    print("Testing ArtifactState...")
    
    # Valid
    a1 = ArtifactState(current_version="v1", cycle_count=0, status=ArtifactStatus.PASS)
    assert a1.current_version == "v1"
    
    # Invalid version
    try:
        a2 = ArtifactState(current_version="v5", cycle_count=0, status=ArtifactStatus.PASS)
        assert False, "Should reject v5"
    except ValidationError as e:
        print(f"  ✓ Rejected v5: {e.errors()[0]['msg'][:50]}")
    
    # Cycle > 3
    try:
        a3 = ArtifactState(current_version="v4", cycle_count=4, status=ArtifactStatus.PASS)
        assert False, "Should reject cycle_count=4"
    except ValidationError as e:
        print(f"  ✓ Rejected cycle_count=4: {e.errors()[0]['msg'][:50]}")
    
    print("  ✓ ArtifactState OK\n")


def test_change_request():
    """Test ChangeRequest validation"""
    print("Testing ChangeRequest...")
    
    # Valid
    cr1 = ChangeRequest(
        cr_id="CR-001",
        finding_id="F-001",
        artifact="research_packet",
        reviewed_version="v1",
        target_version="v2",
        severity=Severity.BLOCKER,
        assigned_to="quant-researcher",
        cycle=1,
        status=CRStatus.OPEN,
    )
    assert cr1.cr_id == "CR-001"
    
    # Invalid CR ID
    try:
        cr2 = ChangeRequest(
            cr_id="CR-1",  # Wrong format
            finding_id="F-001",
            artifact="research_packet",
            reviewed_version="v1",
            target_version="v2",
            severity=Severity.BLOCKER,
            assigned_to="quant-researcher",
            cycle=1,
            status=CRStatus.OPEN,
        )
        assert False, "Should reject CR-1"
    except ValidationError as e:
        print(f"  ✓ Rejected CR-1: {e.errors()[0]['msg'][:50]}")
    
    print("  ✓ ChangeRequest OK\n")


def test_verification_record():
    """Test VerificationRecord validation"""
    print("Testing VerificationRecord...")
    
    # Valid
    vr1 = VerificationRecord(
        review_id="REV-001",
        review_scope="research_packet",
        artifact_version="v1",
        verdict=Verdict.CHANGES_REQUESTED,
        findings_count=3,
        blocker_count=1,
        major_count=1,
        minor_count=1,
    )
    assert vr1.findings_count == 3
    
    # Invalid sum
    try:
        vr2 = VerificationRecord(
            review_id="REV-001",
            review_scope="research_packet",
            artifact_version="v1",
            verdict=Verdict.CHANGES_REQUESTED,
            findings_count=5,  # Wrong sum
            blocker_count=1,
            major_count=1,
            minor_count=1,
        )
        assert False, "Should reject wrong sum"
    except ValidationError as e:
        print(f"  ✓ Rejected wrong sum: {e.errors()[0]['msg'][:60]}")
    
    print("  ✓ VerificationRecord OK\n")


def test_run_state_cycle_limit():
    """Test RunState cycle limit validation"""
    print("Testing RunState cycle limit...")
    
    # Valid (cycle 3)
    rs1 = RunState(
        run_id="2026-11-08-test",
        timestamp="2026-11-08T10:00:00Z",
        source_ref="source.md",
        artifacts={
            "research_packet": ArtifactState(
                current_version="v4",
                cycle_count=3,
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
        next_action="Owner decision",
    )
    assert rs1.artifacts["research_packet"].cycle_count == 3
    print("  ✓ Accepted cycle=3")
    
    # Invalid (cycle 4)
    try:
        rs2 = RunState(
            run_id="2026-11-08-test",
            timestamp="2026-11-08T10:00:00Z",
            source_ref="source.md",
            artifacts={
                "research_packet": ArtifactState(
                    current_version="v4",  # Would be v5, but capped at v4
                    cycle_count=4,  # Exceeds limit
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
            next_action="Owner decision",
        )
        assert False, "Should reject cycle=4"
    except ValidationError as e:
        print(f"  ✓ Rejected cycle=4: {e.errors()[0]['msg'][:60]}")
    
    print("  ✓ RunState cycle limit OK\n")


def test_pass_with_blocker():
    """Test RunState: no PASS with unresolved BLOCKER"""
    print("Testing PASS with unresolved BLOCKER...")
    
    # Invalid: PASS + unresolved BLOCKER
    try:
        rs = RunState(
            run_id="2026-11-08-test",
            timestamp="2026-11-08T10:00:00Z",
            source_ref="source.md",
            artifacts={
                "research_packet": ArtifactState(
                    current_version="v1",
                    cycle_count=0,
                    status=ArtifactStatus.PASS,  # PASS
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
                    status=CRStatus.OPEN,
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
        assert False, "Should reject PASS with unresolved BLOCKER"
    except ValidationError as e:
        print(f"  ✓ Rejected: {e.errors()[0]['msg'][:80]}")
    
    print("  ✓ PASS with BLOCKER validation OK\n")


def test_release_eligibility():
    """Test Release eligibility conditions"""
    print("Testing Release eligibility...")
    
    # Invalid: eligible=true but final_audit not PASS
    try:
        rs = RunState(
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
                status=FinalAuditStatus.CHANGES_REQUESTED,  # Not PASS
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
        assert False, "Should reject eligible=true with final_audit=changes_requested"
    except ValidationError as e:
        print(f"  ✓ Rejected: {e.errors()[0]['msg'][:80]}")
    
    # Invalid: eligible=true but no path
    try:
        rs = RunState(
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
                path=None,  # Missing path
            ),
            current_phase="released",
            next_action="None",
        )
        assert False, "Should reject eligible=true without path"
    except ValidationError as e:
        print(f"  ✓ Rejected: {e.errors()[0]['msg'][:80]}")
    
    print("  ✓ Release eligibility validation OK\n")


if __name__ == "__main__":
    print("D3 Schema Validation Tests\n")
    print("=" * 60)
    
    test_artifact_state()
    test_change_request()
    test_verification_record()
    test_run_state_cycle_limit()
    test_pass_with_blocker()
    test_release_eligibility()
    
    print("=" * 60)
    print("✓ All tests passed!")
