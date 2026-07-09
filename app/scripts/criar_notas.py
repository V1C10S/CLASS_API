import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

ALUNOS_PATH = DATA_DIR / "alunos.json"
MATERIAS_PATH = DATA_DIR / "materias.json"
NOTAS_DIR = DATA_DIR / "notas"


MEDIA_APROVACAO = 6.0

STATUS_PENDENTE = "pendente"
STATUS_APROVADO = "aprovado"
STATUS_REPROVADO = "reprovado"


def carregar_json(caminho: Path):
    if not caminho.exists():
        return []

    with open(caminho, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()

        if not conteudo:
            return []

        return json.loads(conteudo)


def salvar_json(caminho: Path, dados):
    caminho.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def normalizar_texto(texto: str):
    return str(texto).strip().lower()


def normalizar_codigo(codigo: str):
    return str(codigo).strip().upper()


def normalizar_ra(ra: str):
    return str(ra).strip()


def materia_esta_ativa(materia: dict):
    return normalizar_texto(materia.get("status", "ativa")) == "ativa"


def gerar_caminho_notas(curso: str, turma_id: str):
    curso_normalizado = normalizar_codigo(curso)
    turma_normalizada = normalizar_codigo(turma_id)

    return NOTAS_DIR / curso_normalizado / f"{turma_normalizada}.json"


def gerar_nota_id(ra: str, codigo_materia: str):
    return f"{normalizar_ra(ra)}_{normalizar_codigo(codigo_materia)}"


def calcular_media(nota_1, nota_2):
    if nota_1 is None or nota_2 is None:
        return None

    return round((nota_1 + nota_2) / 2, 2)


def calcular_status(media):
    if media is None:
        return STATUS_PENDENTE

    if media >= MEDIA_APROVACAO:
        return STATUS_APROVADO

    return STATUS_REPROVADO


def extrair_numero_aluno(ra: str):
    return int(normalizar_ra(ra)[-3:])


def extrair_numero_materia(codigo_materia: str):
    partes = normalizar_codigo(codigo_materia).split("_")

    if len(partes) != 3:
        return 1

    numero = partes[2].replace("M", "")

    if not numero.isdigit():
        return 1

    return int(numero)


def gerar_nota_fake(aluno: dict, materia: dict):
    numero_aluno = extrair_numero_aluno(aluno["ra"])
    semestre = int(materia["semestre"])
    numero_materia = extrair_numero_materia(materia["codigo"])

    base = (numero_aluno + semestre + numero_materia) % 10

    nota_1 = round(5.0 + (base * 0.45), 2)
    nota_2 = round(4.5 + (base * 0.5), 2)

    if nota_1 > 10:
        nota_1 = 10.0

    if nota_2 > 10:
        nota_2 = 10.0

    return nota_1, nota_2


def criar_mapa_materias_por_curso(materias):
    mapa = {}

    for materia in materias:
        if not materia_esta_ativa(materia):
            continue

        curso = normalizar_codigo(materia["curso"])

        if curso not in mapa:
            mapa[curso] = []

        mapa[curso].append(materia)

    for curso in mapa:
        mapa[curso] = sorted(
            mapa[curso],
            key=lambda materia: (
                int(materia["semestre"]),
                normalizar_codigo(materia["codigo"])
            )
        )

    return mapa


def criar_mapa_alunos_por_turma(alunos):
    mapa = {}

    for aluno in alunos:
        curso = normalizar_codigo(aluno["curso"])
        turma_id = normalizar_codigo(aluno["turma_id"])

        chave = (curso, turma_id)

        if chave not in mapa:
            mapa[chave] = []

        mapa[chave].append(aluno)

    for chave in mapa:
        mapa[chave] = sorted(
            mapa[chave],
            key=lambda aluno: normalizar_ra(aluno["ra"])
        )

    return mapa


def nota_ja_existe(notas_existentes, nota_id: str):
    nota_id_normalizado = normalizar_codigo(nota_id)

    for nota in notas_existentes:
        if normalizar_codigo(nota["nota_id"]) == nota_id_normalizado:
            return True

    return False


def gerar_nota(aluno: dict, materia: dict):
    nota_1, nota_2 = gerar_nota_fake(aluno, materia)
    media = calcular_media(nota_1, nota_2)
    status = calcular_status(media)

    return {
        "nota_id": gerar_nota_id(aluno["ra"], materia["codigo"]),
        "ra": normalizar_ra(aluno["ra"]),
        "codigo_materia": normalizar_codigo(materia["codigo"]),
        "curso": normalizar_codigo(aluno["curso"]),
        "turma_id": normalizar_codigo(aluno["turma_id"]),
        "semestre": int(materia["semestre"]),
        "nota_1": nota_1,
        "nota_2": nota_2,
        "media": media,
        "status": status
    }


def adicionar_notas_sem_apagar():
    NOTAS_DIR.mkdir(parents=True, exist_ok=True)

    alunos = carregar_json(ALUNOS_PATH)
    materias = carregar_json(MATERIAS_PATH)

    if not alunos:
        print("Nenhum aluno encontrado em alunos.json.")
        print("Rode primeiro: python app/scripts/criar_alunos.py")
        return

    if not materias:
        print("Nenhuma matéria encontrada em materias.json.")
        print("Rode primeiro: python app/scripts/criar_materias.py")
        return

    materias_por_curso = criar_mapa_materias_por_curso(materias)
    alunos_por_turma = criar_mapa_alunos_por_turma(alunos)

    arquivos_processados = 0
    notas_adicionadas_total = 0
    notas_ignoradas_total = 0
    notas_geradas_total = 0

    for chave, alunos_da_turma in alunos_por_turma.items():
        curso, turma_id = chave
        materias_do_curso = materias_por_curso.get(curso, [])

        if not materias_do_curso:
            continue

        caminho_notas = gerar_caminho_notas(curso, turma_id)
        notas_existentes = carregar_json(caminho_notas)

        notas_adicionadas = 0
        notas_ignoradas = 0

        for aluno in alunos_da_turma:
            for materia in materias_do_curso:
                nova_nota = gerar_nota(aluno, materia)
                notas_geradas_total += 1

                if nota_ja_existe(notas_existentes, nova_nota["nota_id"]):
                    notas_ignoradas += 1
                    continue

                notas_existentes.append(nova_nota)
                notas_adicionadas += 1

        notas_existentes = sorted(
            notas_existentes,
            key=lambda nota: (
                normalizar_ra(nota["ra"]),
                int(nota["semestre"]),
                normalizar_codigo(nota["codigo_materia"])
            )
        )

        salvar_json(caminho_notas, notas_existentes)

        arquivos_processados += 1
        notas_adicionadas_total += notas_adicionadas
        notas_ignoradas_total += notas_ignoradas

    print(f"Pasta de notas atualizada em: {NOTAS_DIR}")
    print(f"Alunos usados como base: {len(alunos)}")
    print(f"Matérias usadas como base: {len(materias)}")
    print(f"Arquivos de turma processados: {arquivos_processados}")
    print(f"Notas geradas no ciclo: {notas_geradas_total}")
    print(f"Notas adicionadas: {notas_adicionadas_total}")
    print(f"Notas ignoradas por já existirem: {notas_ignoradas_total}")


if __name__ == "__main__":
    adicionar_notas_sem_apagar()