from http import HTTPStatus

from tests.conftest import TaskFactory
from crud_backend.models.tasks import Task, TaskStatus


def test_create_task(app_client, mock_db_time, project):
    with mock_db_time(model=Task) as time:
        res = app_client.post(
            f"/projects/{project.id}/tasks",
            json={
                "title": "Test task",
                "description": "Test task description",
                "status": "pending",
                "assigned_to": "TI",
            },
        )

    assert res.status_code == HTTPStatus.CREATED
    assert res.json() == {
        "id": 1,
        "title": "Test task",
        "description": "Test task description",
        "status": "pending",
        "assigned_to": "TI",
        "created_at": time.isoformat(),
        "updated_at": time.isoformat(),
    }


def test_create_task_project_not_found(app_client):
    res = app_client.post(
        "/projects/4/tasks",
        json={
            "title": "Test task",
            "description": "Test task description",
            "status": "pending",
            "assigned_to": "TI",
        },
    )

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Project not found"}


def test_list_tasks_should_return_5_tasks(session, app_client, project):
    expected_todos = 5
    session.bulk_save_objects(TaskFactory.create_batch(5, project_id=project.id))
    session.commit()

    res = app_client.get(f"/projects/{project.id}/tasks/")

    assert len(res.json()["tasks"]) == expected_todos


def test_list_tasks_pagination_should_return_2_tasks(session, app_client, project):
    expected_todos = 2
    session.bulk_save_objects(TaskFactory.create_batch(5, project_id=project.id))
    session.commit()

    res = app_client.get(f"/projects/{project.id}/tasks/?offset=1&limit=2")

    assert len(res.json()["tasks"]) == expected_todos


def test_list_tasks_filter_title_should_return_5_tasks(session, app_client, project):
    expected_todos = 5
    session.bulk_save_objects(
        TaskFactory.create_batch(5, project_id=project.id, title="Test task title")
    )
    session.commit()

    res = app_client.get(f"/projects/{project.id}/tasks/?title=Test task title")

    assert len(res.json()["tasks"]) == expected_todos


def test_list_tasks_filter_description_should_return_5_tasks(
    session, app_client, project
):
    expected_todos = 5
    session.bulk_save_objects(
        TaskFactory.create_batch(
            5, project_id=project.id, description="Test task description"
        )
    )
    session.commit()

    res = app_client.get(
        f"/projects/{project.id}/tasks/?description=Test task description"
    )

    assert len(res.json()["tasks"]) == expected_todos


def test_list_tasks_filter_status_should_return_5_tasks(session, app_client, project):
    expected_todos = 5
    session.bulk_save_objects(
        TaskFactory.create_batch(5, project_id=project.id, status=TaskStatus.deleted)
    )
    session.commit()

    res = app_client.get(f"/projects/{project.id}/tasks/?status=deleted")

    assert len(res.json()["tasks"]) == expected_todos


def test_list_tasks_filter_assigned_to_should_return_5_tasks(
    session, app_client, project
):
    expected_todos = 5
    session.bulk_save_objects(
        TaskFactory.create_batch(
            5, project_id=project.id, assigned_to="Test task assigned_to"
        )
    )
    session.commit()

    res = app_client.get(
        f"/projects/{project.id}/tasks/?assigned_to=Test task assigned_to"
    )

    assert len(res.json()["tasks"]) == expected_todos


def test_list_tasks_should_return_all_expected_fields(
    session, app_client, mock_db_time, project
):
    with mock_db_time(model=Task) as time:
        task = TaskFactory.create(project_id=project.id)
        session.add(task)
        session.commit()

    session.refresh(task)
    res = app_client.get(f"/projects/{project.id}/tasks/")

    assert res.status_code == HTTPStatus.OK
    assert res.json()["tasks"] == [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "assigned_to": task.assigned_to,
            "created_at": time.isoformat(),
            "updated_at": time.isoformat(),
        }
    ]


def test_list_tasks_project_not_found(session, app_client):
    session.bulk_save_objects(TaskFactory.create_batch(5, project_id=10))
    session.commit()

    res = app_client.get("projects/10/tasks/")

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Project not found"}


def test_read_task(app_client, project, task):
    res = app_client.get(f"projects/{project.id}/tasks/{task.id}")

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "assigned_to": task.assigned_to,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }


def test_read_task_projet_not_found(app_client, task):
    res = app_client.get(f"projects/10/tasks/{task.id}")

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Project not found"}


def test_read_task_not_found(app_client, project):
    res = app_client.get(f"projects/{project.id}/tasks/10")

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Task not found"}


def test_patch_task(app_client, task, project):
    res = app_client.patch(
        f"/projects/{project.id}/tasks/{task.id}",
        json={
            "title": "Updated task",
            "description": "Updated task description",
            "status": "doing",
            "assigned_to": "Dev",
        },
    )

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {
        "id": task.id,
        "title": "Updated task",
        "description": "Updated task description",
        "status": "doing",
        "assigned_to": "Dev",
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }


def test_patch_task_project_not_found(app_client, task):
    res = app_client.patch(
        f"/projects/10/tasks/{task.id}", json={"title": "test patch"}
    )

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Project not found"}


def test_patch_task_not_found(app_client, project):
    res = app_client.patch(
        f"/projects/{project.id}/tasks/10", json={"title": "test patch"}
    )

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Task not found"}


def test_delete_task(app_client, task, project):
    res = app_client.delete(f"/projects/{project.id}/tasks/{task.id}")

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"message": "Task deleted successfully"}


def test_delete_task_project_not_found(app_client, task):
    res = app_client.delete(f"/projects/10/tasks/{task.id}")

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Project not found"}


def test_delete_task_not_found(app_client, project):
    res = app_client.delete(f"/projects/{project.id}/tasks/10")

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Task not found"}
