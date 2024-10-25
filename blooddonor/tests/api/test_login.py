import pytest

from blooddonor.core.config import settings


@pytest.mark.asyncio
async def test_user_login_by_mobile(client):
    data = {
        "username": settings.FIRST_SUPERUSER_MOBILE,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = await client.post("login/access-token", data=data)
    res = r.json()
    assert res["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_user_login_by_email(client):
    data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = await client.post("login/access-token", data=data)
    res = r.json()
    assert res["token_type"] == "bearer"
    return res["access_token"]


@pytest.mark.asyncio
async def test_user_change_password(client):
    token = await test_user_login_by_email(client)
    update_data = {"password": "admin"}
    headers = {"Authorization": f"Bearer {token}"}
    r = await client.post(
        "/change_password", json=update_data, headers=headers, follow_redirects=True
    )
    res = r.json()
    assert res["msg"] == "Password updated successfully"


# TODO LIST
# test for password-recovery
# test for reset-password
