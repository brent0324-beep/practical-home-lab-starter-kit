# Local Release Process

Use this process to prepare a local v0.1 release package without pushing to a
remote repository.

## 1. Review Scope

Confirm the release includes only sanitized public starter-kit content:

- README and documentation.
- Templates and Ansible examples.
- Diagrams and video planning docs.
- Product planning docs.
- GitHub readiness assets.
- Validation and packaging scripts.

Do not include real lab inventories, real configs, private keys, tokens, PSKs,
account data, public-facing infrastructure addresses, or private environment
details.

## 2. Validate

Run:

```bash
./scripts/validate.sh
```

This confirms required files exist and contain expected starter-kit content.

## 3. Redaction Review

Run:

```bash
./scripts/redaction-check.sh
```

Then manually review examples, diagrams, and templates. The script is a
guardrail, not a complete security review.

## 4. Syntax and Whitespace Checks

Run:

```bash
bash -n scripts/validate.sh scripts/redaction-check.sh scripts/package-release.sh
git diff --check
```

Fix all issues before packaging.

## 5. Package Locally

Run:

```bash
./scripts/package-release.sh
```

The package script creates a `.tar.gz` archive under `dist/` and excludes `.git`
and `dist/` from the archive. The `dist/` directory is ignored by Git.

## 6. Confirm Archive

List the archive:

```bash
ls -lh dist/
```

Optionally inspect the contents:

```bash
tar -tzf dist/practical-home-lab-starter-kit-v0.1.0.tar.gz | head
```

## 7. Commit

Commit release workflow changes locally after checks pass.

## 8. Tagging

Optional local tag:

```bash
git tag v0.1.0
```

Only tag after reviewing the commit. Do not push tags unless you intentionally
want to publish them.

## 9. Optional Remote Push

Remote push is optional and should happen only after final review:

```bash
git push origin main
git push origin v0.1.0
```

Do not push from this process unless publishing is explicitly approved.
