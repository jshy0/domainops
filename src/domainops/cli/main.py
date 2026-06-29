from dotenv import load_dotenv
load_dotenv()

import typer
from domainops.core.orchestrator import run_pipeline
from domainops.utils.formatter import console, print_header, print_results

app = typer.Typer()


@app.command()
def run(
    idea: list[str] = typer.Argument(...),
    provider: str = typer.Option("ollama", "--provider", "-p", help="LLM provider: ollama (default, free) or openai"),
    checker: str = typer.Option("rdap", "--checker", "-c", help="Domain checker: rdap (default, free) or godaddy"),
    show_all: bool = typer.Option(False, "--show-all", "-a", help="Show taken and errored domains too"),
) -> None:
    idea_str = " ".join(idea)
    print_header(idea_str, provider)

    with console.status("[bold green]Generating names...[/bold green]", spinner="dots"):
        from domainops.core.generator import generate_names_llm
        from domainops.core.expander import expand_domains
        names = generate_names_llm(idea_str, provider=provider)
        domains = expand_domains(names)

    console.print(f"[green]✓[/green] Generated [bold]{len(names)}[/bold] names across [bold]{len(domains)}[/bold] domains\n")

    with console.status("[bold green]Checking domains...[/bold green]", spinner="dots"):
        from domainops.services.checker import check_domains
        from domainops.providers import rdap, godaddy
        provider_map = {"rdap": rdap, "godaddy": godaddy}
        results = check_domains(domains, provider=provider_map.get(checker, rdap))

    if not show_all:
        results = [r for r in results if r.get("available") is True]

    print_results(results, checker=checker)


if __name__ == "__main__":
    app()
