# Bilingual README Layout

Use two files for a bilingual repository rather than duplicating every section in one long document:

```text
README.md        English primary GitHub landing page
README.zh-CN.md  Simplified Chinese technical rewrite
```

Put this near the top of both files:

```markdown
[English](./README.md) | [简体中文](./README.zh-CN.md)
```

## Parity rules

- If an existing README is detected, ask the user to choose: replace it completely, replace it while selectively retaining approved information, or extend it in place.
- Prefer selectable options for every user decision; use free-form input only when anticipated options cannot cover the request.
- Write the English README first so the GitHub landing page is complete on its own.
- Rewrite the Chinese version naturally; do not translate sentence by sentence when that harms clarity.
- Both files must use the same initial section order when the sections apply: Highlights → optional Architecture → optional Usage Example → Quick Install → Quick Start.
- Make the same inclusion/omission decision for Architecture and Usage Example in both files.
- Do not use emoji in either language file.
- Use the same header treatment in both files: if one centers the identity band, so does the other, with the same visual, badge set, and block order.
- Architecture diagrams must be the same source-backed topology with aligned technical labels and identifiers in fenced `text` blocks. Never use Mermaid in either language file.
- Usage Examples must use the same confirmed or verified code, commands, URLs, paths, image assets, expected result, and technical identifiers. Natural prose may differ.
- Keep commands, code blocks, environment variable names, URLs, paths, version numbers, badge destinations, Star History owner/repo identifiers, and license identifiers factually identical.
- Both language files must contain corresponding, non-empty, verified Quick Start sections; if the first-use path is missing, ask the user instead of finalizing either file.
- Verify both language-switch links after files are written.
- Do not create either file until the user explicitly asks to write or update the README.
