from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from config import db
from services.crop_service import get_crop_recommendation
from utils.auth_utils import get_current_user_id, login_required


crop_bp = Blueprint("crop_bp", __name__)


@crop_bp.route("/api/crop/recommend", methods=["POST"])
@login_required
def recommend_crop():
    data = request.get_json(silent=True) or {}

    soil_type = str(data.get("soilType", "")).strip()
    season = str(data.get("season", "")).strip()

    if not soil_type or not season:
        return jsonify({
            "success": False,
            "message": "Soil type and season are required"
        }), 400

    recommendation = get_crop_recommendation(
        soil_type,
        season
    )

    history_data = {
        "userId": get_current_user_id(),
        "soilType": soil_type,
        "season": season,
        "recommendedCrops": recommendation["crops"],
        "reason": recommendation["reason"],
        "createdAt": datetime.now(
            timezone.utc
        ).isoformat()
    }

    db.crop_history.insert_one(
        history_data.copy()
    )

    response_data = history_data.copy()

    response_data.pop(
        "userId",
        None
    )

    return jsonify({
        "success": True,
        "message": "Crop recommendation generated successfully",
        "data": response_data
    })


@crop_bp.route("/api/crop/history", methods=["GET"])
@login_required
def crop_history():

    history = list(
        db.crop_history.find(
            {
                "userId": get_current_user_id()
            },
            {
                "_id": 0,
                "userId": 0
            }
        )
        .sort("createdAt", -1)
        .limit(10)
    )

    return jsonify({
        "success": True,
        "data": history
    })