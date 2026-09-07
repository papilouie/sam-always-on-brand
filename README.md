# SAM — Always-On Brand Post Generator

SAM is a guided content system that turns a topic, product, image, link, document, or rough idea into approved, on-brand posts. It uses portable Brand Packs, campaign briefs, approval-first Post Blueprints, and platform-aware generation.

Version 1 includes:

- Guided and quick brand onboarding
- Portable Brand Packs and Campaign Packs
- Campaign planning with contextual recommendations
- One to five distinct Post Blueprints
- A mandatory approval gate before final generation
- Platform adaptations for social posts, carousels, scripts, articles, and newsletters
- Visual briefs, image prompts, text overlays, and alt text
- A shared OpenAI/Claude Agent Skill package
- A no-backend Custom GPT configuration package
- Validation scripts, examples, and evaluation scenarios

SAM does not publish posts, store brands in a cloud database, or provide legal approval in Version 1.

## Quick start

1. Read [Getting Started](docs/getting-started.md).
2. Try the fictional [Sunny Spoon Brand Pack](examples/brands/sunny-spoon/manifest.yaml).
3. Install the package using the appropriate platform guide:
   - [Custom GPT](docs/custom-gpt.md)
   - [OpenAI Skill](docs/openai-skill.md)
   - [Claude Skill](docs/claude-skill.md)
4. Validate the examples with the bundled validator.
5. Build platform ZIPs with `scripts/build_releases.py`.

## Repository map

- `packages/sam-aobpg/` — canonical cross-platform Agent Skill
- `schemas/` — JSON Schemas for portable packs
- `adapters/custom-gpt/` — builder configuration and consolidated Knowledge
- `examples/` — fictional Brand Pack, Campaign Pack, and golden-path artifacts
- `evals/` — behavioral scenarios and review rubric
- `scripts/` — repository validation and release packaging
- `tests/` — automated tests

## Privacy

Real client Brand Packs and Campaign Packs belong in `workspace/`, which is ignored by Git. Never commit client assets, credentials, unpublished campaigns, testimonials without permission, analytics exports, or private URLs.

## Status

This repository contains SAM Version 1.0.0.
