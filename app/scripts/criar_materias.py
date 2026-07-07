import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CURSOS_PATH = DATA_DIR / "cursos.json"
MATERIAS_PATH = DATA_DIR / "materias.json"


MATERIAS_POR_SEMESTRE = 2
CARGA_HORARIA_PADRAO = 80


NOMES_POR_SEMESTRE = {
    1: [
        "fundamentos",
        "introducao profissional"
    ],
    2: [
        "metodos aplicados",
        "pratica aplicada"
    ],
    3: [
        "processos profissionais",
        "laboratorio aplicado"
    ],
    4: [
        "analise profissional",
        "projeto aplicado"
    ],
    5: [
        "gestao aplicada",
        "projeto integrador"
    ],
    6: [
        "tecnicas avancadas",
        "solucoes profissionais"
    ],
    7: [
        "topicos avancados",
        "pesquisa aplicada"
    ],
    8: [
        "planejamento profissional",
        "projeto profissional"
    ],
    9: [
        "pratica supervisionada",
        "estudos avancados"
    ],
    10: [
        "estagio supervisionado",
        "projeto final"
    ],
    11: [
        "pratica especializada",
        "aprofundamento profissional"
    ],
    12: [
        "estagio final",
        "conclusao profissional"
    ]
}


def carregar_json(caminho: Path):
    if not caminho.exists():
        return []

    with open(caminho, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()

        if not conteudo:
            return []

        return json.loads(conteudo)


def salvar_json(caminho: Path, dados):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def normalizar_texto(texto: str):
    return str(texto).strip().lower()


def normalizar_sigla(sigla: str):
    return str(sigla).strip().upper()


def normalizar_status(status: str):
    return str(status).strip().lower()


def gerar_codigo_materia(curso_sigla: str, semestre: int, numero_materia: int):
    sigla = normalizar_sigla(curso_sigla)
    semestre_codigo = str(semestre).zfill(2)
    materia_codigo = str(numero_materia).zfill(2)

    return f"{sigla}_S{semestre_codigo}_M{materia_codigo}"


def pegar_nomes_do_semestre(semestre: int):
    if semestre in NOMES_POR_SEMESTRE:
        return NOMES_POR_SEMESTRE[semestre]

    return [
        f"materia aplicada {semestre}.1",
        f"materia aplicada {semestre}.2"
    ]


def gerar_nome_materia(nome_base: str, nome_curso: str):
    return f"{normalizar_texto(nome_base)} de {normalizar_texto(nome_curso)}"


def converter_cursos_para_materias():
    cursos = carregar_json(CURSOS_PATH)
    materias_formatadas = []

    for curso in cursos:
        curso_sigla = normalizar_sigla(curso["sigla"])
        nome_curso = normalizar_texto(curso["nome_curso"])
        duracao_semestres = int(curso["duracao_semestres"])

        for semestre in range(1, duracao_semestres + 1):
            nomes_do_semestre = pegar_nomes_do_semestre(semestre)

            for numero_materia, nome_base in enumerate(nomes_do_semestre, start=1):
                materia = {
                    "codigo": gerar_codigo_materia(curso_sigla, semestre, numero_materia),
                    "nome": gerar_nome_materia(nome_base, nome_curso),
                    "curso": curso_sigla,
                    "semestre": semestre,
                    "carga_horaria": CARGA_HORARIA_PADRAO,
                    "status": "ativa"
                }

                materias_formatadas.append(materia)

    return materias_formatadas


def criar_materias():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    cursos = carregar_json(CURSOS_PATH)

    if not cursos:
        print("Nenhum curso encontrado em cursos.json.")
        print("Rode primeiro: python app/scripts/criar_cursos.py")
        return

    materias = converter_cursos_para_materias()

    salvar_json(MATERIAS_PATH, materias)

    print(f"Arquivo criado com sucesso em: {MATERIAS_PATH}")
    print(f"Cursos usados como base: {len(cursos)}")
    print(f"Matérias por semestre: {MATERIAS_POR_SEMESTRE}")
    print(f"Total de matérias geradas: {len(materias)}")


if __name__ == "__main__":
    criar_materias()