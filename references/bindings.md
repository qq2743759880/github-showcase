# Preview Bindings

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

此表是选型索引，不是完整执行绑定。所有子 Skill 均未 vendored；不能从本仓获得其入口、successCheck 与文件闭包。不得猜测调用，实体不可加载时 BLOCKED。

所有输入来自 adapter：F01 只读项目根；F02/F08 读公开叙事；F03 读架构事实；F04 读流程；F05 读可证实指标；F06 读视觉 brief；F07 读批准的演示场景；F09 审导出树；F10 只交通过安全闸的包。

允许因依赖、兼容性、媒体或覆盖范围失败切换 fallback；secret/privacy/license/authorization 拒绝一律 STOP。F10 发布后必须验证仓库、visibility、branch、commit 和远端关键文件。
