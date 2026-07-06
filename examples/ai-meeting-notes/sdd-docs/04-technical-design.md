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

## Architecture Decision Lens

| Option | Real Pain Solved | Stage Fit / Overengineering Risk | One-Year Technical Debt | Team Scaling Cost | Migration / Rollback Path | Evidence |
|---|---|---|---|---|---|---|
| Pluggable transcription adapter | Avoids locking the product to one transcription engine before accuracy/cost research is complete. | Good MVP fit; lower risk than building custom speech recognition. | Adapter maintenance and fixture drift across providers. | Backend and eval work can split by adapter contract. | Swap provider behind interface; keep transcript segment schema stable. | `01-reality-research.md#GitHub And Open Source Findings`, `research_ledger.json.github_open_source` |
| Review-before-CRM-write gate | Solves trust gap for generated sales notes and prevents bad external writes. | Not overengineering because CRM writes are a core risk. | More UI and audit complexity than auto-sync. | Clear frontend/backend boundary for approval state. | Feature flag external sync; retain markdown/CSV export fallback. | `01-reality-research.md#Risk And Compliance Findings` |
| Relational DB plus object storage | Separates structured approvals from large audio files. | Standard fit for uploaded recordings; avoids premature event sourcing. | Retention and deletion workflows must stay synchronized. | Data ownership remains understandable for new contributors. | Additive migrations; object keys remain outside note schema. | `01-reality-research.md#Official Documentation Findings` |

## Frontend Architecture Decisions

| Decision Area | Options To Research | Chosen Direction | Why It Fits | Validation Evidence |
|---|---|---|---|---|
| rendering | CSR / SSR / hybrid routes | Hybrid: marketing pages can be SSR/static; review workflow is interactive app UI. | Review screen needs rich interaction; public pages may need SEO. | route snapshot plus Core Web Vitals before launch. |
| state ownership | server state / client global / URL / local UI | Server state for meetings/transcripts; local UI state for unsaved edits; URL for selected meeting. | Avoids duplicating meeting truth in client stores. | approval-flow state test and unsaved-edit warning test. |
| interaction and motion | CSS transitions / animation library / none | Minimal transitions for upload, processing, and approve/export feedback. | Trust matters more than decorative motion. | screenshot/manual motion review with reduced-motion rule. |
| component system | existing component library / headless primitives / custom | Accessible table, dialog, upload, and diff/review primitives. | Faster MVP while preserving a11y. | a11y contrast and keyboard review. |

## Backend Architecture Decisions

| Decision Area | Options To Research | Chosen Direction | Why It Fits | Validation Evidence |
|---|---|---|---|---|
| deployment shape | modular monolith / services / serverless jobs | Modular monolith plus background job adapter for MVP. | Keeps CRM gate, notes, and transcript workflow understandable. | integration tests for job status transitions. |
| domain boundaries | CRUD modules / DDD contexts | Modules: meetings, transcription, notes, CRM export, evals. | Clear enough without premature DDD ceremony. | module boundary review. |
| API style | REST / RPC / GraphQL | REST-like endpoints for upload/review/export. | Simple client contract and easy HTTP testing. | API contract tests. |
| async/workflow | direct call / queue / workflow engine | Background job for transcription and note extraction. | Uploads can be slow and retryable. | retry/idempotency tests. |
| caching | no cache / app cache / HTTP cache | Avoid caching sensitive transcript/note detail in MVP. | Privacy and correctness beat speed. | cache-control header review. |

## Data Architecture Decisions

| Decision Area | Options To Research | Chosen Direction | Why It Fits | Validation Evidence |
|---|---|---|---|---|
| primary store | relational / document / object | Relational DB for metadata and structured notes; object storage for audio. | Approval, audit, and export state need relational consistency. | schema and relationship tests. |
| schema and migrations | additive / destructive | Additive migrations for statuses, versions, and export records. | Preserves rollback and auditability. | migration command. |
| indexes and query paths | owner/time/status indexes | Index meetings by owner/status/created_at; action items by meeting_id. | Main flows list user meetings and load one review. | query plan or benchmark before launch. |
| transactions and consistency | strong / eventual / idempotent | Strong approval state; idempotent CRM export. | Prevents duplicate or unapproved writes. | CRM export gate tests. |
| retention and privacy | TTL / policy field / hard delete | `retention_until` for audio; transcript/note retention follows workspace policy. | Meeting data is sensitive. | retention policy tests. |

## Algorithm And Data Structure Decisions

| Capability | Options To Research | Trigger To Use | Chosen Direction | Validation Evidence |
|---|---|---|---|---|
| search | keyword / full-text / vector | Needed only after users need historical call retrieval. | Defer to future pack; keep transcript segments searchable later. | not_applicable for MVP. |
| ranking/recommendation | rules / scoring / embeddings | Not central to upload-first MVP. | not_applicable. | not_applicable. |
| rate limiting | fixed window / token bucket / quota ledger | Needed to control upload/transcription cost. | Simple per-user upload quota for MVP. | quota limit test before build-ready. |
| scheduling/queues | FIFO / delay queue / workflow DAG | Required for transcription and extraction retries. | FIFO job queue with retry and idempotency key. | retry and duplicate job tests. |
| graph/relationship | adjacency / graph DB | No graph traversal in MVP. | not_applicable. | not_applicable. |

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
| `evals` | reference cases and deterministic checks | production side effects |

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
| Eval report | reference and regression cases | `python scripts/run_evals.py` |
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
