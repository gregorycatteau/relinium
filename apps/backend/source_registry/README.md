# Source Registry

`source_registry` stores the enterprise data sources that Relinium should observe later.

The v0.1 scope is deliberately narrow:

- declare local, network, server, cloud/GED, or other sources;
- store a label, non-secret locator reference, status, read rules, exclusions, and redacted notes;
- hash the locator reference for comparison and audit;
- keep every source read-only by default;
- record redacted audit events for source lifecycle actions.

## No Secrets In V0.1

This app must not store passwords, API keys, OAuth tokens, cookies, or bearer tokens.
Validation rejects obvious secret-like values such as `password=`, `token=`, `api_key=`, `secret=`, and `Bearer`.

Future connector credentials must use encrypted backend storage with rotation, access audit, and operator/admin separation.

## Future Scanner Link

The registry prepares source declarations for the future Go scanner, but does not run it automatically.

Planned command shape:

```bash
relinium-cartography-scan --root <source> --mode presence --out <snapshot.ndjson>
```

Scanner output should remain a derived snapshot and must not rewrite append-only event streams.
