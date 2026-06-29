from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

user = User(
    email="test@example.com",
    senha=hash_password("123456")
)

db.add(user)
db.commit()

print("✅ usuário criado")
from datetime import datetime
from app.db.session import SessionLocal
from app.models.expense import Expense

db = SessionLocal()

dados = [
    ("Energia", "ENERGIA", 122.43),
    ("Energia", "ENERGIA", 204),
    ("Internet", "INTERNET", 156),
    ("Seguranca", "SEGURANCA", 30),
    ("Tratamento Alergia", "SAUDE", 210),
    ("FIES", "FIXO", 887),
    ("TV", "FIXO", 59),
    ("Agua", "AGUA", 52),
    ("Amazon", "SUPERMERCADO", 231),
    ("Seguro Carro", "CARRO", 181),
    ("Lava Jato", "TRANSPORTE", 80),
    ("Saude", "SAUDE", 31),
    ("Carro", "CARRO", 206),
    ("Supermercado", "SUPERMERCADO", 811.2),
    ("Restaurante", "RESTAURANTE", 305.26),
    ("Casa", "CASA", 135),
    ("Saude Extra", "SAUDE", 180),
    ("Divisao", "SAUDE", 334),
    ("Shein", "CASA", 65),
]

meses = [1, 2, 3, 4, 5]

for mes in meses:
    for nome, categoria, valor in dados:
        db.add(Expense(
            descricao=nome,
            valor=float(valor),
            categoria=categoria,
            data=datetime(2026, mes, 1),
            pdf_path="manual"  # ✅ ESSENCIAL
        ))

db.commit()

print("✅ HISTÓRICO INSERIDO")