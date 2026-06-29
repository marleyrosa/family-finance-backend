from decimal import Decimal

from pydantic import BaseModel


class SummaryCards(BaseModel):
    total_despesas: Decimal
    total_renda: Decimal
    saldo: Decimal


class MonthlyPoint(BaseModel):
    mes: str
    despesas: float
    rendas: float


class CategoryPoint(BaseModel):
    categoria: str
    valor: float


class UserSplitPoint(BaseModel):
    nome: str
    valor_devido: float
    percentual: float


class DashboardResponse(BaseModel):
    cards: SummaryCards
    evolucao_mensal: list[MonthlyPoint]
    gastos_por_categoria: list[CategoryPoint]
    divisao_por_pessoa: list[UserSplitPoint]
