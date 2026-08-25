from datetime import datetime, timezone
from flask import Blueprint, jsonify, request

from config import db
from services.irrigation_service import get_irrigation_advice
from utils.auth_utils import get_current_user_id, login_required

irrigation_bp = Blueprint("irrigation_bp", __name__)


@irrigation_bp.route("/api/irrigation/advice", methods=["POST"])
@login_required
def irrigation_advice():
    data = request.get_json(silent=True) or {}

    crop = str(data.get("crop", "")).strip()
    soil_type = str(data.get("soilType", "")).strip()
    moisture_level = str(data.get("moistureLevel", "")).strip()

    if not crop or not soil_type or not moisture_level:
        return jsonify({
            "success": False,
            "message": "Crop, soil type, and moisture level are required"
        }), 400

    advice = get_irrigation_advice(crop, soil_type, moisture_level)

    history_data = {
        "userId": get_current_user_id(),
        "crop": crop,
        "soilType": soil_type,
        "moistureLevel": moisture_level,
        "status": advice["status"],
        "priority": advice["priority"],
        "description": advice["description"],
        "tips": advice["tips"],
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    db.irrigation_history.insert_one(history_data.copy())

    response_data = history_data.copy()
    response_data.pop("userId")

    return jsonify({
        "success": True,
        "message": "Irrigation advice generated successfully",
        "data": response_data
    })


@irrigation_bp.route("/api/irrigation/history", methods=["GET"])
@login_required
def irrigation_history():
    history = list(
        db.irrigation_history.find(
            {"userId": get_current_user_id()},
            {"_id": 0, "userId": 0}
        )
        .sort("createdAt", -1)
        .limit(10)
    )

    return jsonify({
        "success": True,
        "data": history
    })