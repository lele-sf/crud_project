from datetime import datetime
from pydantic import BaseModel

from crud_backend.models.projects import ProjectStatus
from crud_backend.schemas.schemas import FilterPage


class ProjectSchema(BaseModel):
    title: str
    description: str
    status: ProjectStatus


class ProjectPublic(ProjectSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectList(BaseModel):
    projects: list[ProjectPublic]
    total: int | None


class FilterProject(FilterPage):
    title: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None
