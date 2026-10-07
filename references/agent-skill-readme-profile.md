# Agent Skill README Profile

Select when the current source establishes an Agent-loadable method Skill. This is a reader profile inside the native readme-skill authoring/QA workflow, not a per-project template or an extra producer. Current source is the only behavior authority; historical exports are presentation history, never current facts.

## Reader journey

Explain what it is and the user problem in plain language. Show when it helps and when it does not. When the process is the product's value, place a linked static workflow preview and an obvious **Open Interactive Diagram** entry directly after the brief introduction/value/applicability, before installation and task examples. Agent, Workflow, Pipeline, Automation and Orchestrator projects use the same process-first rule when evidence supports it; a name alone does not trigger diagrams. Motion is an optional reading aid, not a runtime demo.

Then offer one installation section followed by one useful Quick Start / task section. Do not repeat installation as a second start section. The headings and count are flexible. Each real task path specifies: user's input, what the Agent does, limits/non-actions relevant to that task, and expected deliverable. Prompt examples are source-backed task requests, not invented CLI commands or guarantees. A self-audit of the published Skill is verification evidence, not the primary customer example.

Finish with results and safety/recovery boundaries, then task-oriented deeper docs and version/license. Safety-critical setup can be called out at the point of use. Never hide a mandatory environment constraint until after a destructive prompt. No generic numeric benefit, fake screens, host portability promise or architecture diagram without evidence.

## Runtime installation clarity

Distinguish files actually loaded for execution from legal files shipped for redistribution. State exactly which files go into the host Agent's Skill directory, what the host must support, how it loads the entry, and what successful first use looks like. Link the verified minimal Runtime artifact. A full Git clone is a Showcase checkout; its images, HTML and source IR are not Agent dependencies. Do not invent one discovery path common to every host. A host-neutral verified route is extracting the package and asking a file-capable Agent to read its exact `SKILL.md` before a bounded task.

Preserve the original install-relative paths. When a current Runtime artifact exists, inspect its inventory and bind `source_distribution` authority before drafting the install table. Distinguish a repository root license copy from the original Skill legal file; equal hashes alone do not make renamed paths faithful. Every described task must expose input, actions, limits and deliverable; recovery/conflict handling needs an actionable request as well as a prose boundary.

## License identifiers

SPDX IDs are immutable identifiers, never localized: `MIT` 开源许可证, `Apache-2.0`, `GPL-*`, `BSD-*`, `MPL-*`. Preserve expressions, versions and exceptions exactly as the authoritative license. Use code formatting for IDs in prose; language changes affect surrounding prose only. Browser translation is outside source control: check the actual repository bytes, never copy a browser's translated license expansion into authored text.

## Authoring and QA

Continue native fact discovery, four-state ledger, explicit handling scope, full draft, pre-write and actual-file checklist. A task-authorized profile overrides native generic section placement; record that override rather than changing the vendor or marking required checks silently satisfied. Keep Quick Start useful. Draft task examples from source rules and requested customer tasks, qualify expected outcomes; do not describe hypothetical cleanup as an executed result.

Record profile anchors and workflow asset/interactive URL in publication policy. The release gate checks process-first placement and license localization. The independent README-only reviewer must still answer what/problem/input/output/difference, and additionally assess installation boundary and task-path clarity. Machine placement checks do not replace that reading review.

Historical version download links use a released tag or full commit, never a mutable default branch. Link Showcase third-party notices under `licenses/showcase/`, separately from the original Skill license.

For simultaneous Stable / Preview releases, preserve Stable's tag, Release and default installation link. Label the Preview as a candidate, state its own requirements and exact Runtime inventory, and explicitly distinguish which instructions apply to each channel. Recommend an isolated preview location; two same-name Skills should not both enter a host's automatic discovery scope. Include a useful first-use route for the default channel, even when tool-based Quick Start belongs only to Preview. A preview Release is `prerelease=true` and must not become latest stable. Declare `release_channels` with distinct stable/preview versioned URLs, preview `prerelease: true` and `default_install: stable`; the gate checks the declared coexistence contract, while remote readback verifies actual GitHub state.
