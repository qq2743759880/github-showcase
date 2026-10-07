# Public copy normalization

After consuming readme-skill/Snap-X outputs and composing README/public docs, perform PUBLIC_COPY_NORMALIZATION then PUBLIC_COPY_REVIEW before the final delivery gate. Keep vendors unchanged. Choose the reader language from the explicit user request, otherwise the main language of the current request.

Distinguish internal orchestration taxonomy (F01–F10, asset roles, Surface, producer/consumer, route/binding/receipt/native gate), real product terminology (MCP, HTTP, SQLite, Python, PowerShell, Runtime, API, GitHub Actions, Archify), and reader-facing copy. Internal terms belong in private traces, contracts and implementation explanations. Ordinary target-project headings describe reader content, not production stages or asset types. Technical names remain accurate; English is not itself an error.

| Internal concept | Ordinary Chinese reader copy |
|---|---|
| Hero | Usually omit the heading; image alt may say 项目主视觉 / 项目头图 |
| Languages | 编程语言 / 技术栈, based on actual content |
| Capabilities | 能力概览 / 支持能力 |
| Workflow | 工作流程 |
| Architecture | 系统架构 |
| Quick Start | 快速开始 |
| Runtime | Keep Runtime or use 运行时 according to product meaning |
| Showcase | 项目展示 / 展示页面 only when that is the actual subject |
| Reader / Publication Surface | Omit from ordinary target-project reader headings |

This table guides semantic authoring; never use global string replacement. For example, replace a Languages Hero section about dependencies with 技术栈 (English: Technology Stack), not 语言主视觉. A top hero image needs no Hero section. Preserve filenames such as hero.png, identifiers, commands and URLs.

Review actual headings, navigation, image captions/alt, CTA/button text, first-screen labels and public-doc headings: do they sound like a real project README, describe user content, and avoid internal phase labels, awkward bilingual joins and asset-role headings? The Agent makes this semantic judgment. The deterministic PUBLIC_COPY_FAIL gate catches bounded obvious label leaks, not all language quality or all rendered text. A passing gate cannot replace this review.

The gate runs inside release-gate.py --showcase-gate. Markdown headings (including Setext), visible link labels and image alt, HTML titles/headings/nav links/buttons/labels/captions are inspected. Code blocks, inline code, URLs, filenames, scripts, vendor docs, private evidence and source identifiers are excluded. Hero is rejected in these labels, not in prose. Runtime/API remain legal technical terms. Chinese labels containing Showcase/Consumer/Producer/Binding/Route are flagged for semantic correction. No automatic rewriting occurs.

Explicit exceptions use policy.public_copy_allowlist: each entry has exact term, nonempty purpose, and evidence {path, sha256}. Evidence must be a public project document containing the exact term and bound to its current bytes. No default github-showcase exemption. For example, Publication Surface is legal when this product genuinely defines it, an architecture document proves that fact and the explicit allowance explains why readers need it. Allowances for one term do not waive other leaked terms. This proves evidence binding; the Agent still judges whether the exception is justified.
