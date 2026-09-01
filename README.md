# CLASS_API

Uma API REST para gestão acadêmica.

O projeto reproduz o núcleo de um sistema acadêmico por meio da implementação de operações CRUD, rotas específicas e regras de negócio para cada entidade.

A base de dados sintética contém 40 cursos, sendo 10 por área — TI, Medicina, Exatas e Economia. Os cursos possuem duração de 5 a 12 semestres e turmas com 40 alunos por padrão.

## STACK

| Tecnologia | Aplicação |
|---|---|
| FastAPI | Framework web |
| Pydantic v2 | Validação e schemas |
| Uvicorn | Servidor ASGI |
| JSON | Persistência dos dados |
| Python 3.11+ | Linguagem |

## ESTRUTURA

<pre>
CLASS_API/
├── README.md
└── app/
    ├── app.py
    ├── routes/
    │   ├── alunos.py
    │   ├── cursos.py
    │   ├── grade.py
    │   ├── horarios.py
    │   ├── materias.py
    │   ├── notas.py
    │   └── turmas.py
    ├── crud/
    │   ├── alunos.py
    │   ├── cursos.py
    │   ├── grade.py
    │   ├── horarios.py
    │   ├── materias.py
    │   ├── notas.py
    │   └── turmas.py
    ├── scripts/
    └── data/
</pre>

O projeto segue o fluxo:

<pre>
Requisição → routes → crud → data
</pre>

- `routes/`: endpoints e validação dos dados;
- `crud/`: operações CRUD e regras de negócio;
- `scripts/`: geração dos dados sintéticos;
- `data/`: armazenamento em arquivos JSON.

## USO

Clone o repositório e prepare o ambiente:

<pre>
git clone https://github.com/V1C10S/CLASS_API.git
cd CLASS_API

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install fastapi uvicorn
cd app
</pre>

Gere a base de dados:

<pre>
python scripts/criar_cursos.py
python scripts/criar_turmas.py
python scripts/criar_alunos.py
python scripts/criar_materias.py
python scripts/criar_horarios.py
python scripts/criar_notas.py
</pre>

Inicie a API:

<pre>
uvicorn app:app --reload
</pre>

## DOCUMENTAÇÃO

Com a API em execução:

- [Swagger UI](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)
- [Health check](http://127.0.0.1:8000/health)
