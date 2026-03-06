import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Banco de dados
# ---------------------------------------------------------------------------

def get_db():
    """Abre a conexão com o banco e retorna (con, cur). Feche con ao terminar."""
    con = sqlite3.connect("users.db")
    # row_factory permite acessar colunas pelo nome (ex: row["name_users"])
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return con, cur


def run_sql(sql: str, params: tuple = ()):
    """
    Executa qualquer comando SQL com parâmetros opcionais.

    Usar parâmetros (placeholders '?') em vez de f-strings evita SQL Injection.
    Exemplo seguro:   run_sql("SELECT * FROM users WHERE id_users = ?", (id,))
    Exemplo inseguro: run_sql(f"SELECT * FROM users WHERE id_users = {id}")
    """
    con, cur = get_db()
    try:
        cur.execute(sql, params)
        data = [dict(row) for row in cur.fetchall()]  # converte para lista de dicionários
        con.commit()
        return data
    finally:
        con.close()  # garante que a conexão sempre será fechada


# ---------------------------------------------------------------------------
# Lifespan — executa ao iniciar e encerrar a API
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria a tabela se não existir.
    # SERIAL é sintaxe do PostgreSQL — no SQLite o correto é INTEGER PRIMARY KEY AUTOINCREMENT
    run_sql(
        """
        CREATE TABLE IF NOT EXISTS users (
            id_users        INTEGER PRIMARY KEY AUTOINCREMENT,
            password_users  VARCHAR(255) NOT NULL,
            name_users      VARCHAR(255) NOT NULL,
            email_users     VARCHAR(255) NOT NULL
        )
        """
    )
    yield


# ---------------------------------------------------------------------------
# Aplicação FastAPI
# ---------------------------------------------------------------------------

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()


# ---------------------------------------------------------------------------
# Modelos Pydantic
# ---------------------------------------------------------------------------

class UserBody(BaseModel):
    """Estrutura esperada no corpo das requisições POST e PUT."""
    password_users: int
    name_users: str
    email_users: str


class UserResponse(UserBody):
    """Estrutura retornada nas respostas — inclui o id gerado pelo banco."""
    id_users: int


# ---------------------------------------------------------------------------
# Rotas — CRUD completo
# ---------------------------------------------------------------------------

@router.get("/")
def health():
    return {
        "status": "ok"
    }

@router.get("/users", response_model=list[UserResponse])
def get_users():
    """R — Read All: retorna todos os usuários."""
    return run_sql("SELECT * FROM users")


@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int):
    """R — Read by ID: retorna um usuário pelo id."""
    try:
        result = run_sql("SELECT * FROM users WHERE id_users = ?", (id,))
        return result[0]  # IndexError se a lista vier vazia (usuário não existe)
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com id {id} não encontrado."
        )


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(body: UserBody):
    """C — Create: cadastra um novo usuário e retorna o registro criado."""
    run_sql(
        "INSERT INTO users (password_users, name_users, email_users) VALUES (?, ?, ?)",
        (body.password_users, body.name_users, body.email_users),
    )

    # Busca o registro recém-criado para retornar na resposta
    result = run_sql(
        "SELECT * FROM users WHERE id_users = (SELECT MAX(id_users) FROM users)"
    )
    return result[0]


@router.put("/users/{id}", response_model=UserResponse)
def update_user(id: int, body: UserBody):
    """U — Update: atualiza os dados de um usuário existente."""
    try:
        # Verifica se o usuário existe antes de tentar atualizar
        run_sql("SELECT * FROM users WHERE id_users = ?", (id,))[0]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com id {id} não encontrado."
        )

    run_sql(
        """
        UPDATE users
        SET password_users = ?,
            name_users     = ?,
            email_users    = ?
        WHERE id_users = ?
        """,
        (body.password_users, body.name_users, body.email_users, id),
    )

    return run_sql("SELECT * FROM users WHERE id_users = ?", (id,))[0]


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    """D — Delete: remove um usuário pelo id."""
    try:
        run_sql("SELECT * FROM users WHERE id_users = ?", (id,))[0]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com id {id} não encontrado."
        )

    run_sql("DELETE FROM users WHERE id_users = ?", (id,))


# ---------------------------------------------------------------------------
# Registra o router na aplicação
# ---------------------------------------------------------------------------

app.include_router(router)
