import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "alunos.json"


STATUS_VALIDOS = ["ativo", "trancado", "inativo"]


def garantir_arquivo_alunos():
    DATA_DIR.mkdir(exist_ok=True)

    if not DATA_PATH.exists():
        with open(DATA_PATH, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo, ensure_ascii=False, indent=4)


def carregar_alunos():
    garantir_arquivo_alunos()

    with open(DATA_PATH, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()

        if not conteudo:
            return []

        return json.loads(conteudo)


def salvar_alunos(alunos):
    DATA_DIR.mkdir(exist_ok=True)

    with open(DATA_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(alunos, arquivo, ensure_ascii=False, indent=4)


def normalizar_texto(texto: str):
    return str(texto).strip().lower()


def normalizar_sigla(sigla: str):
    return str(sigla).strip().upper()


def normalizar_ra(ra: str):
    return str(ra).strip()


def normalizar_email(email: str):
    return str(email).strip().lower()


def normalizar_turma_id(turma_id: str):
    return str(turma_id).strip().upper()


def validar_status(status: str):
    return normalizar_texto(status) in STATUS_VALIDOS


def validar_ra(ra: str):
    return normalizar_ra(ra).isdigit()


def converter_letra_para_numero(letra: str):
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letra_normalizada = letra.strip().upper()

    if letra_normalizada not in alfabeto:
        return "00"

    numero = alfabeto.index(letra_normalizada) + 1

    return str(numero).zfill(2)


def converter_sigla_para_codigo(sigla: str):
    sigla_normalizada = normalizar_sigla(sigla)
    codigo = ""

    for letra in sigla_normalizada:
        codigo += converter_letra_para_numero(letra)

    return codigo


def converter_periodo_para_turno(periodo: str):
    periodo_normalizado = normalizar_texto(periodo)

    periodos = {
        "manha": "MAN",
        "tarde": "TAR",
        "noite": "NOT"
    }

    if periodo_normalizado not in periodos:
        raise ValueError("Período inválido. Use: manha, tarde ou noite.")

    return periodos[periodo_normalizado]


def converter_turno_para_codigo(turno: str):
    turno_normalizado = normalizar_sigla(turno)

    turnos = {
        "MAN": "01",
        "TAR": "02",
        "NOT": "03"
    }

    if turno_normalizado not in turnos:
        raise ValueError("Turno inválido. Use: MAN, TAR ou NOT.")

    return turnos[turno_normalizado]


def extrair_dados_da_turma_id(turma_id: str):
    turma_id_normalizado = normalizar_turma_id(turma_id)
    partes = turma_id_normalizado.split("_")

    if len(partes) != 4:
        raise ValueError("turma_id inválido. Use o formato ADS_2026_S1_001.")

    entrada_semestre = partes[2].replace("S", "")
    numero_turma = partes[3]

    if not entrada_semestre.isdigit():
        raise ValueError("Semestre de entrada inválido no turma_id.")

    if not numero_turma.isdigit():
        raise ValueError("Número da turma inválido no turma_id.")

    entrada_codigo = entrada_semestre.zfill(2)
    numero_turma_codigo = numero_turma.zfill(3)

    return entrada_codigo, numero_turma_codigo


def extrair_numero_aluno_do_ra(ra: str):
    ra_normalizado = normalizar_ra(ra)

    if not validar_ra(ra_normalizado):
        raise ValueError("RA inválido. O RA deve conter apenas números.")

    return ra_normalizado[-3:]


def gerar_ra(ano: int, curso: str, turma_id: str, turno: str, numero_aluno: str):
    ano_codigo = str(ano)
    curso_codigo = converter_sigla_para_codigo(curso)
    entrada_codigo, numero_turma_codigo = extrair_dados_da_turma_id(turma_id)
    turno_codigo = converter_turno_para_codigo(turno)

    return f"{ano_codigo}{curso_codigo}{entrada_codigo}{turno_codigo}{numero_turma_codigo}{numero_aluno}"


def gerar_proximo_numero_aluno(alunos, turma_id: str):
    turma_id_normalizado = normalizar_turma_id(turma_id)
    maior_numero = 0

    for aluno in alunos:
        if normalizar_turma_id(aluno["turma_id"]) == turma_id_normalizado:
            numero_aluno = int(extrair_numero_aluno_do_ra(aluno["ra"]))

            if numero_aluno > maior_numero:
                maior_numero = numero_aluno

    proximo_numero = maior_numero + 1

    return str(proximo_numero).zfill(3)


def ra_ja_existe_em_outro_aluno(alunos, novo_ra: str, ra_atual: str):
    novo_ra_normalizado = normalizar_ra(novo_ra)
    ra_atual_normalizado = normalizar_ra(ra_atual)

    for aluno in alunos:
        if (
            normalizar_ra(aluno["ra"]) == novo_ra_normalizado
            and normalizar_ra(aluno["ra"]) != ra_atual_normalizado
        ):
            return True

    return False


def email_ja_existe_em_outro_aluno(alunos, novo_email: str, ra_atual: str):
    email_normalizado = normalizar_email(novo_email)
    ra_atual_normalizado = normalizar_ra(ra_atual)

    for aluno in alunos:
        if (
            normalizar_email(aluno["email"]) == email_normalizado
            and normalizar_ra(aluno["ra"]) != ra_atual_normalizado
        ):
            return True

    return False


def listar_alunos():
    return carregar_alunos()


def buscar_aluno_por_ra(ra: str):
    alunos = carregar_alunos()
    ra_normalizado = normalizar_ra(ra)

    for aluno in alunos:
        if normalizar_ra(aluno["ra"]) == ra_normalizado:
            return aluno

    return None


def buscar_aluno_por_email(email: str):
    alunos = carregar_alunos()
    email_normalizado = normalizar_email(email)

    for aluno in alunos:
        if normalizar_email(aluno["email"]) == email_normalizado:
            return aluno

    return None


def listar_alunos_por_turma(turma_id: str):
    alunos = carregar_alunos()
    turma_id_normalizado = normalizar_turma_id(turma_id)

    resultado = []

    for aluno in alunos:
        if normalizar_turma_id(aluno["turma_id"]) == turma_id_normalizado:
            resultado.append(aluno)

    return resultado


def listar_alunos_por_curso(curso: str):
    alunos = carregar_alunos()
    curso_normalizado = normalizar_sigla(curso)

    resultado = []

    for aluno in alunos:
        if normalizar_sigla(aluno["curso"]) == curso_normalizado:
            resultado.append(aluno)

    return resultado


def listar_alunos_por_ano(ano: int):
    alunos = carregar_alunos()
    resultado = []

    for aluno in alunos:
        if int(aluno["ano"]) == int(ano):
            resultado.append(aluno)

    return resultado


def listar_alunos_por_periodo(periodo: str):
    alunos = carregar_alunos()
    periodo_normalizado = normalizar_texto(periodo)

    resultado = []

    for aluno in alunos:
        if normalizar_texto(aluno["periodo"]) == periodo_normalizado:
            resultado.append(aluno)

    return resultado


def listar_alunos_por_turno(turno: str):
    alunos = carregar_alunos()
    turno_normalizado = normalizar_sigla(turno)

    resultado = []

    for aluno in alunos:
        if normalizar_sigla(aluno["turno"]) == turno_normalizado:
            resultado.append(aluno)

    return resultado


def listar_alunos_por_status(status: str):
    alunos = carregar_alunos()
    status_normalizado = normalizar_texto(status)

    resultado = []

    for aluno in alunos:
        if normalizar_texto(aluno["status"]) == status_normalizado:
            resultado.append(aluno)

    return resultado


def buscar_alunos_por_termo(termo: str):
    alunos = carregar_alunos()
    termo_normalizado = normalizar_texto(termo)

    resultado = []

    for aluno in alunos:
        nome = normalizar_texto(aluno["nome"])
        ra = normalizar_ra(aluno["ra"])
        turma_id = normalizar_texto(aluno["turma_id"])
        email = normalizar_email(aluno["email"])
        curso = normalizar_texto(aluno["curso"])
        ano = str(aluno["ano"])
        periodo = normalizar_texto(aluno["periodo"])
        turno = normalizar_texto(aluno["turno"])
        status = normalizar_texto(aluno["status"])

        if (
            termo_normalizado in nome
            or termo_normalizado in ra
            or termo_normalizado in turma_id
            or termo_normalizado in email
            or termo_normalizado in curso
            or termo_normalizado in ano
            or termo_normalizado in periodo
            or termo_normalizado in turno
            or termo_normalizado in status
        ):
            resultado.append(aluno)

    return resultado


def criar_aluno(novo_aluno: dict):
    alunos = carregar_alunos()

    campos_obrigatorios = [
        "nome",
        "turma_id",
        "email",
        "curso",
        "ano",
        "periodo"
    ]

    for campo in campos_obrigatorios:
        if campo not in novo_aluno:
            raise ValueError(f"Campo obrigatório ausente: {campo}")

    nome = str(novo_aluno["nome"]).strip()
    turma_id = normalizar_turma_id(novo_aluno["turma_id"])
    email = normalizar_email(novo_aluno["email"])
    curso = normalizar_sigla(novo_aluno["curso"])
    ano = int(novo_aluno["ano"])
    periodo = normalizar_texto(novo_aluno["periodo"])
    turno = converter_periodo_para_turno(periodo)
    status = normalizar_texto(novo_aluno.get("status", "ativo"))

    if not validar_status(status):
        raise ValueError("Status inválido. Use: ativo, trancado ou inativo.")

    if buscar_aluno_por_email(email):
        raise ValueError("Já existe um aluno com esse email.")

    numero_aluno = gerar_proximo_numero_aluno(alunos, turma_id)
    ra = gerar_ra(ano, curso, turma_id, turno, numero_aluno)

    if buscar_aluno_por_ra(ra):
        raise ValueError("Já existe um aluno com esse RA.")

    aluno_formatado = {
        "nome": nome,
        "ra": ra,
        "turma_id": turma_id,
        "email": email,
        "curso": curso,
        "ano": ano,
        "periodo": periodo,
        "turno": turno,
        "status": status
    }

    alunos.append(aluno_formatado)
    salvar_alunos(alunos)

    return aluno_formatado


def atualizar_aluno(ra: str, novos_dados: dict):
    alunos = carregar_alunos()
    ra_normalizado = normalizar_ra(ra)

    for aluno in alunos:
        if normalizar_ra(aluno["ra"]) == ra_normalizado:
            ra_antigo = aluno["ra"]
            precisa_recalcular_ra = False

            if "nome" in novos_dados:
                aluno["nome"] = str(novos_dados["nome"]).strip()

            if "email" in novos_dados:
                novo_email = normalizar_email(novos_dados["email"])

                if email_ja_existe_em_outro_aluno(alunos, novo_email, ra_antigo):
                    raise ValueError("Já existe outro aluno com esse email.")

                aluno["email"] = novo_email

            if "turma_id" in novos_dados:
                aluno["turma_id"] = normalizar_turma_id(novos_dados["turma_id"])
                precisa_recalcular_ra = True

            if "curso" in novos_dados:
                aluno["curso"] = normalizar_sigla(novos_dados["curso"])
                precisa_recalcular_ra = True

            if "ano" in novos_dados:
                aluno["ano"] = int(novos_dados["ano"])
                precisa_recalcular_ra = True

            if "periodo" in novos_dados:
                aluno["periodo"] = normalizar_texto(novos_dados["periodo"])
                aluno["turno"] = converter_periodo_para_turno(aluno["periodo"])
                precisa_recalcular_ra = True

            if "turno" in novos_dados and "periodo" not in novos_dados:
                aluno["turno"] = normalizar_sigla(novos_dados["turno"])
                converter_turno_para_codigo(aluno["turno"])
                precisa_recalcular_ra = True

            if "status" in novos_dados:
                novo_status = normalizar_texto(novos_dados["status"])

                if not validar_status(novo_status):
                    raise ValueError("Status inválido. Use: ativo, trancado ou inativo.")

                aluno["status"] = novo_status

            if precisa_recalcular_ra:
                numero_aluno = extrair_numero_aluno_do_ra(ra_antigo)

                novo_ra = gerar_ra(
                    aluno["ano"],
                    aluno["curso"],
                    aluno["turma_id"],
                    aluno["turno"],
                    numero_aluno
                )

                if ra_ja_existe_em_outro_aluno(alunos, novo_ra, ra_antigo):
                    raise ValueError("A alteração geraria um RA que já existe.")

                aluno["ra"] = novo_ra

            salvar_alunos(alunos)

            return aluno

    return None


def alterar_status_aluno(ra: str, novo_status: str):
    alunos = carregar_alunos()
    ra_normalizado = normalizar_ra(ra)
    status_normalizado = normalizar_texto(novo_status)

    if not validar_status(status_normalizado):
        raise ValueError("Status inválido. Use: ativo, trancado ou inativo.")

    for aluno in alunos:
        if normalizar_ra(aluno["ra"]) == ra_normalizado:
            aluno["status"] = status_normalizado
            salvar_alunos(alunos)

            return aluno

    return None


def deletar_aluno(ra: str):
    alunos = carregar_alunos()
    ra_normalizado = normalizar_ra(ra)

    for aluno in alunos:
        if normalizar_ra(aluno["ra"]) == ra_normalizado:
            alunos.remove(aluno)
            salvar_alunos(alunos)

            return aluno

    return None