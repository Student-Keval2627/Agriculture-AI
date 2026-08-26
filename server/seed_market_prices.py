from config import db


market_prices = [

    {
        "crop": "Wheat",
        "cropKey": "wheat",
        "category": "Food grain",
        "market": "Amreli",
        "marketKey": "amreli",
        "minPrice": 2350,
        "maxPrice": 2620,
        "trend": 4.2
    },

    {
        "crop": "Cotton",
        "cropKey": "cotton",
        "category": "Cash crop",
        "market": "Rajkot",
        "marketKey": "rajkot",
        "minPrice": 6850,
        "maxPrice": 7250,
        "trend": 2.8
    },

    {
        "crop": "Groundnut",
        "cropKey": "groundnut",
        "category": "Oilseed crop",
        "market": "Amreli",
        "marketKey": "amreli",
        "minPrice": 5250,
        "maxPrice": 5680,
        "trend": 1.9
    },

    {
        "crop": "Maize",
        "cropKey": "maize",
        "category": "Food grain",
        "market": "Ahmedabad",
        "marketKey": "ahmedabad",
        "minPrice": 1950,
        "maxPrice": 2180,
        "trend": -1.1
    },

    {
        "crop": "Onion",
        "cropKey": "onion",
        "category": "Vegetable",
        "market": "Surat",
        "marketKey": "surat",
        "minPrice": 1580,
        "maxPrice": 1920,
        "trend": 5.6
    },

    {
        "crop": "Soybean",
        "cropKey": "soybean",
        "category": "Oilseed crop",
        "market": "Rajkot",
        "marketKey": "rajkot",
        "minPrice": 4250,
        "maxPrice": 4680,
        "trend": 1.4
    },

    {
        "crop": "Potato",
        "cropKey": "potato",
        "category": "Vegetable",
        "market": "Ahmedabad",
        "marketKey": "ahmedabad",
        "minPrice": 1250,
        "maxPrice": 1540,
        "trend": -0.8
    },

    {
        "crop": "Tomato",
        "cropKey": "tomato",
        "category": "Vegetable",
        "market": "Surat",
        "marketKey": "surat",
        "minPrice": 1800,
        "maxPrice": 2250,
        "trend": 3.7
    }

]


db.market_prices.delete_many({})

db.market_prices.insert_many(
    market_prices
)


print("-------------------------------------")
print("Market prices added successfully.")
print("Total records:", len(market_prices))
print("-------------------------------------")