from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.meta import Meta
from app.models.user import User

router = APIRouter(prefix="/meta", tags=["meta"])

@router.post("")
def criar_meta(
    valor: float,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    nova = Meta(
        valor_limite=valor,
        user_id=user.id  # ✅ importante
    )

    db.add(nova)
    db.commit()

    return {
        "status": "meta criada",
        "valor": valor
    }