from io import BytesIO

import pytest_asyncio
from httpx import AsyncClient
from PIL import Image

from blooddonor.api.deps import get_db
from blooddonor.core.config import settings
from blooddonor.db.base import Base
from blooddonor.db.init_db import init_db
from blooddonor.tests.utility.data import data_for_random_user
from blooddonor.tests.utility.db import TestingSessionLocal, test_engine
from blooddonor.tests.utility.utils import get_superuser_token_header
from main import app

TEST_URL = f"{str(settings.SERVER_HOST).rstrip('/')}{settings.API_V1_STR}"


@pytest_asyncio.fixture
async def db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        await init_db(session)
        await session.commit()
        yield session


@pytest_asyncio.fixture
async def client(db):  # noqa
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url=TEST_URL) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def superuser_token_headers(client):
    return await get_superuser_token_header(client)


@pytest_asyncio.fixture
async def user_token_headers(client):
    email = data_for_random_user["email"]
    password = data_for_random_user["password"]
    data = {"username": email, "password": password}
    r = await client.post("/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


@pytest_asyncio.fixture
async def fake_image_file():
    img = Image.new("RGB", (200, 200), color=(255, 0, 0))
    file_data = BytesIO()
    img.save(file_data, format="JPEG")
    file_data.seek(0)
    file_data.name = "fake_img.jpeg"
    return file_data
