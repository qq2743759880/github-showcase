---
name: readme-skill
description: Draft, improve, restructure, translate, or audit fact-based GitHub README files. Use when the user wants a README for an open-source repository, bilingual README documentation, badges, README visuals, ASCII architecture diagrams, usage examples, Star History charts, or a safe README rewrite.
---

# README Skill

Create accurate, readable GitHub README files by grounding every external claim in repository evidence or explicit user confirmation. Establish value first, provide a fast path to use, then route readers to deeper documentation.

## Non-negotiable rules

- **Drafts are shown in the conversation by default; do not create a draft file automatically.**
- **Do not create or modify `README.md`, `README.zh-CN.md`, or any other README until the user explicitly asks to write or update it.**
- If the user wants a saved draft, use the exact target path they provide; otherwise ask for one. Do not invent a draft filename.
- Never invent commands, APIs, links, badges, performance claims, compatibility promises, release data, community locations, license terms, architecture components, data flows, or repository ownership.
- Never expose API keys in README content, commands committed to a repository, source files, or image URLs. Examples may reference environment variables only.
- Every README draft must include a **Quick Start** section that shows the shortest verified path from availability or installation to a useful result. If that path cannot be verified from repository evidence or user confirmation, ask for the missing first-use details; do not invent, leave empty, or omit the section.
- When the first discovery scan finds an existing README, stop and ask the user to choose one handling mode: **1) Replace completely** — ignore all existing README information; **2) Replace with selected existing information** — rewrite while retaining only user-approved accurate content; **3) Extend existing README** — preserve the existing README and add or improve content in place. Do not infer the mode from the original request.
- Prefer questions with multiple explicit options. Use a selectable list whenever the decision can be reasonably anticipated; offer a free-form “Other” choice only when the available options cannot cover the user’s intent.
- Keep a clear separation between **Verified from repository**, **Confirmed by user**, **Uncertain**, and **Missing** information.
- Do not copy another repository’s wording, project-specific commands, branding, or content. Use only general information architecture and writing principles.
- Do not use emoji in generated README files. Keep visual guidance limited to verified image assets, badges, and source-backed ASCII diagrams.
- Center the header identity band by default: optional visual, project name, one-line positioning, language switch, and badges. Use `<h1 align="center">` for the title and a separate `<p align="center">` for each other block. Everything from the first `##` heading down stays left-aligned — never center headings, prose, tables, lists, code blocks, or ASCII diagrams. Follow the centered header standard in [README structure guidance](references/readme-structure.md#centered-header-standard).
- Include an architecture diagram only when the repository evidence or the user confirms its components, boundaries, and relationships. Architecture diagrams are ASCII Art in a fenced `text` block—**never Mermaid**.
- Include a usage example only when the user supplies or confirms the example’s prose, image/assets, code or commands, expected result, placement, and language. Do not turn an unverified idea into a public example.

## ASCII Architecture Diagram Standard

Use this standard only for a source-backed optional `##` Architecture section. Put it immediately after Highlights and before an optional Usage Example. Never use Mermaid, Mermaid fences, or Mermaid syntax.

### Allowed symbols

```text
boxes:       ┌─┐ │ └─┘
arrows:      ──▶  ◀──  ──▷  ↑ ↓ ←  →
double line: ═══  ║
labels:      Place a label on or above an arrow, for example ──[HTTP]──▶
```

### Layout examples

Single layer:

```text
┌─────────┐     ┌─────────┐     ┌──────────┐
│  Client │────▶│   API   │────▶│ Database │
└─────────┘     └─────────┘     └──────────┘
```

Grouped or layered:

```text
┌─────────────────────────────────┐
│             Backend             │
│  ┌──────────┐  ┌─────────────┐  │
│  │   Auth   │  │  Business   │  │
│  │ Service  │  │   Service   │  │
│  └──────────┘  └─────────────┘  │
└─────────────────────────────────┘
```

Labeled arrows:

```text
┌─────────┐  REST/HTTPS  ┌─────────┐  SQL  ┌──────────┐
│  Client │─────────────▶│   API   │──────▶│ Postgres │
└─────────┘              └─────────┘       └──────────┘
                               │
                          gRPC │
                               ▼
                         ┌─────────┐
                         │  Cache  │
                         │ (Redis) │
                         └─────────┘
```

### Diagram rules

- Use a fenced `text` block so GitHub preserves alignment.
- Keep box widths aligned and boxes on the same layer at the same height.
- Prefer a horizontal layout; switch to vertical only when the hierarchy needs it.
- Place arrow labels above or on the connecting line.
- Draw only verified or user-confirmed components, boundaries, and flows. Omit the entire section when those facts are missing.

## Workflow

### 1. Discover repository facts first

Perform a bounded scan. Do not read the entire codebase without a README-specific reason.

1. Determine whether the directory is a Git repository; inspect the root file list and, when available, the configured remote URL.
2. Read existing README variants, `LICENSE*`, contribution and security files, plus the docs index.
3. Read only manifests that are present, such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, or language-equivalent metadata.
4. Inspect CI, release/publishing, deployment configuration, examples, and public entry points only when needed to verify installation, first use, platform support, architecture, usage examples, or documentation links.
5. If any README variant exists, ask the user to choose its handling mode before drafting:
   - **1) Replace completely:** write a new README without using any information from the existing README.
   - **2) Replace with selected existing information:** write a new README, retaining only accurate existing content that the user approves.
   - **3) Extend existing README:** preserve the existing README structure and accurate content, then add or improve content in place.
6. Build a fact ledger before drafting:

| Status | Meaning |
|---|---|
| Verified from repository | Directly supported by a local file, manifest, CI configuration, or configured remote. |
| Confirmed by user | Explicitly supplied or approved by the user. |
| Uncertain | Plausible but not safe to state publicly without confirmation. |
| Missing | Needed for a desired section but not discoverable. |

If no remote repository can be verified, say so. Do not assume an owner, repository URL, public demo, release page, community, hosting provider, or architecture.

### 2. Load only applicable guidance

- Before selecting sections or composing prose, read [README structure guidance](references/readme-structure.md).
- When badges are requested or evaluated, read [badge guidance](references/badge-style.md).
- When images are requested, read [image guidance](references/image-generation.md).
- Before presenting a final draft and again before writing files, read [quality checklist](references/quality-checklist.md).
- After project type and language layout are known, read only the relevant template(s) in `templates/`.

### 3. Ask only for decisions that evidence cannot answer

Ask **one question at a time**. Present the decision as a list of explicit options whenever practical; include a free-form “Other” option only when necessary. Do not repeat information already verified or answered.

1. If an existing README was found during discovery, ask the user to choose the handling mode described above before asking later content preferences.
2. Ask for the language layout: English, English plus Simplified Chinese, or Chinese.
   - For bilingual output, `README.md` is the English primary GitHub landing page and `README.zh-CN.md` is the Chinese version.
   - For Chinese-only output, explain that GitHub displays root `README.md` by default and ask whether Chinese should be the primary page.
3. Ask whether the user wants Shields.io badge recommendations.
   - Offer explicit choices such as **include verified recommendations**, **omit badges**, or **Other**.
   - If the repository contains a verified `LICENSE*` file, recommend a linked static License badge by default as part of the verified badge set; let the user approve or remove it.
   - Recommend only badges whose claims and destinations are verifiable, then let the user approve, remove, or add items.
4. Ask whether to include an ASCII architecture diagram.
   - Offer **include a source-backed ASCII diagram**, **omit it**, or **Other**.
   - If included, confirm the components, group boundaries, relationships, and labels from repository evidence or the user before drawing it.
5. Ask whether to include a usage example.
   - Offer **include a supplied example**, **omit it**, or **Other**.
   - If included, collect confirmed example prose, image/assets, code or commands, expected result, preferred placement, and language. Verify local image paths before referencing them and never expose credentials.
6. Use the centered header by default. Ask only when the user requests a different look; offer **centered header with minimal HTML**, **plain left-aligned Markdown header**, or **Other**.
7. Ask whether imagery is wanted.
   - Offer **no image**, **use an existing asset**, or **generate a new image**.
   - If yes, ask whether existing assets are available.
   - If no assets are available, ask whether the visual should be icon only, icon plus one short line, or icon plus project name and one short line.
   - If the user chooses an OpenAI image service, ask for the API URL and API key (or the names of environment variables that already contain them) before generating anything. Do not guess an endpoint, model, response format, or output location.
   - Use [`scripts/generate-image.py`](./scripts/generate-image.py) for the generation request. Pass credentials through environment variables or process arguments only; never write them to the repository, README, prompt, image URL, or command committed to Git.
   - Verify the generated local asset before adding its path to a README. If generation fails, show the provider-neutral prompt and report the failure rather than inventing an image reference.
8. Ask whether to add a Star History chart.
   - Offer **include it**, **omit it**, or **Other**.
   - Include it only after user confirmation **and** only when a public GitHub `owner/repo` identifier can be verified from the remote URL or supplied by the user.
   - Place it after **Community & support** and immediately before **License**.
   - State that it embeds a third-party dynamic SVG for a public GitHub repository; omit it if the repository is private, the owner/repo is uncertain, or the user declines.
9. Ask only for remaining public information that cannot be verified: target audience, key emphasis, documentation site, demo, community, contribution route, FAQ, roadmap, citation, or security policy.

### 4. Compose the draft

Use the relevant structure and template, then remove every inapplicable section **except Quick Start**. A Quick Start must remain in every draft and use the shortest verified first-use path; if no such path exists, ask the user for it before presenting a final draft. Prefer short, evidence-led prose and a useful first-run experience over exhaustive feature lists.

When selected and supported, preserve this order near the beginning of every README:

```text
Highlights → optional Architecture → optional Usage Example → Quick Install → Quick Start
```

Before any file write, present:

1. A concise structural recommendation.
2. Complete Markdown draft(s) for each selected language file.
3. The fact ledger and list of user-confirmed details.
4. Proposed badges and each badge’s data source.
5. The source-backed ASCII architecture diagram when requested.
6. Usage-example content, provenance, and placement when requested.
7. Image placement and generation recommendations, when requested.
8. Star History placement and the verified `owner/repo`, when requested.
9. If a README already exists, an explicit **keep / move / merge / remove** summary.

### 5. Write only after explicit confirmation

A request to draft, improve, review, or show a README is **not** permission to write files. Write only after the user explicitly asks to write, update, replace, or save to named target paths.

Immediately before writing, state every target file and what will change:

- English: `README.md`.
- Bilingual: `README.md` and `README.zh-CN.md`.
- Chinese: use the user-confirmed primary path.
- Saved draft: only the user-specified path.

For existing files, retain useful, still-accurate content where possible. Do not silently discard content; explain material moves, merges, or removals. After writing, run the quality checklist against the actual files.

## Final report

Use this compact outcome format:

```text
Files changed:
- <path and purpose, or “None — draft shown in conversation only”>

Verified:
- <facts, commands, paths, links, or badge sources>

Needs confirmation:
- <unverified public information or manual checks>

Not included:
- <sections, badges, images, or charts omitted because they were unverified or declined>
```
