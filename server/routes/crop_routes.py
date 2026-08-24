from datetime import datetime, timezone
from flask import Blueprint, jsonify, request

from config import db
from services.crop_service import get_crop_recommendation

crop_bp = Blueprint("crop_bp", __name__)


@crop_bp.route("/api/crop/recommend", methods=["POST"])
def recommend_crop():
    data = request.get_json(silent=True) or {}

    soil_type = str(data.get("soilType", "")).strip()
    season = str(data.get("season", "")).strip()

    if not soil_type or not season:
        return jsonify({
            "success": False,
            "message": "Soil type and season are required"
        }), 400

    recommendation = get_crop_recommendation(soil_type, season)

    history_data = {
        "soilType": soil_type,
        "season": season,
        "recommendedCrops": recommendation["crops"],
        "reason": recommendation["reason"],
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    db.crop_history.insert_one(history_data.copy())

    return jsonify({
        "success": True,
        "message": "Crop recommendation generated successfully",
        "data": history_data
    })


@crop_bp.route("/api/crop/history", methods=["GET"])
def crop_history():
    history = list(
        db.crop_history.find({}, {"_id": 0})
        .sort("createdAt", -1)
        .limit(10)
    )

    return jsonify({
        "success": True,
        "data": history
    })