from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel

from sqllite import run_sql

#função lifespan define uma função de ciclo de vida de uma API, no caso ela vai executar um código específico sempre que a API foi inicializada e sempre que ela for encerrada
#O bloco de código que vem antes do yield é a parte que é executada quando é inicializada e o que vem depois do yield é quando encerrada(nesse caso nada acontece quando ela é encerrada por que não tem nada)
#Essa função executar a função run_sql que está no arquivo de banco e manda como argumento um código SQL que cria o banco se ele não existir e se já existir não faz nada
@asynccontextmanager
async def lifespan(app: FastAPI):
    run_sql(
        """
        CREATE TABLE IF NOT EXISTS users (
            id_users            SERIAL PRIMARY KEY,
            password_users      VARCHAR(255) NOT NULL,
            name_users          VARCHAR(255) NOT NULL,
            email_users         VARCHAR(255) NOT NULL
        )
        """
    )
    yield


# Cria a aplicação FastAPI e registra o lifespan
app = FastAPI(lifespan=lifespan)


#Middleware de CORS permite que outros processos rodando em outras portas acessem a API, por exemplo o frontend rodando em http://localhost:3000 poder acessar uma API que está rodando em http://localhost:8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router é uma forma de organizar rotas separadas do app principal
router = APIRouter()

#Modelo do Pydantic que define como deve ser o JSON no corpo da requisição, para mais informações pesquise sobre Pydantic e BaseModel
class User(BaseModel):
    password_users: str
    name_users: str
    email_users: str

#Rota que excuta método GET
@router.get("/")
def get_users():
    #Executa uma query que busca todos os usuários da tabela users
    return run_sql("SELECT * FROM users")

#Rota que executa método POST
@router.post("/users")
def create_users(body: User):
    
    # Extraindo dados do body(Seguindo o padrão definido pelo BaseModel)
    password_users, name_users, email_users = body.password_users, body.name_users, body.email_users

    #Executa uma query que cadastro um novo usuário no banco
    return run_sql(
        f"""
            INSERT INTO users(password_users, name_users, email_users) 
            VALUES('{password_users}', '{name_users}', '{email_users}')
        """
    )

#Registra as rotas dentro do app
app.include_router(router=router)
