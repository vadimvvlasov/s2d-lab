#!/usr/bin/env python3
"""
Pydantic schema for run state validation.

D3.1 implementation (session 05) - Pydantic 2.x syntax.
"""

import re
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class ArtifactStatus(str, Enum):
    """Artifact lifecycle status"""

    DRAFT = "draft"
    SUBMITTED_FOR_REVIEW = "submitted_for_review"
    PASS = "pass"
    CHANGES_REQUESTED = "changes_requested"
    ESCALATED = "escalated"
    NOT_STARTED = "not_started"


class CRStatus(str, Enum):
    """Change Request resolution status"""

    OPEN = "open"
    SUBMITTED_FOR_RECHECK = "submitted_for_recheck"
    VERIFIED_RESOLVED = "verified_resolved"
    ACCEPTED_WITH_LIMITATION = "accepted_with_limitation"
    ESCALATED_TO_OWNER = "escalated_to_owner"


class Severity(str, Enum):
    """Finding severity levels"""

    BLOCKER = "BLOCKER"
    MAJOR = "MAJOR"
    MINOR = "MINOR"


class Verdict(str, Enum):
    """Audit verdict"""

    PASS = "PASS"
    PASS_WITH_LIMITATIONS = "PASS_WITH_LIMITATIONS"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    BLOCKED = "BLOCKED"


class FinalAuditStatus(str, Enum):
    """Final audit lifecycle status"""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PASS = "pass"
    PASS_WITH_LIMITATIONS = "pass_with_limitations"
    CHANGES_REQUESTED = "changes_requested"
    BLOCKED = "blocked"


class ArtifactState(BaseModel):
    """State of a single artifact"""

    current_version: Optional[str] = None
    cycle_count: int = Field(ge=0, le=3)
    status: ArtifactStatus

    @field_validator("current_version")
    @classmethod
    def validate_version_format(cls, v):
        """Version must be v1, v2, v3, v4, or None"""
        if v is not None and not re.match(r"^v[1-4]$", v):
            raise ValueError(f"Invalid version format: {v} (must be v1, v2, v3, or v4)")
        return v


class ChangeRequest(BaseModel):
    """Change Request metadata"""

    cr_id: str
    finding_id: str
    artifact: str
    reviewed_version: str
    target_version: str
    severity: Severity
    assigned_to: str
    cycle: int = Field(ge=1, le=3)
    status: CRStatus
    resolution_attempts: Optional[int] = None

    @field_validator("cr_id")
    @classmethod
    def validate_cr_id_format(cls, v):
        """CR ID must be CR-NNN"""
        if not re.match(r"^CR-\d{3}$", v):
            raise ValueError(f"Invalid CR ID format: {v} (must be CR-NNN)")
        return v

    @field_validator("finding_id")
    @classmethod
    def validate_finding_id_format(cls, v):
        """Finding ID must be F-NNN"""
        if not re.match(r"^F-\d{3}$", v):
            raise ValueError(f"Invalid finding ID format: {v} (must be F-NNN)")
        return v


class VerificationRecord(BaseModel):
    """Audit history entry"""

    review_id: str
    review_scope: str
    artifact_version: str
    verdict: Verdict
    findings_count: int = Field(ge=0)
    blocker_count: int = Field(ge=0)
    major_count: int = Field(ge=0)
    minor_count: int = Field(ge=0)

    @field_validator("review_id")
    @classmethod
    def validate_review_id_format(cls, v):
        """Review ID must be REV-NNN"""
        if not re.match(r"^REV-\d{3}$", v):
            raise ValueError(f"Invalid review ID format: {v} (must be REV-NNN)")
        return v

    @model_validator(mode="after")
    def validate_findings_sum(self):
        """Total findings must equal sum of severity counts"""
        total = self.findings_count
        blocker = self.blocker_count
        major = self.major_count
        minor = self.minor_count

        if total != blocker + major + minor:
            raise ValueError(
                f"findings_count {total} != sum of severities "
                f"({blocker} BLOCKER + {major} MAJOR + {minor} MINOR = {blocker + major + minor})"
            )

        return self


class FinalAudit(BaseModel):
    """Final report audit status"""

    status: FinalAuditStatus
    report_version_audited: Optional[str] = None
    unresolved_blockers: int = Field(ge=0)


class Release(BaseModel):
    """Release gate"""

    eligible: bool
    path: Optional[str] = None
    reason: Optional[str] = None


class RunState(BaseModel):
    """Complete run state"""

    run_id: str
    timestamp: str
    source_ref: str
    artifacts: Dict[str, ArtifactState]
    change_requests: List[ChangeRequest] = []
    verification_history: List[VerificationRecord] = []
    final_audit: FinalAudit
    release: Release
    current_phase: str
    next_action: str

    # Optional fields (for fixture runs)
    fixture: Optional[str] = None
    model: Optional[str] = None
    seeded_defect: Optional[str] = None
    scripted_producers: Optional[str] = None

    @field_validator("run_id")
    @classmethod
    def validate_run_id_format(cls, v):
        """Run ID should be YYYY-MM-DD-slug"""
        if not re.match(r"^\d{4}-\d{2}-\d{2}-.+$", v):
            raise ValueError(
                f"Invalid run_id format: {v} (expected YYYY-MM-DD-slug)"
            )
        return v

    @field_validator("artifacts")
    @classmethod
    def validate_cycle_limit(cls, artifacts):
        """D3 Rule 1: Cycle count must not exceed 3"""
        for name, artifact in artifacts.items():
            if artifact.cycle_count > 3:
                raise ValueError(
                    f"Artifact '{name}': cycle_count {artifact.cycle_count} exceeds limit 3"
                )
        return artifacts

    @field_validator("artifacts")
    @classmethod
    def validate_version_cycle_consistency(cls, artifacts):
        """D3 Rule 4: Version must match cycle count"""
        for name, artifact in artifacts.items():
            version = artifact.current_version
            if version:
                # Extract version number (v1 -> 1, v2 -> 2, etc.)
                version_num = int(version[1])
                expected_cycle = version_num - 1

                if artifact.cycle_count != expected_cycle:
                    raise ValueError(
                        f"Artifact '{name}': version {version} but cycle_count "
                        f"{artifact.cycle_count} (expected {expected_cycle})"
                    )
        return artifacts

    @model_validator(mode="after")
    def validate_pass_with_blocker(self):
        """D3 Rule 2: No artifact can be 'pass' with unresolved BLOCKERs"""
        artifacts = self.artifacts
        change_requests = self.change_requests

        # Find unresolved BLOCKERs
        unresolved_blockers = [
            cr
            for cr in change_requests
            if cr.severity == Severity.BLOCKER
            and cr.status
            not in [CRStatus.VERIFIED_RESOLVED, CRStatus.ACCEPTED_WITH_LIMITATION]
        ]

        if not unresolved_blockers:
            return self

        # Check if any artifact is marked "pass" with unresolved BLOCKERs
        for name, artifact in artifacts.items():
            if artifact.status == ArtifactStatus.PASS:
                raise ValueError(
                    f"Artifact '{name}' status='pass' but unresolved BLOCKER CRs exist: "
                    f"{[cr.cr_id for cr in unresolved_blockers]}"
                )

        return self

    @model_validator(mode="after")
    def validate_release_eligibility(self):
        """D3 Rule 3: Release eligibility conditions"""
        release = self.release
        final_audit = self.final_audit
        change_requests = self.change_requests

        if not release or not release.eligible:
            return self  # Not claiming eligibility, OK

        # Condition 1: Final audit must be PASS or PASS_WITH_LIMITATIONS
        if final_audit.status not in [
            FinalAuditStatus.PASS,
            FinalAuditStatus.PASS_WITH_LIMITATIONS,
        ]:
            raise ValueError(
                f"Release eligible=true but final_audit.status={final_audit.status.value} "
                f"(must be 'pass' or 'pass_with_limitations')"
            )

        # Condition 2: No unresolved BLOCKERs
        unresolved_blockers = [
            cr
            for cr in change_requests
            if cr.severity == Severity.BLOCKER
            and cr.status
            not in [CRStatus.VERIFIED_RESOLVED, CRStatus.ACCEPTED_WITH_LIMITATION]
        ]
        if unresolved_blockers:
            raise ValueError(
                f"Release eligible=true but unresolved BLOCKER CRs exist: "
                f"{[cr.cr_id for cr in unresolved_blockers]}"
            )

        # Condition 3: Release path must be set
        if not release.path:
            raise ValueError("Release eligible=true but release.path is null")

        return self
