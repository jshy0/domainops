from typing import Any, Optional

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

_CURRENCY_SYMBOLS: dict[str, str] = {
    "USD": "$",
    "GBP": "£",
    "EUR": "€",
    "AUD": "A$",
    "CAD": "C$",
    "INR": "₹",
    "JPY": "¥",
}


def _format_price(micros: Optional[int], currency: str) -> str:
    if not micros:
        return "[dim]—[/dim]"
    symbol = _CURRENCY_SYMBOLS.get(currency, currency)
    return f"{symbol}{micros / 1_000_000:.2f}"


def print_header(idea: str, provider: str) -> None:
    console.print(Panel(
        f"[bold cyan]DomainOps[/bold cyan]  [dim]{idea} · via {provider}[/dim]",
        expand=False
    ))


def print_results(results: list[dict[str, Any]], checker: str = "rdap") -> None:
    show_pricing = checker == "godaddy"

    table = Table(box=box.ROUNDED, header_style="bold magenta")
    table.add_column("Domain", style="cyan", min_width=28)
    table.add_column("Status", min_width=12)

    if show_pricing:
        table.add_column("Purchase", justify="right", min_width=10)
        table.add_column("Renewal", justify="right", min_width=10)

    for r in results:
        currency = r.get("currency", "USD")

        if r.get("available") is True:
            row: list[str] = [r["domain"], "[bold green]✅ Available[/bold green]"]
            if show_pricing:
                row += [_format_price(r.get("price"), currency), _format_price(r.get("renewal_price"), currency)]
            table.add_row(*row)
        elif r.get("available") is False:
            row = [r["domain"], "[red]❌ Taken[/red]"]
            if show_pricing:
                row += ["[dim]—[/dim]", "[dim]—[/dim]"]
            table.add_row(*row)
        else:
            error = r.get("error", "unknown")
            row = [r["domain"], f"[yellow]⚠️  {error}[/yellow]"]
            if show_pricing:
                row += ["[dim]—[/dim]", "[dim]—[/dim]"]
            table.add_row(*row)

    console.print(table)
