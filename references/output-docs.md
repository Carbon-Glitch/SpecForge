# SpecForge Document Contract

The pack is designed for AI coding agents. It should be precise, traceable, and executable.

## preflight-idea-pressure-test.md

Purpose: decide whether a greenfield idea should proceed into formal SDD.

Must include:

- verdict: `continue`, `pivot`, `research-needed`, or `pause`
- scorecard
- core assumption
- fatal flaws with fast tests
- problem reality
- current behavior and alternatives
- first 10 users
- two-week MVP test
- decision and evidence to verify

## 00-product-brief.md

Purpose: turn the user's rough idea into a clear working brief.

Must include:

- mode: `greenfield` or `feature`
- brainstorming summary
- one-sentence product concept
- existing system context when adding to a codebase
- scope boundary: `in_pack`, `referenced_only`, and `future_pack`
- prescriptive inputs
- this pack owns
- target users
- jobs-to-be-done
- primary workflows
- constraints
- assumptions
- success criteria with IDs, for example `SC-001`
- open questions grouped by blocking vs non-blocking

Use this document to record clarification answers. If the user does not answer, choose conservative defaults and label them.

## 01-reality-research.md

Purpose: align the product and technology plan with the real world.

Must include:

- research status
- market reality
- competitor table
- current user behavior evidence
- existing system reality when a codebase is provided
- current official documentation findings
- current GitHub/open-source findings
- open-source reuse/fork/integration decision table by subsystem
- risk and compliance findings
- implementation prior art
- rejected options
- sources

This document must be written before stack decisions are finalized.

## 02-prd-behavior-contract.md

Purpose: define why the product exists and how it should behave.

Must include:

- problem statement
- goals and measurable success metrics
- personas
- scope and anti-goals
- core user journeys
- compatibility contract for existing behavior when in Feature Mode
- behavior contract
- guardrails
- failure behavior
- release criteria

For AI products, focus on behavior and failure modes, not only feature lists.

## 03-sdd-requirements-spec.md

Purpose: define testable requirements.

Must include:

- functional requirements with stable IDs
- non-functional requirements
- user stories
- EARS acceptance criteria
- regression requirements for existing behavior when in Feature Mode
- edge cases
- out-of-scope items

Every requirement should be testable and traceable.

## 04-technical-design.md

Purpose: turn product requirements into architecture.

Must include:

- architecture overview
- stack decision with source-backed rationale
- open-source reuse plan: what to integrate, fork, wrap, extract, or build from scratch
- integration plan for existing modules, APIs, routes, data, jobs, and tests when in Feature Mode
- module boundaries
- data flow
- state truth model: persisted state, runtime-only state, derived state, source of truth, snapshot/diff/reset behavior, migrations, and sensitive state
- workflow navigation action contract: routes, screens, dialogs, tabs, commands, transitions, side effects, invalid transitions, and future test selectors or route declarations
- generated artifact plan: source declarations, generated outputs, generator commands, regeneration triggers, and no-hand-edit rules
- failure handling
- observability
- performance and cost notes
- migration and rollback plan

Do not make technology choices before `01-reality-research.md` is filled.

## 05-contracts-data-permissions.md

Purpose: define the interfaces the code agent should not improvise.

Must include:

- API contracts
- data model
- state model contract
- tool contracts
- access and permission rules
- module file responsibility contract: each module/file role, allowed content, forbidden content, ownership, dependency direction, and public interface
- security boundaries
- storage and retention rules
- external integrations

For Agent products, include read-only, read-write, and destructive tool tiers.

## 06-eval-and-test-cases.md

Purpose: define what good enough means.

Must include:

- eval philosophy
- launch, target, and aspirational thresholds
- deterministic judge contract: code/state/API/file/screenshot/log/manual evidence for each requirement
- evidence matrix mapping requirement IDs to judge type, command, fixture, expected state, and failure signal
- data sufficiency check for defaults, fixtures, seed scenarios, edge cases, and bad cases
- UI judge when the product has visible UI: `screenshot_manual`, `a11y_contrast`, `route_snapshot`, or explicit manual-only reason
- case source policy: each reference, bad, and regression case must declare `user-confirmed`, `real-source-derived`, `existing-test-derived`, or `synthetic`; build-ready packs must not use only synthetic cases
- reference cases
- bad cases
- regression cases
- edge cases
- automated checks
- manual review checks
- regression gates

Cases can be JSON, CSV, markdown, screenshots, fixtures, API examples, or scenario tables, but they must be concrete.

## 07-agent-execution-plan.md

Purpose: give Cursor/Codex/Claude/Antigravity a direct implementation playbook.

Must include:

- agent operating rules
- implementation phases
- task list with IDs
- dependencies and parallelization
- source-vs-generated rules
- design and visual implementation phase when `08-ui-visual-design.md` exists
- validation commands
- handoff to coding agent
- generated `AGENTS.md` content
- done definition

Tasks should be small enough for a coding agent to execute one by one and must include verification.

## 08-ui-visual-design.md

Purpose: define a visual implementation contract for UI-heavy products.

Must include:

- visual design status
- design source of truth: `08`, `DESIGN.md`, or both
- design positioning
- design tokens
- core components and states
- page skeletons
- interaction and motion
- responsive and accessibility rules
- UI judge contract
- MVP visual non-goals
- design orchestration with `$design` and `$visual-ralph` when available

This document is optional for pure API/backend/CLI products.

## Traceability

Populate `traceability_matrix.json` with mappings like:

```json
{
  "requirement_id": "FR-001",
  "source": "02-prd-behavior-contract.md#Core User Journeys",
  "design_refs": ["04-technical-design.md#Module Boundaries"],
  "contract_refs": ["05-contracts-data-permissions.md#API Contracts"],
  "task_refs": ["07-agent-execution-plan.md#Task List"],
  "eval_refs": ["06-eval-and-test-cases.md#Reference Cases"]
}
```

## Build Readiness Levels

Use these labels in `handoff_manifest.json`:

- `gate-review-required` — a gate has been scaffolded or drafted and needs user confirmation
- `spec-complete` — docs, scope, contracts, traceability, and eval plan are complete enough for engineering review
- `build-ready` — `spec-complete` plus fixtures/seed data, at least one runnable validation command, non-empty automated checks, and no blocker for the first implementation slice
- `blocked` — missing external access or critical unanswered question

## Stage Gates

SpecForge should be reviewed in staged gates:

- `gate0` — complete `preflight-idea-pressure-test.md`, then stop for user confirmation.
- `gate1` — complete `00-product-brief.md` and `01-reality-research.md`, then stop for user confirmation.
- `gate2` — complete `02-prd-behavior-contract.md`, `03-sdd-requirements-spec.md`, and `04-technical-design.md`, then stop for user confirmation.
- optional visual gate — complete `08-ui-visual-design.md` for UI-heavy products after Gate 2.
- `gate3` — complete `05-contracts-data-permissions.md`, `06-eval-and-test-cases.md`, and `07-agent-execution-plan.md`, then validate and hand off.

Do not mark a pack `build-ready` until all gates have either been reviewed or explicitly skipped by the user.
