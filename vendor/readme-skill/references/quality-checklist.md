# README Quality Checklist

Use this checklist before showing a final draft and again before any file write.

## Facts and executability

- [ ] Project name, short description, installation command, runtime requirements, API/CLI syntax, configuration keys, paths, and license terms are verified from the repository or confirmed by the user.
- [ ] Uncertain claims are explicitly marked for confirmation or omitted.
- [ ] Quick Install uses an actual supported package manager, installer, or source-build route.
- [ ] Quick Start is present and non-empty in every README.
- [ ] Quick Start uses real entry points, flags, imports, environment variables, and expected behavior.
- [ ] If no verified first-use path exists, the draft is blocked pending user confirmation rather than omitting or inventing Quick Start.
- [ ] Code fences have the appropriate language label.
- [ ] README URLs, local document links, image paths, package references, and community links exist or are user-confirmed.
- [ ] API keys are represented only by environment variable names; no secret is embedded in text, code, URL, or asset.

## Architecture and usage examples

- [ ] No emoji appears anywhere in the README, including headings, table rows, prose, badges, code blocks, image alt text, and ASCII diagrams.
- [ ] Architecture is included only when its components, boundaries, and relationships are verified or user-confirmed.
- [ ] Architecture immediately follows Highlights, uses an aligned ASCII diagram inside a `text` code fence, and contains no Mermaid fence, syntax, or speculative flow.
- [ ] A Usage Example immediately follows Architecture, or follows Highlights when Architecture is omitted.
- [ ] Each usage example contains only confirmed or verified prose, local/verified image paths, code or commands, and expected outcome; no secret appears in example material.
- [ ] Example images have meaningful alt text and example code/commands are executable or explicitly identified as illustrative only when the user confirmed that scope.

## Badges and Star History

- [ ] Every badge has a verified source and accurately represents it.
- [ ] When a verified `LICENSE*` file exists and the user requested badge recommendations, the default badge proposal includes a linked static License badge unless the user declined it.
- [ ] Static badge labels are percent-encoded and palette choices match the badge guide.
- [ ] Dynamic badges use a verified endpoint; no endpoint was guessed.
- [ ] Star History is included only after user approval and verification of a public GitHub `owner/repo`.
- [ ] The Star History section comes after Community & support and immediately before License.
- [ ] The Star History code uses the verified identifier and is omitted for private or uncertain repositories.

## Presentation and language layout

- [ ] Unless the user chose a plain Markdown header, the identity band is centered: optional visual, `<h1 align="center">` title, and a separate `<p align="center">` for positioning, language switch, and badges.
- [ ] The centered header uses `<a href="...">` rather than Markdown links, keeps all badges on one line in one paragraph, and separates HTML blocks with a blank line.
- [ ] Centering stops at the header; no `##` heading, prose, table, list, code block, or ASCII diagram is centered.
- [ ] A centered header emits either `<h1 align="center">` or `# Title`, never both.
- [ ] Heading hierarchy is logical; no empty sections remain.
- [ ] Tables are short and remain understandable on narrow screens.
- [ ] Each image has meaningful alt text; no key information exists only inside an image.
- [ ] HTML is limited to GitHub-compatible structural elements; no JavaScript, CSS, or `iframe` is used.
- [ ] The README links to detailed docs rather than repeating a complete manual.
- [ ] In bilingual mode, language-switch links are reciprocal and correct.
- [ ] In bilingual mode, both files contain corresponding Quick Start sections and their technical identifiers match.
- [ ] In bilingual mode, Architecture and Usage Example inclusion decisions, diagram topology, example code, expected behavior, images, commands, URLs, paths, versions, and license identifiers remain factually aligned. Natural prose may differ.

## Existing README and write gate

When an existing README is present, before drafting ask the user to choose one handling mode:

1. **Replace completely:** ignore all information in the existing README.
2. **Replace with selected existing information:** create a new README while retaining only accurate content the user approves.
3. **Extend existing README:** preserve accurate existing content and add or improve content in place.

Then produce an explicit list of content to **keep**, **move**, **merge**, and **remove**, with reasons tied to current repository facts.

Before writing any file, verify all of the following:

- [ ] The user explicitly asked for a write or update.
- [ ] When a README already existed, the user selected its handling mode before drafting.
- [ ] Questions with predictable decisions offered explicit selectable options; free-form input was reserved for uncovered cases.
- [ ] Every target path is named.
- [ ] The user can see what is being replaced or reorganized.
- [ ] No image references point to absent assets.
- [ ] Dynamic badges use a verified endpoint.
- [ ] Any Star History chart uses a verified public owner/repo identifier.

If any checkbox fails, keep the output as an in-conversation draft and state what blocks writing.

## Exceptions

| Situation | Required response |
|---|---|
| Directory is not a Git repository or remote is unavailable | State the reduced verification scope; continue from local files and user input. |
| Conflicting manifests or configurations | Identify the conflicting files and ask which public behavior to document. |
| Existing README | Ask the user to choose replace completely, replace with selected existing information, or extend existing README before drafting. |
| Absent license | Omit the license section and badge; invite the user to choose or add one. |
| No verified Quick Start | Ask for the missing first-use path; do not finalize a README without a Quick Start section. |
| No verified architecture | Omit the ASCII Architecture section rather than inferring components or flows. |
| No confirmed usage example | Omit the Usage Example section rather than inventing prose, images, code, commands, or outcomes. |
| No verified docs, community, or demo | Omit the corresponding section and badge instead of creating a placeholder. |
| Code-versus-README contradiction | Show the conflict, treat code/configuration as the stronger source, and ask before making an external claim. |
| Image unavailable or path unknown | Give placement guidance only; do not add an image reference. |
| Star History owner/repo unavailable or repository private | Omit the chart and explain why. |

## Completion report

Report the result in exactly these categories:

```text
Files changed:
- <path and purpose, or “None — draft shown in conversation only”>

Verified:
- <facts, commands, paths, links, badge sources, or owner/repo>

Needs confirmation:
- <unverified public information or manual checks>

Not included:
- <sections, badges, images, or charts omitted because they were unverified or declined>
```
