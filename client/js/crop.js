const cropForm = document.getElementById("cropForm");
const soilType = document.getElementById("soilType");
const season = document.getElementById("season");
const recommendButton = document.getElementById("recommendButton");
const formMessage = document.getElementById("formMessage");

const emptyState = document.getElementById("emptyState");
const resultContent = document.getElementById("resultContent");
const cropList = document.getElementById("cropList");
const reasonText = document.getElementById("reasonText");

cropForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  formMessage.textContent = "";

  if (!soilType.value || !season.value) {
    formMessage.textContent = "Please select both soil type and season.";
    return;
  }

  recommendButton.disabled = true;
  recommendButton.textContent = "Finding suitable crops...";

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/crop/recommend",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          soilType: soilType.value,
          season: season.value
        })
      }
    );

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(result.message || "Recommendation could not be generated.");
    }

    cropList.innerHTML = "";

    result.data.recommendedCrops.forEach((crop) => {
      const cropTag = document.createElement("span");
      cropTag.className = "crop-tag";
      cropTag.textContent = crop;
      cropList.appendChild(cropTag);
    });

    reasonText.textContent = result.data.reason;

    emptyState.classList.add("hidden");
    resultContent.classList.remove("hidden");
  } catch (error) {
    formMessage.textContent = error.message;
  } finally {
    recommendButton.disabled = false;
    recommendButton.textContent = "Get crop recommendation";
  }
});