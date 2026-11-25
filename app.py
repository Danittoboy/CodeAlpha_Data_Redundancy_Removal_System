from flask import Flask, render_template, request
import sqlite3
import hashlib
import json
from datetime import datetime

app = Flask(__name__)

DATABASE = "records.db"


def connect_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    with connect_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                fingerprint TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def generate_fingerprint(name, email):
    data = {
        "name": name.strip().lower(),
        "email": email.strip().lower()
    }

    content = json.dumps(data, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()


def get_records():
    with connect_db() as connection:
        return connection.execute(
            "SELECT * FROM records ORDER BY id DESC"
        ).fetchall()


@app.route("/")
def home():
    return render_template(
        "index.html",
        records=get_records(),
        message=None,
        status=None
    )


@app.route("/add", methods=["POST"])
def add_record():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()

    if len(name) < 2 or len(name) > 100:
        return show_result(
            "Enter a valid name (2–100 characters).", "error"
        )

    if "@" not in email or "." not in email.split("@")[-1]:
        return show_result("Enter a valid email address.", "error")

    if len(phone) > 30:
        return show_result("Phone number is too long.", "error")

    fingerprint = generate_fingerprint(name, email)

    with connect_db() as connection:
        existing = connection.execute(
            "SELECT id FROM records WHERE fingerprint = ?",
            (fingerprint,)
        ).fetchone()

        if existing:
            return show_result(
                "Duplicate record detected. This entry already exists.",
                "duplicate"
            )

        similar = connection.execute(
            "SELECT id FROM records WHERE lower(trim(name)) = ? LIMIT 1",
            (name.lower(),)
        ).fetchone()

        connection.execute("""
            INSERT INTO records
            (name, email, phone, fingerprint, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            phone,
            fingerprint,
            datetime.now().isoformat()
        ))

    if similar:
        return show_result(
            "Unique record saved, but a similar name exists. "
            "Please review it to avoid a false positive.",
            "review"
        )

    return show_result(
        "New verified record saved successfully!",
        "success"
    )


def show_result(message, status):
    return render_template(
        "index.html",
        records=get_records(),
        message=message,
        status=status
    )


@app.route("/health")
def health():
    return {"status": "running"}


create_table()


if __name__ == "__main__":
    app.run(debug=True)
