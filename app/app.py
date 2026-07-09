from fastapi import FastAPI


# ===== API'S =====


app = FastAPI(title="CLASS_API")


# ===== IMPORTS =====


from routes.alunos import router as alunos_router
from routes.cursos import router as cursos_router
from routes.grade import router as grade_router
from routes.horarios import router as horarios_router
from routes.materias import router as materias_router
from routes.notas import router as notas_router
from routes.turmas import router as turmas_router


# ===== ROUTERS =====


app.include_router(alunos_router)
app.include_router(cursos_router)
app.include_router(grade_router)
app.include_router(horarios_router)
app.include_router(materias_router)
app.include_router(notas_router)
app.include_router(turmas_router)


# ===== CHECKING =====


@app.get("/health")
def health():

    return {"status": "OK"}

@app.get("/")
def back_status():

    return {
        "app": "CLASS_API",
        "status": "A TODO VAPOR"
    }