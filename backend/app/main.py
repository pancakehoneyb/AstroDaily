import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import models  # noqa: F401  (garante o registro das tabelas)
from .database import Base, engine
from .routers import equipamentos, observacoes, usuarios

Base.metadata.create_all(bind=engine)
os.makedirs("uploads", exist_ok=True)

app = FastAPI(
    title="AstroDiário API",
    description=(
        "API REST do AstroDiário, um diário de observações astronômicas. "
        "Permite cadastrar usuários e equipamentos, registrar observações do céu "
        "(com nota de visibilidade calculada), anexar fotos e consultar o feed da comunidade."
    ),
    version="1.0.0",
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(usuarios.router)
app.include_router(equipamentos.router)
app.include_router(observacoes.router)


@app.get("/", tags=["Status"])
def raiz():
    return {"app": "AstroDiário API", "docs": "/docs"}
