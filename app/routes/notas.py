from enum import Enum
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from crud.notas import (
    listar_notas,
    buscar_nota_por_id,
    buscar_nota_por_ra_e_materia,
    listar_notas_por_ra,
    listar_notas_por_turma,
    listar_notas_por_materia,
    listar_notas_por_curso,
    listar_notas_por_semestre,
    listar_notas_por_status,
    listar_notas_por_ra_e_semestre,
    listar_notas_por_ra_e_status,
    criar_nota,
    atualizar_nota,
    lancar_nota_1,
    lancar_nota_2,
    deletar_nota
)


router = APIRouter(
    prefix="/notas",
    tags=["Notas"]
)


class StatusNota(str, Enum):
    pendente = "pendente"
    aprovado = "aprovado"
    reprovado = "reprovado"


class NotaCreate(BaseModel):
    ra: str
    codigo_materia: str
    nota_1: Optional[float] = None
    nota_2: Optional[float] = None


class NotaUpdate(BaseModel):
    ra: Optional[str] = None
    codigo_materia: Optional[str] = None
    nota_1: Optional[float] = None
    nota_2: Optional[float] = None


class NotaValor(BaseModel):
    valor: float


@router.get("/")
def get_notas():
    notas = listar_notas()

    return {
        "total": len(notas),
        "notas": notas
    }


@router.get("/id/{nota_id}")
def get_nota_por_id(nota_id: str):
    nota = buscar_nota_por_id(nota_id)

    if not nota:
        raise HTTPException(
            status_code=404,
            detail="Nota não encontrada"
        )

    return nota


@router.get("/ra/{ra}/materia/{codigo_materia}")
def get_nota_por_ra_e_materia(ra: str, codigo_materia: str):
    nota = buscar_nota_por_ra_e_materia(ra, codigo_materia)

    if not nota:
        raise HTTPException(
            status_code=404,
            detail="Nota não encontrada para esse RA e matéria"
        )

    return nota


@router.get("/ra/{ra}/semestre/{semestre}")
def get_notas_por_ra_e_semestre(ra: str, semestre: int):
    notas = listar_notas_por_ra_e_semestre(ra, semestre)

    if not notas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma nota encontrada para esse RA e semestre"
        )

    return {
        "ra": ra,
        "semestre": semestre,
        "total": len(notas),
        "notas": notas
    }


@router.get("/ra/{ra}/status/{status}")
def get_notas_por_ra_e_status(ra: str, status: StatusNota):
    notas = listar_notas_por_ra_e_status(ra, status.value)

    if not notas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma nota encontrada para esse RA e status"
        )

    return {
        "ra": ra,
        "status": status.value,
        "total": len(notas),
        "notas": notas
    }


@router.get("/ra/{ra}")
def get_notas_por_ra(ra: str):
    notas = listar_notas_por_ra(ra)

    if not notas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma nota encontrada para esse RA"
        )

    return {
        "ra": ra,
        "total": len(notas),
        "notas": notas
    }


@router.get("/turma/{turma_id}")
def get_notas_por_turma(turma_id: str):
    notas = listar_notas_por_turma(turma_id)

    if not notas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma nota encontrada para essa turma"
        )

    return {
        "turma_id": turma_id.upper(),
        "total": len(notas),
        "notas": notas
    }


@router.get("/materia/{codigo_materia}")
def get_notas_por_materia(codigo_materia: str):
    notas = listar_notas_por_materia(codigo_materia)

    if not notas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma nota encontrada para essa matéria"
        )

    return {
        "codigo_materia": codigo_materia.upper(),
        "total": len(notas),
        "notas": notas
    }


@router.get("/curso/{curso}")
def get_notas_por_curso(curso: str):
    notas = listar_notas_por_curso(curso)

    if not notas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma nota encontrada para esse curso"
        )

    return {
        "curso": curso.upper(),
        "total": len(notas),
        "notas": notas
    }


@router.get("/semestre/{semestre}")
def get_notas_por_semestre(semestre: int):
    notas = listar_notas_por_semestre(semestre)

    if not notas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma nota encontrada para esse semestre"
        )

    return {
        "semestre": semestre,
        "total": len(notas),
        "notas": notas
    }


@router.get("/status/{status}")
def get_notas_por_status(status: StatusNota):
    notas = listar_notas_por_status(status.value)

    if not notas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma nota encontrada para esse status"
        )

    return {
        "status": status.value,
        "total": len(notas),
        "notas": notas
    }


@router.post("/")
def post_nota(nova_nota: NotaCreate):
    try:
        nota = criar_nota(
            nova_nota.model_dump(exclude_none=True)
        )

        return {
            "mensagem": "Nota criada com sucesso",
            "nota": nota
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.put("/id/{nota_id}")
def put_nota(nota_id: str, novos_dados: NotaUpdate):
    try:
        nota = atualizar_nota(
            nota_id,
            novos_dados.model_dump(exclude_none=True)
        )

        if not nota:
            raise HTTPException(
                status_code=404,
                detail="Nota não encontrada"
            )

        return {
            "mensagem": "Nota atualizada com sucesso",
            "nota": nota
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.patch("/id/{nota_id}/nota-1")
def patch_nota_1(nota_id: str, dados: NotaValor):
    try:
        nota = lancar_nota_1(nota_id, dados.valor)

        if not nota:
            raise HTTPException(
                status_code=404,
                detail="Nota não encontrada"
            )

        return {
            "mensagem": "Nota 1 lançada com sucesso",
            "nota": nota
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.patch("/id/{nota_id}/nota-2")
def patch_nota_2(nota_id: str, dados: NotaValor):
    try:
        nota = lancar_nota_2(nota_id, dados.valor)

        if not nota:
            raise HTTPException(
                status_code=404,
                detail="Nota não encontrada"
            )

        return {
            "mensagem": "Nota 2 lançada com sucesso",
            "nota": nota
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.delete("/id/{nota_id}")
def delete_nota(nota_id: str):
    nota = deletar_nota(nota_id)

    if not nota:
        raise HTTPException(
            status_code=404,
            detail="Nota não encontrada"
        )

    return {
        "mensagem": "Nota deletada com sucesso",
        "nota": nota
    }