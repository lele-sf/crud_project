from datetime import datetime
from pydantic import BaseModel

from crud_backend.models.tasks import TaskStatus
from crud_backend.schemas.schemas import FilterPage


class TaskSchema(BaseModel):
    title: str
    description: str
    status: TaskStatus
    assigned_to: str


class TaskPublic(TaskSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    tasks: list[TaskPublic]


class FilterTasks(FilterPage):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    assigned_to: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    assigned_to: str | None = None
