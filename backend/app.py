

cat > backend/app.py <<'EOF'
import os
import re

from flask import Flask, jsonify, request
from psycopg import IntegrityError

from db import get_connection

app = Flask(__name__)


def valid_employee(data):
    if not isinstance(data, dict):
        return False

    for field in ("name", "email", "department"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            return False

    email = data["email"].strip()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False

    return True


@app.get("/")
def home():
    return jsonify({
        "application": "Employee Management API",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "status": "running",
    })


@app.get("/health")
def health():
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception:
        app.logger.exception("Health check failed")
        return jsonify({"status": "unhealthy"}), 503


@app.get("/version")
def version():
    return jsonify({"version": os.getenv("APP_VERSION", "1.0.0")})


@app.get("/employees")
def list_employees():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, email, department, created_at "
            "FROM employees ORDER BY id"
        ).fetchall()

    return jsonify([
        {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "department": row[3],
            "created_at": row[4].isoformat() if row[4] else None,
        }
        for row in rows
    ])


@app.post("/employees")
def create_employee():
    data = request.get_json(silent=True)

    if not valid_employee(data):
        return jsonify({
            "error": "Provide non-empty name, valid email and department"
        }), 400

    try:
        with get_connection() as conn:
            row = conn.execute(
                """
                INSERT INTO employees (name, email, department)
                VALUES (%s, %s, %s)
                RETURNING id, name, email, department, created_at
                """,
                (
                    data["name"].strip(),
                    data["email"].strip(),
                    data["department"].strip(),
                ),
            ).fetchone()

        return jsonify({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "department": row[3],
            "created_at": row[4].isoformat() if row[4] else None,
        }), 201

    except IntegrityError:
        return jsonify({"error": "Email already exists"}), 409


@app.get("/employees/<int:employee_id>")
def get_employee(employee_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, email, department, created_at "
            "FROM employees WHERE id = %s",
            (employee_id,),
        ).fetchone()

    if row is None:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "department": row[3],
        "created_at": row[4].isoformat() if row[4] else None,
    })


@app.put("/employees/<int:employee_id>")
def update_employee(employee_id):
    data = request.get_json(silent=True)

    if not valid_employee(data):
        return jsonify({
            "error": "Provide non-empty name, valid email and department"
        }), 400

    try:
        with get_connection() as conn:
            row = conn.execute(
                """
                UPDATE employees
                SET name = %s, email = %s, department = %s
                WHERE id = %s
                RETURNING id, name, email, department, created_at
                """,
                (
                    data["name"].strip(),
                    data["email"].strip(),
                    data["department"].strip(),
                    employee_id,
                ),
            ).fetchone()

        if row is None:
            return jsonify({"error": "Employee not found"}), 404

        return jsonify({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "department": row[3],
            "created_at": row[4].isoformat() if row[4] else None,
        })

    except IntegrityError:
        return jsonify({"error": "Email already exists"}), 409


@app.delete("/employees/<int:employee_id>")
def delete_employee(employee_id):
    with get_connection() as conn:
        result = conn.execute(
            "DELETE FROM employees WHERE id = %s RETURNING id",
            (employee_id,),
        ).fetchone()

    if result is None:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({"message": "Employee deleted", "id": result[0]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
EOF
