from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.models.user import User

router = APIRouter(tags=["login"])


@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email e senha sao obrigatorios",
        )

    user = db.scalar(select(User).where(User.email == email))
    password_hash = user.senha or user.password_hash if user else None

    if not user or not password_hash or not verify_password(senha, password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais invalidas",
        )

    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
