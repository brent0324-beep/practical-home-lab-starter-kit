# labctl Spec Reference

This is the native input contract used by `./scripts/labctl`.

## Top-level fields

- `name` (required): DNS-safe lab identifier; used for rendered topology name.
- `description` (optional): Human text.
- `api_version` (optional): Reserved version marker.
- `mgmt_ipv4_subnet` (optional): Containerlab management subnet, for example
  `172.30.90.0/24`. This may use profile variables.
- `variables` (optional): Map merged with an optional profile.
- `nodes` (required): Map of node names to node specifications.
- `links` (required): List of link objects, each with exactly two endpoints.

## Node fields

- `kind` (required): Containerlab node kind string (for example `linux`).
- `image` (required): Public container image reference.
- `mgmt_ipv4` (optional): Bare management IPv4 host address for the node.
  If a prefix is supplied in input, the renderer strips it and validates the
  resulting host inside `mgmt_ipv4_subnet`.
- `startup_config` (optional): Relative startup path. Absolute paths and `..` are rejected.
- `binds` (optional): List of bind strings (`host:container:ro` or `host:container`).
  Host source paths must be relative and may not include parent traversal.
- `env` (optional): Environment map passed to the node.

## Link fields

- `endpoints` (required): Exactly two strings in the form `node:interface`.

## Profile merge

- If `--profile` is supplied, profile `variables` are merged over `spec.variables`.
- Template interpolation uses `{{ variable_name }}` in any string value.
- Missing variables cause explicit errors before rendering.

## Output

- Validation output is `labctl validate`.
- Render output is a containerlab topology:

```yaml
name: two-node-ptp
topology:
  nodes:
    ...
  links:
    ...
```

- `deploy` renders to `lab.clab` path (or explicit `--output`) then calls:
  `containerlab deploy -t <path>`.
