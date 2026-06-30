from typing import Any
from unittest.mock import AsyncMock, MagicMock

from domainops.providers.whosedomains import check_bulk


def _mock_client(status_code: int, body: dict[str, Any] | None = None) -> Any:
    client = AsyncMock()
    response = MagicMock(status_code=status_code)
    if body is not None:
        response.json = lambda: body
    client.post.return_value = response
    return client


class TestCheckBulk:
    async def test_available(self):
        client = _mock_client(200, {
            "code": 0,
            "data": {"results": [{"domain": "fitora.com", "status": "available"}]},
        })
        results = await check_bulk(client, ["fitora.com"])
        assert results == [{"domain": "fitora.com", "available": True}]

    async def test_taken(self):
        client = _mock_client(200, {
            "code": 0,
            "data": {"results": [{"domain": "google.com", "status": "taken"}]},
        })
        results = await check_bulk(client, ["google.com"])
        assert results == [{"domain": "google.com", "available": False}]

    async def test_unknown_status(self):
        client = _mock_client(200, {
            "code": 0,
            "data": {"results": [{"domain": "x.com", "status": "unknown"}]},
        })
        results = await check_bulk(client, ["x.com"])
        assert results[0]["available"] is None

    async def test_rate_limited(self):
        client = _mock_client(429)
        results = await check_bulk(client, ["fitora.com"])
        assert results[0]["available"] is None
        assert results[0]["error"] == "Rate limited"

    async def test_http_error(self):
        client = _mock_client(500)
        results = await check_bulk(client, ["fitora.com"])
        assert results[0]["available"] is None
        assert "HTTP 500" in results[0]["error"]

    async def test_api_error_code(self):
        client = _mock_client(200, {"code": 1, "msg": "bad request"})
        results = await check_bulk(client, ["fitora.com"])
        assert results[0]["available"] is None
        assert results[0]["error"] == "bad request"
