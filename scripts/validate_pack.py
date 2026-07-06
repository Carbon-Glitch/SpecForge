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
    "preflight-idea-pressure-test.md": [
        "Pressure Test Status",
        "Verdict",
        "Scorecard",
        "SDD Mode Decision",
        "Core Assumption",
        "Fatal Flaws",
        "Problem Reality",
        "Current Behavior And Alternatives",
        "First 10 Users",
        "Two Week MVP Test",
        "Decision",
        "Evidence To Verify",
    ],
    "00-product-brief.md": [
        "Mode",
        "SDD Mode",
        "Brainstorming Summary",
        "Concept",
        "Target Users",
        "Jobs To Be Done",
        "Scope Boundary",
        "Prescriptive Inputs",
        "This Pack Owns",
        "Existing System Context",
        "Success Criteria",
        "Open Questions",
    ],
    "01-reality-research.md": [
        "Research Status",
        "Market Reality",
        "Existing System Reality",
        "Official Documentation Findings",
        "GitHub And Open Source Findings",
        "Open Source Reuse Decisions",
        "Sources",
    ],
    "02-prd-behavior-contract.md": [
        "Problem Statement",
        "Scope",
        "Anti Goals",
        "Compatibility Contract",
        "Behavior Contract",
        "Guardrails",
    ],
    "03-sdd-requirements-spec.md": [
        "Functional Requirements",
        "Non Functional Requirements",
        "EARS Acceptance Criteria",
        "Regression Requirements",
    ],
    "04-technical-design.md": [
        "Architecture Overview",
        "Stack Decision",
        "Architecture Decision Lens",
        "Frontend Architecture Decisions",
        "Backend Architecture Decisions",
        "Data Architecture Decisions",
        "Algorithm And Data Structure Decisions",
        "Open Source Reuse Plan",
        "Integration Plan",
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
        "Access And Permission Rules",
        "Cache And Consistency Contract",
        "Data Access And Index Contract",
        "Module File Responsibility Contract",
    ],
    "06-eval-and-test-cases.md": [
        "Launch Thresholds",
        "Deterministic Judge Contract",
        "Evidence Matrix",
        "Architecture Fitness Checks",
        "Data Sufficiency Check",
        "UI Judge",
        "Case Source Policy",
        "Reference Cases",
        "Bad Cases",
        "Regression Cases",
        "Regression Gates",
        "Launch Readiness Checks",
    ],
    "07-agent-execution-plan.md": [
        "Agent Operating Rules",
        "Task List",
        "Agent Session Plan",
        "Architecture Workstream Prompt Packets",
        "Source Vs Generated Rules",
        "Design And Visual Implementation Phase",
        "Living Spec Update Protocol",
        "Validation Commands",
        "Launch Handoff",
        "Done Definition",
    ],
    "08-ui-visual-design.md": [
        "Visual Design Status",
        "Design Source Of Truth",
        "Design Positioning",
        "Design Tokens",
        "Core Components",
        "Page Skeletons",
        "Interaction And Motion",
        "Responsive And Accessibility",
        "UI Judge Contract",
        "MVP Visual Non Goals",
        "Design Orchestration",
    ],
}

STAGE_DOCS = {
    "gate0": ["preflight-idea-pressure-test.md"],
    "gate1": [
        "preflight-idea-pressure-test.md",
        "00-product-brief.md",
        "01-reality-research.md",
    ],
    "gate2": [
        "preflight-idea-pressure-test.md",
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

HEADING_ALIASES: dict[str, list[str]] = {
    "Anti Goals": ["Anti-Goals", "Anti-goals", "Non Goals", "Non-Goals"],
    "Non Functional Requirements": ["Non-Functional Requirements", "Nonfunctional Requirements", "NFRs"],
    "Out Of Scope": ["Out of Scope", "Out-of-Scope"],
    "Workflow Navigation Action Contract": [
        "Workflow/Navigation/Action Contract",
        "Workflow Navigation And Action Contract",
        "Workflow Action Contract",
    ],
    "Access And Permission Rules": ["Permission Rules", "Access Rules", "Permissions"],
    "Module File Responsibility Contract": [
        "Module/File Responsibility Contract",
        "Module Responsibility Contract",
        "File Responsibility Contract",
    ],
    "UI Judge": ["Visual Judge", "UI Evaluation", "Visual Evaluation"],
    "SDD Mode": ["SDD Depth", "Spec Mode", "Specification Mode"],
    "Architecture Decision Lens": ["Architecture Decision Matrix", "ADR Decision Lens", "Technical Decision Matrix"],
    "Agent Session Plan": ["Prompt Packet Plan", "Agent Prompt Packets", "Session Plan"],
    "Living Spec Update Protocol": ["Spec Update Protocol", "Living Specification Protocol"],
    "Launch Readiness Checks": ["Production Readiness Checks", "Launch Checklist", "Production Checklist"],
    "Launch Handoff": ["Production Handoff", "Release Handoff"],
    "Frontend Architecture Decisions": ["Frontend Decision Matrix", "Frontend Architecture Matrix"],
    "Backend Architecture Decisions": ["Backend Decision Matrix", "Backend Architecture Matrix"],
    "Data Architecture Decisions": ["Database Architecture Decisions", "Data Decision Matrix"],
    "Algorithm And Data Structure Decisions": ["Algorithm Decisions", "Algorithmic Decisions", "Data Structure Decisions"],
    "Cache And Consistency Contract": ["Cache Consistency Contract", "Caching And Consistency"],
    "Data Access And Index Contract": ["Index Contract", "Query And Index Contract", "Data Access Contract"],
    "Architecture Fitness Checks": ["Architecture Validation Checks", "Fitness Checks"],
    "Architecture Workstream Prompt Packets": ["Workstream Prompt Packets", "Architecture Prompt Packets"],
}


def normalize_heading(value: str) -> str:
    """Normalize a markdown heading for tolerant matching."""
    value = value.lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def heading_present(text: str, heading: str) -> bool:
    """Return true if a markdown heading exists."""
    wanted = [heading, *HEADING_ALIASES.get(heading, [])]
    existing = [
        match.group(1).strip()
        for match in re.finditer(r"^##+\s+(.+?)\s*$", text, flags=re.MULTILINE)
    ]
    existing_normalized = {normalize_heading(item) for item in existing}
    return any(normalize_heading(item) in existing_normalized for item in wanted)


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
    if "research_depth" not in data:
        errors.append("research_ledger.json missing research_depth")
    elif data.get("research_depth") not in {"light", "standard", "deep"}:
        errors.append("research_ledger.json research_depth must be light, standard, or deep")
    if "unverified_claims" not in data:
        errors.append("research_ledger.json missing unverified_claims")
    pressure_test = data.get("idea_pressure_test")
    if not isinstance(pressure_test, dict):
        errors.append("research_ledger.json missing idea_pressure_test object")
    elif strict:
        if pressure_test.get("status") in {None, "", "pending"}:
            errors.append("strict mode: idea_pressure_test.status must be completed, skipped, or blocked")
        if not pressure_test.get("decision"):
            errors.append("strict mode: idea_pressure_test.decision is required")
    categories = data.get("categories", {})
    required = [
        "market",
        "official_docs",
        "github_open_source",
        "open_source_reuse_decisions",
        "risk_compliance",
        "implementation_prior_art",
        "architecture_decision_sources",
        "production_readiness",
        "domain_architecture",
    ]
    for key in required:
        if key not in categories:
            errors.append(f"research_ledger.json missing category: {key}")
        elif strict and not categories[key]:
            errors.append(f"strict mode: research category has no sources: {key}")
    return errors


def validate_handoff_manifest(pack_dir: Path, strict: bool) -> list[str]:
    """Validate handoff readiness semantics."""
    path = pack_dir / "handoff_manifest.json"
    errors = validate_json(path)
    if errors:
        return errors
    data = json.loads(path.read_text(encoding="utf-8"))
    readiness = data.get("build_readiness")
    if readiness not in {
        "gate-review-required",
        "spec-incomplete",
        "spec-complete",
        "build-ready",
        "launch-ready",
        "demo-only",
        "blocked",
    }:
        errors.append(f"handoff_manifest.json has unknown build_readiness: {readiness}")
    if readiness == "build-ready":
        eval_text = (pack_dir / "06-eval-and-test-cases.md").read_text(encoding="utf-8") if (pack_dir / "06-eval-and-test-cases.md").exists() else ""
        plan_text = (pack_dir / "07-agent-execution-plan.md").read_text(encoding="utf-8") if (pack_dir / "07-agent-execution-plan.md").exists() else ""
        if not section_text(eval_text, "Automated Checks").strip():
            errors.append("build-ready requires non-empty 06 Automated Checks")
        if "```" not in section_text(plan_text, "Validation Commands") and "manual-only" not in plan_text.lower():
            errors.append("build-ready requires runnable 07 Validation Commands or explicit manual-only marking")
    if readiness == "launch-ready":
        eval_text = (pack_dir / "06-eval-and-test-cases.md").read_text(encoding="utf-8") if (pack_dir / "06-eval-and-test-cases.md").exists() else ""
        plan_text = (pack_dir / "07-agent-execution-plan.md").read_text(encoding="utf-8") if (pack_dir / "07-agent-execution-plan.md").exists() else ""
        launch_text = section_text(eval_text, "Launch Readiness Checks") + section_text(plan_text, "Launch Handoff")
        for term in ["security", "performance", "monitoring", "CI/CD", "rollback"]:
            if term.lower() not in launch_text.lower():
                errors.append(f"launch-ready requires launch readiness evidence for: {term}")
    if strict and data.get("gates_skipped") and "single-pass" not in json.dumps(data, ensure_ascii=False).lower():
        errors.append("strict mode: gates_skipped must record an explicit single-pass rationale")
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


def validate_eval_cases(pack_dir: Path, strict: bool) -> list[str]:
    """Validate source provenance and obvious self-certification patterns."""
    errors: list[str] = []
    path = pack_dir / "06-eval-and-test-cases.md"
    if not path.exists():
        return errors
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    allowed_sources = ["user-confirmed", "real-source-derived", "existing-test-derived", "synthetic"]
    if strict:
        if not any(source in lower for source in allowed_sources):
            errors.append(
                "strict mode: reference/bad/regression cases must include source markers: "
                "user-confirmed, real-source-derived, existing-test-derived, or synthetic"
            )
        if (
            "synthetic" in lower
            and "user-confirmed" not in lower
            and "real-source-derived" not in lower
            and "existing-test-derived" not in lower
        ):
            errors.append("strict mode: build-ready evals must not rely only on synthetic cases")

    case_sections = "\n".join(
        section_text(text, heading)
        for heading in ["Reference Cases", "Bad Cases", "Regression Cases", "Edge Cases"]
    )
    contradiction = re.search(
        r"\b(ok|pass|passed|success|succeeded|通过)\b.*\b(error|failed|failure|exception|traceback|错误|失败)\b",
        case_sections.lower(),
    )
    if contradiction:
        errors.append("06-eval-and-test-cases.md has a pass/ok case that also contains error/failure language")

    case_lines = [
        normalize_case_line(line)
        for line in case_sections.splitlines()
        if line.strip().startswith(("-", "|")) and len(normalize_case_line(line)) >= 20
    ]
    if len(case_lines) >= 3:
        unique_ratio = len(set(case_lines)) / len(case_lines)
        if unique_ratio < 0.67:
            errors.append("06-eval-and-test-cases.md has too many near-duplicate case lines")
    return errors


def validate_requirement_task_refs(pack_dir: Path, strict: bool) -> list[str]:
    """Check that requirement IDs are at least referenced by the task plan."""
    if not strict:
        return []
    req_path = pack_dir / "03-sdd-requirements-spec.md"
    plan_path = pack_dir / "07-agent-execution-plan.md"
    if not req_path.exists() or not plan_path.exists():
        return []
    req_text = req_path.read_text(encoding="utf-8")
    plan_text = plan_path.read_text(encoding="utf-8")
    ids = sorted(set(re.findall(r"\b(?:FR|NFR)-\d+\b", req_text)))
    if not ids:
        return []
    missing = [item for item in ids if item not in plan_text and "manual-only" not in plan_text.lower()]
    if missing:
        return [f"strict mode: requirement IDs not referenced in 07 task plan: {', '.join(missing[:10])}"]
    return []


def validate_architecture_decision_lens(pack_dir: Path, strict: bool) -> list[str]:
    """Validate that architecture decisions carry durable reasoning."""
    errors: list[str] = []
    path = pack_dir / "04-technical-design.md"
    if not path.exists():
        return errors
    text = path.read_text(encoding="utf-8")
    section = section_text(text, "Architecture Decision Lens")
    if not section:
        return errors
    required_terms = ["Real Pain Solved", "One-Year Technical Debt", "Team Scaling Cost", "Migration"]
    missing = [term for term in required_terms if term.lower() not in section.lower()]
    if missing:
        errors.append(f"04 Architecture Decision Lens missing concepts: {', '.join(missing)}")
    if strict and "01-reality-research.md" not in section and "research_ledger" not in section and "http" not in section:
        errors.append("strict mode: 04 Architecture Decision Lens must cite research evidence")
    return errors


def validate_domain_architecture_decisions(pack_dir: Path, strict: bool) -> list[str]:
    """Validate frontend/backend/data/algorithm decision scaffolds."""
    errors: list[str] = []
    path = pack_dir / "04-technical-design.md"
    if not path.exists():
        return errors
    text = path.read_text(encoding="utf-8")
    required = {
        "Frontend Architecture Decisions": ["rendering", "state", "motion", "Validation"],
        "Backend Architecture Decisions": ["deployment", "domain", "API", "async", "caching"],
        "Data Architecture Decisions": ["store", "migrations", "indexes", "transactions", "retention"],
        "Algorithm And Data Structure Decisions": ["search", "ranking", "rate", "scheduling", "graph"],
    }
    for heading, terms in required.items():
        section = section_text(text, heading)
        if not section:
            continue
        missing = [term for term in terms if term.lower() not in section.lower()]
        if missing:
            errors.append(f"04 {heading} missing decision dimensions: {', '.join(missing)}")
    if strict:
        eval_text = (pack_dir / "06-eval-and-test-cases.md").read_text(encoding="utf-8") if (pack_dir / "06-eval-and-test-cases.md").exists() else ""
        if not section_text(eval_text, "Architecture Fitness Checks"):
            errors.append("strict mode: 06 must include Architecture Fitness Checks for domain architecture decisions")
    return errors


def validate_agent_session_plan(pack_dir: Path, strict: bool) -> list[str]:
    """Validate prompt packets and living-spec update rules."""
    errors: list[str] = []
    path = pack_dir / "07-agent-execution-plan.md"
    if not path.exists():
        return errors
    text = path.read_text(encoding="utf-8")
    session = section_text(text, "Agent Session Plan")
    if session:
        required_terms = ["Role", "Context", "Task", "Constraints", "Output", "Validation"]
        missing = [term for term in required_terms if term.lower() not in session.lower()]
        if missing:
            errors.append(f"07 Agent Session Plan missing prompt-packet fields: {', '.join(missing)}")
    if strict:
        living = section_text(text, "Living Spec Update Protocol")
        if not living or not any(term in living.lower() for term in ["behavior", "api", "schema", "permission"]):
            errors.append("strict mode: 07 Living Spec Update Protocol must cover behavior/API/schema/permission changes")
    return errors


def validate_ui_visual_contract(pack_dir: Path, strict: bool) -> list[str]:
    """Validate optional visual design contract when present."""
    errors: list[str] = []
    visual_path = pack_dir / "08-ui-visual-design.md"
    if not visual_path.exists():
        return errors
    text = visual_path.read_text(encoding="utf-8")
    for heading in REQUIRED_DOCS["08-ui-visual-design.md"]:
        if not heading_present(text, heading):
            errors.append(f"08-ui-visual-design.md missing heading: {heading}")
    eval_path = pack_dir / "06-eval-and-test-cases.md"
    plan_path = pack_dir / "07-agent-execution-plan.md"
    eval_text = eval_path.read_text(encoding="utf-8") if eval_path.exists() else ""
    plan_text = plan_path.read_text(encoding="utf-8") if plan_path.exists() else ""
    if "screenshot_manual" not in eval_text and "a11y_contrast" not in eval_text and "route_snapshot" not in eval_text:
        errors.append("08-ui-visual-design.md present but 06 UI Judge lacks screenshot_manual, a11y_contrast, or route_snapshot")
    if strict and "08-ui-visual-design.md" not in plan_text and "DESIGN.md" not in plan_text:
        errors.append("strict mode: 07 must cite 08-ui-visual-design.md or DESIGN.md when visual contract exists")
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

    if (pack_dir / "08-ui-visual-design.md").exists():
        # Optional document: validate when present, independent of stage.
        pass

    for filename in SUPPORT_FILES:
        errors.extend(validate_json(pack_dir / filename))

    errors.extend(validate_research_ledger(pack_dir, strict))
    errors.extend(validate_handoff_manifest(pack_dir, strict))
    if stage in {"gate3", "all"}:
        errors.extend(validate_eval_cases(pack_dir, strict))
        errors.extend(validate_requirement_task_refs(pack_dir, strict))
        errors.extend(validate_agent_session_plan(pack_dir, strict))
        errors.extend(validate_architecture_decision_lens(pack_dir, strict))
        errors.extend(validate_domain_architecture_decisions(pack_dir, strict))
    errors.extend(validate_ui_visual_contract(pack_dir, strict))
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
