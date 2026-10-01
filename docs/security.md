# Security

发布前检查导出树：凭据、令牌、个人联系信息、私人目录、运行配置、缓存、研究候选、内部任务与私有事实。只用批准的事实，源码项目明确 include/exclude，隔离 staging。

F09 对 secret/privacy/license/authorization 的 BLOCK 必须传递到 F10 STOP。不得通过 fallback 绕过。未授权时只交本地包；授权后发布仍需远端 read-back。Private 仓库升级为 Public 需要维护者单独批准。
