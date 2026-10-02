# 验证结果实录（本包）

> 本文件所有条目均为本 run 会话内实跑的命令与输出摘录；过程 trace 在维护者侧 run 目录（trace/f0X-trace.md 与 output/private-review/）。没有一条是「应该如此」的声称。

## 1. 视觉资产验收（生成即验收）

| 资产 | 命令（真实执行） | 结果 |
|---|---|---|
| 首屏社交卡 | `node scripts/snap-x.mjs check <design.mjs> ×2`（pinned CLI 0.2.1） | `✅ github-social-preview.mjs / ✅ og.mjs — All designs valid.` EXIT=0，零 error |
| 首屏社交卡 | `node scripts/snap-x.mjs render … --out <export>/assets` | 两卡渲染成功 EXIT=0；PNG IHDR 机检 **1280×640 / 1200×630** |
| 首屏目视 | 渲染 PNG 逐张检视 | 首渲检出**简体字形空框缺陷**（日文字体子集缺简体码位）→ 显式加载简体中文字体重渲 → 复检零空框、零遮挡、零裁切 |
| 架构图 | `node scripts/render-c4.mjs -i assets/architecture.mmd -o assets/architecture.svg`（pinned mermaid-cli 11.17.0） | EXIT=0；首渲检出**图源尾部围栏误生成孤儿节点缺陷** → 修复图源复渲 → 残留检查 0 |
| 流程图 | 同上（workflow-lifecycle.mmd → .svg） | EXIT=0；viewBox 859.5×1682.5；错误元素检查通过 |
| 能力矩阵 | `python render_slide_spec.py trace/f05-spec.json -o assets/capability-matrix.svg` | `OK: rendered heatmap slide` EXIT=0；**30 格逐值核对：27 格 =1、3 格 =0（F07 诚实 0 行）**；行列标签齐全 |

## 2. 范围审查（F09，引擎实扫 + 机检）

| 轴 | 方法 | 结果 |
|---|---|---|
| secret | 凭据扫描引擎真实子进程扫全导出树（含全部文件） | 命中 `[]`，EXIT=0 |
| privacy | 盘符路径 grep、Owner 称谓 grep、内部点目录扫描 | 盘符 0；Owner 命中 1 = [skill/SKILL.md](../../skill/SKILL.md) 契约原文的禁令条款本身（逐字投影，非称谓使用，登记 REVIEW/KEEP）；点目录 0（assets 内曾再生一个簿记点目录，已清除并复查为 0） |
| secret 值形态抽查 | 高危凭据形态正则抽查 | 0 |
| 首屏表层分 | README 首屏九类违禁模式机检（哈希/样本/实体计数/依赖版本/渲染内核/内部运行编号/审计词等） | 0 命中 |
| 断链 | 导出树全 md 相对链接机检 | 最终态 0 断链（见收尾质量门输出） |
| 孤儿资产 | 导出树全资产 vs 全 md 引用比对 | 0 孤儿（见收尾质量门输出） |

## 3. 投影保真

| 文件 | 校验 | 结果 |
|---|---|---|
| [skill/SKILL.md](../../skill/SKILL.md) | sha256 与 Skill 本体包源文件比对 | MATCH |
| [skill/references/project-contract.md](../../skill/references/project-contract.md) | 同上 | MATCH |
| [skill/references/bindings.json](../../skill/references/bindings.json) | 同上 | MATCH |
| [LICENSE](../../LICENSE) | 同上（MIT） | MATCH |

## 4. 打包与全新 clone 复检（F10）

| 步骤 | 结果 |
|---|---|
| 导出树独立 git 提交 | 全部文件提交（含未跟踪清点为空复查）；打包面使用 git archive 隔离（.git 元数据不进压缩包） |
| 压缩包 | 经打包脚本生成于导出树之外（哈希与内容对提交归档） |
| 全新 clone 复检 | clone 到全新临时目录：文件清单与导出树一致；对 clone 树复跑收尾质量门，gates 为空（输出见下节同款 JSON） |

## 5. 收尾质量门（四门，机检强制）

最终门输出存档于本目录 [release-gate-result.json](release-gate-result.json)（由下述命令对最终导出树实跑产出）：

```
python scripts/release-gate.py <export> --policy <policy.json> --showcase-gate \
  --comprehension-receipt <comprehension-receipt> \
  --require-self-dogfood --self-dogfood-receipt <self-dogfood-receipt> \
  --allow-git-dirs
```

判定口径：`gates` 数组为空且 `F09=PASS` → `READY_FOR_APPROVAL=true`。本包发布授权为未批准（NOT_AUTHORIZED）→ `remote_publish=STOP`（零远程写入），终态 READY_FOR_APPROVAL（本地）。

## 6. 读者理解门（如实声明）

Reader Comprehension Gate 的验收人是**独立 Fresh Reviewer**（只读最终 README 回答五题），不由本 run 自评。run 目录中的理解收据为编排方预填稿（五题 + README 原文锚点），供独立 Reviewer 验收使用；本包不据此自称「已被读者验收」。
