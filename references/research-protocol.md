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
