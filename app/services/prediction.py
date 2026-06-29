from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.expense import Expense


def prever_gastos(db: Session, user_id: int):
    resultados = db.query(
        extract("month", Expense.data).label("mes"),
        func.sum(Expense.valor).label("total")
    ).filter(
        Expense.user_id == user_id
    ).group_by("mes").all()

    valores = [float(r.total) for r in resultados]

    if not valores:
        return 0

    # ✅ média simples (AI básica)
    previsao = sum(valores) / len(valores)

    return round(previsao, 2)