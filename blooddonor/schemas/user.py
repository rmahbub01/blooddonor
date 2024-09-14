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


class DepartmentsEnum(int, Enum):
    ARABIC = 1
    BANGLADESH_STUDIES = 2
    BENGALI = 3
    DRAMATICS = 4
    ENGLISH = 5
    HISTORY = 6
    ISLAMIC_HISTORY_CULTURE = 7
    ISLAMIC_STUDIES = 8
    MUSIC = 9
    PALI = 10
    PERSIAN_LANGUAGE_LITERATURE = 11
    PHILOSOPHY = 12
    SANSKRIT = 13
    INSTITUTE_OF_EDUCATION_RESEARCH = 14
    INSTITUTE_OF_FINE_ARTS = 15
    INSTITUTE_OF_MODERN_LANGUAGES = 16
    BIOCHEMISTRY_MOLECULAR_BIOLOGY = 17
    BOTANY = 18
    GENETIC_ENGINEERING_BIOTECHNOLOGY = 19
    GEOGRAPHY_ENVIRONMENTAL_SCIENCE = 20
    MICROBIOLOGY = 21
    PHARMACY = 22
    PSYCHOLOGY = 23
    SOIL_SCIENCE = 24
    ZOOLOGY = 25
    ACCOUNTING = 26
    BANKING_INSURANCE = 27
    FINANCE = 28
    HUMAN_RESOURCE_MANAGEMENT = 29
    MANAGEMENT = 30
    MARKETING = 31
    PHYSICAL_EDUCATION_SPORTS_SCIENCE = 32
    COMPUTER_SCIENCE_ENGINEERING = 33
    ELECTRICAL_ELECTRONIC_ENGINEERING = 34
    LAW = 35
    APPLIED_CHEMISTRY_CHEMICAL_ENGINEERING = 36
    CHEMISTRY = 37
    MATHEMATICS = 38
    MATHEMATICS_SCIENCE_RESEARCH_CENTER = 39
    PHYSICS = 40
    STATISTICS = 41
    INSTITUTE_OF_FORESTRY_ENVIRONMENTAL_SCIENCE = 42
    INSTITUTE_OF_MARINE_SCIENCE_FISHERIES = 43
    ANTHROPOLOGY = 44
    COMMUNICATION_JOURNALISM = 45
    CRIMINOLOGY_POLICE_SCIENCE = 46
    DEVELOPMENT_STUDIES = 47
    ECONOMICS = 48
    INTERNATIONAL_RELATIONS = 49
    POLITICAL_SCIENCE = 50
    PUBLIC_ADMINISTRATION = 51
    SOCIOLOGY = 52


# User Schemas
class UserBase(BaseModel):
    # personal info
    full_name: str
    email: EmailStr
    mobile: str
    department: DepartmentsEnum
    student_id: str | int
    gender: GenderEnum
    district: DistrictEnum
    blood_group: BloodGroupEnum
    studentship_status: StudentShipStatusEnum
    is_available: bool = True
    # permission fields
    is_active: bool = True
    is_admin: bool = False
    is_superuser: bool = False
    created_on: datetime.datetime = datetime.datetime.now(datetime.UTC)

    @field_validator("full_name")
    def name_validator(cls, v):
        if v is None or v.strip() == "":
            raise ValueError("Name is not valid!")
        return v

    @field_validator("mobile")
    def mobile_validator(cls, v):
        if len(v) == 11 and isinstance(int(v), int):
            return v
        raise ValueError("The number format is invalid. Use numbers like 017xxxxxxxx")

    @field_validator("student_id")
    def student_id_validator(cls, v):
        student_id_regex = r"[2-9]{1}[\d]{1}[123]{1}[\d]{5}"
        if len(str(v)) == 8 and re.match(student_id_regex, str(v)):
            return v
        raise ValueError("The student id is not valid.")

    @field_validator("department")
    def department_validator(cls, v):
        if v in DepartmentsEnum:
            return v
        raise ValueError("The provided integer doesn't match with any department.")


class UserCreateBase(UserBase):
    full_name: str
    email: EmailStr
    mobile: str
    department: DepartmentsEnum
    student_id: str | int
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
