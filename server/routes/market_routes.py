from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from config import db
from utils.auth_utils import get_current_user_id, login_required


market_bp = Blueprint("market_bp", __name__)


# =========================================================
# GET ALL MARKET PRICES
# =========================================================

@market_bp.route("/api/market-prices", methods=["GET"])
@login_required
def get_market_prices():

    prices = list(
        db.market_prices.find(
            {},
            {
                "_id": 0,
                "cropKey": 0,
                "marketKey": 0
            }
        ).sort("crop", 1)
    )

    return jsonify({
        "success": True,
        "count": len(prices),
        "prices": prices,
        "message": "Market prices loaded successfully"
    })


# =========================================================
# CHECK SELECTED CROP + MARKET PRICE
# =========================================================

@market_bp.route("/api/market-prices", methods=["POST"])
@login_required
def find_market_price():

    data = request.get_json(silent=True) or {}

    crop = str(data.get("crop", "")).strip()
    market = str(data.get("market", "")).strip()

    if not crop:
        return jsonify({
            "success": False,
            "message": "Please select a crop"
        }), 400

    if not market:
        return jsonify({
            "success": False,
            "message": "Please select a market"
        }), 400


    # Search market price from MongoDB
    result = db.market_prices.find_one(
        {
            "cropKey": crop.lower(),
            "marketKey": market.lower()
        },
        {
            "_id": 0,
            "cropKey": 0,
            "marketKey": 0
        }
    )


    if result is None:
        return jsonify({
            "success": False,
            "message": f"No market price found for {crop} in {market}"
        }), 404


    # Save farmer search history
    history_data = {
        "userId": get_current_user_id(),
        "crop": result["crop"],
        "market": result["market"],
        "minPrice": result["minPrice"],
        "maxPrice": result["maxPrice"],
        "trend": result.get("trend", 0),
        "createdAt": datetime.now(timezone.utc).isoformat()
    }


    db.market_search_history.insert_one(
        history_data.copy()
    )


    return jsonify({
        "success": True,
        "price": result,
        "message": "Market price found successfully"
    })


# =========================================================
# MARKET PRICE SEARCH HISTORY
# =========================================================

@market_bp.route(
    "/api/market-prices/history",
    methods=["GET"]
)
@login_required
def market_price_history():

    history = list(
        db.market_search_history.find(
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