# 系统架构

github-showcase 的方法文件由 Agent host 加载；Python 和 Node 是实际可运行的 CLI 边界。vendor 方法资源不是独立服务。Context 面向项目使用者；Container 面向安装者和维护者。更深组件、部署或动态视图未因本次读者问题触发。

## 系统边界

![C4 Context，说明用户、Agent、项目和远端的关系](./diagrams/context.svg)

[打开交互图](https://shltbro.github.io/github-showcase/diagrams/context.html) · [本地 HTML](./diagrams/context.html) · [可编辑数据](./diagrams/context.json) · [C4 Mermaid 源码](./diagrams/c4-context.mmd) · [C4 原生渲染](./diagrams/c4-context.svg)

| 从 → 到 | 动作与机制 | 当前依据 |
|---|---|---|
| 项目使用者 → 方法 | 指定范围与批准公开，用户请求 | `SKILL.md`、项目契约 |
| Agent host → 方法 | 读取 Skill 及按需资源，文件 | `SKILL.md` |
| 方法 → 目标项目 | 读取事实并生成获批导出，文件系统 | `route-plan.py`、`package-project.py` |
| 方法 → GitHub | 仅授权后公开与回读，Git/HTTPS | `references/publish-backends.md` |

## 本地工具进程

![C4 Container，显示 Python、Node、浏览器和文件边界](./diagrams/containers.svg)

[打开交互图](https://shltbro.github.io/github-showcase/diagrams/containers.html) · [本地 HTML](./diagrams/containers.html) · [可编辑数据](./diagrams/containers.json) · [C4 Mermaid 源码](./diagrams/c4-containers.mmd) · [C4 原生渲染](./diagrams/c4-containers.svg)

| 从 → 到 | 动作与机制 | 当前依据 |
|---|---|---|
| Agent → Python | 调用 route、gate、packaging CLI | `SKILL.md`、`scripts/route-plan.py`、`scripts/release-gate.py` |
| Agent → Node | 调用图像与图表工具 CLI | `scripts/snap-x.mjs`、`scripts/render-c4.mjs`、原 Archify CLI |
| Node → 浏览器 | 交付 HTML，DevTools 检查 | Archify 原生 browser-check、Mermaid wrapper |
| Python → 项目文件 | 核对字节和清单，文件系统 | `scripts/runtime-package.py` |
| Python → Git/文件系统 | 打包已提交源码，Git CLI | `scripts/package-project.py` |
| Git → GitHub | 授权后普通推送，Git/HTTPS | `references/publish-backends.md` |

图例颜色沿原生 Viewer 类型显示，描述文字才是 C4 身份依据：方法不是服务，文件节点不表示运行了数据库。关系状态是源码定义的当前执行方法，不能把图中的连线理解为宿主强制策略。
