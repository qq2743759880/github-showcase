# 能力矩阵：十槽位 × 三轴（本 run 实测）

> F05 产物。渲染成品 [assets/capability-matrix.svg](../assets/capability-matrix.svg)。
> 验收：渲染器 exit 0 + 30 格逐值核对（27 格 = 1，3 格 = 0）；数据全部来自本 run 落盘 trace 与导出树，可逐格复算。

![十槽位 × 三轴实测矩阵](../assets/capability-matrix.svg)

## 逐格出处

三轴定义：**本 run 路由**（route-plan 判 RUN/SKIP）· **产物 successCheck**（逐产物验收命令实测）· **进入展示面**（产物被 README/docs 真实引用，见消费台账）。

| phase | 路由 | 验收 | 进入展示面 | 出处（本 run） |
|---|---|---|---|---|
| F01 取证 | 1 | 1 | 1 | facts 逐条带来源引用；结论进入 intro/cases |
| F02 叙事 | 1 | 1 | 1 | 公开投影 → [intro.md](intro.md) 与 README 首屏 |
| F03 架构图 | 1 | 1 | 1 | 渲染 exit 0 → [architecture.md](architecture.md) 内嵌 |
| F04 流程图 | 1 | 1 | 1 | 渲染 exit 0 → [workflow.md](workflow.md) 内嵌 |
| F05 数据图 | 1 | 1 | 1 | 渲染 exit 0 + 30 格逐值核对 → 本文内嵌 |
| F06 首屏视觉 | 1 | 1 | 1 | check 零 error → render exit 0 → README 首屏 img |
| F07 演示 | **0** | **0** | **0** | 演示素材不可用（契约 demo_scenario=NOT_AVAILABLE）→ 跳过，不产占位件 |
| F08 README 组装 | 1 | 1 | 1 | 12 节 README + 全资产消费 |
| F09 范围审查 | 1 | 1 | 1 | 引擎实扫回执 + 首屏机检 → [verification-results.md](verification/verification-results.md) |
| F10 打包/发布 | 1 | 1 | 1 | git 提交 + 全新 clone 复检 + 质量门输出存档 |

## 为什么有一行 0

F07 演示槽位的路由条件是「存在获批演示素材」。本 run（自展示）没有可录制、可公开的运行时演示面——三案例即使用示例证据。**如实跳过并显式声明，好过放一个占位图或伪造素材**：这正是本方法「无数据不编造」纪律在能力矩阵上的体现。

## 与指标纪律的关系

本图是**状态矩阵**（路由/验收/消费三轴的 0/1），不是规模数字：它回答「哪些能力在本 run 真实走过链」。凡涉及数量的能力表述（工具数、模块行数、测试数）一律回源计数或实测，见 [cases.md](cases.md) 的逐案例证据。
