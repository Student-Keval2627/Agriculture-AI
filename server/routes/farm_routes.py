from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from config import db
from utils.auth_utils import get_current_user_id, login_required


farm_bp = Blueprint("farm", __name__, url_prefix="/api/farm")


def empty_profile():
    return {
        "farmName": "",
        "location": "",
        "farmArea": "",
        "soilType": "",
        "mainCrop": ""
    }


@farm_bp.route("/profile", methods=["GET"])
@login_required
def get_farm_profile():
    user_id = get_current_user_id()

    profile = db.farm_profiles.find_one(
        {"userId": user_id},
        {"_id": 0}
    )

    return jsonify({
        "success": True,
        "data": profile or empty_profile()
    })


@farm_bp.route("/profile", methods=["PUT"])
@login_required
def save_farm_profile():
    user_id = get_current_user_id()
    data = request.get_json(silent=True) or {}

    farm_name = str(data.get("farmName", "")).strip()
    location = str(data.get("location", "")).strip()
    farm_area = str(data.get("farmArea", "")).strip()
    soil_type = str(data.get("soilType", "")).strip()
    main_crop = str(data.get("mainCrop", "")).strip()

    if not all([farm_name, location, farm_area, soil_type, main_crop]):
        return jsonify({
            "success": False,
            "message": "Please fill in all farm details."
        }), 400

    now = datetime.now(timezone.utc).isoformat()

    profile_data = {
        "userId": user_id,
        "farmName": farm_name,
        "location": location,
        "farmArea": farm_area,
        "soilType": soil_type,
        "mainCrop": main_crop,
        "updatedAt": now
    }

    db.farm_profiles.update_one(
        {"userId": user_id},
        {
            "$set": profile_data,
            "$setOnInsert": {
                "createdAt": now
            }
        },
        upsert=True
    )

    return jsonify({
        "success": True,
        "message": "Farm profile saved successfully.",
        "data": profile_data
    })