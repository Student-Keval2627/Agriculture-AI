const cropSelect = document.getElementById("cropSelect");
const marketSelect = document.getElementById("marketSelect");

const checkPriceButton = document.querySelector(".check-price-button");
const refreshPriceButton = document.querySelector(".refresh-price-button");

const priceTable = document.querySelector(".price-table");
const marketStatus = document.querySelector(".market-status");
console.log("Market Prices JS connected");


const API_BASE =
  window.location.port === "5000"
    ? ""
    : "http://127.0.0.1:5000";


const cropIcons = {
  Wheat: "🌾",
  Cotton: "☁️",
  Groundnut: "🥜",
  Maize: "🌽",
  Soybean: "🌱",
  Onion: "🧅",
  Potato: "🥔",
  Tomato: "🍅"
};


function formatPrice(price) {
  return `₹${Number(price).toLocaleString("en-IN")}`;
}


function getTrendHTML(trend) {
  const value = Number(trend);

  if (value >= 0) {
    return `
      <span class="trend-up">
        ↑ ${Math.abs(value).toFixed(1)}%
      </span>
    `;
  }

  return `
    <span class="trend-down">
      ↓ ${Math.abs(value).toFixed(1)}%
    </span>
  `;
}


function createPriceRow(item) {
  const icon = cropIcons[item.crop] || "🌱";

  return `
    <div class="price-row">

      <div class="crop-cell">

        <div class="crop-avatar">
          ${icon}
        </div>

        <div>
          <strong>${item.crop}</strong>
          <p>${item.category}</p>
        </div>

      </div>

      <span class="market-location">
        ${item.market}
      </span>

      <span class="price-value">
        ${formatPrice(item.minPrice)}
      </span>

      <span class="price-value max-price">
        ${formatPrice(item.maxPrice)}
      </span>

      ${getTrendHTML(item.trend)}

    </div>
  `;
}


function renderPrices(prices) {
  if (!priceTable) {
    return;
  }

  priceTable.innerHTML = `
    <div class="price-table-header">
      <span>Crop</span>
      <span>Market</span>
      <span>Min Price</span>
      <span>Max Price</span>
      <span>Trend</span>
    </div>

    ${prices.map(createPriceRow).join("")}
  `;
}


function renderMessage(message, type = "normal") {
  if (!priceTable) {
    return;
  }

  let className = "loading-text";

  if (type === "error") {
    className = "error-text";
  }

  priceTable.innerHTML = `
    <div style="padding: 25px;">
      <p class="${className}">
        ${message}
      </p>
    </div>
  `;
}


async function loadAllPrices() {
  try {
    marketStatus.textContent = "● Loading...";

    renderMessage("Loading market prices...");

    const response = await fetch(
      `${API_BASE}/api/market-prices`,
      {
        method: "GET",
        credentials: "include"
      }
    );

    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(
        data.message || "Unable to load market prices"
      );
    }

    renderPrices(data.prices);

    marketStatus.textContent = "● Backend connected";

  } catch (error) {
    console.error(error);

    marketStatus.textContent = "● Connection failed";

    renderMessage(
      "Unable to connect to the Market Prices server.",
      "error"
    );
  }
}


async function checkSelectedPrice() {
  const crop = cropSelect.value;
  const market = marketSelect.value;

  if (!crop) {
    alert("Please select a crop.");
    cropSelect.focus();
    return;
  }

  if (!market) {
    alert("Please select a market.");
    marketSelect.focus();
    return;
  }

  try {
    checkPriceButton.disabled = true;
    checkPriceButton.textContent = "Checking...";

    marketStatus.textContent = "● Searching...";

    const response = await fetch(
      `${API_BASE}/api/market-prices`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        credentials: "include",

        body: JSON.stringify({
          crop,
          market
        })
      }
    );

    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(
        data.message || "Price not found"
      );
    }

    renderPrices([data.price]);

    marketStatus.textContent = "● Price found";

  } catch (error) {
    console.error(error);

    marketStatus.textContent = "● No result";

    renderMessage(
      error.message,
      "error"
    );

  } finally {
    checkPriceButton.disabled = false;
    checkPriceButton.textContent = "Check Price →";
  }
}


checkPriceButton?.addEventListener(
  "click",
  checkSelectedPrice
);


refreshPriceButton?.addEventListener(
  "click",
  () => {
    cropSelect.value = "";
    marketSelect.value = "";

    loadAllPrices();
  }
);


document.addEventListener(
  "DOMContentLoaded",
  loadAllPrices
);