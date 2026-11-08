#!/usr/bin/env python3
"""
E1 Structural Tests: Claim Dependency Graph Validation

Tests claim dependency validation using D2 validator.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

import pytest


class TestClaimDependencies:
    """Test claim dependency graph validation (D2 validator)"""

    def test_valid_dag_passes(self):
        """Valid DAG should pass validation"""
        # Use d2-test-5-valid-dag.md
        fixture = Path("tests/d2-test-5-valid-dag.md")
        if not fixture.exists():
            pytest.skip("Fixture not available")

        from validate_artifact import ArtifactValidator

        validator = ArtifactValidator()
        result = validator.validate_file(fixture)

        assert result.is_valid, f"Valid DAG should pass, errors: {result.errors}"

    def test_self_dependency_rejected(self):
        """Claim depending on itself should be rejected"""
        import tempfile

        from validate_artifact import ArtifactValidator

        artifact_content = """---
artifact_type: "research_packet"
version: "v1"
run_id: "2026-11-08-test"
created_by: "quant-researcher"
created_at: "2026-11-08T10:00:00Z"
source_refs:
  - path: "source.md"
    type: "conversation"
---

## Q1 — Test

**Claim Q1.C1** — Self-dependent
- **Claim ID:** Q1.C1
- **Depends on:** [Q1.C1]
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(artifact_content)
            temp_path = Path(f.name)

        try:
            validator = ArtifactValidator()
            result = validator.validate_file(temp_path)

            assert not result.valid, "Should reject self-dependency"
            assert any(
                "self-dependency" in f.message.lower()
                for f in result.findings
                if f.severity == "ERROR"
            )
        finally:
            temp_path.unlink()

    def test_nonexistent_dependency_rejected(self):
        """Dependency to non-existent claim should be rejected"""
        fixture = Path("tests/d2-test-1-nonexistent.md")
        if not fixture.exists():
            pytest.skip("Fixture not available")

        from validate_artifact import ArtifactValidator

        validator = ArtifactValidator()
        result = validator.validate_file(fixture)

        assert not result.is_valid, "Should reject non-existent dependency"
        assert any(
            "non-existent" in str(e).lower() or "Q9.C99" in str(e)
            for e in result.errors
        )

    def test_cycle_detected_and_rejected(self):
        """Circular dependency should be detected and rejected"""
        fixture = Path("tests/d2-test-3-cycle-2.md")
        if not fixture.exists():
            pytest.skip("Fixture not available")

        from validate_artifact import ArtifactValidator

        validator = ArtifactValidator()
        result = validator.validate_file(fixture)

        assert not result.is_valid, "Should reject cycle"
        assert any("cycle" in str(e).lower() for e in result.errors)

    def test_transitive_scope_calculation(self):
        """Transitive scope calculation should include all dependents"""
        from validate_artifact import ArtifactValidator

        # Test the get_transitive_recheck_scope method directly
        claims = [
            {"id": "Q1.C1", "depends_on": []},
            {"id": "Q1.C2", "depends_on": []},
            {"id": "Q1.C3", "depends_on": ["Q1.C1"]},
            {"id": "Q1.C4", "depends_on": ["Q1.C2", "Q1.C3"]},
        ]

        validator = ArtifactValidator()
        changed = {"Q1.C1"}
        scope = validator.get_transitive_recheck_scope(changed, claims)

        # Q1.C1 changed → scope should include Q1.C1, Q1.C3 (depends on C1), Q1.C4 (depends on C3)
        expected = {"Q1.C1", "Q1.C3", "Q1.C4"}
        assert scope == expected, f"Expected {expected}, got {scope}"

    def test_transitive_scope_multiple_changed(self):
        """Transitive scope with multiple changed claims"""
        from validate_artifact import ArtifactValidator

        claims = [
            {"id": "Q1.C1", "depends_on": []},
            {"id": "Q1.C2", "depends_on": []},
            {"id": "Q1.C3", "depends_on": ["Q1.C1"]},
            {"id": "Q1.C4", "depends_on": ["Q1.C2"]},
        ]

        validator = ArtifactValidator()
        changed = {"Q1.C1", "Q1.C2"}
        scope = validator.get_transitive_recheck_scope(changed, claims)

        # Both Q1.C1 and Q1.C2 changed → scope includes all 4 claims
        expected = {"Q1.C1", "Q1.C2", "Q1.C3", "Q1.C4"}
        assert scope == expected, f"Expected {expected}, got {scope}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
