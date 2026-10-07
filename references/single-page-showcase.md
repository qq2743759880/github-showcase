# Single-page Showcase: read everything important without leaving the page

This is the default reader-experience profile for every full GitHub Showcase produced by github-showcase, not a template specific to github-showcase itself or to Agent Skill projects. An explicit, scoped user request can select a different information architecture; an Agent preference or upstream template cannot. Preserve existing approved positioning, plain-language explanation and useful visual assets. Change navigation and content placement before rewriting good copy.

## Reader outcome

For the release gate, use the first level-two section as the visible explanation index. In the run policy, declare `single_page.required_sections` as the actual anchor names for the task's essential explanations and `single_page.required_previews` as canonical README-relative image paths for all required views. These values follow the current target's facts, not fixed headings or a fixed picture count. `release-gate.py --showcase-gate` applies the structural check to every project kind; its bounded heading approximation is provisional until actual GitHub-rendered anchors are checked. Record any explicitly authorized partial-layout exception separately; do not claim a full single-page delivery for it.

After the brief project introduction, show a small, visible table of contents. Its explanation links target sections of the same rendered page. A reader who never opens another document must still understand the project, determine applicability, install or obtain it, perform the first useful task, interpret the architecture/workflow, understand outputs, and see relevant configuration, recovery and safety limits.

This is a single reading surface, not a one-file repository. Source code, scripts, tests, licenses, editable diagram sources, download packages, native interactive HTML and private verification records remain in their correct distribution surfaces. Never paste private facts, traces or the entire repository into README merely to satisfy this profile.

## Default composition

Keep the introduction and approved top visual. Place a compact page-local index immediately after that introduction and before the detailed body. For process-valued projects, put the workflow explanation and static preview at the start of the detailed body, before installation. Build the index from the actual final sections; do not force a fixed section count, empty sections, numbered phase names or a large sidebar.

A typical reading order is:

Brief introduction → page-local index → workflow/product overview → capabilities and delivered results → installation and configuration → first use and common tasks → architecture details → recovery/troubleshooting and publication when applicable → limitations and license summary.

Adapt the order to the real project. Installation commands and first use have distinct jobs and must not repeat one another. Necessary safety constraints appear before the affected action. Do not bury core instructions or the whole index in closed details blocks. Optional long reference material may use details, but essential usage remains visible.

## Same-page navigation

Use Markdown fragment links, for example `[安装](#安装)`, to actual unique headings in the current README. Explicit stable anchors are also supported, for example `<a name="gs-install"></a>` followed by `## 安装`, linked with `[安装](#gs-install)`. Keep visible labels natural in the reader's language; ASCII anchor IDs are implementation details.

The primary explanation index must contain only same-document fragments. `docs/install.md`, `README.md#install`, a GitHub blob URL, and a Pages URL are not equivalent to a same-page `#install` link. Downloads, source/reference links and optional interactive viewing belong beside their relevant content, not in place of the primary explanation index.

Keep anchors unique; resolve every entry after final heading edits, including Unicode, punctuation, duplicate titles and percent-encoded fragments. Prefer supported headings/anchors over inventing a JavaScript navigation widget. Test the actual GitHub-rendered page when publishing. The promise is in-page navigation, not a guaranteed smooth-scroll animation on every GitHub client.

## Inline content, not a directory of other documents

Move or compose all reader-required explanations into the README. A section containing only “see architecture.md”, an image download link or a table of external document entries is not complete. An index added above such stubs does not satisfy this profile.

Installation includes prerequisites, working directory, commands, necessary configuration and expected result. First use includes a concrete project task with inputs, actions and outputs. Architecture includes the readable static diagram and the essential explanation of real components and relationships. Workflow includes the normal path and consequential failure/recovery behavior, whether drawn in one view or several. Public release instructions and authorization boundaries are inline when publication is a real user task.

Existing docs can remain as optional technical/source references or be composed into the page. Do not blindly concatenate them: remove repeated introductions, normalize heading levels, preserve important qualifications, and rebase image paths and internal links relative to README. Keep a private source-section → destination-anchor map for the migration. Only approved public material may be moved. Avoid two separately maintained versions of the same user instructions; designate the README as the public reading authority and retain optional docs as references or generated derivatives.

## Diagrams and interaction

Every required reader diagram has a meaningful static preview embedded in the README, with an adjacent explanation sufficient to understand it. For semantic decomposition, all required views appear on the same reading page, not only the overview. An image path can still point to an asset file; the reader must see the image without opening that file.

Retain Archify's complete native authoring, source, validation, HTML and static export obligations. GitHub README does not become an interactive web application: do not inject script/iframe-based navigation or promise that native interactive HTML runs inside GitHub Markdown. The interactive link and editable source remain optional enhancements, never prerequisites for understanding the diagram.

If a GitHub Pages reader surface is requested, it should follow the same single-page information architecture. It may embed an existing native interactive viewer within that page if actual browser/security checks support it, with the same static fallback. Pages availability does not excuse a README that requires page changes to understand the project.

## Integration with existing methods

F02 keeps the approved plain-language copy. F03/F04/F05/F06 provide the required inline previews without inventing unavailable content. F08 loads this profile before the locked readme-skill structure/template, records the user-authorized placement override, then follows the full native fact ledger, draft, pre-write checks and actual-file QA. Keep vendor originals unchanged. Single-page composition overrides “link deeper docs instead of duplicating” only for reader-required explanations; developer internals and optional references still need not be reproduced.

The existing asset reachability test and five-question comprehension receipt are necessary but not sufficient: a linked document can consume an image while the README reader never sees it. Add actual same-page review of installation, first use, architecture/workflow and limits. Bind review results to the final README, never the old copy.

## Acceptance

Structural checks must verify index placement, fragment-only explanation navigation, unique/existing anchor targets, the inline presence of required sections and previews, and correct references after composition. Code fences, source snippets, download URLs, citations, license files and optional native interactive URLs must not be misclassified as forbidden explanation navigation. Do not implement a blanket ban on all non-fragment links.

An independent reader receives only the final README and its inline rendered assets, not linked explanatory documents or private briefing. They must explain what the project does, who it is for, inputs/outputs, installation/first-use steps, important architecture/workflow and limitations with same-page evidence. Anchors existing and sections being nonempty do not prove semantic completeness.

Use the existing final release/comprehension flow; do not create another approval bureaucracy. Missing anchors, link-only required sections or missing required previews are repaired and rechecked by the Agent in the current run. These ordinary presentation defects do not by themselves end the task or authorize relaxing safety checks.

## Compatibility and release boundary

Do not delete old docs or break historical external links merely to reorganize the homepage. Preserve immutable published Runtime archives and installation directories. This profile changes future Skill behavior: a new built/versioned Runtime is required before claiming installed Codex agents use it. A README-only homepage update and an installed Skill upgrade are separate deliverables.

## Primary platform references

- GitHub Docs, Basic writing and formatting syntax, section links and custom anchors: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
- GitHub Flavored Markdown specification, rendered-content post-processing and sanitization: https://github.github.com/gfm/
