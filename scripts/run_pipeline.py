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
            "Scope Boundary",
            "Prescriptive Inputs",
            "This Pack Owns",
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
        "08-ui-visual-design.md",
        "visual",
        "UI Visual Design",
        [
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
            "UI Judge",
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
            "Design And Visual Implementation Phase",
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

GATE_REVIEW_ORDER = ["gate0", "gate1", "gate2"]

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
        body = "<!-- Fill with specific, sourced, AI-readable content. -->"
        if section == "Scope Boundary":
            body = (
                "| Area | Status | Rule |\n"
                "|---|---|---|\n"
                "| primary slice | in_pack | This pack specifies and tasks this scope. |\n"
                "| adjacent systems | referenced_only | Mention contracts only; do not task implementation. |\n"
                "| deferred systems | future_pack | Capture assumptions and future-pack handoff. |"
            )
        elif section == "Prescriptive Inputs":
            body = "| Source | Why It Is Prescriptive | Rule |\n|---|---|---|\n| TBD | TBD | TBD |"
        elif section == "This Pack Owns":
            body = "| Owned Area | Requirements | Explicit Non-Ownership |\n|---|---|---|\n| TBD | TBD | TBD |"
        elif section == "UI Judge":
            body = (
                "| Type | Target | Evidence |\n"
                "|---|---|---|\n"
                "| screenshot_manual | key route and viewport | reviewer checks non-overlap, minimum heights, and visual state |\n"
                "| a11y_contrast | token pairs | contrast meets selected threshold |\n"
                "| route_snapshot | key route | screenshot command proves expected screen, not a wrong/default page |"
            )
        elif section == "Design And Visual Implementation Phase":
            body = (
                "- If `08-ui-visual-design.md` exists, UI tasks must cite it before implementation.\n"
                "- If repo-level design governance is needed, create or refresh `DESIGN.md` with `$design` first.\n"
                "- If pixel/reference matching is required, hand off to `$visual-ralph` after reference approval."
            )
        elif section == "Design Orchestration":
            body = (
                "- `08-ui-visual-design.md` is the agent visual contract.\n"
                "- `DESIGN.md` is the durable repo design source of truth when needed.\n"
                "- `$visual-ralph` owns approved-reference implementation and visual verdict loops."
            )
        elif section == "UI Judge Contract":
            body = (
                "| Type | Requirement | Evidence |\n"
                "|---|---|---|\n"
                "| screenshot_manual | key screens fit at desktop and 375px mobile | screenshot path or manual review note |\n"
                "| a11y_contrast | text and controls meet contrast target | contrast command or manual audit |\n"
                "| route_snapshot | expected route renders the intended screen | screenshot command and route state |"
            )
        lines.extend(
            [
                f"## {section}",
                "",
                body,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def summarize_markdown_docs(repo_root: Path, limit: int = 40) -> list[dict[str, str]]:
    """Return a lightweight docs-first index for existing markdown files."""
    if not repo_root.exists():
        return []
    ignored_parts = {".git", "node_modules", ".venv", "venv", "dist", "build", ".next", ".cache"}
    docs: list[dict[str, str]] = []
    for path in sorted(repo_root.rglob("*.md")):
        if any(part in ignored_parts for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        title = ""
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                title = stripped.lstrip("#").strip()
                break
            if stripped:
                title = stripped[:90]
                break
        docs.append(
            {
                "path": str(path.relative_to(repo_root)),
                "title_or_first_line": title,
                "bytes": str(path.stat().st_size),
            }
        )
        if len(docs) >= limit:
            break
    return docs


def initial_traceability(idea: str, include_visual: bool) -> dict[str, Any]:
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
            "If 08-ui-visual-design.md exists, UI tasks must cite its visual contract and UI judge entries.",
        ],
        "optional_documents": ["08-ui-visual-design.md"] if include_visual else [],
    }


def initial_research_ledger(idea: str) -> dict[str, Any]:
    """Create an empty research ledger with required categories."""
    return {
        "schema": "specforge-research-ledger-v1",
        "product": idea,
        "generated_at": now_iso(),
        "status": "pending-live-research",
        "research_depth": "light",
        "unverified_claims": [],
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


def readiness_for_stage(stage: str) -> str:
    """Return conservative readiness for the scaffolded stage."""
    if stage in {"gate0", "gate1", "gate2"}:
        return "gate-review-required"
    return "spec-complete"


def initial_handoff(
    idea: str,
    out_dir: Path,
    stage: str,
    include_visual: bool,
    single_pass: bool,
    scope: str,
    exclude: str,
    repo_root: Path | None,
) -> dict[str, Any]:
    """Create a handoff manifest."""
    wanted_stages = set(STAGE_ORDER[stage])
    if include_visual:
        wanted_stages.add("visual")
    docs_index = summarize_markdown_docs(repo_root) if repo_root else []
    return {
        "schema": "specforge-handoff-v1",
        "product": idea,
        "generated_at": now_iso(),
        "stage": stage,
        "stage_gate": STAGE_NEXT_ACTION[stage],
        "documents": [filename for filename, doc_stage, _, _ in DOCS if doc_stage in wanted_stages],
        "pending_documents": [
            filename for filename, doc_stage, _, _ in DOCS if doc_stage not in wanted_stages and doc_stage != "visual"
        ],
        "optional_documents": ["08-ui-visual-design.md"] if include_visual else [],
        "support_artifacts": [
            "traceability_matrix.json",
            "research_ledger.json",
            "handoff_manifest.json",
        ],
        "output_dir": str(out_dir),
        "build_readiness": readiness_for_stage(stage),
        "build_readiness_meaning": {
            "spec-complete": "Documents and traceability can be reviewed for implementation.",
            "build-ready": "Requires populated seed data or fixtures, at least one runnable validation command, and non-empty automated checks.",
        },
        "scope": {
            "requested": scope or "full-product",
            "excluded": [item.strip() for item in exclude.split(",") if item.strip()],
            "rule": "Put in-pack, referenced-only, and future-pack boundaries in 00-product-brief.md#Scope Boundary and generated AGENTS.md.",
        },
        "docs_first": {
            "repo_root": str(repo_root) if repo_root else "",
            "markdown_docs_indexed": docs_index,
            "rule": "Treat existing repository docs as evidence; label prescriptive inputs separately from this pack's ownership.",
        },
        "gates_skipped": GATE_REVIEW_ORDER if single_pass and stage in {"gate3", "all"} else [],
        "open_questions": [],
        "next_action": STAGE_NEXT_ACTION[stage],
    }


def run_pipeline(
    idea: str,
    out_dir: Path,
    force: bool = False,
    stage: str = "gate0",
    include_visual: bool = False,
    single_pass: bool = False,
    scope: str = "",
    exclude: str = "",
    repo_root: Path | None = None,
) -> Path:
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
    wanted_stages = set(STAGE_ORDER[stage])
    if include_visual:
        wanted_stages.add("visual")
    for filename, doc_stage, title, sections in DOCS:
        if doc_stage not in wanted_stages:
            continue
        path = out_dir / filename
        if path.exists() and not force:
            continue
        path.write_text(render_doc(filename, title, sections, idea), encoding="utf-8")

    artifacts = {
        "traceability_matrix.json": initial_traceability(idea, include_visual),
        "research_ledger.json": initial_research_ledger(idea),
        "handoff_manifest.json": initial_handoff(
            idea=idea,
            out_dir=out_dir,
            stage=stage,
            include_visual=include_visual,
            single_pass=single_pass,
            scope=scope,
            exclude=exclude,
            repo_root=repo_root,
        ),
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
    parser.add_argument("--include-visual", action="store_true", help="Include optional 08-ui-visual-design.md")
    parser.add_argument("--single-pass", action="store_true", help="Record that staged gate review was intentionally skipped")
    parser.add_argument("--scope", default="", help="Scope slice to own in this pack, for example user-app-only")
    parser.add_argument("--exclude", default="", help="Comma-separated subsystems excluded from this pack")
    parser.add_argument("--repo-root", default="", help="Existing repository root for docs-first markdown indexing")
    args = parser.parse_args()

    repo_root = Path(args.repo_root) if args.repo_root else None
    out = run_pipeline(
        idea=args.idea,
        out_dir=Path(args.out),
        force=args.force,
        stage=args.stage,
        include_visual=args.include_visual,
        single_pass=args.single_pass,
        scope=args.scope,
        exclude=args.exclude,
        repo_root=repo_root,
    )
    print(f"Created SpecForge {args.stage} document pack at {out.resolve()}")
    print(STAGE_NEXT_ACTION[args.stage])
    if args.include_visual:
        print("Included optional 08-ui-visual-design.md. Use it as the agent visual contract; use DESIGN.md or Visual Ralph for deeper design governance or pixel matching.")
    if args.single_pass:
        print("Single-pass mode recorded in handoff_manifest.json.gates_skipped.")


if __name__ == "__main__":
    main()
