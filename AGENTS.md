# AGENTS.md

Note: @Clanker refers to the "ai agent" (you) who is working on this task.

## General agent guidance

This section outlines the universal rules and expectations for any LLM agent working
within this repository.

**Safety and Quality First:** The highest priority is to produce secure,
well-documented, and high-quality code. Do not introduce vulnerabilities, hardcoded
secrets, or unreadable code.

**Propose a Plan:** For any new task, first provide a brief plan of action. This plan
should clearly outline the intended changes and the rationale behind them.

**Maintain Context:** Before making any changes, an agent must read and understand the
relevant files, including the project's main documentation and existing code structure.

**Be Sparse:** Only introduce new code if needed. Comment only what is worth commenting.
When testing focus on the business use case. When writing documentations keep the
explanation to a minimum.

**Never Commit:** Do not run `git commit`, `git push`, or any other version control
write operation. Only the author is allowed to commit changes. You may stage files, run
diffs, and prepare commit messages, but the actual commit and push must be done by the
author.

## Project structure

@Clanker document the structure of this project in this section.

## Environment & tooling

## Coding conventions

@Clanker document project specific coding conventions in this section.
