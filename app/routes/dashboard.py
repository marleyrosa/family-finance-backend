from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, select

from app.db.session import get_db
from app.models.expense import Expense
from app.models.income import Income
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def get_dashboard(
    mes: int,
    ano: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # USUÁRIO LOGADO
    usuario_nome = current_user.nome

    # TOTAL DESPESAS
    total_despesas = float(
        db.scalar(
            select(func.coalesce(func.sum(Expense.valor), 0)).where(
                Expense.user_id == current_user.id,
                extract("month", Expense.data) == mes,
                extract("year", Expense.data) == ano,
            )
        ) or 0
    )

    # TOTAL RENDA
    total_renda = float(
        db.scalar(
            select(func.coalesce(func.sum(Income.valor), 0)).where(
                Income.user_id == current_user.id,
                Income.mes == mes,
                Income.ano == ano,
            )
        ) or 0
    )

    saldo = total_renda - total_despesas

    # GASTOS POR CATEGORIA
    category_rows = db.execute(
        select(
            Expense.categoria,
            func.coalesce(func.sum(Expense.valor), 0)
        ).where(
            extract("month", Expense.data) == mes,
            extract("year", Expense.data) == ano,
        ).group_by(Expense.categoria)
    ).all()

    categorias = [
        {"categoria": cat or "Outros", "valor": float(valor)}
        for cat, valor in category_rows
    ]

    # EVOLUÇÃO MENSAL
    monthly_rows = db.execute(
        select(
            extract("month", Expense.data),
            func.coalesce(func.sum(Expense.valor), 0)
        ).where(
            extract("year", Expense.data) == ano
        ).group_by(extract("month", Expense.data))
    ).all()

    evolucao = [
        {"mes": int(m), "despesas": float(v)}
        for m, v in monthly_rows
    ]

    # RENDA POR PESSOA
    renda_por_usuario = db.execute(
        select(
            User.nome,
            func.coalesce(func.sum(Income.valor), 0)
        )
        .join(Income, Income.user_id == User.id)
        .where(
            Income.mes == mes,
            Income.ano == ano
        )
        .group_by(User.nome)
    ).all()

    rendas = [
        {"nome": nome, "valor": float(valor)}
        for nome, valor in renda_por_usuario
    ]

    return {
        "usuario": usuario_nome,
        "cards": {
            "total_despesas": total_despesas,
            "total_renda": total_renda,
            "saldo": saldo,
        },
        "gastos_por_categoria": categorias,
        "evolucao_mensal": evolucao,
        "renda_por_pessoa": rendas
    }
