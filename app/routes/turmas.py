from fastapi import APIRouter, HTTPException

from crud.turmas import (
    listar_turmas,
    buscar_turma_por_id,
    listar_turmas_por_curso,
    listar_turmas_por_ano,
    listar_turmas_por_entrada,
    listar_turmas_por_periodo,
    listar_turmas_por_status,
    buscar_turmas_por_termo
)


router = APIRouter(
    prefix="/turmas",
    tags=["Turmas"]
)


@router.get("/")
def get_turmas():
    turmas = listar_turmas()

    return {
        "total": len(turmas),
        "turmas": turmas
    }


@router.get("/search/{termo}")
def search_turmas(termo: str):
    turmas = buscar_turmas_por_termo(termo)

    if not turmas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma turma encontrada para esse termo"
        )

    return {
        "termo": termo,
        "total": len(turmas),
        "turmas": turmas
    }


@router.get("/curso/{curso_sigla}")
def get_turmas_por_curso(curso_sigla: str):
    turmas = listar_turmas_por_curso(curso_sigla)

    if not turmas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma turma encontrada para esse curso"
        )

    return {
        "curso_sigla": curso_sigla.upper(),
        "total": len(turmas),
        "turmas": turmas
    }


@router.get("/ano/{ano}")
def get_turmas_por_ano(ano: int):
    turmas = listar_turmas_por_ano(ano)

    if not turmas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma turma encontrada para esse ano"
        )

    return {
        "ano": ano,
        "total": len(turmas),
        "turmas": turmas
    }


@router.get("/entrada/{entrada_semestre}")
def get_turmas_por_entrada(entrada_semestre: int):
    turmas = listar_turmas_por_entrada(entrada_semestre)

    if not turmas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma turma encontrada para esse semestre de entrada"
        )

    return {
        "entrada_semestre": entrada_semestre,
        "total": len(turmas),
        "turmas": turmas
    }


@router.get("/periodo/{periodo}")
def get_turmas_por_periodo(periodo: str):
    turmas = listar_turmas_por_periodo(periodo)

    if not turmas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma turma encontrada para esse período"
        )

    return {
        "periodo": periodo,
        "total": len(turmas),
        "turmas": turmas
    }


@router.get("/status/{status}")
def get_turmas_por_status(status: str):
    turmas = listar_turmas_por_status(status)

    if not turmas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma turma encontrada para esse status"
        )

    return {
        "status": status,
        "total": len(turmas),
        "turmas": turmas
    }


@router.get("/{turma_id}")
def get_turma_por_id(turma_id: str):
    turma = buscar_turma_por_id(turma_id)

    if not turma:
        raise HTTPException(
            status_code=404,
            detail="Turma não encontrada"
        )

    return turma