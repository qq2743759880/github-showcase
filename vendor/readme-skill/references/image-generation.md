# README Image Guidance

Read this guide only when the user wants a visual in the README.

## Ask before proposing or generating imagery

Determine:

1. whether the user wants a logo/icon, hero banner, product screenshot, architecture diagram, or demo GIF;
2. whether approved assets already exist;
3. whether the image should contain no text, an icon plus one short line, or an icon plus project name and one short line; and
4. where it will appear in the README.
5. whether the requested architecture view is a generated visual or a source-backed inline ASCII diagram.

Prefer verified local assets first, then user-provided assets, and generate a new visual only after approval. Verify local paths before referencing them, and never insert a speculative image URL. Product screenshots should show an actual UI or output.

Inline README architecture diagrams are not generated visuals: they must be source-backed ASCII Art in a fenced `text` block and must never use Mermaid. Follow the canonical standard in [`readme-structure.md`](./readme-structure.md#architecture-diagram). Use this guide only when the user wants an actual image asset such as an icon, banner, screenshot, generated architecture visual, or demo GIF.

Default recommendation: a concise icon plus no more than one or two short lines. Avoid dense, poster-like graphics, full feature lists, and UI mockups that claim nonexistent functionality.

| Asset type | Suitable placement |
|---|---|
| Logo / icon | Above or beside the title |
| Hero banner | Before the positioning statement |
| Product screenshot | After Quick Start or in a features section |
| Architecture diagram | Architecture or advanced use section |
| Demo GIF | After the related command or workflow |

## Concise prompt formula

Use confirmed project facts only. Keep the prompt short:

```text
Create a clean GitHub README visual for [project type].
Visual metaphor: [one core idea].
Style: [two or three adjectives]. Palette: [two or three colors].
Composition: [icon-centered or wide banner].
Text: [none, or exact short text under 12 words]. No dense UI, feature lists, paragraphs, logos of unrelated brands, or watermarks.
```

Image-model typography can be inaccurate. An icon-only image with a Markdown title is the most reliable option. If text is desired, use only confirmed wording and warn the user that they may need to replace rendered text in a design tool.

## OpenAI-compatible image service

Use this route only after the user explicitly chooses an OpenAI image service and provides an API URL and API key, or identifies environment variables that contain them. Do not guess a provider endpoint, model, response format, output format, or pricing. Never place the credential in a repository file, README, prompt, image URL, shell history, or commit.

The repository includes [`scripts/generate-image.py`](../scripts/generate-image.py). It uses Python's standard library and supports an OpenAI-compatible Images Generations endpoint. The script accepts either a complete endpoint or a base URL and adds `/v1/images/generations` when needed. It reads image data from either `data[0].b64_json` or `data[0].url`.

Pass credentials through environment variables:

```bash
export IMAGE_API_URL='https://example.invalid/v1/images/generations'
export IMAGE_API_KEY='replace-with-your-key'

python3 scripts/generate-image.py \
  --model gpt-image-2 \
  --prompt 'Create a clean GitHub README visual for a documentation skill. Visual metaphor: verified facts becoming a clear document. Style: minimal, technical, calm. Palette: midnight blue, cyan, white. Composition: wide hero banner. Text: readme-skill; Evidence before prose. No dense UI, feature lists, unrelated logos, or watermarks.' \
  --size 1536x1024 \
  --output assets/readme-skill-hero.png
```

The script also accepts `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `IMAGE_MODEL` as alternatives. Inspect `python3 scripts/generate-image.py --help` for all options. Verify the resulting local file before adding it to a README. If the request fails or the provider uses a different API contract, report the error and use the provider-neutral prompt instead of inventing a compatible response.

## If OpenAI image access is unavailable

Offer the provider-neutral concise prompt first. Ask which image tool or provider the user already uses. Do not assume an account, API key, endpoint, output format, or pricing. Provide provider-specific commands only after the user names the provider or explicitly asks for an alternative.
