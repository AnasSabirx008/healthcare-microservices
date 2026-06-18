import os
from flask import Flask, jsonify, render_template_string

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


@app.route("/")
def home():
    return render_template_string("""
    <html>
    <head><title>Patient Portal - HealthFirst Clinic</title></head>
    <body>
        <h1>Welcome to HealthFirst Clinic</h1>
        <p>Use this portal to view your appointments and provider information.</p>
        <a href="/patients">View Patient Directory</a>
    </body>
    </html>
    """)


@app.route("/patients")
def list_patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, first_name, last_name, provider, appointment_date FROM patients")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(patients)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)