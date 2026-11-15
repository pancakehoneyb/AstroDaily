# AstroDiário

Diário de observações astronômicas: aplicativo Android (Kotlin) + API REST (FastAPI) com banco SQLite.

> README provisório. Será completado com prints do app e instruções finais.

## Estrutura
- `backend/`: API REST em FastAPI (Swagger em `/docs`)
- `android/`: aplicativo Android em Kotlin

## Como rodar o backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Swagger: http://localhost:8000/docs
