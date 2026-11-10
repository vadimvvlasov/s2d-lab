#!/usr/bin/env python3
"""
S2D Lab Artifact Validator (C1 implementation)

Validates artifact frontmatter and body structure against docs/artifact-schema.md.
Implements P-1 through P-5 from session-03-summary.md.

Usage:
    uv run scripts/validate-artifact.py <artifact-path>
    uv run scripts/validate-artifact.py runs/.work/*/  # validate all

Exit codes:
    0 - all valid
    1 - validation errors found
    2 - usage/file error
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    print(
        "Error: PyYAML required. Install with: uv pip install pyyaml", file=sys.stderr
    )
    sys.exit(2)


@dataclass
class Finding:
    """Validation finding"""

    severity: str  # ERROR, WARNING, INFO
    category: str
    message: str
    location: str = ""


@dataclass
class ValidationResult:
    """Result of validating one artifact"""

    path: Path
    valid: bool
    findings: list[Finding] = field(default_factory=list)
    artifact_type: str | None = None
    version: str | None = None

    def add_error(self, category: str, message: str, location: str = ""):
        self.findings.append(Finding("ERROR", category, message, location))
        self.valid = False

    def add_warning(self, category: str, message: str, location: str = ""):
        self.findings.append(Finding("WARNING", category, message, location))

    def add_info(self, category: str, message: str, location: str = ""):
        self.findings.append(Finding("INFO", category, message, location))


class ArtifactValidator:
    """Validates S2D Lab artifacts"""

    # P-1: Evidence Type enum (resolved per session-04 validation)
    EVIDENCE_TYPES = {
        "PRIMARY_DOCUMENT",  # Official docs, prospectuses, primary sources
        "OFFICIAL_DATA",  # API data, official statistics
        "SECONDARY_DOCUMENT",  # Educational/reference (e.g., Investopedia, Wikipedia)
        "SEARCH_RESULT",  # Web search snippets
        "CALCULATION",  # Derived calculation result
        "USER_SUPPLIED",  # From conversation/attachment
    }

    # P-1: Access status enum
    ACCESS_STATUSES = {
        "FULL_TEXT_OPENED",
        "OFFICIAL_DATA_OR_API_RETRIEVED",
        "SEARCH_SNIPPET_ONLY",
        "METADATA_ONLY",
        "INACCESSIBLE",
        "USER_SUPPLIED",
    }

    # Artifact types
    ARTIFACT_TYPES = {
        "question_map",
        "research_packet",
        "verification_report",
        "final_report",
    }

    # Version enum
    VERSIONS = {"v1", "v2", "v3", "v4"}

    # Created by enum
    CREATORS = {
        "conversation-analyst",
        "quant-researcher",
        "independent-auditor",
        "research-lead",
    }

    # Question classes
    QUESTION_CLASSES = {
        "EXPLICIT_QUESTION",
        "IMPLIED_QUESTION",
        "PARTICIPANT_CONCERN",
        "RESEARCHER_ADDED_CONTEXT",
        "RHETORICAL_OR_JOKE",
    }

    # Confidence levels
    CONFIDENCE_LEVELS = {"HIGH", "MEDIUM", "LOW"}

    # Priority levels
    PRIORITY_LEVELS = {"HIGH", "MEDIUM", "LOW"}

    def __init__(self, run_workspace: Path | None = None):
        """
        Args:
            run_workspace: Optional runs/.work/<run-id>/ for cross-checking
        """
        self.run_workspace = run_workspace

    def validate_file(self, path: Path) -> ValidationResult:
        """Validate single artifact file"""
        result = ValidationResult(path=path, valid=True)

        if not path.exists():
            result.add_error("file", f"File not found: {path}")
            return result

        if not path.is_file():
            result.add_error("file", f"Not a file: {path}")
            return result

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            result.add_error("file", f"Cannot read file: {e}")
            return result

        # Parse frontmatter
        frontmatter, body = self._parse_frontmatter(content)

        if frontmatter is None:
            result.add_error("frontmatter", "No valid YAML frontmatter found")
            return result

        # Validate common fields
        self._validate_common_frontmatter(frontmatter, result)

        # Type-specific validation
        artifact_type = frontmatter.get("artifact_type")
        result.artifact_type = artifact_type
        result.version = frontmatter.get("version")

        if artifact_type == "question_map":
            self._validate_question_map(frontmatter, body, result)
        elif artifact_type == "research_packet":
            self._validate_research_packet(frontmatter, body, result)
        elif artifact_type == "verification_report":
            self._validate_verification_report(frontmatter, body, result)
        elif artifact_type == "final_report":
            self._validate_final_report(frontmatter, body, result)

        # P-3: Cross-check CR status if this is a revision
        if frontmatter.get("version") in {"v2", "v3", "v4"}:
            self._validate_cr_status_cross_check(frontmatter, result)

        return result

    def _parse_frontmatter(self, content: str) -> tuple[dict | None, str]:
        """Parse YAML frontmatter from content"""
        # Match --- frontmatter ---
        pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
        match = re.match(pattern, content, re.DOTALL)

        if not match:
            return None, content

        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)
            return frontmatter, body
        except yaml.YAMLError:
            return None, content

    def _validate_common_frontmatter(self, fm: dict, result: ValidationResult):
        """Validate common frontmatter fields"""
        # artifact_type
        if "artifact_type" not in fm:
            result.add_error("frontmatter", "Missing required field: artifact_type")
        elif fm["artifact_type"] not in self.ARTIFACT_TYPES:
            result.add_error(
                "frontmatter",
                f"Invalid artifact_type: {fm['artifact_type']}. "
                f"Must be one of: {', '.join(sorted(self.ARTIFACT_TYPES))}",
            )

        # version
        if "version" not in fm:
            result.add_error("frontmatter", "Missing required field: version")
        elif fm["version"] not in self.VERSIONS:
            result.add_error(
                "frontmatter",
                f"Invalid version: {fm['version']}. "
                f"Must be one of: {', '.join(sorted(self.VERSIONS))}",
            )

        # run_id
        if "run_id" not in fm:
            result.add_error("frontmatter", "Missing required field: run_id")
        elif not re.match(r"^\d{4}-\d{2}-\d{2}-[\w-]+$", fm["run_id"]):
            result.add_warning(
                "frontmatter",
                f"run_id format should be YYYY-MM-DD-slug: {fm['run_id']}",
            )

        # created_by
        if "created_by" not in fm:
            result.add_error("frontmatter", "Missing required field: created_by")
        elif fm["created_by"] not in self.CREATORS:
            result.add_error(
                "frontmatter",
                f"Invalid created_by: {fm['created_by']}. "
                f"Must be one of: {', '.join(sorted(self.CREATORS))}",
            )

        # created_at
        if "created_at" not in fm:
            result.add_error("frontmatter", "Missing required field: created_at")
        elif not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", fm["created_at"]):
            result.add_warning(
                "frontmatter",
                f"created_at should be ISO 8601 (YYYY-MM-DDTHH:MM:SSZ): {fm['created_at']}",
            )

        # source_refs
        if "source_refs" not in fm:
            result.add_error("frontmatter", "Missing required field: source_refs")
        elif not isinstance(fm["source_refs"], list) or len(fm["source_refs"]) == 0:
            result.add_error("frontmatter", "source_refs must be non-empty array")
        else:
            for i, ref in enumerate(fm["source_refs"]):
                if not isinstance(ref, dict):
                    result.add_error("frontmatter", f"source_refs[{i}] must be dict")
                    continue
                if "path" not in ref:
                    result.add_error("frontmatter", f"source_refs[{i}] missing 'path'")
                if "type" not in ref:
                    result.add_error("frontmatter", f"source_refs[{i}] missing 'type'")

        # Revision fields if v2+ (a verification report is a new review, not a revision
        # of the previous report: its version tracks the recheck, no revision fields)
        version = fm.get("version")
        if version in {"v2", "v3", "v4"} and fm.get("artifact_type") != "verification_report":
            if "revision_of" not in fm:
                result.add_error(
                    "frontmatter", f"version {version} requires 'revision_of' field"
                )
            elif fm["revision_of"] not in self.VERSIONS:
                result.add_error(
                    "frontmatter", f"Invalid revision_of: {fm['revision_of']}"
                )

            if "change_requests_addressed" not in fm:
                result.add_error(
                    "frontmatter",
                    f"version {version} requires 'change_requests_addressed' field",
                )
            elif not isinstance(fm["change_requests_addressed"], list):
                result.add_error(
                    "frontmatter", "change_requests_addressed must be array"
                )
            else:
                # P-3: Validate CR structure
                for i, cr in enumerate(fm["change_requests_addressed"]):
                    if not isinstance(cr, dict):
                        result.add_error(
                            "frontmatter",
                            f"change_requests_addressed[{i}] must be dict",
                        )
                        continue
                    if "cr_id" not in cr:
                        result.add_error(
                            "frontmatter",
                            f"change_requests_addressed[{i}] missing 'cr_id'",
                        )
                    if "status" not in cr:
                        result.add_error(
                            "frontmatter",
                            f"change_requests_addressed[{i}] missing 'status'",
                        )

    def _validate_question_map(self, fm: dict, body: str, result: ValidationResult):
        """Validate question map specific fields"""
        # Extract questions from body
        questions = self._extract_questions(body)

        if len(questions) == 0:
            result.add_warning("content", "No questions found in body")

        for q in questions:
            qid = q.get("id", "unknown")

            # Required fields per schema
            if "class" not in q or q["class"] not in self.QUESTION_CLASSES:
                result.add_error("content", f"Question {qid}: invalid or missing class")

            if "raised_by" not in q:
                result.add_warning(
                    "content", f"Question {qid}: missing 'Raised by' field"
                )

            if "source_anchor" not in q and "source_span" not in q:
                result.add_error(
                    "content",
                    f"Question {qid}: missing source anchor/span (B4 requirement)",
                )

            if "source_quote" not in q:
                result.add_warning("content", f"Question {qid}: missing source quote")

    def _extract_questions(self, body: str) -> list[dict]:
        """Extract question metadata from body"""
        questions = []
        # Simple extraction - look for ### Q{N} — pattern
        pattern = r"### (Q\d+) — (.+?)(?=###|$)"
        matches = re.finditer(pattern, body, re.DOTALL)

        for match in matches:
            qid = match.group(1)
            content = match.group(2)

            q = {"id": qid}

            # Extract fields
            if m := re.search(r"\*\*Class:\*\* (\w+)", content):
                q["class"] = m.group(1)
            if m := re.search(r"\*\*Raised by:\*\* (.+)", content):
                q["raised_by"] = m.group(1).strip()
            if m := re.search(r"\*\*Source (?:span|anchor):\*\* (.+)", content):
                q["source_anchor"] = m.group(1).strip()
            if m := re.search(r'\*\*Source quote:\*\* "(.+?)"', content):
                q["source_quote"] = m.group(1).strip()

            questions.append(q)

        return questions

    def _validate_research_packet(self, fm: dict, body: str, result: ValidationResult):
        """Validate research packet specific fields"""
        # Extract claims and evidence
        claims = self._extract_claims(body)
        evidence_items = self._extract_evidence(body)

        # Build claim ID set for existence checks (D2.1.1)
        all_claim_ids = {claim.get("id", "") for claim in claims}

        # Per-task packets declare their questions; claims must stay inside them
        scope = fm.get("questions")
        if scope is not None:
            if not isinstance(scope, list) or not all(
                isinstance(q, str) and re.match(r"^Q\d+$", q) for q in scope
            ):
                result.add_error("frontmatter", f"questions must be a list like [\"Q1\", \"Q3\"], got {scope!r}")
            else:
                outside = sorted(
                    cid for cid in all_claim_ids if cid.split(".")[0] not in scope
                )
                if outside:
                    result.add_error(
                        "content",
                        f"Claims outside the packet's questions {scope}: {', '.join(outside)}",
                    )

        # Validate claim IDs (format Q{N}.C{M})
        claim_id_pattern = r"^Q\d+\.C\d+$"
        for claim in claims:
            cid = claim.get("id", "")
            if not re.match(claim_id_pattern, cid):
                result.add_error(
                    "content", f"Invalid claim ID format: {cid}. Must be Q{{N}}.C{{M}}"
                )

            # Check depends_on references
            if "depends_on" in claim:
                deps = claim["depends_on"]

                # D2: Self-dependency check (existing)
                if cid in deps:
                    result.add_error(
                        "content", f"Claim {cid}: self-dependency detected"
                    )

                # D2.1.1: Existence check
                for dep_id in deps:
                    if dep_id not in all_claim_ids:
                        result.add_error(
                            "content",
                            f"Claim {cid}: depends_on references non-existent claim {dep_id}",
                        )

        # D2.1.2: Cycle detection (DAG enforcement)
        cycle_path = self._detect_cycle(claims)
        if cycle_path:
            result.add_error(
                "content", f"Claim dependency cycle detected: {' → '.join(cycle_path)}"
            )

        # P-1: Validate evidence fields
        for ev in evidence_items:
            eid = ev.get("id", "unknown")
            ev_type = ev.get("type")
            access_status = ev.get("access_status")

            # P-1: Evidence Type validation
            if ev_type and ev_type not in self.EVIDENCE_TYPES:
                result.add_error(
                    "content",
                    f"Evidence {eid}: invalid type '{ev_type}'. "
                    f"Must be one of: {', '.join(sorted(self.EVIDENCE_TYPES))}",
                )

            # P-1: Access status validation
            # Per session-04: omit field for derived/CALCULATION, not "N/A"
            if ev_type == "CALCULATION":
                if access_status is not None:
                    if access_status == "N/A":
                        result.add_info(
                            "content",
                            f"Evidence {eid}: CALCULATION with access_status='N/A' - "
                            f"schema recommends omitting field entirely",
                        )
                    else:
                        result.add_warning(
                            "content",
                            f"Evidence {eid}: CALCULATION type should omit access_status field "
                            f"(found: {access_status})",
                        )
            elif ev_type == "USER_SUPPLIED":
                if access_status and access_status != "USER_SUPPLIED":
                    result.add_warning(
                        "content",
                        f"Evidence {eid}: USER_SUPPLIED type should have matching access_status",
                    )
            else:
                # Other types require access_status
                if not access_status:
                    result.add_error(
                        "content", f"Evidence {eid}: missing access_status field"
                    )
                elif access_status not in self.ACCESS_STATUSES:
                    result.add_error(
                        "content",
                        f"Evidence {eid}: invalid access_status '{access_status}'. "
                        f"Must be one of: {', '.join(sorted(self.ACCESS_STATUSES))}",
                    )

    def _detect_cycle(self, claims: list[dict]) -> list[str] | None:
        """
        Detect cycles in claim dependency graph using DFS.
        Returns cycle path if found, None otherwise.

        D2.1.2 implementation.
        """
        # Build adjacency list
        graph = {}
        for claim in claims:
            cid = claim.get("id", "")
            deps = claim.get("depends_on", [])
            graph[cid] = deps

        visited = set()
        rec_stack = set()

        def dfs(node: str, path: list[str]) -> list[str] | None:
            if node in rec_stack:
                # Cycle detected: return cycle path
                cycle_start = path.index(node)
                return path[cycle_start:] + [node]

            if node in visited:
                return None

            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for dep in graph.get(node, []):
                if (
                    dep in graph
                ):  # Only check if dep exists (existence already validated)
                    cycle = dfs(dep, path[:])
                    if cycle:
                        return cycle

            rec_stack.remove(node)
            return None

        # Check all nodes (handle disconnected components)
        for claim_id in graph:
            if claim_id not in visited:
                cycle = dfs(claim_id, [])
                if cycle:
                    return cycle

        return None

    def get_transitive_recheck_scope(
        self, changed_claim_ids: set[str], claims: list[dict]
    ) -> set[str]:
        """
        Calculate transitive recheck scope: changed claims + all claims that depend on them.

        D2.1.3 implementation (helper for differential audits).

        Args:
            changed_claim_ids: Set of claim IDs that were modified
            claims: List of claim dicts with 'id' and 'depends_on' fields

        Returns:
            Set of claim IDs to recheck (changed + dependents, transitive)
        """
        # Build reverse adjacency: claim_id -> [claims that depend on it]
        dependents = {}
        for claim in claims:
            cid = claim.get("id", "")
            for dep_id in claim.get("depends_on", []):
                if dep_id not in dependents:
                    dependents[dep_id] = []
                dependents[dep_id].append(cid)

        # BFS to find all transitive dependents
        scope = set(changed_claim_ids)
        queue = list(changed_claim_ids)

        while queue:
            current = queue.pop(0)
            for dependent_id in dependents.get(current, []):
                if dependent_id not in scope:
                    scope.add(dependent_id)
                    queue.append(dependent_id)

        return scope

    def _extract_claims(self, body: str) -> list[dict]:
        """Extract claim metadata from body"""
        claims = []
        # Pattern: **Claim Q{N}.C{M}** — ...
        pattern = r"\*\*Claim (Q\d+\.C\d+)\*\*"
        matches = re.finditer(pattern, body)

        for match in matches:
            cid = match.group(1)
            # Extract section after claim ID
            start = match.end()
            # Find next claim or section
            next_match = re.search(
                r"(\*\*Claim Q\d+\.C\d+\*\*|\*\*Evidence E\d+:\*\*|###)",
                body[start : start + 1000],
            )
            if next_match:
                content = body[start : start + next_match.start()]
            else:
                content = body[start : start + 500]

            claim = {"id": cid}

            # Extract depends_on
            if m := re.search(r"\*\*Depends on:\*\* \[([^\]]*)\]", content):
                deps_str = m.group(1)
                if deps_str.strip():
                    # Parse list like "Q1.C1", "Q1.C2"
                    deps = [d.strip(" \"'") for d in deps_str.split(",") if d.strip()]
                    claim["depends_on"] = deps
                else:
                    claim["depends_on"] = []

            claims.append(claim)

        return claims

    def _extract_evidence(self, body: str) -> list[dict]:
        """Extract evidence metadata from body"""
        evidence = []
        # Pattern: **Evidence E{N}:**
        pattern = r"\*\*Evidence (E\d+):\*\*"
        matches = re.finditer(pattern, body)

        for match in matches:
            eid = match.group(1)
            start = match.end()
            # Find next evidence or section
            next_match = re.search(
                r"(\*\*Evidence E\d+:\*\*|\*\*Calculation|###)",
                body[start : start + 1000],
            )
            if next_match:
                content = body[start : start + next_match.start()]
            else:
                content = body[start : start + 500]

            ev = {"id": eid}

            # Extract Type
            if m := re.search(r"\*\*Type:\*\* (\w+)", content):
                ev["type"] = m.group(1)

            # Extract Access status
            if m := re.search(r"\*\*Access status:\*\* ([A-Z_]+)", content):
                ev["access_status"] = m.group(1)

            evidence.append(ev)

        return evidence

    def _validate_verification_report(
        self, fm: dict, body: str, result: ValidationResult
    ):
        """Validate verification report specific fields"""
        # Check audit_mode field
        if "audit_mode" not in fm:
            result.add_error("frontmatter", "verification_report requires 'audit_mode'")
        elif fm["audit_mode"] not in {"baseline", "differential"}:
            result.add_error("frontmatter", f"Invalid audit_mode: {fm['audit_mode']}")

        # If differential, should have change_requests_under_review
        if fm.get("audit_mode") == "differential":
            if "change_requests_under_review" not in fm:
                result.add_warning(
                    "frontmatter",
                    "differential audit should have change_requests_under_review",
                )

    def _validate_final_report(self, fm: dict, body: str, result: ValidationResult):
        """Validate final report specific fields"""
        # Final reports should reference Question Map and Research Packet
        source_refs = fm.get("source_refs", [])
        ref_types = {ref.get("type") for ref in source_refs if isinstance(ref, dict)}

        if "question_map" not in ref_types:
            result.add_warning(
                "frontmatter",
                "final_report should reference question_map in source_refs",
            )
        if "research_packet" not in ref_types:
            result.add_warning(
                "frontmatter",
                "final_report should reference research_packet in source_refs",
            )

    def _validate_cr_status_cross_check(self, fm: dict, result: ValidationResult):
        """
        P-3: Cross-check producer self-declared CR status against verification report.

        Producer frontmatter may claim CR "resolved" but acceptance criteria unmet.
        Must cross-check against the latest verification report's CR-resolution record.
        """
        if not self.run_workspace or not self.run_workspace.exists():
            result.add_info(
                "cross-check",
                "P-3: CR status cross-check skipped (no run workspace provided)",
            )
            return

        # Get CRs claimed as addressed
        crs_addressed = fm.get("change_requests_addressed", [])

        for cr_entry in crs_addressed:
            if not isinstance(cr_entry, dict):
                continue

            cr_id = cr_entry.get("cr_id")
            claimed_status = cr_entry.get("status")

            if claimed_status == "resolved":
                # Find latest verification report that checked this CR
                verified = self._find_cr_verification(cr_id)

                if verified is None:
                    result.add_warning(
                        "cross-check",
                        f"P-3: CR {cr_id} claimed 'resolved' but no verification report found",
                    )
                elif verified["status"] != "resolved":
                    result.add_error(
                        "cross-check",
                        f"P-3: CR {cr_id} self-declared 'resolved' but verification report "
                        f"shows '{verified['status']}' (false-resolution, fx07 pattern)",
                    )

    def _find_cr_verification(self, cr_id: str) -> dict | None:
        """Find latest verification report that resolved this CR"""
        if not self.run_workspace:
            return None

        # Look for verification reports in workspace
        verification_reports = sorted(self.run_workspace.glob("*verification*.md"))

        for vr_path in reversed(verification_reports):  # Latest first
            try:
                content = vr_path.read_text(encoding="utf-8")
                # Look for CR resolution table with this CR
                if cr_id in content:
                    # Simple heuristic: if "resolved" appears near CR_id
                    window_start = content.find(cr_id)
                    if window_start >= 0:
                        window = content[window_start : window_start + 500]
                        if "resolved" in window.lower():
                            return {"status": "resolved", "source": vr_path}
                        elif "unmet" in window.lower() or "remaining" in window.lower():
                            return {"status": "unresolved", "source": vr_path}
            except:
                continue

        return None


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    paths = sys.argv[1:]
    all_results = []
    error_count = 0

    for path_str in paths:
        path = Path(path_str)

        if path.is_dir():
            # Validate all .md files in directory
            md_files = list(path.glob("*.md"))
            if not md_files:
                print(f"No .md files found in {path}", file=sys.stderr)
                continue

            for md_file in md_files:
                # Determine run workspace for cross-checking
                run_workspace = (
                    md_file.parent if md_file.parent.name.startswith("2026-") else None
                )
                validator = ArtifactValidator(run_workspace=run_workspace)
                result = validator.validate_file(md_file)
                all_results.append(result)
        else:
            # Single file
            run_workspace = (
                path.parent if path.parent.name.startswith("2026-") else None
            )
            validator = ArtifactValidator(run_workspace=run_workspace)
            result = validator.validate_file(path)
            all_results.append(result)

    # Report results
    for result in all_results:
        status = "✓" if result.valid else "✗"
        print(f"{status} {result.path}")

        if result.artifact_type:
            print(f"  Type: {result.artifact_type} {result.version or ''}")

        for finding in result.findings:
            symbol = {"ERROR": "✗", "WARNING": "⚠", "INFO": "ℹ"}[finding.severity]
            location = f" ({finding.location})" if finding.location else ""
            print(
                f"  {symbol} [{finding.severity}] {finding.category}: {finding.message}{location}"
            )

        if not result.valid:
            error_count += 1

        print()

    # Summary
    total = len(all_results)
    valid = total - error_count
    print(f"Summary: {valid}/{total} valid artifacts")

    if error_count > 0:
        print(f"{error_count} artifact(s) with errors", file=sys.stderr)
        sys.exit(1)
    else:
        print("All artifacts valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
