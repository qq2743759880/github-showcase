# README composition: readme-skill native workflow

Use this route when the requested deliverable includes a new or revised GitHub README. Its producer is the locked `vendor/readme-skill/SKILL.md`; read that file before executing. This workflow maps Showcase inputs into its native authoring process. A successful general release gate does not substitute for the producer's own quality checklist.

The default reading surface is a complete single-page README. Load `references/single-page-showcase.md` before selecting the native structure/template. Preserve approved plain-language copy and visuals, add a compact page-local index after the introduction, and place every reader-required explanation and static preview on the same page. Optional source, download and interactive links supplement that content; they do not replace it. This profile applies to all full Showcase projects, not only Agent Skills.

The output must help a new reader understand the project and reach the first useful result without opening another explanatory document. It must also consume the routed assets and distinguish verified implementation from design. Completion means a source-grounded README at the exact authorized target, native QA against the actual file, verified first-use evidence, an asset consumption ledger and an independent comprehension receipt bound to the final README.

## Inputs and write scope

Consume only the same run's source facts, approved narrative, architecture/workflow specification, approved visual assets and public boundary review. Existing source README files are evidence; isolated Showcase work writes only the new run export. Record `create_export`, the full target path and the read-only source boundary. The current user task can authorize creating or editing the local export; use its stated authorization and do not ask the same save question again.

For an existing target, record the authorized handling mode: complete replacement, selected factual retention, or extension. Do not infer replacement merely because a source README exists. Keep a `keep / move / merge / remove` table before writing, including the original section/path, chosen treatment, factual basis and reader benefit. Preserve source content outside this export. Do not overwrite an existing unrelated output to reuse a run name. For a navigation-only request, preserve approved wording and approved assets unless a factual or usability defect requires a scoped change.

## 1. Discover and classify facts

Perform the producer's bounded discovery. Read root inventory, README variants, license/security/contribution files, docs index and manifests actually present. Inspect CLI/API definitions, CI, deployment, configuration and examples only to verify the intended README claims and first-use route. Reuse verified project evidence from the same run; revisit definitions when a public symbol or command lacks an authoritative anchor. A previous README or historical run is not current implementation evidence.

Before drafting, build a four-state fact ledger:

| Status | Meaning | Required evidence |
|---|---|---|
| Verified from repository | Current source/manifest/configuration or an actual local execution supports the claim | Relative source path and lines, or command/log and result |
| Confirmed by user | Explicit user statement resolves a fact or decision | The scoped user instruction |
| Uncertain | Plausible but not safe to publish | Omit or qualify; identify the unresolved point |
| Missing | Necessary information is absent | Block the affected section; for Quick Start block final README completion |

Every external claim, number, command, API/import, path, supported version, badge, license and architecture relationship must have a ledger entry. No observed metrics means no quantified chart or benefit percentage. Design inputs must stay labeled as design; an unimplemented demo must not become a screenshot, command or claimed behavior.

## 2. Load relevant native guidance

Apply `references/single-page-showcase.md` for the public reading surface. When source establishes an Agent Skill, also load `references/agent-skill-readme-profile.md` and `references/distribution-surfaces.md`. Apply its source-backed task journey and Runtime installation clarity. For process-valued Agent/Workflow/Pipeline/Automation/Orchestrator projects, the early workflow rule also applies: introduction, compact local index, then inline workflow before installation/tasks. Record the profile's task-authorized override of generic section placement; continue complete native authoring and actual-file QA. License identifiers are never translated.

Record a load ledger with actual resource paths, why each was needed and where it affected the output. Load:

1. `vendor/readme-skill/SKILL.md`.
2. `vendor/readme-skill/references/readme-structure.md` before section selection.
3. `vendor/readme-skill/references/quality-checklist.md` before the draft, again immediately before writing, and against the actual final files.
4. Only the template for the selected language: `templates/README.en.md`, `templates/README.zh-CN.md`, or `templates/README.bilingual.md` plus the applicable language template.

Load `references/badge-style.md` only for requested/evaluated badges and `references/image-generation.md` only when selecting/generating README imagery. Existing approved Hero assets can be reused without invoking the optional image generation API. Do not load generator code or ask for provider credentials for an existing local asset. Star History needs a verified public repository identifier and explicit choice; it does not require reading unrelated resources.

## 3. Resolve applicable decisions

Record each decision as `verified input`, `user-confirmed`, `default supported by the task`, `omitted with reason`, or `unresolved`. Preserve existing session choices. Ask one genuinely blocking unknown at a time; code and evidence answer technical facts.

| Decision | Native behavior and reader-profile override |
|---|---|
| Language | English primary, Chinese primary, or bilingual according to the task. For bilingual output, preserve the chosen primary language and record any user override. Each language page is independently complete; language switching is optional, not a dependency for understanding it. |
| Header | Center the identity band by default with separate compatible HTML blocks. A user-requested plain Markdown header is an explicit override. Body starts left aligned at the first `##`. |
| Navigation | A small fragment-only explanation index after the introduction; all destinations exist on the same page. Do not substitute a directory of docs links or GitHub's hidden outline control. |
| Badges | Optional. Use approved badges with verified claims and destinations. When badges are requested and a license is verified, propose a linked static license badge. Omission is valid. |
| Architecture in README | Optional and source-backed. The native optional text sketch uses aligned ASCII; independently routed C4/Archify diagrams have inline static previews and essential explanation under the single-page profile. Do not require opening a separate architecture document. |
| Usage example | Optional selection, but documented first use is always required. Include only supplied or repository-verified example prose, code/assets and expected result. |
| Imagery | Reuse approved local assets or route generation only when actually requested. Validate the asset before referencing it. Embed required reader previews in README; do not merely link their filenames. |
| Star History | Optional. Require explicit selection and a verified public GitHub owner/repo; disclose third-party dynamic SVG use. Omit for private/uncertain repositories. |
| Community/support/contribution | Include only actual supported routes or user-confirmed information. No invented Discord, package page, release or maintainer identity. |

Retain native source formats and validation. A public static preview is not a replacement for the C4 semantic source or the native Archify HTML. Record the profile override and each required preview's exact inline README consumer. Download/source/interactive links remain additional options. A filename in a private trace, standalone inventory or linked doc is not same-page reader delivery.

## 4. Compose and review the draft

Use the native authoring method and applicable template, remove unsupported optional sections and keep Quick Start. Do not impose a fixed twelve-section checklist. Put the approved brief introduction first, a compact same-page index next, and all essential explanation in the body. Process-valued projects lead the body with the workflow preview. Installation and task examples follow a logical user journey. The single-page profile overrides the native generic placement order when needed; preserve native fact and quality obligations rather than altering vendor files.

Migrate reader-facing details from existing architecture, installation, usage, recovery and publication documents into their corresponding README sections. Keep a private source-section → final-anchor map. Remove duplicate introductions, rebase relative assets/links, and preserve safety qualifications. Optional developer reference and source documents can still be linked. Do not duplicate entire research, source or legal archives, and do not leave a required section as “see another page”.

Quick Start must show the shortest verified path from availability/installation to a useful result. Include required prerequisites, working directory, real command or API, minimal setup, expected behavior and the verification result on the current page. A heading with placeholders or an unexplained installation command is not a Quick Start. If there is no runnable entry for a non-code project, verify the real browsing/use path from the exported files and label it accordingly. If no useful first-use route can be verified, do not fabricate one or report final README PASS.

Before the authorized write, place the complete Markdown draft in the run review record, with structure recommendation, fact ledger, optional inclusion/omission decisions, exact target and `keep / move / merge / remove` treatment. Report relevant unresolved items. The review record is an implementation artifact under the approved run root, not public product content. User authorization for the current local export permits proceeding after these checks.

For bilingual output, both versions must have matching inclusion decisions, diagram semantics, code/commands/paths/versions/badge destinations/license identifiers, complete useful Quick Start sections and reciprocal language links. Rewrite prose naturally; do not drift technical facts between languages. Each index targets its own page's anchors.

## 5. Native QA on the actual files

Apply the locked `quality-checklist.md` before drafting, before writing and after writing. Keep criterion-level results with evidence or an explicit inapplicability reason. Check:

- Source facts, real APIs/CLI/config paths, environment-variable-only secret examples and verified license.
- Nonempty useful installation/Quick Start on this page; execute examples when feasible and retain logs. Exact checks not run remain disclosed.
- No emoji. Source-backed architecture and confirmed optional usage example; record authorized placement overrides instead of silently waiving the native method.
- Correct centered header unless the user chose plain layout; left-aligned body, valid HTML, heading hierarchy and no empty/template sections.
- Compact index after the introduction; explanation links contain only local fragments, with unique/resolvable destinations after final heading changes.
- Every selected badge/Star History source/identifier/destination and required placement.
- Meaningful alt text and valid rebased references. Required visual previews appear in README itself, including every required decomposed view; optional full interactive/source artifacts still satisfy their separate native delivery contract.
- Bilingual technical parity and reciprocal links when selected.
- Honest limits/non-goals and clear implementation/design distinction on the same page. Linked optional deeper references must not contain the only usable installation, workflow or safety explanation.

Existing recursive asset reachability and ordinary file-link validation are not sufficient to certify the last two reader requirements. Actually inspect the final index and same-page reading experience. On GitHub use supported section fragments/custom anchors; no script-dependent scrolling or claim of guaranteed smooth animation. Repair broken anchors and missing inline explanation in the current run.

After native QA, route the independent `good-readme` reviewer in Improve/Audit mode when that reviewer is enabled. It reads the complete final README and authoritative source, extracts and checks documented symbols, scores every actual numbered native criterion and proposes source-backed fixes. If upstream's stated count differs from its actual list, report the discrepancy and assess the full list. Keep its report separate from the producer trace. Accepted edits require native QA and a refreshed final-file comprehension receipt; a prior README hash cannot certify changed prose.

## Evidence and final report

The run must retain a producer trace with exact locked revision/resources, trigger and scoped inputs, decisions, fact ledger, draft review, write target, native QA result, command logs and exact final consumption locations. Use the product fidelity receipt validator for the current schema; evidence must refer to actual artifacts and their hashes. An assertion that only repeats this workflow text is not execution evidence.

The independent reader receipt follows `scripts/evidence.py` kind `reader-comprehension`: status PASS, final `readme_sha256`, named reviewer, `independent=true`, and five answers (`what`, `problem`, `input`, `output`, `difference`) each quoting the README. The reviewer receives the README and its inline rendered assets, with no private product briefing or linked explanatory documents. Also assess installation, first-use steps, important architecture/workflow and safety limits with same-page evidence. Keep those checks alongside the native receipt without inventing a new mandatory approval stage. Mechanical acceptance of a receipt is a consistency check; the quoted answers must still be assessed for correctness.

Report the producer's native outcome: files changed and purpose; verified facts/commands/paths/links; same-page content and navigation checks; items needing confirmation or checks not run; sections/assets omitted and why. Include deviations from upstream with their user authorization and rationale. Final Core fidelity is demonstrated by new fixtures/traces, not by the vendor's presence or a successful final archive.
