# 🧠 DomainOps

DomainOps is a multi-stage domain intelligence tool that turns startup ideas into ranked, brandable domain names using AI-assisted naming, real-time availability checks and scoring heuristics.

## 🤔 What does it do?

DomainOps helps founders, developers and indie hackers move from idea to shortlist without all the faff.

```
Idea → Name generation → Domain expansion → Availability checks → Ranking
```

## ⚙️ How it works

The pipeline runs in stages:

1. Generate candidate names from your idea
2. Expand them into domain variants like `.com`, `.app` and `.ai`
3. Check availability through domain providers
4. Score and rank the results

## 💻 Example

```bash
uv run domainops run ai fitness coaching app
```

```
🚀 Generating names via ollama...
💡 Generated 10 names — expanding across 5 TLDs...
🌐 Checking 50 domains...

fitora.app        ✅ Available
mindpulse.ai      ✅ Available
trainly.com       ❌ Taken
bodyforge.co      ✅ Available
```

## ✨ Features

- 🧠 AI-assisted name generation — works with Ollama (free) or OpenAI
- 🌐 Real-time domain availability checking across `.com`, `.io`, `.app`, `.ai` and `.co`
- ⚡ Async API execution for fast parallel checks
- 📊 Scoring and ranking for a better shortlist
- 💻 Clean CLI — no UI faff
- 🔌 Modular pipeline architecture

## 🧱 Architecture

```
core/      → generation, scoring, orchestration
services/  → async domain checking engine
providers/ → external APIs (GoDaddy, RDAP)
cli/       → command-line interface
utils/     → formatting and helpers
```

## 🤷 Why does it exist?

Most tools either generate names without validating them or check availability without ranking the results. DomainOps does both so you can make better decisions faster — without bouncing between five different tabs.

## 🚀 Getting started

```bash
uv venv
uv sync
```

By default DomainOps uses **Ollama** — free, runs locally, no API key needed. Make sure you've got Ollama running with a model pulled:

```bash
ollama pull llama3.2
ollama serve
```

Then run:

```bash
uv run domainops run your idea here
```

To use OpenAI instead, copy `.env.example` to `.env`, add your key and pass the flag:

```bash
uv run domainops run your idea here --provider openai
```

## 🗺️ Roadmap

### v1 — MVP
- CLI tool
- Async domain checker
- LLM name generation (Ollama + OpenAI)
- TLD expansion

### v2
- Scoring and ranking engine
- Provider plugin system
- Bulk domain evaluation

### v3
- FastAPI layer
- Web dashboard
- Shareable results

## 🤝 Contributing

Contributions are welcome for:

- 🌐 New domain providers
- 🧠 Scoring improvements
- 🔤 Name generation strategies
- ⚡ Performance optimisations

## 📜 Licence

MIT
