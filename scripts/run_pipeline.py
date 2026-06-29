#!/usr/bin/env python3
"""Create a SpecForge document pack skeleton.

This script is deterministic. It does not perform live web research or write
final product strategy. It creates a staged workspace, traceability files, and
validation-friendly headings that the agent must fill.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DOCS: list[tuple[str, str, str, list[str]]] = [
    (
        "preflight-idea-pressure-test.md",
        "gate0",
        "Idea Pressure Test",
        [
            "Pressure Test Status",
            "Verdict",
            "Scorecard",
            "Core Assumption",
            "Fatal Flaws",
            "Problem Reality",
            "Current Behavior And Alternatives",
            "First 10 Users",
            "Two Week MVP Test",
            "Decision",
            "Evidence To Verify",
        ],
    ),
    (
        "00-product-brief.md",
        "gate1",
        "Product Brief",
        [
            "Mode",
            "Brainstorming Summary",
            "Concept",
            "Target Users",
            "Jobs To Be Done",
            "Existing System Context",
            "Success Criteria",
            "Constraints",
            "Assumptions",
            "Open Questions",
        ],
    ),
    (
        "01-reality-research.md",
        "gate1",
        "Reality Research",
        [
            "Research Status",
            "Market Reality",
            "Competitors And Substitutes",
            "User Behavior Evidence",
            "Existing System Reality",
            "Official Documentation Findings",
            "GitHub And Open Source Findings",
            "Open Source Reuse Decisions",
            "Risk And Compliance Findings",
            "Implementation Prior Art",
            "Rejected Options",
            "Sources",
        ],
    ),
    (
        "02-prd-behavior-contract.md",
        "gate2",
        "PRD And Behavior Contract",
        [
            "Problem Statement",
            "Goals",
            "Personas",
            "Scope",
            "Anti Goals",
            "Core User Journeys",
            "Compatibility Contract",
            "Behavior Contract",
            "Guardrails",
            "Success Metrics",
            "Release Criteria",
        ],
    ),
    (
        "03-sdd-requirements-spec.md",
        "gate2",
        "SDD Requirements Spec",
        [
            "Functional Requirements",
            "Non Functional Requirements",
            "User Stories",
            "EARS Acceptance Criteria",
            "Regression Requirements",
            "Edge Cases",
            "Out Of Scope",
        ],
    ),
    (
        "04-technical-design.md",
        "gate2",
        "Technical Design",
        [
            "Architecture Overview",
            "Stack Decision",
            "Open Source Reuse Plan",
            "Integration Plan",
            "Module Boundaries",
            "Data Flow",
            "State Truth Model",
            "Workflow Navigation Action Contract",
            "Generated Artifact Plan",
            "Failure Handling",
            "Observability",
            "Performance And Cost",
            "Migration And Rollback",
        ],
    ),
    (
        "05-contracts-data-permissions.md",
        "gate3",
        "Contracts Data And Permissions",
        [
            "API Contracts",
            "Data Model",
            "State Model Contract",
            "Tool Contracts",
            "Access And Permission Rules",
            "Module File Responsibility Contract",
            "Security Boundaries",
            "Storage And Retention",
            "External Integrations",
        ],
    ),
    (
        "06-eval-and-test-cases.md",
        "gate3",
        "Eval And Test Cases",
        [
            "Eval Philosophy",
            "Launch Thresholds",
            "Deterministic Judge Contract",
            "Evidence Matrix",
            "Data Sufficiency Check",
            "Case Source Policy",
            "Reference Cases",
            "Bad Cases",
            "Regression Cases",
            "Edge Cases",
            "Automated Checks",
            "Manual Review",
            "Regression Gates",
        ],
    ),
    (
        "07-agent-execution-plan.md",
        "gate3",
        "Agent Execution Plan",
        [
            "Agent Operating Rules",
            "Implementation Phases",
            "Task List",
            "Parallelization",
            "Source Vs Generated Rules",
            "Validation Commands",
            "Handoff To Coding Agent",
            "Generated AGENTS.md Content",
            "Done Definition",
        ],
    ),
]

STAGE_ORDER = {
    "gate0": {"gate0"},
    "gate1": {"gate0", "gate1"},
    "gate2": {"gate0", "gate1", "gate2"},
    "gate3": {"gate0", "gate1", "gate2", "gate3"},
    "all": {"gate0", "gate1", "gate2", "gate3"},
}

STAGE_NEXT_ACTION = {
    "gate0": "Stop for user confirmation of the idea pressure test before writing product brief or research docs.",
    "gate1": "Stop for user confirmation of product brief and reality research before writing PRD or technical design.",
    "gate2": "Stop for user confirmation of PRD, requirements, and technical design before writing contracts, evals, and task plan.",
    "gate3": "Review the full pack, run validation, then hand off to the coding agent.",
    "all": "Review the full pack, run validation, then hand off to the coding agent.",
}


def slugify(value: str) -> str:
    """Return a stable short slug for filenames and IDs."""
    text = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", value.strip()).strip("-")
    return text[:48] or "product"


def now_iso() -> str:
    """Return an ISO timestamp in UTC."""
    return datetime.now(timezone.utc).isoformat()


def render_doc(filename: str, title: str, sections: list[str], idea: str) -> str:
    """Render one markdown document skeleton."""
    lines = [
        f"# {title}",
        "",
        f"- Product idea: {idea}",
        f"- Generated: {now_iso()}",
        "- Status: draft",
        "- Research requirement: live web research must be completed before final claims",
        "",
    ]
    for section in sections:
        lines.extend(
            [
                f"## {section}",
                "",
                "<!-- Fill with specific, sourced, AI-readable content. -->",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def initial_traceability(idea: str) -> dict[str, Any]:
    """Create a traceability matrix placeholder."""
    return {
        "schema": "specforge-traceability-v1",
        "product": idea,
        "generated_at": now_iso(),
        "coverage": [],
        "rules": [
            "Every requirement must map to at least one design decision.",
            "Every requirement must map to at least one task.",
            "Every task must map to at least one validation command or evidence requirement.",
            "Every current-world claim must map to a research ledger source.",
            "Every generated artifact must map to a source declaration and regeneration command.",
            "Every requirement must declare a deterministic judge or explicit manual evidence.",
            "Reference, bad, and regression cases must declare a source: user-confirmed, real-source-derived, existing-test-derived, or synthetic.",
            "Build-ready packs must not rely only on synthetic reference cases.",
            "Greenfield commercial products should pass the idea pressure test or carry an explicit pivot/research-needed decision before Gate 1.",
        ],
    }


def initial_research_ledger(idea: str) -> dict[str, Any]:
    """Create an empty research ledger with required categories."""
    return {
        "schema": "specforge-research-ledger-v1",
        "product": idea,
        "generated_at": now_iso(),
        "status": "pending-live-research",
        "idea_pressure_test": {
            "status": "pending",
            "verdict": "unknown",
            "core_assumption": "",
            "decision": "not-reviewed",
            "evidence_to_verify": [],
        },
        "categories": {
            "market": [],
            "official_docs": [],
            "github_open_source": [],
            "open_source_reuse_decisions": [],
            "risk_compliance": [],
            "implementation_prior_art": [],
        },
        "source_fields": [
            "title",
            "url",
            "publisher",
            "published_or_updated",
            "accessed_at",
            "claim_supported",
            "confidence",
        ],
    }


def initial_handoff(idea: str, out_dir: Path, stage: str) -> dict[str, Any]:
    """Create a handoff manifest."""
    return {
        "schema": "specforge-handoff-v1",
        "product": idea,
        "generated_at": now_iso(),
        "stage": stage,
        "stage_gate": STAGE_NEXT_ACTION[stage],
        "documents": [filename for filename, doc_stage, _, _ in DOCS if doc_stage in STAGE_ORDER[stage]],
        "pending_documents": [
            filename for filename, doc_stage, _, _ in DOCS if doc_stage not in STAGE_ORDER[stage]
        ],
        "support_artifacts": [
            "traceability_matrix.json",
            "research_ledger.json",
            "handoff_manifest.json",
        ],
        "output_dir": str(out_dir),
        "build_readiness": "gate-review-required" if stage in {"gate0", "gate1", "gate2"} else "not-ready-until-research-and-validation-complete",
        "open_questions": [],
        "next_action": STAGE_NEXT_ACTION[stage],
    }


def run_pipeline(idea: str, out_dir: Path, force: bool = False, stage: str = "gate1") -> Path:
    """Create the document pack.

    Args:
        idea: Product concept or rough requirement.
        out_dir: Directory to create.
        force: Overwrite existing generated files when true.
        stage: Document stage to scaffold.

    Returns:
        The output directory path.

    Raises:
        FileExistsError: If files exist and force is false.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    wanted_stages = STAGE_ORDER[stage]
    for filename, doc_stage, title, sections in DOCS:
        if doc_stage not in wanted_stages:
            continue
        path = out_dir / filename
        if path.exists() and not force:
            continue
        path.write_text(render_doc(filename, title, sections, idea), encoding="utf-8")

    artifacts = {
        "traceability_matrix.json": initial_traceability(idea),
        "research_ledger.json": initial_research_ledger(idea),
        "handoff_manifest.json": initial_handoff(idea, out_dir, stage),
    }
    for filename, data in artifacts.items():
        path = out_dir / filename
        if path.exists() and not force:
            continue
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_dir


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Create a staged SpecForge SDD pack.")
    parser.add_argument("--idea", required=True, help="Product concept or rough requirement")
    parser.add_argument("--out", default="sdd-docs", help="Output directory")
    parser.add_argument(
        "--stage",
        choices=sorted(STAGE_ORDER),
        default="gate0",
        help="Scaffold gate0, gate1, gate2, gate3, or all documents. Default: gate0.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing generated files")
    args = parser.parse_args()

    out = run_pipeline(args.idea, Path(args.out), args.force, args.stage)
    print(f"Created SpecForge {args.stage} document pack at {out.resolve()}")


if __name__ == "__main__":
    main()
