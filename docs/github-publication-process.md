# GitHub Publication Process

Use this process when you are ready to publish the repository to GitHub. This
document is intentionally written as a checklist; do not push until the final
review is complete.

## 1. Confirm Local Branch

The default branch should be `main`.

```bash
git branch --show-current
```

If the branch is still `master`, rename it locally before publishing:

```bash
git branch -m master main
```

## 2. Create the GitHub Repository

Create an empty GitHub repository through the GitHub UI or GitHub CLI.

Recommended settings:

- Repository name: `practical-home-lab-starter-kit`
- Visibility: public when ready
- Do not initialize with a README, license, or gitignore if this local repo
  already contains those files.
- Keep issues enabled if you want public documentation feedback.

## 3. Set the Remote

After creating the empty GitHub repository, add the remote.

Example HTTPS pattern:

```bash
git remote add origin https://github.com/YOUR-USER/practical-home-lab-starter-kit.git
```

Example SSH pattern:

```bash
git remote add origin git@github.com:YOUR-USER/practical-home-lab-starter-kit.git
```

Use your own GitHub account or organization name.

## 4. Final Validation

Run the full local check set:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
bash -n scripts/validate.sh scripts/redaction-check.sh scripts/package-release.sh
git diff --check
```

Review the README, diagrams, templates, and release notes manually. The scripts
are guardrails, not a full security review.

## 5. Confirm Release Package

Create the local archive:

```bash
./scripts/package-release.sh
```

Confirm it exists:

```bash
ls -lh dist/
```

Do not commit files under `dist/`.

## 6. Push Main

After final review, push the default branch:

```bash
git push -u origin main
```

## 7. Create the v0.1.0 Tag

Create a local tag after the release commit is reviewed:

```bash
git tag v0.1.0
```

Push the tag only when you are ready to publish it:

```bash
git push origin v0.1.0
```

## 8. Optional GitHub Release

Create a GitHub release from the `v0.1.0` tag.

Optional release assets:

- `dist/practical-home-lab-starter-kit-v0.1.0.tar.gz`

Before uploading the archive, inspect it to confirm it excludes `.git`, `dist/`,
and local workflow metadata.

## 9. Post-Publication Review

After publication:

- Confirm README rendering.
- Confirm Mermaid diagrams render.
- Confirm issue templates appear.
- Confirm the repo description and topics are set.
- Confirm no generated `dist/` archive was committed.
