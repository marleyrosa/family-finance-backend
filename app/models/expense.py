from datetime import datetime

from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    descricao: Mapped[str] = mapped_column(String(255))
    valor: Mapped[float] = mapped_column(Float)
    categoria: Mapped[str] = mapped_column(String(100), default="Outros")

    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    pdf_path: Mapped[str] = mapped_column(String(255), default="manual")

    # ✅ ✅ AGORA SIM: RELAÇÃO COM USUÁRIO
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User")