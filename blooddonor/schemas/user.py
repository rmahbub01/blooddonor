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
    # Arts and Humanities
    ARABIC = "1"
    BANGLADESH_STUDIES = "2"
    BANGLA = "3"
    DRAMATICS = "4"
    EDUCATION_AND_RESEARCH = "5"
    ENGLISH = "6"
    ENGLISH_TEACHERS_OF_ARTS_AND_HUMANITIES_FACULTY = "7"
    FINE_ARTS = "8"
    HISTORY = "9"
    ISLAMIC_HISTORY_AND_CULTURE = "10"
    ISLAMIC_STUDIES = "11"
    MODERN_LANGUAGES = "12"
    MUSIC = "13"
    PALI = "14"
    PERSIAN_LANGUAGE_AND_LITERATURE = "15"
    PHILOSOPHY = "16"
    SANSKRIT = "17"

    # Science
    APPLIED_CHEMISTRY_AND_CHEMICAL_ENGINEERING = "18"
    CHEMISTRY = "19"
    ENGLISH_TEACHERS_OF_SCIENCE_FACULTY = "20"
    FORESTRY_AND_ENVIRONMENTAL_SCIENCES = "21"
    JAMAL_NAZRUL_ISLAM_RESEARCH_CENTRE = "22"
    MATHEMATICS = "23"
    PHYSICS = "24"
    STATISTICS = "25"

    # Business Administration
    ACCOUNTING = "26"
    BANKING_AND_INSURANCE = "27"
    BUREAU_OF_BUSINESS_RESEARCH = "28"
    CENTER_FOR_BUSINESS_ADMINISTRATION = "29"
    ENGLISH_TEACHERS_OF_BUSINESS_ADMINISTRATION_FACULTY = "30"
    FINANCE = "31"
    HUMAN_RESOURCE_MANAGEMENT = "32"
    MANAGEMENT = "33"
    MARKETING = "34"

    # Social Sciences
    ANTHROPOLOGY = "35"
    COMMUNICATION_AND_JOURNALISM = "36"
    CRIMINOLOGY_AND_POLICE_SCIENCE = "37"
    DEVELOPMENT_STUDIES = "38"
    ECONOMICS = "39"
    ENGLISH_TEACHERS_OF_SOCIAL_SCIENCES_FACULTY = "40"
    INTERNATIONAL_RELATIONS = "41"
    POLITICAL_SCIENCE = "42"
    PUBLIC_ADMINISTRATION = "43"
    SOCIAL_SCIENCE_RESEARCH = "44"
    SOCIOLOGY = "45"

    # Law
    LAW = "46"

    # Biological Sciences
    BIOCHEMISTRY_AND_MOLECULAR_BIOLOGY = "47"
    BOTANY = "48"
    ENGLISH_TEACHERS_OF_BIOLOGICAL_SCIENCES_FACULTY = "49"
    GEOGRAPHY_AND_ENVIRONMENTAL_STUDIES = "50"
    GENETIC_ENGINEERING_AND_BIOTECHNOLOGY = "51"
    MICROBIOLOGY = "52"
    PHARMACY = "53"
    PSYCHOLOGY = "54"
    SOIL_SCIENCE = "55"
    ZOOLOGY = "56"

    # Engineering
    COMPUTER_SCIENCE_AND_ENGINEERING = "57"
    ELECTRICAL_AND_ELECTRONIC_ENGINEERING = "58"

    # Education
    PHYSICAL_EDUCATION_AND_SPORTS_SCIENCE = "59"

    # Marine Sciences and Fisheries
    FISHERIES = "60"
    MARINE_SCIENCES = "61"
    OCEANOGRAPHY = "62"

    # Medicine
    COMMUNITY_OPHTHALMOLOGY = "63"
    PAEDIATRICS = "64"


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
        student_id_regex = r"[1-9]{1}[\d]{1}[1-9]{1}[\d]{5}"
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
