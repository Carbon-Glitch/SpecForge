# Research Protocol

The skill treats live research as a required production step. The agent must not choose market positioning, pricing, frameworks, APIs, models, SDKs, or open-source libraries from memory alone.

## Research Passes

### 1. Market Reality

Find current evidence for:

- direct competitors
- indirect substitutes
- target user workflow
- pricing and packaging patterns
- distribution channels
- common complaints and unmet needs
- category maturity

Minimum source mix:

- official product pages for competitors
- pricing pages or changelogs where available
- current reviews, forums, app stores, Reddit, Hacker News, G2, Product Hunt, or similar sources when relevant
- recent articles only as supporting evidence, not primary truth

### 2. Official Documentation

For every major technology candidate, read official docs:

- framework docs
- API docs
- model provider docs
- SDK docs
- deployment platform docs
- database or vector-store docs

Prefer docs with visible version numbers, release notes, or changelog dates.

### 3. GitHub And Open Source Reuse

The goal is not just to know what exists. The goal is to reduce development cost by reusing real engineering assets when appropriate.

For each product subsystem, search for reusable:

- full applications or starter kits
- frameworks
- modules
- libraries
- UI components
- backend services
- workflow engines
- agent runtimes
- tool registries
- eval harnesses
- reference implementations

For each open-source option, inspect:

- README scope and install instructions
- latest release date
- commit recency
- issue activity
- license
- ecosystem fit
- API stability
- project size and complexity
- maintenance risk

Stars are weak evidence. A repository with fewer stars but active maintenance and better API fit may be better.

Classify every serious candidate with one reuse decision:

| Decision | Meaning |
| --- | --- |
| `reuse as-is` | Use directly with configuration only |
| `integrate via API/SDK` | Keep as dependency/service and connect through its public surface |
| `wrap` | Build a thin adapter around it |
| `fork and modify` | Copy/fork and change internals because the fit is close but incomplete |
| `extract pattern only` | Do not use the code, but use its architecture or UX pattern |
| `build from scratch` | Reuse is unsuitable after evidence-backed review |

For every `build from scratch` decision, record why reuse was rejected. Common valid reasons:

- license conflict
- inactive or abandoned project
- poor security posture
- API mismatch that would cost more than implementation
- excessive dependency weight
- incompatible architecture
- missing critical feature
- low trust because tests/docs/issues suggest instability

Common invalid reasons:

- "we can write it ourselves"
- "the agent knows how"
- "not invented here"
- "stars are too low" without maintenance or fit analysis

## Open-Source Cost Model

Estimate both saved cost and integration cost:

| Field | Description |
| --- | --- |
| saved_build_scope | What we do not need to build |
| integration_work | Adapter, migration, customization, styling, auth, hosting, tests |
| maintenance_burden | Fork drift, dependency upgrades, security patches |
| lock_in | Whether the architecture becomes coupled to this project |
| confidence | high, medium, low |

Example:

```json
{
  "subsystem": "workflow engine",
  "candidate": "example/workflow-runtime",
  "decision": "integrate via API/SDK",
  "saved_build_scope": "DAG execution, retries, job state, visualization",
  "integration_work": "write adapters for project tasks and evidence events",
  "maintenance_burden": "medium",
  "confidence": "medium"
}
```

### 4. Risk, Compliance, And Safety

Search current rules and common risk patterns:

- privacy and data retention
- user consent
- model/provider terms
- data residency
- regulated-domain constraints
- prompt injection and tool permission risks
- destructive action approvals
- audit log expectations

For legal/regulatory claims, prefer official government/regulator/vendor policy pages. Mark uncertain interpretations as inference.

### 5. Implementation Prior Art

Look for:

- reference architectures
- starter kits
- example apps
- common anti-patterns
- migration guides
- production postmortems
- benchmark results

Use these to reduce implementation risk and to define validation commands.

### 6. Architecture Decision Evidence

For each major architecture, stack, hosting, data, auth, agent, or open-source choice, gather evidence that helps answer:

- what real product or engineering pain the choice solves
- whether it fits the current stage or is premature overengineering
- what one-year technical debt or migration burden it creates
- whether a larger team or multiple code agents can work safely with it
- what the migration, replacement, or rollback path looks like

Do not copy static technology recommendations from old articles or model memory. Use current official docs, repository health, release notes, migration guides, issue history, and primary vendor guidance.

### 7. Launch Readiness

For production-intended or `production-hardening` packs, research current guidance for:

- authentication, authorization, secrets, and destructive-action approvals
- data privacy, retention, audit logs, and permission boundaries
- performance budgets, Core Web Vitals for web UI, or API latency targets for backend products
- monitoring, logging, tracing, error reporting, and privacy-safe observability
- CI/CD, preview/prod separation, environment variables, migration rollout, and rollback

Prefer official platform docs and primary vendor guidance. Record unclear launch claims as `Inference` or `Unknown`.

### 8. Domain Architecture

Research the engineering decision dimensions that match the product surface. Do not hardcode a favorite stack.

Frontend research:

- rendering and routing modes: CSR, SSR, SSG, ISR, server components, native shells, or hybrid choices
- state ownership: server/cache state, client global state, URL state, local UI state, and duplicate-source-of-truth risks
- interaction and motion: CSS transitions, animation libraries, timeline engines, reduced-motion support, and performance impact
- component and design-system options: headless primitives, component libraries, custom systems, accessibility, and theming

Backend research:

- deployment shape: modular monolith, services, serverless, edge functions, workers, or hybrid
- domain boundaries: CRUD modules, DDD bounded contexts, plugin architecture, or generated modules
- API style: REST, GraphQL, RPC/tRPC, gRPC, events, webhooks, or tool interfaces
- async/workflow: direct calls, queues, schedulers, workflow engines, event streams, retries, and idempotency
- caching: HTTP/CDN, app cache, data cache, client cache, invalidation, and staleness budgets

Data research:

- primary and secondary stores: relational, document, key-value, graph, object, vector, search engine, or warehouse
- schema and migrations: additive vs destructive migration, generated schema, rollback, seed data
- indexes and query paths: B-tree, compound, partial, full-text, vector, graph traversal, or external search
- transactions and consistency: strong consistency, eventual consistency, optimistic concurrency, idempotency, and conflict resolution
- retention and privacy: TTL, soft delete, hard delete, audit archive, data export, and per-tenant isolation

Algorithm and data-structure research:

- search: keyword, full-text, vector, hybrid, reranking, or external engine
- ranking/recommendation: rules, scoring functions, embeddings, graph features, or learning-to-rank
- rate limiting and quotas: fixed window, sliding window, token bucket, leaky bucket, account ledger
- scheduling and queues: FIFO, priority queue, delay queue, workflow DAG, retries, dead-letter handling
- graph/relationship logic: adjacency lists, closure tables, derived edges, graph database, permission traversal

For each selected option, record official docs, GitHub/package health when applicable, rejected alternatives, and a validation command or evidence type. If a workstream is irrelevant, mark it `not_applicable` with reason.

## Source Scoring

Use this confidence scale:

| Confidence | Source Pattern |
| --- | --- |
| High | Official docs, standards, repository source/release notes, primary data |
| Medium | Maintainer blogs, reputable technical articles, high-signal forum posts with evidence |
| Low | Generic blogs, marketing pages without details, unsourced social posts |

Every claim in `01-reality-research.md` should be labeled as:

- `Evidence` — directly supported by a source
- `Inference` — reasoned conclusion from evidence
- `Unknown` — not established by available evidence

## Required Research Ledger Fields

Each source in `research_ledger.json` should include:

```json
{
  "title": "Source title",
  "url": "https://example.com",
  "publisher": "Example",
  "published_or_updated": "2026-06-01",
  "accessed_at": "2026-06-28T00:00:00Z",
  "claim_supported": "What this source proves",
  "confidence": "high"
}
```

## Research Failure Handling

If web search is unavailable:

1. Continue generating the pack.
2. Put `Research Status: blocked` in `01-reality-research.md`.
3. Mark stack choices as provisional.
4. List exact searches that should be run later.
5. Do not pretend current-world claims are verified.

## Rejected Options

Every major choice needs a rejected-options table:

| Option | Why rejected | Evidence | Revisit trigger |
| --- | --- | --- | --- |

This prevents the code agent from re-litigating decisions without new evidence.

## Required Open-Source Reuse Table

`01-reality-research.md` must include:

| Subsystem | Candidate | URL | Decision | Why | Integration Cost | Build Cost Saved | License | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

At least one row is required for every non-trivial subsystem. If no candidate exists, the row should still document the search terms and explain why the decision is `build from scratch`.
