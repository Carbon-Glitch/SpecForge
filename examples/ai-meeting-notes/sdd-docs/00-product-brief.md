# Product Brief

- Product idea: AI meeting notes for sales teams
- Status: demo-complete
- Stage: gate1

## Mode

greenfield

## SDD Mode

`full-sdd` for a real build because the product handles private meeting data, external CRM writes, and multiple implementation modules. This example pack is `demo-only` and must refresh live research before implementation.

## Brainstorming Summary

The product direction is an upload-first sales meeting notes tool, not a live meeting bot. The recommended MVP emphasizes transcript-grounded action items, human review, and gated CRM export.

## Concept

MeetingBrief is a privacy-aware AI meeting notes product for sales teams. It records or imports meeting audio, transcribes the conversation, extracts decisions and action items, and syncs structured follow-ups to the CRM.

## Target Users

| ID | User | Job |
|---|---|---|
| U-001 | Account executive | Leave calls with accurate follow-up actions without manual note cleanup. |
| U-002 | Sales manager | Review call outcomes and risks without watching recordings. |
| U-003 | RevOps admin | Ensure CRM notes are complete, structured, and auditable. |

## Jobs To Be Done

- JTBD-001: Capture reliable notes from customer calls.
- JTBD-002: Extract decisions, objections, next steps, and owners.
- JTBD-003: Sync reviewed summaries to the CRM.
- JTBD-004: Preserve privacy and consent boundaries for recorded meetings.

## Scope Boundary

| Area | Status | Rule |
|---|---|---|
| Upload-first meeting note workflow | in_pack | Specify upload, transcript, structured notes, review, and gated CRM export. |
| Live meeting bot | future_pack | Mention assumptions only; do not task implementation. |
| Multi-CRM marketplace | future_pack | Keep export contract generic and defer provider-specific marketplace work. |
| Sales coaching analytics | referenced_only | Preserve data shape for future analytics but do not build dashboards. |

## Prescriptive Inputs

| Source | Why It Is Prescriptive | Rule |
|---|---|---|
| Gate 0 pressure test | Defines narrow sales workflow wedge. | Avoid generic meeting assistant scope. |
| Reality research ledger | Records open-source and competitor evidence. | Cite source-backed claims before stack and product decisions. |

## This Pack Owns

| Owned Area | Requirements | Explicit Non-Ownership |
|---|---|---|
| Meeting upload and processing | FR-001, FR-002, FR-003 | No live meeting bot. |
| Review and CRM export gate | FR-004, NFR-001, NFR-003 | No uncontrolled external writes. |
| Evidence-backed action items | FR-005 | No unsupported generated claims. |

## Existing System Context

Not applicable. This demo describes a greenfield product. For feature work, this section should summarize the existing repository, current architecture, affected modules, tests, and integration constraints.

## Success Criteria

| ID | Criterion |
|---|---|
| SC-001 | A user can upload a meeting recording and receive transcript, summary, decisions, and action items. |
| SC-002 | Every action item includes owner, due date or missing-date flag, source quote, and confidence. |
| SC-003 | Users review and approve notes before CRM sync. |
| SC-004 | The system stores source citations from transcript spans for every generated claim. |

## Constraints

- MVP supports recording upload first; live meeting bot is out of scope.
- CRM sync starts with HubSpot-style generic contact/deal mapping.
- All AI outputs require user review before external write.

## Assumptions

- Sales teams already have recordings or call audio exports.
- English-language calls are the first target.
- Privacy-sensitive customers prefer review-before-sync over full automation.

## Open Questions

| ID | Question | Blocking |
|---|---|---|
| Q-001 | Which CRM should be first: HubSpot, Salesforce, or a generic webhook? | yes |
| Q-002 | Should the first version support local transcription, cloud transcription, or both? | yes |
| Q-003 | What retention policy is required for audio files? | yes |
| Q-004 | Should managers see raw transcripts or only approved notes? | no |
