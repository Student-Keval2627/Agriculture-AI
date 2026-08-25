from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from config import db
from utils.auth_utils import get_current_user_id, login_required


weather_bp = Blueprint("weather", __name__, url_prefix="/api/weather")


WEATHER_GUIDANCE = {
    "Sunny": {
        "title": "Sunny field guidance",
        "priority": "Medium",
        "advice": [
            "Water early morning or late evening to reduce water loss.",
            "Avoid applying fertilizer during the hottest hours.",
            "Check young plants for heat stress."
        ]
    },
    "Cloudy": {
        "title": "Cloudy field guidance",
        "priority": "Low",
        "advice": [
            "Check soil moisture before irrigating.",
            "Monitor leaves for fungal symptoms if humidity stays high.",
            "Use the cooler weather for field inspection."
        ]
    },
    "Rainy": {
        "title": "Rainy field guidance",
        "priority": "High",
        "advice": [
            "Avoid irrigation until soil moisture is checked.",
            "Ensure field drainage is clear.",
            "Delay fertilizer or pesticide application during heavy rain."
        ]
    },
    "Windy": {
        "title": "Windy field guidance",
        "priority": "Medium",
        "advice": [
            "Avoid spraying fertilizer or pesticide in strong wind.",
            "Check support for young or tall crops.",
            "Water the soil slowly to reduce moisture loss."
        ]
    }
}


@weather_bp.route("/advice", methods=["POST"])
@login_required
def get_weather_advice():
    user_id = get_current_user_id()
    data = request.get_json(silent=True) or {}

    weather = str(data.get("weather", "")).strip()
    rain_expected = str(data.get("rainExpected", "")).strip()

    if weather not in WEATHER_GUIDANCE or rain_expected not in ["Yes", "No"]:
        return jsonify({
            "success": False,
            "message": "Please select weather condition and rain expectation."
        }), 400

    guidance = WEATHER_GUIDANCE[weather]
    advice = list(guidance["advice"])

    if rain_expected == "Yes":
        advice.append("Keep irrigation low and inspect drainage before rain starts.")
    else:
        advice.append("Plan irrigation according to your crop and current soil moisture.")

    result = {
        "userId": user_id,
        "weather": weather,
        "rainExpected": rain_expected,
        "title": guidance["title"],
        "priority": guidance["priority"],
        "advice": advice,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    db.weather_history.insert_one(result)

    response_data = result.copy()
    response_data.pop("_id", None)
    response_data.pop("userId", None)

    return jsonify({
        "success": True,
        "data": response_data
    })