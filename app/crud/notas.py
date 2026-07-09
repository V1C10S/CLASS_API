import json
from pathlib import Path

from crud.alunos import buscar_aluno_por_ra
from crud.materias import buscar_materia_por_codigo


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
NOTAS_DIR = DATA_DIR / "notas"


MEDIA_APROVACAO = 6.0

STATUS_PENDENTE = "pendente"
STATUS_APROVADO = "aprovado"
STATUS_REPROVADO = "reprovado"

STATUS_VALIDOS = [
    STATUS_PENDENTE,
    STATUS_APROVADO,
    STATUS_REPROVADO
]


def garantir_pasta_notas():
    NOTAS_DIR.mkdir(parents=True, exist_ok=True)


def normalizar_texto(texto: str):
    return str(texto).strip().lower()


def normalizar_codigo(codigo: str):
    return str(codigo).strip().upper()


def normalizar_ra(ra: str):
    return str(ra).strip()


def validar_ra(ra: str):
    return normalizar_ra(ra).isdigit()


def gerar_caminho_notas(curso: str, turma_id: str):
    curso_normalizado = normalizar_codigo(curso)
    turma_normalizada = normalizar_codigo(turma_id)

    return NOTAS_DIR / curso_normalizado / f"{turma_normalizada}.json"


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


def carregar_notas_por_arquivo(curso: str, turma_id: str):
    caminho = gerar_caminho_notas(curso, turma_id)

    return carregar_json(caminho)


def salvar_notas_por_arquivo(curso: str, turma_id: str, notas):
    caminho = gerar_caminho_notas(curso, turma_id)

    salvar_json(caminho, notas)


def carregar_todas_as_notas():
    garantir_pasta_notas()

    notas = []

    for arquivo in NOTAS_DIR.glob("*/*.json"):
        notas.extend(carregar_json(arquivo))

    return notas


def carregar_notas_por_curso_arquivo(curso: str):
    garantir_pasta_notas()

    curso_normalizado = normalizar_codigo(curso)
    pasta_curso = NOTAS_DIR / curso_normalizado

    notas = []

    if not pasta_curso.exists():
        return notas

    for arquivo in pasta_curso.glob("*.json"):
        notas.extend(carregar_json(arquivo))

    return notas


def normalizar_nota(nota):
    if nota is None:
        return None

    valor = float(nota)

    if valor < 0 or valor > 10:
        raise ValueError("Nota inválida. Use valores entre 0 e 10.")

    return round(valor, 2)


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


def materia_esta_ativa(materia: dict):
    return normalizar_texto(materia.get("status", "ativa")) == "ativa"


def gerar_nota_id(ra: str, codigo_materia: str):
    return f"{normalizar_ra(ra)}_{normalizar_codigo(codigo_materia)}"


def extrair_ra_do_nota_id(nota_id: str):
    nota_id_normalizado = str(nota_id).strip()

    partes = nota_id_normalizado.split("_")

    if not partes:
        return None

    ra = partes[0]

    if not validar_ra(ra):
        return None

    return ra


def validar_aluno_e_materia(ra: str, codigo_materia: str):
    ra_normalizado = normalizar_ra(ra)
    codigo_normalizado = normalizar_codigo(codigo_materia)

    if not validar_ra(ra_normalizado):
        raise ValueError("RA inválido. O RA deve conter apenas números.")

    aluno = buscar_aluno_por_ra(ra_normalizado)

    if not aluno:
        raise ValueError("Aluno não encontrado.")

    materia = buscar_materia_por_codigo(codigo_normalizado)

    if not materia:
        raise ValueError("Matéria não encontrada.")

    if not materia_esta_ativa(materia):
        raise ValueError("Não é possível lançar nota para uma matéria cancelada.")

    if normalizar_codigo(aluno["curso"]) != normalizar_codigo(materia["curso"]):
        raise ValueError("A matéria não pertence ao curso do aluno.")

    return aluno, materia


def montar_nota_formatada(aluno: dict, materia: dict, nota_1=None, nota_2=None):
    nota_1_normalizada = normalizar_nota(nota_1)
    nota_2_normalizada = normalizar_nota(nota_2)

    media = calcular_media(
        nota_1_normalizada,
        nota_2_normalizada
    )

    status = calcular_status(media)

    return {
        "nota_id": gerar_nota_id(aluno["ra"], materia["codigo"]),
        "ra": normalizar_ra(aluno["ra"]),
        "codigo_materia": normalizar_codigo(materia["codigo"]),
        "curso": normalizar_codigo(aluno["curso"]),
        "turma_id": normalizar_codigo(aluno["turma_id"]),
        "semestre": int(materia["semestre"]),
        "nota_1": nota_1_normalizada,
        "nota_2": nota_2_normalizada,
        "media": media,
        "status": status
    }


def ordenar_notas(notas):
    return sorted(
        notas,
        key=lambda nota: (
            normalizar_ra(nota["ra"]),
            int(nota["semestre"]),
            normalizar_codigo(nota["codigo_materia"])
        )
    )


def nota_ja_existe(notas, nota_id: str):
    nota_id_normalizado = normalizar_codigo(nota_id)

    for nota in notas:
        if normalizar_codigo(nota["nota_id"]) == nota_id_normalizado:
            return True

    return False


def localizar_nota(nota_id: str):
    ra = extrair_ra_do_nota_id(nota_id)

    if not ra:
        return None, None, None

    aluno = buscar_aluno_por_ra(ra)

    if not aluno:
        return None, None, None

    caminho = gerar_caminho_notas(
        aluno["curso"],
        aluno["turma_id"]
    )

    notas = carregar_json(caminho)
    nota_id_normalizado = normalizar_codigo(nota_id)

    for nota in notas:
        if normalizar_codigo(nota["nota_id"]) == nota_id_normalizado:
            return nota, notas, caminho

    return None, notas, caminho


def listar_notas():
    return carregar_todas_as_notas()


def buscar_nota_por_id(nota_id: str):
    nota, notas, caminho = localizar_nota(nota_id)

    return nota


def buscar_nota_por_ra_e_materia(ra: str, codigo_materia: str):
    nota_id = gerar_nota_id(
        ra,
        codigo_materia
    )

    return buscar_nota_por_id(nota_id)


def listar_notas_por_ra(ra: str):
    aluno = buscar_aluno_por_ra(ra)

    if not aluno:
        return []

    notas = carregar_notas_por_arquivo(
        aluno["curso"],
        aluno["turma_id"]
    )

    ra_normalizado = normalizar_ra(ra)

    resultado = []

    for nota in notas:
        if normalizar_ra(nota["ra"]) == ra_normalizado:
            resultado.append(nota)

    return ordenar_notas(resultado)


def listar_notas_por_turma(turma_id: str):
    turma_normalizada = normalizar_codigo(turma_id)
    todas = carregar_todas_as_notas()

    resultado = []

    for nota in todas:
        if normalizar_codigo(nota["turma_id"]) == turma_normalizada:
            resultado.append(nota)

    return ordenar_notas(resultado)


def listar_notas_por_materia(codigo_materia: str):
    todas = carregar_todas_as_notas()
    codigo_normalizado = normalizar_codigo(codigo_materia)

    resultado = []

    for nota in todas:
        if normalizar_codigo(nota["codigo_materia"]) == codigo_normalizado:
            resultado.append(nota)

    return ordenar_notas(resultado)


def listar_notas_por_curso(curso: str):
    notas = carregar_notas_por_curso_arquivo(curso)

    return ordenar_notas(notas)


def listar_notas_por_semestre(semestre: int):
    todas = carregar_todas_as_notas()
    semestre_normalizado = int(semestre)

    resultado = []

    for nota in todas:
        if int(nota["semestre"]) == semestre_normalizado:
            resultado.append(nota)

    return ordenar_notas(resultado)


def listar_notas_por_status(status: str):
    todas = carregar_todas_as_notas()
    status_normalizado = normalizar_texto(status)

    resultado = []

    for nota in todas:
        if normalizar_texto(nota["status"]) == status_normalizado:
            resultado.append(nota)

    return ordenar_notas(resultado)


def listar_notas_por_ra_e_semestre(ra: str, semestre: int):
    notas = listar_notas_por_ra(ra)
    semestre_normalizado = int(semestre)

    resultado = []

    for nota in notas:
        if int(nota["semestre"]) == semestre_normalizado:
            resultado.append(nota)

    return ordenar_notas(resultado)


def listar_notas_por_ra_e_status(ra: str, status: str):
    notas = listar_notas_por_ra(ra)
    status_normalizado = normalizar_texto(status)

    resultado = []

    for nota in notas:
        if normalizar_texto(nota["status"]) == status_normalizado:
            resultado.append(nota)

    return ordenar_notas(resultado)


def criar_nota(nova_nota: dict):
    campos_obrigatorios = [
        "ra",
        "codigo_materia"
    ]

    for campo in campos_obrigatorios:
        if campo not in nova_nota:
            raise ValueError(f"Campo obrigatório ausente: {campo}")

    aluno, materia = validar_aluno_e_materia(
        nova_nota["ra"],
        nova_nota["codigo_materia"]
    )

    curso = normalizar_codigo(aluno["curso"])
    turma_id = normalizar_codigo(aluno["turma_id"])

    notas = carregar_notas_por_arquivo(curso, turma_id)

    nota_formatada = montar_nota_formatada(
        aluno=aluno,
        materia=materia,
        nota_1=nova_nota.get("nota_1"),
        nota_2=nova_nota.get("nota_2")
    )

    if nota_ja_existe(notas, nota_formatada["nota_id"]):
        raise ValueError("Já existe uma nota para esse aluno nessa matéria.")

    notas.append(nota_formatada)
    notas = ordenar_notas(notas)

    salvar_notas_por_arquivo(curso, turma_id, notas)

    return nota_formatada


def atualizar_nota(nota_id: str, novos_dados: dict):
    campos_bloqueados = [
        "nota_id",
        "curso",
        "turma_id",
        "semestre",
        "media",
        "status"
    ]

    for campo in campos_bloqueados:
        if campo in novos_dados:
            raise ValueError(f"O campo {campo} não pode ser alterado manualmente.")

    nota_antiga, notas_antigas, caminho_antigo = localizar_nota(nota_id)

    if not nota_antiga:
        return None

    ra_novo = normalizar_ra(
        novos_dados.get("ra", nota_antiga["ra"])
    )

    codigo_materia_novo = normalizar_codigo(
        novos_dados.get("codigo_materia", nota_antiga["codigo_materia"])
    )

    aluno_novo, materia_nova = validar_aluno_e_materia(
        ra_novo,
        codigo_materia_novo
    )

    nota_1 = nota_antiga["nota_1"]
    nota_2 = nota_antiga["nota_2"]

    if "nota_1" in novos_dados:
        nota_1 = normalizar_nota(novos_dados["nota_1"])

    if "nota_2" in novos_dados:
        nota_2 = normalizar_nota(novos_dados["nota_2"])

    nota_nova = montar_nota_formatada(
        aluno=aluno_novo,
        materia=materia_nova,
        nota_1=nota_1,
        nota_2=nota_2
    )

    curso_novo = normalizar_codigo(aluno_novo["curso"])
    turma_nova = normalizar_codigo(aluno_novo["turma_id"])
    caminho_novo = gerar_caminho_notas(curso_novo, turma_nova)

    mesmo_arquivo = caminho_antigo == caminho_novo
    mesmo_id = normalizar_codigo(nota_antiga["nota_id"]) == normalizar_codigo(nota_nova["nota_id"])

    if mesmo_arquivo:
        notas_atualizadas = []

        for nota in notas_antigas:
            if normalizar_codigo(nota["nota_id"]) == normalizar_codigo(nota_antiga["nota_id"]):
                continue

            notas_atualizadas.append(nota)

        if not mesmo_id and nota_ja_existe(notas_atualizadas, nota_nova["nota_id"]):
            raise ValueError("A alteração geraria uma nota duplicada.")

        notas_atualizadas.append(nota_nova)
        notas_atualizadas = ordenar_notas(notas_atualizadas)

        salvar_json(caminho_antigo, notas_atualizadas)

        return nota_nova

    notas_novas = carregar_json(caminho_novo)

    if nota_ja_existe(notas_novas, nota_nova["nota_id"]):
        raise ValueError("A alteração geraria uma nota duplicada.")

    notas_antigas_filtradas = []

    for nota in notas_antigas:
        if normalizar_codigo(nota["nota_id"]) == normalizar_codigo(nota_antiga["nota_id"]):
            continue

        notas_antigas_filtradas.append(nota)

    notas_novas.append(nota_nova)

    salvar_json(caminho_antigo, ordenar_notas(notas_antigas_filtradas))
    salvar_json(caminho_novo, ordenar_notas(notas_novas))

    return nota_nova


def lancar_nota_1(nota_id: str, valor):
    return atualizar_nota(
        nota_id,
        {
            "nota_1": valor
        }
    )


def lancar_nota_2(nota_id: str, valor):
    return atualizar_nota(
        nota_id,
        {
            "nota_2": valor
        }
    )


def deletar_nota(nota_id: str):
    nota, notas, caminho = localizar_nota(nota_id)

    if not nota:
        return None

    notas_filtradas = []

    for item in notas:
        if normalizar_codigo(item["nota_id"]) == normalizar_codigo(nota_id):
            continue

        notas_filtradas.append(item)

    salvar_json(caminho, ordenar_notas(notas_filtradas))

    return nota