# Changelog

## 1.2.0 - 2026-06-28

- Adds explicit staged gates: Gate 1 brief/research, Gate 2 PRD/requirements/technical design, Gate 3 contracts/evals/agent plan.
- Changes `run_pipeline.py` default behavior to scaffold Gate 1 only; full-pack scaffolding now uses `--stage all`.
- Adds staged validation with `validate_pack.py --stage gate1|gate2|gate3|all`.
- Adds golden-case provenance rules and strict checks for all-synthetic evals, contradictory pass/error cases, and duplicate-looking cases.
- Adds a compact completed example pack under `examples/ai-meeting-notes/sdd-docs/`.
- Strengthens README positioning around live research, open-source reuse, executable contracts, and deterministic eval planning.

## 1.1.0 - 2026-06-28

- Adds executable contracts before code-agent implementation.
- Adds required state truth, workflow/action, deterministic judge, module/file boundary, generated artifact, and data sufficiency sections.
- Updates scaffold, validator, manifest, and eval criteria to enforce the new contracts.

## 1.0.0 - 2026-06-28

- Initial release.
- Adds the eight-document SDD pack contract.
- Adds mandatory live research protocol for market, official docs, GitHub open-source technology, risk, and implementation prior art.
- Adds scaffold, validation, eval, and cross-platform install support.
