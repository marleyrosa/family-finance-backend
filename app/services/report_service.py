import csv
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy import extract, select
from sqlalchemy.orm import Session

from app.models.expense import Expense


def export_expenses_csv(db: Session, mes: int, ano: int, output_path: Path) -> Path:
    expenses = db.scalars(
        select(Expense).where(extract("month", Expense.data) == mes, extract("year", Expense.data) == ano)
    ).all()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "descricao", "valor", "data", "categoria", "pdf_path"])
        for exp in expenses:
            writer.writerow([exp.id, exp.descricao, str(exp.valor), exp.data.isoformat(), exp.categoria, exp.pdf_path])

    return output_path


def export_expenses_pdf(db: Session, mes: int, ano: int, output_path: Path) -> Path:
    expenses = db.scalars(
        select(Expense).where(extract("month", Expense.data) == mes, extract("year", Expense.data) == ano)
    ).all()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, f"Relatorio de Despesas - {mes:02d}/{ano}")
    y -= 30

    c.setFont("Helvetica", 10)
    for exp in expenses:
        line = f"{exp.data.isoformat()} | {exp.categoria} | R$ {exp.valor} | {exp.descricao}"
        c.drawString(40, y, line[:110])
        y -= 16
        if y < 60:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50

    c.save()
    return output_path
