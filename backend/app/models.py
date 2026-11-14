from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    nivel = Column(String(30), nullable=False, default="OLHO_NU")

    equipamentos = relationship(
        "Equipamento", back_populates="usuario", cascade="all, delete-orphan"
    )
    observacoes = relationship(
        "Observacao", back_populates="usuario", cascade="all, delete-orphan"
    )


class Equipamento(Base):
    __tablename__ = "equipamentos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(String(50), nullable=False)
    modelo = Column(String(100), nullable=True)

    usuario = relationship("Usuario", back_populates="equipamentos")


class Observacao(Base):
    __tablename__ = "observacoes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    titulo = Column(String(120), nullable=False)
    descricao = Column(Text, nullable=True)
    tipo_objeto = Column(String(30), nullable=False)
    local = Column(String(120), nullable=False)
    nuvens = Column(String(20), nullable=False)
    poluicao_luminosa = Column(Integer, nullable=False)
    lua_visivel = Column(Boolean, nullable=False, default=False)
    nota_visibilidade = Column(Integer, nullable=False)
    classificacao = Column(String(20), nullable=False)
    foto_url = Column(String(255), nullable=True)
    publica = Column(Boolean, nullable=False, default=False)
    data = Column(DateTime, nullable=False, default=datetime.now)

    usuario = relationship("Usuario", back_populates="observacoes")

    @property
    def usuario_nome(self):
        return self.usuario.nome if self.usuario else None
