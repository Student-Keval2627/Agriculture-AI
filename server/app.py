from flask import Flask, jsonify
from flask_cors import CORS

from config import client
from routes.crop_routes import crop_bp
from routes.disease_routes import disease_bp
from routes.fertilizer_routes import fertilizer_bp
from routes.irrigation_routes import irrigation_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(crop_bp)
app.register_blueprint(disease_bp)
app.register_blueprint(fertilizer_bp)
app.register_blueprint(irrigation_bp)


@app.route("/")
def home():
    return jsonify({
        "message": "Agriculture AI server is running"
    })


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