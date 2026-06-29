from pathlib import Path
from uuid import uuid4
from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.expense import Expense

from app.services.report_service import export_expenses_csv, export_expenses_pdf
from app.services.pdf_reader import extract_items_from_pdf
from app.services.category_ai import categorize_expense

# ✅ ✅ ISSO FALTAVA (CAUSAVA O ERRO)
router = APIRouter(prefix="/relatorios", tags=["relatorios"])

REPORTS_DIR = Path("reports")


# ✅ DOWNLOAD CSV
@router.get("/csv/{mes}/{ano}")
def download_csv(
    mes: int,
    ano: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    file_path = REPORTS_DIR / f"despesas_{mes}_{ano}_{uuid4().hex}.csv"
    output = export_expenses_csv(db, mes, ano, file_path)

    return FileResponse(
        path=str(output),
        filename=output.name,
        media_type="text/csv"
    )


# ✅ DOWNLOAD PDF
@router.get("/pdf/{mes}/{ano}")
def download_pdf(
    mes: int,
    ano: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    file_path = REPORTS_DIR / f"despesas_{mes}_{ano}_{uuid4().hex}.pdf"
    output = export_expenses_pdf(db, mes, ano, file_path)

    return FileResponse(
        path=str(output),
        filename=output.name,
        media_type="application/pdf"
    )


# ✅ UPLOAD COMPLETO COM EXTRAÇÃO + SALVAMENTO
@router.post("/upload")
async def upload_boleto(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contents = await file.read()

    # ✅ extrair itens da fatura
    itens = extract_items_from_pdf(contents)

    resultados = []

    for item in itens:
        categoria = categorize_expense(item["descricao"])

        nova = Expense(
            valor=item["valor"],
            mes=datetime.now().month,
            ano=datetime.now().year,
            descricao=item["descricao"],
            categoria=categoria,
            user_id=user.id
        )

        # ✅ salvar cartão (se existir no model)
        try:
            nova.cartao = item.get("cartao")
        except:
            pass

        db.add(nova)

        resultados.append({
            "descricao": item["descricao"],
            "valor": item["valor"],
            "categoria": categoria,
            "cartao": item.get("cartao"),
        })

    db.commit()

    return {
        "status": "processado",
        "itens": resultados
    }