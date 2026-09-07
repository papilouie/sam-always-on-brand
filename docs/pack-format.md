# Portable pack format

Brand Packs and Campaign Packs combine YAML manifests and structured records with Markdown guidance and original assets. Every manifest declares `schema_version: "1.0"`, a `pack_type`, stable IDs, file references, readiness or approval state, and unresolved verification items.

Use `packages/sam-aobpg/scripts/validate_pack.py` to validate packs against the schemas and confirm that referenced files stay inside the pack and exist.

Temporary campaign preferences never silently overwrite a Brand Pack. Real packs belong under the ignored `workspace/` directory.
