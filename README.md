# SpecForge

**From a rough product idea to research-grounded, eval-ready build specs.**

SpecForge is a cross-platform agent skill that turns a simple product concept into a research-grounded Spec-Driven Development document pack for AI coding agents.

Unlike generic spec generators, SpecForge combines live research, GitHub open-source reuse analysis, executable engineering contracts, and deterministic eval planning before coding begins.

It supports both new products and feature work in existing repositories.

It is designed for Cursor, Codex, Claude Code, Antigravity, GitHub Copilot, Gemini CLI, Windsurf, Cline, Roo, Kiro, OpenCode, Goose, and other agent environments that can read `SKILL.md`, `AGENTS.md`, or project rules.

## Why SpecForge

Vibe coding works best when the agent is not forced to invent product scope, architecture, state models, evaluation criteria, and implementation order while writing code.

SpecForge creates the missing bridge:

```text
rough product idea
  -> discovery brainstorming
  -> Gate 1: product brief + live market and technology research
  -> human review
  -> product and behavior specs
  -> human review
  -> executable engineering contracts
  -> evals, test fixtures, and regression cases
  -> coding-agent task plan
```

## What It Produces

SpecForge generates eight core documents in `sdd-docs/`:

1. `00-product-brief.md` - clarified concept, users, jobs, constraints, assumptions, and open questions
2. `01-reality-research.md` - live market, competitor, official-doc, and GitHub open-source research with citations
3. `02-prd-behavior-contract.md` - PRD, behavior contract, scope, guardrails, and success metrics
4. `03-sdd-requirements-spec.md` - functional/non-functional requirements, user stories, and EARS acceptance criteria
5. `04-technical-design.md` - architecture, stack choices, state truth model, workflows/actions, generated artifacts, and observability
6. `05-contracts-data-permissions.md` - API/data/tool contracts, permissions, storage, module/file boundaries, and integrations
7. `06-eval-and-test-cases.md` - deterministic judge contract, evidence matrix, test fixtures, reference cases, bad cases, and regression gates
8. `07-agent-execution-plan.md` - coding-agent implementation plan, task order, validation commands, and AGENTS.md handoff rules

Support artifacts:

- `traceability_matrix.json`
- `research_ledger.json`
- `handoff_manifest.json`

## Core Principles

- **Brainstorm before specs**: clarify intent, mode, options, assumptions, and material unknowns before writing documents.
- **Research before architecture**: market claims, compliance claims, APIs, frameworks, and open-source choices must be checked against current sources.
- **Respect existing systems**: for feature work, inspect the current codebase and preserve compatibility unless the user asks for a redesign.
- **GitHub reuse before custom build**: if a subsystem already has a suitable open-source implementation, evaluate integration, wrapping, forking, or pattern extraction before building from scratch.
- **Executable contracts before tasks**: state, workflows, actions, modules, generated files, data, and judges must be explicit before implementation starts.
- **Agent-readable over prose-heavy**: stable headings, IDs, tables, acceptance criteria, validation commands, and traceability beat vague planning text.
- **Evidence-based verification**: every task should have a command, state/API/file check, screenshot/log evidence, or explicit manual review criterion.

## Quick Start

```bash
python scripts/run_pipeline.py --idea "AI meeting notes for sales teams" --out sdd-docs
python scripts/validate_pack.py sdd-docs --stage gate1
```

By default, SpecForge creates Gate 1 only: product brief plus reality research. Review that gate, then continue:

```bash
python scripts/run_pipeline.py --idea "AI meeting notes for sales teams" --out sdd-docs --stage gate2
python scripts/validate_pack.py sdd-docs --stage gate2

python scripts/run_pipeline.py --idea "AI meeting notes for sales teams" --out sdd-docs --stage gate3
python scripts/validate_pack.py sdd-docs --stage all
```

Use `/specforge` in your coding-agent session to fill each stage with live research and final content.

## Example Output

See [`examples/ai-meeting-notes/sdd-docs/`](examples/ai-meeting-notes/sdd-docs/) for a compact completed demo pack. It shows the intended shape of all eight documents, including research ledger entries, executable contracts, case provenance, and agent handoff rules.

Example prompts:

```text
/specforge Build a lightweight CRM for solo founders
/specforge Generate build specs for an AI legal contract reviewer
/specforge Create SDD docs before adding multi-language support to this repo
/specforge Add subscription billing to this existing repo; inspect auth, user model, routes, and tests first
```

## Install

### Codex / Universal Agent Path

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.agents\skills\specforge-skill"
```

### Claude Code

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.claude\skills\specforge-skill"
```

### Cursor

Cursor uses project-level skills:

```powershell
New-Item -ItemType Directory -Force .cursor\skills | Out-Null
Copy-Item -Recurse . ".cursor\skills\specforge-skill"
```

### Antigravity

```powershell
New-Item -ItemType Directory -Force .agent\skills | Out-Null
Copy-Item -Recurse . ".agent\skills\specforge-skill"
```

### Shell Installer

On macOS, Linux, or Git Bash:

```bash
./install.sh --platform codex
./install.sh --platform claude
./install.sh --platform cursor
./install.sh --platform antigravity
```

On Windows PowerShell:

```powershell
.\install.ps1 -Platform codex
.\install.ps1 -Platform claude
.\install.ps1 -Platform cursor
.\install.ps1 -Platform antigravity
```

## Validation

```bash
python scripts/validate_pack.py sdd-docs --stage all
python scripts/validate_pack.py sdd-docs --stage all --strict
python scripts/run_evals.py --validate
```

Skill package validation:

```bash
python scripts/run_evals.py --rollout
```

## No External Python Dependencies

The bundled scripts use only the Python standard library.

---

# SpecForge 中文说明

**从一句产品想法，到有真实调研、有评测规划、AI 可执行的开发规范包。**

SpecForge 是一个跨平台 agent skill，用来把简单的产品概念转成适合 AI coding agent 执行的规范驱动开发文档包。

它适配 Cursor、Codex、Claude Code、Antigravity、GitHub Copilot、Gemini CLI、Windsurf、Cline、Roo、Kiro、OpenCode、Goose 等能读取 `SKILL.md`、`AGENTS.md` 或项目规则的 agent 环境。

它和普通“生成 PRD/spec”的工具不同：SpecForge 会在开发前加入真实调研、GitHub 开源复用分析、可执行工程契约和确定性评测规划。

它既支持从 0 到 1 的新产品，也支持在已有代码库中加功能、改模块或做集成。

## 为什么需要 SpecForge

vibe coding 真正容易翻车的地方，不是 agent 不会写代码，而是它在写代码时还要临时猜：

- 产品范围是什么
- 哪些需求是真需求
- 技术栈是否过时
- GitHub 上有没有能复用的开源项目
- 状态应该放在哪里
- 哪些文件负责什么
- 怎么判断功能真的做完了
- 每一步应该如何验证

SpecForge 做的事情就是把这些内容提前变成 AI 可读、可追踪、可验证的开发规范。

## 生成什么

SpecForge 会生成 8 份核心文档：

1. `00-product-brief.md` - 产品概念、用户、任务、约束、假设和开放问题
2. `01-reality-research.md` - 真实市场、竞品、官方文档、GitHub 开源方案调研和引用来源
3. `02-prd-behavior-contract.md` - PRD、行为契约、范围、护栏和成功指标
4. `03-sdd-requirements-spec.md` - 可测试需求、用户故事和 EARS 验收标准
5. `04-technical-design.md` - 架构、技术栈、状态真相模型、流程动作、生成物和可观测性
6. `05-contracts-data-permissions.md` - API、数据、工具、权限、存储、模块文件边界和集成契约
7. `06-eval-and-test-cases.md` - 确定性评测、证据矩阵、测试 fixtures、reference cases、bad cases 和回归门槛
8. `07-agent-execution-plan.md` - 给 code agent 执行的任务顺序、验证命令和 AGENTS.md 交接规则

辅助文件：

- `traceability_matrix.json`
- `research_ledger.json`
- `handoff_manifest.json`

## 核心原则

- **先 brainstorm，再写规范**：先澄清意图、模式、方向、假设和关键未知数。
- **先联网调研，再做架构**：市场、合规、API、框架、开源项目都必须和真实世界对齐。
- **尊重现有系统**：已有项目加功能时，先读当前代码、接口、数据、测试和部署约束。
- **先看 GitHub 能否复用，再决定自研**：能集成、包装、fork、魔改或借鉴的，不默认从零造。
- **先定义可执行契约，再拆开发任务**：状态、流程、动作、模块、生成物、数据、评测都要提前说清楚。
- **给 AI 看优先于给人写散文**：稳定标题、ID、表格、验收标准、验证命令、追踪矩阵比漂亮长文更重要。
- **完成必须有证据**：每个任务都应有命令、状态/API/文件检查、截图/日志证据或明确人工验收标准。

## 快速使用

```bash
python scripts/run_pipeline.py --idea "面向销售团队的 AI 会议纪要产品" --out sdd-docs
python scripts/validate_pack.py sdd-docs --stage gate1
```

默认只生成 Gate 1：产品 brief 和真实调研。确认后再继续：

```bash
python scripts/run_pipeline.py --idea "面向销售团队的 AI 会议纪要产品" --out sdd-docs --stage gate2
python scripts/validate_pack.py sdd-docs --stage gate2

python scripts/run_pipeline.py --idea "面向销售团队的 AI 会议纪要产品" --out sdd-docs --stage gate3
python scripts/validate_pack.py sdd-docs --stage all
```

然后在支持 skill 的 agent 会话中使用：

```text
/specforge 做一个面向独立开发者的轻量 CRM
/specforge 为 AI 合同审查产品生成开发规范
/specforge 给现有 React 项目加权限系统，先生成 SDD 文档包
/specforge 给现有项目增加订阅支付；先分析 auth、用户模型、路由和测试
```

## 示例输出

查看 [`examples/ai-meeting-notes/sdd-docs/`](examples/ai-meeting-notes/sdd-docs/) 可以看到一个精简但完整的 8 文档 demo，包括调研台账、工程契约、用例来源标记和 agent 交接规则。

## 安装

### Codex / 通用 agent 路径

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.agents\skills\specforge-skill"
```

### Claude Code

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.claude\skills\specforge-skill"
```

### Cursor

```powershell
New-Item -ItemType Directory -Force .cursor\skills | Out-Null
Copy-Item -Recurse . ".cursor\skills\specforge-skill"
```

### Antigravity

```powershell
New-Item -ItemType Directory -Force .agent\skills | Out-Null
Copy-Item -Recurse . ".agent\skills\specforge-skill"
```

## 验证

```bash
python scripts/validate_pack.py sdd-docs --stage all
python scripts/validate_pack.py sdd-docs --stage all --strict
python scripts/run_evals.py --validate
python scripts/run_evals.py --rollout
```

## 依赖

内置脚本只使用 Python 标准库，不需要额外 Python 依赖。
