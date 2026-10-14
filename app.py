import os
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("CLEANBENIN_SECRET_KEY", "change-this-secret-before-deployment")
DB_PATH = os.environ.get("CLEANBENIN_DB", "cleanbenin.db")

ADMIN_USERNAME = os.environ.get("CLEANBENIN_ADMIN_USERNAME", "CleanBenin")
ADMIN_PASSWORD = "jesus-christ6"

SERVICES = [
    ("Chambre + salon", 5000),
    ("Chambre + salon + douche", 7000),
    ("Deux chambres + salon + douche", 15000),
    ("Maison complète", 25000),
    ("Douche seule", 2500),
    ("Cuisine seule", 2500),
]
CITIES = ["Cotonou", "Porto-Novo", "Abomey-Calavi", "Pahou"]

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            city TEXT NOT NULL,
            service TEXT NOT NULL,
            date TEXT NOT NULL,
            details TEXT DEFAULT '',
            status TEXT DEFAULT 'Nouvelle',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")

init_db()

def admin_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapped

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

@app.route("/")
def home():
    return render_template("index.html", services=SERVICES, cities=CITIES)

@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.form
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    city = data.get("city", "").strip()
    service = data.get("service", "").strip()
    date = data.get("date", "").strip()
    details = data.get("details", "").strip()[:1000]
    valid_services = {name for name, price in SERVICES}
    if not all([name, phone, city, service, date]) or city not in CITIES or service not in valid_services:
        flash("Vérifie les champs obligatoires puis réessaie.", "error")
        return redirect(url_for("home") + "#reservation")
    with db() as conn:
        conn.execute(
            "INSERT INTO bookings (name, phone, city, service, date, details) VALUES (?, ?, ?, ?, ?, ?)",
            (name[:100], phone[:40], city, service, date, details)
        )
    flash("Ta demande a bien été envoyée. Nous te contacterons selon les coordonnées fournies.", "success")
    return redirect(url_for("home") + "#reservation")

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if not ADMIN_PASSWORD:
            error = "Le mot de passe administrateur n'est pas encore configuré sur le serveur."
        elif username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Nom d'utilisateur ou mot de passe incorrect."
    return render_template("login.html", error=error)

@app.route("/admin/reservations")
@admin_required
def dashboard():
    with db() as conn:
        bookings = conn.execute("SELECT * FROM bookings ORDER BY id DESC").fetchall()
    return render_template("dashboard.html", bookings=bookings)

@app.route("/admin/status/<int:booking_id>", methods=["POST"])
@admin_required
def update_status(booking_id):
    status = request.form.get("status", "")
    if status not in ["Nouvelle", "Confirmée", "Terminée", "Annulée"]:
        flash("Statut invalide.", "error")
    else:
        with db() as conn:
            conn.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id))
        flash("Statut mis à jour.", "success")
    return redirect(url_for("dashboard"))

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    # Local testing only. For deployment, use a production WSGI server.
    app.run(host="127.0.0.1", port=5000, debug=False)
