import pytest

from blooddonor.core.config import settings


@pytest.mark.asyncio
async def test_search_filter(client):
    queries = {
        "full_name": settings.FIRST_SUPERUSER,
        "mobile": settings.FIRST_SUPERUSER_MOBILE,
        "department": settings.FIRST_SUPERUSER_DEPARTMENT,
        "student_id": settings.FIRST_SUPERUSER_STUDENT_ID,
        "gender": settings.FIRST_SUPERUSER_GENDER,
        "district": settings.FIRST_SUPERUSER_DISTRICT,
        "blood_group": settings.FIRST_SUPERUSER_BLOOD_GROUP,
        "academic_year": settings.FIRST_SUPERUSER_ACADEMIC_YEAR,
    }
    for key, val in queries.items():
        r = await client.get("/search/filter_donors", params={key: val})
        res = r.json()
        assert key in str(res)
