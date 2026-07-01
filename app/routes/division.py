from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.expense import Expense
from app.models.user import User
from app.schemas.division import DivisionResult
from app.services.division_service import calculate_division

router = APIRouter(prefix="/divisao", tags=["divisao"])


@router.get("/resumo")
def resumo_divisao(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    totais = db.query(
        Expense.user_id,
        func.sum(Expense.valor)
    ).group_by(Expense.user_id).all()

    resultado = {user_id: total for user_id, total in totais}

    total_geral = sum(resultado.values())

    return {
        "total_geral": total_geral,
        "por_usuario": resultado
    }


@router.get("/{mes}/{ano}", response_model=DivisionResult)
def get_division(
    mes: int,
    ano: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return calculate_division(db, current_user, mes, ano)
