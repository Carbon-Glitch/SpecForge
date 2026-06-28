# Platform Adapters

The skill is portable because the core instructions live in `SKILL.md` and the companion instructions live in `AGENTS.md`.

## Codex

Recommended install:

```powershell
Copy-Item -Recurse specforge-skill "$env:USERPROFILE\.agents\skills\specforge-skill"
```

Use:

```text
/specforge <idea>
```

For projects, also place generated `AGENTS.md` at the repository root.

## Claude Code

Recommended install:

```powershell
Copy-Item -Recurse specforge-skill "$env:USERPROFILE\.claude\skills\specforge-skill"
```

Claude Code can invoke skills by slash command and can use the generated docs as implementation context.

## Cursor

Cursor has project-level skill/rule behavior. Install per repository:

```powershell
New-Item -ItemType Directory -Force .cursor\skills | Out-Null
Copy-Item -Recurse specforge-skill ".cursor\skills\specforge-skill"
```

If using rules instead of skills, create `.cursor/rules/sdd-docs.mdc` with:

```markdown
---
description: Generate research-grounded SDD docs before implementation.
alwaysApply: false
---
Use /specforge when the user asks for SDD, PRD, specs, implementation docs, or product-to-code planning.
```

## Antigravity

Antigravity uses `.agent/skills/` at project level:

```powershell
New-Item -ItemType Directory -Force .agent\skills | Out-Null
Copy-Item -Recurse specforge-skill ".agent\skills\specforge-skill"
```

Also keep generated `AGENTS.md` in the project root for broader compatibility.

## GitHub Copilot / VS Code

Use project-level `.github/skills/` or copy the generated `AGENTS.md` into repository-level instructions.

## Windsurf / Trae / Other Rule-Based Tools

If the tool does not read `SKILL.md`, copy the body of `SKILL.md` into its rule format and preserve:

- trigger terms
- research gate
- eight-document contract
- validation commands
- stop conditions

## Agent Handoff Pattern

After generating docs, the implementation agent should start from:

1. `07-agent-execution-plan.md`
2. `03-sdd-requirements-spec.md`
3. `04-technical-design.md`
4. `06-eval-golden-dataset.md`
5. `AGENTS.md` if exported

The agent should not start from PRD alone.
