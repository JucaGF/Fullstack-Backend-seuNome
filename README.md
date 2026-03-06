# Full Stack - Backend

## Tarefa

Implementar um `CRUD` em FastAPI.

| Letra | Descrição | Implementado |
| --- | --- | --- |
| C | Create | :white_check_mark: |
| R | Read (All) | :white_check_mark: |
| R | Read (id_users) | :white_check_mark: |
| U | Update | :white_check_mark: |
| D | Delete | :white_check_mark: |

## Comandos Úteis

### Clone o repositório

```bash
git clone <url-do-repositorio>
cd <nome-da-pasta>
```

### Crie um ambiente virtual (recomendado)

#### Linux / Mac

```bash
python -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Instalar bibliotecas

```
pip install fastapi uvicorn

```

### Executar o servidor

```bash
uvicorn main:app --reload
```

O servidor iniciará em:

```
http://127.0.0.1:8000
```

## Referências

- [Slide](https://www.canva.com/design/DAG__eOlTbA/M6jAKkXBcXzS1zproSq3UA/edit?utm_content=DAG__eOlTbA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
  
- [Artigo Medium](https://medium.com/@guilhermehuther/back-end-basics-e9a2ed1f244a)
  
- [Postman - Vizualizar funcionamento da API](https://learning.postman.com/)

- [SQLite Viewer - Florian Klampfer](https://marketplace.visualstudio.com/items/?itemName=qwtel.sqlite-viewer)

- [Documentação FastAPI](https://fastapi.tiangolo.com/)

- [Documentação sqllite](https://docs.python.org/3/library/sqlite3.html)

- [HTTP/HTTPS](http://developer.mozilla.org/pt-BR/docs/Web/HTTP)
