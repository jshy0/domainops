import asyncio
from typing import Any

import httpx

from domainops.providers import rdap


async def _check_all(domains: list[str], provider: Any = rdap) -> list[dict[str, Any]]:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        if hasattr(provider, "check_bulk"):
            return await provider.check_bulk(client, domains)

        sem = asyncio.Semaphore(10)

        async def throttled(client: httpx.AsyncClient, domain: str) -> dict[str, Any]:
            async with sem:
                return await provider.check_single(client, domain)

        tasks = [throttled(client, d) for d in domains]
        return await asyncio.gather(*tasks)


def check_domains(domains: list[str], provider: Any = rdap) -> list[dict[str, Any]]:
    return asyncio.run(_check_all(domains, provider))
