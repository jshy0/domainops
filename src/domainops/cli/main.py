from dotenv import load_dotenv
load_dotenv()

import typer
from domainops.core.orchestrator import run_pipeline
app = typer.Typer()


@app.command()
def run(
    idea: list[str] = typer.Argument(...),
    provider: str = typer.Option("ollama", "--provider", "-p", help="LLM provider: ollama (default, free) or openai"),
) -> None:
    results = run_pipeline(" ".join(idea), provider=provider)

    print()
    for r in results:
        if r.get("available") is True:
            status = "✅ Available"
        elif r.get("available") is False:
            status = "❌ Taken"
        else:
            error = r.get("error", "unknown error")
            status = f"⚠️  Error: {error}"
        print(f"{r['domain']:<28} {status}")


if __name__ == "__main__":
    app()
