from http import HTTPStatus

from tests.conftest import ProjectFactory
from crud_backend.models.projects import Project, ProjectStatus


def test_create_project(app_client, mock_db_time, client):
    with mock_db_time(model=Project) as time:
        res = app_client.post(
            f"clients/{client.id}/projects",
            json={
                "title": "Test project",
                "description": "Test project description",
                "status": "pending",
            },
        )

    assert res.json() == {
        "id": 1,
        "title": "Test project",
        "description": "Test project description",
        "status": "pending",
        "created_at": time.isoformat(),
        "updated_at": time.isoformat(),
    }


def test_create_project_client_not_found(app_client):
    res = app_client.post(
        "clients/4/projects/",
        json={
            "title": "Test project",
            "description": "Test project description",
            "status": "pending",
        },
    )

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Client not found"}


def test_list_projects_should_return_5_projects(session, app_client, client):
    expected_projects = 5
    session.bulk_save_objects(ProjectFactory.create_batch(5, client_id=client.id))
    session.commit()

    res = app_client.get(f"clients/{client.id}/projects/")

    assert res.status_code == HTTPStatus.OK
    assert len(res.json()["projects"]) == expected_projects


def test_list_projects_pagination_should_return_2_projects(session, app_client, client):
    expected_projects = 2
    session.bulk_save_objects(ProjectFactory.create_batch(5, client_id=client.id))
    session.commit()

    res = app_client.get(f"clients/{client.id}/projects/?offset=1&limit=2")

    assert len(res.json()["projects"]) == expected_projects


def test_list_projects_filter_title_should_return_5_projects(
    session, app_client, client
):
    expected_projects = 5
    session.bulk_save_objects(
        ProjectFactory.create_batch(5, client_id=client.id, title="Test project title")
    )
    session.commit()

    res = app_client.get(f"clients/{client.id}/projects/?title=Test project title")

    assert len(res.json()["projects"]) == expected_projects


def test_list_projects_filter_description_should_return_5_projects(
    session, app_client, client
):
    expected_projects = 5
    session.bulk_save_objects(
        ProjectFactory.create_batch(
            5, client_id=client.id, description="Test project description"
        )
    )
    session.commit()

    res = app_client.get(
        f"clients/{client.id}/projects/?description=Test project description"
    )

    assert len(res.json()["projects"]) == expected_projects


def test_list_projects_filter_status_should_return_5_projects(
    session, app_client, client
):
    expected_projects = 5
    session.bulk_save_objects(
        ProjectFactory.create_batch(
            5, client_id=client.id, status=ProjectStatus.pending
        )
    )
    session.commit()

    res = app_client.get(f"clients/{client.id}/projects/?status=pending")

    assert len(res.json()["projects"]) == expected_projects


def test_list_projects_should_return_all_expected_fields(
    session, app_client, client, mock_db_time
):
    with mock_db_time(model=Project) as time:
        project = ProjectFactory.create(client_id=client.id)
        session.add(project)
        session.commit()

    session.refresh(project)
    res = app_client.get(f"clients/{client.id}/projects/")

    assert res.json()["projects"] == [
        {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "status": project.status,
            "created_at": time.isoformat(),
            "updated_at": time.isoformat(),
        }
    ]


def test_list_projects_client_not_found(session, app_client):
    session.bulk_save_objects(ProjectFactory.create_batch(5, client_id=10))
    session.commit()

    res = app_client.get("clients/10/projects/")

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Client not found"}


def test_read_project(app_client, client, project):
    res = app_client.get(f"clients/{client.id}/projects/{project.id}")

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {
        "title": project.title,
        "description": project.description,
        "status": project.status,
        "id": project.id,
        "created_at": project.created_at.isoformat(),
        "updated_at": project.updated_at.isoformat(),
    }


def test_read_project_client_not_found(app_client, project):
    res = app_client.get(f"clients/10/projects/{project.id}")

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Client not found"}


def test_read_project_not_found(app_client, client):
    res = app_client.get(f"clients/{client.id}/projects/10")

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Project not found"}


def test_patch_project(app_client, project, client):
    res = app_client.patch(
        f"clients/{client.id}/projects/{project.id}",
        json={"title": "teste!"},
    )

    assert res.status_code == HTTPStatus.OK
    assert res.json()["title"] == "teste!"


def test_patch_project_client_not_found(app_client, project):
    res = app_client.patch(
        f"clients/10/projects/{project.id}",
        json={"title": "teste!"},
    )

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Client not found"}


def test_patch_project_not_found(app_client, client):
    res = app_client.patch(
        f"clients/{client.id}/projects/10",
        json={"title": "teste!"},
    )

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Project not found"}


def test_delete_project(app_client, project, client):
    res = app_client.delete(f"clients/{client.id}/projects/{project.id}")

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"message": "Project deleted successfully"}


def test_delete_project_client_not_found(app_client, project):
    res = app_client.delete(f"clients/10/projects/{project.id}")

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Client not found"}


def test_delete_project_not_found(app_client, client):
    res = app_client.delete(f"clients/{client.id}/projects/10")

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Project not found"}
