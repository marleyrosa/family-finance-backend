from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.relation import UserRelation
from app.models.user import User
from app.schemas.couple import CoupleInvite, CoupleOut

router = APIRouter(prefix="/casal", tags=["casal"])


@router.post("/convidar", response_model=CoupleOut, status_code=status.HTTP_201_CREATED)
def invite_partner(
    payload: CoupleInvite,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    invited_user = db.scalar(select(User).where(User.email == payload.email))
    if not invited_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario convidado nao encontrado")

    if invited_user.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nao e possivel convidar a si mesmo")

    existing_relation = db.scalar(
        select(UserRelation).where(
            or_(
                UserRelation.user1_id == current_user.id,
                UserRelation.user2_id == current_user.id,
                UserRelation.user1_id == invited_user.id,
                UserRelation.user2_id == invited_user.id,
            )
        )
    )
    if existing_relation:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Relacao de casal ja existe")

    user1_id, user2_id = sorted([current_user.id, invited_user.id])
    relation = UserRelation(user1_id=user1_id, user2_id=user2_id)
    db.add(relation)
    db.commit()
    db.refresh(relation)
    return relation


@router.get("/me", response_model=CoupleOut)
def get_my_relation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    relation = db.scalar(
        select(UserRelation).where(
            or_(UserRelation.user1_id == current_user.id, UserRelation.user2_id == current_user.id)
        )
    )
    if not relation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relacao de casal nao encontrada")
    return relation
