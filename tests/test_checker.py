from unittest.mock import AsyncMock, MagicMock

from domainops.services.checker import check_all


async def test_routes_to_bulk():
    client = AsyncMock()
    provider = MagicMock()
    provider.check_bulk = AsyncMock(return_value=[{"domain": "fitora.com", "available": True}])

    results = await check_all(["fitora.com"], provider=provider, client=client)

    assert results == [{"domain": "fitora.com", "available": True}]
    provider.check_bulk.assert_called_once_with(client, ["fitora.com"])


async def test_routes_to_single():
    client = AsyncMock()
    provider = MagicMock(spec=[])  # no check_bulk
    provider.check_single = AsyncMock(return_value={"domain": "fitora.com", "available": True})

    results = await check_all(["fitora.com"], provider=provider, client=client)

    assert results == [{"domain": "fitora.com", "available": True}]
    provider.check_single.assert_called_once_with(client, "fitora.com")