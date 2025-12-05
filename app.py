from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = "chave_super_secreta"

DB_PATH = "quiz_answers.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        anon_id TEXT,
        created_at TEXT,
        sent_to_admin INTEGER DEFAULT 0
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER,
        page INTEGER,
        answers_json TEXT,
        created_at TEXT,
        FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS routines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER,
        admin_id INTEGER,
        routine_text TEXT,
        created_at TEXT,
        FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT
    )""")
    conn.commit()
    conn.close()

init_db()

# template filter to parse stored JSON in templates (admin view)
@app.template_filter('loads')
def loads_filter(s):
    try:
        return json.loads(s)
    except:
        return {}

def get_or_create_quiz_row():
    if "quiz_id" in session:
        return session["quiz_id"]
    user_id = session.get("user_id")
    anon_id = None
    if not user_id:
        if "anon_id" not in session:
            session["anon_id"] = str(uuid.uuid4())
        anon_id = session["anon_id"]
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO quizzes (user_id, anon_id, created_at)
        VALUES (?, ?, ?)
    """, (user_id, anon_id, datetime.utcnow().isoformat()))
    quiz_id = cur.lastrowid
    conn.commit()
    conn.close()
    session["quiz_id"] = quiz_id
    return quiz_id

def is_admin():
    return session.get("user_id") == 1

def ligar_quiz_ao_usuario(user_id):
    if "quiz_id" in session:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE quizzes
            SET user_id = ?, anon_id = NULL
            WHERE id = ?
        """, (user_id, session["quiz_id"]))
        conn.commit()
        conn.close()

# ---------------------------
# ROUTES FOR QUIZ PAGES (explicit endpoints quiz1..quiz7)
# ---------------------------
@app.route("/")
def index():
    return redirect(url_for("quiz1"))

@app.route("/quiz1")
def quiz1():
    return render_template("quiz1.html", page=1)

@app.route("/quiz2")
def quiz2():
    return render_template("quiz2.html", page=2)

@app.route("/quiz3")
def quiz3():
    return render_template("quiz3.html", page=3)

@app.route("/quiz4")
def quiz4():
    return render_template("quiz4.html", page=4)

@app.route("/quiz5")
def quiz5():
    return render_template("quiz5.html", page=5)

@app.route("/quiz6")
def quiz6():
    return render_template("quiz6.html", page=6)

@app.route("/quiz7")
def quiz7():
    return render_template("quiz7.html", page=7)

# ---------------------------
# API: save answer
# ---------------------------
@app.route("/api/save_answer", methods=["POST"])
def api_save_answer():
    data = request.get_json()
    if not data or "page" not in data:
        return jsonify({"ok": False, "error": "dados inválidos"}), 400
    page = int(data["page"])
    choices = data.get("choices", [])
    skip = bool(data.get("skip", False))
    quiz_id = get_or_create_quiz_row()
    payload = json.dumps({"choices": choices, "skip": skip}, ensure_ascii=False)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM answers WHERE quiz_id = ? AND page = ?", (quiz_id, page))
    row = cur.fetchone()
    now = datetime.utcnow().isoformat()
    if row:
        cur.execute("""
            UPDATE answers
            SET answers_json = ?, created_at = ?
            WHERE id = ?
        """, (payload, now, row["id"]))
    else:
        cur.execute("""
            INSERT INTO answers (quiz_id, page, answers_json, created_at)
            VALUES (?, ?, ?, ?)
        """, (quiz_id, page, payload, now))
    conn.commit()
    conn.close()
    next_page = min(page + 1, 7)
    # build endpoint name like 'quiz2', 'quiz3', ...
    next_endpoint = f"quiz{next_page}"
    return jsonify({"ok": True, "next": url_for(next_endpoint)})

@app.route("/api/finish_quiz", methods=["POST"])
def finish_quiz():
    get_or_create_quiz_row()
    return jsonify({"ok": True})

@app.route("/api/send_quiz_to_admin", methods=["POST"])
def api_send_quiz_to_admin():
    if "user_id" not in session:
        return jsonify({"ok": False, "error": "not logged in"}), 403
    quiz_id = session.get("quiz_id")
    if not quiz_id:
        return jsonify({"ok": False, "error": "no quiz"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE quizzes SET sent_to_admin = 1 WHERE id = ?", (quiz_id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

# ---------------------------
# ADMIN dashboard (keeps same behavior)
# ---------------------------
@app.route("/admin")
def admin_dashboard():
    if not is_admin():
        return "Acesso proibido", 403
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT q.id AS quiz_id, q.user_id, q.created_at, q.sent_to_admin,
               u.nome, u.email
        FROM quizzes q
        LEFT JOIN users u ON u.id = q.user_id
        WHERE q.sent_to_admin = 1
        ORDER BY q.id DESC
    """)
    quizzes = cur.fetchall()
    dados = []
    for q in quizzes:
        cur.execute("SELECT page, answers_json FROM answers WHERE quiz_id = ? ORDER BY page", (q["quiz_id"],))
        respostas = cur.fetchall()
        for r in respostas:
            dados.append({
                "id": q["quiz_id"],
                "user_id": q["user_id"],
                "nome": q["nome"],
                "email": q["email"],
                "page": r["page"],
                "answers": json.loads(r["answers_json"]),
                "sent_to_admin": q["sent_to_admin"],
                "created_at": q["created_at"]
            })
    conn.close()
    return render_template("admin_dashboard.html", dados=dados)

@app.route("/admin/quiz/<int:quiz_id>")
def admin_view_quiz(quiz_id):
    if not is_admin():
        return "Acesso proibido", 403
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT q.id, q.user_id, q.created_at, u.nome, u.email
        FROM quizzes q
        LEFT JOIN users u ON u.id = q.user_id
        WHERE q.id = ?
    """, (quiz_id,))
    quiz_info = cur.fetchone()
    cur.execute("SELECT page, answers_json FROM answers WHERE quiz_id = ? ORDER BY page", (quiz_id,))
    answers = cur.fetchall()
    cur.execute("SELECT routine_text FROM routines WHERE quiz_id = ? ORDER BY id DESC LIMIT 1", (quiz_id,))
    routine = cur.fetchone()
    conn.close()
    return render_template("admin_quiz_detail.html", quiz=quiz_info, answers=answers, routine=routine["routine_text"] if routine else "")

@app.route("/admin/save_routine", methods=["POST"])
def admin_save_routine():
    if not is_admin():
        return "Acesso proibido", 403
    quiz_id = request.form.get("quiz_id")
    routine_text = request.form.get("routine")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO routines (quiz_id, admin_id, routine_text, created_at)
        VALUES (?, ?, ?, ?)
    """, (quiz_id, session["user_id"], routine_text, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_view_quiz", quiz_id=quiz_id))

# ---------------------------
# LOGIN / REGISTER Fake (para testes)
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    session["user_id"] = 1
    ligar_quiz_ao_usuario(1)
    if request.args.get("attach_quiz"):
        return redirect(url_for("quiz7"))
    return redirect("/admin")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (nome, email) VALUES (?, ?)", ("Novo Usuário", "email@example.com"))
    user_id = cur.lastrowid
    conn.commit()
    conn.close()
    session["user_id"] = user_id
    ligar_quiz_ao_usuario(user_id)
    if request.args.get("attach_quiz"):
        return redirect(url_for("quiz7"))
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
