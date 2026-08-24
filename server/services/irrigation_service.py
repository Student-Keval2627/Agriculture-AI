def get_irrigation_advice(crop, soil_type, moisture_level):
    crop_name = crop.strip().lower()
    soil = soil_type.strip().lower()
    moisture = moisture_level.strip().lower()

    if moisture == "dry":
        return {
            "status": "Water Needed",
            "priority": "High",
            "description": f"The {soil} soil appears dry. Your {crop_name} crop may need irrigation soon.",
            "tips": [
                "Check soil moisture below the top surface before watering.",
                "Water slowly to avoid runoff.",
                "Irrigate during cooler morning or evening hours.",
                "Avoid standing water around plant roots."
            ]
        }

    if moisture == "wet":
        return {
            "status": "Do Not Irrigate Now",
            "priority": "Low",
            "description": f"The {soil} soil is already wet. Extra water may harm the {crop_name} crop.",
            "tips": [
                "Do not add more water until the soil becomes less wet.",
                "Check drainage channels for waterlogging.",
                "Observe roots and leaves for stress.",
                "Keep the field free from standing water."
            ]
        }

    if crop_name == "rice":
        return {
            "status": "Maintain Field Water Level",
            "priority": "Medium",
            "description": "Rice needs regular field-water monitoring during normal moisture conditions.",
            "tips": [
                "Maintain the suitable water level for your rice stage.",
                "Check field bunds for water leakage.",
                "Avoid unnecessary overwatering.",
                "Follow local agriculture guidance for irrigation timing."
            ]
        }

    return {
        "status": "Monitor Moisture",
        "priority": "Medium",
        "description": f"The {soil} soil has normal moisture for your {crop_name} crop.",
        "tips": [
            "Check the soil again before the next irrigation.",
            "Water only when the root area begins to dry.",
            "Use proper drainage to avoid waterlogging.",
            "Adjust irrigation based on local weather conditions."
        ]
    }