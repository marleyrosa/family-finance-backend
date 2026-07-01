from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine

from app.routes.auth import router as auth_router
from app.routes.auth import public_router as auth_public_router
from app.routes.couple import router as couple_router
from app.routes.dashboard import router as dashboard_router
from app.routes.division import router as division_router
from app.routes.expense import router as expense_router
from app.routes.finance import router as finance_router
from app.routes.income import router as income_router
from app.routes.login import router as login_router
from app.routes.report import router as report_router
from app.routes.meta import router as meta_router

# 👉 Importa models (IMPORTANTE)
from app.models import expense, income, relation, user  # noqa: F401
from app.models import finance  # noqa: F401

# ✅ CONFIGURAÇÕES
settings = get_settings()

configured_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
render_frontend_origin = "https://family-finance-frontend-7cc4.onrender.com"
if render_frontend_origin not in configured_origins:
    configured_origins.append(render_frontend_origin)

# ✅ APP
app = FastAPI(
    title="Family Finance API",
    version="1.0.0"
)

# ✅ ✅ CORS LIBERADO
app.add_middleware(
    CORSMiddleware,
    allow_origins=configured_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ✅ CRIAR TABELAS (SEM APAGAR)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)  # ✅ NÃO usa drop_all


# ✅ ✅ HEALTH CHECK
@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "family-finance-backend"
    }


# ✅ ✅ ROTAS
app.include_router(auth_public_router)
app.include_router(auth_router)
app.include_router(login_router)
app.include_router(couple_router)
app.include_router(income_router)
app.include_router(expense_router)
app.include_router(division_router)
app.include_router(dashboard_router)
app.include_router(report_router)
app.include_router(meta_router)
app.include_router(finance_router)
