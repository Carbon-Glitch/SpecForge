# PRD And Behavior Contract

- Product idea: AI meeting notes for sales teams
- Status: demo-complete
- Stage: gate2

## Problem Statement

Sales teams lose follow-up quality when meeting notes are incomplete, unstructured, or disconnected from CRM workflows.

## Goals

| ID | Goal |
|---|---|
| G-001 | Convert meeting audio into transcript-grounded sales notes. |
| G-002 | Require human review before CRM sync. |
| G-003 | Make every AI claim traceable to a transcript span. |

## Personas

- Account executive: wants fast follow-up and less admin.
- Sales manager: wants reviewable deal risk and commitments.
- RevOps admin: wants structured, auditable CRM data.

## Scope

In scope:

- Audio upload
- Transcription adapter
- Summary, decisions, objections, action items
- Review and edit workflow
- CRM-ready export payload

## Anti Goals

- No live meeting bot in MVP.
- No automatic CRM writes without approval.
- No unsupported language expansion before English evals pass.

## Core User Journeys

| ID | Journey |
|---|---|
| J-001 | Upload recording -> transcript -> review summary -> export CRM note. |
| J-002 | Review action items -> assign owner -> mark missing due dates -> approve. |
| J-003 | Manager opens approved meeting -> sees risks, decisions, and evidence snippets. |

## Compatibility Contract

Not applicable for this greenfield demo. For Feature Mode, this section must list existing behaviors, APIs, data shapes, tests, and user workflows that the new feature must preserve.

## Behavior Contract

- The system must never present generated notes as final until approved.
- Every extracted action item must link back to transcript evidence.
- CRM export must fail closed if required account/deal/contact fields are missing.

## Guardrails

- Do not infer promises that are not supported by transcript spans.
- Do not write to external systems without explicit user action.
- Do not retain raw audio beyond configured retention.

## Success Metrics

| ID | Metric |
|---|---|
| M-001 | 90% of generated action items have owner and evidence span. |
| M-002 | 80% of reviewed meetings are approved with minor edits only. |
| M-003 | 0 unapproved CRM write attempts in automated tests. |

## Release Criteria

- Gate 3 evals pass on at least 10 user-confirmed or real-source-derived cases.
- CRM export contract is covered by automated tests.
- Retention and delete flows are implemented.
