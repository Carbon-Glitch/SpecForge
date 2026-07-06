# SpecForge

**From a rough product idea to research-grounded, eval-ready, agent-session-ready build specs.**

SpecForge is a cross-platform agent skill that turns a simple product concept into a research-grounded Spec-Driven Development document pack for AI coding agents.

Unlike generic spec generators, SpecForge combines live research with a Temporal Freshness Guard, GitHub open-source reuse analysis, executable engineering contracts, deterministic eval planning, architecture decision lenses, frontend/backend/data/algorithm decision matrices, and code-agent prompt packets before coding begins.

It supports both new products and feature work in existing repositories.

It is designed for Cursor, Codex, Claude Code, Antigravity, GitHub Copilot, Gemini CLI, Windsurf, Cline, Roo, Kiro, OpenCode, Goose, and other agent environments that can read `SKILL.md`, `AGENTS.md`, or project rules.

## Why SpecForge

Vibe coding works best when the agent is not forced to invent product scope, architecture, state models, evaluation criteria, and implementation order while writing code.

SpecForge creates the missing bridge:

```text
rough product idea
  -> discovery brainstorming
  -> Gate 0: idea pressure test
  -> human go / pivot / pause decision
  -> optional scope slice / docs-first indexing
  -> SDD mode decision: vibe-prototype / spec-lite / full-sdd / production-hardening
  -> Gate 1: product brief + live market and technology research
  -> human review
  -> product and behavior specs
  -> optional Gate 2.5: visual design contract
  -> human review
  -> executable engineering contracts
  -> evals, test fixtures, and regression cases
  -> coding-agent task plan and prompt packets
```

## What It Produces

SpecForge generates one preflight decision document plus eight core development documents in `sdd-docs/`.

Preflight:

- `preflight-idea-pressure-test.md` - core assumption, fatal flaws, current alternatives, first users, 2-week MVP test, and continue/pivot/pause decision

Core documents:

1. `00-product-brief.md` - clarified concept, SDD mode, users, jobs, constraints, assumptions, and open questions
2. `01-reality-research.md` - live market, competitor, official-doc, and GitHub open-source research with citations
3. `02-prd-behavior-contract.md` - PRD, behavior contract, scope, guardrails, and success metrics
4. `03-sdd-requirements-spec.md` - functional/non-functional requirements, user stories, and EARS acceptance criteria
5. `04-technical-design.md` - architecture, stack choices, architecture decision lens, frontend/backend/data/algorithm decisions, state truth model, workflows/actions, generated artifacts, and observability
6. `05-contracts-data-permissions.md` - API/data/tool contracts, permissions, cache consistency, data access/index contracts, storage, module/file boundaries, and integrations
7. `06-eval-and-test-cases.md` - deterministic judge contract, architecture fitness checks, evidence matrix, test fixtures, reference cases, bad cases, regression gates, and launch readiness checks
8. `07-agent-execution-plan.md` - coding-agent implementation plan, prompt packets, architecture workstream packets, task order, validation commands, living-spec update protocol, and AGENTS.md handoff rules

Optional:

- `08-ui-visual-design.md` - UI visual contract for design positioning, tokens, core components, page skeletons, motion, responsive/a11y checks, and UI judge rules

Support artifacts:

- `traceability_matrix.json`
- `research_ledger.json`
- `handoff_manifest.json`

## Core Principles

- **Brainstorm before specs**: clarify intent, mode, options, assumptions, and material unknowns before writing documents.
- **Pressure-test before planning**: for greenfield commercial ideas, test whether the idea deserves SDD work before generating development specs.
- **Research before architecture**: market claims, compliance claims, APIs, frameworks, and open-source choices must be checked against current sources.
- **Anchor time before searching**: record the current date/year/timezone, derive latest/current search terms from that anchor, and label sources as `fresh`, `acceptable`, `stale`, `undated`, or `blocked`.
- **Choose the right SDD depth**: use `vibe-prototype`, `spec-lite`, `full-sdd`, or `production-hardening` based on risk, not ceremony.
- **Respect existing systems**: for feature work, inspect the current codebase and preserve compatibility unless the user asks for a redesign.
- **GitHub reuse before custom build**: if a subsystem already has a suitable open-source implementation, evaluate integration, wrapping, forking, or pattern extraction before building from scratch.
- **Architecture decisions must age well**: each major choice should explain real pain solved, stage fit, one-year technical debt, team scaling cost, and rollback path.
- **Engineering choices are explicit**: frontend rendering/state/motion, backend API/workflow/cache, data store/index/transaction/retention, and algorithm/search/ranking/rate-limit decisions are researched and validated instead of improvised during coding.
- **Executable contracts before tasks**: state, workflows, actions, modules, generated files, data, and judges must be explicit before implementation starts.
- **Scope before expansion**: when only one slice should be built, mark every subsystem as `in_pack`, `referenced_only`, or `future_pack`.
- **Visual contracts before UI coding**: UI-heavy products can add `08-ui-visual-design.md`; use `$design` for durable `DESIGN.md` and `$visual-ralph` for pixel/reference implementation.
- **Agent-readable over prose-heavy**: stable headings, IDs, tables, acceptance criteria, validation commands, and traceability beat vague planning text.
- **Evidence-based verification**: every task should have a command, state/API/file check, screenshot/log evidence, or explicit manual review criterion.
- **Prompt packets over giant chats**: implementation slices should tell the code agent which role to take, which files to read, what to change, what not to change, and how to prove completion.
- **Workstream handoff**: frontend, backend, data, and algorithm tasks get separate prompt packets and evidence expectations when those surfaces exist.
- **Living specs during implementation**: behavior/API/schema/permission/security/visual/eval changes update the upstream docs before task completion.

## Quick Start

```bash
python scripts/run_pipeline.py --idea "AI meeting notes for sales teams" --out sdd-docs
python scripts/validate_pack.py sdd-docs --stage gate0
```

By default, SpecForge creates Gate 0 only: the idea pressure test. Review the verdict, then continue:

```bash
python scripts/run_pipeline.py --idea "AI meeting notes for sales teams" --out sdd-docs --stage gate1
python scripts/validate_pack.py sdd-docs --stage gate1

python scripts/run_pipeline.py --idea "AI meeting notes for sales teams" --out sdd-docs --stage gate2
python scripts/validate_pack.py sdd-docs --stage gate2

python scripts/run_pipeline.py --idea "AI meeting notes for sales teams" --out sdd-docs --stage gate2 --include-visual

python scripts/run_pipeline.py --idea "AI meeting notes for sales teams" --out sdd-docs --stage gate3
python scripts/validate_pack.py sdd-docs --stage all
```

Useful options:

```bash
python scripts/run_pipeline.py --idea "Spell Academy" --out sdd-docs --scope user-app-only --exclude factory,admin,crawler
python scripts/run_pipeline.py --idea "Add onboarding" --out sdd-docs --repo-root .
python scripts/run_pipeline.py --idea "Harden checkout flow" --out sdd-docs --sdd-mode production-hardening
python scripts/run_pipeline.py --idea "Ship compressed docs" --out sdd-docs --stage all --single-pass
```

Use `/specforge` in your coding-agent session to fill each stage with live research and final content.

## Example Output

See [`examples/ai-meeting-notes/sdd-docs/`](examples/ai-meeting-notes/sdd-docs/) for a compact completed demo pack. It shows the intended shape of the pressure-test preflight plus all eight core documents, including research ledger entries, executable contracts, case provenance, and agent handoff rules.

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

**从一句产品想法，到有真实调研、有评测规划、AI 会话可执行的开发规范包。**

SpecForge 是一个跨平台 agent skill，用来把简单的产品概念转成适合 AI coding agent 执行的规范驱动开发文档包。

它适配 Cursor、Codex、Claude Code、Antigravity、GitHub Copilot、Gemini CLI、Windsurf、Cline、Roo、Kiro、OpenCode、Goose 等能读取 `SKILL.md`、`AGENTS.md` 或项目规则的 agent 环境。

它和普通“生成 PRD/spec”的工具不同：SpecForge 会在开发前加入带时间新鲜度护栏的真实调研、GitHub 开源复用分析、可执行工程契约、确定性评测规划、架构决策透镜、前端/后端/数据/算法选型矩阵和 code agent prompt packet。

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

SpecForge 会生成 1 份前置决策文档和 8 份核心开发文档。

前置文档：

- `preflight-idea-pressure-test.md` - 核心假设、致命风险、当前替代方案、首批用户、两周 MVP 验证和继续/调整/暂停决策

核心文档：

1. `00-product-brief.md` - 产品概念、SDD 模式、用户、任务、约束、假设和开放问题
2. `01-reality-research.md` - 真实市场、竞品、官方文档、GitHub 开源方案调研和引用来源
3. `02-prd-behavior-contract.md` - PRD、行为契约、范围、护栏和成功指标
4. `03-sdd-requirements-spec.md` - 可测试需求、用户故事和 EARS 验收标准
5. `04-technical-design.md` - 架构、技术栈、架构决策透镜、前端/后端/数据/算法选型、状态真相模型、流程动作、生成物和可观测性
6. `05-contracts-data-permissions.md` - API、数据、工具、权限、缓存一致性、数据访问/索引、存储、模块文件边界和集成契约
7. `06-eval-and-test-cases.md` - 确定性评测、架构适配检查、证据矩阵、测试 fixtures、reference cases、bad cases、回归门槛和上线准备检查
8. `07-agent-execution-plan.md` - 给 code agent 执行的 prompt packets、架构工种 prompt packets、任务顺序、验证命令、living spec 更新协议和 AGENTS.md 交接规则

可选文档：

- `08-ui-visual-design.md` - UI 视觉合同，包括设计定位、tokens、核心组件、页面骨架、动效、响应式/可访问性检查和 UI judge

辅助文件：

- `traceability_matrix.json`
- `research_ledger.json`
- `handoff_manifest.json`

## 核心原则

- **先 brainstorm，再写规范**：先澄清意图、模式、方向、假设和关键未知数。
- **先压力测试，再进入规划**：从 0 到 1 的商业产品先判断是否值得进入 SDD，而不是把任何想法都包装成开发文档。
- **先选 SDD 深度，再决定文档强度**：按风险选择 `vibe-prototype`、`spec-lite`、`full-sdd` 或 `production-hardening`。
- **先联网调研，再做架构**：市场、合规、API、框架、开源项目都必须和真实世界对齐。
- **先锚定时间，再发起搜索**：记录当前日期/年份/时区，用这个锚点生成 latest/current 搜索词，并把来源标成 `fresh`、`acceptable`、`stale`、`undated` 或 `blocked`。
- **尊重现有系统**：已有项目加功能时，先读当前代码、接口、数据、测试和部署约束。
- **先看 GitHub 能否复用，再决定自研**：能集成、包装、fork、魔改或借鉴的，不默认从零造。
- **架构决策要经得住一年后复盘**：重大选择要回答真实痛点、阶段适配、技术债、团队扩张成本和回滚路径。
- **工程选型要提前说清楚**：前端渲染/状态/动效、后端 API/工作流/缓存、数据存储/索引/事务/留存、算法搜索/排序/限流等，都要先联网调研再写入 spec。
- **先定义可执行契约，再拆开发任务**：状态、流程、动作、模块、生成物、数据、评测都要提前说清楚。
- **先切范围，再防膨胀**：只做一个切片时，把子系统标成 `in_pack`、`referenced_only` 或 `future_pack`。
- **先定视觉合同，再写 UI**：消费产品、移动端、游戏、dashboard 等可加 `08-ui-visual-design.md`；需要 DESIGN.md 用 `$design`，需要像素对照实现用 `$visual-ralph`。
- **给 AI 看优先于给人写散文**：稳定标题、ID、表格、验收标准、验证命令、追踪矩阵比漂亮长文更重要。
- **完成必须有证据**：每个任务都应有命令、状态/API/文件检查、截图/日志证据或明确人工验收标准。
- **不要把所有开发塞进一个长会话**：每个实现切片要给 code agent 明确角色、上下文文件、任务、约束、输出格式和验证证据。
- **按工种交接给 AI**：前端、后端、数据、算法任务各自有 prompt packet 和验收证据，不让一个会话临时乱猜全部架构。
- **实现期间保持规范活着**：行为、API、schema、权限、安全、视觉合同或 eval 变化时，先更新上游文档和追踪关系。

## 快速使用

```bash
python scripts/run_pipeline.py --idea "面向销售团队的 AI 会议纪要产品" --out sdd-docs
python scripts/validate_pack.py sdd-docs --stage gate0
```

默认只生成 Gate 0：产品想法压力测试。确认方向后再继续：

```bash
python scripts/run_pipeline.py --idea "面向销售团队的 AI 会议纪要产品" --out sdd-docs --stage gate1
python scripts/validate_pack.py sdd-docs --stage gate1

python scripts/run_pipeline.py --idea "面向销售团队的 AI 会议纪要产品" --out sdd-docs --stage gate2
python scripts/validate_pack.py sdd-docs --stage gate2

python scripts/run_pipeline.py --idea "面向销售团队的 AI 会议纪要产品" --out sdd-docs --stage gate2 --include-visual

python scripts/run_pipeline.py --idea "面向销售团队的 AI 会议纪要产品" --out sdd-docs --stage gate3
python scripts/validate_pack.py sdd-docs --stage all
```

常用参数：

```bash
python scripts/run_pipeline.py --idea "咒语学院" --out sdd-docs --scope user-app-only --exclude factory,admin,crawler
python scripts/run_pipeline.py --idea "给现有项目加 onboarding" --out sdd-docs --repo-root .
python scripts/run_pipeline.py --idea "强化支付流程上线质量" --out sdd-docs --sdd-mode production-hardening
python scripts/run_pipeline.py --idea "一次性压缩产出文档" --out sdd-docs --stage all --single-pass
```

然后在支持 skill 的 agent 会话中使用：

```text
/specforge 做一个面向独立开发者的轻量 CRM
/specforge 为 AI 合同审查产品生成开发规范
/specforge 给现有 React 项目加权限系统，先生成 SDD 文档包
/specforge 给现有项目增加订阅支付；先分析 auth、用户模型、路由和测试
```

## 示例输出

查看 [`examples/ai-meeting-notes/sdd-docs/`](examples/ai-meeting-notes/sdd-docs/) 可以看到一个精简但完整的 demo，包括压力测试前置文档、8 份核心文档、调研台账、工程契约、用例来源标记和 agent 交接规则。

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
