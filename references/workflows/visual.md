# Visual producer — snap-x

本工作流仅在本次 Showcase 需要 Hero / README card / social preview 时加载。先从 F06 binding 的 `snap-x` producer 记录解析原入口，再从 vendors.lock.json 取得锁定 revision，读取原 SKILL.md。保留其四步顺序和原 QA，执行命令使用产品锁定 wrapper：`node scripts/snap-x.mjs`。renderer 是工具，不能代替本工作流。

输入为当前 run 的证据账本、公开叙事、品牌或明确的 brief、需要的发布 surface，以及已批准的输出根。项目事实、品牌缺失和设计提案必须分别写明。数字需有 evidence/as_of；没有数字不画指标。真实logo存在才使用并记录source；没有则text wordmark。不得拿产品说明当被展示项目的事实。

没有visual需求时记 `NOT_ROUTED`，不加载子Skill/参考，也不生成占位图。secret/privacy/license/authorization拒绝直接STOP，不能换renderer或fallback绕过。

## 1. Inspect

现在只加载原 `references/step-1-inspect.md`。通过repo manifest/README/已批准public brief和本地品牌资产回答**原inspect九问**，并写入 `trace/visual/inspect.md`：

1. Name：名称与出处。
2. Description：一句价值及出处。
3. Domain / brand：真实公开URL或品牌；无domain时明确省略。
4. Tags / proof：仅2–3个真实labels/证据点；无量化证据不用数字。
5. Stack / surface：真实实现/产品面；设计未实现必须说明。
6. Font：源字体或有理由的fallback。
7. Accent color：logo/CSS源色或明确提案。
8. Theme：源主题或brief决定。
9. Logo / brand assets：检索范围、选择的真实文件及其可公开来源，或明确 `none → text wordmark`。

记录所读路径+lines、矛盾源裁决、所有absence和assumptions。若复用已有 `_brand.mjs`，先读取并核对当前source，不把旧plan的PASS传递本run。使用logo时必须实际看该文件；SVG若无法直接看，先render可视副本。资产来源写 `trace/visual/assets/SOURCES.md`，图中不得引入未批准第三方customer logo。

完成门：九问全部有source或明确缺失理由；任何load-bearing无据claim已移除；没有真实资产就用wordmark。Step2 planning的九项不能冒充inspect九問。

## 2. Plan

现在加载原 `references/step-2-plan.md`、`references/formats.md` 和 `references/design-principles.md`。先执行并保存 `node scripts/snap-x.mjs formats` 回执，再按选定id或尺寸执行formats lookup。只制作项目真正需要的格式；通常一张README Hero已足够。选定format的size、alpha、verified/unverified和placement zones全部写进plan；对没有zones的格式写理由，不能省略调查。

在创建design之前写 `trace/visual/snap-plan.md`，包含：

- 一个hook、目标读者、真实分发surface和每个format的准确copy。
- 色板、字体与weights、text wordmark或asset variant/source；设计提案/假设单独记录。
- 每个claim的facts ledger（出处、evidence/as_of），mock仅在获批且明确label时使用。
- 每元素purpose、spacing unit、type scale、每format原archetype、safe zone。
- 原formats回执和guides计划；选择不适用分支的原因。
- 精确可复跑命令 `node scripts/snap-x.mjs render <design-file...> --out <approved-output/assets>`。
- 本run源与output路径，禁止含凭据或将本机绝对路径嵌入公开图。

完成门：plan先于design存在，copy和事实已决定。无real series不添加VARIANTS；无need不增platform图。不得为了达到85%补出无关format。

## 3. Write and check

现在加载原 `references/step-3-design.md`。先写 `trace/visual/designs/_brand.mjs`，再每个format一份design入口；所有入口从helper复用color/fonts/spacing/type。各design导出FORMAT、FONTS和自包含Satori tree，符合原flex/children/no-undefined/font-weight/text-fit规则。使用shape画字体不含的特殊glyph；CJK字形应有明确可用字体并经渲染核实。

保持精确canvas size。body contrast至少4.5:1，大字至少3:1；计算并写plan。选择的版本若不支持某个条件功能，记录compatibility BLOCKED，不用不锁版本的npx替代。

执行原 `node scripts/snap-x.mjs check <design-file...>` 并保存stdout/stderr/exit。必须零error；warning逐项处理或经实际图像确认无影响，不能无视缺字形warning。检查通过只表示技术有效，尚不能交付。

完成门：原check通过，_brand和design可复建，源copy逐项可回源，无placeholder/logo伪造。

## 4. Render, view, review and deliver

Keep the rebuildable Snap-X sources and exact dependency closure in the private build surface by default, particularly for Agent Skill releases. Use the product's pinned renderer and retain design/check/render evidence privately; publish only the final image and legally required notices. Only when a real public developer/build need is explicitly approved, run `python scripts/export-visual-runtime.py <approved-build-surface>` to extract the exact closure and portable Windows runner. A pinned CLI alone can resolve a different core; verify an isolated rebuild with the actual locked runtime. Rebuildability does not make design sources, package manifests/locks or caches user Runtime dependencies, nor automatically authorize their publication.

现在加载原 `references/step-4-render.md`。执行锁定wrapper原render，保存命令、stdout/stderr、exit、输出dimensions。对**每张PNG实际看图**，按原九项检查glyph、换行/clip、text-over-decoration、canvas edges、logo比例/可见性、contrast、alpha（如app store）、copy/source、brand。错误必须改源→重check/render→再实际view；尺寸或check成功不能替代看图。

将每张PNG的六项render review回填plan：focal point、hierarchy、spacing/alignment、contrast、squint、pack consistency各1–3分，任何1分先修。原图和真实显示尺寸的thumbnail都要实际看。一个Hero的pack consistency可记录same-source helper一致或single-image N/A理由，不能为了评分造第二张图。

有placement zones时执行原guides，实际看overlay和mobile crop；没有zones记录CLI输出 `nothing to check`（合法N/A）。不要手写QA design替代guides。留存实际view文件和缺陷/修复记录于 `trace/visual/qa.md`。

OG QA 只有确有 OG/social sharing 需求时，按 reviewer/reference 索引加载 `vendor/og-image-design/plugins/heyimjames-design/skills/og-image-design/SKILL.md` 的 Thumbnail survival、Workflow 和 QA/debug 部分。其缩略/center crop/greyscale可作为额外 review；它不是 snap-x fallback，也不能代替原六项 render review。不要连带执行无需要的 archetype/AI generation 路线。外部 unfurl 只有发布后且获授权才测；本地候选必须记 `NOT_RUN_LOCAL_ONLY`，不能写已真实 unfurl PASS。

写 `trace/visual/share-copy.txt`：实际产物→用途、尺寸、mock/assumptions、品牌来源、精确regenerate命令。公开export只含最终需要资产及获批sources；内部QA/trace留private run。

最后由README composer在最终README/docs引用本run最终资产，消费ledger记录artifact+final consumer+lines。visual producer只到 `PRODUCED_AND_REVIEWED`；消费证明完成后才 `CONSUMED`。无最终引用就是ORPHAN，不得给integrated fidelity PASS。

## Fidelity receipt

每次路由必须在 `trace/visual/fidelity.json` 或等价trace中留下：source revision与实际读取reference顺序、inspect9问、plan-before-design、facts/assumptions、formats/zone决定、原check/render命令回执、每PNG实际view+六轴review、guides判定、share-copy、最终消费定位。引用其它run只能作背景，不能代替本run证据。

完成条件是完整适用核心义务均有证据。conditional branches（无logo、无zones、无series、无OG）必须写N/A理由；核心inspect/plan/check/render/view/review/share/消费不能标N/A。任何未验证步骤明确UNVERIFIED；不得从图片存在推断完整Skill高保真。
