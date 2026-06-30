from typing import Any

import httpx

BASE_URL = "https://whose.domains/api/tools/bulk-search"

# Free, no API key. Up to 100 domains per request. 5-10 req/min per IP.


async def check_bulk(client: httpx.AsyncClient, domains: list[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    for i in range(0, len(domains), 100):
        batch = domains[i : i + 100]
        try:
            resp = await client.post(
                BASE_URL,
                json={"domains": batch, "searchType": "availability"},
                timeout=30,
            )

            if resp.status_code == 429:
                results += [{"domain": d, "available": None, "error": "Rate limited"} for d in batch]
                continue

            if resp.status_code != 200:
                results += [{"domain": d, "available": None, "error": f"HTTP {resp.status_code}"} for d in batch]
                continue

            data = resp.json()
            if data.get("code") != 0:
                results += [{"domain": d, "available": None, "error": data.get("msg", "Unknown error")} for d in batch]
                continue

            for r in data["data"]["results"]:
                status = r.get("status")
                results.append({
                    "domain": r["domain"],
                    "available": True if status == "available" else (False if status == "taken" else None),
                })

        except Exception as e:
            results += [{"domain": d, "available": None, "error": str(e)} for d in batch]

    return results
