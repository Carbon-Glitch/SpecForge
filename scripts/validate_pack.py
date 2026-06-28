#!/usr/bin/env python3
"""Validate a specforge document pack.

The validator checks structure and minimum execution-readiness signals. It does
not judge product quality; it catches missing files, missing sections, missing
research ledger categories, and empty traceability artifacts.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_DOCS: dict[str, list[str]] = {
    "00-product-brief.md": [
        "Concept",
        "Target Users",
        "Jobs To Be Done",
        "Success Criteria",
        "Open Questions",
    ],
    "01-reality-research.md": [
        "Research Status",
        "Market Reality",
        "Official Documentation Findings",
        "GitHub And Open Source Findings",
        "Open Source Reuse Decisions",
        "Sources",
    ],
    "02-prd-behavior-contract.md": [
        "Problem Statement",
        "Scope",
        "Anti Goals",
        "Behavior Contract",
        "Guardrails",
    ],
    "03-sdd-requirements-spec.md": [
        "Functional Requirements",
        "Non Functional Requirements",
        "EARS Acceptance Criteria",
    ],
    "04-technical-design.md": [
        "Architecture Overview",
        "Stack Decision",
        "Open Source Reuse Plan",
        "Module Boundaries",
        "State Truth Model",
        "Workflow Navigation Action Contract",
        "Generated Artifact Plan",
        "Failure Handling",
        "Observability",
    ],
    "05-contracts-data-permissions.md": [
        "API Contracts",
        "Data Model",
        "State Model Contract",
        "Tool Contracts",
        "Permission Mapping",
        "Module File Responsibility Contract",
    ],
    "06-eval-golden-dataset.md": [
        "Launch Thresholds",
        "Deterministic Judge Contract",
        "Evidence Matrix",
        "Data Sufficiency Check",
        "Golden Cases",
        "Bad Cases",
        "Regression Gates",
    ],
    "07-agent-execution-plan.md": [
        "Agent Operating Rules",
        "Task List",
        "Source Vs Generated Rules",
        "Validation Commands",
        "Done Definition",
    ],
}

SUPPORT_FILES = [
    "traceability_matrix.json",
    "research_ledger.json",
    "handoff_manifest.json",
]


def heading_present(text: str, heading: str) -> bool:
    """Return true if a markdown heading exists."""
    pattern = rf"^##+\s+{re.escape(heading)}\s*$"
    return re.search(pattern, text, flags=re.MULTILINE) is not None


def validate_json(path: Path) -> list[str]:
    """Validate a JSON file and return errors."""
    errors: list[str] = []
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing support file: {path.name}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path.name}: {exc}")
    return errors


def validate_research_ledger(pack_dir: Path, strict: bool) -> list[str]:
    """Validate research ledger shape and optional source counts."""
    path = pack_dir / "research_ledger.json"
    errors = validate_json(path)
    if errors:
        return errors
    data = json.loads(path.read_text(encoding="utf-8"))
    categories = data.get("categories", {})
    required = [
        "market",
        "official_docs",
        "github_open_source",
        "open_source_reuse_decisions",
        "risk_compliance",
        "implementation_prior_art",
    ]
    for key in required:
        if key not in categories:
            errors.append(f"research_ledger.json missing category: {key}")
        elif strict and not categories[key]:
            errors.append(f"strict mode: research category has no sources: {key}")
    return errors


def validate_pack(pack_dir: Path, strict: bool = False) -> list[str]:
    """Validate a generated pack and return error messages."""
    errors: list[str] = []
    if not pack_dir.exists():
        return [f"pack directory does not exist: {pack_dir}"]

    for filename, headings in REQUIRED_DOCS.items():
        path = pack_dir / filename
        if not path.exists():
            errors.append(f"missing document: {filename}")
            continue
        text = path.read_text(encoding="utf-8")
        for heading in headings:
            if not heading_present(text, heading):
                errors.append(f"{filename} missing heading: {heading}")
        if strict and "<!-- Fill with specific" in text:
            errors.append(f"strict mode: placeholder remains in {filename}")

    for filename in SUPPORT_FILES:
        errors.extend(validate_json(pack_dir / filename))

    errors.extend(validate_research_ledger(pack_dir, strict))
    return errors


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Validate an SDD document pack.")
    parser.add_argument("pack_dir", nargs="?", default="sdd-docs")
    parser.add_argument("--strict", action="store_true", help="Require sources and no placeholders")
    args = parser.parse_args()

    errors = validate_pack(Path(args.pack_dir), strict=args.strict)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("VALID")


if __name__ == "__main__":
    main()
