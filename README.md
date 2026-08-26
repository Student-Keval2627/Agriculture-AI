# 🌿 Agriculture AI

Agriculture AI is a farmer-friendly smart agriculture web application designed to help farmers make better farming decisions using simple digital tools.

The system provides crop recommendations, fertilizer guidance, irrigation advice, disease assistance, weather-based farming guidance, market prices, farm records, and activity history in one dashboard.

---

## 🌾 Project Overview

Agriculture AI focuses on providing a simple and easy-to-use farming assistant.

The interface is designed so that farmers can quickly access important farming tools without dealing with a complicated system.

The application stores farmer information and activity history in MongoDB and uses a Flask backend to process requests.

---

## ✨ Features

### 🌱 Crop Recommendation

- Select soil type
- Select farming season
- Get suitable crop recommendations
- View recommendation reasons
- Save recommendations in MongoDB

### 🧪 Fertilizer Advisor

- Select crop
- Select soil type
- Select crop growth stage
- Get fertilizer guidance
- Save advice history

### 💧 Irrigation Advisor

- Enter crop information
- Select soil type
- Provide moisture information
- Get irrigation recommendations
- Save irrigation history

### 🔎 Disease Advisor

- Enter crop name
- Enter crop symptoms
- Get possible disease guidance
- View risk information
- Save disease checks

### ☀️ Weather Advisor

- Select current weather condition
- Select whether rain is expected
- Get weather-based farming guidance
- View priority level
- Save weather advice in MongoDB

### ₹ Market Prices

- Select crop
- Select market
- Check minimum crop price
- Check maximum crop price
- View market price trends
- Store market searches in MongoDB

### 🚜 My Farm

- Save farmer farm information
- Store farm profile
- Update farm details
- Access farm information from the dashboard

### ◷ Farm History

View all saved activities in one place.

Available filters:

- 🌱 Crop
- 🔎 Disease
- 🧪 Fertilizer
- 💧 Irrigation
- ₹ Market
- ☀️ Weather

### 🔐 Authentication

- Farmer registration
- Farmer login
- Session-based authentication
- Protected pages
- Global logout
- Automatic redirect to login for unauthorized users

---

## 🖥️ Dashboard

The Agriculture AI dashboard provides quick access to all farming tools.

Dashboard includes:

- Latest crop recommendation
- Saved crop plans
- Latest suggested crop
- Last recommendation date
- Farm profile shortcut
- Crop Recommendation
- Fertilizer Advisor
- Irrigation Advisor
- Disease Advisor
- Weather Advisor
- Market Prices
- Farm History
- Logout

---

## 🛠️ Tech Stack

### Frontend

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

### Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

### Database

![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)

### Development Tools

![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

---

## 📂 Project Structure

```text
AgricultureAI/
│
├── client/
│   │
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   │
│   ├── pages/
│   │   ├── crop-recommendation.html
│   │   ├── fertilizer-advisor.html
│   │   ├── irrigation-advisor.html
│   │   ├── disease-detection.html
│   │   ├── weather-advisor.html
│   │   ├── market-prices.html
│   │   ├── farm-history.html
│   │   └── my-farm.html
│   │
│   ├── css/
│   │   ├── dashboard.css
│   │   ├── crop-recommendation.css
│   │   ├── farm-history.css
│   │   └── market-prices.css
│   │
│   └── js/
│       ├── dashboard.js
│       ├── auth.js
│       ├── crop.js
│       ├── fertilizer.js
│       ├── irrigation.js
│       ├── disease.js
│       ├── weather.js
│       ├── market-prices.js
│       ├── farm-history.js
│       └── app-controls.js
│
├── server/
│   │
│   ├── app.py
│   ├── config.py
│   ├── seed_market_prices.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── crop_routes.py
│   │   ├── disease_routes.py
│   │   ├── fertilizer_routes.py
│   │   ├── irrigation_routes.py
│   │   ├── weather_routes.py
│   │   ├── market_routes.py
│   │   └── farm_routes.py
│   │
│   ├── services/
│   │   └── crop_service.py
│   │
│   └── utils/
│       ├── auth_utils.py
│       └── localization.py
│
└── README.md
