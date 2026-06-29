from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import extract, func, or_, select
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income
from app.models.relation import UserRelation
from app.models.user import User


def _get_couple_user_ids(db: Session, user_id: int) -> list[int]:
    relation = db.scalar(
        select(UserRelation).where(or_(UserRelation.user1_id == user_id, UserRelation.user2_id == user_id))
    )
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relacao de casal nao encontrada",
        )
    return [relation.user1_id, relation.user2_id]


def calculate_division(db: Session, current_user: User, mes: int, ano: int) -> dict:
    user_ids = _get_couple_user_ids(db, current_user.id)

    users = db.scalars(select(User).where(User.id.in_(user_ids))).all()
    incomes = db.scalars(select(Income).where(Income.user_id.in_(user_ids), Income.mes == mes, Income.ano == ano)).all()

    total_expenses = db.scalar(
        select(func.coalesce(func.sum(Expense.valor), 0)).where(
            extract("month", Expense.data) == mes,
            extract("year", Expense.data) == ano,
        )
    )

    income_by_user = {user.id: Decimal("0.00") for user in users}
    for income in incomes:
        income_by_user[income.user_id] += Decimal(income.valor)

    total_income = sum(income_by_user.values(), Decimal("0.00"))
    if total_income <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Renda total precisa ser maior que zero para calcular a divisao",
        )

    users_result = []
    for user in users:
        user_income = income_by_user[user.id]
        percent_decimal = user_income / total_income
        due_value = (percent_decimal * Decimal(total_expenses)).quantize(Decimal("0.01"))
        users_result.append(
            {
                "user_id": user.id,
                "nome": user.nome,
                "renda": user_income,
                "percentual": round(float(percent_decimal * Decimal("100")), 2),
                "valor_devido": due_value,
            }
        )

    return {
        "mes": mes,
        "ano": ano,
        "total_despesas": Decimal(total_expenses),
        "total_renda": total_income,
        "usuarios": users_result,
    }
