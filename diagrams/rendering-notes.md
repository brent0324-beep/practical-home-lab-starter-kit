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

- PNG for README screenshots, blog images, and thumbnails.
- SVG for PDF or scalable documentation when the platform supports it.

## README and Blog Usage

Use diagrams to support the text, not replace it. A good flow is:

1. Show the full topology.
2. Explain remote access.
3. Explain the Ansible control path.

Keep rendered exports in a predictable directory if they are added later, and
continue to keep Mermaid source files in `diagrams/`.
