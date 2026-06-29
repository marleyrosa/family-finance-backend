# Backend - Family Finance

API REST com FastAPI para gerenciamento financeiro familiar.

## Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT
- Upload e leitura de PDF (pdfplumber)

## Estrutura

```text
backend/
  app/
    models/
    routes/
    services/
    schemas/
```

## Como rodar

1. Suba o PostgreSQL:

```bash
docker compose up -d
```

1. Crie e ative ambiente virtual:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

1. Instale dependencias:

```bash
pip install -r requirements.txt
```

1. Configure variaveis:

```bash
copy .env.example .env
```

1. Rode a API:

```bash
uvicorn app.main:app --reload --port 8000
```

Swagger: <http://localhost:8000/docs>
