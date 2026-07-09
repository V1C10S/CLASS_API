from crud.alunos import buscar_aluno_por_ra
from crud.horarios import (
    listar_horarios_por_turma,
    listar_horarios_por_turma_e_semestre
)
from crud.materias import listar_materias


DIAS_ORDEM = {
    "segunda": 1,
    "terca": 2,
    "quarta": 3,
    "quinta": 4,
    "sexta": 5,
    "sabado": 6
}


def normalizar_texto(texto: str):
    return str(texto).strip().lower()


def normalizar_codigo(codigo: str):
    return str(codigo).strip().upper()


def horario_esta_ativo(horario: dict):
    return normalizar_texto(horario.get("status", "ativo")) == "ativo"


def materia_esta_ativa(materia: dict):
    if not materia:
        return False

    return normalizar_texto(materia.get("status", "ativa")) == "ativa"


def criar_mapa_materias():
    materias = listar_materias()
    mapa = {}

    for materia in materias:
        codigo = normalizar_codigo(materia["codigo"])
        mapa[codigo] = materia

    return mapa


def ordenar_grade(grade):
    return sorted(
        grade,
        key=lambda item: (
            DIAS_ORDEM.get(normalizar_texto(item["dia_semana"]), 99),
            item["inicio"],
            item["codigo_materia"]
        )
    )


def montar_item_grade(horario: dict, materias_por_codigo: dict):
    codigo_materia = normalizar_codigo(horario["codigo_materia"])
    materia = materias_por_codigo.get(codigo_materia)

    nome_materia = "matéria não encontrada"
    carga_horaria = None
    status_materia = "indefinido"

    if materia:
        nome_materia = materia["nome"]
        carga_horaria = materia["carga_horaria"]
        status_materia = materia["status"]

    return {
        "horario_id": horario["horario_id"],
        "turma_id": horario["turma_id"],
        "codigo_materia": horario["codigo_materia"],
        "nome_materia": nome_materia,
        "curso": horario["curso"],
        "semestre": horario["semestre"],
        "dia_semana": horario["dia_semana"],
        "inicio": horario["inicio"],
        "fim": horario["fim"],
        "sala": horario["sala"],
        "professor": horario["professor"],
        "carga_horaria": carga_horaria,
        "status_horario": horario["status"],
        "status_materia": status_materia
    }


def filtrar_horarios_para_grade(horarios, somente_ativos=True):
    materias_por_codigo = criar_mapa_materias()
    grade = []

    for horario in horarios:
        codigo_materia = normalizar_codigo(horario["codigo_materia"])
        materia = materias_por_codigo.get(codigo_materia)

        if somente_ativos:
            if not horario_esta_ativo(horario):
                continue

            if not materia_esta_ativa(materia):
                continue

        grade.append(
            montar_item_grade(
                horario,
                materias_por_codigo
            )
        )

    return ordenar_grade(grade)


def montar_resposta_grade(origem: dict, semestre, somente_ativos: bool, grade):
    return {
        "origem": origem,
        "filtro": {
            "semestre": semestre,
            "somente_ativos": somente_ativos
        },
        "total": len(grade),
        "grade": grade
    }


def montar_grade_por_ra(ra: str, somente_ativos=True):
    aluno = buscar_aluno_por_ra(ra)

    if not aluno:
        return None

    horarios = listar_horarios_por_turma(aluno["turma_id"])
    grade = filtrar_horarios_para_grade(horarios, somente_ativos)

    return montar_resposta_grade(
        origem={
            "ra": aluno["ra"],
            "turma_id": aluno["turma_id"]
        },
        semestre="todos",
        somente_ativos=somente_ativos,
        grade=grade
    )


def montar_grade_por_ra_e_semestre(ra: str, semestre: int, somente_ativos=True):
    aluno = buscar_aluno_por_ra(ra)

    if not aluno:
        return None

    horarios = listar_horarios_por_turma_e_semestre(
        aluno["turma_id"],
        semestre
    )

    grade = filtrar_horarios_para_grade(horarios, somente_ativos)

    return montar_resposta_grade(
        origem={
            "ra": aluno["ra"],
            "turma_id": aluno["turma_id"]
        },
        semestre=semestre,
        somente_ativos=somente_ativos,
        grade=grade
    )


def montar_grade_por_turma(turma_id: str, somente_ativos=True):
    horarios = listar_horarios_por_turma(turma_id)
    grade = filtrar_horarios_para_grade(horarios, somente_ativos)

    return montar_resposta_grade(
        origem={
            "turma_id": turma_id.upper()
        },
        semestre="todos",
        somente_ativos=somente_ativos,
        grade=grade
    )


def montar_grade_por_turma_e_semestre(turma_id: str, semestre: int, somente_ativos=True):
    horarios = listar_horarios_por_turma_e_semestre(
        turma_id,
        semestre
    )

    grade = filtrar_horarios_para_grade(horarios, somente_ativos)

    return montar_resposta_grade(
        origem={
            "turma_id": turma_id.upper()
        },
        semestre=semestre,
        somente_ativos=somente_ativos,
        grade=grade
    )