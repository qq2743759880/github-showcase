---
name: github-project-showcase
description: 通用 GitHub 项目展示编排 Skill——按 project-contract 消费任一项目的适配输入，路由 phase 至已冻结子能力（PRIMARY/FALLBACK），完成事实取证、叙事、图、演示、范围审查与本地导出包。本 Skill 只做编排；专业能力全部在子 Skill 实体。
---

# github-project-showcase · 主编排 Skill（Generic V0.2）

> status: ACTIVE · 2026-10-01 · V0.2 泛化：主 Skill 零项目硬编码；项目差异全部进 adapter（`adapters/examples/<project>/adapter.md` 或自行填写的 adapter）。
> 宿主适配：无原生 Skill API/斜杠命令——真实接法 = 显式加载本目录与 adapter/vendor 实体后执行；CLI/MCP 按 binding。缺能力=BLOCKED，不虚构。

## 1. Project Contract（先读）

任何 run 开始：**选定 adapter**（优先读用户提供的 adapter；新项目从 `adapters/template/adapter.md` 创建当前 run 的 adapter，路径全部以用户给定项目为根），读 `references/project-contract.md` 的字段语义，然后读该 adapter 的字段填充。基础契约字段：`project_roots[] / facts_source / public_narrative / architecture_spec / workflow_spec / metrics / demo_scenario / publication_policy / domain_profiles / run_ledger`。adapter 未提供的字段 = 该项目暂无此事实，对应产物按「无数据」规则处理（结构化展示/如实声明），**禁止编造**。

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

整项目「GitHub 展示包」默认路由 F01/F02/F03/F04/F06/F08/F09/F10；F05 仅在指标有证据时路由，F07 仅在存在获批演示素材时路由。局部请求按需求缩小集合。

规则：按用户需求路由 phase 集合（无预核事实源的项目 **F01 必须先行**，其产出回填 facts/narrative 字段）；多 phase 串联共用同一事实输入，显式文件传递；每 run 独立目录 `usage/<run-id>/`（route-plan/逐 phase trace/final-verdict/output）。

## 4. 执行契约

1. invoke 前 dependencyCheck（缺位=BLOCKED 上报，不现场全局安装；确需安装走工程隔离纪律）。
2. invocation 只用 binding 标注的真实形态（显式加载 vendored 实体 / CLI / MCP）。
3. validate：逐产物跑 successCheck；验不过=不产出。
4. fallback/stop：PRIMARY 失败且命中 fallbackCondition → 切 FALLBACK 同验收；PRIMARY 与 FALLBACK 同受环境阻断 → 按 failurePolicy 停止上报；**secret/privacy/license/authorization 拒绝不得绕过**——F09 判 BLOCK 的内容，F10 对其 STOP。
5. 留痕：每次真实调用写 trace（输入/命令形态/产物/验收）。

## 5. Publish gate

`publication_policy.authorization != APPROVED` 时零远程写入，只到本地 private-review/public-export 与 READY_FOR_APPROVAL；批准并执行发布后，远端 read-back 全核过才称 PUBLISHED_VERIFIED。

## 6. 运行入口与状态

本包包含 20 个固定版本子实体。调用权威为 `references/bindings.json`；先读该 phase 的 binding，再真实加载 primary.entry 及其资源。文件完整性用 `python scripts/verify-vendors.py`；环境用 `python scripts/doctor.py`；状态见 `manifests/preview-runtime-status.md`。没有历史会话也应能完成路由，不能依赖作者研究目录。缺子实体、依赖或产物验收时 BLOCKED。

代码项目另外必填顶层 `source_release`，运行与验证依赖分开。F10 三步为 Package、Publish Backend、Remote Verification，见 `references/publish-backends.md`。

F06 必须调用 `node scripts/snap-x.mjs check <design.mjs>` 和 `node scripts/snap-x.mjs render <design.mjs> --out <approved-output>`，wrapper 固定 CLI 版本与项目内缓存。先 `npm ci` 安装外部渲染依赖；不要执行上游示例里的未钉版 npx。方法学文件保留原文，执行配置以本条与 binding 为准。F10 普通项目使用 scripts/package-project.py；只有 Skill 产物使用 scripts/package-release.py 调用 skill-creator，不触发可选描述优化或其他 Agent 会话消息。F08 整项目展示包采用已记录的 create_export：源 README 只读，在批准的 run 目录创建新版 README；目标已存在时仍需明确处理模式。

F03 C4 渲染：根目录 `npm ci --ignore-scripts`，再 `node scripts/render-c4.mjs -i <diagram.mmd> -o <output.svg>`。wrapper 优先使用 `PUPPETEER_EXECUTABLE_PATH` 或已有 Chrome/Edge（host runtime），所有临时 profile 留在 checkout/.cache。没有浏览器时，设置 `PUPPETEER_CACHE_DIR=<checkout>/.cache/puppeteer` 后执行 `node node_modules/puppeteer/install.mjs` 下载项目内浏览器。必须检查真实渲染输出；沙箱进程启动超时可按授权申请工具自动审查，不能直接称 PASS。F04 fallback 按 binding 在 vendor/pretty-mermaid 内安装固定 lock 的依赖；所有 npm cache 放 checkout/.cache。Node 要求 >=24。
