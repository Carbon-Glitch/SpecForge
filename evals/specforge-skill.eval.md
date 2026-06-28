# Eval: specforge-skill

This eval checks that the skill can scaffold and validate an eight-document SDD pack.

```json
{
  "skill": "specforge-skill",
  "run": "python scripts/run_pipeline.py --idea \"{idea}\" --out {output} --force",
  "criteria": [
    {
      "id": "valid-pack",
      "text": "The generated pack passes validate_pack.py.",
      "type": "command",
      "cmd": "python scripts/validate_pack.py {output}"
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
