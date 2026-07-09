import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

TURMAS_PATH = DATA_DIR / "turmas.json"
MATERIAS_PATH = DATA_DIR / "materias.json"
HORARIOS_PATH = DATA_DIR / "horarios.json"


DIAS_POR_MATERIA = {
    "01": "segunda",
    "02": "quarta"
}


HORARIOS_POR_PERIODO = {
    "manha": {
        "inicio": "08:00",
        "fim": "10:00"
    },
    "tarde": {
        "inicio": "14:00",
        "fim": "16:00"
    },
    "noite": {
        "inicio": "19:00",
        "fim": "21:00"
    }
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


def normalizar_codigo(codigo: str):
    return str(codigo).strip().upper()


def materia_esta_ativa(materia: dict):
    return normalizar_texto(materia.get("status", "ativa")) == "ativa"


def extrair_numero_materia(codigo_materia: str):
    codigo = normalizar_codigo(codigo_materia)
    partes = codigo.split("_")

    if len(partes) != 3:
        return "01"

    numero = partes[2].replace("M", "")

    if not numero.isdigit():
        return "01"

    return numero.zfill(2)


def gerar_horario_id(turma_id: str, codigo_materia: str):
    return f"{normalizar_codigo(turma_id)}_{normalizar_codigo(codigo_materia)}"


def escolher_dia_semana(codigo_materia: str):
    numero_materia = extrair_numero_materia(codigo_materia)

    return DIAS_POR_MATERIA.get(numero_materia, "sexta")


def escolher_horario(periodo: str):
    periodo_normalizado = normalizar_texto(periodo)

    return HORARIOS_POR_PERIODO.get(
        periodo_normalizado,
        {
            "inicio": "00:00",
            "fim": "00:00"
        }
    )


def gerar_sala(turma: dict, materia: dict):
    curso = normalizar_sigla(turma["curso_sigla"])
    semestre = str(materia["semestre"]).zfill(2)
    numero_turma = turma["numero_turma"]

    return f"SALA-{curso}-S{semestre}-T{numero_turma}"


def gerar_professor(materia: dict):
    curso = normalizar_sigla(materia["curso"])
    semestre = str(materia["semestre"]).zfill(2)
    numero_materia = extrair_numero_materia(materia["codigo"])

    return f"Professor {curso} S{semestre} M{numero_materia}"


def converter_turmas_e_materias_para_horarios():
    turmas = carregar_json(TURMAS_PATH)
    materias = carregar_json(MATERIAS_PATH)

    horarios_formatados = []

    for turma in turmas:
        curso_turma = normalizar_sigla(turma["curso_sigla"])
        periodo = normalizar_texto(turma["periodo"])
        horario_base = escolher_horario(periodo)

        for materia in materias:
            curso_materia = normalizar_sigla(materia["curso"])

            if curso_materia != curso_turma:
                continue

            if not materia_esta_ativa(materia):
                continue

            horario = {
                "horario_id": gerar_horario_id(
                    turma["turma_id"],
                    materia["codigo"]
                ),
                "turma_id": turma["turma_id"],
                "codigo_materia": materia["codigo"],
                "curso": curso_turma,
                "semestre": materia["semestre"],
                "dia_semana": escolher_dia_semana(materia["codigo"]),
                "inicio": horario_base["inicio"],
                "fim": horario_base["fim"],
                "sala": gerar_sala(turma, materia),
                "professor": gerar_professor(materia),
                "status": "ativo"
            }

            horarios_formatados.append(horario)

    return horarios_formatados


def criar_horarios():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    turmas = carregar_json(TURMAS_PATH)
    materias = carregar_json(MATERIAS_PATH)

    if not turmas:
        print("Nenhuma turma encontrada em turmas.json.")
        print("Rode primeiro: python app/scripts/criar_turmas.py")
        return

    if not materias:
        print("Nenhuma matéria encontrada em materias.json.")
        print("Rode primeiro: python app/scripts/criar_materias.py")
        return

    horarios = converter_turmas_e_materias_para_horarios()

    salvar_json(HORARIOS_PATH, horarios)

    print(f"Arquivo criado com sucesso em: {HORARIOS_PATH}")
    print(f"Turmas usadas como base: {len(turmas)}")
    print(f"Matérias usadas como base: {len(materias)}")
    print(f"Total de horários gerados: {len(horarios)}")


if __name__ == "__main__":
    criar_horarios()