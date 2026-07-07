from fastapi import APIRouter

router = APIRouter(
    prefix="/escolhas",
    tags=["Escolhas"]
)


@router.get("/")
def listar_escolhas():
    return {
        "message": "Rota de escolhas funcionando"
    }