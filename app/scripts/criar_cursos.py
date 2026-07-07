import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "cursos.json"


AREAS_CURSOS = [
    {
        "area": "TI",
        "cursos": [
            {
                "nome_curso": "analise e desenvolvimento de sistemas",
                "sigla": "ADS",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            },
            {
                "nome_curso": "ciencia da computacao",
                "sigla": "CDC",
                "tipo": "bacharelado",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "engenharia da computacao",
                "sigla": "EGC",
                "tipo": "bacharelado",
                "duracao_semestres": 10
            },
            {
                "nome_curso": "sistemas de informacao",
                "sigla": "SDI",
                "tipo": "bacharelado",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "gestao da tecnologia",
                "sigla": "GTC",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            },
            {
                "nome_curso": "ciberseguranca",
                "sigla": "CBS",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            },
            {
                "nome_curso": "big data",
                "sigla": "BGD",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            },
            {
                "nome_curso": "ciencia de dados",
                "sigla": "CDD",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            },
            {
                "nome_curso": "engenharia de dados",
                "sigla": "EGD",
                "tipo": "bacharelado",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "inteligencia artificial",
                "sigla": "ITA",
                "tipo": "bacharelado",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "computacao em nuvem",
                "sigla": "CEN",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            },
            {
                "nome_curso": "desenvolvimento de software",
                "sigla": "DDS",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            },
            {
                "nome_curso": "engenharia de software",
                "sigla": "EGS",
                "tipo": "bacharelado",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "programacao de computadores",
                "sigla": "PDC",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            },
            {
                "nome_curso": "jogos digitais",
                "sigla": "JDG",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            },
            {
                "nome_curso": "computacao grafica",
                "sigla": "CGI",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            },
            {
                "nome_curso": "robotica",
                "sigla": "RBT",
                "tipo": "bacharelado",
                "duracao_semestres": 10
            },
            {
                "nome_curso": "automacao e controle",
                "sigla": "AUC",
                "tipo": "bacharelado",
                "duracao_semestres": 10
            },
            {
                "nome_curso": "gestao de infraestrutura",
                "sigla": "GIT",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            }
        ]
    },
    {
        "area": "Medicina",
        "cursos": [
            {
                "nome_curso": "medicina",
                "sigla": "MED",
                "tipo": "bacharelado",
                "duracao_semestres": 12
            },
            {
                "nome_curso": "enfermagem",
                "sigla": "ENF",
                "tipo": "bacharelado",
                "duracao_semestres": 10
            },
            {
                "nome_curso": "biomedicina",
                "sigla": "BMD",
                "tipo": "bacharelado",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "farmacia",
                "sigla": "FAR",
                "tipo": "bacharelado",
                "duracao_semestres": 10
            },
            {
                "nome_curso": "fisioterapia",
                "sigla": "FIS",
                "tipo": "bacharelado",
                "duracao_semestres": 10
            },
            {
                "nome_curso": "nutricao",
                "sigla": "NUT",
                "tipo": "bacharelado",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "odontologia",
                "sigla": "ODO",
                "tipo": "bacharelado",
                "duracao_semestres": 10
            },
            {
                "nome_curso": "psicologia",
                "sigla": "PSI",
                "tipo": "bacharelado",
                "duracao_semestres": 10
            }
        ]
    },
    {
        "area": "Exatas",
        "cursos": [
            {
                "nome_curso": "matematica",
                "sigla": "MAT",
                "tipo": "licenciatura",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "fisica",
                "sigla": "FSC",
                "tipo": "licenciatura",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "estatistica",
                "sigla": "EST",
                "tipo": "bacharelado",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "engenharia civil",
                "sigla": "ECV",
                "tipo": "bacharelado",
                "duracao_semestres": 10
            },
            {
                "nome_curso": "engenharia mecanica",
                "sigla": "EGM",
                "tipo": "bacharelado",
                "duracao_semestres": 10
            },
            {
                "nome_curso": "engenharia eletrica",
                "sigla": "EGE",
                "tipo": "bacharelado",
                "duracao_semestres": 10
            },
            {
                "nome_curso": "engenharia de producao",
                "sigla": "EGP",
                "tipo": "bacharelado",
                "duracao_semestres": 10
            }
        ]
    },
    {
        "area": "Economia",
        "cursos": [
            {
                "nome_curso": "economia",
                "sigla": "ECO",
                "tipo": "bacharelado",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "administracao",
                "sigla": "ADM",
                "tipo": "bacharelado",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "ciencias contabeis",
                "sigla": "CCO",
                "tipo": "bacharelado",
                "duracao_semestres": 8
            },
            {
                "nome_curso": "gestao financeira",
                "sigla": "GFI",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            },
            {
                "nome_curso": "comercio exterior",
                "sigla": "CEX",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            },
            {
                "nome_curso": "logistica",
                "sigla": "LOG",
                "tipo": "tecnologo",
                "duracao_semestres": 5
            }
        ]
    }
]


def normalizar_nome(nome: str):
    return nome.strip().lower()


def normalizar_sigla(sigla: str):
    return sigla.strip().upper()


def normalizar_tipo(tipo: str):
    return tipo.strip().lower()


def normalizar_status(status: str):
    return status.strip().lower()


def carregar_cursos_existentes():
    if not DATA_PATH.exists():
        return []

    with open(DATA_PATH, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()

        if not conteudo:
            return []

        return json.loads(conteudo)


def converter_areas_para_lista():
    cursos_formatados = []

    for area in AREAS_CURSOS:
        nome_area = area["area"]

        for curso in area["cursos"]:
            cursos_formatados.append({
                "area": nome_area,
                "nome_curso": normalizar_nome(curso["nome_curso"]),
                "sigla": normalizar_sigla(curso["sigla"]),
                "tipo": normalizar_tipo(curso["tipo"]),
                "duracao_semestres": int(curso["duracao_semestres"]),
                "status": "ativo"
            })

    return cursos_formatados


def encontrar_curso_existente(cursos_existentes, novo_curso):
    for curso in cursos_existentes:
        mesma_sigla = normalizar_sigla(curso["sigla"]) == normalizar_sigla(novo_curso["sigla"])
        mesmo_nome = normalizar_nome(curso["nome_curso"]) == normalizar_nome(novo_curso["nome_curso"])

        if mesma_sigla or mesmo_nome:
            return curso

    return None


def atualizar_curso_existente(curso_existente, novo_curso):
    curso_existente["area"] = novo_curso["area"]
    curso_existente["nome_curso"] = novo_curso["nome_curso"]
    curso_existente["sigla"] = novo_curso["sigla"]
    curso_existente["tipo"] = novo_curso["tipo"]
    curso_existente["duracao_semestres"] = novo_curso["duracao_semestres"]

    if "status" not in curso_existente:
        curso_existente["status"] = novo_curso["status"]

    curso_existente["status"] = normalizar_status(curso_existente["status"])

    return curso_existente


def adicionar_ou_atualizar_cursos():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    cursos_existentes = carregar_cursos_existentes()
    novos_cursos = converter_areas_para_lista()

    cursos_adicionados = 0
    cursos_atualizados = 0

    for novo_curso in novos_cursos:
        curso_existente = encontrar_curso_existente(cursos_existentes, novo_curso)

        if curso_existente:
            atualizar_curso_existente(curso_existente, novo_curso)
            cursos_atualizados += 1
            continue

        cursos_existentes.append(novo_curso)
        cursos_adicionados += 1

    with open(DATA_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(cursos_existentes, arquivo, ensure_ascii=False, indent=4)

    areas = sorted(set(curso["area"] for curso in cursos_existentes))
    tipos = sorted(set(curso["tipo"] for curso in cursos_existentes))

    print(f"Arquivo atualizado com segurança em: {DATA_PATH}")
    print(f"Cursos adicionados: {cursos_adicionados}")
    print(f"Cursos atualizados: {cursos_atualizados}")
    print(f"Total de áreas no arquivo: {len(areas)}")
    print(f"Total de tipos no arquivo: {len(tipos)}")
    print(f"Total de cursos no arquivo: {len(cursos_existentes)}")


if __name__ == "__main__":
    adicionar_ou_atualizar_cursos()