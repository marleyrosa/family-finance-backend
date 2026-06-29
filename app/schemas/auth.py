from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    nome: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
