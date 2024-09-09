import datetime
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


# User Schemas
class UserBase(BaseModel):
    # personal info
    full_name: str
    email: EmailStr
    mobile: str
    nid: str = Field(exclude=True)
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

    @field_validator("nid")
    def nid_validator(cls, v):
        if (len(v) == 10 or len(v) == 13) and isinstance(int(v), int):
            return v
        raise ValueError("Please enter a valid nid number.")


class UserCreateBase(UserBase):
    full_name: str
    email: EmailStr
    mobile: str
    nid: str
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
    email: EmailStr | None = None
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
