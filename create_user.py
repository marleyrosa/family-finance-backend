from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

# ✅ MARLEY
marley = User(
    nome="Marley",
    email="marley@gmail.com",
    password_hash=hash_password("123456")
)

# ✅ SILVIA
silvia = User(
    nome="Silvia",
    email="silvia@gmail.com",
    password_hash=hash_password("123456")
)

db.add(marley)
db.add(silvia)

db.commit()

print("✅ usuários Marley e Silvia criados com sucesso")