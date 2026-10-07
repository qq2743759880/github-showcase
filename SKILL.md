---
name: github-showcase
description: This skill should be used when the user asks to turn a project into a GitHub showcase, assemble a verified README and visual pack, or prepare a source release. It routes evidence, editing, architecture, visual design, composition and local delivery by project contract with safety and verification gates.
metadata:
  version: "1.0.0-rc4"
license: MIT
---

# GitHub Showcase

Turn project evidence and approved public scope into a readable, verifiable showcase. Finish with a local source package and review receipts. Require separate publication authorization and remote read-back before declaring a published release.

For independent installation, run `python scripts/doctor.py` from the extracted package. Read `references/portable-runtime.md` when installing, diagnosing missing phase dependencies or relocating.

## Start and route

Read `references/project-contract.md` and the selected adapter. Reuse an existing adapter or fill `adapters/template/adapter.md` from source evidence. Missing facts remain unknown. Never invent numbers, demos, implementation, credentials or project ownership.

For every full project Showcase, apply `references/single-page-showcase.md`: preserve approved plain-language copy and visuals, place a compact same-page index immediately after the introduction, and keep all essential project explanations, installation/use instructions and required static diagram previews in that one README. Primary explanation navigation uses local fragments, not links to other documents. Downloads, source references and optional interactive views remain supplementary.

Classify the current project form from its actual entry. Agent Skills additionally use `references/agent-skill-readme-profile.md` and `references/distribution-surfaces.md`: process-first presentation, clear customer tasks, minimal original-byte Runtime artifact, and separate Showcase/private build evidence. Historical exports do not establish current facts. Preserve SPDX license identifiers in every language.

Run `python scripts/route-plan.py <adapter.json> --output <run>/route.json`. For Markdown YAML adapters, install the separately declared PyYAML dependency in the project environment. For a partial request, pass `--phases F02 F08` as appropriate; unverified facts still require F01. Record all work under a new approved run directory.

Read only each routed phase's `workflow` from the plan. Load the named original vendor entry only when executing that capability; load its step/type reference only when reaching that step. Do not read the whole vendor tree, reviewer catalog or all phase bindings. An available dependency is not execution evidence.

## Capability responsibilities

- F01: internal bounded fact discovery. Keep provenance, unknowns and an approved narrative. After bounded recon, use its complexity decision to invoke Optional **codebase-knowledge-builder** only for unresolved consequential questions inside approved scope; execute its complete original method when invoked.
- F02: internal factual draft. Route **humanizer** as an optional editor only when prose needs its distinctive review; run its full mark → rewrite → fact-check → final workflow. It is not counted as an integrated producer.
- F03: **c4-architecture** for evidenced software architecture. Include Context and Container; choose deeper levels only when useful. Design or knowledge collections must not acquire invented services.
- F03/F04 presentation: **archify** authors typed JSON and delivers validated interactive HTML plus a canonical static preview. Route repository-backed or local-content-bound provenance explicitly; missing origin never cancels an evidenced diagram. After bounded presentation repairs, use complete semantic decomposition with a union coverage ledger; every required view must pass native gates and be consumed. C4 retains software boundary and level semantics. Follow `references/workflows/archify.md` for details; Mermaid remains compatibility or an explicitly justified static fallback.
- F05: internal capability composition. Without measurements, use categories and explicit implementation status.
- F06: **snap-x**. Inspect, plan, design, check, render, view every result and deliver share notes. Its CLI is a renderer inside this workflow.
- F08: **readme-skill**. Preserve its fact ledger, handling mode, verified Quick Start, native guidance and actual-file QA. Apply the user-first single-page profile: embed required C4/flow previews with explanations directly in README, including every required decomposed view, and provide fragment navigation. Linked docs or an image filename alone do not establish same-page reader delivery. Record the profile's authorized placement override without modifying vendor originals.
- F09/F10: internal safety and delivery with an extracted deterministic secret engine. Secret, privacy, license or authorization rejection stops the action. Only exact reviewed synthetic security-test findings can use the content-bound fixture contract in `references/workflows/delivery.md`; preserve raw findings, never ignore test directories or exempt critical secrets. No reviewer can override rejection.

Integrated Skills have observable obligations in `references/core-contracts.json`. Reviewer/reference material and full external extensions have separate roles in `references/bindings.json`; they are not fallbacks or integrated Skills.

## Evidence and delivery

After composing README/public docs, read `references/public-copy.md` and run PUBLIC_COPY_NORMALIZATION → PUBLIC_COPY_REVIEW. Use the requested reader language and natural content headings; internal phase/asset labels are not reader copy. Preserve technical terminology. Final `--showcase-gate` rejects obvious label leaks; justified project terms require exact, evidence-bound `public_copy_allowlist` entries.

Validate the final same-page index, anchor targets and inline required content per `references/single-page-showcase.md`. A reader must understand installation, first use, architecture/workflow and limits without opening another explanation page. Existing recursive link-consumption checks are not proof of this. Repair ordinary navigation/content defects and recheck rather than ending the task; do not claim structural automation that was not actually executed.

Follow `references/workflows/delivery.md`. Validate each original workflow, preserve distinctive output, and record source resources, intermediate evidence, native QA and final consumers. Run `scripts/skill-fidelity.py` on the content-bound trace. That check proves recorded artifacts and obligations; independently review semantic fidelity before claiming the 85% target.

Run the full `scripts/release-gate.py --showcase-gate` with this run's JSON receipts. Require linked asset consumption, five README-backed independent answers and fresh-clone install → setup → start → verification install → tests for code/mixed projects. Self-release also requires a new self-dogfood receipt bound to the current product and export. Stale receipts fail.

Use `scripts/package-project.py` for the final clean local export repository. Packaging requires all showcase gates; source travels with code projects. `NOT_AUTHORIZED` permits local preparation only. After explicit remote publication authorization, follow `references/publish-backends.md` and compare remote contents with the approved commit. Remote write success alone is insufficient.
