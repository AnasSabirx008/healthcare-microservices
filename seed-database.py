import mysql.connector

DB_CONFIG = {
    "host": "",
    "user": "admin",
    "password": "",
    "database": "clinic",
}

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    provider VARCHAR(100) NOT NULL,
    appointment_date DATE NOT NULL
)
""")

patients = [
    ("Sarah", "Johnson", "1985-03-15", "Dr. Emily Chen", "2026-06-25"),
    ("Michael", "Williams", "1972-08-22", "Dr. James Park", "2026-06-26"),
    ("Jessica", "Brown", "1990-11-03", "Dr. Emily Chen", "2026-06-27"),
    ("David", "Martinez", "1968-05-30", "Dr. Aisha Patel", "2026-06-28"),
    ("Amanda", "Taylor", "1995-01-17", "Dr. James Park", "2026-06-30"),
]

cursor.executemany(
    "INSERT INTO patients (first_name, last_name, date_of_birth, provider, appointment_date) VALUES (%s, %s, %s, %s, %s)",
    patients
)

conn.commit()
print(f"Inserted {cursor.rowcount} patients.")
cursor.close()
conn.close()