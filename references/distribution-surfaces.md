# Execution, redistribution, Showcase, Publication and private evidence

Every Agent Skill release separates installation, reader, publication and private evidence surfaces based on current source dependencies, not file counts.

If the Owner has sealed the current Runtime ZIP as an exact archive identity, set `preserve_source_distribution: true` in the package manifest as well as `source_distribution`. The same runtime-package CLI validates member paths, original bytes, metadata version and legal closure, then copies the authority archive without recompressing it and fresh-extracts the copied result. Its receipt binds the original and delivered ZIP SHA. Missing authority or any different member fails. Do not replace a sealed archive with an equivalent re-compression; equality of member bytes alone is insufficient. When no archive identity is required, existing deterministic packaging remains available.

For an existing Skill with a current original Runtime artifact, inspect that artifact's member paths as distribution authority in bounded fact discovery. Declare its source-relative path as `source_distribution` in the minimal package manifest and gate policy. The packager verifies the entire current-version original path/byte closure and retains its authority hash in the private receipt. A root LICENSE with identical bytes does not authorize replacing an original `references/LICENSE` path. If the existing artifact has an old version, it cannot establish the new closure; derive the new release from current original source and record the changed authority instead. With no existing artifact, establish the original relative paths from current source; do not invent an archive or treat every reference as a dependency.

- **Execution Surface:** entry Skill and actual method/tool/reference files the Agent must load. **Redistribution Surface:** the complete install package, including Execution and mandatory legal files. Do not call legal notices execution dependencies. Runtime Distribution is this packaged redistribution closure. Preserve source bytes and relative paths. Determine the inclusion closure from inspected entry/reference/tool usage; an unrelated reference directory is not automatically runtime. Record each included file's reason.
- **Showcase Surface:** README, identity image, useful static previews, self-contained interactive HTML, selected editable typed JSON when requested, and essential user docs. Include only attribution/notice actually required for redistributed embedded content. Archify is a product build capability; do not copy its tooling package into every target. Embedded viewer code in the delivered self-contained HTML belongs to Showcase, not the Agent installation.
- **Publication Surface:** intentionally public CI, release automation and deployment metadata, with a recorded purpose per file. Publication is neither user Showcase nor an Agent Runtime dependency. Examples: `.github/workflows/*.yml`, `.github/*.json`, release manifests and deployment configuration. It belongs to the exhaustive public allowlist, never the installation ZIP.
- **Build / Verification Evidence:** authoring/design sources, dependency manifests/locks, CLI logs, orchestration traces, intermediate diagrams, native finalize/browser receipts, source inventories and reviewer receipts. Keep private under the run by default. Rebuildability does not authorize putting all build files into the target public repo. If a project genuinely has a public developer SDK/build contract, route that separately with an explicit user need.

The policy declares `project_form: agent-skill`, exact `distribution_surface.execution`, `.redistribution`, `.runtime` (redistribution compatibility alias), `.showcase` and `.publication` file lists, `.evidence: []`, `readme_profile`, and private `minimal_runtime_receipt`. The public allowlist is exhaustive. Pure build artifacts in Showcase fail the gate. Runtime files are checked independently against the package and current export; legal additions for HTML must not leak into the install package.

Use `scripts/runtime-package.py <manifest.json> <name>-v<version>-skill.zip --extract <fresh-dir> --receipt <private-json>`. Manifest includes name, current version, read-only source_root and exact relative files. Outputs must be fresh and outside source; linked/escaping files and stale metadata fail. The ZIP has one named Skill directory, deterministic member metadata and original bytes. Fresh extract must contain exactly its allowlist. Recheck package, extracted files and current export at the full release gate. Never invent software tests for a method-only Skill.

Publish the Runtime ZIP as a GitHub Release asset when authorized and supported. When the upload transport is unavailable, an explicitly allowlisted downloadable ZIP in the repository is a valid Runtime distribution artifact; link it from README and Release without claiming it is a Release attachment. Record its relative path as `runtime_artifact`, and verify its bytes against the minimal-runtime receipt at the release gate. This archive is an installation deliverable, not build evidence; its contents still contain only Runtime files. Keep source-only distribution as another documented fallback. Before marking available, download the real remote artifact to a new path, verify bytes/inventory, fresh-extract again and perform the documented first-use method. A filename or upload success is insufficient. README must distinguish artifact installation from cloning the Showcase.

For updates, create a new isolated export from current facts, preserve the existing remote history and update main without force. Derived diagrams must pin a real source-containing Git commit; a prepared local commit can anchor finalize before pushing, but publication is not complete until that commit is remotely reachable and its source bytes match. Revalidate Pages byte identity, relative docs, all public files, fresh GitHub clone and Runtime download. Old receipts never prove the new version.

## Historical installation identity and legal layout

Every versioned installer URL must bind the exact released tag or a full commit. Release assets are preferred when supported; repository ZIP fallback follows the same immutable-ref rule. A correct current download from main is not a historical release guarantee. Declare `release_artifact` in the policy so the release gate can reject mutable default-branch URLs. Preserve existing tags and verify bytes and commit identity.

Preserve the original Skill legal file path in the install package. Put only embedded Showcase content licenses/notices under `licenses/showcase/<producer>/`, linking both surfaces distinctly from user docs. Include exact authoritative SPDX identifier in `license_identifier` contract; check all named primary-license documents, not one known translated string.

## Publication contract and safety

```json
{
  "distribution_surface": {
    "execution": ["SKILL.md"],
    "redistribution": ["SKILL.md", "references/LICENSE"],
    "runtime": ["SKILL.md", "references/LICENSE"],
    "showcase": ["README.md"],
    "publication": [".github/workflows/release.yml", ".github/release.json"],
    "evidence": []
  },
  "publication_purposes": {
    ".github/workflows/release.yml": "Publish an authorized immutable release",
    ".github/release.json": "Declare the public release tag and download"
  },
  "publication_authorization": "APPROVED",
  "release_artifact": {
    "version": "v1.0.0",
    "url": "https://github.com/owner/project/releases/download/v1.0.0/project.zip"
  }
}
```

Every file has one nonempty purpose; Runtime, Showcase and Publication are disjoint and their union is the entire public tree. Execution is a subset of redistribution; runtime equals redistribution. Empty Publication is valid (omission remains compatible with old policies). Conventional GitHub workflow and direct JSON configuration paths cannot be disguised as Runtime or Showcase. Custom release/deployment paths must be explicitly classified by the author. The Runtime packager also rejects conventional Publication paths or a manifest's declared publication members.

The full release gate applies its existing vendored secret scanner and explicit privacy literals to Publication too. Publication additionally rejects machine-absolute paths, evidence/receipt/trace/log directories, log files and recognized private receipt fields. A purpose string never authorizes exposing private data; classification is not a universal detector for arbitrary undisclosed private material. Review the actual contents and declare private literals.

Actions workflows require a static explicit top-level `permissions` map, `read-all` or `write-all`; any job-specific map is also parsed. Duplicate YAML keys, missing/dynamic/invalid scopes or a missing parser block. Any root/job `write` (including `write-all`) requires separate `publication_authorization: APPROVED`; generic `authorization` does not imply it. Reuse the pinned PyYAML from `requirements-verification.txt` for this conditional gate (`python -m pip install PyYAML==6.0.3`); JSON-only/non-Publication runs remain standard-library paths. Empty explicit `permissions: {}` is valid. These checks establish the declared scope, not working GitHub access or script semantics.

Each actual JSON `release_tag` or `artifact_url`, when present, must individually match policy `release_artifact`. A tag-only manifest with a repository-relative ZIP path is valid; it does not invent an absent URL. JSON embedded `release_artifact` / `release_channels` and literal GitHub artifact download URLs still pass the existing immutable-ref checks. URLs must be explicitly bound to release identity; mutable refs fail. Workflow shell expansion is not a remote tag verification. After any authorized publication, read back the actual tag, release and asset bytes as required by [publish backends](publish-backends.md). Local package PASS does not authorize or attest a remote write.
