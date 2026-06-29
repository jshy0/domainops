import os
from typing import Any, Dict

import httpx

BASE_URL = "https://api.godaddy.com/v1/domains/available"

# Access requirements:
# - $20/month average spend with GoDaddy, OR 50+ domains on account


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
            "available": data.get("available"),
            "price": data.get("price"),
            "renewal_price": data.get("renewalPrice"),
            "currency": data.get("currency", "USD"),
            "definitive": data.get("definitive"),
            "period": data.get("period"),
        }

    except Exception as e:
        return {"domain": domain, "available": None, "error": str(e)}
