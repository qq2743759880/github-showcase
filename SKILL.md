---
name: github-project-showcase
description: 通用 GitHub 项目展示编排 Skill——按 project-contract 消费任一项目的适配输入，路由 phase 至已冻结子能力（PRIMARY/FALLBACK），完成事实取证、叙事、图、演示、范围审查与本地导出包。本 Skill 只做编排；专业能力全部在子 Skill 实体。
---

# github-project-showcase · 主编排 Skill（Generic V0.2）

> status: ACTIVE · 2026-10-01 · V0.2 泛化：主 Skill 零项目硬编码；项目差异全部进 adapter（`adapters/examples/<project>/adapter.md` 或自行填写的 adapter）。
> 宿主适配：无原生 Skill API/斜杠命令——真实接法 = 显式加载本目录与 adapter/vendor 实体后执行；CLI/MCP 按 binding。缺能力=BLOCKED，不虚构。

## 1. Project Contract（先读）

任何 run 开始：**选定 adapter**（用户指名项目 → `adapters/` 下自声明该项目的 adapter），读 `references/project-contract.md` 的字段语义，然后读该 adapter 的字段填充。十项契约字段：`project_roots[] / facts_source / public_narrative / architecture_spec / workflow_spec / metrics / demo_scenario / publication_policy / domain_profiles / run_ledger`。adapter 未提供的字段 = 该项目暂无此事实，对应产物按「无数据」规则处理（结构化展示/如实声明），**禁止编造**。

## 2. 数据流边界

- 公开成品只准消费 adapter 的 `public_narrative` 与已批准 assets；私有事实源（`facts_source` 私有部分）仅供内部核验。
- 成品进 public-export 前必须过 Narrative Leak Check（`docs/security.md`；P0/P1 必修）。
- 对外措辞用「项目维护者」，不用「Owner」。

## 3. 需求解析 → phase 路由

| 触发 | phase | 消费 binding | 输入（来自 adapter 契约字段） |
|---|---|---|---|
| 项目边界/事实缺失 | F01 取证 | references/bindings.md | `project_roots[]`（只读） |
| 项目叙事/介绍 | F02 | references/bindings.md | `public_narrative` |
| 架构图 | F03 | references/bindings.md | `architecture_spec` |
| 流程图 | F04 | references/bindings.md | `workflow_spec` |
| 数据/矩阵图 | F05 | references/bindings.md | `metrics`（无量化数据→结构化展示） |
| 首屏视觉 | F06 | references/bindings.md | 视觉 brief（自 `public_narrative`+domain_profiles） |
| 演示素材 | F07 | references/bindings.md | `demo_scenario` |
| README/文档 | F08 | references/bindings.md | `public_narrative` + assets |
| 公开范围审查 | F09 | references/bindings.md | `publication_policy` + 待审目录 fixture |
| 打包/发布 | F10 | references/bindings.md | 隔离 staging（未授权=只 dry-run） |

规则：按用户需求路由 phase 集合（无预核事实源的项目 **F01 必须先行**，其产出回填 facts/narrative 字段）；多 phase 串联共用同一事实输入，显式文件传递；每 run 独立目录 `usage/<run-id>/`（route-plan/逐 phase trace/final-verdict/output）。

## 4. 执行契约

1. invoke 前 dependencyCheck（缺位=BLOCKED 上报，不现场全局安装；确需安装走工程隔离纪律）。
2. invocation 只用 binding 标注的真实形态（显式加载 vendored 实体 / CLI / MCP）。
3. validate：逐产物跑 successCheck；验不过=不产出。
4. fallback/stop：PRIMARY 失败且命中 fallbackCondition → 切 FALLBACK 同验收；PRIMARY 与 FALLBACK 同受环境阻断 → 按 failurePolicy 停止上报；**secret/privacy/license/authorization 拒绝不得绕过**——F09 判 BLOCK 的内容，F10 对其 STOP。
5. 留痕：每次真实调用写 trace（输入/命令形态/产物/验收）。

## 5. Publish gate

`publication_policy.authorization != APPROVED` 时零远程写入，只到本地 private-review/public-export 与 READY_FOR_APPROVAL；批准并执行发布后，远端 read-back 全核过才称 PUBLISHED_VERIFIED。

## 6. Preview 状态

本包只含主编排与可移植示例，未含第三方子 Skill。运行状态唯一来源为 `manifests/preview-runtime-status.md`；产品绑定索引为 `references/bindings.md`。子实体不在场时 BLOCKED，不依赖作者研究目录或历史会话。
