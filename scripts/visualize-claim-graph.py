#!/usr/bin/env python3
"""
Visualize claim dependency graph from a Research Packet.

Usage:
    uv run --with pyyaml --with graphviz scripts/visualize-claim-graph.py <research-packet-path> [options]

Options:
    --output <path>      Output file path (default: claim-graph.svg)
    --format <fmt>       Output format: svg, png, pdf, dot (default: svg)
    --changed <ids>      Comma-separated changed claim IDs to highlight (e.g., Q1.C1,Q1.C3)
    --no-render          Only generate DOT file, don't render to image

Examples:
    # Generate SVG
    uv run --with pyyaml --with graphviz scripts/visualize-claim-graph.py runs/.work/2026-11-08-fx01-short-simple/02-research-packet-v1.md

    # Highlight changed claims
    uv run --with pyyaml --with graphviz scripts/visualize-claim-graph.py packet.md --changed Q1.C1,Q1.C3

    # Generate PNG
    uv run --with pyyaml --with graphviz scripts/visualize-claim-graph.py packet.md --format png --output graph.png

D2.2 implementation (session 05).
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import graphviz
    import yaml
except ImportError as e:
    print(f"Error: Missing dependency: {e}")
    print("Run with: uv run --with pyyaml --with graphviz scripts/visualize-claim-graph.py")
    sys.exit(1)


class ClaimGraph:
    """Claim dependency graph extractor and visualizer"""

    def __init__(self, packet_path: Path):
        self.packet_path = packet_path
        self.claims = []
        self.frontmatter = {}

    def parse(self):
        """Parse Research Packet and extract claims + dependencies"""
        content = self.packet_path.read_text()

        # Parse frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                self.frontmatter = yaml.safe_load(parts[1])
                body = parts[2]
            else:
                body = content
        else:
            body = content

        # Extract claims
        pattern = r"\*\*Claim (Q\d+\.C\d+)\*\*"
        matches = re.finditer(pattern, body)

        for match in matches:
            cid = match.group(1)
            start = match.end()

            # Extract section after claim ID
            next_match = re.search(
                r"(\*\*Claim Q\d+\.C\d+\*\*|\*\*Evidence E\d+:\*\*|###)",
                body[start : start + 1000],
            )
            if next_match:
                content_section = body[start : start + next_match.start()]
            else:
                content_section = body[start : start + 500]

            claim = {"id": cid, "depends_on": []}

            # Extract depends_on
            if m := re.search(r"\*\*Depends on:\*\* \[([^\]]*)\]", content_section):
                deps_str = m.group(1)
                if deps_str.strip():
                    deps = [d.strip(" \"'") for d in deps_str.split(",") if d.strip()]
                    claim["depends_on"] = deps

            self.claims.append(claim)

        return len(self.claims)

    def build_graph(
        self, changed_claim_ids: set[str] | None = None
    ) -> graphviz.Digraph:
        """
        Build graphviz Digraph from claims.

        Args:
            changed_claim_ids: Set of claim IDs to highlight as changed

        Returns:
            graphviz.Digraph object
        """
        changed_claim_ids = changed_claim_ids or set()

        # Calculate transitive dependents if changed claims provided
        dependent_claim_ids = set()
        if changed_claim_ids:
            dependent_claim_ids = self._get_dependents(changed_claim_ids)

        # Create graph
        dot = graphviz.Digraph(comment="Claim Dependencies")
        dot.attr(rankdir="LR")
        dot.attr("node", shape="box", style="filled")

        # Add nodes
        for claim in self.claims:
            cid = claim["id"]

            if cid in changed_claim_ids:
                # Changed claims: red
                dot.node(cid, cid, fillcolor="#ffcccc", color="#cc0000", penwidth="2")
            elif cid in dependent_claim_ids:
                # Dependent claims: yellow
                dot.node(cid, cid, fillcolor="#ffffcc", color="#ccaa00", penwidth="1.5")
            else:
                # Unchanged claims: white
                dot.node(cid, cid, fillcolor="white", color="#666666")

        # Add edges
        for claim in self.claims:
            cid = claim["id"]
            for dep_id in claim["depends_on"]:
                # Edge from current claim to dependency
                # (dependency direction: A depends_on B → edge A→B)
                dot.edge(cid, dep_id)

        return dot

    def _get_dependents(self, changed_claim_ids: set[str]) -> set[str]:
        """
        Get all claims that (transitively) depend on changed claims.

        Args:
            changed_claim_ids: Set of changed claim IDs

        Returns:
            Set of dependent claim IDs (not including changed claims themselves)
        """
        # Build reverse adjacency: claim_id -> [claims that depend on it]
        dependents_map = {}
        for claim in self.claims:
            cid = claim["id"]
            for dep_id in claim["depends_on"]:
                if dep_id not in dependents_map:
                    dependents_map[dep_id] = []
                dependents_map[dep_id].append(cid)

        # BFS to find all transitive dependents
        dependents = set()
        queue = list(changed_claim_ids)

        while queue:
            current = queue.pop(0)
            for dependent_id in dependents_map.get(current, []):
                if dependent_id not in changed_claim_ids and dependent_id not in dependents:
                    dependents.add(dependent_id)
                    queue.append(dependent_id)

        return dependents

    def render(
        self,
        output_path: Path,
        format: str = "svg",
        changed_claim_ids: set[str] | None = None,
        no_render: bool = False,
    ):
        """
        Render claim graph to file.

        Args:
            output_path: Output file path
            format: Output format (svg, png, pdf, dot)
            changed_claim_ids: Set of changed claim IDs to highlight
            no_render: If True, only save DOT source without rendering
        """
        dot = self.build_graph(changed_claim_ids)

        if no_render:
            # Save DOT source only
            dot_path = output_path.with_suffix(".dot")
            dot_path.write_text(dot.source)
            print(f"DOT source saved to: {dot_path}")
        else:
            # Render to image
            dot.format = format
            output_base = str(output_path.with_suffix(""))
            rendered_path = dot.render(output_base, cleanup=True)
            print(f"Graph rendered to: {rendered_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Visualize claim dependency graph from Research Packet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage:")[1] if "Usage:" in __doc__ else "",
    )
    parser.add_argument("packet_path", type=Path, help="Path to Research Packet markdown file")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("claim-graph.svg"),
        help="Output file path (default: claim-graph.svg)",
    )
    parser.add_argument(
        "--format",
        choices=["svg", "png", "pdf", "dot"],
        default="svg",
        help="Output format (default: svg)",
    )
    parser.add_argument(
        "--changed",
        type=str,
        help="Comma-separated changed claim IDs to highlight (e.g., Q1.C1,Q1.C3)",
    )
    parser.add_argument(
        "--no-render",
        action="store_true",
        help="Only generate DOT file, don't render to image",
    )

    args = parser.parse_args()

    if not args.packet_path.exists():
        print(f"Error: File not found: {args.packet_path}")
        sys.exit(1)

    # Parse changed claim IDs
    changed_ids = set()
    if args.changed:
        changed_ids = {cid.strip() for cid in args.changed.split(",") if cid.strip()}

    # Parse and visualize
    graph = ClaimGraph(args.packet_path)
    num_claims = graph.parse()

    if num_claims == 0:
        print("Warning: No claims found in Research Packet")
        sys.exit(0)

    print(f"Found {num_claims} claims")
    if changed_ids:
        print(f"Highlighting changed claims: {', '.join(sorted(changed_ids))}")

    graph.render(args.output, args.format, changed_ids, args.no_render)


if __name__ == "__main__":
    main()
