
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "skillswap.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            teach_skill TEXT NOT NULL,
            learn_skill TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    skills = conn.execute(
        "SELECT * FROM skills ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("index.html", skills=skills)


@app.route("/post", methods=["GET", "POST"])
def post_skill():
    if request.method == "POST":
        student_name = request.form["student_name"].strip()
        teach_skill = request.form["teach_skill"].strip()
        learn_skill = request.form["learn_skill"].strip()
        description = request.form["description"].strip()

        if student_name and teach_skill and learn_skill:
            conn = get_db()
            conn.execute(
                """INSERT INTO skills
                (student_name, teach_skill, learn_skill, description)
                VALUES (?, ?, ?, ?)""",
                (student_name, teach_skill, learn_skill, description)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    return render_template("post_skill.html")


@app.route("/matches")
def matches():
    conn = get_db()
    skills = conn.execute(
        "SELECT * FROM skills ORDER BY teach_skill"
    ).fetchall()
    conn.close()
    return render_template("matches.html", skills=skills)


@app.route("/my-exchanges")
def my_exchanges():
    conn = get_db()
    skills = conn.execute(
        "SELECT * FROM skills ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("my_exchanges.html", skills=skills)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
