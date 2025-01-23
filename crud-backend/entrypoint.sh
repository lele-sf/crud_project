#!/bin/sh

# Executa as migrações do banco de dados
poetry run alembic upgrade head

# Inicia a aplicação
poetry run fastapi run crud_backend/main.py --host 0.0.0.0