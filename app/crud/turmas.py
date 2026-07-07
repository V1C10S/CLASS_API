import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "turmas.json"


def garantir_arquivo_turmas():
    DATA_DIR.mkdir(exist_ok=True)

    if not DATA_PATH.exists():
        with open(DATA_PATH, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo, ensure_ascii=False, indent=4)


def carregar_turmas():
    garantir_arquivo_turmas()

    with open(DATA_PATH, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()

        if not conteudo:
            return []

        return json.loads(conteudo)


def normalizar_texto(texto: str):
    return texto.strip().lower()


def normalizar_sigla(sigla: str):
    return sigla.strip().upper()


def normalizar_turma_id(turma_id: str):
    return turma_id.strip().upper()


def listar_turmas():
    return carregar_turmas()


def buscar_turma_por_id(turma_id: str):
    turmas = carregar_turmas()
    turma_id_normalizado = normalizar_turma_id(turma_id)

    for turma in turmas:
        if normalizar_turma_id(turma["turma_id"]) == turma_id_normalizado:
            return turma

    return None


def listar_turmas_por_curso(curso_sigla: str):
    turmas = carregar_turmas()
    sigla_normalizada = normalizar_sigla(curso_sigla)

    resultado = []

    for turma in turmas:
        if normalizar_sigla(turma["curso_sigla"]) == sigla_normalizada:
            resultado.append(turma)

    return resultado


def listar_turmas_por_ano(ano: int):
    turmas = carregar_turmas()

    resultado = []

    for turma in turmas:
        if turma["ano"] == ano:
            resultado.append(turma)

    return resultado


def listar_turmas_por_entrada(entrada_semestre: int):
    turmas = carregar_turmas()

    resultado = []

    for turma in turmas:
        if turma["entrada_semestre"] == entrada_semestre:
            resultado.append(turma)

    return resultado


def listar_turmas_por_periodo(periodo: str):
    turmas = carregar_turmas()
    periodo_normalizado = normalizar_texto(periodo)

    resultado = []

    for turma in turmas:
        if normalizar_texto(turma["periodo"]) == periodo_normalizado:
            resultado.append(turma)

    return resultado


def listar_turmas_por_status(status: str):
    turmas = carregar_turmas()
    status_normalizado = normalizar_texto(status)

    resultado = []

    for turma in turmas:
        if normalizar_texto(turma["status"]) == status_normalizado:
            resultado.append(turma)

    return resultado


def buscar_turmas_por_termo(termo: str):
    turmas = carregar_turmas()
    termo_normalizado = normalizar_texto(termo)

    resultado = []

    for turma in turmas:
        turma_id = normalizar_texto(turma["turma_id"])
        curso_sigla = normalizar_texto(turma["curso_sigla"])
        ano = str(turma["ano"])
        entrada_semestre = f"s{turma['entrada_semestre']}"
        numero_turma = normalizar_texto(turma["numero_turma"])
        periodo = normalizar_texto(turma["periodo"])
        turno_codigo = normalizar_texto(turma["turno_codigo"])
        status = normalizar_texto(turma["status"])

        if (
            termo_normalizado in turma_id
            or termo_normalizado in curso_sigla
            or termo_normalizado in ano
            or termo_normalizado in entrada_semestre
            or termo_normalizado in numero_turma
            or termo_normalizado in periodo
            or termo_normalizado in turno_codigo
            or termo_normalizado in status
        ):
            resultado.append(turma)

    return resultado