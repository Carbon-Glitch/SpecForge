---
name: specforge-skill
activation: /specforge
description: >-
  Generate a research-grounded Spec-Driven Development document pack for AI vibe coding from a simple product idea. Use for SDD, PRD, requirements, technical design, market research, GitHub open-source stack research, evals, AGENTS.md guidance, task breakdowns, Cursor, Codex, Claude Code, Antigravity, and other coding agents. Strongly emphasizes live web search, real market evidence, current official docs, and up-to-date GitHub technology choices before development.
license: MIT
metadata:
  author: Codex
  version: 1.8.0
  created: 2026-06-28
  last_reviewed: 2026-07-06
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
/specforge --scope user-app-only --exclude factory,admin 为咒语学院生成用户端开发包
```

## Operating Modes

- **Greenfield Mode** — use when the user is creating a new product from a concept.
- **Feature Mode** — use when the user is adding, changing, refactoring, or integrating functionality in an existing codebase.
- **Docs-First Mode** — use when an existing repository already contains product docs, design docs, plans, or domain markdown that should be indexed before writing a new pack.
- **Scope Slice Mode** — use when only part of a product should be owned by this pack, such as `user-app-only`, while other subsystems are referenced or deferred.

In Feature Mode, inspect the repository before writing specs when a path is available. Treat current code, tests, docs, API schemas, data models, routes, and deployment constraints as evidence. Do not redesign the product from scratch unless the user asks.

In Docs-First Mode, scan existing markdown docs before writing Gate 1. Put path plus one-line responsibility into `00-product-brief.md#Existing System Context`. Separate **Prescriptive Inputs** from **This Pack Owns** so the new pack does not drift away from existing source docs.

## Final Pack

The completed pack contains one preflight gate document plus eight core development documents in `sdd-docs/`.

Preflight:

- `preflight-idea-pressure-test.md` — product idea pressure test, core assumption, fatal flaws, real alternatives, first users, 2-week validation test, and continue/pivot/pause decision

Core development documents:

1. `00-product-brief.md` — mode, SDD depth, brainstorm summary, concept or change brief, users, jobs, constraints, assumptions, and open questions
2. `01-reality-research.md` — live market, existing-system reality, official-doc, and GitHub open-source research with citations
3. `02-prd-behavior-contract.md` — product PRD plus behavior contract, scope, anti-goals, guardrails, and success metrics
4. `03-sdd-requirements-spec.md` — testable functional/non-functional requirements, user stories, and EARS acceptance criteria
5. `04-technical-design.md` — architecture, stack decision, architecture decision lens, frontend/backend/data/algorithm decision matrices, module boundaries, data flow, state truth model, workflow/action contract, generated artifact plan, failure handling, observability
6. `05-contracts-data-permissions.md` — API/data/tool schemas, access and permission rules, cache consistency, data access/index contracts, state and storage contracts, module/file responsibility contracts, model context, migration, integration contracts
7. `06-eval-and-test-cases.md` — eval criteria, deterministic judge contract, architecture fitness checks, evidence matrix, data sufficiency check, reference cases, bad cases, regression cases, edge cases, launch readiness checks
8. `07-agent-execution-plan.md` — agent-facing implementation plan, prompt packets, architecture workstream packets, source-vs-generated rules, task order, validation commands, living-spec update protocol, AGENTS.md content, handoff rules

Also generate these support artifacts when useful:

- `traceability_matrix.json` — requirement to design to task to eval coverage
- `research_ledger.json` — sources searched, source dates, URLs, claims, and confidence
- `handoff_manifest.json` — file list, confidence, unresolved questions, and next action
- optional `AGENTS.md` and `tasks.md` exports derived from `07-agent-execution-plan.md`

Optional visual layer:

- `08-ui-visual-design.md` — visual design contract for UI-heavy products: design positioning, tokens, core components, page skeletons, motion rules, responsive/accessibility checks, UI judge, and MVP visual non-goals

Generate `08-ui-visual-design.md` for consumer products, games, mobile apps, dashboards, landing pages, visual tools, and any product where default component-library styling would be unacceptable. Skip it for pure API/backend/CLI packs unless the user asks.

If pixel-level fidelity is required, run `$design` first to create or refresh repo-local `DESIGN.md`, then use `$visual-ralph` after the visual reference is approved. `08-ui-visual-design.md` is an agent contract, not a screenshot-matching loop.

## Non-Negotiable Research Gate

Do not generate technical recommendations from model memory alone.

Before writing `01-reality-research.md`, perform live web research unless the user explicitly says offline-only. If web access is unavailable, write `research_status: blocked` and mark all current-world claims as unverified.

Mandatory research passes:

1. **Market reality search** — current competitors, user behavior, pricing, distribution, product patterns, failure modes.
2. **Official documentation search** — current platform/API/framework docs for the proposed stack.
3. **GitHub open-source search** — current repositories, activity, stars are not enough; inspect recency, releases, issues, docs, license, API fit, and maintenance. Treat GitHub as an engineering asset library: if a framework, module, workflow engine, UI component, agent runtime, evaluation harness, backend service, or reference app already exists and is suitable, prefer integrating, wrapping, forking, or modifying it over building from scratch.
4. **Risk and compliance search** — privacy, safety, permissions, AI policy, data retention, domain-specific constraints.
5. **Implementation prior art search** — current examples, templates, reference architectures, and known traps.
6. **Architecture decision evidence search** — current evidence for the chosen pattern's fit, operational cost, migration path, and team-scaling burden.
7. **Launch readiness search** — current host/platform guidance for auth, security, performance, monitoring, CI/CD, environment separation, and rollback.
8. **Domain architecture search** — current official docs, GitHub projects, package docs, benchmarks, security guidance, and production examples for frontend rendering/state/motion, backend API/workflow/cache, data store/index/transaction/retention, and algorithm/search/ranking/rate-limit/scheduler/graph decisions.

Prefer primary sources: official docs, repository README/releases/issues, standards, papers, regulatory pages, vendor docs. Use blogs and social posts only as weak supporting evidence.

Every material market or technology claim must have a source or be labeled as inference. Research must survive into decisions: `04-technical-design.md#Architecture Decision Lens` must cite `01-reality-research.md` or `research_ledger.json` for each major choice.

See `references/research-protocol.md` for the detailed source scoring rubric.

## Domain Architecture Decision Gate

Do not let a code agent improvise frontend state, rendering, backend boundaries, database schema, indexes, cache invalidation, queues, or algorithms while coding.

In Gate 2, `04-technical-design.md` must include decision matrices for relevant workstreams:

| Workstream | Required Decisions |
|---|---|
| Frontend | rendering strategy, state ownership, interaction/motion, component/design-system approach, performance and accessibility evidence |
| Backend | deployment shape, domain boundaries, API style, async/workflow strategy, caching and invalidation |
| Data | primary store, schema and migrations, indexes/query paths, transactions/consistency, retention and privacy |
| Algorithm/Data Structure | search, ranking/recommendation, rate limiting, scheduling/queues, graph/relationship traversal, matching/retrieval when relevant |

Each decision must state options researched, chosen direction, why it fits this product, rejected alternatives, validation evidence, and source links. Use current official docs and GitHub/package evidence. Static recommendations from an article, model memory, or a previous project are examples to investigate, not defaults to copy.

In Gate 3, connect these choices to:

- `05#Cache And Consistency Contract`
- `05#Data Access And Index Contract`
- `06#Architecture Fitness Checks`
- `07#Architecture Workstream Prompt Packets`

If a product has no UI/backend/data/algorithm surface, mark that workstream `not_applicable` with reason.

## SDD Mode Decision

Choose the lightest mode that protects the work. Record the decision in Gate 0 and `00-product-brief.md`.

| Mode | Use When | Required Depth |
|---|---|---|
| `vibe-prototype` | disposable demo, learning spike, or throwaway exploration | Gate 0/1 light; never claim `build-ready` |
| `spec-lite` | small feature, narrow MVP slice, or low-risk internal flow | Gate 1 plus focused Gate 2/3 contracts |
| `full-sdd` | production-intended product, broad feature, shared codebase, or real money/privacy/users | all gates, traceability, evals, contracts |
| `production-hardening` | existing app is nearing launch or reliability/security matters | full-sdd plus launch readiness evidence |

Upgrade the mode when any signal appears: context drift, recurring regressions, team expansion, production intent, private data, payments, public launch, or fear that a feature change may break unknown behavior. Do not force full SDD for every sketch; the goal is enough specification to reduce risk, not ceremony.

## Gate 0 — Idea Pressure Test

Run this before Gate 1 for greenfield commercial products, SaaS, consumer apps, AI agents, creator tools, marketplaces, and any idea where the user may be about to build before validating demand. Use a lighter version for Feature Mode or skip it only when the user is implementing a mandated requirement, internal tool, learning demo, or already validated scope.

The goal is not to be harsh for theater. The goal is to prevent beautiful specs for products that should not be built yet.

Create `preflight-idea-pressure-test.md` and stop for user confirmation before writing the product brief or reality research.

Evaluate:

1. **Verdict** — `continue`, `pivot`, `research-needed`, or `pause`.
2. **Scorecard** — pain intensity, buyer/user clarity, urgency, differentiation, speed to validate, founder or team advantage.
3. **Core assumption** — the single riskiest assumption that must be true.
4. **Fatal flaws** — the top 1-3 reasons this idea fails, each with a fast disconfirming test.
5. **Problem reality** — painkiller vs vitamin, frequency, cost of pain, current workaround.
6. **Current behavior and alternatives** — direct competitors, indirect competitors, spreadsheets, agencies, manual workflows, habit, or status quo.
7. **First 10 users** — where to find real early users manually before paid acquisition or automation.
8. **Two-week MVP test** — the smallest real-user test that proves or kills the core assumption.
9. **Decision** — whether to proceed to Gate 1, adjust the idea first, do more research, or stop.

Use live search when current market or competitor facts matter. Do not invent market size, demand, or competitor claims. Record the pressure-test decision in `research_ledger.json.idea_pressure_test`.

Also record the SDD mode decision. A weak or unvalidated idea may proceed as `vibe-prototype` or `spec-lite`; it should not be promoted to `full-sdd` unless the user accepts the validation risk.

## Discovery Brainstorming Gate

Do this before or during Gate 0. Keep it short and decision-oriented.

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

## Scope Slice Gate

If the user supplies `--scope`, `--exclude`, or natural-language boundaries such as "user app only" or "factory later", create a scope boundary before Gate 1.

`00-product-brief.md#Scope Boundary` must include:

| Area | Status | Rule |
|---|---|---|
| owned subsystem | `in_pack` | This pack specifies and tasks it. |
| dependency/context subsystem | `referenced_only` | Mention contracts only; do not task implementation. |
| deferred subsystem | `future_pack` | Capture assumptions and handoff boundary. |

Put the first rule of generated `AGENTS.md` as: implement only `in_pack` scope unless the user explicitly expands scope.

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

## Readiness Levels

Do not use `build-ready` as a synonym for "the markdown files exist".

Use:

| Status | Meaning |
|---|---|
| `gate-review-required` | A gate has been scaffolded or drafted and needs user confirmation. |
| `spec-complete` | Documents, scope, contracts, traceability, and eval plan are complete enough for engineering review. |
| `build-ready` | `spec-complete` plus seed data or fixtures, at least one runnable validation command, non-empty automated checks, and no unresolved blocker affecting the first implementation slice. |
| `launch-ready` | `build-ready` plus auth/security, performance, monitoring/logging, CI/CD, environment separation, and rollback evidence. |
| `blocked` | A missing decision, source, permission, or dependency prevents reliable implementation. |

Strict validation should reject `build-ready` when `06 Automated Checks` is empty or `07 Validation Commands` has no runnable command and no explicit `manual-only` marking.
Do not mark `launch-ready` until `06 Launch Readiness Checks` and `07 Launch Handoff` cover security, performance, monitoring, CI/CD, preview/prod separation, and rollback.

## Workflow

### 1. Initialize Gate 0

Run the scaffold script when you need local files. By default it creates only the pressure-test preflight:

```bash
python scripts/run_pipeline.py --idea "<product concept>" --out sdd-docs
```

Populate `preflight-idea-pressure-test.md`, then stop. Continue only after the user confirms the decision or asks to proceed with explicit assumptions.

Validate Gate 0 with:

```bash
python scripts/validate_pack.py sdd-docs --stage gate0
```

### 2. Gate 1 — Brief And Reality Research

After Gate 0 is confirmed or explicitly skipped, scaffold Gate 1:

```bash
python scripts/run_pipeline.py --idea "<product concept>" --out sdd-docs --stage gate1
```

Use `--sdd-mode vibe-prototype|spec-lite|full-sdd|production-hardening` when the desired depth is known. Otherwise keep the default `auto` mode and decide in Gate 0.

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

`04-technical-design.md#Architecture Decision Lens` must answer for every major architecture or stack choice:

- what real pain this choice solves
- why it fits the current project stage and is not premature overengineering
- what one-year technical debt it creates
- what happens when the team doubles or multiple agents work in parallel
- how to migrate, replace, or roll back if the choice fails
- which research source supports the decision

Also fill the domain architecture decision matrices. For example, UI-heavy products must decide rendering, state ownership, and motion constraints; backend products must decide API/workflow/cache boundaries; data-heavy products must decide stores, indexes, transactions, and retention; search/recommendation/scheduler products must decide algorithms and validation cases.

Validate Gate 2 with:

```bash
python scripts/validate_pack.py sdd-docs --stage gate2
```

### 3.5. Optional Visual Contract

For UI-heavy products, scaffold the optional visual contract after Gate 2:

```bash
python scripts/run_pipeline.py --idea "<product concept>" --out sdd-docs --stage gate2 --include-visual
```

Then write `08-ui-visual-design.md`. It must define:

1. design source of truth: `08` only, `DESIGN.md`, or `DESIGN.md + 08`
2. design positioning and visual personality
3. tokens: color, typography, spacing, radius, elevation, motion
4. 3-5 core components with states
5. page/screen skeletons with minimum responsive constraints
6. UI judge entries: `screenshot_manual`, `a11y_contrast`, `route_snapshot`, or explicit manual-only reason
7. MVP visual non-goals

If `$design` exists in the host, use it when the repository needs durable design governance in `DESIGN.md`. If `$visual-ralph` exists and pixel/reference matching is required, use it after the user approves the visual reference. SpecForge should hand off the visual contract; it should not pretend to run a pixel-diff loop inside the spec pack.

### 4. Gate 3 — Contracts, Evals, And Agent Plan

After Gate 2 is confirmed, scaffold the final stage:

```bash
python scripts/run_pipeline.py --idea "<product concept>" --out sdd-docs --stage gate3
```

Then write:

1. `05-contracts-data-permissions.md`
2. `06-eval-and-test-cases.md`
3. `07-agent-execution-plan.md`

Do not let later docs invent requirements not traceable to earlier docs. If a new idea appears, update upstream docs and traceability.

Before starting `07-agent-execution-plan.md`, verify that documents `04`, `05`, and `06` contain the executable contracts gate above. Implementation tasks must reference these contracts, not re-infer state, navigation, module ownership, generated files, or eval evidence.

`05-contracts-data-permissions.md` must include cache/consistency and data access/index contracts when the product uses caching, databases, search, queues, or external state.

Reference, bad, and regression cases must declare provenance: `user-confirmed`, `real-source-derived`, `existing-test-derived`, or `synthetic`. A build-ready pack must include at least one non-synthetic reference case; do not rely only on cases made by the same model that writes the eval.

For UI products, `06-eval-and-test-cases.md#UI Judge` must include at least one of:

- `screenshot_manual` — named route, viewport, state, expected visual evidence, reviewer rule
- `a11y_contrast` — token pair, minimum contrast threshold, check command or manual rule
- `route_snapshot` — route, viewport, screenshot command, and non-overlap/no-overflow assertions

`06-eval-and-test-cases.md#Launch Readiness Checks` must cover auth/security, performance, monitoring/logging, CI/CD, environment separation, and rollback when the pack targets production or `production-hardening`.

`06-eval-and-test-cases.md#Architecture Fitness Checks` must include evidence for selected frontend, backend, data, and algorithm decisions: screenshot/render metrics, contract tests, migration/query/index tests, cache invalidation tests, golden ranking/search cases, rate-limit burst tests, queue retry/idempotency tests, or graph permission traversal cases.

`07-agent-execution-plan.md#Agent Session Plan` must provide prompt packets for implementation slices:

| Field | Requirement |
|---|---|
| role | the agent stance needed for the task |
| context/files to read | exact docs and source files to load first |
| task | one concrete change or module slice |
| constraints | scope, contracts, forbidden changes, compatibility rules |
| output format | expected diff, files, report, or artifact |
| validation evidence | command, screenshot, API/state/file evidence, or manual review |

Use one session per module or task slice when context may drift. Do not ask a code agent to carry the whole product in one chat if the work naturally splits.

`07-agent-execution-plan.md#Architecture Workstream Prompt Packets` must split frontend, backend, data, and algorithm tasks when those surfaces exist, so each agent session starts from the relevant contracts and validation evidence.

`07-agent-execution-plan.md#Living Spec Update Protocol` must state: if implementation changes behavior, API, schema, permissions, generated artifacts, security boundaries, visual contract, or validation evidence, update upstream specs and traceability before marking the task complete.

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
- whether the handoff is `spec-complete`, `build-ready`, `blocked`, or `gate-review-required`

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
- for UI products, include visual acceptance checks rather than subjective beauty claims

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

For every major technical choice, include the chosen option, current official source, GitHub/package health when open source, reuse strategy, fit rationale, rejected alternatives, operational risks, and migration/fallback path. Use `references/research-protocol.md` for the full evidence rubric.

## Open-Source Reuse Rule

Before proposing custom implementation for any non-trivial subsystem, search GitHub and package registries for reusable assets.

Always research reuse for app scaffolds, auth, dashboards/admin panels, workflow engines, queues, agent runtimes, RAG/search/vector pipelines, eval harnesses, UI components, realtime, notifications, files, media, payments, and analytics when relevant. Evaluate fit, integration surface, license, maintenance health, dependency/security risk, docs/tests, and fork burden.

Do not default to "build from scratch" unless the research shows that reuse is unsuitable, riskier, or more expensive than implementation.

## Agent Compatibility

For Codex, Claude Code, and tools that read `AGENTS.md`, export the agent execution rules from `07-agent-execution-plan.md` into a project `AGENTS.md`.

For Cursor, also create `.cursor/rules/sdd-docs.mdc` or install this skill under `.cursor/skills/`.

For Antigravity, install this skill under `.agent/skills/` and include the generated `AGENTS.md` in the project root.

See `references/platform-adapters.md`.

## Orchestration With Sister Skills

Use this lightweight orchestration map when the host has these skills:

| Stage | Tooling |
|---|---|
| Idea pressure test | SpecForge Gate 0 |
| Behavior and engineering specs | SpecForge Gate 1-3 |
| Durable design source of truth | `$design` creates or refreshes repo-local `DESIGN.md` |
| Visual implementation against reference | `$visual-ralph` after approved reference/baseline |
| Coding handoff | `07-agent-execution-plan.md` plus generated `AGENTS.md` |

Do not force sister skills when unavailable. Record the missing capability and keep the SpecForge pack self-contained.

## When To Stop

Stop only when:

- all eight core docs exist
- optional `08-ui-visual-design.md` exists for UI-heavy products or the reason for omission is explicit
- current-world research is complete or explicitly marked blocked
- each requirement traces to a task and eval
- every task has a verification command or manual evidence requirement
- handoff readiness is not overstated beyond the evidence in `06` and `07`
- unresolved questions are listed with impact

Do not stop after only PRD/spec/tasks unless the user explicitly requests a lightweight draft.
