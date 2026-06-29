from decimal import Decimal

from pydantic import BaseModel


class DivisionUserResult(BaseModel):
    user_id: int
    nome: str
    renda: Decimal
    percentual: float
    valor_devido: Decimal


class DivisionResult(BaseModel):
    mes: int
    ano: int
    total_despesas: Decimal
    total_renda: Decimal
    usuarios: list[DivisionUserResult]
