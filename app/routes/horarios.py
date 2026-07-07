from fastapi import APIRouter

router = APIRouter(
    prefix="/horarios",
    tags=["Horarios"]
)


@router.get("/")
def listar_horarios():
    return {
        "message": "Rota de horarios funcionando"
    }