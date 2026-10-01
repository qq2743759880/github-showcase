# F10: Package / Publish Backend / Remote Verification

## F10-A Package

包含源码、入口、配置示例、运行依赖与独立验证依赖。生成文件清单、逐文件 SHA256 与许可证 notices。只包含 F09 放行文件。代码输出仓必须 fresh clone 安装、配置、启动并通过测试。Skill 出厂打包可消费随包 skill-creator 的校验与 package 工具，不将其可选 claude eval 流程列为交付必需能力。

## F10-B Publish Backend

探测顺序：GitHub Connector（profile → repo access → 实际 write capability）→ gh CLI（version → auth → repo write access）→ NO_GITHUB_WRITE_BACKEND。账号具有 push 权限不证明 integration 拥有 Contents 写权限；403 必须如实记录。Connector 是 HOST_CAPABILITY，不 vendor，不读取或打包 OAuth 凭据。

两者均不可用时只阻塞 remote publish，F01-F09 与本地打包继续。主编排不得自动创建 token、读取凭据文件或无限重试。

## F10-C Remote Verification

读取 repo、visibility、default branch、提交、README、LICENSE、SKILL 与 manifest，逐文件与本地 hash/字节比对；若有 CI 则读取 status 与相关 run。非强制写入、保留远端父提交；读回不一致即失败。全部通过才 PUBLISHED_VERIFIED。

本 Preview 的一次发布使用本机现有 Git 认证完成非强制 push，Connector 负责读回。它是本次 release engineering 通道；通用产品仍以 Connector / gh 为约定后端，不能声称 Connector 写入验证已通过。
