# README Structure and Writing Guide

Use this guide before choosing sections or composing prose. It defines a flexible reading flow, not a mandatory checklist, **except that every README must include a verified Quick Start section**. Delete unsupported optional sections. If no verified first-use path is available, ask the user for it rather than omitting Quick Start.

## Reading flow

Use this order when the corresponding information genuinely exists:

```text
centered header: optional visual
→ centered project name and one-sentence positioning
→ centered language links and verified badges
→ left-aligned value proposition
→ 3–6 benefit-led highlights
→ optional ASCII architecture diagram
→ optional usage example
→ Quick Install
→ Quick Start
→ commands or API example
→ configuration, integrations, or advanced architecture details
→ task-organized documentation links
→ contributing when supported
→ community when verified
→ optional Star History chart when confirmed and owner/repo is verified
→ license when present
```

Readers should understand the project before being asked to configure it. They should be able to reach a first useful result before being sent to advanced documentation.

## Section rules

### Positioning and value

A one-sentence positioning statement says:

1. what the project is;
2. who it serves or what situation it addresses; and
3. one factual differentiator.

Avoid unverified superlatives such as “best,” “fastest,” “production-ready,” or “industry-leading.” Prefer concrete language over slogans.

### Headings

Write plain text headings. Do not use emoji in headings, table rows, prose, badges, code blocks, image alt text, or ASCII diagrams.

### Highlights table

Use a table only when it makes comparison easier. Keep it to 3–6 rows. Each row leads with a user outcome and follows with a verified technical basis or relevant use case.

```markdown
| Highlight | Why it matters |
|---|---|
| <Verified capability> | <Reader benefit grounded in evidence> |
```

Do not make a long feature inventory masquerade as highlights.

### Architecture diagram

An Architecture section is optional. Include it only when repository evidence or the user confirms its components, group boundaries, and relationships.

- Place it immediately after Highlights and before an optional Usage Example.
- Use only a fenced `text` block containing ASCII Art. **Never use Mermaid**, Mermaid fences, or Mermaid syntax.
- Follow the canonical box, arrow, label, grouping, and alignment rules in [`SKILL.md`](../SKILL.md#ascii-architecture-diagram-standard).
- Keep same-layer boxes equal in height, align box widths, prefer horizontal flow, and move to vertical layout only when hierarchy needs it.
- Omit the entire section rather than drawing speculative components or flows.

### Usage example

A Usage Example section is optional. Place it immediately after Architecture; when Architecture is omitted, place it immediately after Highlights.

Include only content supplied or confirmed by the user, or otherwise verified from the repository:

- concise explanatory prose;
- existing or generated local image assets with meaningful alt text;
- real code or commands;
- the expected result or validation outcome;
- the requested placement and language layout.

Do not turn a proposed workflow, screenshot, command, output, or benchmark result into a public example without evidence. Keep a broad Usage Example distinct from a project-specific API example: include both only when each helps a different reader task.

### Quick Install

Provide the lowest-friction **verified** installation route. Use a copyable command and state prerequisites, supported platform constraints, or required runtime immediately after it. Do not publish a package-manager command merely because the project uses a language commonly distributed that way.

### Quick Start

Show the shortest verified path from availability or installation to a useful result. This section is required in every generated README. Keep code/commands small, label fences correctly, and explain expected behavior without inventing output. If the repository and user provide no verifiable first-use path, ask for that information before finalizing the draft; do not delete, leave empty, or replace the section with generic instructions.

### Commands, APIs, and deployment

Choose content based on the project type:

| Project type | Include | Exclude unless verified |
|---|---|---|
| CLI or agent tool | Command table or slash-command table with real command syntax | SDK/API snippets not supplied by the repository |
| Library or SDK | Minimal import and call example based on public API | CLI command section |
| Web service | Verified local run path or documented deployment route | Deployment/support claims without documentation |
| General application | Supported installation or launch path | Architecture diagrams without source facts |

Never force every project into every category.

### Documentation navigation

Use a task-organized table, not a raw list of folders:

```markdown
| Topic | What it covers | Link |
|---|---|---|
| <Reader task> | <Short factual description> | [Open documentation](./docs/<verified-path>.md) |
```

Order items by the likely reader journey: start, use, configure, integrate, contribute, then reference. Link to detailed docs instead of attempting to duplicate a full manual.

### Community, Star History, and license

Include community only when a functioning public channel is verified or confirmed. If the user confirms a Star History chart and an `owner/repo` identifier is verified, place this section after community and before license:

```markdown
## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=OWNER%2FREPOSITORY&type=Date)](https://star-history.com/#OWNER/REPOSITORY&Date)
```

Replace `OWNER/REPOSITORY` with the verified public identifier. Explain only when relevant that the chart is a third-party dynamic SVG. Do not include the chart for a private repository or an uncertain identifier.

Keep the license ending concise: name the actual license only when a license file or user confirmation supports it, and link to that real file.

## Bilingual layout

For bilingual projects, English is the primary GitHub landing page:

```text
README.md        English primary GitHub landing page
README.zh-CN.md  Simplified Chinese technical rewrite
```

Put a reciprocal language switch near the top of both files:

```markdown
[English](./README.md) | [简体中文](./README.zh-CN.md)
```

The Chinese version is natural technical writing, not sentence-by-sentence translation. Both files must include corresponding verified Quick Start sections. Keep commands, code blocks, environment variable names, URLs, file paths, version numbers, license identifiers, architecture component labels, image paths, and usage-example identifiers factually identical across language versions. Keep the selected inclusion/omission decision and section order aligned for Architecture and Usage Example.

## Centered header standard

Center the header block by default. It covers only the identity band at the very top: optional visual, project name, one-line positioning, language switch, and badges. Body content starts at the first `##` heading and is always left-aligned.

Emit the blocks in this order, skipping any that lack evidence:

```html
<p align="center">
  <img src="./assets/<verified-image>.png" width="320" alt="<meaningful description>">
</p>

<h1 align="center">Project name</h1>

<p align="center">One-line positioning statement.</p>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="<verified destination>"><img src="<verified badge URL>" alt="<factual label>"></a>
</p>
```

Rules for the centered header:

- Use `<h1 align="center">` for the title instead of `# Project name` when the header is centered. Do not emit both.
- Keep each block in its own `<p align="center">`: positioning, language switch, and badges do not share one paragraph.
- Put every badge on one line inside a single centered paragraph so they render as one row.
- Leave one blank line between HTML blocks so GitHub does not merge them.
- A centered image needs an explicit `width` when the source asset is large; a square icon reads well at 200–320px.
- Inside a centered header, links use `<a href="...">`, not Markdown link syntax.
- Keep the header short. Anything longer than one positioning line — value proposition, requirements, install notes — belongs in left-aligned body text below.
- Stop centering after the header. Never center `##` headings, prose, tables, lists, code blocks, or ASCII diagrams; centered code and diagrams lose their alignment.
- When the user prefers plain Markdown, use `# Project name` with left-aligned positioning, language switch, and badges instead. Offer this as an explicit alternative rather than assuming it.

## GitHub-compatible layout

Markdown is the default for body content; HTML appears only in the centered header described above. Limited use of `<p>`, `<img>`, `<a>`, `<h1>`, and `align="center"` is acceptable there. Do not use JavaScript, embedded CSS, `iframe`, scripted widgets, or visual-only essential information. Every image needs meaningful alt text, and core explanations must exist in text.
