import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CURSOS_PATH = DATA_DIR / "cursos.json"
TURMAS_PATH = DATA_DIR / "turmas.json"


ANO_TURMAS = 2026
TURMAS_POR_SEMESTRE = 2

ENTRADAS_SEMESTRE = [1, 2]

PERIODOS_PADRAO = [
    "manha",
    "noite"
]


def normalizar_sigla(sigla: str):
    return sigla.strip().upper()


def normalizar_periodo(periodo: str):
    return periodo.strip().lower()


def normalizar_status(status: str):
    return status.strip().lower()


def gerar_turno_codigo(periodo: str):
    periodo_normalizado = normalizar_periodo(periodo)

    turnos = {
        "manha": "MAN",
        "tarde": "TAR",
        "noite": "NOT"
    }

    return turnos.get(periodo_normalizado, "NDF")


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


def carregar_cursos():
    return carregar_json(CURSOS_PATH)


def carregar_turmas_existentes():
    return carregar_json(TURMAS_PATH)


def gerar_numero_turma(numero: int):
    return str(numero).zfill(3)


def gerar_turma_id(curso_sigla: str, ano: int, entrada_semestre: int, numero_turma: str):
    sigla = normalizar_sigla(curso_sigla)

    return f"{sigla}_{ano}_S{entrada_semestre}_{numero_turma}"


def escolher_periodo(numero_turma: int):
    indice = (numero_turma - 1) % len(PERIODOS_PADRAO)

    return PERIODOS_PADRAO[indice]


def converter_cursos_para_turmas():
    cursos = carregar_cursos()
    turmas_formatadas = []

    for curso in cursos:
        curso_sigla = normalizar_sigla(curso["sigla"])

        for entrada_semestre in ENTRADAS_SEMESTRE:
            for numero in range(1, TURMAS_POR_SEMESTRE + 1):
                numero_turma = gerar_numero_turma(numero)
                periodo = escolher_periodo(numero)
                status = "ativa"

                turmas_formatadas.append({
                    "turma_id": gerar_turma_id(
                        curso_sigla,
                        ANO_TURMAS,
                        entrada_semestre,
                        numero_turma
                    ),
                    "curso_sigla": curso_sigla,
                    "ano": ANO_TURMAS,
                    "entrada_semestre": entrada_semestre,
                    "numero_turma": numero_turma,
                    "periodo": periodo,
                    "turno_codigo": gerar_turno_codigo(periodo),
                    "status": normalizar_status(status)
                })

    return turmas_formatadas


def turma_ja_existe(turmas_existentes, nova_turma):
    for turma in turmas_existentes:
        if turma["turma_id"] == nova_turma["turma_id"]:
            return True

    return False


def adicionar_turmas_sem_apagar():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    cursos = carregar_cursos()

    if not cursos:
        print("Nenhum curso encontrado em cursos.json.")
        print("Rode primeiro: python app/scripts/criar_cursos.py")
        return

    turmas_existentes = carregar_turmas_existentes()
    novas_turmas = converter_cursos_para_turmas()

    turmas_adicionadas = 0
    turmas_ignoradas = 0

    for nova_turma in novas_turmas:
        if turma_ja_existe(turmas_existentes, nova_turma):
            turmas_ignoradas += 1
            continue

        turmas_existentes.append(nova_turma)
        turmas_adicionadas += 1

    salvar_json(TURMAS_PATH, turmas_existentes)

    total_cursos = len(cursos)
    total_turmas_esperadas_por_ano = total_cursos * len(ENTRADAS_SEMESTRE) * TURMAS_POR_SEMESTRE

    print(f"Arquivo atualizado com segurança em: {TURMAS_PATH}")
    print(f"Cursos usados como base: {total_cursos}")
    print(f"Turmas esperadas para {ANO_TURMAS}: {total_turmas_esperadas_por_ano}")
    print(f"Turmas adicionadas: {turmas_adicionadas}")
    print(f"Turmas ignoradas por já existirem: {turmas_ignoradas}")
    print(f"Total de turmas no arquivo: {len(turmas_existentes)}")


if __name__ == "__main__":
    adicionar_turmas_sem_apagar()