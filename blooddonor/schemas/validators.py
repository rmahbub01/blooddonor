import re
from enum import Enum

from pydantic import field_validator

from blooddonor.schemas.user import AcademicYearEnum


class DepartmentsEnum(str, Enum):
    # Faculty of Arts and Humanities
    BANGLA = "101"
    ENGLISH = "102"
    HISTORY = "103"
    ISLAMIC_HISTORY_AND_CULTURE = "104"
    PHILOSOPHY = "105"
    FINE_ARTS = "106"
    ARABIC = "107"
    PALI = "108"
    ISLAMIC_STUDIES = "110"
    DRAMATICS = "111"
    PERSIAN_LANGUAGE_AND_LITERATURE = "112"
    EDUCATION_AND_RESEARCH = "113"
    MODERN_LANGUAGES = "114"
    SANSKRIT = "115"
    MUSIC = "116"
    BANGLADESH_STUDIES = "117"

    # Faculty of Science
    PHYSICS = "201"
    CHEMISTRY = "202"
    MATHEMATICS = "203"
    STATISTICS = "204"
    FORESTRY_AND_ENVIRONMENTAL_SCIENCES = "208"
    APPLIED_CHEMISTRY_AND_CHEMICAL_ENGINEERING = "209"

    # Faculty of Business Administration
    ACCOUNTING = "301"
    MANAGEMENT = "302"
    FINANCE = "303"
    MARKETING = "304"
    HUMAN_RESOURCE_MANAGEMENT = "305"
    BANKING_AND_INSURANCE = "306"

    # Faculty of Social Sciences
    ECONOMICS = "401"
    POLITICAL_SCIENCE = "402"
    SOCIOLOGY = "403"
    PUBLIC_ADMINISTRATION = "404"
    ANTHROPOLOGY = "405"
    INTERNATIONAL_RELATIONS = "406"
    COMMUNICATION_AND_JOURNALISM = "407"
    DEVELOPMENT_STUDIES = "408"
    CRIMINOLOGY_AND_POLICE_SCIENCE = "409"

    # Faculty of Law
    LAW = "501"

    # Faculty of Biological Sciences
    ZOOLOGY = "601"
    BOTANY = "602"
    GEOGRAPHY_AND_ENVIRONMENTAL_STUDIES = "603"
    BIOCHEMISTRY_AND_MOLECULAR_BIOLOGY = "604"
    MICROBIOLOGY = "605"
    SOIL_SCIENCE = "606"
    GENETIC_ENGINEERING_AND_BIOTECHNOLOGY = "607"
    PSYCHOLOGY = "608"
    PHARMACY = "609"

    # Faculty of Engineering
    COMPUTER_SCIENCE_AND_ENGINEERING = "701"
    ELECTRICAL_AND_ELECTRONIC_ENGINEERING = "702"

    # Faculty of Education
    PHYSICAL_EDUCATION_AND_SPORTS_SCIENCE = "801"

    # Faculty of Marine Sciences and Fisheries
    MARINE_SCIENCES = "901"
    OCEANOGRAPHY = "902"
    FISHERIES = "903"


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
        if v in DepartmentsEnum:
            return v
        raise ValueError("The provided dept code doesn't match with any department.")

    @field_validator("academic_year", check_fields=False)
    def validate_department(cls, v):
        if v in AcademicYearEnum:
            return v
        raise ValueError(
            "The selected academic session doesn't match with listed sessions."
        )

    @field_validator("student_id", check_fields=False)
    def validate_student_id(cls, v, info):
        v = str(v)
        department = info.data.get("department")
        student_id_regex = r"[1-9]{1}[\d]{1}[1-9]{1}[\d]{5}"
        if (
            (len(v) == 8)
            and re.match(student_id_regex, v)
            and (str(department.value) == v[2:5])
            and (1 <= int(v[-3:]) <= 150)
        ):
            return v
        raise ValueError(
            "The student id is not valid or doesn't associate with the respective department"
        )


class PasswordValidationMixin:
    @field_validator("password", check_fields=False)
    def password_validator(cls, v):
        if len(v) < 5:
            raise ValueError("Password must be equal or greater than 5 characters")
        return v
