# Package, publication and remote verification

## Local package

Use `scripts/package-project.py <clean-export> <output.zip> --policy <policy.json>` plus comprehension, fidelity and fresh-clone receipt arguments. Source and dependency manifests accompany code. All showcase gates run over the isolated Git archive before writing output. Skill bundles use the same internal packager through `package-release.py`; skill-creator is no longer a runtime dependency.

## Publication backend

Only after explicit authorization inspect the host GitHub Connector's write capability or gh's existing access. Do not read credential files, create tokens, force push, or change remote history. Missing backend blocks publication while local review continues. No write backend is needed for local vNext.

An existing Git credential helper may perform a normal non-force push without the Agent reading its credentials. If the Connector lacks Release mutation and browser or local gh is unavailable, an Owner-authorized repository publishing workflow can use GitHub Actions' ephemeral GITHUB_TOKEN with contents-write scoped to that repository. Classify workflow/config in `distribution_surface.publication`, with an exact `publication_purposes` entry per file, never Runtime, user Showcase or evidence of successful release. Declare `publication_authorization: APPROVED` separately for root/job write scopes and run the same full gate before export. Explicit static Actions permissions are parsed with the existing optional PyYAML dependency; missing/ambiguous scopes block. See [the Publication contract](distribution-surfaces.md#publication-contract-and-safety). It must validate the sealed artifact SHA before writing, preserve an existing tag or release without moving/editing it, create a prerelease with `--verify-tag --prerelease --latest=false`, and avoid token output. Never infer working Actions permissions from the YAML. Require actual successful workflow and public Release/asset readback. Do not introduce this path when publication is not authorized, or use it to bypass a rejected access policy.

For Stable / Preview coexistence, record the existing Stable tag commit, Release ID/prerelease status, latest stable and default README download before publishing. Verify those identities again afterwards. A successful new prerelease is incomplete if Stable moved or the default install silently changed.

## Remote verification

After an authorized publish, independently read repository visibility, branch and commit, compare README/LICENSE/SKILL/manifests and approved source/assets with the local commit, and verify required CI. Compare bytes or hashes, not only existence. Read-back mismatch is failure. Report PUBLISHED_VERIFIED only after all checks; local receipts never attest remote publication.

## Immutable version artifact

Use an actual Release attachment when the authorized backend supports it. Otherwise pin repository downloads to the released tag or complete commit; never main/master/default branch for historical versions. Record release_artifact version/url/default_branch and run IMMUTABLE_ARTIFACT_FAIL gate before changing Release/README. Resolve tag remotely, preserve it without force, download the public artifact again and compare original byte identity.

## Public CI and delivery files

The exhaustive Agent Skill export allowlist is redistribution/runtime + showcase + publication, with evidence empty. Publication is omitted from Runtime ZIPs and frozen install packages; the public repository may retain necessary authorized CI and release metadata. Reuse the existing secret/privacy and immutable artifact gates; purpose strings do not waive them. Actual JSON release_tag/artifact_url must bind policy release_artifact. Keep private machine paths, receipts and execution logs outside public files. This model applies to generic CI/release/deployment files, not one project filename. Read-only workflows can be packaged without remote publication authorization when their explicit permissions grant no writes. Never confuse this local classification with successful CI or release readback.
