from fastapi import APIRouter, HTTPException

from crud.grade import (
    montar_grade_por_ra,
    montar_grade_por_ra_e_semestre,
    montar_grade_por_turma,
    montar_grade_por_turma_e_semestre
)


router = APIRouter(
    prefix="/grade",
    tags=["Grade"]
)


@router.get("/ra/{ra}")
def get_grade_por_ra(ra: str, somente_ativos: bool = True):
    grade = montar_grade_por_ra(ra, somente_ativos)

    if not grade:
        raise HTTPException(
            status_code=404,
            detail="RA não encontrado"
        )

    return grade


@router.get("/ra/{ra}/semestre/{semestre}")
def get_grade_por_ra_e_semestre(
    ra: str,
    semestre: int,
    somente_ativos: bool = True
):
    grade = montar_grade_por_ra_e_semestre(
        ra,
        semestre,
        somente_ativos
    )

    if not grade:
        raise HTTPException(
            status_code=404,
            detail="RA não encontrado"
        )

    if grade["total"] == 0:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma grade encontrada para esse RA e semestre"
        )

    return grade


@router.get("/turma/{turma_id}")
def get_grade_por_turma(turma_id: str, somente_ativos: bool = True):
    grade = montar_grade_por_turma(turma_id, somente_ativos)

    if grade["total"] == 0:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma grade encontrada para essa turma"
        )

    return grade


@router.get("/turma/{turma_id}/semestre/{semestre}")
def get_grade_por_turma_e_semestre(
    turma_id: str,
    semestre: int,
    somente_ativos: bool = True
):
    grade = montar_grade_por_turma_e_semestre(
        turma_id,
        semestre,
        somente_ativos
    )

    if grade["total"] == 0:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma grade encontrada para essa turma e semestre"
        )

    return grade