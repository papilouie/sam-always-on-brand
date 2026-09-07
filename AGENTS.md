# SAM repository guidance

Use `packages/sam-aobpg/` as the canonical Agent Skill. Keep the OpenAI and Claude releases behaviorally equivalent. Custom GPT Knowledge is generated from the same canonical references.

Never add real client Brand Packs, Campaign Packs, credentials, private links, or unpublished assets to this repository. Use the ignored `workspace/` directory for local brand work.

When changing SAM behavior, preserve the Campaign Brief and Post Blueprint approval gates, update relevant evaluations, and run validation and tests.
