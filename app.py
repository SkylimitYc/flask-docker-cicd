from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "tasksdb"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASS", "password")
    )

@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (name) VALUES (%s)", (task,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
