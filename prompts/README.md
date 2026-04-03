# System Prompts

## Purpose

This folder contains system prompts used in the retrieval prototype (Phase 1). These prompts tell a frontier model (Claude/GPT-4) how to behave as a Kirundi tutor while being constrained to your approved content.

## Key principle

The model should NEVER generate free Kirundi. It should:
- Retrieve and present your approved content
- Explain your content in English/French
- Scaffold dialogues from your approved scripts
- Correct learners by matching against your approved corrections and variants

## Files to create here

- `tutor_system_prompt.md` — main system prompt for the teaching assistant
- `translation_prompt.md` — prompt template for translation tasks
- `correction_prompt.md` — prompt template for correction tasks
- `dialogue_prompt.md` — prompt template for dialogue practice

These will be developed when you build the retrieval prototype (Milestone 3).
