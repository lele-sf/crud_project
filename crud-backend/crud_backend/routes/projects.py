from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from crud_backend.database import get_session
from crud_backend.models.clients import Client
from crud_backend.models.projects import Project
from crud_backend.schemas.projects import (
    FilterProject,
    ProjectList,
    ProjectPublic,
    ProjectSchema,
    ProjectUpdate,
)
from crud_backend.schemas.schemas import Message

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED, response_model=ProjectPublic)
def create_project(
    client_id: int, project: ProjectSchema, session: Session = Depends(get_session)
) -> ProjectPublic:
    """Cria um novo projeto."""
    db_client = session.scalar(select(Client).where(Client.id == client_id))
    if not db_client:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Client not found")

    project_data = project.model_dump()
    project_data["client_id"] = client_id
    db_project = Project(**project_data)

    session.add(db_project)
    session.commit()
    session.refresh(db_project)

    return ProjectPublic.model_validate(db_project)


@router.get("/", response_model=ProjectList)
def list_projects(
    client_id: int,
    project_filter: Annotated[FilterProject, Query()],
    session: Session = Depends(get_session),
) -> ProjectList:
    """Recupera uma lista de projetos com paginação."""
    db_client = session.scalar(select(Client).where(Client.id == client_id))
    if not db_client:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Client not found")

    query = select(Project).where(Project.client_id == client_id)

    if project_filter.title:
        query = query.filter(Project.title.contains(project_filter.title))

    if project_filter.description:
        query = query.filter(Project.description.contains(project_filter.description))

    if project_filter.status:
        query = query.filter(Project.status == project_filter.status)

    total = session.scalar(select(func.count()).select_from(query.subquery()))

    projects = session.scalars(
        query.offset(project_filter.offset).limit(project_filter.limit)
    ).all()

    project_public_list = [
        ProjectPublic.model_validate(project) for project in projects
    ]

    return ProjectList(projects=project_public_list, total=total)


@router.get("/{project_id}", response_model=ProjectPublic)
def read_project(
    client_id: int, project_id: int, session: Session = Depends(get_session)
) -> ProjectPublic:
    """Recupera um projeto específico pelo ID."""
    db_client = session.scalar(select(Client).where(Client.id == client_id))
    if not db_client:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Client not found")

    db_project = session.scalar(
        select(Project).where(Project.id == project_id, Project.client_id == client_id)
    )
    if not db_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Project not found"
        )

    return ProjectPublic.model_validate(db_project)


@router.patch("/{project_id}", response_model=ProjectPublic)
def patch_project(
    client_id: int,
    project: ProjectUpdate,
    project_id: int,
    session: Session = Depends(get_session),
) -> ProjectPublic:
    """Atualiza um projeto existente."""
    db_client = session.scalar(select(Client).where(Client.id == client_id))
    if not db_client:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Client not found")

    db_project = session.scalar(
        select(Project).where(Project.client_id == client_id, Project.id == project_id)
    )

    if not db_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Project not found"
        )

    for key, value in project.model_dump(exclude_unset=True).items():
        setattr(db_project, key, value)

    session.add(db_project)
    session.commit()
    session.refresh(db_project)

    return ProjectPublic.model_validate(db_project)


@router.delete("/{project_id}", response_model=Message)
def delete_project(
    project_id: int, client_id: int, session: Session = Depends(get_session)
) -> Message:
    """Remove um projeto pelo ID."""
    db_client = session.scalar(select(Client).where(Client.id == client_id))
    if not db_client:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Client not found")

    project = session.scalar(
        select(Project).where(Project.client_id == client_id, Project.id == project_id)
    )

    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Project not found"
        )

    session.delete(project)
    session.commit()

    return Message(message="Project deleted successfully")
