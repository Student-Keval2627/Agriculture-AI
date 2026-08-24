from datetime import datetime, timezone
from flask import Blueprint, jsonify, request

from config import db
from services.fertilizer_service import get_fertilizer_advice

fertilizer_bp = Blueprint("fertilizer_bp", __name__)


@fertilizer_bp.route("/api/fertilizer/advice", methods=["POST"])
def fertilizer_advice():
    data = request.get_json(silent=True) or {}

    crop = str(data.get("crop", "")).strip()
    soil_type = str(data.get("soilType", "")).strip()
    stage = str(data.get("stage", "")).strip()

    if not crop or not soil_type or not stage:
        return jsonify({
            "success": False,
            "message": "Crop, soil type, and crop stage are required"
        }), 400

    advice = get_fertilizer_advice(crop, soil_type, stage)

    history_data = {
        "crop": crop,
        "soilType": soil_type,
        "stage": stage,
        "title": advice["title"],
        "priority": advice["priority"],
        "description": advice["description"],
        "tips": advice["tips"],
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    db.fertilizer_history.insert_one(history_data.copy())

    return jsonify({
        "success": True,
        "message": "Fertilizer advice generated successfully",
        "data": history_data
    })


@fertilizer_bp.route("/api/fertilizer/history", methods=["GET"])
def fertilizer_history():
    history = list(
        db.fertilizer_history.find({}, {"_id": 0})
        .sort("createdAt", -1)
        .limit(10)
    )

    return jsonify({
        "success": True,
        "data": history
    })