import re

from pydantic import field_validator


class CommonFieldValidationMixin:
    @field_validator("full_name", check_fields=False)
    def validate_full_name(cls, v):
        if v is None or v.strip() == "":
            raise ValueError("Name is not valid!")
        return v

    @field_validator("mobile", check_fields=False)
    def validate_mobile(cls, v):
        mobile_regex = r"(?:\+88)?(01[\d]+)"
        mobile = re.match(mobile_regex, v)
        if mobile:
            mobile = mobile.group(1)
            if isinstance(int(mobile), int) and len(mobile) == 11:
                return mobile
        raise ValueError("The number format is invalid. Use numbers like 017xxxxxxxx")

    @field_validator("department", mode="before", check_fields=False)
    def validate_department(cls, v):
        from blooddonor.schemas.user import DepartmentsEnum

        if v in DepartmentsEnum:
            return v
        raise ValueError("The provided dept code doesn't match with any department.")

    @field_validator("student_id", check_fields=False)
    def validate_student_id(cls, v, info):
        v = str(v)
        department = info.data.get("department")
        student_id_regex = r"[1-9]{1}[\d]{1}[1-9]{1}[\d]{5}"
        if v and (
            (len(v) == 8)
            and re.match(student_id_regex, v)
            and (str(department.value) == v[2:5])
            and (1 <= int(v[-3:]) <= 150)
        ):
            return v
        raise ValueError(
            "The student id is not valid or doesn't associate with the respective department"
        )

    @field_validator("academic_year", check_fields=False)
    def validate_academic_year(cls, v, info):
        from blooddonor.schemas.user import AcademicYearEnum

        student_id = info.data.get("student_id")
        if v in AcademicYearEnum and student_id and student_id[:2] == v[-2:]:
            return v
        raise ValueError("Your session is not valid.")


class PasswordValidationMixin:
    @field_validator("password", check_fields=False)
    def password_validator(cls, v):
        if len(v) < 5:
            raise ValueError("Password must be equal or greater than 5 characters")
        return v
