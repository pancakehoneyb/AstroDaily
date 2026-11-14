from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

Nivel = Literal["OLHO_NU", "INSTRUMENTOS", "ASTRO_INICIANTE", "ASTRO_AVANCADO"]
Nuvens = Literal["LIMPO", "PARCIAL", "NUBLADO"]
TipoObjeto = Literal["LUA", "PLANETA", "ESTRELA", "CONSTELACAO", "GALAXIA", "OUTRO"]


# ---------- Usuário ----------
class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    nivel: Nivel = "OLHO_NU"


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=2, max_length=100)
    nivel: Optional[Nivel] = None


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    nivel: str


class Estatisticas(BaseModel):
    total_observacoes: int
    media_nota: float
    objeto_mais_observado: Optional[str]
    total_fotos: int
    total_equipamentos: int
    xp: int
    patente: str


# ---------- Equipamento ----------
class EquipamentoCreate(BaseModel):
    tipo: str = Field(min_length=2, max_length=50)
    modelo: Optional[str] = Field(default=None, max_length=100)


class EquipamentoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    tipo: str
    modelo: Optional[str]


# ---------- Observação ----------
class ObservacaoCreate(BaseModel):
    usuario_id: int
    titulo: str = Field(min_length=2, max_length=120)
    descricao: Optional[str] = None
    tipo_objeto: TipoObjeto
    local: str = Field(min_length=2, max_length=120)
    nuvens: Nuvens
    poluicao_luminosa: int = Field(ge=0, le=10)
    lua_visivel: bool = False
    publica: bool = False


class ObservacaoUpdate(BaseModel):
    titulo: Optional[str] = Field(default=None, min_length=2, max_length=120)
    descricao: Optional[str] = None
    tipo_objeto: Optional[TipoObjeto] = None
    local: Optional[str] = Field(default=None, min_length=2, max_length=120)
    nuvens: Optional[Nuvens] = None
    poluicao_luminosa: Optional[int] = Field(default=None, ge=0, le=10)
    lua_visivel: Optional[bool] = None
    publica: Optional[bool] = None


class ObservacaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    usuario_nome: Optional[str] = None
    titulo: str
    descricao: Optional[str]
    tipo_objeto: str
    local: str
    nuvens: str
    poluicao_luminosa: int
    lua_visivel: bool
    nota_visibilidade: int
    classificacao: str
    foto_url: Optional[str]
    publica: bool
    data: datetime
