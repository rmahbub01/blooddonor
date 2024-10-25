from blooddonor.core.config import settings


async def get_superuser_token_header(client):
    login_data = {
        "username": settings.FIRST_SUPERUSER_MOBILE,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = await client.post("/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
