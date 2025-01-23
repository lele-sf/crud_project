from fastapi import APIRouter, Depends, HTTPException, Query
from http import HTTPStatus
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from crud_backend.schemas.clients import ClientPublic, ClientSchema, ClientList
from crud_backend.schemas.schemas import FilterPage, Message
from crud_backend.database import get_session
from crud_backend.models.clients import Client


router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED, response_model=ClientPublic)
def create_client(
    client: ClientSchema, session: Session = Depends(get_session)
) -> ClientPublic:
    """Cria um novo cliente."""
    db_client_email = session.scalar(select(Client).where(Client.email == client.email))
    if db_client_email:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Email already exists"
        )

    db_client_phone = session.scalar(select(Client).where(Client.phone == client.phone))
    if db_client_phone:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Phone already exists"
        )

    db_client = Client(company=client.company, email=client.email, phone=client.phone)

    session.add(db_client)
    session.commit()
    session.refresh(db_client)

    return ClientPublic.model_validate(db_client)


@router.get("/", response_model=ClientList)
def read_clients(
    filter: Annotated[FilterPage, Query()], session: Session = Depends(get_session)
) -> ClientList:
    """Recupera uma lista de clientes com paginação."""
    clients = session.scalars(select(Client).limit(filter.limit).offset(filter.offset))

    client_public_list = [ClientPublic.model_validate(client) for client in clients]

    return ClientList(clients=client_public_list)


@router.get("/{client_id}", response_model=ClientPublic)
def read_client(
    client_id: int, session: Session = Depends(get_session)
) -> ClientPublic:
    """Recupera um cliente específico pelo ID."""
    db_client = session.scalar(select(Client).where(Client.id == client_id))

    if not db_client:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Client not found")

    return ClientPublic.model_validate(db_client)


@router.patch("/{client_id}", response_model=ClientPublic)
def patch_client(
    client_id: int, client: ClientSchema, session: Session = Depends(get_session)
) -> ClientPublic:
    """Atualiza um cliente existente."""
    db_client = session.scalar(select(Client).where(Client.id == client_id))

    if not db_client:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Client not found")

    try:
        for key, value in client.model_dump(exclude_unset=True).items():
            setattr(db_client, key, value)
        session.commit()
        session.refresh(db_client)

        return ClientPublic.model_validate(db_client)

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Email or Phone already exists"
        )


@router.delete("/{client_id}", response_model=Message)
def delete_client(client_id: int, session: Session = Depends(get_session)) -> Message:
    """Remove um cliente pelo ID."""
    db_client = session.scalar(select(Client).where(Client.id == client_id))

    if not db_client:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Client not found")

    session.delete(db_client)
    session.commit()

    return Message(message="Client deleted!")
