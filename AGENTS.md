# SpecForge

This directory is an installable cross-platform agent skill. Use it when a user wants to turn a rough product concept into a research-grounded Spec-Driven Development document pack for AI vibe coding.

Primary invocation:

```text
/specforge <product idea or rough requirements>
```

Begin with a concise discovery brainstorming gate: restate intent, classify `greenfield` vs `feature`, ask only material questions, offer options when useful, and state assumptions.

Choose SDD depth explicitly: `vibe-prototype`, `spec-lite`, `full-sdd`, or `production-hardening`. Upgrade depth when there is context drift, recurring regression, team expansion, production intent, private data, payments, or fear of unknown side effects.

For greenfield commercial products, run `preflight-idea-pressure-test.md` before Gate 1. Decide `continue`, `pivot`, `research-needed`, or `pause` from the core assumption, fatal flaws, current alternatives, first users, and 2-week MVP test. Use a lighter version for feature work or mandated internal tools.

The skill generates one preflight decision document plus eight AI-readable core documents:

0. `preflight-idea-pressure-test.md`
1. `00-product-brief.md`
2. `01-reality-research.md`
3. `02-prd-behavior-contract.md`
4. `03-sdd-requirements-spec.md`
5. `04-technical-design.md`
6. `05-contracts-data-permissions.md`
7. `06-eval-and-test-cases.md`
8. `07-agent-execution-plan.md`

Optional UI-heavy packs may also include `08-ui-visual-design.md`. Treat it as the visual contract for tokens, components, page skeletons, motion, responsive/a11y checks, and UI judge rules. If repo-level design governance is needed, run `$design` to create or refresh `DESIGN.md`; if pixel/reference matching is needed, hand off to `$visual-ralph` after reference approval.

Key operating rule: perform live web research before market claims, technology choices, API choices, compliance claims, or open-source recommendations. If live research is unavailable, label those claims unverified.

Research must feed decisions. For every major architecture or stack choice, `04-technical-design.md#Architecture Decision Lens` must cite `01-reality-research.md` or `research_ledger.json` and answer: real pain solved, stage fit, one-year technical debt, team scaling cost, and migration or rollback path.

Domain-architecture rule: when the product has UI, backend, data, or algorithmic behavior, `04-technical-design.md` must include relevant decision matrices for frontend rendering/state/motion, backend deployment/API/workflow/cache, data stores/migrations/indexes/consistency/retention, and algorithms/search/ranking/rate-limit/scheduling/graph logic. These choices require live official-doc and GitHub/package research; article examples and model memory are only leads.

Feature-mode rule: when the request targets an existing project, inspect current code, tests, docs, schemas, routes, data, and deployment constraints before writing specs. Preserve compatibility unless the user asks for redesign.

Docs-first rule: when the repository already contains product/domain/design markdown, index those docs before Gate 1. Put path plus one-line responsibility in `00-product-brief.md#Existing System Context`, then separate `Prescriptive Inputs` from `This Pack Owns`.

Scope-slice rule: if the user supplies `--scope` or `--exclude`, put `in_pack`, `referenced_only`, and `future_pack` boundaries in `00-product-brief.md#Scope Boundary` and generated `AGENTS.md`. Implement only `in_pack` scope.

Executable-contract operating rule: before implementation tasks, require contracts for state truth, workflow/navigation/actions, deterministic judging, module/file boundaries, generated artifacts, and data sufficiency. Tasks should reference those contracts and include concrete validation commands or evidence requirements.

Data/cache operating rule: when caching, databases, search, queues, or external state exist, `05-contracts-data-permissions.md` must define cache invalidation, staleness budget, data access paths, indexes/search structures, permission filters, and migration/rollback constraints.

Agent-session rule: `07-agent-execution-plan.md` must include prompt packets for implementation slices: role, context/files to read, task, constraints, output format, and validation evidence. Use one session per module or task slice when context may drift.

Workstream rule: split frontend, backend, data, and algorithm prompt packets when those surfaces exist. Each workstream must start from the relevant contracts and end with its own evidence: screenshot/render/a11y, API/contract/workflow, migration/query/index/cache, or golden search/ranking/rate-limit/graph cases.

Living-spec rule: if implementation changes behavior, API, schema, permissions, generated artifacts, security boundaries, visual contract, or validation evidence, update upstream specs and traceability before marking the task complete.

Stage-gate rule: do not fill the full pack in one pass unless the user explicitly asks to skip review. Complete the pressure test and stop for confirmation, then complete `00-product-brief.md` and `01-reality-research.md`, stop for confirmation, then complete PRD/requirements/technical design, stop again, then complete contracts/evals/agent plan.

Eval provenance rule: reference, bad, and regression cases must declare `user-confirmed`, `real-source-derived`, `existing-test-derived`, or `synthetic`. A build-ready pack cannot rely only on synthetic cases.

Readiness rule: `spec-complete` means the docs and traceability are reviewable. `build-ready` requires non-empty automated checks, at least one runnable validation command or explicit `manual-only`, seed/fixture coverage for the first implementation slice, and no blocker. `launch-ready` additionally requires security, performance, monitoring/logging, CI/CD, environment separation, and rollback evidence.

Use `SKILL.md` for the full workflow. Use `references/research-protocol.md` for the source-scoring rules and `references/output-docs.md` for the exact content contract.

Useful commands:

```bash
python scripts/run_pipeline.py --idea "<product idea>" --out sdd-docs
python scripts/validate_pack.py sdd-docs --stage gate0
python scripts/run_pipeline.py --idea "<product idea>" --out sdd-docs --stage gate1
python scripts/validate_pack.py sdd-docs --stage gate1
python scripts/run_pipeline.py --idea "<product idea>" --out sdd-docs --stage gate2 --include-visual
python scripts/run_evals.py --validate
```
