# SDD Requirements Spec

- Product idea: AI meeting notes for sales teams
- Status: demo-complete
- Stage: gate2

## Functional Requirements

| ID | Requirement |
|---|---|
| FR-001 | The system shall accept an audio file upload and create a meeting record. |
| FR-002 | The system shall generate a transcript with timestamped segments. |
| FR-003 | The system shall generate summary, decisions, objections, and action items. |
| FR-004 | The system shall require user approval before CRM export. |
| FR-005 | The system shall include transcript evidence for each generated action item. |

## Non Functional Requirements

| ID | Requirement |
|---|---|
| NFR-001 | The system shall preserve an audit trail for edits and approvals. |
| NFR-002 | The system shall support configurable audio retention. |
| NFR-003 | The system shall avoid external writes in test and preview environments. |

## User Stories

- US-001: As an account executive, I want generated action items so I can follow up quickly.
- US-002: As a manager, I want evidence-linked risks so I can inspect deal status.
- US-003: As RevOps, I want exportable structured notes so CRM data stays consistent.

## EARS Acceptance Criteria

- When a user uploads a supported audio file, the system shall create a meeting record with status `transcribing`.
- When transcription completes, the system shall store timestamped transcript segments.
- When notes are generated, the system shall attach at least one evidence segment to each action item.
- If a required CRM field is missing, the system shall block export and show the missing field list.
- While a meeting is unapproved, the system shall not write notes to the CRM.

## Regression Requirements

Not applicable for this greenfield demo. For Feature Mode, list existing tests and behaviors that must remain unchanged.

## Edge Cases

- Empty or corrupted audio file
- Multiple speakers with unclear attribution
- Action item without explicit due date
- User edits generated notes before approval
- CRM contact cannot be matched

## Out Of Scope

- Live bot joining meetings
- Real-time coaching
- Multi-language transcription quality guarantees
