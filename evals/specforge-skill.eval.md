# Eval: specforge-skill

This eval checks that the skill can scaffold and validate a pressure-test preflight, the eight-document SDD pack, and the optional visual contract.

```json
{
  "skill": "specforge-skill",
  "run": "python scripts/run_pipeline.py --idea \"{idea}\" --out {output} --stage all --include-visual --force",
  "criteria": [
    {
      "id": "valid-pack",
      "text": "The generated pack passes validate_pack.py.",
      "type": "command",
      "cmd": "python scripts/validate_pack.py {output} --stage all"
    },
    {
      "id": "has-preflight-plus-eight-core-docs-and-visual",
      "text": "The pack contains the pressure-test preflight, the eight core markdown documents, and optional visual design contract.",
      "type": "command",
      "cmd": "python -c \"from pathlib import Path; p=Path(r'{output}'); docs={x.name for x in p.glob('*.md')}; assert 'preflight-idea-pressure-test.md' in docs and '08-ui-visual-design.md' in docs and len(docs)==10\""
    },
    {
      "id": "has-research-ledger",
      "text": "The pack includes a research ledger JSON artifact.",
      "type": "command",
      "cmd": "python -c \"import json, pathlib; json.load(open(pathlib.Path(r'{output}')/'research_ledger.json', encoding='utf-8'))\""
    },
    {
      "id": "has-temporal-freshness-guard",
      "text": "The research ledger includes a current date anchor, freshness policy, query log, freshness summary, and source freshness fields.",
      "type": "command",
      "cmd": "python -c \"import json, pathlib; p=pathlib.Path(r'{output}'); data=json.load(open(p/'research_ledger.json', encoding='utf-8')); assert 'current_date_anchor' in data and 'current_year' in data['current_date_anchor']; assert 'freshness_policy' in data and 'query_log' in data and 'freshness_summary' in data; fields=set(data['source_fields']); assert {'freshness_status','freshness_reason','retrieval_method','query_used'} <= fields\""
    },
    {
      "id": "reality-research-has-freshness-sections",
      "text": "The reality research document includes temporal freshness guard, search query log, and freshness assessment sections.",
      "type": "command",
      "cmd": "python -c \"from pathlib import Path; text=(Path(r'{output}')/'01-reality-research.md').read_text(encoding='utf-8'); assert '## Temporal Freshness Guard' in text and '## Search Query Log' in text and '## Freshness Assessment' in text\""
    },
    {
      "id": "has-scope-and-docs-first-fields",
      "text": "The generated pack includes scope boundary, prescriptive inputs, this-pack ownership, SDD mode, research depth, and unverified-claims fields.",
      "type": "command",
      "cmd": "python -c \"import json, pathlib; p=pathlib.Path(r'{output}'); text=(p/'00-product-brief.md').read_text(encoding='utf-8'); assert '## Scope Boundary' in text and '## SDD Mode' in text; data=json.load(open(p/'research_ledger.json', encoding='utf-8')); assert 'research_depth' in data and 'unverified_claims' in data\""
    },
    {
      "id": "visual-contract-connected-to-evals",
      "text": "The optional visual contract is connected to the eval/UI judge and agent execution plan.",
      "type": "llm-judge"
    },
    {
      "id": "readiness-is-not-overstated",
      "text": "The skill distinguishes spec-complete from build-ready and does not claim build-ready without automated checks and runnable validation evidence.",
      "type": "llm-judge"
    },
    {
      "id": "research-is-mandatory",
      "text": "The output clearly requires live research before final technology and market claims.",
      "type": "llm-judge"
    },
    {
      "id": "open-source-reuse-is-mandatory",
      "text": "The output requires GitHub open-source reuse decisions before building non-trivial subsystems from scratch.",
      "type": "llm-judge"
    },
    {
      "id": "has-executable-contracts",
      "text": "The generated pack contains executable contracts for state truth, workflow/navigation/actions, module/file boundaries, generated artifacts, deterministic judging, and data sufficiency.",
      "type": "llm-judge"
    },
    {
      "id": "has-sdd-mode-decision",
      "text": "The skill chooses between vibe-prototype, spec-lite, full-sdd, and production-hardening based on risk signals such as context drift, regressions, team expansion, and production intent.",
      "type": "llm-judge"
    },
    {
      "id": "has-architecture-decision-lens",
      "text": "The technical design requires major architecture choices to explain real pain solved, stage fit, one-year debt, team scaling cost, rollback path, and research evidence.",
      "type": "llm-judge"
    },
    {
      "id": "has-domain-architecture-decisions",
      "text": "The technical design requires frontend rendering/state/motion, backend deployment/API/workflow/cache, data store/index/transaction/retention, and algorithm/search/ranking/rate-limit decisions when those surfaces exist.",
      "type": "llm-judge"
    },
    {
      "id": "domain-decisions-require-live-research",
      "text": "Frontend, backend, data, and algorithm choices are framed as current official-doc/GitHub/package research tasks, not hardcoded recommendations from model memory or an old article.",
      "type": "llm-judge"
    },
    {
      "id": "prevents-stale-year-query-contamination",
      "text": "The skill requires latest/current searches to derive year terms from the current date anchor and forbids stale hardcoded years unless the query is historical, migration-related, or user-specified.",
      "type": "llm-judge"
    },
    {
      "id": "has-cache-and-index-contracts",
      "text": "The data/contracts document requires cache consistency and data access/index contracts when caching, databases, search, queues, or external state exist.",
      "type": "llm-judge"
    },
    {
      "id": "has-architecture-fitness-checks",
      "text": "The eval plan requires architecture fitness checks for selected frontend, backend, data, and algorithm decisions using concrete commands or evidence.",
      "type": "llm-judge"
    },
    {
      "id": "has-agent-prompt-packets",
      "text": "The execution plan includes prompt packets with role, context/files to read, task, constraints, output format, and validation evidence for code-agent sessions.",
      "type": "llm-judge"
    },
    {
      "id": "has-workstream-prompt-packets",
      "text": "The execution plan splits frontend, backend, data, and algorithm workstream prompt packets when those implementation surfaces exist.",
      "type": "llm-judge"
    },
    {
      "id": "has-living-spec-protocol",
      "text": "The execution plan requires upstream docs and traceability to be updated when implementation changes behavior, API, schema, permissions, security, visual contract, or eval evidence.",
      "type": "llm-judge"
    },
    {
      "id": "has-launch-ready-state",
      "text": "The pack distinguishes launch-ready from build-ready and requires security, performance, monitoring, CI/CD, environment separation, and rollback evidence before launch-ready handoff.",
      "type": "llm-judge"
    },
    {
      "id": "verification-is-evidence-based",
      "text": "The output requires each implementation task or requirement to be verified by a concrete command, state/API/file evidence, screenshot/log evidence, or explicit manual review criteria.",
      "type": "llm-judge"
    },
    {
      "id": "pressure-test-gate-is-explicit",
      "text": "The skill requires or recommends an idea pressure-test gate before Gate 1 for greenfield commercial products, with a proceed, pivot, research-needed, or pause decision.",
      "type": "llm-judge"
    },
    {
      "id": "stage-gates-are-explicit",
      "text": "The skill requires stopping for user confirmation after product brief plus reality research, and again after PRD plus requirements plus technical design.",
      "type": "llm-judge"
    },
    {
      "id": "eval-cases-avoid-self-certification",
      "text": "The skill requires reference, bad, and regression cases to declare provenance and not rely only on synthetic cases before build-ready handoff.",
      "type": "llm-judge"
    },
    {
      "id": "feature-mode-is-supported",
      "text": "The skill supports adding features to existing repositories by requiring existing-system reality, compatibility, integration, and regression planning.",
      "type": "llm-judge"
    },
    {
      "id": "brainstorming-gate-is-explicit",
      "text": "The skill requires a concise brainstorming gate before research and specification work, including mode classification, key questions, options, and assumptions.",
      "type": "llm-judge"
    }
  ],
  "golden": [
    {
      "id": "case-1",
      "input": "golden/case-1/input.txt",
      "expected": null,
      "split": "val",
      "expected_status": "pending-first-green"
    },
    {
      "id": "case-2",
      "input": "golden/case-2/input.txt",
      "expected": null,
      "split": "val",
      "expected_status": "pending-first-green"
    },
    {
      "id": "case-3",
      "input": "golden/case-3/input.txt",
      "expected": null,
      "split": "val",
      "expected_status": "pending-first-green"
    }
  ]
}
```
