# Contracts Data And Permissions

- Product idea: AI meeting notes for sales teams
- Status: demo-complete
- Stage: gate3

## API Contracts

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/meetings` | POST | Create meeting from upload metadata. |
| `/api/meetings/{id}` | GET | Read meeting, transcript, notes, status. |
| `/api/meetings/{id}/approve` | POST | Approve reviewed notes. |
| `/api/meetings/{id}/crm-export` | POST | Export approved notes. |

## Data Model

| Entity | Required fields |
|---|---|
| Meeting | `id`, `owner_id`, `status`, `created_at`, `retention_until` |
| TranscriptSegment | `id`, `meeting_id`, `start_ms`, `end_ms`, `speaker`, `text` |
| ActionItem | `id`, `meeting_id`, `owner`, `task`, `due_date`, `evidence_segment_ids`, `confidence` |
| Approval | `id`, `meeting_id`, `approved_by`, `approved_at`, `note_version` |
| CrmExport | `id`, `meeting_id`, `target`, `status`, `idempotency_key` |

## State Model Contract

- Persist meeting status transitions.
- Persist generated notes and user edits as versions.
- Runtime UI state may hold unsaved edits but must warn before leaving.
- Snapshot tests should compare meeting, transcript, notes, approvals, and export status.

## Tool Contracts

| Tool | Tier | Contract |
|---|---|---|
| Transcription adapter | read-write internal | Reads audio, writes transcript segments. |
| Note extractor | read-write internal | Reads transcript, writes draft notes with evidence. |
| CRM exporter | external write | Requires approval and idempotency key. |

## Access And Permission Rules

| Role | Allowed |
|---|---|
| AE | Upload, review own meetings, approve own notes, export own notes. |
| Manager | View team approved notes and risk summaries. |
| Admin | Configure CRM mapping and retention policy. |

## Cache And Consistency Contract

| Cached Thing | Source Of Truth | Cache Layer | Invalidation Rule | Staleness Budget | Failure Behavior |
|---|---|---|---|---|---|
| Meeting list | database | client/server data cache | invalidate after upload, approve, export, delete | 30 seconds for list view | refresh from database |
| Meeting detail | database | no persistent shared cache in MVP | reload after every status transition | 0 for approval/export state | fail closed before CRM export |
| CRM export preview | generated from approved note and mapping | runtime only | regenerate after note edit or mapping change | 0 | block export |

## Data Access And Index Contract

| Query / Access Path | Owner | Expected Cardinality | Index / Search Structure | Permission Filter | Validation |
|---|---|---|---|---|---|
| list user's meetings | meetings service | thousands per user | `(owner_id, created_at desc)` | `owner_id = current_user` | query plan or repository test |
| load review screen | meetings service | one meeting with transcript segments | `meeting_id` on transcript/action/approval/export rows | owner or team permission | API contract test |
| find export by idempotency key | CRM exporter | one per approved meeting/export target | unique `(target, idempotency_key)` | owner/admin export permission | duplicate export test |

## Module File Responsibility Contract

| File / module | Allowed | Forbidden |
|---|---|---|
| `notes/extractor` | Schema extraction and evidence mapping | CRM writes |
| `crm/exporter` | Payload construction and sync | AI generation |
| `meetings/service` | Status transitions and retention | UI-only draft state |
| `evals/cases` | Fixtures and expected outcomes | Production secrets |

## Security Boundaries

- Audio and transcripts are sensitive.
- CRM tokens must be encrypted and never logged.
- Export actions require approval and audit record.

## Storage And Retention

Raw audio retention defaults to 30 days in the demo. Transcript and approved notes follow workspace retention policy.

## External Integrations

CRM integration begins as a generic webhook or HubSpot-like adapter. Salesforce support is deferred until field mapping requirements are confirmed.
