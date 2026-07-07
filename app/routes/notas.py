from fastapi import APIRouter

router = APIRouter(
    prefix="/notas",
    tags=["Notas"]
)


@router.get("/")
def listar_notas():
    return {
        "message": "Rota de notas funcionando"
    }