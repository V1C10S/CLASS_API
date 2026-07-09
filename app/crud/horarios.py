import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "horarios.json"


STATUS_VALIDOS = ["ativo", "cancelado"]
STATUS_PADRAO = "ativo"

DIAS_VALIDOS = [
    "segunda",
    "terca",
    "quarta",
    "quinta",
    "sexta",
    "sabado"
]


def garantir_arquivo_horarios():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_PATH.exists():
        with open(DATA_PATH, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo, ensure_ascii=False, indent=4)


def carregar_horarios():
    garantir_arquivo_horarios()

    with open(DATA_PATH, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()

        if not conteudo:
            return []

        return json.loads(conteudo)


def salvar_horarios(horarios):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(DATA_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(horarios, arquivo, ensure_ascii=False, indent=4)


def normalizar_texto(texto: str):
    return str(texto).strip().lower()


def normalizar_codigo(codigo: str):
    return str(codigo).strip().upper()


def normalizar_status(status: str):
    return str(status).strip().lower()


def normalizar_dia(dia: str):
    dia_normalizado = normalizar_texto(dia)

    trocas = {
        "terça": "terca",
        "sábado": "sabado"
    }

    return trocas.get(dia_normalizado, dia_normalizado)


def validar_status(status: str):
    return normalizar_status(status) in STATUS_VALIDOS


def validar_dia(dia: str):
    return normalizar_dia(dia) in DIAS_VALIDOS


def validar_hora(hora: str):
    hora_normalizada = str(hora).strip()

    partes = hora_normalizada.split(":")

    if len(partes) != 2:
        return False

    horas = partes[0]
    minutos = partes[1]

    if not horas.isdigit() or not minutos.isdigit():
        return False

    horas = int(horas)
    minutos = int(minutos)

    if horas < 0 or horas > 23:
        return False

    if minutos < 0 or minutos > 59:
        return False

    return True


def normalizar_hora(hora: str):
    hora_normalizada = str(hora).strip()

    if not validar_hora(hora_normalizada):
        raise ValueError("Horário inválido. Use o formato HH:MM.")

    horas, minutos = hora_normalizada.split(":")

    return f"{str(int(horas)).zfill(2)}:{str(int(minutos)).zfill(2)}"


def validar_intervalo(inicio: str, fim: str):
    inicio_normalizado = normalizar_hora(inicio)
    fim_normalizado = normalizar_hora(fim)

    if inicio_normalizado >= fim_normalizado:
        raise ValueError("O horário de início deve ser menor que o horário de fim.")

    return inicio_normalizado, fim_normalizado


def normalizar_semestre(semestre):
    semestre = int(semestre)

    if semestre <= 0:
        raise ValueError("Semestre inválido.")

    return semestre


def gerar_horario_id(turma_id: str, codigo_materia: str):
    return f"{normalizar_codigo(turma_id)}_{normalizar_codigo(codigo_materia)}"


def horario_id_ja_existe(horarios, horario_id: str):
    horario_id_normalizado = normalizar_codigo(horario_id)

    for horario in horarios:
        if normalizar_codigo(horario["horario_id"]) == horario_id_normalizado:
            return True

    return False


def horario_id_ja_existe_em_outro(horarios, novo_horario_id: str, horario_id_atual: str):
    novo_normalizado = normalizar_codigo(novo_horario_id)
    atual_normalizado = normalizar_codigo(horario_id_atual)

    for horario in horarios:
        mesmo_id_novo = normalizar_codigo(horario["horario_id"]) == novo_normalizado
        nao_e_o_atual = normalizar_codigo(horario["horario_id"]) != atual_normalizado

        if mesmo_id_novo and nao_e_o_atual:
            return True

    return False


def listar_horarios():
    return carregar_horarios()


def buscar_horario_por_id(horario_id: str):
    horarios = carregar_horarios()
    horario_id_normalizado = normalizar_codigo(horario_id)

    for horario in horarios:
        if normalizar_codigo(horario["horario_id"]) == horario_id_normalizado:
            return horario

    return None


def listar_horarios_por_turma(turma_id: str):
    horarios = carregar_horarios()
    turma_id_normalizado = normalizar_codigo(turma_id)

    resultado = []

    for horario in horarios:
        if normalizar_codigo(horario["turma_id"]) == turma_id_normalizado:
            resultado.append(horario)

    return resultado


def listar_horarios_por_materia(codigo_materia: str):
    horarios = carregar_horarios()
    codigo_materia_normalizado = normalizar_codigo(codigo_materia)

    resultado = []

    for horario in horarios:
        if normalizar_codigo(horario["codigo_materia"]) == codigo_materia_normalizado:
            resultado.append(horario)

    return resultado


def listar_horarios_por_curso(curso: str):
    horarios = carregar_horarios()
    curso_normalizado = normalizar_codigo(curso)

    resultado = []

    for horario in horarios:
        if normalizar_codigo(horario["curso"]) == curso_normalizado:
            resultado.append(horario)

    return resultado


def listar_horarios_por_semestre(semestre: int):
    horarios = carregar_horarios()
    semestre_normalizado = normalizar_semestre(semestre)

    resultado = []

    for horario in horarios:
        if normalizar_semestre(horario["semestre"]) == semestre_normalizado:
            resultado.append(horario)

    return resultado


def listar_horarios_por_dia(dia_semana: str):
    horarios = carregar_horarios()
    dia_normalizado = normalizar_dia(dia_semana)

    resultado = []

    for horario in horarios:
        if normalizar_dia(horario["dia_semana"]) == dia_normalizado:
            resultado.append(horario)

    return resultado


def listar_horarios_por_professor(professor: str):
    horarios = carregar_horarios()
    professor_normalizado = normalizar_texto(professor)

    resultado = []

    for horario in horarios:
        if professor_normalizado in normalizar_texto(horario["professor"]):
            resultado.append(horario)

    return resultado


def listar_horarios_por_status(status: str):
    horarios = carregar_horarios()
    status_normalizado = normalizar_status(status)

    resultado = []

    for horario in horarios:
        if normalizar_status(horario["status"]) == status_normalizado:
            resultado.append(horario)

    return resultado


def listar_horarios_por_turma_e_semestre(turma_id: str, semestre: int):
    horarios = carregar_horarios()
    turma_id_normalizado = normalizar_codigo(turma_id)
    semestre_normalizado = normalizar_semestre(semestre)

    resultado = []

    for horario in horarios:
        mesma_turma = normalizar_codigo(horario["turma_id"]) == turma_id_normalizado
        mesmo_semestre = normalizar_semestre(horario["semestre"]) == semestre_normalizado

        if mesma_turma and mesmo_semestre:
            resultado.append(horario)

    return resultado

def criar_horario(novo_horario: dict):
    horarios = carregar_horarios()

    campos_obrigatorios = [
        "turma_id",
        "codigo_materia",
        "curso",
        "semestre",
        "dia_semana",
        "inicio",
        "fim",
        "sala",
        "professor"
    ]

    for campo in campos_obrigatorios:
        if campo not in novo_horario:
            raise ValueError(f"Campo obrigatório ausente: {campo}")

    turma_id = normalizar_codigo(novo_horario["turma_id"])
    codigo_materia = normalizar_codigo(novo_horario["codigo_materia"])
    curso = normalizar_codigo(novo_horario["curso"])
    semestre = normalizar_semestre(novo_horario["semestre"])
    dia_semana = normalizar_dia(novo_horario["dia_semana"])
    inicio, fim = validar_intervalo(novo_horario["inicio"], novo_horario["fim"])
    sala = normalizar_codigo(novo_horario["sala"])
    professor = str(novo_horario["professor"]).strip()
    status = normalizar_status(novo_horario.get("status", STATUS_PADRAO))

    if not validar_dia(dia_semana):
        raise ValueError("Dia inválido. Use: segunda, terca, quarta, quinta, sexta ou sabado.")

    if not validar_status(status):
        raise ValueError("Status inválido. Use: ativo ou cancelado.")

    horario_id = gerar_horario_id(turma_id, codigo_materia)

    if horario_id_ja_existe(horarios, horario_id):
        raise ValueError("Já existe um horário para essa turma e matéria.")

    horario_formatado = {
        "horario_id": horario_id,
        "turma_id": turma_id,
        "codigo_materia": codigo_materia,
        "curso": curso,
        "semestre": semestre,
        "dia_semana": dia_semana,
        "inicio": inicio,
        "fim": fim,
        "sala": sala,
        "professor": professor,
        "status": status
    }

    horarios.append(horario_formatado)
    salvar_horarios(horarios)

    return horario_formatado


def atualizar_horario(horario_id: str, novos_dados: dict):
    horarios = carregar_horarios()
    horario_id_normalizado = normalizar_codigo(horario_id)

    if "horario_id" in novos_dados:
        raise ValueError("O horario_id não pode ser alterado manualmente.")

    for horario in horarios:
        if normalizar_codigo(horario["horario_id"]) == horario_id_normalizado:
            turma_antiga = normalizar_codigo(horario["turma_id"])
            materia_antiga = normalizar_codigo(horario["codigo_materia"])

            nova_turma = normalizar_codigo(novos_dados.get("turma_id", turma_antiga))
            nova_materia = normalizar_codigo(novos_dados.get("codigo_materia", materia_antiga))

            mudou_turma = nova_turma != turma_antiga
            mudou_materia = nova_materia != materia_antiga

            if "curso" in novos_dados:
                horario["curso"] = normalizar_codigo(novos_dados["curso"])

            if "semestre" in novos_dados:
                horario["semestre"] = normalizar_semestre(novos_dados["semestre"])

            if "dia_semana" in novos_dados:
                novo_dia = normalizar_dia(novos_dados["dia_semana"])

                if not validar_dia(novo_dia):
                    raise ValueError("Dia inválido. Use: segunda, terca, quarta, quinta, sexta ou sabado.")

                horario["dia_semana"] = novo_dia

            inicio = novos_dados.get("inicio", horario["inicio"])
            fim = novos_dados.get("fim", horario["fim"])

            inicio_normalizado, fim_normalizado = validar_intervalo(inicio, fim)
            horario["inicio"] = inicio_normalizado
            horario["fim"] = fim_normalizado

            if "sala" in novos_dados:
                horario["sala"] = normalizar_codigo(novos_dados["sala"])

            if "professor" in novos_dados:
                horario["professor"] = str(novos_dados["professor"]).strip()

            if "status" in novos_dados:
                novo_status = normalizar_status(novos_dados["status"])

                if not validar_status(novo_status):
                    raise ValueError("Status inválido. Use: ativo ou cancelado.")

                horario["status"] = novo_status

            if mudou_turma or mudou_materia:
                novo_horario_id = gerar_horario_id(nova_turma, nova_materia)

                if horario_id_ja_existe_em_outro(horarios, novo_horario_id, horario_id):
                    raise ValueError("A alteração geraria um horario_id que já existe.")

                horario["turma_id"] = nova_turma
                horario["codigo_materia"] = nova_materia
                horario["horario_id"] = novo_horario_id

            salvar_horarios(horarios)

            return horario

    return None


def alterar_status_horario(horario_id: str, novo_status: str):
    horarios = carregar_horarios()
    horario_id_normalizado = normalizar_codigo(horario_id)
    status_normalizado = normalizar_status(novo_status)

    if not validar_status(status_normalizado):
        raise ValueError("Status inválido. Use: ativo ou cancelado.")

    for horario in horarios:
        if normalizar_codigo(horario["horario_id"]) == horario_id_normalizado:
            horario["status"] = status_normalizado
            salvar_horarios(horarios)

            return horario

    return None


def deletar_horario(horario_id: str):
    horarios = carregar_horarios()
    horario_id_normalizado = normalizar_codigo(horario_id)

    for horario in horarios:
        if normalizar_codigo(horario["horario_id"]) == horario_id_normalizado:
            horarios.remove(horario)
            salvar_horarios(horarios)

            return horario

    return None