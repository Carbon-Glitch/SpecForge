# Idea Pressure Test

- Product idea: AI meeting notes for sales teams
- Generated: 2026-06-28T00:00:00Z
- Status: demo sample
- Research requirement: validate current competitors, pricing, and open-source alternatives before final product decisions

## Pressure Test Status

`completed-demo-sample`

This example is intentionally compact. It demonstrates the shape of a pressure-test gate; it is not a live 2026 market report.

## Verdict

`research-needed -> continue only as a narrow wedge`

The broad "AI meeting notes" category is crowded. The stronger wedge is not generic transcription; it is sales-call follow-up that writes CRM-ready summaries, extracts next steps, and preserves customer objections with evidence.

## Scorecard

| Area | Score | Read |
|---|---:|---|
| Pain intensity | 4/5 | Sales reps lose time turning calls into follow-up and CRM updates. |
| Buyer clarity | 3/5 | Sales leaders and founders care, but seat-level willingness to pay needs proof. |
| Urgency | 3/5 | Useful after every call, but crowded tooling reduces urgency unless workflow fit is sharp. |
| Differentiation | 2/5 | Generic notes are weak; CRM-ready action memory is the possible wedge. |
| Speed to validate | 5/5 | Can test with manual call uploads and hand-edited outputs before full automation. |
| Team advantage | 3/5 | Advantage depends on access to sales users and CRM workflow knowledge. |

## SDD Mode Decision

| Signal | Observation | Mode Impact |
|---|---|---|
| production intent | Commercial SaaS idea with CRM writes and meeting-data privacy risk. | `full-sdd` for real implementation; this example remains `demo-only`. |
| context drift risk | Multiple adapters: upload, transcription, notes, review, CRM export. | Use prompt packets by module in `07`. |
| regression risk | External write gate must never regress. | Requires deterministic evals before build-ready. |
| team scaling | Frontend, backend, and eval work can split. | Explicit module boundaries and session plan required. |

## Core Assumption

Sales teams will repeatedly use and pay for a tool that turns calls into trusted CRM-ready follow-up faster than their current meeting recorder, note template, or manual process.

## Fatal Flaws

| Risk | Severity | Why It Matters | Fast Test |
|---|---|---|---|
| Generic recorder parity | High | Existing tools already summarize meetings. | Ask 10 sales users what they use now and what they still rewrite manually. |
| CRM trust gap | High | If extracted fields are wrong, users must re-check everything. | Manually process 20 real calls and measure correction rate. |
| Privacy and recording friction | Medium | Customer calls may include sensitive data and consent constraints. | Interview 5 teams about recording policy and retention requirements. |

## Problem Reality

- Pain: post-call follow-up, CRM hygiene, missed objections, and next-step tracking.
- Early adopter: founder-led sales teams or small sales teams with messy CRM notes.
- Painkiller or vitamin: painkiller only if it reduces real follow-up and CRM work; vitamin if it only creates nicer summaries.

## Current Behavior And Alternatives

- Current behavior: call recorder, manual notes, CRM fields after the call, sales manager review.
- Direct alternatives: AI meeting assistants and call intelligence tools.
- Indirect alternatives: CRM note templates, outsourced sales ops, rep discipline, spreadsheets.

## First 10 Users

1. Founder-led B2B SaaS teams doing sales calls weekly.
2. Small sales agencies managing client calls and follow-ups.
3. RevOps consultants who see repeated CRM note cleanup pain.

## Two Week MVP Test

- Build: manual upload or calendar import for recorded calls, transcript processing, structured summary, objections, next steps, CRM-ready fields, export to markdown/CSV.
- Cut: automatic bot joining, full CRM sync, team admin, analytics dashboard, advanced coaching.
- Test: process 30 real calls from 5 users; require at least 3 users to reuse it after the first result and at least 2 users to ask for CRM integration or paid continuation.

## Decision

Proceed to Gate 1 only if research confirms a narrow sales workflow wedge and at least one repeat-use signal from real users. Otherwise pivot toward an internal sales-ops tool or a workflow-specific CRM assistant.

## Evidence To Verify

- Current AI meeting assistant competitors and pricing.
- Current open-source transcription and meeting-note projects.
- Sales-user complaints about CRM follow-up and post-call admin.
- Privacy and recording expectations for customer calls.
