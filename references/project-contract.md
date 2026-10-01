# project-contract.md — 项目适配字段契约（Generic V0.2）

> 主 Skill 只消费以下十个字段；每个项目一个 adapter（`adapters/<project>/adapter.md`）负责把该项目的事实源翻译成这些字段。adapter 未提供的字段=项目暂无此事实，对应产物按「无数据」规则处理（结构化展示/如实声明 UNVERIFIED），禁止编造。

| 字段 | 语义 | 类型/形态 |
|---|---|---|
| `project_roots[]` | 参与展示的项目根目录清单（只读取证范围） | `[{path, root_type, notes}]`；root_type ∈ {code, docs, knowledge-base, design, mixed} |
| `facts_source` | 事实权威来源：已有预核事实文件的路径清单；`preverified=true` 时 F01 可跳过，否则 F01 先行取证 | `{preverified: bool, files[], private_files[]}` |
| `public_narrative` | 对外叙事唯一输入（定位/价值/域介绍/能力/案例/限制/可公开性） | 单文件；面向外部读者、无内部痕迹 |
| `architecture_spec` | 架构图事实：节点/边/层级 + 「不存在的边」禁令 | `{nodes[], edges[], forbidden_edges[], legend}` |
| `workflow_spec` | 流程图事实：链路步骤 | `{chains[{name, steps[]}], boundary_notes}` |
| `metrics` | 可展示数字（只收有证据的数字；无则 `[]` → 结构化展示） | `[{label, value, evidence, as_of}]` |
| `demo_scenario` | 演示素材的脚本素材与获批命令子集 | `{storyboard, approved_commands[]}` 或 `{status: NOT_AVAILABLE}` |
| `publication_policy` | 发布授权与导出策略 | `{authorization: NOT_AUTHORIZED\|APPROVED, export_layout, review_axes[], source_release}` |
| `source_release` | **代码项目必填**：源码是否随包 + 可部署验收 | `{include_code: bool, entry_points[], excluded[], fresh_clone_verify: {deps_cmd, run_cmd, check_cmd}}`；硬规则见下节 |
| `domain_profiles[]` | 领域/模块画像清单（对外命名） | `[{name, summary}]` |
| `run_ledger` | 本次 run 的目录约定 | `{dir: usage/<run-id>}` |

## 源码发布硬规则（代码项目）

`project_roots` 含 code/mixed 且存在可运行入口时：`include_code` 必须 `true`，导出树必须包含 entry_points 全部文件与真实依赖清单；**READY_FOR_APPROVAL 前，必须在全新 clone 的目录上跑通 `fresh_clone_verify` 全链（装依赖 → 启动检查 → 测试/验收命令）**，实测输出写进 trace——README Quick Start 引用的每个文件、每条命令都必须在包内存在且被这样验证过。纯知识/纯设计项目可 `include_code: false` 并如实声明（如「实现未编写」）。

## Leak Check 基线（所有项目通用禁词）

凭据、私人信息、本机绝对路径、内部审计内容与未获批准的项目事实不得进入公开成品；对外称「项目维护者」。
