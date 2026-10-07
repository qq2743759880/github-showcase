<p align="center">
  <img src="./assets/hero.png" width="640" alt="github-showcase：从事实、原方法到经过验证的交付">
</p>

<h1 align="center">github-showcase</h1>

<p align="center">让 Agent 从项目事实出发，完成 README、适用的视觉资产和可验证的源码交付。</p>

## 适用场景

github-showcase 是一个供 Agent 加载的 Skill，适合已有项目准备公开展示、重写事实准确的 README，或整理源码发布包。它解决文案、图像与实际实现脱节，以及本地看似完成却缺少交付验证的问题。

你提供项目目录、已有事实、目标读者和可公开范围。Agent 先取证，再选择需要的原生方法，最后交付 README、适用的架构与流程图、项目主视觉、干净源码包及私有检查记录。

## 工作流程

![从事实到源码包的完整流程，包含缺失事实、修复和安全拒绝分支](./docs/diagrams/showcase.svg)

[打开交互流程图](https://qq2743759880.github.io/github-showcase/diagrams/showcase.html) · [下载 HTML 在本地打开](./docs/diagrams/showcase.html) · [编辑图的源数据](./docs/diagrams/showcase.json)

流程是：取证 → 选择能力 → 编写 → 执行原生方法 → 审查 → 检查 → 打包。检查失败需要修复后重新检查，不能伪造通过；真实密钥或越权内容不能进入公开包。

## 能力概览

| 你需要的结果 | 实际做法与边界 |
|---|---|
| 有依据的 README | 从源码与已批准事实建立账本，保持可执行的首次使用路径 |
| 读得懂的架构与流程 | 软件架构使用 C4；Archify 交付可交互 HTML、可编辑数据和静态预览 |
| 一张有用的项目主视觉 | Snap-X 完成调查、设计、检查、渲染和实际看图；没有依据不填数字 |
| 可核对的交付 | 绑定源码、资产、原方法记录、读者审查与独立安装结果 |

它与普通 README generator 的区别在于：还负责按项目事实选择和执行原生方法、消费图像资产，并核对源码包与检查证据。脚本检查文件一致性和记录；业务含义仍由 Agent 和审查者判断。

## 快速安装

当前推荐候选版是 **1.0.0-rc3**，属于 Pre-release，不代表 Stable。

1. [下载固定版本安装包](https://github.com/qq2743759880/github-showcase/releases/download/v1.0.0-rc3/github-showcase-v1.0.0-rc3.zip)，解压到独立目录。
2. 进入解压后的 `github-showcase/`。需要能读取文件、执行命令的 Agent 和 Python。图像/图表阶段还需要 Node.js 24+；交互图和 C4 渲染需要可用的 Chrome/Chromium。需要源码打包时还要 Git。
3. 先检查环境；图像/图表任务再安装锁定依赖：

```powershell
python scripts/doctor.py
npm ci --no-audit --fund=false
python scripts/verify-vendors.py
```

可用的预装浏览器设置、可选 YAML 依赖和阶段检查见[环境安装说明](./references/portable-runtime.md)。`doctor` 默认只报告能力；传入实际 route plan 才检查本次所需阶段。浏览器和 `node_modules` 不在安装 ZIP 中。

在 Codex 中，把解压后的完整 `github-showcase` 目录放入本机的 Skill 发现目录，或将已有入口指向它；同名 Skill 只保留一个发现入口。其他宿主的发现位置按其规定配置。无需自动发现时，直接让具备文件与工具权限的 Agent 读取这个目录的 `SKILL.md`。

**安装 ZIP 是完整执行与分发闭包**：保留原相对路径、许可证、按需方法资源和验证源码。仓库中的 README、`assets/`、展示用 `docs/`、Pages 配置与私有构建记录不是 Agent 的安装依赖。克隆整个仓库用于阅读或开发，安装时优先使用固定版本 ZIP。

## 快速开始

从已解压目录确认 `doctor` 能运行、vendor 校验通过，然后给 Agent 一个有界任务：

```text
读取已安装 github-showcase 的 SKILL.md。
只检查我指定的项目目录，为第一次接触项目的读者整理 README。
先核对源码事实和首次使用命令；有架构/流程事实才生成对应图。
输出到新的独立展示目录，保留私有验证记录。
完成本地安全、资产引用、读者理解和源码包检查；本次不发布到远端。
```

首次有用结果是新目录里的 README 与当前任务确实需要的资产、源码包和检查记录；不是启动一个托管服务。Agent 遇到事实缺口应解释并保留未知，不能编造指标、功能或成功记录。发布到 GitHub 是另一个明确授权的操作。

恢复一次中断的任务时，可以这样请求：

```text
读取本次任务已有记录，核对当前源码、输出与检查证据。
修复失败项并重新验证；不覆盖未知的用户改动，不沿用已经失效的 PASS。
只在通过本地检查后继续已授权的发布，并回读实际远端内容。
```

## 按需生成与安全边界

- 有软件运行边界才生成 C4 Context/Container；方法文件和每个 vendor Skill 不被画成独立服务。
- 有真实流程才生成流程图；复杂呈现保留失败和恢复语义。
- 没有测量数据时使用能力分类，不编造收益图表；没有真实视频需求就跳过视频。
- 密钥、私人信息、许可或公开范围问题必须修正后再交付。普通布局、文案和环境失败应自主修复并复检。
- 工具不能保证业务正确，也不能阻止整个宿主绕过入口。远端写入后必须回读验证。

## 系统架构与发布

[查看系统边界、工具进程及关系依据](./docs/architecture.md)。Skill 是 Agent 加载的方法；Python 与 Node 是实际本地工具进程，浏览器负责 HTML 检查与查看，Git/文件系统保存源码与交付。

[查看发布流程](./docs/publication.md)：本地包 → 授权 → 公开导出 → 普通 Git 推送 → Pre-release → 远端回读。版本安装链接固定在 tag；不移动旧 tag，不 force push。

## 当前限制

本次实际安装和渲染验证基于 Windows、Python 3.14、Node.js 24 与本机 Chrome。没有据此宣称其他操作系统或其他模型都已验证。候选版不提供托管后端、自动密钥修复、跨宿主强制限制或性能提升保证。Python 检查与原生渲染不能替代语义审查。

## 文档与许可证

| 要做的事 | 入口 |
|---|---|
| 安装和诊断依赖 | [环境说明](./references/portable-runtime.md) |
| 理解软件边界 | [系统架构](./docs/architecture.md) |
| 理解安全发布与回读 | [发布流程](./docs/publication.md) |
| 执行一次有界展示任务 | [Skill 入口](./SKILL.md) |

项目采用 [`MIT`](./LICENSE)。安装包保留各原生资源的许可证与[第三方声明](./THIRD_PARTY_NOTICES.md)；交互展示的嵌入代码和字体另见[展示资产许可](./licenses/showcase/archify/LICENSE)与[字体 OFL](./licenses/showcase/archify/JetBrainsMono-OFL.txt)。
