import random

import pytest

from blooddonor.core.config import settings
from blooddonor.crud.crud_utility import user
from blooddonor.helper.email import generate_password_reset_token
from blooddonor.schemas.user import AcademicYearEnum
from blooddonor.tests.utility.data import (
    data_for_random_user,
    data_for_superuser_by_superuser,
    data_for_user_by_superuser,
    data_user_create_superuser,
)


@pytest.mark.asyncio
async def test_read_users(client):
    r = await client.get("/users/read_users")
    res = r.json()
    assert r.status_code == 200
    for data in res:
        assert "email" in data


@pytest.mark.asyncio
async def test_existence_superuser(client, superuser_token_headers):
    r = await client.get("/users/me", headers=superuser_token_headers)
    res = r.json()
    assert res["email"] == settings.FIRST_SUPERUSER_EMAIL


@pytest.mark.asyncio
async def test_create_user_by_superuser(client, superuser_token_headers):
    user_data = data_for_user_by_superuser
    r = await client.post(
        "/users/create_user_by_superuser",
        json=user_data,
        headers=superuser_token_headers,
    )
    res = r.json()
    assert res["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_create_superuser_by_superuser(client, superuser_token_headers):
    user_data = data_for_superuser_by_superuser
    r = await client.post(
        "/users/create_user_by_superuser",
        json=user_data,
        headers=superuser_token_headers,
    )
    res = r.json()
    assert res["is_superuser"] == user_data["is_superuser"]


@pytest.mark.asyncio
async def test_user_create_superuser(client):
    user_data = data_user_create_superuser
    user_data["is_superuser"] = True
    await client.post(
        "/users/create_user",
        json=user_data,
    )
    email = user_data["email"]
    r = await client.get(f"/users/read_user/{email}")
    res = r.json()
    assert res["is_superuser"] is False


@pytest.mark.asyncio
async def test_create_user(client):
    user_data = data_for_random_user
    await client.post(
        "/users/create_user",
        json=user_data,
    )
    email = user_data["email"]
    r = await client.get(f"/users/read_user/{email}")
    res = r.json()
    assert res["email"] == email
    assert res["is_superuser"] is False


@pytest.mark.asyncio
async def test_verify_user(client):
    user_data = data_for_random_user
    token = await generate_password_reset_token(email=user_data["email"])
    token = {"token": token}
    r = await client.post("/users/verify-account", json=token)
    res = r.json()
    assert res["msg"] == "Account verification successful."


@pytest.mark.asyncio
async def test_delete_user_by_superuser(client, db, superuser_token_headers):
    email = data_for_superuser_by_superuser["email"]
    r = await client.delete(
        f"/users/delete_user/{email}", headers=superuser_token_headers
    )
    res = r.json()
    user_ = await user.get_by_email(db, email=email)
    assert res["msg"] == "The user has been removed!"
    assert not user_


@pytest.mark.asyncio
async def test_delete_user_by_user(client, user_token_headers):
    user_data = data_for_random_user
    email = user_data["email"]
    r = await client.get("/users/me", headers=user_token_headers)
    res = r.json()
    assert res["email"] == email
    assert res["is_superuser"] is False

    r = await client.delete(f"/users/delete_user/{email}", headers=user_token_headers)
    res = r.json()
    assert r.status_code == 400
    assert res["detail"] == "The user doesn't have enough privileges"


@pytest.mark.asyncio
async def test_user_update_me(client, user_token_headers):
    update_data = {
        "full_name": "User in Use (updated)",
        "blood_group": "ab+",
        "is_superuser": True,
        "password": data_for_random_user["password"],
    }
    r = await client.patch(
        "/users/update/me", json=update_data, headers=user_token_headers
    )
    res = r.json()
    assert res["full_name"] == update_data["full_name"]
    assert res["blood_group"] == "ab+"
    assert res["is_superuser"] is False


@pytest.mark.asyncio
async def test_read_profile_by_id(client, user_token_headers):
    user_data = await client.get("/users/me", headers=user_token_headers)
    user_id = user_data.json()["id"]
    r = await client.get(f"/users/read_profile/{user_id}")
    res = r.json()
    assert res["donor_id"] == user_id


@pytest.mark.asyncio
async def test_update_profile_me(client, user_token_headers):
    profile_data = {
        "facebook": "https://facebook.com/username",
        "employment_status": "employed",
        "extra_field": "extra",
    }
    r = await client.patch(
        "/users/update_profile/me", json=profile_data, headers=user_token_headers
    )
    res = r.json()
    assert res["facebook"] == profile_data["facebook"]
    assert res["employment_status"] == profile_data["employment_status"]
    assert "extra_field" not in res


@pytest.mark.asyncio
async def test_read_user_by_email(client):
    user_data = data_for_random_user
    r = await client.get(f"/users/read_user/{user_data["email"]}")
    res = r.json()
    assert res["email"] == user_data["email"]
    assert res["mobile"] == user_data["mobile"]


@pytest.mark.asyncio
async def test_user_update_using_email_by_superuser(client, superuser_token_headers):
    user_data = data_for_random_user
    update_data = {
        "full_name": "User Update by Superuser using email",
        "is_available": False,
    }
    r = await client.patch(
        f"/users/update/{user_data["email"]}",
        json=update_data,
        headers=superuser_token_headers,
    )
    res = r.json()
    assert res["full_name"] == update_data["full_name"]
    assert res["is_available"] is False
    assert res["mobile"] == user_data["mobile"]


@pytest.mark.asyncio
async def test_update_user_using_email_by_user(client, user_token_headers):
    user_data = data_for_random_user
    update_data = {
        "full_name": "User Update by Superuser using email",
        "is_available": False,
    }
    r = await client.patch(
        f"/users/update/{user_data["email"]}",
        json=update_data,
        headers=user_token_headers,
    )
    res = r.json()
    assert res["detail"] == "The user doesn't have enough privileges"


@pytest.mark.asyncio
async def test_upload_profile_img(client, fake_image_file, user_token_headers):
    file = {"file": ("fake_img.jpeg", fake_image_file)}
    r = await client.post(
        "/users/upload_profile_img", files=file, headers=user_token_headers
    )
    res = r.json()
    assert res["msg"] == "Profile image upload successful."
    user_ = await client.get("/users/me", headers=user_token_headers)
    user_ = user_.json()
    import os

    IMAGES_DIR = "./blooddonor/static/images"
    image_path = os.path.join(IMAGES_DIR, str(user_["profile"]["profile_img"]))
    if os.path.exists(image_path):
        os.remove(image_path)


@pytest.mark.asyncio
async def test_get_profile_img_by_id(client, user_token_headers):
    r = await client.get("/users/me", headers=user_token_headers)
    res = r.json()
    user_id = res["id"]
    r = await client.get(f"/users/get_profile_img/{user_id}")
    assert r.headers["content-type"] == "image/png"


@pytest.mark.asyncio
async def test_get_users_counts(client, db):
    r = await client.get("/users/counts")
    res = r.json()
    assert r.status_code == 200
    db_counts = await user.get_user_count(db)

    db_counts_copy = db_counts.copy()
    res_copy = res.copy()
    del db_counts_copy["blood_group_percentages"]
    del res_copy["blood_group_percentages"]

    paired_values = list(zip(db_counts_copy.values(), res_copy.values(), strict=False))
    bool_vals = [x[0] == x[1] for x in paired_values]
    assert all(bool_vals)


@pytest.mark.asyncio
async def test_get_me(client, user_token_headers):
    user_data = data_for_random_user
    r = await client.get("/users/me", headers=user_token_headers)
    res = r.json()
    assert res["email"] == user_data["email"]
    assert res["mobile"] == user_data["mobile"]


@pytest.mark.asyncio
async def test_delete_user_current_superuser_error(client, superuser_token_headers):
    r = await client.delete(
        f"/users/delete_user/{settings.FIRST_SUPERUSER_EMAIL}",
        headers=superuser_token_headers,
    )
    res = r.json()
    assert res["detail"] == "Super users are not allowed to delete themselves"


@pytest.mark.asyncio
async def test_user_not_found(client):
    r = await client.get("/users/read_user/randomemailaddr@gmail.com")
    res = r.json()
    assert r.status_code == 404
    assert res["detail"] == "User not found!"


@pytest.mark.asyncio
async def test_user_exists(client):
    user_data = data_for_user_by_superuser
    r = await client.post("/users/create_user", json=user_data)
    res = r.json()
    assert r.status_code == 400
    assert (
        res["detail"]
        == "The user with this mobile, email or student_id already exists in the system"
    )


@pytest.mark.asyncio
async def test_validation_error(client, superuser_token_headers):
    email = settings.FIRST_SUPERUSER_EMAIL
    test_data = {
        "full_name": "",
        "email": "user@example",
        "mobile": "017111111111",
        "department": "1011",
        "student_id": "2020202002",
        "gender": "malee",
        "profile": {"employment_status": "invalid"},
        "district": "district",
        "blood_group": "A_POSITIVE",
        "academic_year": "2010-2012",
        "password": "PASS",
    }
    for key, val in test_data.items():
        updated_data = {key: val}
        r = await client.patch(
            f"/users/update/{email}", json=updated_data, headers=superuser_token_headers
        )
        res = r.json()
        if key == "profile":
            field_name = res["detail"][0]["field"]
            assert field_name == "employment_status"
        else:
            field_name = res["detail"][0]["field"]
            assert field_name == key

    # test for invalid academic year
    academic_year = settings.FIRST_SUPERUSER_ACADEMIC_YEAR
    academic_year = random.choice(
        [year.value for year in AcademicYearEnum if year.value != academic_year]  # noqa
    )
    r = await client.patch(
        f"/users/update/{email}",
        json={"academic_year": academic_year},
        headers=superuser_token_headers,
    )
    res = r.json()
    field_name = res["detail"][0]["field"]
    assert field_name == "academic_year"
