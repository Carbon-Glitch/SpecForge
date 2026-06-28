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

| ID | Task | Depends on | Verify |
|---|---|---|---|
| T-001 | Create meeting data model and upload endpoint | none | `pytest tests/test_meeting_upload.py` |
| T-002 | Add transcription adapter interface | T-001 | `pytest tests/test_transcription_adapter.py` |
| T-003 | Store timestamped transcript segments | T-002 | `pytest tests/test_transcript_segments.py` |
| T-004 | Generate structured notes with evidence IDs | T-003 | `pytest tests/test_action_item_evidence.py` |
| T-005 | Build review and approval flow | T-004 | `pytest tests/test_approval_flow.py` |
| T-006 | Build CRM export gate | T-005 | `pytest tests/test_crm_export_gate.py` |

## Parallelization

Frontend review UI can start after API contracts are stable. CRM adapter tests can be written in parallel with note extraction once payload schema is fixed.

## Source Vs Generated Rules

- API schemas are generated from route/type definitions.
- Eval reports are generated from golden cases.
- Do not hand-edit generated schemas or reports.

## Validation Commands

```bash
pytest tests/test_meeting_upload.py
pytest tests/test_action_item_evidence.py
pytest tests/test_crm_export_gate.py
python scripts/validate_pack.py sdd-docs --stage all --strict
```

## Handoff To Coding Agent

Start with T-001 and stop after each phase if validation fails. Use `06-eval-golden-dataset.md` as the regression contract.

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
- Golden cases include provenance.
- CRM export requires approval.
- Handoff manifest marks build readiness as `build-ready`.
