from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crud_backend.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Client:
    """Representa o cliente no banco de dados."""
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    company: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    projects: Mapped[list["Project"]] = relationship(
        init=False, back_populates="client"
    )


from crud_backend.models.projects import Project  # noqa
