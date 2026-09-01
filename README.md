# CLASS_API


Uma API REST para gestão acadêmica.
O projeto reproduz o núcleo de um sistema acadêmico, com entidades, rotas e regras de negócio próprias. Seu desenvolvimento envolveu a construção de operações CRUD para alunos, matérias, horários e notas, além de consultas de cursos, turmas e grades curriculares.
A base de dados sintética contém 40 cursos, divididos entre as áreas de TI, Medicina, Exatas e Economia. Os cursos possuem duração de 5 a 12 semestres e turmas com 40 alunos por padrão.


## STACK


| Tecnologia | Aplicação |
|---|---|
| FastAPI | Framework web |
| Pydantic v2 | Validação e schemas |
| Uvicorn | Servidor ASGI |
| JSON | Persistência dos dados |
| Python 3.11+ | Linguagem |


## ESTRUTURA


CLASS_API/

└── app/
    ├── routes/   
    ├── crud/
    ├── scripts/    
    ├── data/
    └── app.py

## USO

git clone https://github.com/V1C10S/CLASS_API.git
cd CLASS_API

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install fastapi uvicorn

cd app

Para gerar a base de dados:

python scripts/criar_cursos.py
python scripts/criar_turmas.py
python scripts/criar_alunos.py
python scripts/criar_materias.py
python scripts/criar_horarios.py
python scripts/criar_notas.py

Inicie a API:

uvicorn app:app --reload


## ENDPOINTS


Com a API em execução:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health
