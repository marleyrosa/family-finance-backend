from sqlalchemy import Column, Integer, Float
from app.db.base import Base

class Meta(Base):
    __tablename__ = "metas"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    valor_limite = Column(Float)
