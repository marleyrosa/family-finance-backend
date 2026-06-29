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

    class Config:
        orm_mode = True
