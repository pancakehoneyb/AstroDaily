import os
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..services import calcular_nota, classificar

router = APIRouter(prefix="/observacoes", tags=["Observações"])

UPLOAD_DIR = "uploads"


def buscar_observacao(observacao_id: int, db: Session) -> models.Observacao:
    obs = db.get(models.Observacao, observacao_id)
    if not obs:
        raise HTTPException(status_code=404, detail="Observação não encontrada")
    return obs


def aplicar_nota(obs: models.Observacao) -> None:
    obs.nota_visibilidade = calcular_nota(
        obs.nuvens, obs.poluicao_luminosa, obs.lua_visivel, obs.tipo_objeto
    )
    obs.classificacao = classificar(obs.nota_visibilidade)


@router.post("", response_model=schemas.ObservacaoOut, status_code=status.HTTP_201_CREATED)
def criar_observacao(dados: schemas.ObservacaoCreate, db: Session = Depends(get_db)):
    if not db.get(models.Usuario, dados.usuario_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    obs = models.Observacao(**dados.model_dump())
    aplicar_nota(obs)
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs


@router.get("", response_model=List[schemas.ObservacaoOut])
def listar_observacoes(usuario_id: Optional[int] = None, db: Session = Depends(get_db)):
    consulta = db.query(models.Observacao)
    if usuario_id is not None:
        consulta = consulta.filter(models.Observacao.usuario_id == usuario_id)
    return consulta.order_by(models.Observacao.data.desc()).all()


# Precisa vir ANTES de "/{observacao_id}".
@router.get("/publicas", response_model=List[schemas.ObservacaoOut])
def feed_comunidade(db: Session = Depends(get_db)):
    return (
        db.query(models.Observacao)
        .filter(models.Observacao.publica.is_(True))
        .order_by(models.Observacao.data.desc())
        .all()
    )


@router.get("/{observacao_id}", response_model=schemas.ObservacaoOut)
def obter_observacao(observacao_id: int, db: Session = Depends(get_db)):
    return buscar_observacao(observacao_id, db)


@router.put("/{observacao_id}", response_model=schemas.ObservacaoOut)
def atualizar_observacao(
    observacao_id: int, dados: schemas.ObservacaoUpdate, db: Session = Depends(get_db)
):
    obs = buscar_observacao(observacao_id, db)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(obs, campo, valor)
    aplicar_nota(obs)  # recalcula, pois nuvens/poluição/lua podem ter mudado
    db.commit()
    db.refresh(obs)
    return obs


@router.delete("/{observacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_observacao(observacao_id: int, db: Session = Depends(get_db)):
    obs = buscar_observacao(observacao_id, db)
    if obs.foto_url:
        caminho = os.path.join(UPLOAD_DIR, os.path.basename(obs.foto_url))
        if os.path.exists(caminho):
            os.remove(caminho)
    db.delete(obs)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{observacao_id}/foto", response_model=schemas.ObservacaoOut)
def enviar_foto(observacao_id: int, arquivo: UploadFile = File(...), db: Session = Depends(get_db)):
    obs = buscar_observacao(observacao_id, db)
    if not (arquivo.content_type or "").startswith("image/"):
        raise HTTPException(status_code=400, detail="O arquivo precisa ser uma imagem")

    extensao = os.path.splitext(arquivo.filename or "")[1].lower() or ".jpg"
    nome_arquivo = f"{uuid.uuid4().hex}{extensao}"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(os.path.join(UPLOAD_DIR, nome_arquivo), "wb") as destino:
        destino.write(arquivo.file.read())

    obs.foto_url = f"/uploads/{nome_arquivo}"
    db.commit()
    db.refresh(obs)
    return obs
