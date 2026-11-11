"""Flask web app: technical library for cars and motorcycles."""
import os

from flask import Flask, abort, render_template, request
from database import get_connection, init_db

app = Flask(__name__, template_folder=".", static_folder=".")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")


def fetch_all(query, params=()):
    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


def fetch_one(query, params=()):
    with get_connection() as conn:
        return conn.execute(query, params).fetchone()


@app.template_filter("vnd")
def format_vnd(value):
    if value is None or int(value) <= 0:
        return "Chưa cập nhật"
    return f"{int(value):,}".replace(",", ".") + " đ"


@app.context_processor
def inject_site_labels():
    return {"site_name": "MOTORLAB | Thư viện kỹ thuật phương tiện"}


@app.route("/")
def index():
    counts = {
        "oto": fetch_one("SELECT COUNT(*) AS n FROM vehicles WHERE vehicle_type='oto'")["n"],
        "xemay": fetch_one("SELECT COUNT(*) AS n FROM vehicles WHERE vehicle_type='xemay'")["n"],
        "faults": fetch_one("SELECT COUNT(*) AS n FROM faults")["n"],
        "parts": fetch_one("SELECT COUNT(*) AS n FROM parts")["n"],
    }
    latest_vehicles = fetch_all("SELECT * FROM vehicles ORDER BY id DESC LIMIT 4")
    latest_faults = fetch_all("SELECT * FROM faults ORDER BY id DESC LIMIT 3")
    return render_template("index.html", counts=counts, vehicles=latest_vehicles, faults=latest_faults)


@app.route("/vehicles")
def vehicles():
    q = request.args.get("q", "").strip()
    vehicle_type = request.args.get("type", "").strip()
    sql = "SELECT * FROM vehicles WHERE 1=1"
    params = []
    if vehicle_type in ("oto", "xemay"):
        sql += " AND vehicle_type = ?"
        params.append(vehicle_type)
    if q:
        like = f"%{q}%"
        sql += " AND (brand LIKE ? OR model LIKE ? OR engine LIKE ? OR fuel_system LIKE ?)"
        params.extend([like, like, like, like])
    sql += " ORDER BY vehicle_type, brand, model"
    rows = fetch_all(sql, params)
    return render_template("vehicles.html", vehicles=rows, q=q, selected_type=vehicle_type)


@app.route("/vehicles/<int:vehicle_id>")
def vehicle_detail(vehicle_id):
    vehicle = fetch_one("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
    if vehicle is None:
        abort(404)
    related_faults = fetch_all(
        "SELECT * FROM faults WHERE vehicle_type = ? ORDER BY id LIMIT 4",
        (vehicle["vehicle_type"],),
    )
    related_parts = fetch_all(
        "SELECT * FROM parts WHERE vehicle_type = ? ORDER BY id LIMIT 4",
        (vehicle["vehicle_type"],),
    )
    return render_template(
        "vehicle_detail.html", vehicle=vehicle,
        faults=related_faults, parts=related_parts,
    )


@app.route("/faults")
def faults():
    q = request.args.get("q", "").strip()
    vehicle_type = request.args.get("type", "").strip()
    sql = "SELECT * FROM faults WHERE 1=1"
    params = []
    if vehicle_type in ("oto", "xemay"):
        sql += " AND vehicle_type = ?"
        params.append(vehicle_type)
    if q:
        like = f"%{q}%"
        sql += " AND (code LIKE ? OR symptom LIKE ? OR causes LIKE ? OR model LIKE ?)"
        params.extend([like, like, like, like])
    sql += " ORDER BY CASE severity WHEN 'Cao' THEN 0 WHEN 'Trung bình' THEN 1 ELSE 2 END, id"
    rows = fetch_all(sql, params)
    return render_template("faults.html", faults=rows, q=q, selected_type=vehicle_type)


@app.route("/parts")
def parts():
    q = request.args.get("q", "").strip()
    vehicle_type = request.args.get("type", "").strip()
    sql = "SELECT * FROM parts WHERE 1=1"
    params = []
    if vehicle_type in ("oto", "xemay"):
        sql += " AND vehicle_type = ?"
        params.append(vehicle_type)
    if q:
        like = f"%{q}%"
        sql += " AND (name LIKE ? OR compatible LIKE ? OR function LIKE ?)"
        params.extend([like, like, like])
    sql += " ORDER BY vehicle_type, name"
    rows = fetch_all(sql, params)
    return render_template("parts.html", parts=rows, q=q, selected_type=vehicle_type)


@app.route("/tools")
def tools():
    q = request.args.get("q", "").strip()
    if q:
        like = f"%{q}%"
        rows = fetch_all(
            "SELECT * FROM tools WHERE name LIKE ? OR category LIKE ? OR usage LIKE ? ORDER BY category, name",
            (like, like, like),
        )
    else:
        rows = fetch_all("SELECT * FROM tools ORDER BY category, name")
    return render_template("tools.html", tools=rows, q=q)


@app.route("/prices")
def prices():
    vehicle_type = request.args.get("type", "").strip()
    sql = "SELECT * FROM repair_prices WHERE 1=1"
    params = []
    if vehicle_type in ("oto", "xemay"):
        sql += " AND vehicle_type = ?"
        params.append(vehicle_type)
    sql += " ORDER BY vehicle_type, job"
    rows = fetch_all(sql, params)
    return render_template("prices.html", prices=rows, selected_type=vehicle_type)


@app.route("/efi")
def efi():
    return render_template("efi.html")


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


init_db()


if __name__ == "__main__":
    # Chỉ dùng debug khi phát triển trên máy cá nhân.
    app.run(host="127.0.0.1", port=5000, debug=True)
