from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crud_backend.models.registry import table_registry


class ProjectStatus(str, Enum):
    """Representa o status do projeto."""
    pending = "pending"
    doing = "doing"
    completed = "completed"
    paused = "paused"
    deleted = "deleted"


@table_registry.mapped_as_dataclass
class Project:
    """Representa o projeto no banco de dados."""
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[ProjectStatus]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))

    client: Mapped["Client"] = relationship(init=False, back_populates="projects")
    tasks: Mapped[list["Task"]] = relationship(init=False, back_populates="project")


from crud_backend.models.clients import Client  # noqa
from crud_backend.models.tasks import Task  # noqa
