# Adapter: template

此为可移植示例，所有路径由使用者按真实项目填写；不是已加载的事实证据。

```yaml
project: template
project_roots:
  - {path: "./project", root_type: docs, notes: "replace with your project"}
facts_source:
  preverified: false
  files: []
  private_files: []
public_narrative: "./inputs/public-narrative.md"
architecture_spec: {nodes: [], edges: [], forbidden_edges: [], legend: ""}
workflow_spec: {chains: [], boundary_notes: "仅使用有证据的公开事实"}
metrics: []
demo_scenario: {status: NOT_AVAILABLE}
publication_policy:
  authorization: NOT_AUTHORIZED
  export_layout: "README + docs + assets"
  review_axes: [secret, license, privacy]
source_release:
  include_code: false
  entry_points: []
  excluded: [credentials, runtime-config, caches, binaries]
  fresh_clone_verify:
    deps_cmd: ""
    run_cmd: ""
    check_cmd: ""
domain_profiles: []
run_ledger: {dir: "usage/current"}
```

纯设计与知识项目不承诺可运行程序。示例不携带原项目指标或私有事实。
