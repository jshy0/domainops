import asyncio
from typing import Any, Dict

import httpx

_BOOTSTRAP_URL = "https://data.iana.org/rdap/dns.json"
_FALLBACK_URL = "https://rdap.org/domain"


class RDAPProvider:
    def __init__(self) -> None:
        self._tld_map: Dict[str, str] = {}
        self._loaded = False
        self._lock = asyncio.Lock()

    async def _load_bootstrap(self, client: httpx.AsyncClient) -> None:
        if self._loaded:
            return
        async with self._lock:
            if self._loaded:
                return
            try:
                resp = await client.get(_BOOTSTRAP_URL, timeout=10)
                resp.raise_for_status()
                for tlds, servers in resp.json()["services"]:
                    if servers:
                        base = servers[0].rstrip("/") + "/"
                        for tld in tlds:
                            self._tld_map[tld.lower()] = base
                self._loaded = True
            except Exception:
                pass

    def _rdap_url(self, domain: str) -> str:
        tld = domain.rsplit(".", 1)[-1].lower()
        base = self._tld_map.get(tld)
        return f"{base}domain/{domain}" if base else f"{_FALLBACK_URL}/{domain}"

    async def check_single(self, client: httpx.AsyncClient, domain: str) -> Dict[str, Any]:
        await self._load_bootstrap(client)
        url = self._rdap_url(domain)
        try:
            resp = await client.get(url, timeout=10)

            if resp.status_code == 200:
                return {"domain": domain, "available": False}
            elif resp.status_code == 404:
                return {"domain": domain, "available": True}
            elif resp.status_code == 429:
                await asyncio.sleep(5)
                resp = await client.get(url, timeout=10)
                if resp.status_code == 200:
                    return {"domain": domain, "available": False}
                elif resp.status_code == 404:
                    return {"domain": domain, "available": True}
                return {"domain": domain, "available": None, "error": "Rate limited"}
            else:
                return {"domain": domain, "available": None, "error": f"HTTP {resp.status_code}"}

        except Exception as e:
            return {"domain": domain, "available": None, "error": str(e)}


rdap = RDAPProvider()
