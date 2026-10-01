# Roadmap

1. 经授权的 Public Preview 发布并远端回读，让维护者先查看产品结构。
2. 拆分 runtime_deps_cmd 与 verification_deps_cmd；明确安装、启动、测试步骤。
3. 固定最小 vendor 闭包、移除无许可证 fallback、生成 notices 与 hash lock。
4. F10 分成 Package / Publish Backend / Remote Verification；Connector 优先，gh 备用。
5. 提供 doctor、vendor 校验、adapter 验证；固定 snap-x 版本。
6. 从远端 fresh clone，以 SKILL.md 为唯一入口验证真实 primary、fallback、STOP 和生成代码项目再次 clone 运行。

全部证据通过后才报告 SELF_CONTAINED_ORCHESTRATION_VERIFIED；公开可用性另由维护者审阅。
