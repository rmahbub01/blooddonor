import datetime
import uuid
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator

from blooddonor.schemas.validators import (
    CommonFieldValidationMixin,
    PasswordValidationMixin,
)


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class DistrictEnum(str, Enum):
    BAGERHAT = "bagerhat"
    BANDARBAN = "bandarban"
    BARGUNA = "barguna"
    BARISAL = "barisal"
    BHOLA = "bhola"
    BOGURA = "bogura"
    BRAHMANBARIA = "brahmanbaria"
    CHANDPUR = "chandpur"
    CHAPAINAWABGANJ = "chapainawabganj"
    CHATTOGRAM = "chattogram"
    CHUADANGA = "chuadanga"
    COXS_BAZAR = "cox's bazar"
    CUMILLA = "cumilla"
    DHAKA = "dhaka"
    DINAJPUR = "dinajpur"
    FARIDPUR = "faridpur"
    FENI = "feni"
    GAIBANDHA = "gaibandha"
    GAZIPUR = "gazipur"
    GOPALGANJ = "gopalganj"
    HABIGANJ = "habiganj"
    JAMALPUR = "jamalpur"
    JESSORE = "jessore"
    JHALOKATI = "jhalokati"
    JHENAIDAH = "jhenaidah"
    JOYPURHAT = "joypurhat"
    KHAGRACHHARI = "khagrachhari"
    KHULNA = "khulna"
    KISHOREGANJ = "kishoreganj"
    KURIGRAM = "kurigram"
    KUSHTIA = "kushtia"
    LAKSHMIPUR = "lakshmipur"
    LALMONIRHAT = "lalmonirhat"
    MADARIPUR = "madaripur"
    MAGURA = "magura"
    MANIKGANJ = "manikganj"
    MEHERPUR = "meherpur"
    MOULVIBAZAR = "moulvibazar"
    MUNSHIGANJ = "munshiganj"
    MYMENSINGH = "mymensingh"
    NAOGAON = "naogaon"
    NARAIL = "narail"
    NARAYANGANJ = "narayanganj"
    NARSINGDI = "narsingdi"
    NATORE = "natore"
    NETROKONA = "netrokona"
    NILPHAMARI = "nilphamari"
    NOAKHALI = "noakhali"
    PABNA = "pabna"
    PANCHAGARH = "panchagarh"
    PATUAKHALI = "patuakhali"
    PIROJPUR = "pirojpur"
    RAJBARI = "rajbari"
    RAJSHAHI = "rajshahi"
    RANGAMATI = "rangamati"
    RANGPUR = "rangpur"
    SATKHIRA = "satkhira"
    SHARIATPUR = "shariatpur"
    SHERPUR = "sherpur"
    SIRAJGANJ = "sirajganj"
    SUNAMGANJ = "sunamganj"
    SYLHET = "sylhet"
    TANGAIL = "tangail"
    THAKURGAON = "thakurgaon"


class BloodGroupEnum(str, Enum):
    A_POSITIVE = "a+"
    A_NEGATIVE = "a-"
    B_POSITIVE = "b+"
    B_NEGATIVE = "b-"
    AB_POSITIVE = "ab+"
    AB_NEGATIVE = "ab-"
    O_POSITIVE = "o+"
    O_NEGATIVE = "o-"


class AcademicYearEnum(str, Enum):
    YEAR_2010_2011 = "2010-2011"
    YEAR_2011_2012 = "2011-2012"
    YEAR_2012_2013 = "2012-2013"
    YEAR_2013_2014 = "2013-2014"
    YEAR_2014_2015 = "2014-2015"
    YEAR_2015_2016 = "2015-2016"
    YEAR_2016_2017 = "2016-2017"
    YEAR_2017_2018 = "2017-2018"
    YEAR_2018_2019 = "2018-2019"
    YEAR_2019_2020 = "2019-2020"
    YEAR_2020_2021 = "2020-2021"
    YEAR_2021_2022 = "2021-2022"
    YEAR_2022_2023 = "2022-2023"
    YEAR_2023_2024 = "2023-2024"
    YEAR_2024_2025 = "2024-2025"
    YEAR_2025_2026 = "2025-2026"
    YEAR_2026_2027 = "2026-2027"
    YEAR_2027_2028 = "2027-2028"
    YEAR_2028_2029 = "2028-2029"
    YEAR_2029_2030 = "2029-2030"
    YEAR_2030_2031 = "2030-2031"
    YEAR_2031_2032 = "2031-2032"
    YEAR_2032_2033 = "2032-2033"
    YEAR_2033_2034 = "2033-2034"
    YEAR_2034_2035 = "2034-2035"
    YEAR_2035_2036 = "2035-2036"
    YEAR_2036_2037 = "2036-2037"
    YEAR_2037_2038 = "2037-2038"
    YEAR_2038_2039 = "2038-2039"
    YEAR_2039_2040 = "2039-2040"
    YEAR_2040_2041 = "2040-2041"
    YEAR_2041_2042 = "2041-2042"
    YEAR_2042_2043 = "2042-2043"
    YEAR_2043_2044 = "2043-2044"
    YEAR_2044_2045 = "2044-2045"
    YEAR_2045_2046 = "2045-2046"
    YEAR_2046_2047 = "2046-2047"
    YEAR_2047_2048 = "2047-2048"
    YEAR_2048_2049 = "2048-2049"
    YEAR_2049_2050 = "2049-2050"


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


class EmploymentStatusEnum(str, Enum):
    STUDENT = "student"
    EMPLOYED = "employed"
    UNEMPLOYED = "unemployed"


# User Schemas
class UserBase(BaseModel, CommonFieldValidationMixin):
    # personal info
    full_name: str
    email: EmailStr
    mobile: str
    department: DepartmentsEnum
    student_id: str
    gender: GenderEnum
    district: DistrictEnum
    blood_group: BloodGroupEnum
    academic_year: AcademicYearEnum
    is_available: bool = True
    # permission fields
    is_active: bool = True
    is_admin: bool = False
    is_superuser: bool = False
    created_on: datetime.datetime | None = None
    donated_on: datetime.datetime | None = None


class UserCreateBase(UserBase, CommonFieldValidationMixin, PasswordValidationMixin):
    full_name: str
    email: EmailStr
    mobile: str
    department: DepartmentsEnum
    student_id: str
    gender: GenderEnum
    district: DistrictEnum
    blood_group: BloodGroupEnum
    academic_year: AcademicYearEnum
    password: str = Field(exclude=True)


class UserUpdateBase(BaseModel, CommonFieldValidationMixin, PasswordValidationMixin):
    full_name: str | None = None
    blood_group: BloodGroupEnum | None = None
    district: DistrictEnum | None = None
    password: str | None = Field(default=None, exclude=True)


class UpdateBySuperUser(UserBase, CommonFieldValidationMixin, PasswordValidationMixin):
    full_name: str | None = None
    email: EmailStr | None = None
    mobile: str | None = None
    department: DepartmentsEnum | None = None
    student_id: str | None = None
    gender: GenderEnum | None = None
    district: DistrictEnum | None = None
    blood_group: BloodGroupEnum | None = None
    academic_year: AcademicYearEnum | None = None
    # permission fields
    is_active: bool | None = True
    is_admin: bool | None = False
    is_superuser: bool | None = False
    password: str | None = Field(exclude=True, default=None)


# update user password schema
class UserChangePassword(BaseModel, PasswordValidationMixin):
    token: str
    password: str


class UserInDBBase(UserBase):
    id: uuid.UUID | None = None

    class Config:
        from_attributes = True


# for additional info returned by api
class UserApi(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str = Field(exclude=True)


class UserProfile(BaseModel):
    profile_img: str | None = None
    facebook: str | None = None
    instagram: str | None = None
    linkedin: str | None = None
    website: str | None = None
    employment_status: str | EmploymentStatusEnum = None

    @field_validator("employment_status", check_fields=False)
    def validate_employment_status(cls, v):
        if v in EmploymentStatusEnum:
            return v
        raise ValueError(
            "Please input one from these options: student, employed, unemployed"
        )


class ProfileResponse(UserProfile):
    id: uuid.UUID | None = None
    donor_id: uuid.UUID | None = None

    class Config:
        from_attributes = True


class UpdateProfile(UserProfile):
    pass


class DonorFilterSchema(BaseModel):
    full_name: str | None = None
    student_id: str | None = None
    gender: GenderEnum | None = None
    district: DistrictEnum | None = None
    blood_group: BloodGroupEnum | None = None
    academic_year: AcademicYearEnum | None = None
    department: DepartmentsEnum | None = None

    class Config:
        from_attributes = True
