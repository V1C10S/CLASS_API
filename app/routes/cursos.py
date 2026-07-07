from fastapi import APIRouter, HTTPException

from crud.cursos import (
    listar_cursos,
    listar_areas,
    listar_cursos_por_area,
    buscar_curso_por_nome,
    buscar_curso_por_sigla,
    buscar_cursos_por_termo
)


router = APIRouter(
    prefix="/cursos",
    tags=["Cursos"]
)


@router.get("/")
def get_cursos():
    cursos = listar_cursos()

    return {
        "total": len(cursos),
        "cursos": cursos
    }


@router.get("/areas")
def get_areas():
    areas = listar_areas()

    return {
        "total": len(areas),
        "areas": areas
    }


@router.get("/area/{area}")
def get_cursos_por_area(area: str):
    cursos = listar_cursos_por_area(area)

    if not cursos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum curso encontrado nessa área"
        )

    return {
        "area": area,
        "total": len(cursos),
        "cursos": cursos
    }


@router.get("/sigla/{sigla}")
def get_curso_por_sigla(sigla: str):
    curso = buscar_curso_por_sigla(sigla)

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso não encontrado"
        )

    return curso


@router.get("/nome/{nome_curso}")
def get_curso_por_nome(nome_curso: str):
    curso = buscar_curso_por_nome(nome_curso)

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso não encontrado"
        )

    return curso

@router.get("/search/{termo}")
def search_cursos(termo: str):
    cursos = buscar_cursos_por_termo(termo)

    if not cursos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum curso encontrado para esse termo"
        )

    return {
        "termo": termo,
        "total": len(cursos),
        "cursos": cursos
    }