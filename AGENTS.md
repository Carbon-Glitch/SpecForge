# SpecForge

This directory is an installable cross-platform agent skill. Use it when a user wants to turn a rough product concept into a research-grounded Spec-Driven Development document pack for AI vibe coding.

Primary invocation:

```text
/specforge <product idea or rough requirements>
```

Begin with a concise discovery brainstorming gate: restate intent, classify `greenfield` vs `feature`, ask only material questions, offer options when useful, and state assumptions.

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

Key operating rule: perform live web research before market claims, technology choices, API choices, compliance claims, or open-source recommendations. If live research is unavailable, label those claims unverified.

Feature-mode rule: when the request targets an existing project, inspect current code, tests, docs, schemas, routes, data, and deployment constraints before writing specs. Preserve compatibility unless the user asks for redesign.

Executable-contract operating rule: before implementation tasks, require contracts for state truth, workflow/navigation/actions, deterministic judging, module/file boundaries, generated artifacts, and data sufficiency. Tasks should reference those contracts and include concrete validation commands or evidence requirements.

Stage-gate rule: do not fill the full pack in one pass unless the user explicitly asks to skip review. Complete the pressure test and stop for confirmation, then complete `00-product-brief.md` and `01-reality-research.md`, stop for confirmation, then complete PRD/requirements/technical design, stop again, then complete contracts/evals/agent plan.

Eval provenance rule: reference, bad, and regression cases must declare `user-confirmed`, `real-source-derived`, `existing-test-derived`, or `synthetic`. A build-ready pack cannot rely only on synthetic cases.

Use `SKILL.md` for the full workflow. Use `references/research-protocol.md` for the source-scoring rules and `references/output-docs.md` for the exact content contract.

Useful commands:

```bash
python scripts/run_pipeline.py --idea "<product idea>" --out sdd-docs
python scripts/validate_pack.py sdd-docs --stage gate0
python scripts/run_pipeline.py --idea "<product idea>" --out sdd-docs --stage gate1
python scripts/validate_pack.py sdd-docs --stage gate1
python scripts/run_evals.py --validate
```
