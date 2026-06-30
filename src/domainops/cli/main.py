from dotenv import load_dotenv
load_dotenv()

from typing import Any

import typer

from domainops.core.expander import expand_domains
from domainops.core.generator import generate_names_llm
from domainops.providers import godaddy, rdap, whosedomains
from domainops.services.checker import check_domains
from domainops.utils.formatter import console, print_header, print_results

app = typer.Typer(invoke_without_command=False)

_CHECKER_MAP: dict[str, Any] = {
    "rdap": rdap,
    "godaddy": godaddy,
    "whosedomains": whosedomains,
}


@app.command()
def run(
    idea: list[str] = typer.Argument(...),
    number: int = typer.Option(10, "--number", "-n", help="Number of names to generate"),
    provider: str = typer.Option("ollama", "--provider", "-p", help="LLM provider: ollama (default, free) or openai"),
    checker: str = typer.Option("rdap", "--checker", "-c", help="Domain checker: rdap (default), whosedomains, or godaddy"),
    show_all: bool = typer.Option(False, "--show-all", "-a", help="Show taken and errored domains too"),
) -> None:
    idea_str = " ".join(idea)
    print_header(idea_str, provider)

    with console.status("[bold green]Generating names...[/bold green]", spinner="dots"):
        names = generate_names_llm(idea_str, provider=provider, number=number)
        domains = expand_domains(names)

    console.print(f"[green]✓[/green] Generated [bold]{len(names)}[/bold] names across [bold]{len(domains)}[/bold] domains\n")

    with console.status("[bold green]Checking domains...[/bold green]", spinner="dots"):
        domain_checker = _CHECKER_MAP.get(checker, rdap)
        results = check_domains(domains, provider=domain_checker)

    if not show_all:
        results = [r for r in results if r.get("available") is True]

    print_results(results, checker=checker)


if __name__ == "__main__":
    app()
