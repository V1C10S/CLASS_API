from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from enum import Enum

from crud.alunos import (
    listar_alunos,
    buscar_aluno_por_ra,
    buscar_aluno_por_email,
    listar_alunos_por_turma,
    listar_alunos_por_curso,
    listar_alunos_por_ano,
    listar_alunos_por_periodo,
    listar_alunos_por_turno,
    listar_alunos_por_status,
    buscar_alunos_por_termo,
    criar_aluno,
    atualizar_aluno,
    alterar_status_aluno,
    deletar_aluno
)


router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)


class AlunoCreate(BaseModel):
    nome: str
    turma_id: str
    email: str
    curso: str
    ano: int
    periodo: str
    status: Optional[str] = "ativo"


class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    turma_id: Optional[str] = None
    email: Optional[str] = None
    curso: Optional[str] = None
    ano: Optional[int] = None
    periodo: Optional[str] = None
    turno: Optional[str] = None
    status: Optional[str] = None

class StatusAluno(str, Enum):
    ativo = "ativo"
    trancado = "trancado"
    inativo = "inativo"

class StatusUpdate(BaseModel):
    status: StatusAluno

@router.get("/")
def get_alunos():
    alunos = listar_alunos()

    return {
        "total": len(alunos),
        "alunos": alunos
    }


@router.get("/search/{termo}")
def search_alunos(termo: str):
    alunos = buscar_alunos_por_termo(termo)

    if not alunos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum aluno encontrado para esse termo"
        )

    return {
        "termo": termo,
        "total": len(alunos),
        "alunos": alunos
    }


@router.get("/ra/{ra}")
def get_aluno_por_ra(ra: str):
    aluno = buscar_aluno_por_ra(ra)

    if not aluno:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )

    return aluno


@router.get("/email/{email}")
def get_aluno_por_email(email: str):
    aluno = buscar_aluno_por_email(email)

    if not aluno:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )

    return aluno


@router.get("/turma/{turma_id}")
def get_alunos_por_turma(turma_id: str):
    alunos = listar_alunos_por_turma(turma_id)

    if not alunos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum aluno encontrado para essa turma"
        )

    return {
        "turma_id": turma_id.upper(),
        "total": len(alunos),
        "alunos": alunos
    }


@router.get("/curso/{curso}")
def get_alunos_por_curso(curso: str):
    alunos = listar_alunos_por_curso(curso)

    if not alunos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum aluno encontrado para esse curso"
        )

    return {
        "curso": curso.upper(),
        "total": len(alunos),
        "alunos": alunos
    }


@router.get("/ano/{ano}")
def get_alunos_por_ano(ano: int):
    alunos = listar_alunos_por_ano(ano)

    if not alunos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum aluno encontrado para esse ano"
        )

    return {
        "ano": ano,
        "total": len(alunos),
        "alunos": alunos
    }


@router.get("/periodo/{periodo}")
def get_alunos_por_periodo(periodo: str):
    alunos = listar_alunos_por_periodo(periodo)

    if not alunos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum aluno encontrado para esse período"
        )

    return {
        "periodo": periodo,
        "total": len(alunos),
        "alunos": alunos
    }


@router.get("/turno/{turno}")
def get_alunos_por_turno(turno: str):
    alunos = listar_alunos_por_turno(turno)

    if not alunos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum aluno encontrado para esse turno"
        )

    return {
        "turno": turno.upper(),
        "total": len(alunos),
        "alunos": alunos
    }


@router.get("/status/{status}")
def get_alunos_por_status(status: str):
    alunos = listar_alunos_por_status(status)

    if not alunos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum aluno encontrado para esse status"
        )

    return {
        "status": status.lower(),
        "total": len(alunos),
        "alunos": alunos
    }


@router.post("/")
def post_aluno(novo_aluno: AlunoCreate):
    try:
        aluno = criar_aluno(novo_aluno.model_dump(exclude_none=True))

        return {
            "mensagem": "Aluno criado com sucesso",
            "aluno": aluno
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.put("/ra/{ra}")
def put_aluno(ra: str, novos_dados: AlunoUpdate):
    try:
        aluno = atualizar_aluno(
            ra,
            novos_dados.model_dump(exclude_none=True)
        )

        if not aluno:
            raise HTTPException(
                status_code=404,
                detail="Aluno não encontrado"
            )

        return {
            "mensagem": "Aluno atualizado com sucesso",
            "aluno": aluno
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.patch("/ra/{ra}/status/{status}")
def patch_status_aluno_opcao(ra: str, status: StatusAluno):
    try:
        aluno = alterar_status_aluno(ra, status.value)

        if not aluno:
            raise HTTPException(
                status_code=404,
                detail="Aluno não encontrado"
            )

        return {
            "mensagem": "Status do aluno alterado com sucesso",
            "aluno": aluno
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )


@router.delete("/ra/{ra}")
def delete_aluno(ra: str):
    aluno = deletar_aluno(ra)

    if not aluno:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )

    return {
        "mensagem": "Aluno deletado com sucesso",
        "aluno": aluno
    }