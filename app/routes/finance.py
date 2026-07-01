from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.finance import DEFAULT_CATEGORIES, Expense, Income
from app.models.user import User

router = APIRouter(tags=["finance"])


class ExpenseCreate(BaseModel):
    category: str
    amount: float


class IncomeCreate(BaseModel):
    amount: float


@router.post("/expense", status_code=status.HTTP_201_CREATED)
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount deve ser maior que 0")

    if payload.category not in DEFAULT_CATEGORIES:
        raise HTTPException(status_code=400, detail="Categoria invalida")

    new_expense = Expense(
        user_email=current_user.email,
        category=payload.category,
        amount=float(payload.amount),
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.post("/income", status_code=status.HTTP_201_CREATED)
def create_income(
    payload: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount deve ser maior que 0")

    new_income = Income(
        user_email=current_user.email,
        amount=float(payload.amount),
    )
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income


@router.get("/expenses")
def list_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _ = current_user
    return db.scalars(select(Expense).order_by(Expense.created_at.desc())).all()


@router.get("/incomes")
def list_incomes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _ = current_user
    return db.scalars(select(Income).order_by(Income.created_at.desc())).all()


@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _ = current_user

    total_expense = float(db.scalar(select(func.coalesce(func.sum(Expense.amount), 0.0))) or 0.0)
    total_income = float(db.scalar(select(func.coalesce(func.sum(Income.amount), 0.0))) or 0.0)

    return {
        "total_expense": total_expense,
        "total_income": total_income,
        "balance": total_income - total_expense,
    }


@router.get("/split")
def get_split(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _ = current_user

    total_expense = float(db.scalar(select(func.coalesce(func.sum(Expense.amount), 0.0))) or 0.0)

    income_rows = db.execute(
        select(
            Income.user_email,
            func.coalesce(func.sum(Income.amount), 0.0).label("income"),
        )
        .group_by(Income.user_email)
        .order_by(Income.user_email)
    ).all()

    total_income = float(sum(float(row.income or 0.0) for row in income_rows))

    users = []
    for row in income_rows:
        income_value = float(row.income or 0.0)
        share = (income_value / total_income) if total_income > 0 else 0.0
        amount_to_pay = total_expense * share
        users.append(
            {
                "user_email": row.user_email,
                "income": income_value,
                "percentage": round(share * 100, 2),
                "amount_to_pay": round(amount_to_pay, 2),
            }
        )

    return {
        "total_expense": total_expense,
        "total_income": total_income,
        "users": users,
    }


@router.get("/categories")
def list_categories(
    current_user: User = Depends(get_current_user),
):
    _ = current_user
    return {"categories": DEFAULT_CATEGORIES}
