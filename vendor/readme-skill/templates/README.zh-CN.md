<!-- 如果检测到已有 README，应询问用户选择：完全覆盖、覆盖但选择性保留已批准的信息，或在原文基础上扩展。后续询问也应尽量提供明确选项。 -->

<!-- 仅使用仓库事实或用户确认支持的章节。展示草稿前删除本说明和所有不适用的可选章节。“快速开始”是必需章节：如果没有已验证的首次使用路径，应询问用户，不得删除、留空或臆造该章节。最终 README 不得保留占位内容。 -->

<!-- 居中头部：可选视觉、标题、定位语、语言切换、徽章。各块之间保留一个空行。从第一个 ## 标题开始全部左对齐。 -->

<!-- 可选顶部视觉：仅使用已验证的本地资源，并提供有意义的替代文本。资源较大时设置 width。 -->
<!--
<p align="center">
  <img src="./assets/<verified-image-path>" width="320" alt="<meaningful visual description>">
</p>
-->

<h1 align="center"><项目名称></h1>

<!-- 用一句可验证的话说明：它是什么、服务于谁或什么场景、以及一个真实差异点。 -->
<p align="center"><一句话定位说明。></p>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a>
</p>

<!-- 可选：只保留用户批准且来源已验证的徽章。所有徽章放在同一个居中段落的一行内。 -->
<!--
<p align="center">
  <a href="<verified destination>"><img src="<verified badge URL>" alt="<factual label>"></a>
</p>
-->

## 核心亮点

<!-- 保持 3–6 行，并确保每行有仓库证据支持。不要使用 emoji。 -->
| 亮点 | 对使用者的价值 |
|---|---|
| <已验证能力> | <基于仓库证据的实际收益> |

<!-- 可选。仅在架构事实已验证或经用户确认时保留，并紧跟在核心亮点之后。禁止使用 Mermaid。 -->
## 架构

<!-- 仅绘制有来源依据的组件和关系，使用 text 代码块。保持方框宽度/高度对齐，优先横向布局，并遵循 skill 指南中的方框、箭头和标注规范。 -->
```text
<verified ASCII architecture diagram>
```

<!-- 可选。紧跟在架构之后；若省略架构，则紧跟在核心亮点之后。只放入用户提供或仓库验证过的文字、图片/资源、代码/命令和预期结果。 -->
## 使用示例

<!-- 添加前确认示例文字、图片路径/资源、代码或命令、预期结果、位置和语言。 -->
<confirmed usage example>

## 快速安装

<!-- 提供阻力最低且已验证的安装方式，并注明必要前置条件。 -->

```text
<verified installation command>
```

## 快速开始

<!-- “快速开始”是必需章节。展示从可用或安装到首次获得有用结果的最短验证路径；缺少证据时应询问用户，而不是删除或臆造该章节。 -->

```text
<verified command or code example>
```

## 命令

<!-- 仅用于 CLI 或 Agent 工具；库和 SDK 请删除此节。 -->

| 命令 | 用途 |
|---|---|
| `<verified command>` | <可验证结果> |

## API 示例

<!-- 仅用于库或 SDK；无已验证公开 API 的项目请删除此节。 -->

```text
<verified import and minimal call>
```

## 配置与集成

<!-- 仅包含已文档化的选项、环境变量、集成方式或高级架构说明。 -->

## 文档

| 主题 | 内容 | 链接 |
|---|---|---|
| <读者任务> | <简短且可验证的说明> | [打开文档](./<verified-path>) |

## 参与贡献

<!-- 仅当存在贡献说明或用户确认的贡献渠道时保留。 -->

## 社区与支持

<!-- 仅包含已验证或用户确认的公开渠道。 -->

## Star 历史

<!-- 仅在用户确认且公开 GitHub owner/repo 已验证时保留；位置必须在“社区与支持”之后、“许可证”之前。 -->
<!-- [![Star History Chart](https://api.star-history.com/svg?repos=OWNER%2FREPOSITORY&type=Date)](https://star-history.com/#OWNER/REPOSITORY&Date) -->

## 许可证

<!-- 仅写入并链接已验证的许可证文件。 -->

<!-- 示例：本项目基于 [MIT 许可证](./LICENSE) 发布。 -->

<!-- 命令、代码块、环境变量、URL、路径、版本号和许可证标识必须与 README.md 中的英文版本保持完全一致。 -->
