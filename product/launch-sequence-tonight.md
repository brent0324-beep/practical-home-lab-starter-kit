# Launch Sequence Tonight

Use this order for a practical first public launch.

## 1. Push Main

Run final local checks first:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
bash -n scripts/*.sh
git diff --check
```

Then push:

```bash
git push origin main
```

## 2. Review GitHub README

After pushing:

- Confirm README renders cleanly.
- Confirm SVG placeholders render.
- Confirm Mermaid source links work.
- Confirm all internal links resolve.
- Confirm no `dist/` archive is committed.

## 3. Add Topics and About Text

Use `product/github-repo-description.md` for:

- Short description.
- About text.
- Suggested topics.
- Pinned repo wording.

## 4. Publish LinkedIn Post

Use `product/linkedin-launch-post-v2.md` or adapt it slightly.

Keep the post practical:

- Free starter repo.
- Linux, GNS3, Ansible, remote access, repeatable workflow.
- Sanitized examples.
- No hype or guaranteed outcomes.

## 5. Optionally Share Reddit Later

Use `product/reddit-value-first-post.md`.

Share later only if the community rules allow it. Lead with lessons learned and
ask for feedback rather than pushing the link.

## 6. Defer Paid Bundle

Wait on the paid bundle until there are enough polished assets:

- Screenshots.
- Rendered diagrams.
- PDF workbook.
- Printable checklists.
- Implementation worksheets.
- Walkthrough companion material.
