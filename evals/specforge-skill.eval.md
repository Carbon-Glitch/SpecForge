# Eval: specforge-skill

This eval checks that the skill can scaffold and validate an eight-document SDD pack.

```json
{
  "skill": "specforge-skill",
  "run": "python scripts/run_pipeline.py --idea \"{idea}\" --out {output} --stage all --force",
  "criteria": [
    {
      "id": "valid-pack",
      "text": "The generated pack passes validate_pack.py.",
      "type": "command",
      "cmd": "python scripts/validate_pack.py {output} --stage all"
    },
    {
      "id": "has-eight-docs",
      "text": "The pack contains exactly the eight core markdown documents.",
      "type": "command",
      "cmd": "python -c \"from pathlib import Path; p=Path(r'{output}'); docs=list(p.glob('*.md')); assert len(docs)==8\""
    },
    {
      "id": "has-research-ledger",
      "text": "The pack includes a research ledger JSON artifact.",
      "type": "command",
      "cmd": "python -c \"import json, pathlib; json.load(open(pathlib.Path(r'{output}')/'research_ledger.json', encoding='utf-8'))\""
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
