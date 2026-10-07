# Architecture and workflow diagrams

This workflow owns the meaning and evidence of F03 architecture and F04 user or system workflows. A renderer owns only executable diagram syntax and image generation. Renderer success does not establish C4 modeling, user flow coverage, source truth, or a complete vendor invocation.

## Inputs and scope decision

Read the current run's approved evidence and `architecture_spec` / `workflow_spec`. Record the target reader, the question each diagram answers, and the evidence for every proposed node and relationship. Source evidence may support implemented behavior, design intent, or an unknown. Keep those states visible in the diagram and its explanation. The main Skill, binding, and project contract remain the authority for output and authorization.

Use a bounded scope decision before loading architecture expertise:

1. **Software architecture:** the source establishes a running or deployable application, service, library runtime, tool process, database, or a proposed deployment with explicit design evidence. Invoke the locked `c4-architecture` entry and required syntax/common-mistakes references. The complete base output is Context plus Container, at their separate abstraction levels.
2. **Knowledge, document, method, or design organization:** the nodes are documents, concepts, stages, rules, or relationships without a genuine deployable boundary. Use an evidence-backed overview from the internal workflow. Do not label document folders, references, methods, or phases as C4 containers. Record `C4_NOT_APPLICABLE` and its reason; that does not skip the useful architecture overview.
3. **Mixed project:** apply C4 to the actual software boundary only. Explain knowledge or design organization separately. A project marked `design` may contain a proposed software deployment; label it as proposed, never as implemented. A project marked `code` does not justify adding containers unsupported by its source.

An Agent Skill is usually a method loaded by a host Agent. The Skill file and adapter are data; a method step is not a process. A C4 view is appropriate only when the execution boundary is evidenced: host Agent process, actual Python or Node tool processes, their files, and external systems. Avoid modeling every sub-skill as a deployable container. When the host execution model is unknown, keep the method overview and record the unknown instead of fabricating software architecture.

## F03: complete C4 software lane

Follow the original skill workflow: understand scope, analyze the source, generate the appropriate diagrams, and write explanatory documentation.

1. Read the locked C4 `SKILL.md`, `references/c4-syntax.md`, and `references/common-mistakes.md`. Read `advanced-patterns.md` only when the source contains the relevant microservice, event, or deployment pattern. Record exact resource paths in the trace. Do not infer runtime support from a documentation catalog.
2. Identify people, the system of interest, and external systems from evidence. Create one **Context** diagram. External services remain black boxes. Explain what the system does for each actor and how each relationship crosses its boundary.
3. Identify the actual applications, service/tool processes, and data stores within the system boundary. Create a separate **Container** diagram. A container is deployable or runnable; modules, shared libraries, Skill methods, adapter content, and configuration files are not separate applications. Technology labels come from manifests or source evidence; use unknown when not established.
4. Use real Mermaid C4 syntax (`C4Context`, `C4Container`) and preserve one level per source file. Retain `assets/c4-context.mmd` and `assets/c4-containers.mmd`; document them in `docs/architecture/c4-context.md` and `docs/architecture/c4-containers.md`. Approved filenames may differ, but each diagram and level must remain independently editable and identifiable.
5. Every element has name, type, description, and technology where applicable. Each arrow is unidirectional, names the real action, and includes protocol or technology where the evidence provides it. Explain **every relationship** in a table or prose: source node, target node, action/data, protocol if known, evidence location, and status (implemented/designed/inferred/unknown). Node-only mapping is insufficient.
6. Keep each diagram below 20 elements, use meaningful aliases and concise labels, and give it a specific title. Split a crowded view on an actual boundary. Keep names and notation consistent across the set and explain the legend. Preserve forbidden relationships from the approved spec.
7. Add **Component** only when evidenced internal responsibilities answer the developer's question. Add **Dynamic** only for a complex, real request or interaction that benefits from a numbered trace. Add **Deployment** only when real or explicitly proposed infrastructure nodes and deployment facts exist. These are conditional branches, not unused obligations in the default coverage denominator. Record the trigger or `not applicable` reason for each.
8. Render each C4 semantic/compatibility source with the pinned Mermaid CLI using the existing `scripts/render-c4.mjs`. The wrapper name does not restrict it to C4, but C4 must use a renderer that actually supports C4. An experimental syntax warning is a compatibility risk to verify, not evidence that rendering cannot work. Fix errors with a minimal failing statement and rerender; never silently downgrade a C4 invocation to a generic flowchart while retaining a C4 success label.
9. Author and finalize separate Archify architecture views under [archify.md](archify.md), preserving every C4 level and relationship. Check the original C4 quality rules: deployable vs component separation, audience, external black boxes, real topic/queue boundaries if relevant, no deployment details smuggled into the container level, labels/types/protocols, titles, consistent notation, and readable layout. Inspect the rendered images. Exit zero and a nonempty file alone are insufficient.

Publish a navigation page, normally `docs/architecture/index.md`, with links to each rendered image, editable source, explanatory level document, and applicable dynamic/deployment view. Give the reader the system boundary before implementation details. Record unresolved architecture facts in the private trace; include only user-relevant limitations in the public explanation.

## F04: evidence-backed interactive workflow

Use the full Integrated Archify workflow in [archify.md](archify.md). Preserve entry, normal steps, alternate/error outcomes, recovery and postconditions from actual source. Generic process diagrams use Workflow v2; other modes are selected by the reader question. Mermaid may remain an explicitly justified internal syntax/compatibility source, not the default public presentation. Never imply app screens or software containers from method steps.

## Syntax references and renderer contract

Mermaid syntax is provided by the pinned Mermaid runtime, not by an additional integrated producer. The standalone Mermaid catalog is not vendored. For the C4 lane, read the retained C4 syntax reference and record it. For internal flowchart, sequence, or state views, use the installed runtime parser and a minimal successful rendering to establish syntax support. The base forms are `flowchart TB` with labeled decisions and arrows, `stateDiagram-v2` with named states and transitions, and `sequenceDiagram` with participants and messages. Keep the chosen source form and runtime validation in the trace. A diagram catalog or a claim of support does not replace executing the current version's parser.

Run from the product root or invoke the wrapper by absolute path:

```text
node scripts/render-c4.mjs -i <approved-source.mmd> -o <approved-rendered.svg>
```

The existing wrapper fixes Mermaid CLI version and confines browser profile/cache to the checkout. Record the actual version, executable, command, exit code, output path, and image inspection in the private trace. Output directories must already be approved. Runtime installation follows the runtime binding; do not switch engines to avoid a semantic or safety rejection. The optional pretty-mermaid utility has a different engine and supported-type matrix and is not a workflow/C4 fallback. It is unnecessary when the installed Mermaid CLI meets the required output.

## Completion and evidence

Keep a private `trace/diagrams/` receipt for each selected view:

- Input and scope: project question, target reader, source revision or content identity, evidence paths, design/implementation status, and C4 applicability.
- Resources: locked entry plus the exact required and chosen reference paths actually read.
- Meaning: node and **every relationship** mapping, forbidden edges, normal/alternate/error outcomes, and conditional-level trigger or reason for no use.
- Execution: source and rendered output paths, pinned renderer command/version/exit, syntax defects and rerender results.
- Inspection: actual image viewed, titles, labels/typography/contrast, clipping/overlap, arrows, legend, and semantic check against the inputs. If a view cannot be inspected, mark it unverified.
- Consumption: all selected images and editable sources are linked from final README or docs; the root composer writes the consumption ledger. No orphan selected asset may pass.

A selected C4 lane completes only with the original model, Context plus Container and any triggered optional views, explanatory documentation, relationship evidence, successful render, visual inspection, and final consumption. A generic workflow completes with every evidenced step and alternate/error outcome represented, image/source validated and inspected, and the final reader-facing document consuming them. Missing evidence is an explicit limitation; a successful renderer does not erase it.
