import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

TURMAS_PATH = DATA_DIR / "turmas.json"
ALUNOS_PATH = DATA_DIR / "alunos.json"


ALUNOS_POR_TURMA = 40


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
    return texto.strip().lower()


def normalizar_sigla(sigla: str):
    return sigla.strip().upper()


def gerar_numero(numero: int):
    return str(numero).zfill(3)


def converter_letra_para_numero(letra: str):
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    letra_normalizada = letra.strip().upper()

    if letra_normalizada not in alfabeto:
        return "00"

    numero = alfabeto.index(letra_normalizada) + 1

    return str(numero).zfill(2)


def converter_sigla_para_codigo(sigla: str):
    sigla_normalizada = sigla.strip().upper()
    codigo = ""

    for letra in sigla_normalizada:
        codigo += converter_letra_para_numero(letra)

    return codigo


def converter_entrada_para_codigo(entrada_semestre: int):
    return str(entrada_semestre).zfill(2)


def converter_turno_para_codigo(turno: str):
    turno_normalizado = turno.strip().upper()

    turnos = {
        "MAN": "01",
        "TAR": "02",
        "NOT": "03"
    }

    return turnos.get(turno_normalizado, "00")


def gerar_ra(turma: dict, numero_aluno: str):
    ano = str(turma["ano"])
    curso_codigo = converter_sigla_para_codigo(turma["curso_sigla"])
    entrada_codigo = converter_entrada_para_codigo(turma["entrada_semestre"])
    turno_codigo = converter_turno_para_codigo(turma["turno_codigo"])
    numero_turma = turma["numero_turma"]

    return f"{ano}{curso_codigo}{entrada_codigo}{turno_codigo}{numero_turma}{numero_aluno}"


def gerar_nome(turma: dict, numero_aluno: str):
    curso = normalizar_sigla(turma["curso_sigla"])
    ano = turma["ano"]

    return f"Aluno {curso} {ano} {numero_aluno}"


def gerar_email(turma: dict, numero_aluno: str):
    curso = normalizar_sigla(turma["curso_sigla"]).lower()
    ano = turma["ano"]
    entrada_semestre = turma["entrada_semestre"]
    numero_turma = turma["numero_turma"]

    return f"{curso}_{ano}_s{entrada_semestre}_t{numero_turma}_a{numero_aluno}@email.com"


def aluno_ja_existe(alunos_existentes, novo_aluno):
    for aluno in alunos_existentes:
        if aluno["ra"] == novo_aluno["ra"]:
            return True

    return False


def converter_turmas_para_alunos():
    turmas = carregar_json(TURMAS_PATH)
    alunos_formatados = []

    for turma in turmas:
        for numero in range(1, ALUNOS_POR_TURMA + 1):
            numero_aluno = gerar_numero(numero)

            aluno = {
                "nome": gerar_nome(turma, numero_aluno),
                "ra": gerar_ra(turma, numero_aluno),
                "turma_id": turma["turma_id"],
                "email": gerar_email(turma, numero_aluno),
                "curso": normalizar_sigla(turma["curso_sigla"]),
                "ano": turma["ano"],
                "periodo": normalizar_texto(turma["periodo"]),
                "turno": normalizar_sigla(turma["turno_codigo"]),
                "status": "ativo"
            }

            alunos_formatados.append(aluno)

    return alunos_formatados


def adicionar_alunos_sem_apagar():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    turmas = carregar_json(TURMAS_PATH)

    if not turmas:
        print("Nenhuma turma encontrada em turmas.json.")
        print("Rode primeiro: python app/scripts/criar_turmas.py")
        return

    alunos_existentes = carregar_json(ALUNOS_PATH)
    novos_alunos = converter_turmas_para_alunos()

    alunos_adicionados = 0
    alunos_ignorados = 0

    for novo_aluno in novos_alunos:
        if aluno_ja_existe(alunos_existentes, novo_aluno):
            alunos_ignorados += 1
            continue

        alunos_existentes.append(novo_aluno)
        alunos_adicionados += 1

    salvar_json(ALUNOS_PATH, alunos_existentes)

    print(f"Arquivo atualizado com segurança em: {ALUNOS_PATH}")
    print(f"Turmas usadas como base: {len(turmas)}")
    print(f"Alunos por turma: {ALUNOS_POR_TURMA}")
    print(f"Alunos esperados no total: {len(turmas) * ALUNOS_POR_TURMA}")
    print(f"Alunos adicionados: {alunos_adicionados}")
    print(f"Alunos ignorados por já existirem: {alunos_ignorados}")
    print(f"Total de alunos no arquivo: {len(alunos_existentes)}")


if __name__ == "__main__":
    adicionar_alunos_sem_apagar()