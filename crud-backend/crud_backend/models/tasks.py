from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crud_backend.models.registry import table_registry


class TaskStatus(str, Enum):
    """Representa o status da tarefa."""
    pending = "pending"
    doing = "doing"
    completed = "completed"
    paused = "paused"
    deleted = "deleted"


@table_registry.mapped_as_dataclass
class Task:
    """Representa a tarefa no banco de dados."""
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    assigned_to: Mapped[str]
    status: Mapped[TaskStatus]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

    project: Mapped["Project"] = relationship(init=False, back_populates="tasks")


from crud_backend.models.projects import Project  # noqa
