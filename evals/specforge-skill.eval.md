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
      "id": "has-scope-and-docs-first-fields",
      "text": "The generated pack includes scope boundary, prescriptive inputs, this-pack ownership, research depth, and unverified-claims fields.",
      "type": "command",
      "cmd": "python -c \"import json, pathlib; p=pathlib.Path(r'{output}'); assert '## Scope Boundary' in (p/'00-product-brief.md').read_text(encoding='utf-8'); data=json.load(open(p/'research_ledger.json', encoding='utf-8')); assert 'research_depth' in data and 'unverified_claims' in data\""
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
