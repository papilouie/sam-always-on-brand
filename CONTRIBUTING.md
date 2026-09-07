# Contributing

Keep changes scoped to SAM's approved workflow. Update canonical guidance in `packages/sam-aobpg/references/`; do not hand-edit generated release ZIPs.

Before proposing a change:

1. Add or update a behavioral scenario when behavior changes.
2. Validate Brand Packs and Campaign Packs.
3. Run the automated tests.
4. Confirm that no real client data is present.
5. Record user-visible changes in `CHANGELOG.md`.

Generated prose need not match snapshots word for word. Tests should protect observable behavior: guidance, approvals, factual handling, brand fidelity, variation, and output structure.
