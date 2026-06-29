from pydantic import BaseModel, EmailStr


# ✅ BASE
class UserBase(BaseModel):
    nome: str
    email: EmailStr


# ✅ CRIAÇÃO
class UserCreate(UserBase):
    password: str


# ✅ RESPOSTA
class UserResponse(UserBase):
    id: int

    cmodel_config = {
    "from_attributes": True
}

