from sqlalchemy import select
from dataclasses import asdict

from crud_backend.models.clients import Client
from crud_backend.models.projects import Project
from crud_backend.models.tasks import Task


def test_create_client(session, mock_db_time):
    with mock_db_time(model=Client) as time:
        new_client = Client(
            email="teste@test", phone="12345-6789", company="test-company"
        )
        session.add(new_client)
        session.commit()

    client = session.scalar(select(Client).where(Client.company == "test-company"))

    assert asdict(client) == {
        "id": 1,
        "email": "teste@test",
        "phone": "12345-6789",
        "company": "test-company",
        "projects": [],
        "created_at": time,
        "updated_at": time,
    }


def test_create_project(session, client):
    project = Project(
        title="Test Project",
        description="Test Desc",
        status="pending",
        client_id=client.id,
    )

    session.add(project)
    session.commit()
    session.refresh(project)

    client = session.scalar(select(Client).where(Client.id == client.id))

    assert project in client.projects


def test_create_task(session, project):
    task = Task(
        title="Test Task",
        description="Test Desc",
        assigned_to="TI",
        status="pending",
        project_id=project.id,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    project = session.scalar(select(Project).where(Project.id == project.id))

    assert task in project.tasks
