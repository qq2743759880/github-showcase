# 安全边界

> F09 产物（公开面摘要）。完整机检输出见 [verification/verification-results.md](verification/verification-results.md)；资产消费台账见 [verification/asset-consumption-ledger.md](verification/asset-consumption-ledger.md)。

## 数据流边界（公开成品只消费公开面）

| 层 | 内容 | 规则 |
|---|---|---|
| 私有事实源 | 项目内部文件、未批准事实、维护者私有配置 | 仅供内部核验；**不得进入公开成品** |
| 公开投影 | 公开叙事、契约字段公开面、已批准 assets | 公开成品的唯一消费来源 |
| 公开成品 | README / docs / assets / 台账 / 投影 | 进入导出树前必须过泄漏基线与范围审查 |

通用泄漏基线（所有项目）：凭据、私人信息、本机绝对路径、内部审计内容、未获批准的项目事实不得进入公开成品；对外称「项目维护者」。

## 凭据排除（本包实测）

- 导出树经凭据扫描引擎真实扫描（含测试文件在内全树），命中数为 0（回执见 [verification/verification-results.md](verification/verification-results.md)）。
- 隐私轴机检：维护者个人信息、内部会话标识、机器特定路径零命中。
- 首屏机检：README 第一屏（首个二级标题之前）不得出现哈希、固定装置样本、实体计数、依赖版本、内部运行编号、审计细节等维护者信息——机检零命中（这是四道质量门中的「表层分」门）。

## 发布闸（授权与远程写入）

- 本包发布授权状态为**未批准**（NOT_AUTHORIZED）：全程零远程写入，止步本地 READY_FOR_APPROVAL。
- 范围审查判 BLOCK 的内容，打包面对其 STOP——不得换工具、换通道并入（三案例中知识库项目对含凭据候选文件的处置即此规则的真实执行）。
- 「可发布（READY_FOR_APPROVAL）」与「已发布（PUBLISHED_VERIFIED）」是两个状态：后者要求明确批准 + 真实远程写入 + 读回全核通过。

## 四道质量门（收尾机检，全过才可 READY_FOR_APPROVAL）

1. **资产消费门**：被路由且验收通过的视觉产物必须被 README/docs 真实引用；孤儿资产 = FAIL；被路由资产缺失 = FAIL。
2. **读者理解门**：独立 Fresh Reviewer 只读最终 README，五题（是什么/解决什么/输入/输出/与普通 README 生成器的区别）全部有原文依据；本包收据为编排方预填稿，**待独立 Reviewer 验收**。
3. **表层分门**：README 第一屏零维护者信息（机检强制）。
4. **自展示门**：本方法 Stable Release 前必须用当前待发布版本展示自己并走完同一条链，收据含 SELF_DOGFOOD_PASS 标记——本包即该收据的载体 run。

## 已知边界（如实）

- GitHub 站内实渲染（fence / 社交卡 / OG unfurl）本地无法预验，属发布后首查项。
- 本包含 Skill 公开投影（逐字），若上游契约文件更新，投影需同步重新生成并复检。
- 展示包不含 Skill 可运行本体（脚本、子能力实体、锁定依赖）——本体的分发走独立打包链，其自身安全审查不在本包范围内。
