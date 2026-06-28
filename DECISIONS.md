# Decisions

## Skill Shape

This is a simple skill, not a suite. The workflow has one core objective: produce a research-grounded SDD document pack for AI coding agents.

## Document Count

The skill outputs eight core documents. This is intentionally smaller than a full enterprise AIPM 22-document system but richer than a minimal `requirements/design/tasks` trio.

## Research Gate

Live research is mandatory because product markets, open-source libraries, APIs, policies, and coding-agent platforms change quickly. The skill treats model memory as insufficient for current-world claims.

## Scripts

Scripts are deterministic helpers only. They scaffold and validate the pack. The agent still performs the market research, reasoning, writing, and citations.

## Dependencies

Python standard library only, to keep the skill portable across Codex, Claude Code, Cursor, Antigravity, and other agent hosts.

## Executable Contracts

The skill makes state, navigation/actions, judges, generated artifacts, and module boundaries explicit before implementation. This keeps vibe coding from becoming prose-driven guesswork and gives code agents concrete contracts to follow and verify.
