const activityList = document.getElementById("activityList");
const refreshButton = document.getElementById("refreshButton");
const filterButtons = document.querySelectorAll(".filter-button");

const cropCount = document.getElementById("cropCount");
const diseaseCount = document.getElementById("diseaseCount");
const fertilizerCount = document.getElementById("fertilizerCount");
const irrigationCount = document.getElementById("irrigationCount");

let allActivities = [];
let selectedFilter = "all";

const endpoints = {
  crop: "/api/crop/history",
  disease: "/api/disease/history",
  fertilizer: "/api/fertilizer/history",
  irrigation: "/api/irrigation/history"
};

function formatDate(dateValue) {
  return new Intl.DateTimeFormat("en-IN", {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(dateValue));
}

function getActivityDetails(type, item) {
  if (type === "crop") {
    return {
      icon: "🌱",
      title: `Suggested crops: ${item.recommendedCrops.join(", ")}`,
      description: `${item.soilType} soil · ${item.season} season`
    };
  }

  if (type === "disease") {
    return {
      icon: "🔎",
      title: item.disease,
      description: `${item.crop} · ${item.symptom} · ${item.risk} risk`
    };
  }

  if (type === "fertilizer") {
    return {
      icon: "🧪",
      title: item.title,
      description: `${item.crop} · ${item.soilType} soil · ${item.stage} stage`
    };
  }

  return {
    icon: "💧",
    title: item.status,
    description: `${item.crop} · ${item.soilType} soil · ${item.moistureLevel} moisture`
  };
}

function renderActivities() {
  const activities = selectedFilter === "all"
    ? allActivities
    : allActivities.filter((activity) => activity.type === selectedFilter);

  activityList.innerHTML = "";

  if (!activities.length) {
    activityList.innerHTML = `<p class="empty-text">No saved ${selectedFilter === "all" ? "farm activity" : selectedFilter + " activity"} found.</p>`;
    return;
  }

  activities.forEach((activity) => {
    const details = getActivityDetails(activity.type, activity.item);

    const card = document.createElement("article");
    card.className = "activity-card";

    const icon = document.createElement("span");
    icon.className = "activity-icon";
    icon.textContent = details.icon;

    const main = document.createElement("div");
    main.className = "activity-main";

    const title = document.createElement("h3");
    title.textContent = details.title;

    const description = document.createElement("p");
    description.textContent = details.description;

    const chip = document.createElement("span");
    chip.className = "type-chip";
    chip.textContent = activity.type.toUpperCase();

    main.appendChild(title);
    main.appendChild(description);
    main.appendChild(chip);

    const date = document.createElement("p");
    date.className = "activity-date";
    date.textContent = formatDate(activity.item.createdAt);

    card.appendChild(icon);
    card.appendChild(main);
    card.appendChild(date);

    activityList.appendChild(card);
  });
}

async function loadHistory() {
  refreshButton.disabled = true;
  refreshButton.textContent = "Loading...";

  activityList.innerHTML = `<p class="loading-text">Loading your farm history...</p>`;

  try {
    const results = await Promise.all(
      Object.entries(endpoints).map(async ([type, url]) => {
        const response = await fetch(url);
        const result = await response.json();

        if (!response.ok || !result.success) {
          throw new Error(`Could not load ${type} history.`);
        }

        return result.data.map((item) => ({ type, item }));
      })
    );

    allActivities = results.flat().sort((first, second) => {
      return new Date(second.item.createdAt) - new Date(first.item.createdAt);
    });

    cropCount.textContent = results[0].length;
    diseaseCount.textContent = results[1].length;
    fertilizerCount.textContent = results[2].length;
    irrigationCount.textContent = results[3].length;

    renderActivities();
  } catch (error) {
    activityList.innerHTML = `<p class="error-text">${error.message} Keep the Flask server running and refresh the page.</p>`;
  } finally {
    refreshButton.disabled = false;
    refreshButton.textContent = "↻ Refresh";
  }
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    selectedFilter = button.dataset.filter;

    filterButtons.forEach((item) => item.classList.remove("active"));
    button.classList.add("active");

    renderActivities();
  });
});

refreshButton.addEventListener("click", loadHistory);

loadHistory();