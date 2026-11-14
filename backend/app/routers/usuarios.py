from collections import Counter

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..services import calcular_patente, calcular_xp

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


def buscar_usuario(usuario_id: int, db: Session) -> models.Usuario:
    usuario = db.get(models.Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.post("", response_model=schemas.UsuarioOut, status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(models.Usuario).filter(models.Usuario.email == dados.email).first():
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    usuario = models.Usuario(**dados.model_dump())
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


# Esta rota precisa vir ANTES de "/{usuario_id}", senão "login" seria lido como id.
@router.get("/login", response_model=schemas.UsuarioOut)
def login_por_email(email: str, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="E-mail não cadastrado")
    return usuario


@router.get("/{usuario_id}", response_model=schemas.UsuarioOut)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return buscar_usuario(usuario_id, db)


@router.put("/{usuario_id}", response_model=schemas.UsuarioOut)
def atualizar_usuario(usuario_id: int, dados: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = buscar_usuario(usuario_id, db)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = buscar_usuario(usuario_id, db)
    db.delete(usuario)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{usuario_id}/estatisticas", response_model=schemas.Estatisticas)
def estatisticas(usuario_id: int, db: Session = Depends(get_db)):
    usuario = buscar_usuario(usuario_id, db)
    observacoes = usuario.observacoes
    total = len(observacoes)
    media = round(sum(o.nota_visibilidade for o in observacoes) / total, 1) if total else 0.0
    mais_observado = (
        Counter(o.tipo_objeto for o in observacoes).most_common(1)[0][0] if total else None
    )
    fotos = sum(1 for o in observacoes if o.foto_url)
    equipamentos = len(usuario.equipamentos)
    xp = calcular_xp(total, fotos, equipamentos)
    return schemas.Estatisticas(
        total_observacoes=total,
        media_nota=media,
        objeto_mais_observado=mais_observado,
        total_fotos=fotos,
        total_equipamentos=equipamentos,
        xp=xp,
        patente=calcular_patente(xp),
    )
