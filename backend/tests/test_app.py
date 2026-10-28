import pytest
from unittest.mock import MagicMock, patch

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200


def test_version_endpoint(client):
    response = client.get("/version")
    assert response.status_code == 200


@patch("app.get_connection")
def test_health_endpoint(mock_connection, client):
    mock_conn = MagicMock()
    mock_connection.return_value = mock_conn

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    mock_conn.close.assert_called_once()


@patch("app.get_connection")
def test_get_employees(mock_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    response = client.get("/employees")

    assert response.status_code == 200
    assert response.json == []


def test_create_employee_missing_fields(client):
    response = client.post("/employees", json={"name": "Rahul"})

    assert response.status_code == 400


@patch("app.get_connection")
def test_create_employee(mock_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        1, "Rahul Sharma", "rahul@example.com", "DevOps", None
    )

    response = client.post(
        "/employees",
        json={
            "name": "Rahul Sharma",
            "email": "rahul@example.com",
            "department": "DevOps",
        },
    )

    assert response.status_code in (200, 201)
    mock_conn.commit.assert_called_once()

