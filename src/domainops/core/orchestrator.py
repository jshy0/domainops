from typing import Any

from domainops.core.expander import expand_domains
from domainops.core.generator import generate_names_llm
from domainops.services.checker import check_domains


def run_pipeline(idea: str, provider: str = "ollama") -> list[dict[str, Any]]:
    print(f"\n🚀 Generating names via {provider}...")
    names = generate_names_llm(idea, provider=provider)
    print(f"💡 Generated {len(names)} names — expanding across {len(expand_domains(['x']))} TLDs...")

    domains = expand_domains(names)

    print(f"🌐 Checking {len(domains)} domains...")
    results = check_domains(domains)
    return results
