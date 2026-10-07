# Shields.io Badge Style Guide

Read this guide only when the user requests or evaluates badges. Badges are optional, should be user-approved, and must represent real, verifiable facts.

## Badge selection

Recommend a badge only if both its claim and destination/source are known:

| Badge category | Evidence required |
|---|---|
| Language / runtime | Manifest, toolchain file, or verified project requirement |
| Supported platform / OS | Explicit documentation, CI matrix, or user confirmation |
| License | Actual `LICENSE*` file or user confirmation |
| CI / tests | Configured workflow and a verified status endpoint |
| Documentation | Existing docs site or repository documentation link |
| Web / demo | Accessible, user-confirmed, or repository-configured destination |
| Package / release | Verified registry/release channel and endpoint |
| Community | Functioning public official channel |
| Security / maintenance | Actual policy or explicitly supported public status |

Never fabricate build state, test state, version, download count, compatibility, maintainer status, demo URL, or community link. When the appropriate dynamic endpoint is not verified, omit the badge rather than guessing.

Aim for 3–7 top badges. Add more only when each solves a distinct reader decision and the header remains readable. When an actual `LICENSE*` file is verified and the user has requested badge recommendations, include a linked static License badge in the default recommendation set unless the user declines it.

## Visual system

Use `style=flat-square` by default. If the existing README already has a coherent badge style, retain it unless the user wants a redesign.

| Category | Color name | Hex |
|---|---|---|
| Language / runtime | Blue | `3776AB` |
| Supported platform / OS | Slate | `4B5563` |
| License | Green | `22C55E` |
| CI / tests | Green | `22C55E` |
| Documentation | Indigo | `4F46E5` |
| Web / demo | Cyan | `0891B2` |
| Package / release | Orange | `F59E0B` |
| Community | Purple | `7C3AED` |
| Security / maintenance | Dark red | `B91C1C` |

Use color semantically. Green is not a generic decoration: it should represent a verified positive status or license category, not an unverified assertion.

## Static badges

Use this form for a static, factual label:

```text
https://img.shields.io/badge/<left>-<right>-<color>?style=flat-square
```

Percent-encode both label fields. Example:

```markdown
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square)
```

Use a linked badge only when its destination is verified:

```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](./LICENSE)
```

## Dynamic badges

Use a documented official endpoint for dynamic data such as CI status, package version, downloads, or a release. Preserve the endpoint’s documented semantics; do not re-label a badge to imply something stronger.

Before including a dynamic badge, verify:

1. the repository or registry identifier;
2. the endpoint pattern and data source;
3. that the target exists and represents the stated status; and
4. that the badge destination is meaningful to readers.

If any item is uncertain, offer a static fact badge if appropriate, or omit the badge.
