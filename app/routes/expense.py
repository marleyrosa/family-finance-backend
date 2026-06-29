from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from typing import List
from pydantic import BaseModel

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseOut
from app.services.pdf_service import parse_pdf_data

router = APIRouter(prefix="/despesas", tags=["despesas"])


# ✅ UPLOAD PDF
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_expense_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser PDF")

    contents = await file.read()

    try:
        itens = parse_pdf_data(contents)
    except Exception as e:
        print("ERRO AO PROCESSAR PDF:", e)
        raise HTTPException(status_code=500, detail="Erro ao processar PDF")

    if not itens:
        raise HTTPException(status_code=400, detail="Nenhum item encontrado no PDF")

    inseridos = 0

    for item in itens:
        try:
            nova = Expense(
                descricao=item.get("descricao", "Sem descrição"),
                valor=float(item.get("valor", 0)),
                data=item.get("data") or datetime.now(),
                categoria=item.get("categoria", "Outros"),
                pdf_path="upload",
                user_id=user.id  # ✅ AGORA RELACIONA AO USUÁRIO
            )

            db.add(nova)
            inseridos += 1

        except Exception as e:
            print("ERRO AO SALVAR ITEM:", e)

    db.commit()

    return {
        "status": "sucesso",
        "quantidade_inserida": inseridos
    }


# ✅ LISTAR DESPESAS
@router.get("", response_model=list[ExpenseOut])
def list_expenses(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return db.scalars(
        select(Expense)
        .where(Expense.user_id == user.id)
        .order_by(Expense.data.desc())
    ).all()


# ✅ SCHEMA MANUAL
class DespesaManual(BaseModel):
    descricao: str
    valor: float
    data: str
    categoria: str


# ✅ ROTA MANUAL (CORRETA)
@router.post("/manual")
def inserir_despesas_manual(
    despesas: List[DespesaManual],
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    total = 0

    for d in despesas:
        try:
            nova = Expense(
                descricao=d.descricao,
                valor=d.valor,
                categoria=d.categoria,
                data=d.data,
                pdf_path="manual",
                user_id=user.id  # ✅ IMPORTANTE
            )
            db.add(nova)
            total += 1

        except Exception as e:
            print("Erro ao inserir:", e)

    db.commit()

    return {
        "status": "sucesso",
        "quantidade_inserida": total
    }