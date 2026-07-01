# UI Visual Design

- Product idea: AI meeting notes for sales teams
- Status: demo-complete
- Stage: optional-visual

## Visual Design Status

`contract-ready-demo`

This document is a visual implementation contract, not a final mockup or pixel baseline.

## Design Source Of Truth

Use this `08-ui-visual-design.md` as the local visual contract for the MVP review screen. If the repository later has `DESIGN.md`, that file owns broader design governance and this document owns the feature-level implementation contract.

## Design Positioning

The MVP should feel work-focused, trustworthy, and reviewable. It should not feel like a generic meeting recorder landing page. The first screen should foreground the generated sales follow-up artifact, transcript evidence, and approval gate.

## Design Tokens

| Token | Value | Use |
|---|---|---|
| `color.bg` | `#F7F8FA` | App background |
| `color.surface` | `#FFFFFF` | Panels and editor surfaces |
| `color.text` | `#17202A` | Primary text |
| `color.muted` | `#5D6775` | Secondary metadata |
| `color.accent` | `#2563EB` | Primary action and focused state |
| `radius.panel` | `8px` | Panels and repeated items |
| `space.grid` | `16px` | Main grid rhythm |

## Core Components

| Component | States | Rule |
|---|---|---|
| Meeting status header | processing, ready, failed, approved | Always shows source file, status, and retry/review action. |
| Evidence-backed action item | normal, low-confidence, edited | Shows owner, due date, confidence, and transcript span link. |
| CRM export preview | blocked, ready, exported | Export button is disabled until approval. |
| Transcript evidence drawer | closed, open, highlighted | Opens without covering the approval action on desktop or mobile. |

## Page Skeletons

| Route | Layout |
|---|---|
| `/meetings` | Dense list with status, owner, date, and next required action. |
| `/meetings/:id/review` | Header, summary/evidence split, action items, CRM preview, approval controls. |
| `/settings/retention` | Retention controls and privacy copy. |

## Interaction And Motion

- Use short state transitions for drawer open/close and approval success.
- Avoid decorative motion during review; the user is checking evidence.
- Respect reduced-motion preferences.

## Responsive And Accessibility

- At 375px width, the review route stacks summary, action items, evidence, and CRM preview vertically.
- Primary actions remain visible after scrolling to CRM preview.
- Text and control contrast should meet WCAG AA.
- Keyboard focus must move through upload, action-item edit, evidence link, approve, and export controls.

## UI Judge Contract

| Type | Requirement | Evidence |
|---|---|---|
| screenshot_manual | Review screen fits at 1440px and 375px without text overlap. | Screenshot paths or reviewer note. |
| a11y_contrast | Primary text, muted text, and accent buttons meet contrast target. | Contrast command or manual audit. |
| route_snapshot | `/meetings/:id/review` renders review UI with GC-002 fixture. | Screenshot command and route state. |

## MVP Visual Non Goals

- No marketing hero page.
- No animated transcript playback.
- No manager analytics dashboard.
- No full CRM marketplace UI.

## Design Orchestration

- Use `$design` first if the repository needs a durable `DESIGN.md`.
- Use `$visual-ralph` only when an approved visual reference or live baseline exists and pixel/reference matching is required.
- Keep `08-ui-visual-design.md` focused on implementation constraints that code agents can execute and validators can check.
