from flask import Blueprint, jsonify, request


market_bp = Blueprint("market", __name__)


MARKET_PRICES = [
    {
        "crop": "Wheat",
        "category": "Food grain",
        "market": "Amreli",
        "minPrice": 2350,
        "maxPrice": 2620,
        "trend": 4.2
    },
    {
        "crop": "Cotton",
        "category": "Cash crop",
        "market": "Rajkot",
        "minPrice": 6850,
        "maxPrice": 7250,
        "trend": 2.8
    },
    {
        "crop": "Groundnut",
        "category": "Oilseed crop",
        "market": "Amreli",
        "minPrice": 5250,
        "maxPrice": 5680,
        "trend": 1.9
    },
    {
        "crop": "Maize",
        "category": "Food grain",
        "market": "Ahmedabad",
        "minPrice": 1950,
        "maxPrice": 2180,
        "trend": -1.1
    },
    {
        "crop": "Onion",
        "category": "Vegetable",
        "market": "Surat",
        "minPrice": 1580,
        "maxPrice": 1920,
        "trend": 5.6
    },
    {
        "crop": "Soybean",
        "category": "Oilseed crop",
        "market": "Rajkot",
        "minPrice": 4250,
        "maxPrice": 4680,
        "trend": 1.4
    },
    {
        "crop": "Potato",
        "category": "Vegetable",
        "market": "Ahmedabad",
        "minPrice": 1250,
        "maxPrice": 1540,
        "trend": -0.8
    },
    {
        "crop": "Tomato",
        "category": "Vegetable",
        "market": "Surat",
        "minPrice": 1800,
        "maxPrice": 2250,
        "trend": 3.7
    }
]


@market_bp.route("/api/market-prices", methods=["GET"])
def get_market_prices():
    return jsonify({
        "success": True,
        "count": len(MARKET_PRICES),
        "prices": MARKET_PRICES,
        "message": "Market price data loaded successfully"
    })


@market_bp.route("/api/market-prices", methods=["POST"])
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

    result = next(
        (
            item
            for item in MARKET_PRICES
            if item["crop"].lower() == crop.lower()
            and item["market"].lower() == market.lower()
        ),
        None
    )

    if result is None:
        return jsonify({
            "success": False,
            "message": f"No market price found for {crop} in {market}"
        }), 404

    return jsonify({
        "success": True,
        "price": result,
        "message": "Market price found successfully"
    })