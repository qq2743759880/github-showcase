# Runtime bindings

`bindings.json` is the local execution authority: locked entry, primary/fallback/compose, dependencyCheck inputs, invocation, successCheck, failurePolicy and fallbackCondition. Read that phase record and load its actual entry; never substitute the name for a real invocation. Paths are relative to the cloned Skill repository.

All selected entities are in `vendor/`, listed in `vendors.lock.json`. F03 design-doc-mermaid has been removed because its license file is absent; it is not a runtime fallback. F10 archives ordinary project exports through the gated Git packager; skill-creator is composed only for Skill artifacts and separates host publish/readback capabilities. See `publish-backends.md`.

Public outputs consume approved narrative, not private facts. Route F01 first when evidence is not preverified. No metrics/demo means skip quantified chart/demo. Primary failure can trigger fallback for dependency/compatibility/media/coverage only. F09 BLOCK always stops F10. Full closure and dispatch verification are pending; vendor presence alone does not prove execution.
