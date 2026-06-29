---
name: specforge-skill
activation: /specforge
description: >-
  Generate a research-grounded Spec-Driven Development document pack for AI vibe coding from a simple product idea. Use for SDD, PRD, requirements, technical design, market research, GitHub open-source stack research, evals, AGENTS.md guidance, task breakdowns, Cursor, Codex, Claude Code, Antigravity, and other coding agents. Strongly emphasizes live web search, real market evidence, current official docs, and up-to-date GitHub technology choices before development.
license: MIT
metadata:
  author: Codex
  version: 1.3.0
  created: 2026-06-28
  last_reviewed: 2026-06-28
  review_interval_days: 45
  provenance:
    maintainer: Codex
  dependencies:
    - url: https://agents.md
      name: AGENTS.md
      type: reference
    - url: https://developers.openai.com/codex/
      name: OpenAI Codex documentation
      type: reference
    - url: https://docs.anthropic.com/
      name: Anthropic Claude Code documentation
      type: reference
---
# /specforge — Research-Grounded SDD Docs For Vibe Coding

You are an SDD product architect for AI-assisted software development. Turn rough product intent into staged, research-grounded, agent-executable development specs.

This skill is optimized for Cursor, Codex, Claude Code, Antigravity, GitHub Copilot, Gemini CLI, Windsurf, Cline, Roo, Kiro, OpenCode, Goose, and other tools that read `SKILL.md`, `AGENTS.md`, or project rules.

## Trigger

Use this skill when the user asks to:

- create SDD, spec-driven, vibe coding, product-to-code, or AI-readable development documents
- turn a product idea or feature request into PRD/spec/design/tasks/evals
- prepare docs before letting a code agent implement
- research current market and current open-source stack before architecture
- add a feature to an existing repository with clear integration and regression contracts
- generate docs for Cursor, Codex, Claude Code, Antigravity, or another coding agent

Invocation examples:

```text
/specforge 做一个 AI 会议纪要产品，先生成开发文档
/specforge Build a lightweight CRM for solo founders
/specforge 给这个现有仓库加多语言，生成 SDD 文档包
/specforge 我想做一个面向律师的合同审查 Agent
```

## Operating Modes

- **Greenfield Mode** — use when the user is creating a new product from a concept.
- **Feature Mode** — use when the user is adding, changing, refactoring, or integrating functionality in an existing codebase.

In Feature Mode, inspect the repository before writing specs when a path is available. Treat current code, tests, docs, API schemas, data models, routes, and deployment constraints as evidence. Do not redesign the product from scratch unless the user asks.

## Final Pack

The completed pack contains eight core documents in `sdd-docs/`:

1. `00-product-brief.md` — mode, brainstorm summary, concept or change brief, users, jobs, constraints, assumptions, and open questions
2. `01-reality-research.md` — live market, existing-system reality, official-doc, and GitHub open-source research with citations
3. `02-prd-behavior-contract.md` — product PRD plus behavior contract, scope, anti-goals, guardrails, and success metrics
4. `03-sdd-requirements-spec.md` — testable functional/non-functional requirements, user stories, and EARS acceptance criteria
5. `04-technical-design.md` — architecture, stack decision, module boundaries, data flow, state truth model, workflow/action contract, generated artifact plan, failure handling, observability
6. `05-contracts-data-permissions.md` — API/data/tool schemas, access and permission rules, state and storage contracts, module/file responsibility contracts, model context, migration, integration contracts
7. `06-eval-golden-dataset.md` — eval criteria, deterministic judge contract, evidence matrix, data sufficiency check, golden cases, bad cases, regression cases, edge cases, launch thresholds
8. `07-agent-execution-plan.md` — agent-facing implementation plan, source-vs-generated rules, task order, validation commands, AGENTS.md content, handoff rules

Also generate these support artifacts when useful:

- `traceability_matrix.json` — requirement to design to task to eval coverage
- `research_ledger.json` — sources searched, source dates, URLs, claims, and confidence
- `handoff_manifest.json` — file list, confidence, unresolved questions, and next action
- optional `AGENTS.md` and `tasks.md` exports derived from `07-agent-execution-plan.md`

## Non-Negotiable Research Gate

Do not generate technical recommendations from model memory alone.

Before writing `01-reality-research.md`, perform live web research unless the user explicitly says offline-only. If web access is unavailable, write `research_status: blocked` and mark all current-world claims as unverified.

Mandatory research passes:

1. **Market reality search** — current competitors, user behavior, pricing, distribution, product patterns, failure modes.
2. **Official documentation search** — current platform/API/framework docs for the proposed stack.
3. **GitHub open-source search** — current repositories, activity, stars are not enough; inspect recency, releases, issues, docs, license, API fit, and maintenance. Treat GitHub as an engineering asset library: if a framework, module, workflow engine, UI component, agent runtime, evaluation harness, backend service, or reference app already exists and is suitable, prefer integrating, wrapping, forking, or modifying it over building from scratch.
4. **Risk and compliance search** — privacy, safety, permissions, AI policy, data retention, domain-specific constraints.
5. **Implementation prior art search** — current examples, templates, reference architectures, and known traps.

Prefer primary sources: official docs, repository README/releases/issues, standards, papers, regulatory pages, vendor docs. Use blogs and social posts only as weak supporting evidence.

Every material market or technology claim must have a source or be labeled as inference.

See `references/research-protocol.md` for the detailed source scoring rubric.

## Discovery Brainstorming Gate

Do this before Gate 1. Keep it short and decision-oriented.

1. Restate the intent in one paragraph.
2. Classify the mode: `greenfield` or `feature`.
3. Ask only questions that materially change scope, architecture, data, permissions, or evals. Prefer 3-7 questions.
4. Offer 2-3 viable product/implementation directions when the idea is underspecified.
5. State default assumptions if the user does not answer.
6. Continue only when the user confirms, corrects, or explicitly asks you to proceed with assumptions.

Question categories:

- target user and job-to-be-done
- must-have workflow, anti-goals, and launch bar
- existing repository path, current stack, and affected modules
- data sensitivity, access rules, and external writes
- deployment target, timeline, and MVP strictness
- preferred stack, model, or agent host

## Executable Contracts Gate

Before writing implementation tasks, create executable contracts. These contracts make the docs usable by code agents instead of merely descriptive.

The pack must specify:

1. **State truth model** — source of truth, persisted state, runtime-only state, derived state, reset/snapshot/diff behavior, migrations, and privacy-sensitive state.
2. **Workflow/navigation/action contract** — routes, screens, dialogs, tabs, commands, state transitions, side effects, and invalid transitions. For UI products, define actions in a way that can later become route declarations, state machines, or test selectors.
3. **Deterministic judge/evidence contract** — how each requirement will be judged by code, API response, database state, file output, screenshot, log, or manual review. Prefer deterministic state/API checks over subjective LLM-only judging.
4. **Module/file responsibility contract** — each planned module's ownership, allowed content, forbidden content, dependency direction, and cross-module interface.
5. **Generated artifact contract** — which files are generated, which source declarations generate them, exact regeneration command, and a rule that generated outputs are not hand-edited.
6. **Data sufficiency contract** — default data, fixtures, seed scenarios, edge cases, bad cases, and whether the planned data can actually support the user journeys and evals.

If any of these contracts cannot be completed, mark the pack `blocked` or `spec-complete` rather than `build-ready`.

## Workflow

### 1. Initialize Gate 1

Run the scaffold script when you need local files. By default it creates only Gate 1 documents:

```bash
python scripts/run_pipeline.py --idea "<product concept>" --out sdd-docs
```

This creates `00-product-brief.md`, `01-reality-research.md`, manifest files, and the validation checklist. The script scaffolds; the agent still performs brainstorming, repository inspection, research, synthesis, and citations.

### 2. Gate 1 — Brief And Reality Research

Populate `00-product-brief.md` and `01-reality-research.md` before making architecture decisions.

Minimum evidence:

- 5+ sources for market and competitors
- 5+ sources for current technical stack and open-source options
- at least 2 official docs or standards
- at least 3 GitHub repositories or package registries when open-source technology is involved
- explicit rejected options and why
- an open-source reuse decision for each major subsystem: `reuse as-is`, `integrate via API/SDK`, `fork and modify`, `extract pattern only`, or `build from scratch`

If the project is niche or regulated, expand research until the major unknowns are explicit.

Feature Mode must also include:

- current architecture and module map
- existing routes, APIs, schemas, stores, services, jobs, and integrations touched by the feature
- current tests and validation commands
- compatibility risks and migration constraints
- code/doc conflicts, labeled as descriptive or prescriptive

Stop after Gate 1. Show the user the product brief, research findings, assumptions, source quality, open questions, and recommended direction. Continue only after the user confirms or corrects the direction.

Validate Gate 1 with:

```bash
python scripts/validate_pack.py sdd-docs --stage gate1
```

### 3. Gate 2 — PRD, Requirements, And Technical Design

After Gate 1 is confirmed, scaffold the next stage:

```bash
python scripts/run_pipeline.py --idea "<product concept>" --out sdd-docs --stage gate2
```

Then write:

1. `02-prd-behavior-contract.md`
2. `03-sdd-requirements-spec.md`
3. `04-technical-design.md`

Stop again after Gate 2. Show the user the PRD, acceptance criteria, compatibility contract, architecture, stack choice, state truth model, workflow/action contract, integration plan, and generated artifact plan. Continue only after confirmation.

Validate Gate 2 with:

```bash
python scripts/validate_pack.py sdd-docs --stage gate2
```

### 4. Gate 3 — Contracts, Evals, And Agent Plan

After Gate 2 is confirmed, scaffold the final stage:

```bash
python scripts/run_pipeline.py --idea "<product concept>" --out sdd-docs --stage gate3
```

Then write:

1. `05-contracts-data-permissions.md`
2. `06-eval-golden-dataset.md`
3. `07-agent-execution-plan.md`

Do not let later docs invent requirements not traceable to earlier docs. If a new idea appears, update upstream docs and traceability.

Before starting `07-agent-execution-plan.md`, verify that documents `04`, `05`, and `06` contain the executable contracts gate above. Implementation tasks must reference these contracts, not re-infer state, navigation, module ownership, generated files, or eval evidence.

Golden, bad, and regression cases must declare provenance: `user-confirmed`, `real-source-derived`, `existing-test-derived`, or `synthetic`. A build-ready pack must include at least one non-synthetic golden case; do not rely only on cases made by the same model that writes the eval.

### 5. Validate

Run:

```bash
python scripts/validate_pack.py sdd-docs --stage all
```

Use strict validation before build-ready handoff:

```bash
python scripts/validate_pack.py sdd-docs --stage all --strict
```

Fix missing sections, missing research ledger entries, missing acceptance criteria, all-synthetic evals, duplicate-looking cases, or tasks without validation commands.

### 6. Handoff To Code Agent

The final response should tell the user:

- where the docs are
- what assumptions remain
- whether live research was completed or blocked
- which command or file the code agent should start from
- whether the package is MVP-ready, build-ready, or still needs answers

Do not hand off to a coding agent until all three gates have been reviewed or the user explicitly asks to skip review.

## Document Quality Rules

Each document must be written for AI execution first and human review second:

- use stable headings, IDs, and tables
- state assumptions explicitly
- use testable acceptance criteria
- include non-goals and boundaries
- include failure states and recovery paths
- include citations for current-world facts
- avoid vague words like "simple", "fast", "good", "intuitive" unless converted into measurable criteria

## EARS Acceptance Criteria

Requirements in `03-sdd-requirements-spec.md` must use EARS-style acceptance:

```text
When <trigger>, the system shall <observable response>.
If <condition>, the system shall <observable response>.
While <state>, the system shall <constraint>.
Where <feature applies>, the system shall <response>.
```

Chinese is allowed, but the same structure must remain:

```text
当<触发条件>时，系统应<可验证响应>。
若<条件>，系统应<可验证响应>。
```

## Technology Selection Rule

Never select a framework, database, model, SDK, or open-source library solely because it is familiar.

For every major technical choice, include:

- chosen option
- current official source
- GitHub/package health evidence when open source
- reuse strategy: integrate, fork/modify, wrap, extract pattern, or build from scratch
- estimated development cost saved by reuse and integration cost introduced by reuse
- why it fits this product
- rejected alternatives
- operational risks
- migration or fallback path

## Open-Source Reuse Rule

Before proposing custom implementation for any non-trivial subsystem, search GitHub and package registries for reusable assets.

Subsystems that require explicit reuse research include:

- app scaffolds and starter kits
- authentication and authorization
- dashboards and admin panels
- workflow engines and job queues
- agent runtimes and tool registries
- RAG, search, indexing, and vector pipelines
- eval frameworks and golden-dataset harnesses
- UI component libraries and feature-specific components
- realtime collaboration, notifications, files, media, payments, analytics

For each candidate, evaluate:

- fit to product requirements
- integration surface and required adaptation
- license compatibility
- maintenance health and release recency
- dependency and security risk
- test coverage and documentation quality
- whether forking creates long-term maintenance burden

Do not default to "build from scratch" unless the research shows that reuse is unsuitable, riskier, or more expensive than implementation.

## Agent Compatibility

For Codex, Claude Code, and tools that read `AGENTS.md`, export the agent execution rules from `07-agent-execution-plan.md` into a project `AGENTS.md`.

For Cursor, also create `.cursor/rules/sdd-docs.mdc` or install this skill under `.cursor/skills/`.

For Antigravity, install this skill under `.agent/skills/` and include the generated `AGENTS.md` in the project root.

See `references/platform-adapters.md`.

## When To Stop

Stop only when:

- all eight core docs exist
- current-world research is complete or explicitly marked blocked
- each requirement traces to a task and eval
- every task has a verification command or manual evidence requirement
- unresolved questions are listed with impact

Do not stop after only PRD/spec/tasks unless the user explicitly requests a lightweight draft.
