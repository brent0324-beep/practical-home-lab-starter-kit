# Diagram Rendering Notes

The source diagrams in this repo use Mermaid so architecture visuals can stay
versioned as text.

## Mermaid Rendering Guidance

- Keep labels short enough to read at README width.
- Prefer simple `flowchart` diagrams for GitHub compatibility.
- Keep source diagrams as the canonical editable version.
- Review rendered diagrams after every meaningful topology change.

## GitHub Rendering Notes

GitHub can render Mermaid in Markdown code blocks and may display `.mmd` source
files as text. For public presentation, link to the `.mmd` files and optionally
include rendered screenshots later.

Before relying on a diagram in the README:

- Preview it in GitHub.
- Confirm labels do not overlap.
- Confirm private lab addresses are examples only.
- Confirm no sensitive data appears in labels.

## Export Recommendations

For blog posts, video, or PDF usage, export diagrams from a trusted Mermaid
renderer after reviewing the source.

Recommended exports:

- SVG for README diagrams, documentation, PDF source material, and any place
  where crisp scaling matters.
- PNG for social cards, blog thumbnails, video thumbnails, and platforms that do
  not display SVG reliably.

When exporting Mermaid diagrams later:

1. Render from the sanitized `.mmd` source file.
2. Review labels for readability at README width.
3. Confirm no real addresses, hostnames, credentials, keys, tokens, PSKs,
   account data, or private details appear.
4. Save reviewed exports under `assets/diagrams/`.
5. Keep filenames descriptive and stable so README links do not churn.

SVG is usually best for diagrams because text and lines stay sharp. PNG is
better when a platform strips SVG, when you need a thumbnail, or when you want a
fixed raster image for a video editor.

## README and Blog Usage

Use diagrams to support the text, not replace it. A good flow is:

1. Show the full topology.
2. Explain remote access.
3. Explain the Ansible control path.

Keep rendered exports in a predictable directory if they are added later, and
continue to keep Mermaid source files in `diagrams/`.
