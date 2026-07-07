import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "cursos.json"


def garantir_arquivo_cursos():
    DATA_DIR.mkdir(exist_ok=True)

    if not DATA_PATH.exists():
        with open(DATA_PATH, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo, ensure_ascii=False, indent=4)


def carregar_cursos():
    garantir_arquivo_cursos()

    with open(DATA_PATH, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()

        if not conteudo:
            return []

        return json.loads(conteudo)


def normalizar_nome(nome_curso: str):
    return nome_curso.strip().lower()


def normalizar_sigla(sigla: str):
    return sigla.strip().upper()


def normalizar_area(area: str):
    return area.strip().lower()


def listar_cursos():
    return carregar_cursos()


def listar_areas():
    cursos = carregar_cursos()

    areas = sorted(set(curso["area"] for curso in cursos))

    return areas


def listar_cursos_por_area(area: str):
    cursos = carregar_cursos()
    area_normalizada = normalizar_area(area)

    cursos_filtrados = []

    for curso in cursos:
        if normalizar_area(curso["area"]) == area_normalizada:
            cursos_filtrados.append(curso)

    return cursos_filtrados


def buscar_curso_por_nome(nome_curso: str):
    cursos = carregar_cursos()
    nome_normalizado = normalizar_nome(nome_curso)

    for curso in cursos:
        if normalizar_nome(curso["nome_curso"]) == nome_normalizado:
            return curso

    return None


def buscar_curso_por_sigla(sigla: str):
    cursos = carregar_cursos()
    sigla_normalizada = normalizar_sigla(sigla)

    for curso in cursos:
        if normalizar_sigla(curso["sigla"]) == sigla_normalizada:
            return curso

    return None

def buscar_cursos_por_termo(termo: str):
    cursos = carregar_cursos()
    termo_normalizado = normalizar_nome(termo)

    resultados = []

    for curso in cursos:
        nome_curso = normalizar_nome(curso["nome_curso"])
        sigla = normalizar_sigla(curso["sigla"])
        area = normalizar_nome(curso["area"])

        if (
            termo_normalizado in nome_curso
            or termo_normalizado in sigla.lower()
            or termo_normalizado in area
        ):
            resultados.append(curso)

    return resultados