# CRUD Backend

Backend desenvolvido com **FastAPI** para gerenciar **clients**, **tasks** e **projects**. Utiliza **Docker**, **Poetry** e **Alembic**.


## Como Rodar

1. **Clone o repositório**:
   ```bash
   git clone https://leticiafernandes1@bitbucket.org/agnesprojects/crud-bakcend.git
   ```

2. **Instale as dependências**:
    ```bash
    poetry install
    ```

## Configuração do banco de dados
1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
    ```bash
    POSTGRES_USER=seu_usuario
    POSTGRES_DB=seu_banco
    POSTGRES_PASSWORD=sua_senha
    DATABASE_URL=postgresql://seu_usuario:sua_senha@crud_database:5432/seu_banco
    ```
2. Rode as migrações:

    ```bash
    poetry run alembic upgrade head
    ```

## Como rodar os testes?
1. Execute os testes:
    ```bash
    poetry run task test
    ```

## Como rodar a aplicação?
1. Inicie o servidor localmente:
    ```bash
    poetry run task run
    ```
2. Acesse a API em http://localhost:8000.