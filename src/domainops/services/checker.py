import asyncio
from typing import Any, Dict, List

import httpx

from domainops.providers import rdap


async def _check_all(domains: List[str], provider=rdap) -> List[Dict[str, Any]]:
    sem = asyncio.Semaphore(10)

    async def throttled(client: httpx.AsyncClient, domain: str) -> Dict[str, Any]:
        async with sem:
            return await provider.check_single(client, domain)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [throttled(client, d) for d in domains]
        return await asyncio.gather(*tasks)


def check_domains(domains: List[str], provider=rdap) -> List[Dict[str, Any]]:
    return asyncio.run(_check_all(domains, provider))
