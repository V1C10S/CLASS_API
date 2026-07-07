from fastapi import APIRouter

router = APIRouter(
    prefix="/grade",
    tags=["Grade"]
)


@router.get("/")
def montar_grade():
    return {
        "message": "Rota de grade funcionando"
    }