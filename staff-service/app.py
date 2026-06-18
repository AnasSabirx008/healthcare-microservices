import os
from flask import Flask, jsonify, render_template_string, request

import mysql.connector

app = Flask(__name__)

# Database connection settings pulled from environment variables
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "admin"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "clinic"),
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/admin/")
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM patients")
    count = cursor.fetchone()["total"]
    cursor.close()
    conn.close()
    return render_template_string("""
    <html>
    <head><title>Staff Dashboard - HealthFirst Clinic</title></head>
    <body>
        <h1>Staff Dashboard</h1>
        <p>Total patients registered: {{ count }}</p>
        <a href="/admin/patients">View All Patient Records</a>
    </body>
    </html>
    """, count=count)


@app.route("/admin/patients")
def list_patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(patients)


@app.route("/admin/patients", methods=["POST"])
def add_patient():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO patients (first_name, last_name, date_of_birth, provider, appointment_date) VALUES (%s, %s, %s, %s, %s)",
        (data["first_name"], data["last_name"], data["date_of_birth"], data["provider"], data["appointment_date"])
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": new_id, "message": "Patient added successfully"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)