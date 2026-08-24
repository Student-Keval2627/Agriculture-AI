DISEASE_RULES = {
    ("tomato", "brown spots"): {
        "disease": "Possible Early Blight",
        "risk": "Medium",
        "description": "Brown spots on tomato leaves can be a sign of early blight.",
        "advice": [
            "Remove badly affected leaves.",
            "Avoid watering leaves in the evening.",
            "Keep proper space between plants.",
            "Consult a local agriculture officer before using any treatment."
        ]
    },
    ("tomato", "white powder"): {
        "disease": "Possible Powdery Mildew",
        "risk": "Medium",
        "description": "White powder-like marks may indicate powdery mildew.",
        "advice": [
            "Remove infected leaves.",
            "Improve air flow around the plant.",
            "Avoid excess humidity.",
            "Ask a local agriculture expert for suitable treatment."
        ]
    },
    ("cotton", "leaf curl"): {
        "disease": "Possible Cotton Leaf Curl Disease",
        "risk": "High",
        "description": "Curled cotton leaves can indicate leaf curl disease.",
        "advice": [
            "Separate severely affected plants.",
            "Keep the field clean from weeds.",
            "Monitor whitefly activity.",
            "Contact a local agriculture officer quickly."
        ]
    },
    ("potato", "brown spots"): {
        "disease": "Possible Early Blight",
        "risk": "Medium",
        "description": "Brown circular spots on potato leaves may indicate early blight.",
        "advice": [
            "Remove infected leaves carefully.",
            "Do not overwater the crop.",
            "Use clean farming tools.",
            "Consult a local agriculture officer for treatment."
        ]
    },
    ("wheat", "white powder"): {
        "disease": "Possible Powdery Mildew",
        "risk": "Medium",
        "description": "White powder-like growth on wheat may indicate powdery mildew.",
        "advice": [
            "Check the affected area regularly.",
            "Avoid excess nitrogen fertilizer.",
            "Maintain field air circulation.",
            "Consult an agriculture expert before treatment."
        ]
    },
    ("rice", "yellow leaves"): {
        "disease": "Possible Nutrient Deficiency",
        "risk": "Low",
        "description": "Yellow rice leaves can happen because of nutrient deficiency or water stress.",
        "advice": [
            "Check water level in the field.",
            "Check soil nutrient condition.",
            "Remove damaged leaves if needed.",
            "Take local agriculture guidance before applying fertilizer."
        ]
    }
}


def get_disease_advice(crop, symptom):
    crop_name = crop.strip().lower()
    symptom_name = symptom.strip().lower()

    result = DISEASE_RULES.get((crop_name, symptom_name))

    if result:
        return result

    return {
        "disease": "Needs Further Inspection",
        "risk": "Unknown",
        "description": "The selected crop and symptom need a closer field inspection.",
        "advice": [
            "Take clear photos of the affected plant.",
            "Check if the problem is spreading.",
            "Remove severely affected leaves if safe.",
            "Consult a local agriculture officer for correct diagnosis."
        ]
    }