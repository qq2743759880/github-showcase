# project-contract.md — 项目适配字段契约（vNext）

> 主 Skill 只消费以下字段；每个项目一个 adapter（`adapters/examples/<project>/adapter.md` 或自建 adapter）负责把该项目的事实源翻译成这些字段。adapter 未提供的字段=项目暂无此事实，对应产物按「无数据」规则处理（结构化展示/如实声明 UNVERIFIED），禁止编造。

## 默认公开阅读方式：单页读完

所有完整 Showcase 默认遵循 [单页阅读规范](single-page-showcase.md)，不只适用于本项目或 Agent Skill。保留用户已认可的大白话介绍和视觉；基本介绍之后放简洁页内索引，项目说明、工作流程、能力、安装配置、首次使用、架构说明、恢复与安全边界均在同一 README 内完整呈现，按实际项目适用范围取舍。用户明确要求其他阅读结构时才覆盖该默认。

索引的说明入口只用同页 `#fragment`。不得用 `docs/*.md`、GitHub blob 链接或 Pages 链接代替核心说明；“本页有标题，内容请点另一页”也不算完成。下载包、许可证原件、来源引用和可选交互图可以保留链接，但不成为理解和首用的前提。静态架构/流程预览必须直接嵌在本页，相关解释相邻。单页是阅读面，不是把所有源码、日志、私有证据放进一个文件。

这是 F02/F03/F04/F06/F08 的共同出稿要求。原生子 Skill 不改字节；由本项目 reader profile 显式覆盖通用模板中不适用的分章节跳转习惯。详见规范中的结构验收和同页独立阅读验收。

| 字段 | 语义 | 类型/形态 |
|---|---|---|
| `project_roots[]` | 参与展示的项目根目录清单（只读取证范围） | `[{path, root_type, notes}]`；root_type ∈ {code, docs, knowledge-base, design, mixed} |
| `facts_source` | 事实权威来源：已有预核事实文件的路径清单；`preverified=true` 时 F01 可跳过，否则 F01 先行取证 | `{preverified: bool, files[], private_files[]}` |
| `public_narrative` | 对外叙事唯一输入（定位/价值/域介绍/能力/案例/限制/可公开性） | 单文件；面向外部读者、无内部痕迹 |
| `architecture_spec` | 架构图事实：节点/边/层级 + 「不存在的边」禁令 | `{nodes[], edges[], forbidden_edges[], legend}` |
| `workflow_spec` | 流程图事实：链路步骤 | `{chains[{name, steps[]}], boundary_notes}` |
| `archify_provenance` | F03/F04 取证模式意图；无该字段时本地内容绑定，不因缺 origin 取消图 | `{repository_evidence_required: bool, origin_approved: bool, link_mode: local-only\|web}`；route 返回 `provenance_mode`，详见 workflows/archify.md |
| `metrics` | 可展示数字（只收有证据的数字；无则 `[]` → 结构化展示） | `[{label, value, evidence, as_of}]` |
| `demo_scenario` | 演示素材的脚本素材与获批命令子集 | `{storyboard, approved_commands[]}` 或 `{status: NOT_AVAILABLE}` |
| `publication_policy` | 发布授权与导出策略 | `{authorization: NOT_AUTHORIZED\|APPROVED, export_layout, review_axes[]}` |
| `source_release` | **代码项目必填**：源码是否随包 + 可部署验收 | `{include_code: bool, entry_points[], excluded[], fresh_clone_verify: {runtime_deps_cmd, verification_deps_cmd, setup_steps[], run_cmd, check_cmd}}`；硬规则见下节 |
| `domain_profiles[]` | 领域/模块画像清单（对外命名） | `[{name, summary}]` |
| `run_ledger` | 本次 run 的目录约定 | `{dir: <approved-run-root>}` |

## 源码发布硬规则（代码项目）

`project_roots` 含 code/mixed 且存在可运行入口时：`include_code` 必须 `true`，导出树必须包含 entry_points 全部文件与真实依赖清单；**READY_FOR_APPROVAL 前，必须在全新 clone 的目录上跑通 `fresh_clone_verify` 全链（运行依赖安装 → 配置准备 → 启动检查 → 验证依赖安装 → 测试/验收命令）**，实测输出写进 trace——README Quick Start 引用的每个文件、每条命令都必须在包内存在且被这样验证过。纯知识/纯设计项目可 `include_code: false` 并如实声明（如「实现未编写」）。

## Leak Check 基线（所有项目通用禁词）

凭据、私人信息、本机绝对路径、内部审计内容与未获批准的项目事实不得进入公开成品；对外称「项目维护者」。

Release policy 的 `secret_fixture_exemptions` 仅允许经过确认、绑定具体 finding 的 synthetic 安全负例，详见 workflows/delivery.md。它不改变 vendor scanner，也不豁免整个测试目录；真实高风险 secret 仍 BLOCK。分解图则声明 `archify_decomposition`，所有 required views 联合覆盖完整语义、分别通过 native gate。各必需视图的静态预览和说明直接在 README 消费，HTML 与可编辑源作为增强入口保留；任一原生交付失败仍需修复该 phase。

## 运行依赖与验证依赖

`source_release` 是顶层字段。代码与 mixed 项目必须显式填写 `fresh_clone_verify.runtime_deps_cmd`、`verification_deps_cmd`、`run_cmd`、`check_cmd`。没有额外测试依赖时，`verification_deps_cmd` 可为空字符串；缺字段不等于没有依赖。配置复制与路径填写写入 `setup_steps[]`，不把作者私有配置随包。旧 `deps_cmd` 不再作为验收输入。

示例：运行安装 `python -m pip install -r requirements.txt`；验证安装 `python -m pip install pytest==9.1.1`。测试依赖不能为了方便塞进生产依赖。命令必须由用户项目的运行环境与源码证据确定；示例不是对任意项目的执行授权。

校验：`python scripts/validate-adapter.py <adapter.json>`（纯标准库），或 Markdown YAML adapter（额外需要 PyYAML）。校验只检查契约，不执行其中命令，不能代替 fresh-clone 运行证据。

## Asset Consumption Contract（消费门）

被路由且 PASS 的 visual phase（F03 architecture / F04 workflow / F05 chart-capability / F06 hero-visual / F07 demo）的 validated output 必须登记消费台账。例如：

```yaml
phase: F03
producer: c4-architecture + archify
artifact: docs/diagrams/architecture.svg
validation: native semantic QA, delivery and actual image inspection
final_consumer: README 架构节
consumed_where: "README.md#系统架构：图片直接嵌入，关系解释紧邻；HTML/JSON 为可选增强入口"
```

现有 `scripts/release-gate.py` 自动检查无引用视觉资产（`ORPHAN_ASSET_FAIL`）和缺失路由资产（`ROUTED_ASSET_MISSING`）。这些检查仍需通过，但“经 README 链接到 docs 后可达”不等于“在首页已被读者看到”。默认单页规范额外要求必需静态预览直接嵌在 README，核心说明在同页，不只在二跳文档出现。F08 需要证明 F02 narrative、F03/F04/F05（若路由）、F06 hero、F07（若路由）、F09 boundary 真正进入当前读者页面。

## Reader Comprehension Gate（读者理解门）

Release Candidate 必须经独立 Fresh Reviewer 验收：Reviewer **只能读取最终 README 及其中直接呈现的图**（禁读源码/SKILL/private trace/历史 prompt/链接说明页），必须仅凭本页准确回答五题：①这个项目是什么 ②解决什么问题 ③用户输入什么 ④用户最后得到什么 ⑤它与该项目最接近的常见替代方式有什么区别。展示本 Skill 时，第⑤题对照普通 README generator；其他项目使用自己的真实语境。任一题无 README 原文依据 → `READER_COMPREHENSION_FAIL`，不得进入 F10 READY_FOR_APPROVAL。收据使用 `scripts/evidence.py` 的现有 JSON schema，绑定最终 README hash 与五个原文引用；关键词和旧版 PASS 不再接受。

同时检查安装条件、首次操作、架构/流程和安全恢复边界能否从同页说清。结果附在现有审阅记录，不另设反复等待 Owner 的审批轮。目录结构、锚点唯一/存在、必需预览和章节可见性由实际结构检查承担；标题存在不能替代内容完整性判断。尚未接入机器检查的项目不得仅凭文档规则标成自动通过。

## User Surface / Maintainer Surface 分层

Agent Skill 额外声明 `project_form: agent-skill`，按 [发布分层](distribution-surfaces.md) 提供完整 Runtime / Showcase / Publication 文件清单、私有构建证据和当前最小包验收。按 [Agent Skill README Profile](agent-skill-readme-profile.md) 组织真实用户路径。简介后先放页内索引；流程为主要价值时，静态预览和解释在随后正文优先出现，早于安装/任务示例。SPDX 许可证标识不可本地化。可重建资产不因此自动获得公开或运行依赖身份。

README 第一屏（首个 `## ` 二级标题之前）只允许：产品价值 / 输入 / 输出 / Hero / 一项核心真实证据。禁止第一屏出现：hash、fixture、vendor entity 数、npm 版本、Puppeteer、内部 run ID、audit 细节。维护者信息留在相应 developer docs 或私有证据面；不是“单页读完”的用户说明内容。release-gate 以 `READER_SURFACE_FAIL` 自动拦截。

## Self-Dogfood Gate（自展示门）

`github-showcase` 自身 Stable Release 前，必须存在 `SELF_DOGFOOD_PASS` 收据：使用当前待发布版本的 Skill 展示 Skill 自己，并经过同一条链（route → visual generation → asset consumption → README composition → F09 → comprehension gate）。无收据不得 Stable Release（release-gate `--require-self-dogfood` 强制）。

## vNext evidence schema

运行证据采用 `scripts/evidence.py` 与 `references/workflows/delivery.md` 的 JSON schema。理解门绑定最终 README；fresh clone 绑定最终导出树与逐步命令日志；自展示绑定当前产品与导出树。旧关键词收据不再有效。路由用 `scripts/route-plan.py` 与单 phase binding，原 PRIMARY/FALLBACK 结构已退出。源码和安全门保持。

## Execution, redistribution and release identity

Agent Skill policy declares `distribution_surface.execution` (files actually loaded by the Agent), `redistribution` (complete install closure including required legal files), `runtime` (compatibility alias for the same packaged redistribution list), `showcase`, `publication`, and empty public `evidence`. Execution must be a subset of redistribution; a legal file is not an execution dependency merely because it ships. Minimal runtime manifests and receipts preserve both lists. Single-page reading does not collapse these file/distribution surfaces.

A versioned download declares `release_artifact: {version, url, default_branch}`. Its HTTPS URL must use that exact release tag or a complete commit, including repository-hosted fallback ZIPs; default branches, HEAD and latest fail. Verify the actual ref and downloaded bytes independently before published status. Never move an existing version tag to a later showcase-only update.

`license_identifier: {identifier, source, documents}` binds the exact authoritative entry identifier and license-facing document paths. IDs/expressions are preserved verbatim in code formatting; translation affects surrounding prose only. Source mismatch or identifier expansion/substitution fails. Third-party Showcase legal files live under `licenses/showcase/<producer>/`; the original Skill legal paths are preserved.

## Public Publication Surface

`distribution_surface.publication` declares public CI/release/deployment files separately from reader `showcase` and install `redistribution` / `runtime`. Their disjoint union is the exhaustive public allowlist; public `evidence` remains empty. `publication_purposes: {relative_path: nonempty_purpose}` must exactly cover Publication. Conventional `.github/workflows/*` and direct `.github/*.json` cannot appear in Runtime or Showcase. See [the authoritative surface and safety contract](distribution-surfaces.md#publication-contract-and-safety).

`publication_authorization: APPROVED` is separately required for any workflow root/job write permission. Workflows require explicit static permissions and the existing optional PyYAML parser; no inferred defaults. Credentials, private machine paths, receipts and logs are prohibited. Existing secret/privacy and immutable artifact checks apply to these files. JSON `release_tag` / `artifact_url` must match policy identity. Neither a purpose nor local gate PASS replaces remote authorization/readback. Packaging does not put Publication in the installed Skill.
