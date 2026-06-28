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

## Permission Mapping

| Role | Allowed |
|---|---|
| AE | Upload, review own meetings, approve own notes, export own notes. |
| Manager | View team approved notes and risk summaries. |
| Admin | Configure CRM mapping and retention policy. |

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
