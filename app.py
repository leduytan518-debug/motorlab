import os
from flask import Flask, jsonify, render_template, request
from database import generate_questions_with_ai, get_connection, init_db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "studylab-secret-key")
SITE_NAME = "STUDYLAB"

init_db()

@app.context_processor
def inject_globals():
    return {"site_name": SITE_NAME}

@app.route("/")
def index():
    conn = get_connection()
    stats = {
        "topics": conn.execute("SELECT COUNT(*) FROM topics").fetchone()[0],
        "questions": conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0],
        "concepts": conn.execute("SELECT COUNT(*) FROM concepts").fetchone()[0],
        "methods": conn.execute("SELECT COUNT(*) FROM methods").fetchone()[0],
    }
    topics = conn.execute("SELECT * FROM topics LIMIT 3").fetchall()
    conn.close()
    return render_template("index.html", stats=stats, topics=topics)

@app.route("/vehicles")
def vehicles():
    q = request.args.get("q", "").strip()
    chapter = request.args.get("chapter", "").strip()
    conn = get_connection()
    sql = "SELECT * FROM topics WHERE 1=1"
    params = []
    if chapter:
        sql += " AND category = ?"
        params.append(chapter)
    if q:
        sql += " AND (title LIKE ? OR summary LIKE ? OR key_points LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])
    items = conn.execute(sql, params).fetchall()
    conn.close()
    return render_template("vehicles.html", items=items, q=q, chapter=chapter)

@app.route("/faults")
def faults():
    q = request.args.get("q", "").strip()
    chapter = request.args.get("chapter", "").strip()
    conn = get_connection()
    sql = "SELECT * FROM questions WHERE 1=1"
    params = []
    if chapter:
        sql += " AND chapter = ?"
        params.append(chapter)
    if q:
        sql += " AND (question LIKE ? OR explanation LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])
    sql += " ORDER BY id DESC"
    questions = conn.execute(sql, params).fetchall()
    conn.close()
    return render_template(
        "faults.html",
        questions=questions,
        q=q,
        chapter=chapter,
        has_env_key=bool(os.environ.get("GEMINI_API_KEY"))
    )

@app.route("/parts")
def parts():
    q = request.args.get("q", "").strip()
    chapter = request.args.get("chapter", "").strip()
    conn = get_connection()
    sql = "SELECT * FROM concepts WHERE 1=1"
    params = []
    if chapter:
        sql += " AND chapter = ?"
        params.append(chapter)
    if q:
        sql += " AND (name LIKE ? OR definition LIKE ? OR exam_tip LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])
    concepts = conn.execute(sql, params).fetchall()
    conn.close()
    return render_template("parts.html", concepts=concepts, q=q, chapter=chapter)

@app.route("/tools")
def tools():
    q = request.args.get("q", "").strip()
    conn = get_connection()
    sql = "SELECT * FROM methods WHERE 1=1"
    params = []
    if q:
        sql += " AND (name LIKE ? OR usage LIKE ? OR how_to_apply LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])
    methods = conn.execute(sql, params).fetchall()
    conn.close()
    return render_template("tools.html", methods=methods, q=q)

@app.route("/efi")
def efi():
    return render_template("efi.html")

@app.route("/prices")
def prices():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM exam_structure").fetchall()
    conn.close()
    return render_template("prices.html", rows=rows)

@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(silent=True) or {}
    res = generate_questions_with_ai(
        chapter=data.get("chapter", "Chương 2"),
        count=int(data.get("count", 5)),
        custom_api_key=data.get("api_key", "")
    )
    return jsonify(res)

@app.errorhandler(404)
def not_found(_e):
    return render_template("index.html", stats={"topics":6,"questions":6,"concepts":6,"methods":6}, topics=[]), 404

if __name__ == "__main__":
    app.run(debug=True)