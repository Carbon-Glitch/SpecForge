#!/usr/bin/env python3
"""Validate the bundled eval specification.

This lightweight runner validates the JSON block inside the eval markdown file.
It can also score a generated output directory by running validate_pack.py.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVAL_PATH = ROOT / "evals" / "specforge-skill.eval.md"


def load_eval_spec() -> dict[str, Any]:
    """Load the fenced JSON eval specification."""
    text = EVAL_PATH.read_text(encoding="utf-8")
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if not match:
        raise ValueError("eval markdown does not contain a fenced JSON block")
    return json.loads(match.group(1))


def validate_spec(spec: dict[str, Any]) -> list[str]:
    """Return validation errors for an eval spec."""
    errors: list[str] = []
    if spec.get("skill") != "specforge-skill":
        errors.append("skill field must be specforge-skill")
    criteria = spec.get("criteria")
    if not isinstance(criteria, list) or len(criteria) < 3:
        errors.append("criteria must contain at least 3 checks")
    for criterion in criteria or []:
        if criterion.get("type") not in {"command", "llm-judge"}:
            errors.append(f"invalid criterion type: {criterion}")
        if not criterion.get("id") or not criterion.get("text"):
            errors.append(f"criterion missing id/text: {criterion}")
    golden = spec.get("golden")
    if not isinstance(golden, list) or len(golden) < 3:
        errors.append("golden must contain at least 3 cases")
    for case in golden or []:
        if case.get("split") != "val":
            errors.append(f"golden case split must be val: {case}")
        input_path = ROOT / "evals" / str(case.get("input", ""))
        if not input_path.exists():
            errors.append(f"golden input missing: {case.get('input')}")
    run = spec.get("run", "")
    if "{output}" not in run:
        errors.append("run command must include {output}")
    return errors


def run_rollout(spec: dict[str, Any]) -> int:
    """Run the deterministic scaffold against golden cases."""
    run_template = spec["run"]
    output_root = ROOT / "evals" / ".rollout"
    output_root.mkdir(parents=True, exist_ok=True)
    exit_code = 0
    for case in spec["golden"]:
        input_path = ROOT / "evals" / case["input"]
        idea = input_path.read_text(encoding="utf-8").strip()
        output_path = output_root / case["id"]
        command = run_template.replace("{input}", str(input_path)).replace("{output}", str(output_path))
        command = command.replace("{idea}", idea.replace('"', "'"))
        result = subprocess.run(command, cwd=ROOT, shell=True)
        if result.returncode != 0:
            print(f"rollout failed for {case['id']}: {result.returncode}")
            exit_code = result.returncode
            continue
        validator = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_pack.py"), str(output_path)],
            cwd=ROOT,
        )
        if validator.returncode != 0:
            exit_code = validator.returncode
    return exit_code


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Validate or rollout eval spec.")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--rollout", action="store_true")
    args = parser.parse_args()

    spec = load_eval_spec()
    errors = validate_spec(spec)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    if args.rollout:
        sys.exit(run_rollout(spec))
    print("VALID")


if __name__ == "__main__":
    main()
