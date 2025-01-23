import pytest
import factory
import factory.fuzzy
from datetime import datetime
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from crud_backend.main import app
from crud_backend.database import get_session
from crud_backend.models.clients import Client
from crud_backend.models.projects import Project, ProjectStatus
from crud_backend.models.registry import table_registry
from crud_backend.models.tasks import Task, TaskStatus


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    company = factory.Sequence(lambda n: f"company-{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.company}@test.com")
    phone = factory.LazyAttribute(lambda obj: f"{obj.company}-phone")


class ProjectFactory(factory.Factory):
    class Meta:
        model = Project

    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    status = factory.fuzzy.FuzzyChoice(ProjectStatus)
    client_id = 1


class TaskFactory(factory.Factory):
    class Meta:
        model = Task

    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    status = factory.fuzzy.FuzzyChoice(TaskStatus)
    assigned_to = factory.Faker("name")
    project_id = 1


@pytest.fixture
def app_client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time
        if hasattr(target, "updated_at"):
            target.updated_at = time

    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture()
def client(session):
    client = ClientFactory()

    session.add(client)
    session.commit()
    session.refresh(client)

    return client


@pytest.fixture
def project(session):
    project = ProjectFactory()

    session.add(project)
    session.commit()
    session.refresh(project)

    return project


@pytest.fixture
def task(session):
    task = TaskFactory()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task
