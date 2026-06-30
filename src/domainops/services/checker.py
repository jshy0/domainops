import asyncio
from typing import Any

import httpx

from domainops.providers import rdap


async def check_all(
    domains: list[str],
    provider: Any = rdap,
    client: httpx.AsyncClient | None = None,
) -> list[dict[str, Any]]:
    async def _run(c: httpx.AsyncClient) -> list[dict[str, Any]]:
        if hasattr(provider, "check_bulk"):
            return await provider.check_bulk(c, domains)

        sem = asyncio.Semaphore(10)

        async def throttled(domain: str) -> dict[str, Any]:
            async with sem:
                return await provider.check_single(c, domain)

        return list(await asyncio.gather(*[throttled(d) for d in domains]))

    if client is not None:
        return await _run(client)
    async with httpx.AsyncClient(follow_redirects=True) as c:
        return await _run(c)


def check_domains(domains: list[str], provider: Any = rdap) -> list[dict[str, Any]]:
    return asyncio.run(check_all(domains, provider))
