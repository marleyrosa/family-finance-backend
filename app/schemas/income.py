from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class IncomeCreate(BaseModel):
    valor: Decimal
    mes: int
    ano: int


class IncomeOut(BaseModel):
    id: int
    user_id: int
    valor: Decimal
    mes: int
    ano: int

    model_config = ConfigDict(from_attributes=True)
