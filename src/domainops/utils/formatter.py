from typing import Any, Dict, List

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def print_header(idea: str, provider: str) -> None:
    console.print(Panel(
        f"[bold cyan]DomainOps[/bold cyan]  [dim]{idea}[/dim]  [dim]via {provider}[/dim]",
        expand=False
    ))


def print_results(results: List[Dict[str, Any]]) -> None:
    table = Table(box=box.ROUNDED, header_style="bold magenta")
    table.add_column("Domain", style="cyan", min_width=28)
    table.add_column("Status", min_width=12)

    for r in results:
        if r.get("available") is True:
            status = "[bold green]✅ Available[/bold green]"
        elif r.get("available") is False:
            status = "[red]❌ Taken[/red]"
        else:
            status = "[yellow]⚠️  Error[/yellow]"

        table.add_row(r["domain"], status)

    console.print(table)
