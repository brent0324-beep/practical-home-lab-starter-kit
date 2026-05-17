# Diagram Strategy

The diagrams in this directory are source assets for the public README, blog
post, future PDF bundle, and short walkthrough video. They use Mermaid so the
architecture can stay versioned as text and render cleanly on platforms that
support Mermaid.

## Files

- `lab-topology.mmd` shows the full starter lab architecture.
- `remote-access-flow.mmd` focuses on the approved remote access path.
- `ansible-control-flow.mmd` shows how Ansible reaches virtual network nodes.

## Usage

Use these diagrams as the canonical visual reference for:

- README architecture explanations.
- Blog post screenshots or embedded Mermaid blocks.
- PDF bundle figures.
- Video walkthrough scenes.
- Future rendered PNG or SVG exports.

## Sanitization Rules

- Use private lab address ranges only.
- Use placeholder hostnames such as `lab-host`, `lab-r1`, and `lab-sw1`.
- Do not include real public-facing addresses.
- Do not include credentials, tokens, PSKs, keys, account details, or private
  environment data.

## Rendering Notes

Mermaid files can be rendered by GitHub, many Markdown editors, and Mermaid CLI.
If exporting images for a PDF or video, review the rendered output for readable
labels, correct direction, and sanitized content before publishing.
