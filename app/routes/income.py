from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.income import Income
from app.models.user import User
from app.schemas.income import IncomeCreate, IncomeOut

router = APIRouter(prefix="/rendas", tags=["rendas"])


# ✅ CRIAR RENDA (AGORA PERMITE VÁRIAS)
@router.post("", response_model=IncomeOut, status_code=status.HTTP_201_CREATED)
def create_income(
    payload: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        nova = Income(
            user_id=current_user.id,
            valor=payload.valor,
            mes=payload.mes,
            ano=payload.ano,
        )

        db.add(nova)
        db.commit()
        db.refresh(nova)

        return nova

    except Exception as e:
        print("Erro ao criar renda:", e)
        return {"error": "Erro ao salvar renda"}


# ✅ LISTAR RENDAS DO USUÁRIO
@router.get("", response_model=list[IncomeOut])
def list_my_incomes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.scalars(
        select(Income)
        .where(Income.user_id == current_user.id)
        .order_by(Income.id.desc())
    ).all()


# ✅ EXTRA: DELETAR RENDA (OPCIONAL)
@router.delete("/{income_id}")
def delete_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    renda = db.get(Income, income_id)

    if not renda or renda.user_id != current_user.id:
        return {"error": "Renda não encontrada"}

    db.delete(renda)
    db.commit()

    return {"status": "removido"}