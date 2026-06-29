from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserRelation(Base):
    __tablename__ = "relacoes_usuarios"
    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="uq_relacao_casal"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user1_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user2_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
