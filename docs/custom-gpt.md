# Install as a Custom GPT

1. In an eligible ChatGPT workspace, create or edit a GPT.
2. Use the name and description in `adapters/custom-gpt/description.md`.
3. Paste `adapters/custom-gpt/instructions.md` into Instructions.
4. Upload `adapters/custom-gpt/knowledge/sam-knowledge.md` as Knowledge.
5. Add the supplied conversation starters.
6. Enable only the capabilities described in `capability-settings.md`.
7. Test the golden path and critical evaluation scenarios before sharing.

Custom GPT conversations do not provide SAM's Version 1 brand persistence. Users should retain and re-upload portable Brand Packs, or a builder may preload a fixed brand into Knowledge for a single-brand GPT.
