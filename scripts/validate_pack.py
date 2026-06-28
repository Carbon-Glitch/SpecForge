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
        "Golden Case Source Policy",
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

STAGE_DOCS = {
    "gate1": ["00-product-brief.md", "01-reality-research.md"],
    "gate2": [
        "00-product-brief.md",
        "01-reality-research.md",
        "02-prd-behavior-contract.md",
        "03-sdd-requirements-spec.md",
        "04-technical-design.md",
    ],
    "gate3": list(REQUIRED_DOCS),
    "all": list(REQUIRED_DOCS),
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


def normalize_case_line(line: str) -> str:
    """Normalize an eval case line for rough duplicate detection."""
    line = re.sub(r"[`*_|\[\](){}:;,.!?-]+", " ", line.lower())
    line = re.sub(r"\b(fr|nfr|gc|bc|ec|case|id|source|expected|input|output)\b", " ", line)
    return re.sub(r"\s+", " ", line).strip()


def section_text(text: str, heading: str) -> str:
    """Extract markdown section text after a heading."""
    pattern = rf"^##+\s+{re.escape(heading)}\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        return ""
    rest = text[match.end() :]
    next_heading = re.search(r"^##+\s+", rest, flags=re.MULTILINE)
    return rest[: next_heading.start()] if next_heading else rest


def validate_golden_cases(pack_dir: Path, strict: bool) -> list[str]:
    """Validate source provenance and obvious self-certification patterns."""
    errors: list[str] = []
    path = pack_dir / "06-eval-golden-dataset.md"
    if not path.exists():
        return errors
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    allowed_sources = ["user-confirmed", "real-source-derived", "synthetic"]
    if strict:
        if not any(source in lower for source in allowed_sources):
            errors.append(
                "strict mode: golden/bad cases must include source markers: "
                "user-confirmed, real-source-derived, or synthetic"
            )
        if "synthetic" in lower and "user-confirmed" not in lower and "real-source-derived" not in lower:
            errors.append("strict mode: build-ready evals must not rely only on synthetic cases")

    case_sections = "\n".join(
        section_text(text, heading) for heading in ["Golden Cases", "Bad Cases", "Edge Cases"]
    )
    contradiction = re.search(
        r"\b(ok|pass|passed|success|succeeded|通过)\b.*\b(error|failed|failure|exception|traceback|错误|失败)\b",
        case_sections.lower(),
    )
    if contradiction:
        errors.append("06-eval-golden-dataset.md has a pass/ok case that also contains error/failure language")

    case_lines = [
        normalize_case_line(line)
        for line in case_sections.splitlines()
        if line.strip().startswith(("-", "|")) and len(normalize_case_line(line)) >= 20
    ]
    if len(case_lines) >= 3:
        unique_ratio = len(set(case_lines)) / len(case_lines)
        if unique_ratio < 0.67:
            errors.append("06-eval-golden-dataset.md has too many near-duplicate case lines")
    return errors


def validate_pack(pack_dir: Path, strict: bool = False, stage: str = "all") -> list[str]:
    """Validate a generated pack and return error messages."""
    errors: list[str] = []
    if not pack_dir.exists():
        return [f"pack directory does not exist: {pack_dir}"]

    for filename in STAGE_DOCS[stage]:
        headings = REQUIRED_DOCS[filename]
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
    if stage in {"gate3", "all"}:
        errors.extend(validate_golden_cases(pack_dir, strict))
    return errors


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Validate an SDD document pack.")
    parser.add_argument("pack_dir", nargs="?", default="sdd-docs")
    parser.add_argument(
        "--stage",
        choices=sorted(STAGE_DOCS),
        default="all",
        help="Validate only documents expected through this stage.",
    )
    parser.add_argument("--strict", action="store_true", help="Require sources and no placeholders")
    args = parser.parse_args()

    errors = validate_pack(Path(args.pack_dir), strict=args.strict, stage=args.stage)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("VALID")


if __name__ == "__main__":
    main()
