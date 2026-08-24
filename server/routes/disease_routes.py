from datetime import datetime, timezone
from flask import Blueprint, jsonify, request

from config import db
from services.disease_service import get_disease_advice

disease_bp = Blueprint("disease_bp", __name__)


@disease_bp.route("/api/disease/check", methods=["POST"])
def check_disease():
    data = request.get_json(silent=True) or {}

    crop = str(data.get("crop", "")).strip()
    symptom = str(data.get("symptom", "")).strip()

    if not crop or not symptom:
        return jsonify({
            "success": False,
            "message": "Crop and symptom are required"
        }), 400

    diagnosis = get_disease_advice(crop, symptom)

    history_data = {
        "crop": crop,
        "symptom": symptom,
        "disease": diagnosis["disease"],
        "risk": diagnosis["risk"],
        "description": diagnosis["description"],
        "advice": diagnosis["advice"],
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    db.disease_history.insert_one(history_data.copy())

    return jsonify({
        "success": True,
        "message": "Disease advice generated successfully",
        "data": history_data
    })


@disease_bp.route("/api/disease/history", methods=["GET"])
def disease_history():
    history = list(
        db.disease_history.find({}, {"_id": 0})
        .sort("createdAt", -1)
        .limit(10)
    )

    return jsonify({
        "success": True,
        "data": history
    })