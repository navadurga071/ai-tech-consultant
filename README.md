# AI Tech Consultant

An AI-powered consulting system that helps software businesses answer customer questions, draft email replies, and turn client meetings into clear scopes of work and proposals.

## Project modules

- **Task 1 — Knowledge Brain:** Python service that indexes the Brilliant Directories Solution Center and answers questions with supporting sources.
- **Task 2 — Inbox Agent:** TypeScript service that drafts customer email replies using the Knowledge Brain API and incorporates human feedback.
- **Task 3 — Meeting to Scope of Work:** Python service that generates a scope of work, task estimates, and client-ready proposals using the Knowledge Brain API.

## Architecture

Tasks 2 and 3 consume Task 1 through its API. Each module has a separate responsibility, and human approval is required for outgoing email and proposals.

## Requirements

- Python (version to be specified)
- Node.js (version to be specified)
- Anthropic API access
- Dependencies listed in each task's configuration

## Run locally

Setup and run instructions will be added after the services and shared startup command are implemented.

## Evaluation

See `EVALS.md` for test cases and measured quality, cost, speed, and reliability.

## Documentation

- `DESIGN.md` — Architecture and design decisions
- `EVALS.md` — Evaluation results
- `AI_LOG.md` — AI-assisted development log
