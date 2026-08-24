FERTILIZER_RULES = {
    ("tomato", "loamy", "flowering"): {
        "title": "Balanced nutrient support",
        "priority": "Medium",
        "description": "Tomato plants at the flowering stage need balanced nutrition and stable watering.",
        "tips": [
            "Check soil moisture before watering.",
            "Use only the fertilizer plan advised by your local agriculture officer.",
            "Avoid applying excess nitrogen at flowering stage.",
            "Remove weak or damaged leaves."
        ]
    },
    ("cotton", "black", "growth"): {
        "title": "Growth-stage soil support",
        "priority": "Medium",
        "description": "Cotton growing in black soil benefits from moisture management and balanced nutrients.",
        "tips": [
            "Avoid waterlogging in the field.",
            "Check plants regularly for pest activity.",
            "Use soil-test guidance before applying fertilizer.",
            "Keep weeds under control."
        ]
    },
    ("rice", "alluvial", "growth"): {
        "title": "Rice growth support",
        "priority": "Medium",
        "description": "Rice in alluvial soil requires proper water level and nutrient monitoring.",
        "tips": [
            "Maintain the required water level.",
            "Observe leaf colour for nutrient stress.",
            "Use fertilizer only according to local guidance.",
            "Keep field drainage channels clean."
        ]
    },
    ("wheat", "alluvial", "growth"): {
        "title": "Wheat growth support",
        "priority": "Low",
        "description": "Wheat in fertile alluvial soil usually needs regular moisture and field monitoring.",
        "tips": [
            "Avoid overwatering the field.",
            "Check for yellow leaves or pest damage.",
            "Follow soil-test recommendations.",
            "Keep the crop area weed-free."
        ]
    },
    ("potato", "loamy", "growth"): {
        "title": "Potato crop support",
        "priority": "Medium",
        "description": "Loamy soil is suitable for potatoes when moisture and drainage are managed well.",
        "tips": [
            "Maintain loose and well-drained soil.",
            "Avoid standing water near plants.",
            "Check leaves for spots or wilting.",
            "Get local advice before applying fertilizer."
        ]
    }
}


def get_fertilizer_advice(crop, soil_type, stage):
    key = (
        crop.strip().lower(),
        soil_type.strip().lower(),
        stage.strip().lower()
    )

    result = FERTILIZER_RULES.get(key)

    if result:
        return result

    return {
        "title": "General soil care advice",
        "priority": "Low",
        "description": "A soil test is the best way to decide the right fertilizer plan for your crop.",
        "tips": [
            "Check soil moisture and drainage.",
            "Use compost or organic matter when suitable.",
            "Do not apply fertilizer without local guidance.",
            "Consult an agriculture officer for a crop-specific plan."
        ]
    }