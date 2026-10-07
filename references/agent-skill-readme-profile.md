# Agent Skill README Profile

Select when the current source establishes an Agent-loadable method Skill. This is a reader profile inside the native readme-skill authoring/QA workflow, not a per-project template or an extra producer. Current source is the only behavior authority; historical exports are presentation history, never current facts. Apply the default `references/single-page-showcase.md` profile too: a reader must not need another explanation page to understand or start using the Skill.

## Reader journey

Explain what it is and the user problem in plain language. Preserve approved positioning and show when it helps and when it does not. Put a compact same-page index immediately after the introduction. For a process-valued project, the detailed body starts with an inline static workflow preview and enough explanation to understand it, before installation and task examples. An obvious **Open Interactive Diagram** entry remains optional enhanced viewing, not the only way to read the workflow. Agent, Workflow, Pipeline, Automation and Orchestrator projects use this process-first rule when evidence supports it; a name alone does not trigger diagrams. Motion is a reading aid, not a runtime demo.

Then offer one installation section followed by one useful Quick Start / task section, both complete on this page. Do not repeat installation as a second start section. The headings and count are flexible. Each real task path specifies: user's input, what the Agent does, limits/non-actions relevant to that task, and expected deliverable. Prompt examples are source-backed task requests, not invented CLI commands or guarantees. A self-audit of the published Skill is verification evidence, not the primary customer example.

Include relevant architecture, configuration, results, safety/recovery and publication explanations on the same page, followed by version/license summary. Optional source and deeper developer references may still link out, but cannot hold the only usable explanation. Necessary environment or safety constraints appear before the affected action. No generic numeric benefit, fake screens, host portability promise or architecture diagram without evidence. Keep essential content visible rather than placing it all in collapsed details.

## Runtime installation clarity

Distinguish files actually loaded for execution from legal files shipped for redistribution. State on the page exactly which files go into the host Agent's Skill directory, what the host must support, how it loads the entry, and what successful first use looks like. Link the verified minimal Runtime artifact as a download, not as a substitute for instructions. A full Git clone is a Showcase checkout; its images, HTML and source IR are not Agent dependencies. Do not invent one discovery path common to every host. A host-neutral verified route is extracting the package and asking a file-capable Agent to read its exact `SKILL.md` before a bounded task.

Preserve the original install-relative paths. When a current Runtime artifact exists, inspect its inventory and bind `source_distribution` authority before drafting the install table. Distinguish a repository root license copy from the original Skill legal file; equal hashes alone do not make renamed paths faithful. Every described task must expose input, actions, limits and deliverable; recovery/conflict handling needs an actionable request as well as a prose boundary on this page.

## License identifiers

SPDX IDs are immutable identifiers, never localized: `MIT` 开源许可证, `Apache-2.0`, `GPL-*`, `BSD-*`, `MPL-*`. Preserve expressions, versions and exceptions exactly as the authoritative license. Use code formatting for IDs in prose; language changes affect surrounding prose only. Browser translation is outside source control: check the actual repository bytes, never copy a browser's translated license expansion into authored text.

## Authoring and QA

Continue native fact discovery, four-state ledger, explicit handling scope, full draft, pre-write and actual-file checklist. A task-authorized profile overrides native generic section placement; record that override rather than changing the vendor or marking required checks silently satisfied. Keep Quick Start useful. Draft task examples from source rules and requested customer tasks, qualify expected outcomes; do not describe hypothetical cleanup as an executed result.

Record profile anchors and workflow asset/interactive URL in publication policy. The release gate's existing process-first placement and license checks remain necessary, but do not by themselves prove same-page completeness. Review real heading positions, not the index's first mention of the same heading. The independent README-only reviewer must answer what/problem/input/output/difference and assess installation, first-use, architecture/workflow and safety/recovery from this page alone. Machine placement checks do not replace that review.

Historical version download links use a released tag or full commit, never a mutable default branch. Link Showcase third-party notices under `licenses/showcase/`, separately from the original Skill license. Legal files and source material do not need to be duplicated in the reading page.

For simultaneous Stable / Preview releases, preserve Stable's tag, Release and default installation link. Label the Preview as a candidate, state its requirements and exact Runtime inventory on the same page, and distinguish which instructions apply to each channel. Recommend an isolated preview location; two same-name Skills should not both enter a host's automatic discovery scope. Include a useful first-use route for the default channel, even when tool-based Quick Start belongs only to Preview. A preview Release is `prerelease=true` and must not become latest stable. Declare `release_channels` with distinct stable/preview versioned URLs, preview `prerelease: true` and `default_install: stable`; the gate checks declared coexistence, while remote readback verifies actual GitHub state.
