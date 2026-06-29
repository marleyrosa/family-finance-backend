from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ExpenseOut(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    data: date
    categoria: str
    pdf_path: str

    model_config = ConfigDict(from_attributes=True)
