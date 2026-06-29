# Eval And Golden Dataset

- Product idea: AI meeting notes for sales teams
- Status: demo-complete
- Stage: gate3

## Eval Philosophy

Evaluation must prove that generated notes are grounded in transcript evidence and that external writes are gated by user approval.

## Launch Thresholds

| Metric | Launch threshold |
|---|---|
| Action item evidence coverage | >= 90% |
| Unapproved CRM writes | 0 |
| Missing required CRM fields blocked | 100% |
| Duplicate export prevention | 100% |

## Deterministic Judge Contract

| Requirement | Judge type | Evidence |
|---|---|---|
| FR-002 | state check | transcript segment count and timestamps |
| FR-004 | API test | CRM export returns blocked before approval |
| FR-005 | state check | every action item has evidence segment IDs |
| NFR-001 | database check | approval and edit audit rows exist |

## Evidence Matrix

| Case | Requirement | Command | Expected |
|---|---|---|---|
| GC-001 | FR-005 | `pytest tests/test_action_item_evidence.py` | all action items include evidence |
| GC-002 | FR-004 | `pytest tests/test_crm_export_gate.py` | export blocked before approval |
| BC-001 | NFR-003 | `pytest tests/test_preview_no_external_write.py` | no external write in preview |

## Data Sufficiency Check

Fixtures must include:

- Clean sales call with clear next steps
- Call with objections but no next step
- Call with ambiguous owner
- Call with missing due date
- Corrupted or empty upload
- CRM contact mismatch

## Golden Case Source Policy

Every case declares one source:

- `user-confirmed`: supplied or approved by a real user
- `real-source-derived`: derived from real product/research source patterns without copying private data
- `existing-test-derived`: derived from existing repository tests or fixtures
- `synthetic`: generated to cover an edge case

Build-ready packs must include at least one non-synthetic golden case and must not rely only on `synthetic` cases.

## Golden Cases

| ID | Source | Input | Expected |
|---|---|---|---|
| GC-001 | real-source-derived | Transcript includes "I'll send pricing tomorrow; Sarah owns the security review." | Action items include pricing follow-up and Sarah security review with evidence spans. |
| GC-002 | user-confirmed | User-approved sample call with a CRM contact and deal ID. | Approved note exports exactly one CRM payload with idempotency key. |
| GC-003 | synthetic | Transcript has decision but no due date. | Action item includes `missing_due_date: true`, not a fabricated date. |

## Bad Cases

| ID | Source | Input | Expected |
|---|---|---|---|
| BC-001 | synthetic | User tries CRM export before approval. | Export is blocked and no external write is attempted. |
| BC-002 | synthetic | Transcript does not mention a discount. | Summary must not invent a discount promise. |

## Regression Cases

| ID | Source | Input | Expected |
|---|---|---|---|
| RC-001 | synthetic | Approved note is exported twice with same idempotency key. | CRM receives one write; second call returns existing export status. |
| RC-002 | synthetic | User edits notes before approval. | Audit trail records generated version and edited version. |

## Edge Cases

| ID | Source | Input | Expected |
|---|---|---|---|
| EC-001 | synthetic | Empty audio file. | Meeting moves to failed status with retry guidance. |
| EC-002 | synthetic | CRM contact mismatch. | Export preview asks user to resolve mapping. |

## Automated Checks

- `pytest tests/test_action_item_evidence.py`
- `pytest tests/test_crm_export_gate.py`
- `pytest tests/test_retention_policy.py`

## Manual Review

Reviewers inspect 10 transcripts and confirm extracted decisions and action items are grounded and useful.

## Regression Gates

- No unapproved external writes.
- No generated action item without evidence.
- No pass case can include unresolved error or failed status.
