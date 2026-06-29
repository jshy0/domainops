# 🧠 DomainOps

DomainOps is a multi-stage domain intelligence tool that turns startup ideas into ranked, brandable domain names using AI-assisted naming and real-time availability checks.

## 🤔 What does it do?

DomainOps helps founders, developers and indie hackers move from idea to shortlist without all the faff.

```
Idea → Name generation → Domain expansion → Availability checks → Ranked results
```

## ⚙️ How it works

The pipeline runs in stages:

1. Generate candidate names from your idea using an LLM
2. Expand them into domain variants across `.com`, `.io`, `.app`, `.ai` and `.co`
3. Check availability in parallel via RDAP or GoDaddy
4. Filter and display the best available options

## 💻 Example

```bash
uv run domainops run ai fitness coaching app
```

```
╭─────────────────────────────────────────────────────╮
│ DomainOps  ai fitness coaching app  via ollama      │
╰─────────────────────────────────────────────────────╯
✓ Generated 10 names across 50 domains

╭──────────────────────────────┬──────────────╮
│ Domain                       │ Status       │
├──────────────────────────────┼──────────────┤
│ fitora.app                   │ ✅ Available │
│ mindpulse.ai                 │ ✅ Available │
│ trainly.com                  │ ✅ Available │
╰──────────────────────────────┴──────────────╯
```

## ✨ Features

- 🧠 AI name generation — works with Ollama (free, local) or OpenAI
- 🌐 Real-time availability checks across `.com`, `.io`, `.app`, `.ai` and `.co`
- ⚡ Async parallel checks for speed
- 🔌 Swappable domain checker — RDAP (free, no account) or GoDaddy (with pricing)
- 💻 Clean CLI with Rich terminal output
- 🏗️ Modular provider architecture

## 🧱 Architecture

```
core/      → generation, orchestration
services/  → async domain checking engine
providers/ → RDAP and GoDaddy implementations
cli/       → command-line interface
utils/     → formatting and helpers
```

## 🤷 Why does it exist?

Most tools either generate names without validating them or check availability without any intelligence behind it. DomainOps combines both so you can go from idea to shortlist in seconds — without bouncing between five different tabs.

## 🚀 Getting started

```bash
uv venv
uv sync
```

By default DomainOps uses **Ollama** for name generation and **RDAP** for domain checking — both free, no API keys required.

Make sure Ollama is running with a model pulled:

```bash
ollama pull llama3.2
ollama serve
```

Then run:

```bash
uv run domainops run your idea here
```

## 🎛️ Options

| Flag | Default | Description |
|------|---------|-------------|
| `--provider` / `-p` | `ollama` | LLM for name generation: `ollama` or `openai` |
| `--checker` / `-c` | `rdap` | Domain checker: `rdap` or `godaddy` |
| `--show-all` / `-a` | off | Show taken and errored domains too |

**Use OpenAI for generation:**
```bash
uv run domainops run your idea here --provider openai
```

**Use GoDaddy checker (includes pricing):**
```bash
uv run domainops run your idea here --checker godaddy
```

> **Note:** GoDaddy API access requires either $20/month average spend or 50+ domains on your account. See [GoDaddy API docs](https://developer.godaddy.com/getstarted).

## 🗺️ Roadmap

### v1 — MVP ✅
- CLI tool
- Async domain checker with RDAP and GoDaddy support
- LLM name generation (Ollama + OpenAI)
- TLD expansion across 5 extensions

### v2
- Scoring and ranking engine
- Bulk domain evaluation

### v3
- FastAPI layer
- Web dashboard
- Shareable results

## 🤝 Contributing

Contributions are welcome for:

- 🌐 New domain checker providers
- 🧠 Scoring improvements
- 🔤 Name generation strategies
- ⚡ Performance optimisations

## 📜 Licence

MIT
