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
    ),
    (
        "00-product-brief.md",
        "gate1",
        "Product Brief",
        [
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
            "Temporal Freshness Guard",
            "Search Query Log",
            "Freshness Assessment",
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
            "Architecture Decision Lens",
            "Frontend Architecture Decisions",
            "Backend Architecture Decisions",
            "Data Architecture Decisions",
            "Algorithm And Data Structure Decisions",
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
            "Cache And Consistency Contract",
            "Data Access And Index Contract",
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
            "Architecture Fitness Checks",
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
            "Launch Readiness Checks",
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
            "Agent Session Plan",
            "Architecture Workstream Prompt Packets",
            "Parallelization",
            "Source Vs Generated Rules",
            "Design And Visual Implementation Phase",
            "Living Spec Update Protocol",
            "Validation Commands",
            "Launch Handoff",
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


def current_date_anchor() -> dict[str, Any]:
    """Return a local date anchor for freshness-aware research."""
    local_now = datetime.now().astimezone()
    offset = local_now.strftime("%z")
    timezone_label = f"UTC{offset[:3]}:{offset[3:]}" if offset else "local"
    return {
        "current_date": local_now.date().isoformat(),
        "current_year": local_now.year,
        "timezone": timezone_label,
        "recorded_at": now_iso(),
    }


def freshness_policy() -> dict[str, Any]:
    """Return default freshness windows for current-world claims."""
    return {
        "market_window_days": 180,
        "fast_moving_technology_window_days": 90,
        "github_activity_window_days": 365,
        "regulatory_window_days": 365,
        "source_status_values": ["fresh", "acceptable", "stale", "undated", "blocked"],
        "stale_year_query_policy": (
            "Do not use old years in latest/current queries unless the query is explicitly "
            "historical, migration-related, backward-compatibility-related, or user-specified."
        ),
    }


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
        if section == "SDD Mode Decision":
            body = (
                "| Signal | Observation | Mode Impact |\n"
                "|---|---|---|\n"
                "| production intent | TBD | choose `full-sdd` or `production-hardening` when real users, money, privacy, or team handoff matter |\n"
                "| context drift risk | TBD | move from `vibe-prototype` to `spec-lite` or `full-sdd` when the agent may lose the plot |\n"
                "| regression risk | TBD | require contracts and evals when changes can break existing behavior |\n"
                "| team scaling | TBD | prefer clearer boundaries and prompt packets when multiple contributors or agents work in parallel |"
            )
        elif section == "SDD Mode":
            body = (
                "| Mode | Use When | Required Pack Depth |\n"
                "|---|---|---|\n"
                "| `vibe-prototype` | disposable demo or learning spike | Gate 0/1 light, no build-ready claim |\n"
                "| `spec-lite` | small feature or low-risk MVP slice | Gate 1 plus focused Gate 2/3 sections |\n"
                "| `full-sdd` | production-intended product or broad feature | all gates, traceability, evals, contracts |\n"
                "| `production-hardening` | existing app nearing launch | full-sdd plus launch readiness and rollback evidence |"
            )
        elif section == "Temporal Freshness Guard":
            anchor = current_date_anchor()
            body = (
                f"- Current date anchor: `{anchor['current_date']}` ({anchor['timezone']}).\n"
                "- Search queries must derive year/date terms from this anchor, not from model memory.\n"
                "- Do not use stale hardcoded years for latest/current research unless the query is explicitly historical, migration-related, or user-specified.\n"
                "- Fast-moving market, framework, model, SDK, policy, pricing, and GitHub health claims need fresh primary-source evidence or an explicit degraded/unverified label."
            )
        elif section == "Search Query Log":
            body = (
                "| Category | Query | Target | Date Basis | Status | Notes |\n"
                "|---|---|---|---|---|---|\n"
                "| market | TBD latest/current + anchored year terms | web | current_date_anchor | pending | replace with actual query |\n"
                "| github_open_source | TBD pushed/updated/released within anchored year or last 12 months | GitHub/package registry | current_date_anchor | pending | record exact query/filter |\n"
                "| official_docs | TBD official docs release notes changelog current | official docs | current_date_anchor | pending | prefer primary source |"
            )
        elif section == "Freshness Assessment":
            body = (
                "| Claim | Source | Freshness Status | Reason | Decision Impact |\n"
                "|---|---|---|---|---|\n"
                "| TBD | TBD | fresh / acceptable / stale / undated / blocked | TBD | verified, provisional, or blocked |"
            )
        elif section == "Scope Boundary":
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
        elif section == "Architecture Decision Lens":
            body = (
                "| Option | Real Pain Solved | Stage Fit / Overengineering Risk | One-Year Technical Debt | Team Scaling Cost | Migration / Rollback Path | Evidence |\n"
                "|---|---|---|---|---|---|---|\n"
                "| TBD | TBD | TBD | TBD | TBD | TBD | link to `01-reality-research.md` or `research_ledger.json` |"
            )
        elif section == "Frontend Architecture Decisions":
            body = (
                "| Decision Area | Options To Research | Chosen Direction | Why It Fits | Validation Evidence |\n"
                "|---|---|---|---|---|\n"
                "| rendering | CSR / SSR / SSG / ISR / RSC / native shell | TBD | match SEO, interactivity, latency, and hosting constraints | Core Web Vitals, route snapshot, bundle or render check |\n"
                "| state ownership | server state / client global / URL / local UI | TBD | avoid duplicate sources of truth and unnecessary re-rendering | state transition test or UI regression |\n"
                "| interaction and motion | CSS transitions / animation library / timeline engine / none | TBD | motion serves task feedback, navigation, or storytelling | screenshot/manual motion review and reduced-motion rule |\n"
                "| component and design system | existing library / headless primitives / custom | TBD | fit brand, accessibility, and maintenance needs | a11y and visual contract checks |"
            )
        elif section == "Backend Architecture Decisions":
            body = (
                "| Decision Area | Options To Research | Chosen Direction | Why It Fits | Validation Evidence |\n"
                "|---|---|---|---|---|\n"
                "| deployment shape | modular monolith / services / serverless / edge / workers | TBD | fit team size, latency, operations, and coupling | build/deploy command or architecture test |\n"
                "| domain boundaries | CRUD modules / DDD bounded contexts / plugin modules | TBD | match business complexity without ceremony | module boundary check |\n"
                "| API style | REST / GraphQL / tRPC/RPC / gRPC / event API | TBD | fit clients, caching, type safety, and service calls | contract test |\n"
                "| async and workflow | direct call / queue / scheduler / workflow engine / event stream | TBD | fit retries, idempotency, throughput, and observability | job or workflow test |\n"
                "| caching | HTTP/CDN / app cache / data cache / no cache | TBD | fit read patterns and invalidation complexity | cache invalidation test |"
            )
        elif section == "Data Architecture Decisions":
            body = (
                "| Decision Area | Options To Research | Chosen Direction | Why It Fits | Validation Evidence |\n"
                "|---|---|---|---|---|\n"
                "| primary store | relational / document / key-value / graph / object / vector | TBD | fit query shape, consistency, and operations | schema or query test |\n"
                "| schema and migrations | additive migrations / destructive migration / generated schema | TBD | preserve data and rollback ability | migration command |\n"
                "| indexes and query paths | B-tree / full-text / vector / compound / partial / none | TBD | match top queries and expected scale | query plan or benchmark |\n"
                "| transactions and consistency | strong / eventual / optimistic / idempotent | TBD | fit user-visible correctness and side effects | concurrency or idempotency test |\n"
                "| retention and privacy | TTL / soft delete / hard delete / audit archive | TBD | fit compliance and user trust | retention test or audit checklist |"
            )
        elif section == "Algorithm And Data Structure Decisions":
            body = (
                "| Capability | Options To Research | Trigger To Use | Chosen Direction | Validation Evidence |\n"
                "|---|---|---|---|---|\n"
                "| search | keyword / full-text / vector / hybrid / external engine | user searches or retrieves semantic content | TBD | relevance fixture or benchmark |\n"
                "| ranking/recommendation | rules / scoring / embedding similarity / learning-to-rank | ordered results affect product value | TBD | golden ranking cases |\n"
                "| rate limiting | fixed window / sliding window / token bucket / quota ledger | abuse, cost, or fairness matters | TBD | limit and burst tests |\n"
                "| scheduling/queues | FIFO / priority queue / delay queue / workflow DAG | background work has dependencies or retries | TBD | retry/idempotency tests |\n"
                "| graph/relationship | adjacency list / closure table / graph DB / derived edges | permissions, social graph, hierarchy, or dependency graph matters | TBD | traversal and permission cases |"
            )
        elif section == "Agent Session Plan":
            body = (
                "| Task | Role | Context / Files To Read | Task Prompt | Constraints | Output Format | Validation Evidence |\n"
                "|---|---|---|---|---|---|---|\n"
                "| T-001 | coding agent | TBD | TBD | follow contracts and scope boundary | diff plus notes | command or manual evidence |\n\n"
                "Use one session per module or task slice when context may drift. Each session should start by reading the listed docs and files instead of relying on previous chat memory."
            )
        elif section == "Design And Visual Implementation Phase":
            body = (
                "- If `08-ui-visual-design.md` exists, UI tasks must cite it before implementation.\n"
                "- If repo-level design governance is needed, create or refresh `DESIGN.md` with `$design` first.\n"
                "- If pixel/reference matching is required, hand off to `$visual-ralph` after reference approval."
            )
        elif section == "Living Spec Update Protocol":
            body = (
                "- If implementation changes behavior, API, schema, permissions, generated artifacts, security boundaries, visual contract, or validation evidence, update upstream specs before marking the task complete.\n"
                "- Update traceability when requirements, tasks, or evals change.\n"
                "- Record intentional divergence in handoff notes with owner, reason, risk, and follow-up validation."
            )
        elif section == "Launch Handoff":
            body = (
                "| Area | Required Evidence | Status |\n"
                "|---|---|---|\n"
                "| auth/security | permissions, secrets, destructive-action gates, audit notes | TBD |\n"
                "| performance | budget, Core Web Vitals or API latency target where relevant | TBD |\n"
                "| monitoring/logging | errors, traces, metrics, correlation IDs, privacy-safe logs | TBD |\n"
                "| CI/CD | test/build/deploy command and preview/prod separation | TBD |\n"
                "| rollback | migration rollback or feature flag plan | TBD |"
            )
        elif section == "Launch Readiness Checks":
            body = (
                "| Area | Check | Evidence |\n"
                "|---|---|---|\n"
                "| auth/security | access boundaries and secret handling verified | command or manual audit |\n"
                "| performance | performance budget or Core Web Vitals target verified where relevant | command, report, or manual note |\n"
                "| monitoring | errors/logs/metrics defined and privacy-safe | config or code reference |\n"
                "| CI/CD | validation runs in CI or documented release command | CI link or command |\n"
                "| rollback | rollback path exists for schema/config/deploy changes | runbook or migration note |"
            )
        elif section == "Cache And Consistency Contract":
            body = (
                "| Cached Thing | Source Of Truth | Cache Layer | Invalidation Rule | Staleness Budget | Failure Behavior |\n"
                "|---|---|---|---|---|---|\n"
                "| TBD | TBD | HTTP/CDN/app/data/client | TBD | TBD | bypass, refresh, or fail closed |"
            )
        elif section == "Data Access And Index Contract":
            body = (
                "| Query / Access Path | Owner | Expected Cardinality | Index / Search Structure | Permission Filter | Validation |\n"
                "|---|---|---|---|---|---|\n"
                "| TBD | TBD | TBD | TBD | TBD | query plan, benchmark, or contract test |"
            )
        elif section == "Architecture Fitness Checks":
            body = (
                "| Architecture Area | Check | Command Or Evidence |\n"
                "|---|---|---|\n"
                "| frontend rendering/state | route renders intended screen, state ownership is not duplicated | screenshot, state test, or render metric |\n"
                "| backend/API/workflow | API contracts, idempotency, queues, and retries behave as specified | contract or integration test |\n"
                "| data/index/consistency | schema, migrations, indexes, permissions, and cache invalidation hold | migration, query plan, or data test |\n"
                "| algorithm/search/ranking | ranking, search, rate limit, graph, or scheduler behavior matches cases | golden cases or benchmark |"
            )
        elif section == "Architecture Workstream Prompt Packets":
            body = (
                "| Workstream | Agent Role | Required Context | Prompt Focus | Required Evidence |\n"
                "|---|---|---|---|---|\n"
                "| frontend | frontend engineer | 04 frontend decisions, 08 visual contract, relevant routes/components | implement rendering/state/motion without changing backend contracts | screenshot, a11y, render/state test |\n"
                "| backend | backend engineer | 04 backend decisions, 05 API/tool contracts | implement API/workflow boundaries and side-effect rules | contract/integration tests |\n"
                "| data | data engineer | 04 data decisions, 05 data/index/cache contracts | implement schema, migrations, indexes, retention, permissions | migration/query/permission checks |\n"
                "| algorithm | algorithm engineer | 04 algorithm decisions, 06 golden cases | implement search/ranking/rate limit/scheduler/graph behavior | golden cases or benchmark |"
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
            "Architecture decisions must answer real pain solved, stage fit, one-year debt, team scaling cost, and rollback path.",
            "Agent execution tasks should include prompt packets with role, context, task, constraints, output format, and validation evidence.",
            "Implementation changes to behavior, API, schema, permissions, security, visual contract, or eval evidence must update upstream specs before completion.",
            "Frontend architecture decisions must cover rendering, state ownership, motion, component system, and validation evidence when UI exists.",
            "Backend architecture decisions must cover deployment shape, domain boundaries, API style, async/workflow, caching, and validation evidence when backend exists.",
            "Data architecture decisions must cover store choice, schema/migrations, indexes/query paths, transactions/consistency, retention/privacy, and validation evidence when data exists.",
            "Algorithm and data-structure decisions must be explicit when the product needs search, ranking, rate limiting, scheduling, queues, graph traversal, matching, recommendation, or retrieval.",
        ],
        "optional_documents": ["08-ui-visual-design.md"] if include_visual else [],
    }


def initial_research_ledger(idea: str) -> dict[str, Any]:
    """Create an empty research ledger with required categories."""
    anchor = current_date_anchor()
    return {
        "schema": "specforge-research-ledger-v1",
        "product": idea,
        "generated_at": now_iso(),
        "status": "pending-live-research",
        "web_research_capability": "pending-check",
        "current_date_anchor": anchor,
        "freshness_policy": freshness_policy(),
        "query_log": [],
        "freshness_summary": {
            "fresh": 0,
            "acceptable": 0,
            "stale": 0,
            "undated": 0,
            "blocked": 0,
        },
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
            "architecture_decision_sources": [],
            "production_readiness": [],
            "domain_architecture": [],
        },
        "source_fields": [
            "title",
            "url",
            "publisher",
            "published_or_updated",
            "accessed_at",
            "claim_supported",
            "confidence",
            "freshness_status",
            "freshness_reason",
            "retrieval_method",
            "query_used",
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
    sdd_mode: str,
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
        "sdd_mode": sdd_mode,
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
            "launch-ready": "Requires build-ready plus security, performance, monitoring, CI/CD, environment, and rollback evidence.",
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
        "living_spec_rule": "When implementation changes behavior, API, schema, permissions, security, visual contract, or eval evidence, update upstream specs and traceability before marking the task done.",
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
    sdd_mode: str = "auto",
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
            sdd_mode=sdd_mode,
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
    parser.add_argument(
        "--sdd-mode",
        choices=["auto", "vibe-prototype", "spec-lite", "full-sdd", "production-hardening"],
        default="auto",
        help="Desired SDD depth. Default: auto.",
    )
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
        sdd_mode=args.sdd_mode,
    )
    print(f"Created SpecForge {args.stage} document pack at {out.resolve()}")
    print(STAGE_NEXT_ACTION[args.stage])
    if args.include_visual:
        print("Included optional 08-ui-visual-design.md. Use it as the agent visual contract; use DESIGN.md or Visual Ralph for deeper design governance or pixel matching.")
    if args.single_pass:
        print("Single-pass mode recorded in handoff_manifest.json.gates_skipped.")


if __name__ == "__main__":
    main()
