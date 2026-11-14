"""Regras de negócio do AstroDiário (processamento dos dados)."""

PENALIDADE_NUVENS = {"LIMPO": 0, "PARCIAL": 30, "NUBLADO": 60}


def calcular_nota(nuvens: str, poluicao_luminosa: int, lua_visivel: bool, tipo_objeto: str) -> int:
    """Nota de visibilidade de 0 a 100.

    Parte de 100 e desconta:
    - nuvens: 0 / 30 / 60 pontos
    - poluição luminosa (0 a 10): 4 pontos por nível
    - lua visível: 10 pontos (atrapalha objetos fracos; não pesa se o alvo é a própria Lua)
    """
    nota = 100
    nota -= PENALIDADE_NUVENS[nuvens]
    nota -= poluicao_luminosa * 4
    if lua_visivel and tipo_objeto != "LUA":
        nota -= 10
    return max(0, min(100, nota))


def classificar(nota: int) -> str:
    if nota >= 80:
        return "Excelente"
    if nota >= 60:
        return "Boa"
    if nota >= 40:
        return "Regular"
    return "Ruim"


def calcular_xp(total_observacoes: int, total_fotos: int, total_equipamentos: int) -> int:
    """Sistema de XP: observar vale mais, foto e equipamento dão bônus."""
    return total_observacoes * 10 + total_fotos * 5 + total_equipamentos * 5


def calcular_patente(xp: int) -> str:
    if xp >= 200:
        return "Mestre do Céu"
    if xp >= 100:
        return "Astrônomo Experiente"
    if xp >= 40:
        return "Explorador"
    return "Iniciante"
