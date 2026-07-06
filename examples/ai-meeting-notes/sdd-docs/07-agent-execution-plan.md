# Agent Execution Plan

- Product idea: AI meeting notes for sales teams
- Status: demo-complete
- Stage: gate3

## Agent Operating Rules

- Start from requirements and contracts, not from PRD prose alone.
- Preserve review-before-sync behavior.
- Do not implement live meeting bot features in MVP.
- Every task must include a validation command or evidence requirement.

## Implementation Phases

| Phase | Goal |
|---|---|
| P1 | Meeting upload and status model |
| P2 | Transcription adapter and transcript segment storage |
| P3 | Structured note extraction with evidence spans |
| P4 | Review and approval UI |
| P5 | CRM export preview and gated write |
| P6 | Evals and regression tests |

## Task List

| ID | Requirements | Task | Depends on | Verify |
|---|---|---|---|---|
| T-001 | FR-001 | Create meeting data model and upload endpoint | none | `pytest tests/test_meeting_upload.py` |
| T-002 | FR-002 | Add transcription adapter interface | T-001 | `pytest tests/test_transcription_adapter.py` |
| T-003 | FR-002 | Store timestamped transcript segments | T-002 | `pytest tests/test_transcript_segments.py` |
| T-004 | FR-003, FR-005 | Generate structured notes with evidence IDs | T-003 | `pytest tests/test_action_item_evidence.py` |
| T-005 | FR-004, NFR-001 | Build review and approval flow | T-004 | `pytest tests/test_approval_flow.py` |
| T-006 | FR-004, NFR-003 | Build CRM export gate | T-005 | `pytest tests/test_crm_export_gate.py` |
| T-007 | NFR-002 | Add configurable audio retention policy | T-001 | `pytest tests/test_retention_policy.py` |

## Agent Session Plan

| Task | Role | Context / Files To Read | Task Prompt | Constraints | Output Format | Validation Evidence |
|---|---|---|---|---|---|---|
| T-001 | backend implementer | `03`, `04#Data Flow`, `05#Data Model` | Create meeting model and upload endpoint. | Keep live bot out of scope. | Code diff plus migration note. | `pytest tests/test_meeting_upload.py` |
| T-004 | AI/eval implementer | `03#EARS Acceptance Criteria`, `06#Reference Cases`, transcript fixtures | Generate structured notes with evidence IDs. | No unsupported action items. | Code diff plus fixture update. | `pytest tests/test_action_item_evidence.py` |
| T-006 | integration implementer | `04#Architecture Decision Lens`, `05#API Contracts`, `06#Bad Cases` | Build gated CRM export preview and write path. | No external write before approval. | Code diff plus sandbox payload example. | `pytest tests/test_crm_export_gate.py` |

Use one session per module when implementation context grows beyond the listed files.

## Parallelization

Frontend review UI can start after API contracts are stable. CRM adapter tests can be written in parallel with note extraction once payload schema is fixed.

## Source Vs Generated Rules

- API schemas are generated from route/type definitions.
- Eval reports are generated from reference, bad, and regression cases.
- Do not hand-edit generated schemas or reports.

## Design And Visual Implementation Phase

- Use `08-ui-visual-design.md` as the UI contract for the review screen before writing frontend code.
- If the repository later gets a durable `DESIGN.md`, keep 08 aligned with it and treat `DESIGN.md` as the broader design source of truth.
- If pixel-level reference matching is required, hand off the approved reference and route state to `$visual-ralph`; do not replace the deterministic product and API checks with subjective UI judgment.

## Living Spec Update Protocol

- If implementation changes behavior, API shape, schema, permissions, CRM side-effect rules, retention policy, visual contract, or validation evidence, update the upstream SpecForge docs before marking the task complete.
- Update `traceability_matrix.json` whenever requirement IDs, task IDs, or eval coverage change.
- Record intentional divergence in the handoff manifest with reason, owner, risk, and validation evidence.

## Validation Commands

```bash
pytest tests/test_meeting_upload.py
pytest tests/test_action_item_evidence.py
pytest tests/test_crm_export_gate.py
python scripts/validate_pack.py sdd-docs --stage all --strict
```

## Launch Handoff

| Area | Required Evidence | Status |
|---|---|---|
| security | approval gate, permission boundary, idempotency, secret handling | required before `launch-ready` |
| performance | upload/status latency and async job budget | required before `launch-ready` |
| monitoring/logging | privacy-safe job logs and failure alerts | required before `launch-ready` |
| CI/CD | automated checks run before deploy; preview uses sandbox CRM | required before `launch-ready` |
| rollback | CRM sync disable path plus data migration rollback note | required before `launch-ready` |

## Handoff To Coding Agent

Start with T-001 and stop after each phase if validation fails. Use `06-eval-and-test-cases.md` as the regression contract.

## Generated AGENTS.md Content

```markdown
# Project Agent Rules

- Follow SpecForge docs in `sdd-docs/`.
- Do not write to CRM before approval.
- Every generated note claim needs transcript evidence.
- Run the validation command listed on each task before marking it done.
```

## Done Definition

- All tasks complete.
- All automated checks pass.
- Eval and test cases include provenance.
- CRM export requires approval.
- Handoff manifest marks build readiness as `build-ready`.
