import datetime
import re
import uuid
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator


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


class StudentShipStatusEnum(str, Enum):
    FIRST_YEAR = "1st"
    SECOND_YEAR = "2nd"
    THIRD_YEAR = "3rd"
    FOURTH_YEAR = "4th"
    MASTERS = "ms"
    UNEMPLOYED = "unemployed"
    EMPLOYED = "employed"


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


# User Schemas
class UserBase(BaseModel):
    # personal info
    full_name: str
    email: EmailStr
    mobile: str
    department: DepartmentsEnum
    student_id: str
    gender: GenderEnum
    district: DistrictEnum
    blood_group: BloodGroupEnum
    studentship_status: StudentShipStatusEnum
    is_available: bool = True
    # permission fields
    is_active: bool = True
    is_admin: bool = False
    is_superuser: bool = False
    created_on: datetime.datetime | None = None
    donated_on: datetime.datetime | None = None

    @field_validator("full_name")
    def name_validator(cls, v):
        if v is None or v.strip() == "":
            raise ValueError("Name is not valid!")
        return v

    @field_validator("mobile")
    def mobile_validator(cls, v):
        mobile_regex = r"(?:\+88)?(01[\d]+)"
        mobile = re.match(mobile_regex, v)
        if mobile:
            mobile = mobile.group(1)
            if isinstance(int(mobile), int) and len(mobile) == 11:
                return mobile
        raise ValueError("The number format is invalid. Use numbers like 017xxxxxxxx")

    @field_validator("department", mode="before")
    def department_validator(cls, v):
        if v in DepartmentsEnum:
            return v
        raise ValueError("The provided dept code doesn't match with any department.")

    @field_validator("student_id")
    def student_id_validator(cls, v, info):
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
            "The student id is not valid or doesn't associated with respective department."
        )


class UserCreateBase(UserBase):
    full_name: str
    email: EmailStr
    mobile: str
    department: DepartmentsEnum
    student_id: str
    gender: GenderEnum
    district: DistrictEnum
    blood_group: BloodGroupEnum
    studentship_status: StudentShipStatusEnum
    password: str = Field(exclude=True)

    @field_validator("password")
    def password_validator(cls, v):
        if len(v) < 5:
            raise ValueError("Password must be equal or greater than 5 characters")
        return v


class UserUpdateBase(UserBase):
    full_name: str | None = None
    mobile: str | None = None
    district: DistrictEnum | None = None
    studentship_status: StudentShipStatusEnum | None = None
    is_available: bool = True
    password: str | None = Field(default=None, exclude=True)


# update user password schema
class UserChangePassword(BaseModel):
    token: str
    password: str

    @field_validator("password")
    def password_validator(cls, v):
        if len(v) < 5:
            raise ValueError("Password must be equal or greater than 5 characters")
        return v


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
    studentship_status: StudentShipStatusEnum | None = None
    department: DepartmentsEnum | None = None

    class Config:
        from_attributes = True
