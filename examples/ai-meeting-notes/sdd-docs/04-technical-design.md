# Technical Design

- Product idea: AI meeting notes for sales teams
- Status: demo-complete
- Stage: gate2

## Architecture Overview

The MVP uses a web app plus API backend. Uploaded audio creates a meeting job. A transcription adapter produces timestamped segments. A note extraction service generates structured notes with evidence spans. A review UI lets users edit and approve. A CRM export adapter creates a write payload only after approval.

## Stack Decision

| Layer | Decision | Rationale |
|---|---|---|
| Frontend | React or Next.js | Fast review UI and file upload workflow. |
| Backend | Python FastAPI or Node API | Simple job orchestration and adapter boundaries. |
| Transcription | pluggable adapter | Allows cloud or local backend evaluation. |
| Storage | relational DB plus object storage | Structured approvals plus audio/transcript retention. |

## Open Source Reuse Plan

| Subsystem | Plan |
|---|---|
| Transcription | Evaluate Whisper, whisper.cpp, and hosted alternatives behind one adapter. |
| Summarization | Build product-specific extraction schema and evals. |
| CRM | Build minimal export adapter; avoid generic workflow engine for MVP. |

## Integration Plan

Greenfield demo: no existing codebase integration. For Feature Mode, map every new component to current modules, routes, APIs, schemas, jobs, stores, tests, and deployment surfaces.

## Module Boundaries

| Module | Owns | Must not own |
|---|---|---|
| `meetings` | meeting records, status, retention | CRM-specific writes |
| `transcription` | audio-to-segment adapter | note extraction |
| `notes` | structured summaries and evidence spans | raw audio storage |
| `crm_export` | export payload and external write gate | note generation |
| `evals` | golden cases and deterministic checks | production side effects |

## Data Flow

`upload -> meeting record -> transcription job -> transcript segments -> note extraction -> review edits -> approval -> CRM export payload`

## State Truth Model

| State | Source of truth | Notes |
|---|---|---|
| Meeting metadata | database | persisted |
| Raw audio | object storage | retention governed |
| Transcript segments | database | persisted and citable |
| Generated notes | database | versioned |
| UI draft edits | client state until save | runtime-only |
| CRM export status | database | persisted external side-effect state |

## Workflow Navigation Action Contract

| Screen | Actions |
|---|---|
| Upload | select file, submit upload |
| Meeting processing | refresh status, cancel job |
| Review notes | edit summary, edit action items, approve |
| Export | preview payload, sync to CRM |

Invalid transitions:

- Export before approval
- Approve before transcript and notes exist
- Delete audio while transcription is still running

## Generated Artifact Plan

| Artifact | Source | Command |
|---|---|---|
| API schema | backend route definitions | `npm run generate:api` or equivalent |
| Eval report | golden cases | `python scripts/run_evals.py` |
| CRM payload fixture | contract examples | `python scripts/export_fixtures.py` |

## Failure Handling

- Transcription failure moves meeting to `transcription_failed`.
- Note extraction failure preserves transcript and allows retry.
- CRM export failure records error code and does not mark meeting synced.

## Observability

Log meeting job ID, stage, duration, adapter, failure type, and retry count. Do not log raw transcript text in application logs.

## Performance And Cost

MVP optimizes correctness and review trust before real-time speed. Batch processing is acceptable for uploaded recordings.

## Migration And Rollback

Use additive schema migrations for meeting status and note versions. Keep CRM export idempotency keys to avoid duplicate writes after rollback.
