const activityList = document.getElementById("activityList");
const refreshButton = document.getElementById("refreshButton");
const filterButtons = document.querySelectorAll(".filter-button");
const weatherCount = document.getElementById("weatherCount");
const cropCount = document.getElementById("cropCount");
const diseaseCount = document.getElementById("diseaseCount");
const fertilizerCount = document.getElementById("fertilizerCount");
const irrigationCount = document.getElementById("irrigationCount");
const marketCount = document.getElementById("marketCount");

let allActivities = [];
let selectedFilter = "all";


const endpoints = {
  crop: "/api/crop/history",
  disease: "/api/disease/history",
  fertilizer: "/api/fertilizer/history",
  irrigation: "/api/irrigation/history",
  market: "/api/market-prices/history",
  weather: "/api/weather/history"
};


function formatDate(dateValue) {
  if (!dateValue) {
    return "Unknown date";
  }

  return new Intl.DateTimeFormat("en-IN", {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(dateValue));
}


function formatPrice(price) {
  if (price === undefined || price === null) {
    return "₹0";
  }

  return `₹${Number(price).toLocaleString("en-IN")}`;
}


function getActivityDetails(type, item) {

  /* =========================
     CROP
  ========================== */

  if (type === "crop") {

    return {
      icon: "🌱",

      title:
        `Suggested crops: ${Array.isArray(item.recommendedCrops)
          ? item.recommendedCrops.join(", ")
          : "Crop recommendation"
        }`,

      description:
        `${item.soilType || "Unknown"} soil · ` +
        `${item.season || "Unknown"} season`
    };
  }
  if (type === "weather") {
    return {
      icon: "☀️",
      title: item.title || `${item.weather} weather guidance`,
      description:
        `${item.weather || "Unknown"} · ` +
        `Rain expected: ${item.rainExpected || "Unknown"} · ` +
        `${item.priority || "Unknown"} priority`
    };
  }


  /* =========================
     DISEASE
  ========================== */

  if (type === "disease") {

    return {
      icon: "🔎",

      title:
        item.disease || "Disease analysis",

      description:
        `${item.crop || "Unknown crop"} · ` +
        `${item.symptom || "Symptoms checked"} · ` +
        `${item.risk || "Unknown"} risk`
    };
  }


  /* =========================
     FERTILIZER
  ========================== */

  if (type === "fertilizer") {

    return {
      icon: "🧪",

      title:
        item.title || "Fertilizer advice",

      description:
        `${item.crop || "Unknown crop"} · ` +
        `${item.soilType || "Unknown"} soil · ` +
        `${item.stage || "Unknown"} stage`
    };
  }


  /* =========================
     IRRIGATION
  ========================== */

  if (type === "irrigation") {

    return {
      icon: "💧",

      title:
        item.status || "Irrigation advice",

      description:
        `${item.crop || "Unknown crop"} · ` +
        `${item.soilType || "Unknown"} soil · ` +
        `${item.moistureLevel ?? "Unknown"} moisture`
    };
  }


  /* =========================
     MARKET PRICE
  ========================== */

  if (type === "market") {

    return {
      icon: "₹",

      title:
        `${item.crop || "Crop"} price checked in ${item.market || "Market"
        }`,

      description:
        `Min ${formatPrice(item.minPrice)} · ` +
        `Max ${formatPrice(item.maxPrice)}`
    };
  }


  return {
    icon: "📋",
    title: "Farm activity",
    description: "Saved farming activity"
  };
}


function renderActivities() {

  const activities =
    selectedFilter === "all"
      ? allActivities
      : allActivities.filter(
        (activity) =>
          activity.type === selectedFilter
      );


  activityList.innerHTML = "";


  if (!activities.length) {

    const filterName =
      selectedFilter === "all"
        ? "farm activity"
        : `${selectedFilter} activity`;

    activityList.innerHTML = `
      <p class="empty-text">
        No saved ${filterName} found.
      </p>
    `;

    return;
  }


  activities.forEach((activity) => {

    const details =
      getActivityDetails(
        activity.type,
        activity.item
      );


    const card =
      document.createElement("article");

    card.className = "activity-card";


    /* ICON */

    const icon =
      document.createElement("span");

    icon.className = "activity-icon";

    icon.textContent =
      details.icon;


    /* MAIN */

    const main =
      document.createElement("div");

    main.className =
      "activity-main";


    /* TITLE */

    const title =
      document.createElement("h3");

    title.textContent =
      details.title;


    /* DESCRIPTION */

    const description =
      document.createElement("p");

    description.textContent =
      details.description;


    /* CHIP */

    const chip =
      document.createElement("span");

    chip.className =
      `type-chip ${activity.type}-chip`;

    chip.textContent =
      activity.type === "market"
        ? "MARKET PRICE"
        : activity.type.toUpperCase();


    main.appendChild(title);
    main.appendChild(description);
    main.appendChild(chip);


    /* DATE */

    const date =
      document.createElement("p");

    date.className =
      "activity-date";

    date.textContent =
      formatDate(
        activity.item.createdAt
      );


    /* CARD */

    card.appendChild(icon);
    card.appendChild(main);
    card.appendChild(date);

    activityList.appendChild(card);

  });
}


async function fetchHistory(type, url) {

  const response =
    await fetch(url, {
      method: "GET",
      credentials: "include"
    });


  let result;


  try {

    result =
      await response.json();

  } catch {

    throw new Error(
      `Invalid response from ${type} history API.`
    );

  }


  if (
    !response.ok ||
    !result.success
  ) {

    throw new Error(
      result.message ||
      `Could not load ${type} history.`
    );

  }


  const data =
    Array.isArray(result.data)
      ? result.data
      : [];


  return data.map((item) => ({
    type,
    item
  }));
}


async function loadHistory() {

  refreshButton.disabled = true;

  refreshButton.textContent =
    "Loading...";


  activityList.innerHTML = `
    <p class="loading-text">
      Loading your farm history...
    </p>
  `;


  try {

    const endpointEntries =
      Object.entries(endpoints);


    const results =
      await Promise.all(

        endpointEntries.map(
          ([type, url]) =>
            fetchHistory(type, url)
        )

      );


    allActivities =
      results
        .flat()
        .sort(
          (first, second) => {

            return (
              new Date(
                second.item.createdAt || 0
              ) -
              new Date(
                first.item.createdAt || 0
              )
            );

          }
        );


    /* =========================
       COUNTS
    ========================== */

    const counts = {};

    endpointEntries.forEach(
      ([type], index) => {

        counts[type] =
          results[index].length;

      }
    );


    if (cropCount) {
      cropCount.textContent =
        counts.crop || 0;
    }


    if (diseaseCount) {
      diseaseCount.textContent =
        counts.disease || 0;
    }


    if (fertilizerCount) {
      fertilizerCount.textContent =
        counts.fertilizer || 0;
    }


    if (irrigationCount) {
      irrigationCount.textContent =
        counts.irrigation || 0;
    }


    if (marketCount) {
      marketCount.textContent =
        counts.market || 0;
    }
    if (weatherCount) {
      weatherCount.textContent = counts.weather || 0;
    }


    renderActivities();


  } catch (error) {

    console.error(
      "Farm history error:",
      error
    );


    activityList.innerHTML = `
      <p class="error-text">
        ${error.message}
        Keep the Flask server running
        and refresh the page.
      </p>
    `;

  } finally {

    refreshButton.disabled = false;

    refreshButton.textContent =
      "↻ Refresh";

  }
}


/* =========================
   FILTER BUTTONS
========================== */

filterButtons.forEach((button) => {

  button.addEventListener(
    "click",
    () => {

      selectedFilter =
        button.dataset.filter;


      filterButtons.forEach(
        (item) =>
          item.classList.remove(
            "active"
          )
      );


      button.classList.add(
        "active"
      );


      renderActivities();

    }
  );

});


/* =========================
   REFRESH
========================== */

refreshButton.addEventListener(
  "click",
  loadHistory
);


/* =========================
   INITIAL LOAD
========================== */

loadHistory();