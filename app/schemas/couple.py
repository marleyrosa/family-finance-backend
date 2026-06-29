from pydantic import BaseModel, ConfigDict, EmailStr


class CoupleInvite(BaseModel):
    email: EmailStr


class CoupleOut(BaseModel):
    id: int
    user1_id: int
    user2_id: int

    model_config = ConfigDict(from_attributes=True)
