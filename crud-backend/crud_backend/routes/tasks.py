from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy import select
from sqlalchemy.orm import Session

from crud_backend.models.tasks import Task
from crud_backend.models.projects import Project
from crud_backend.schemas.schemas import Message
from crud_backend.schemas.tasks import (
    TaskSchema,
    TaskUpdate,
    TaskPublic,
    TaskList,
    FilterTasks,
)
from crud_backend.database import get_session


router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED, response_model=TaskPublic)
def create_task(
    project_id: int, task: TaskSchema, session: Session = Depends(get_session)
) -> TaskPublic:
    """Cria uma nova tarefa."""
    db_project = session.scalar(select(Project).where(Project.id == project_id))
    if not db_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Project not found"
        )

    task_data = task.model_dump()
    task_data["project_id"] = project_id
    db_task = Task(**task_data)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return TaskPublic.model_validate(db_task)


@router.get("/", response_model=TaskList)
def list_tasks(
    project_id: int,
    task_filter: Annotated[FilterTasks, Query()],
    session: Session = Depends(get_session),
) -> TaskList:
    """Recupera uma lista de tarefas com paginação."""
    db_project = session.scalar(select(Project).where(Project.id == project_id))
    if not db_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Project not found"
        )

    query = session.query(Task).filter(Task.project_id == project_id)

    if task_filter.title:
        query = query.filter(Task.title.contains(task_filter.title))

    if task_filter.description:
        query = query.filter(Task.description.contains(task_filter.description))

    if task_filter.status:
        query = query.filter(Task.status == task_filter.status)

    if task_filter.assigned_to:
        query = query.filter(Task.assigned_to.contains(task_filter.assigned_to))

    tasks = session.scalars(
        query.offset(task_filter.offset).limit(task_filter.limit)
    ).all()

    task_public_list = [TaskPublic.model_validate(task) for task in tasks]

    return TaskList(tasks=task_public_list)


@router.get("/{task_id}", response_model=TaskPublic)
def read_task(
    project_id: int, task_id: int, session: Session = Depends(get_session)
) -> TaskPublic:
    """Recupera uma tarefa específica pelo ID."""
    db_project = session.scalar(select(Project).where(Project.id == project_id))
    if not db_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Project not found"
        )

    db_task = session.scalar(
        select(Task).where(Task.id == task_id, Task.project_id == project_id)
    )
    if not db_task:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")

    return TaskPublic.model_validate(db_task)


@router.patch("/{task_id}", response_model=TaskPublic)
def patch_task(
    project_id: int,
    task_id: int,
    task: TaskUpdate,
    session: Session = Depends(get_session),
) -> TaskPublic:
    """Atualiza uma tarefa existente."""
    db_project = session.scalar(select(Project).where(Project.id == project_id))
    if not db_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Project not found"
        )

    db_task = session.scalar(
        select(Task).where(Task.project_id == project_id, Task.id == task_id)
    )
    if not db_task:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return TaskPublic.model_validate(db_task)


@router.delete("/{task_id}", response_model=Message)
def delete_task(
    project_id: int, task_id: int, session: Session = Depends(get_session)
) -> Message:
    """Remove uma tarefa pelo ID."""
    db_project = session.scalar(select(Project).where(Project.id == project_id))
    if not db_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Project not found"
        )

    db_task = session.scalar(
        select(Task).where(Task.project_id == project_id, Task.id == task_id)
    )
    if not db_task:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")

    session.delete(db_task)
    session.commit()

    return Message(message="Task deleted successfully")
