from typing import Any

import typer
from dotenv import load_dotenv

from domainops.core.expander import DEFAULT_TLDS, expand_domains
from domainops.core.generator import generate_names_llm
from domainops.providers import godaddy, rdap, whosedomains
from domainops.services.checker import check_domains
from domainops.utils.formatter import console, print_header, print_results

app = typer.Typer(invoke_without_command=False)

load_dotenv()


@app.callback()
def main() -> None:
    """DomainOps — generate and check startup domain names."""


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
    tlds: str = typer.Option("", "--tlds", "-t", help="Comma-separated TLDs to check, e.g. com,io,ai (default: com,io,app,ai,co)"),
) -> None:
    idea_str = " ".join(idea)
    print_header(idea_str, provider)

    tld_list = [f".{t.strip().lstrip('.')}" for t in tlds.split(",") if t.strip()] or None

    with console.status("[bold green]Generating names...[/bold green]", spinner="dots"):
        names = generate_names_llm(idea_str, provider=provider, number=number)
        domains = expand_domains(names, tlds=tld_list)

    active_tlds = ", ".join(tld_list or DEFAULT_TLDS)
    console.print(f"[green]✓[/green] Generated [bold]{len(names)}[/bold] names · [bold]{len(domains)}[/bold] domains [dim]({active_tlds})[/dim]\n")

    with console.status("[bold green]Checking domains...[/bold green]", spinner="dots"):
        domain_checker = _CHECKER_MAP.get(checker, rdap)
        results = check_domains(domains, provider=domain_checker)

    if not show_all:
        results = [r for r in results if r.get("available") is True]

    print_results(results, checker=checker)


if __name__ == "__main__":
    app()
