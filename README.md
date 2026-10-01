# GitHub Project Showcase

一个面向 Agent 的 GitHub 项目展示编排 Skill：分析项目事实，按需求路由专业子 Skill，生成 README、架构图、流程图、视觉、Demo、安全审查与发布包，并对代码项目执行 fresh-clone 可部署验证。

```text
Status: Generic V0.2 Preview
Design: Verified
Usage: Verified on 3 project shapes
Generated code-project deployability: Verified (one recorded case)
Self-contained child-skill bundle: In Progress
Remote publish backend: In Progress
```

这是产品结构预览。子 Skill 尚未随包，clone 本仓后不能独立运行全部流程。

## 为什么需要它

普通 Agent 整理项目时，容易只总结 README、画出脱离事实的图、编造数字、泄漏秘密、只交文档而漏掉源码，或把 push 成功当成发布验收。本 Skill 用项目契约、真实子能力调用、产物验证和发布安全闸处理这些问题。

## 架构

```mermaid
flowchart TD
  A[Project Adapter] --> B[Main Orchestrator]
  B --> C[F01-F08 按需求路由]
  C --> D[Child Skills]
  D --> E[Validation]
  E --> F[F09 Safety Gate]
  F -->|PASS 与发布授权| G[F10 Delivery]
  F -->|BLOCK| H[STOP]
```

## 十个阶段与当前选型

| Phase | 职责 | Primary / Compose | Fallback |
|---|---|---|---|
| F01 | 事实取证 | codebase-knowledge-builder | wtfismyrepo |
| F02 | 叙事 | humanizer | writing-clearly-and-concisely |
| F03 | 架构 | c4-architecture + mermaid-skill | design-doc-mermaid (license blocked) |
| F04 | 流程 | ux-flow-designer | pretty-mermaid |
| F05 | 数据 | strategy-consulting-visualization | tufte-claude-skill |
| F06 | 视觉 | snap-x + og-image-design QA | og-image-generator |
| F07 | 演示 | video-editing / ffmpeg | record |
| F08 | 文档 | readme-skill | good-readme |
| F09 | 安全 | secret-scanner | polish-repo |
| F10 | 交付 | github-release | skill-creator |

选型来自既有本地验证记录；每个子能力的历史验证范围不同，不能据此声称所有 fallback 都已完成真实切换。完整运行绑定仍在产品化，见 [运行状态](manifests/preview-runtime-status.md)。

## 项目适配

从 [SKILL.md](SKILL.md) 和 [项目契约](references/project-contract.md) 开始。Adapter 把事实来源、公开叙事、架构、流程、指标、演示和发布策略交给编排器。缺数据就跳过或如实声明，不能编造。用 [模板](adapters/template/adapter.md) 填写你自己的输入。

- [知识库示例](adapters/examples/knowledge-base/adapter.md)：多知识域与叙事边界。
- [设计示例](adapters/examples/dy/adapter.md)：设计不能表述为已实现；无数据、无 demo 时不路由相应阶段。
- [代码示例](adapters/examples/local-codebase-mcp/adapter.md)：源码随包、排除凭据、独立安装与测试。

示例已重新写成可移植模板，原项目源码和私有事实未包含。

## 验证证据

截至 2026-10-01，维护者本地记录验证了三种项目形态：知识库（含 STOP）、纯设计（含无指标/无 demo 路由）、真实 MCP 工程。MCP 生成包在全新本地 clone 中安装 runtime 依赖、通过 `server.py --check`，另装 `pytest==9.1.1` 后 **326 tests passed**；6 个需要真实语言服务器的测试被排除。

这是对一个生成项目包的历史实测，不是本 Skill 仓库已完成 fresh-clone E2E。原始私有 trace 不随本 Preview 发布。

## 当前缺口

- 子 Skill vendor、依赖闭包、文件 hash 与逐文件许可证治理仍在进行。
- F03 的 design-doc-mermaid fallback 缺少明确许可证，禁止复制入包。
- GitHub Connector 优先、gh fallback 的后端适配与远端回读仍待产品化。
- 外部 Python / Node / ffmpeg 等需要 doctor 探测；本仓不含这些二进制。
- 运行依赖与验证依赖尚待在契约中拆分。

见 [路线图](docs/roadmap.md)、[路由](docs/routing.md) 和 [安全边界](docs/security.md)。

## 许可

本 Preview 未包含第三方原始 Skill 文件；子 Skill 各自遵循上游许可证。本项目自有内容采用维护者选定的 [MIT License](LICENSE)。该许可证不覆盖未随包的第三方子 Skill。
