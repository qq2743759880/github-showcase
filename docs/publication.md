# 发布流程

![从本地包到实际远端回读，包含授权拒绝、传输重试和身份不符](./diagrams/publication.svg)

[打开交互图](https://shltbro.github.io/github-showcase/diagrams/publication.html) · [本地 HTML](./diagrams/publication.html) · [可编辑数据](./diagrams/publication.json)

先完成本地检查和干净导出。授权不足时保留本地结果；得到明确授权才普通推送，并将 tag 绑定实际公开 commit。Pre-release 上传固定安装包，随后回读 tag、Release、资产字节与 Pages，再从远端全新克隆和安装。

普通传输或展示问题应修复后重试；真实凭据不得公开，历史 tag 不得移动，未知用户内容不得覆盖。检查失败不能伪造 PASS。这个流程描述方法义务，不证明任意宿主无法绕过。具体机制见[发布契约](../references/publish-backends.md)。
