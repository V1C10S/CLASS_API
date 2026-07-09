from enum import Enum
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from crud.horarios import (
    listar_horarios,
    buscar_horario_por_id,
    listar_horarios_por_turma,
    listar_horarios_por_materia,
    listar_horarios_por_curso,
    listar_horarios_por_semestre,
    listar_horarios_por_dia,
    listar_horarios_por_professor,
    listar_horarios_por_status,
    listar_horarios_por_turma_e_semestre,
    criar_horario,
    atualizar_horario,
    alterar_status_horario,
    deletar_horario
)


router = APIRouter(
    prefix="/horarios",
    tags=["Horários"]
)


class StatusHorario(str, Enum):
    ativo = "ativo"
    cancelado = "cancelado"


class DiaSemana(str, Enum):
    segunda = "segunda"
    terca = "terca"
    quarta = "quarta"
    quinta = "quinta"
    sexta = "sexta"
    sabado = "sabado"


class HorarioCreate(BaseModel):
    turma_id: str
    codigo_materia: str
    curso: str
    semestre: int
    dia_semana: DiaSemana
    inicio: str
    fim: str
    sala: str
    professor: str
    status: Optional[StatusHorario] = StatusHorario.ativo


class HorarioUpdate(BaseModel):
    turma_id: Optional[str] = None
    codigo_materia: Optional[str] = None
    curso: Optional[str] = None
    semestre: Optional[int] = None
    dia_semana: Optional[DiaSemana] = None
    inicio: Optional[str] = None
    fim: Optional[str] = None
    sala: Optional[str] = None
    professor: Optional[str] = None
    status: Optional[StatusHorario] = None


@router.get("/")
def get_horarios():
    horarios = listar_horarios()

    return {
        "total": len(horarios),
        "horarios": horarios
    }


@router.get("/id/{horario_id}")
def get_horario_por_id(horario_id: str):
    horario = buscar_horario_por_id(horario_id)

    if not horario:
        raise HTTPException(
            status_code=404,
            detail="Horário não encontrado"
        )

    return horario


@router.get("/turma/{turma_id}/semestre/{semestre}")
def get_horarios_por_turma_e_semestre(turma_id: str, semestre: int):
    horarios = listar_horarios_por_turma_e_semestre(turma_id, semestre)

    if not horarios:
        raise HTTPException(
            status_code=404,
            detail="Nenhum horário encontrado para essa turma e semestre"
        )

    return {
        "turma_id": turma_id.upper(),
        "semestre": semestre,
        "total": len(horarios),
        "horarios": horarios
    }


@router.get("/turma/{turma_id}")
def get_horarios_por_turma(turma_id: str):
    horarios = listar_horarios_por_turma(turma_id)

    if not horarios:
        raise HTTPException(
            status_code=404,
            detail="Nenhum horário encontrado para essa turma"
        )

    return {
        "turma_id": turma_id.upper(),
        "total": len(horarios),
        "horarios": horarios
    }


@router.get("/materia/{codigo_materia}")
def get_horarios_por_materia(codigo_materia: str):
    horarios = listar_horarios_por_materia(codigo_materia)

    if not horarios:
        raise HTTPException(
            status_code=404,
            detail="Nenhum horário encontrado para essa matéria"
        )

    return {
        "codigo_materia": codigo_materia.upper(),
        "total": len(horarios),
        "horarios": horarios
    }


@router.get("/curso/{curso}")
def get_horarios_por_curso(curso: str):
    horarios = listar_horarios_por_curso(curso)

    if not horarios:
        raise HTTPException(
            status_code=404,
            detail="Nenhum horário encontrado para esse curso"
        )

    return {
        "curso": curso.upper(),
        "total": len(horarios),
        "horarios": horarios
    }


@router.get("/semestre/{semestre}")
def get_horarios_por_semestre(semestre: int):
    horarios = listar_horarios_por_semestre(semestre)

    if not horarios:
        raise HTTPException(
            status_code=404,
            detail="Nenhum horário encontrado para esse semestre"
        )

    return {
        "semestre": semestre,
        "total": len(horarios),
        "horarios": horarios
    }


@router.get("/dia/{dia_semana}")
def get_horarios_por_dia(dia_semana: DiaSemana):
    horarios = listar_horarios_por_dia(dia_semana.value)

    if not horarios:
        raise HTTPException(
            status_code=404,
            detail="Nenhum horário encontrado para esse dia"
        )

    return {
        "dia_semana": dia_semana.value,
        "total": len(horarios),
        "horarios": horarios
    }


@router.get("/professor/{professor}")
def get_horarios_por_professor(professor: str):
    horarios = listar_horarios_por_professor(professor)

    if not horarios:
        raise HTTPException(
            status_code=404,
            detail="Nenhum horário encontrado para esse professor"
        )

    return {
        "professor": professor,
        "total": len(horarios),
        "horarios": horarios
    }


@router.get("/status/{status}")
def get_horarios_por_status(status: StatusHorario):
    horarios = listar_horarios_por_status(status.value)

    if not horarios:
        raise HTTPException(
            status_code=404,
            detail="Nenhum horário encontrado para esse status"
        )

    return {
        "status": status.value,
        "total": len(horarios),
        "horarios": horarios
    }


@router.post("/")
def post_horario(novo_horario: HorarioCreate):
    try:
        horario = criar_horario(
            novo_horario.model_dump(mode="json", exclude_none=True)
        )

        return {
            "mensagem": "Horário criado com sucesso",
            "horario": horario
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.put("/id/{horario_id}")
def put_horario(horario_id: str, novos_dados: HorarioUpdate):
    try:
        horario = atualizar_horario(
            horario_id,
            novos_dados.model_dump(mode="json", exclude_none=True)
        )

        if not horario:
            raise HTTPException(
                status_code=404,
                detail="Horário não encontrado"
            )

        return {
            "mensagem": "Horário atualizado com sucesso",
            "horario": horario
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.patch("/id/{horario_id}/status/{status}")
def patch_status_horario(horario_id: str, status: StatusHorario):
    try:
        horario = alterar_status_horario(horario_id, status.value)

        if not horario:
            raise HTTPException(
                status_code=404,
                detail="Horário não encontrado"
            )

        return {
            "mensagem": "Status do horário alterado com sucesso",
            "horario": horario
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.delete("/id/{horario_id}")
def delete_horario(horario_id: str):
    horario = deletar_horario(horario_id)

    if not horario:
        raise HTTPException(
            status_code=404,
            detail="Horário não encontrado"
        )

    return {
        "mensagem": "Horário deletado com sucesso",
        "horario": horario
    }