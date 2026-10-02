# 资产消费台账（Asset Consumption Ledger）

> 本 run 所有被路由且验收通过的视觉产物，逐件登记 phase / producer / artifact / validation / final_consumer / consumed_where。
> 台账即「资产消费门」的证据面：下表每一件的 artifact 都在导出树内存在，且被 final_consumer 列所示面真实引用（机检见 [verification-results.md](verification-results.md)）。
> 注：consumed_where 内的链接均以本台账所在目录（docs/verification/）为基准的相对路径。

```yaml
- phase: F06
  producer: "snap-x (PRIMARY, pinned CLI 0.2.1, via scripts/snap-x.mjs check+render)"
  artifact: assets/github-social-preview.png
  validation: "check EXIT=0 零 error → render EXIT=0 → IHDR 1280x640 机检 → 目视（首渲简体字形空框缺陷 → 加载简体中文字体修复重渲 → 复检零空框零遮挡）"
  final_consumer: README 首屏 Hero（img 标签）
  consumed_where: "README.md 首屏 img 引用 ./assets/github-social-preview.png"

- phase: F06
  producer: "snap-x (PRIMARY, pinned CLI 0.2.1, via scripts/snap-x.mjs check+render)"
  artifact: assets/og.png
  validation: "与社交卡同批 check/render（EXIT=0）→ IHDR 1200x630 机检 → 目视通过"
  final_consumer: README 文档导航（OG 社交卡，发布时作 og:image 素材）
  consumed_where: "README.md「文档导航」表链接 [assets/og.png](../../assets/og.png)"

- phase: F03
  producer: "c4-architecture × mermaid-skill 组合 (PRIMARY, pinned mermaid-cli 11.17.0, via scripts/render-c4.mjs)"
  artifact: assets/architecture.svg
  validation: "render EXIT=0 → SVG viewBox/内容检查 → 首渲缺陷（图源尾部围栏误生成孤儿节点）修复复渲 → 复检无残留"
  final_consumer: README 架构节 + docs/architecture.md
  consumed_where: "README.md「## 架构」img 引用 ./assets/architecture.svg；[docs/architecture.md](../architecture.md) 文首 img 引用 ../assets/architecture.svg"

- phase: F03
  producer: "c4-architecture × mermaid-skill 组合（图源，可编辑）"
  artifact: assets/architecture.mmd
  validation: "与渲染成品同源；文档内嵌 fence 与 .mmd 文件同源一致"
  final_consumer: README 架构节链接 + docs/architecture.md 图源节
  consumed_where: "README.md「## 架构」链接 [assets/architecture.mmd](../../assets/architecture.mmd)；[docs/architecture.md](../architecture.md) 文末 mermaid fence 内嵌"

- phase: F04
  producer: "ux-flow-designer (PRIMARY, 指令型) × mermaid 渲染验收（pinned mermaid-cli 11.17.0）"
  artifact: assets/workflow-lifecycle.svg
  validation: "render EXIT=0 → SVG viewBox/内容检查通过"
  final_consumer: README 流程节 + docs/workflow.md
  consumed_where: "README.md「## 流程」img 引用 ./assets/workflow-lifecycle.svg；[docs/workflow.md](../workflow.md) 文首 img 引用 ../assets/workflow-lifecycle.svg"

- phase: F04
  producer: "ux-flow-designer（图源，可编辑）"
  artifact: assets/workflow-lifecycle.mmd
  validation: "与渲染成品同源"
  final_consumer: README 流程节链接 + docs/workflow.md 图源节
  consumed_where: "README.md「## 流程」链接 [assets/workflow-lifecycle.mmd](../../assets/workflow-lifecycle.mmd)；[docs/workflow.md](../workflow.md) 文末 mermaid fence 内嵌"

- phase: F05
  producer: "strategy-consulting-visualization (PRIMARY, render_slide_spec.py 纯标准库)"
  artifact: assets/capability-matrix.svg
  validation: "render OK（exit 0）→ 30 格逐值核对：27 格 =1、3 格 =0（F07 诚实 0 行）→ 行列标签齐全"
  final_consumer: README 真实能力节 + docs/capability-matrix.md
  consumed_where: "README.md「## 真实能力」img 引用 ./assets/capability-matrix.svg；[docs/capability-matrix.md](../capability-matrix.md) 文首 img 引用 ../assets/capability-matrix.svg"

- phase: F02
  producer: "humanizer (PRIMARY, 指令型显式加载)"
  artifact: docs/intro.md
  validation: "无编造数字/实现声称；事实全部回溯 facts 取证；对外称项目维护者"
  final_consumer: README 价值/工作方式/限制 节 + 文档导航
  consumed_where: "README.md「文档导航」表链接 [docs/intro.md](../intro.md)；价值与差异表述进入 README 正文"

- phase: F09
  producer: "secret-scanner (PRIMARY, engine.py 真实子进程) + 编排层 privacy/surface/link 机检"
  artifact: docs/security-boundary.md
  validation: "引擎实扫导出树命中 0；首屏违禁模式机检 0 命中；四门说明与契约一致"
  final_consumer: README 安全边界节
  consumed_where: "README.md「## 安全边界」链接 [docs/security-boundary.md](../security-boundary.md)"
```

## 非视觉产物的消费（F08 Showcase Composition 自证）

| 产物 | 进入展示面的位置 |
|---|---|
| F01 事实（facts/self-recon.md，run 目录） | 三案例数字与边界结论 → [docs/cases.md](../cases.md)、[docs/verification/verification-results.md](verification-results.md) |
| F09 审查回执（run 目录 output/private-review/） | [docs/verification/verification-results.md](verification-results.md) 的扫描与机检实录 |
| F10 打包与质量门输出 | [docs/verification/verification-results.md](verification-results.md) + [release-gate-result.json](release-gate-result.json) |

> 消费门判定：被路由且 PASS 的视觉 phase（F03/F04/F05/F06）产物 7 件全部被 README 或 docs 真实引用；F07 未路由（无获批演示素材）不产资产，无孤儿资产。
