from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Equipamentos"])


@router.post(
    "/usuarios/{usuario_id}/equipamentos",
    response_model=schemas.EquipamentoOut,
    status_code=status.HTTP_201_CREATED,
)
def adicionar_equipamento(
    usuario_id: int, dados: schemas.EquipamentoCreate, db: Session = Depends(get_db)
):
    if not db.get(models.Usuario, usuario_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    equipamento = models.Equipamento(usuario_id=usuario_id, **dados.model_dump())
    db.add(equipamento)
    db.commit()
    db.refresh(equipamento)
    return equipamento


@router.get("/usuarios/{usuario_id}/equipamentos", response_model=List[schemas.EquipamentoOut])
def listar_equipamentos(usuario_id: int, db: Session = Depends(get_db)):
    if not db.get(models.Usuario, usuario_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db.query(models.Equipamento).filter(models.Equipamento.usuario_id == usuario_id).all()


@router.delete("/equipamentos/{equipamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_equipamento(equipamento_id: int, db: Session = Depends(get_db)):
    equipamento = db.get(models.Equipamento, equipamento_id)
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    db.delete(equipamento)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
