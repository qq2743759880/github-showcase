# Install Commands

Tools, skills, and MCPs that ux-flow-designer can propose to the user.

## Auxiliary Skills

| Skill | Purpose | Phase | Install Command |
|-------|---------|-------|-----------------|
| ui-ux-pro-max | Downstream: visual design | After | `npx skills find ui-ux-pro-max` |
| product-manager-toolkit | Upstream: PRD | Before | `npx skills find product-manager-toolkit` |
| brainstorming | Ideation if no PRD | Before | `npx skills find brainstorming` |

## Figma MCP (only if user requests Figma)

| MCP | Purpose | Install Command |
|-----|---------|-----------------|
| Figma Dev Mode MCP Server | Code to Canvas — bidirectional Figma integration | Enable in Figma desktop preferences, then: `claude mcp add --transport sse figma-dev-mode-mcp-server http://127.0.0.1:3845/sse` |

## Browser Preview MCP

| MCP | Purpose | Install Command |
|-----|---------|-----------------|
| Chrome DevTools MCP | Browser automation for wireframe preview and Figma export | `claude mcp add chrome-devtools npx chrome-devtools-mcp@latest` |
