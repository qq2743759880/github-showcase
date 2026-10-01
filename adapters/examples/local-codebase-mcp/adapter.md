# Adapter: local-codebase-mcp

此为可移植示例，所有路径由使用者按真实项目填写；不是已加载的事实证据。

```yaml
project: local-codebase-mcp
project_roots:
  - {path: "./project", root_type: code, notes: "replace with your project"}
facts_source:
  preverified: false
  files: []
  private_files: []
public_narrative: "./inputs/public-narrative.md"
architecture_spec: {nodes: [], edges: [], forbidden_edges: [], legend: ""}
workflow_spec: {chains: [], boundary_notes: "不要录制真实隧道、令牌或私有项目"}
metrics: []
demo_scenario: {status: NOT_AVAILABLE}
publication_policy:
  authorization: NOT_AUTHORIZED
  export_layout: "README + docs + assets + source"
  review_axes: [secret, license, privacy]
source_release:
  include_code: true
  entry_points: [server.py, requirements.txt, config.example.yaml]
  excluded: [credentials, runtime-config, caches, binaries]
  fresh_clone_verify:
    deps_cmd: "python -m pip install -r requirements.txt"
    run_cmd: "python server.py --check"
    check_cmd: "python -m pytest tests -q"
domain_profiles: []
run_ledger: {dir: "usage/current"}
```

代码示例的验证需要额外 pytest；Preview 尚未将验证依赖拆成独立字段。启动前按示例配置填写 clone 本身的真实目录；测试范围以项目实际条件为准。
