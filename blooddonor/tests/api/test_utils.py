import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    res = await client.get("/utils/health-check/")
    assert res.status_code == 200
    assert res.json() is True
