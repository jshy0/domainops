import asyncio
import os
from typing import Any, Dict, List

import httpx

BASE_URL = "https://api.ote-godaddy.com/v1/domains/available"


async def check_single(client: httpx.AsyncClient, domain: str) -> Dict[str, Any]:
    api_key = os.getenv("GODADDY_API_KEY")
    api_secret = os.getenv("GODADDY_API_SECRET")
    headers = {"Authorization": f"sso-key {api_key}:{api_secret}"}

    try:
        resp = await client.get(f"{BASE_URL}?domain={domain}", headers=headers, timeout=10)

        if resp.status_code != 200:
            return {"domain": domain, "available": None, "error": resp.text}

        data = resp.json()

        return {
            "domain": domain,
            "available": data.get("available", None),
            "price": data.get("price", 0),
            "renewal_price": data.get("renewalPrice", 0),
            "currency": data.get("currency", "USD"),
            "definitive": data.get("definitive", None),
            "period": data.get("period", None),
        }

    except Exception as e:
        return {"domain": domain, "available": None, "error": str(e)}


async def _check_all(domains: List[str]) -> List[Dict[str, Any]]:
    sem = asyncio.Semaphore(5) # Limit concurrent requests to 5

    async def throttled(client: httpx.AsyncClient, domain: str) -> Dict[str, Any]:
        async with sem:
            return await check_single(client, domain)
        
    async with httpx.AsyncClient() as client:
        tasks = [throttled(client, d) for d in domains]
        return await asyncio.gather(*tasks)


def check_domains(domains: List[str]) -> List[Dict[str, Any]]:
    return asyncio.run(_check_all(domains))
