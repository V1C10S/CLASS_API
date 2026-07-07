import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "materias.json"


MATERIAS_POR_SEMESTRE = 2
CARGA_HORARIA_PADRAO = 80

STATUS_VALIDOS = ["ativa", "cancelada"]
STATUS_PADRAO = "ativa"


def garantir_arquivo_materias():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_PATH.exists():
        with open(DATA_PATH, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo, ensure_ascii=False, indent=4)


def carregar_materias():
    garantir_arquivo_materias()

    with open(DATA_PATH, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()

        if not conteudo:
            return []

        return json.loads(conteudo)


def salvar_materias(materias):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(DATA_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(materias, arquivo, ensure_ascii=False, indent=4)


def normalizar_texto(texto: str):
    return str(texto).strip().lower()


def normalizar_sigla(sigla: str):
    return str(sigla).strip().upper()


def normalizar_codigo(codigo: str):
    return str(codigo).strip().upper()


def normalizar_status(status: str):
    return str(status).strip().lower()


def validar_status(status: str):
    status_normalizado = normalizar_status(status)

    return status_normalizado in STATUS_VALIDOS


def normalizar_semestre(semestre):
    semestre = int(semestre)

    if semestre <= 0:
        raise ValueError("Semestre inválido.")

    return semestre


def normalizar_carga_horaria(carga_horaria):
    carga_horaria = int(carga_horaria)

    if carga_horaria <= 0:
        raise ValueError("Carga horária inválida.")

    return carga_horaria


def gerar_codigo_materia(curso: str, semestre: int, numero_materia: str):
    curso_normalizado = normalizar_sigla(curso)
    semestre_codigo = str(semestre).zfill(2)
    numero_codigo = str(numero_materia).zfill(2)

    return f"{curso_normalizado}_S{semestre_codigo}_M{numero_codigo}"


def extrair_numero_materia_do_codigo(codigo: str):
    codigo_normalizado = normalizar_codigo(codigo)
    partes = codigo_normalizado.split("_")

    if len(partes) != 3:
        raise ValueError("Código de matéria inválido. Use o formato ADS_S01_M01.")

    numero_materia = partes[2].replace("M", "")

    if not numero_materia.isdigit():
        raise ValueError("Número da matéria inválido no código.")

    return numero_materia.zfill(2)


def encontrar_numero_materia_disponivel(materias, curso: str, semestre: int, codigo_atual=None):
    curso_normalizado = normalizar_sigla(curso)
    semestre_normalizado = normalizar_semestre(semestre)
    codigo_atual_normalizado = normalizar_codigo(codigo_atual) if codigo_atual else None

    numeros_usados = set()

    for materia in materias:
        mesmo_curso = normalizar_sigla(materia["curso"]) == curso_normalizado
        mesmo_semestre = normalizar_semestre(materia["semestre"]) == semestre_normalizado
        mesmo_codigo_atual = (
            codigo_atual_normalizado
            and normalizar_codigo(materia["codigo"]) == codigo_atual_normalizado
        )

        if mesmo_curso and mesmo_semestre and not mesmo_codigo_atual:
            try:
                numero = int(extrair_numero_materia_do_codigo(materia["codigo"]))
                numeros_usados.add(numero)
            except ValueError:
                continue

    for numero in range(1, MATERIAS_POR_SEMESTRE + 1):
        if numero not in numeros_usados:
            return str(numero).zfill(2)

    return None


def listar_materias():
    return carregar_materias()


def buscar_materia_por_codigo(codigo: str):
    materias = carregar_materias()
    codigo_normalizado = normalizar_codigo(codigo)

    for materia in materias:
        if normalizar_codigo(materia["codigo"]) == codigo_normalizado:
            return materia

    return None


def listar_materias_por_curso(curso: str):
    materias = carregar_materias()
    curso_normalizado = normalizar_sigla(curso)

    resultado = []

    for materia in materias:
        if normalizar_sigla(materia["curso"]) == curso_normalizado:
            resultado.append(materia)

    return resultado


def listar_materias_por_semestre(semestre: int):
    materias = carregar_materias()
    semestre_normalizado = normalizar_semestre(semestre)

    resultado = []

    for materia in materias:
        if normalizar_semestre(materia["semestre"]) == semestre_normalizado:
            resultado.append(materia)

    return resultado


def listar_materias_por_curso_e_semestre(curso: str, semestre: int):
    materias = carregar_materias()
    curso_normalizado = normalizar_sigla(curso)
    semestre_normalizado = normalizar_semestre(semestre)

    resultado = []

    for materia in materias:
        mesmo_curso = normalizar_sigla(materia["curso"]) == curso_normalizado
        mesmo_semestre = normalizar_semestre(materia["semestre"]) == semestre_normalizado

        if mesmo_curso and mesmo_semestre:
            resultado.append(materia)

    return resultado


def listar_materias_por_status(status: str):
    materias = carregar_materias()
    status_normalizado = normalizar_status(status)

    resultado = []

    for materia in materias:
        if normalizar_status(materia["status"]) == status_normalizado:
            resultado.append(materia)

    return resultado


def buscar_materias_por_termo(termo: str):
    materias = carregar_materias()
    termo_normalizado = normalizar_texto(termo)

    resultado = []

    for materia in materias:
        codigo = normalizar_texto(materia["codigo"])
        nome = normalizar_texto(materia["nome"])
        curso = normalizar_texto(materia["curso"])
        semestre = str(materia["semestre"])
        carga_horaria = str(materia["carga_horaria"])
        status = normalizar_texto(materia["status"])

        if (
            termo_normalizado in codigo
            or termo_normalizado in nome
            or termo_normalizado in curso
            or termo_normalizado in semestre
            or termo_normalizado in carga_horaria
            or termo_normalizado in status
        ):
            resultado.append(materia)

    return resultado


def criar_materia(nova_materia: dict):
    materias = carregar_materias()

    campos_obrigatorios = [
        "nome",
        "curso",
        "semestre"
    ]

    for campo in campos_obrigatorios:
        if campo not in nova_materia:
            raise ValueError(f"Campo obrigatório ausente: {campo}")

    nome = normalizar_texto(nova_materia["nome"])
    curso = normalizar_sigla(nova_materia["curso"])
    semestre = normalizar_semestre(nova_materia["semestre"])
    carga_horaria = normalizar_carga_horaria(
        nova_materia.get("carga_horaria", CARGA_HORARIA_PADRAO)
    )
    status = normalizar_status(nova_materia.get("status", STATUS_PADRAO))

    if not validar_status(status):
        raise ValueError("Status inválido. Use: ativa ou cancelada.")

    numero_materia = encontrar_numero_materia_disponivel(
        materias,
        curso,
        semestre
    )

    if not numero_materia:
        raise ValueError("Esse curso e semestre já possuem 2 matérias.")

    codigo = gerar_codigo_materia(curso, semestre, numero_materia)

    materia_formatada = {
        "codigo": codigo,
        "nome": nome,
        "curso": curso,
        "semestre": semestre,
        "carga_horaria": carga_horaria,
        "status": status
    }

    materias.append(materia_formatada)
    salvar_materias(materias)

    return materia_formatada


def atualizar_materia(codigo: str, novos_dados: dict):
    materias = carregar_materias()
    codigo_normalizado = normalizar_codigo(codigo)

    if "codigo" in novos_dados:
        raise ValueError("O código da matéria não pode ser alterado manualmente.")

    for materia in materias:
        if normalizar_codigo(materia["codigo"]) == codigo_normalizado:
            curso_antigo = normalizar_sigla(materia["curso"])
            semestre_antigo = normalizar_semestre(materia["semestre"])

            novo_curso = normalizar_sigla(novos_dados.get("curso", curso_antigo))
            novo_semestre = normalizar_semestre(novos_dados.get("semestre", semestre_antigo))

            mudou_curso = novo_curso != curso_antigo
            mudou_semestre = novo_semestre != semestre_antigo

            if "nome" in novos_dados:
                materia["nome"] = normalizar_texto(novos_dados["nome"])

            if "carga_horaria" in novos_dados:
                materia["carga_horaria"] = normalizar_carga_horaria(
                    novos_dados["carga_horaria"]
                )

            if "status" in novos_dados:
                novo_status = normalizar_status(novos_dados["status"])

                if not validar_status(novo_status):
                    raise ValueError("Status inválido. Use: ativa ou cancelada.")

                materia["status"] = novo_status

            if mudou_curso or mudou_semestre:
                numero_materia = encontrar_numero_materia_disponivel(
                    materias,
                    novo_curso,
                    novo_semestre,
                    codigo_atual=materia["codigo"]
                )

                if not numero_materia:
                    raise ValueError("O novo curso e semestre já possuem 2 matérias.")

                materia["curso"] = novo_curso
                materia["semestre"] = novo_semestre
                materia["codigo"] = gerar_codigo_materia(
                    novo_curso,
                    novo_semestre,
                    numero_materia
                )

            salvar_materias(materias)

            return materia

    return None


def alterar_status_materia(codigo: str, novo_status: str):
    materias = carregar_materias()
    codigo_normalizado = normalizar_codigo(codigo)
    status_normalizado = normalizar_status(novo_status)

    if not validar_status(status_normalizado):
        raise ValueError("Status inválido. Use: ativa ou cancelada.")

    for materia in materias:
        if normalizar_codigo(materia["codigo"]) == codigo_normalizado:
            materia["status"] = status_normalizado
            salvar_materias(materias)

            return materia

    return None


def deletar_materia(codigo: str):
    materias = carregar_materias()
    codigo_normalizado = normalizar_codigo(codigo)

    for materia in materias:
        if normalizar_codigo(materia["codigo"]) == codigo_normalizado:
            materias.remove(materia)
            salvar_materias(materias)

            return materia

    return None