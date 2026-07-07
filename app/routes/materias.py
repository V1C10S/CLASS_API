from enum import Enum
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from crud.materias import (
    listar_materias,
    buscar_materia_por_codigo,
    listar_materias_por_curso,
    listar_materias_por_semestre,
    listar_materias_por_curso_e_semestre,
    listar_materias_por_status,
    buscar_materias_por_termo,
    criar_materia,
    atualizar_materia,
    alterar_status_materia,
    deletar_materia
)


router = APIRouter(
    prefix="/materias",
    tags=["Matérias"]
)


class StatusMateria(str, Enum):
    ativa = "ativa"
    cancelada = "cancelada"


class MateriaCreate(BaseModel):
    nome: str
    curso: str
    semestre: int
    carga_horaria: Optional[int] = 80
    status: Optional[StatusMateria] = StatusMateria.ativa


class MateriaUpdate(BaseModel):
    nome: Optional[str] = None
    curso: Optional[str] = None
    semestre: Optional[int] = None
    carga_horaria: Optional[int] = None
    status: Optional[StatusMateria] = None


@router.get("/")
def get_materias():
    materias = listar_materias()

    return {
        "total": len(materias),
        "materias": materias
    }


@router.get("/search/{termo}")
def search_materias(termo: str):
    materias = buscar_materias_por_termo(termo)

    if not materias:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma matéria encontrada para esse termo"
        )

    return {
        "termo": termo,
        "total": len(materias),
        "materias": materias
    }


@router.get("/codigo/{codigo}")
def get_materia_por_codigo(codigo: str):
    materia = buscar_materia_por_codigo(codigo)

    if not materia:
        raise HTTPException(
            status_code=404,
            detail="Matéria não encontrada"
        )

    return materia


@router.get("/curso/{curso}")
def get_materias_por_curso(curso: str):
    materias = listar_materias_por_curso(curso)

    if not materias:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma matéria encontrada para esse curso"
        )

    return {
        "curso": curso.upper(),
        "total": len(materias),
        "materias": materias
    }


@router.get("/semestre/{semestre}")
def get_materias_por_semestre(semestre: int):
    materias = listar_materias_por_semestre(semestre)

    if not materias:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma matéria encontrada para esse semestre"
        )

    return {
        "semestre": semestre,
        "total": len(materias),
        "materias": materias
    }


@router.get("/curso/{curso}/semestre/{semestre}")
def get_materias_por_curso_e_semestre(curso: str, semestre: int):
    materias = listar_materias_por_curso_e_semestre(curso, semestre)

    if not materias:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma matéria encontrada para esse curso e semestre"
        )

    return {
        "curso": curso.upper(),
        "semestre": semestre,
        "total": len(materias),
        "materias": materias
    }


@router.get("/status/{status}")
def get_materias_por_status(status: StatusMateria):
    materias = listar_materias_por_status(status.value)

    if not materias:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma matéria encontrada para esse status"
        )

    return {
        "status": status.value,
        "total": len(materias),
        "materias": materias
    }


@router.post("/")
def post_materia(nova_materia: MateriaCreate):
    try:
        materia = criar_materia(
            nova_materia.model_dump(mode="json", exclude_none=True)
        )

        return {
            "mensagem": "Matéria criada com sucesso",
            "materia": materia
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.put("/codigo/{codigo}")
def put_materia(codigo: str, novos_dados: MateriaUpdate):
    try:
        materia = atualizar_materia(
            codigo,
            novos_dados.model_dump(mode="json", exclude_none=True)
        )

        if not materia:
            raise HTTPException(
                status_code=404,
                detail="Matéria não encontrada"
            )

        return {
            "mensagem": "Matéria atualizada com sucesso",
            "materia": materia
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.patch("/codigo/{codigo}/status/{status}")
def patch_status_materia(codigo: str, status: StatusMateria):
    try:
        materia = alterar_status_materia(codigo, status.value)

        if not materia:
            raise HTTPException(
                status_code=404,
                detail="Matéria não encontrada"
            )

        return {
            "mensagem": "Status da matéria alterado com sucesso",
            "materia": materia
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.delete("/codigo/{codigo}")
def delete_materia(codigo: str):
    materia = deletar_materia(codigo)

    if not materia:
        raise HTTPException(
            status_code=404,
            detail="Matéria não encontrada"
        )

    return {
        "mensagem": "Matéria deletada com sucesso",
        "materia": materia
    }