# DomainOps

DomainOps is a multi-stage domain intelligence tool that turns startup ideas into ranked, brandable domain names using AI-assisted naming, real-time availability checks, and scoring heuristics.

## What it does

DomainOps helps founders, developers, and indie hackers move from idea to shortlist with less manual work.

Idea → Name generation → Domain expansion → Availability checks → Ranking

## How it works

The pipeline runs in stages:

1. Generate candidate names from an idea
2. Expand them into domain variants such as .com, .app, and .ai
3. Check availability through domain providers
4. Score and rank the results

## Example

```bash
domainops "ai fitness coaching app"
```

Example output:

- Fitora.app — Available
- MindPulse.ai — Available
- Trainly.com — Taken
- BodyForge.co — Available

## Features

- AI- and rule-based name generation
- Real-time domain availability checking
- Async API execution
- Scoring and ranking for better shortlist quality
- Clean CLI workflow
- Modular architecture with separate pipeline stages

## Architecture

- core: generation, scoring, orchestration
- services: async domain checking
- providers: external APIs such as GoDaddy and RDAP
- cli: command-line interface
- utils: formatting and helpers

## Why it exists

Many existing tools either generate names without validating them or check availability without ranking the best options. DomainOps combines both so you can make better decisions faster.

## Installation

```bash
uv venv
uv add -r requirements.txt
```

Run it with:

```bash
uv run domainops run "your idea here"
```

## Roadmap

### v1 (MVP)

- CLI tool
- Async domain checker
- Basic scoring system
- LLM and rule-based name generation

### v2

- Provider plugin system
- Improved scoring heuristics
- Bulk domain evaluation

### v3

- FastAPI layer
- Web dashboard
- Shareable results

## Contributing

Contributions are welcome for:

- New domain providers
- Scoring improvements
- Name generation strategies
- Performance optimizations

## License

MIT
