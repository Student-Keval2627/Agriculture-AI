CROP_RULES = {
    ("black", "kharif"): {
        "crops": ["Cotton", "Soybean", "Groundnut"],
        "reason": "Black soil stores moisture well and is suitable for these Kharif crops."
    },
    ("black", "rabi"): {
        "crops": ["Wheat", "Gram", "Mustard"],
        "reason": "Black soil can support Rabi crops when irrigation is available."
    },
    ("alluvial", "kharif"): {
        "crops": ["Rice", "Maize", "Sugarcane"],
        "reason": "Alluvial soil is fertile and suitable for water-loving crops."
    },
    ("alluvial", "rabi"): {
        "crops": ["Wheat", "Potato", "Mustard"],
        "reason": "Alluvial soil provides good nutrients for these Rabi crops."
    },
    ("red", "kharif"): {
        "crops": ["Groundnut", "Millet", "Pigeon Pea"],
        "reason": "Red soil is suitable for drought-resistant Kharif crops."
    },
    ("loamy", "kharif"): {
        "crops": ["Rice", "Maize", "Vegetables"],
        "reason": "Loamy soil has a balanced mixture of sand, clay, and nutrients."
    },
    ("loamy", "rabi"): {
        "crops": ["Wheat", "Tomato", "Potato"],
        "reason": "Loamy soil supports many winter crops very well."
    }
}


def get_crop_recommendation(soil_type, season):
    soil = soil_type.strip().lower()
    crop_season = season.strip().lower()

    recommendation = CROP_RULES.get((soil, crop_season))

    if recommendation:
        return recommendation

    return {
        "crops": ["Millet", "Pigeon Pea", "Groundnut"],
        "reason": "These crops are generally suitable for many Indian soil types and climates."
    }