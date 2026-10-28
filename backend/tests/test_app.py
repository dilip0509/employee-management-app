

import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from app import app


def make_mock_connection():
    connection = MagicMock()
    connection.__enter__.return_value = connection
    return connection


def test_home_endpoint():
    app.config["TESTING"] = True
    with app.test_client() as client:
        response = client.get("/")
    assert response.status_code == 200


def test_version_endpoint():
    with app.test_client() as client:
        response = client.get("/version")
    assert response.status_code == 200


@patch("app.get_connection")
def test_health_endpoint(mock_get_connection):
    mock_connection = make_mock_connection()
    mock_get_connection.return_value = mock_connection

    with app.test_client() as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    mock_connection.execute.assert_called_once()


@patch("app.get_connection")
def test_get_employees(mock_get_connection):
    mock_connection = make_mock_connection()
    mock_get_connection.return_value = mock_connection
    mock_connection.execute.return_value.fetchall.return_value = []

    with app.test_client() as client:
        response = client.get("/employees")

    assert response.status_code == 200
    assert response.json == []


def test_create_employee_missing_fields():
    with app.test_client() as client:
        response = client.post("/employees", json={"name": "Rahul"})

    assert response.status_code == 400


@patch("app.get_connection")
def test_create_employee(mock_get_connection):
    mock_connection = make_mock_connection()
    mock_get_connection.return_value = mock_connection

    mock_connection.execute.return_value.fetchone.return_value = (
        1,
        "Rahul Sharma",
        "rahul@example.com",
        "DevOps",
        None,
    )

    with app.test_client() as client:
        response = client.post(
            "/employees",
            json={
                "name": "Rahul Sharma",
                "email": "rahul@example.com",
                "department": "DevOps",
            },
        )

    assert response.status_code == 201
    assert response.json["name"] == "Rahul Sharma"

