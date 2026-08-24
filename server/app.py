import os
from datetime import timedelta

from flask import Flask, jsonify, redirect, request, send_from_directory, session
from flask_cors import CORS

from config import SECRET_KEY, client
from routes.auth_routes import auth_bp
from routes.crop_routes import crop_bp
from routes.disease_routes import disease_bp
from routes.fertilizer_routes import fertilizer_bp
from routes.irrigation_routes import irrigation_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "client"))

app = Flask(
    __name__,
    static_folder=CLIENT_DIR,
    static_url_path=""
)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(crop_bp)
app.register_blueprint(disease_bp)
app.register_blueprint(fertilizer_bp)
app.register_blueprint(irrigation_bp)


@app.before_request
def protect_frontend_pages():
    path = request.path

    if path.startswith("/api/"):
        return None

    if path in {"/login.html", "/register.html", "/"}:
        return None

    if path.endswith((".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".ico", ".webp")):
        return None

    if path.endswith(".html") and not session.get("user_id"):
        return redirect("/login.html")

    return None


@app.route("/")
def home():
    if session.get("user_id"):
        return send_from_directory(CLIENT_DIR, "index.html")

    return send_from_directory(CLIENT_DIR, "login.html")


@app.route("/login.html")
def login_page():
    if session.get("user_id"):
        return redirect("/")

    return send_from_directory(CLIENT_DIR, "login.html")


@app.route("/register.html")
def register_page():
    if session.get("user_id"):
        return redirect("/")

    return send_from_directory(CLIENT_DIR, "register.html")


@app.route("/api/health")
def health():
    return jsonify({
        "success": True,
        "message": "Server is healthy"
    })


@app.route("/api/database-status")
def database_status():
    try:
        client.admin.command("ping")

        return jsonify({
            "success": True,
            "message": "MongoDB connected successfully"
        })
    except Exception:
        return jsonify({
            "success": False,
            "message": "MongoDB is not running"
        }), 503


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)