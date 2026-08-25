(() => {
  const cropForm = document.getElementById("cropForm");
  const soilType = document.getElementById("soilType");
  const season = document.getElementById("season");
  const recommendButton = document.getElementById("recommendButton");
  const formMessage = document.getElementById("formMessage");

  const resultCard = document.getElementById("resultCard");
  const emptyState = document.getElementById("emptyState");
  const resultContent = document.getElementById("resultContent");
  const cropList = document.getElementById("cropList");
  const reasonText = document.getElementById("reasonText");

  if (!cropForm) return;

  const originalButtonText = recommendButton.textContent;

  function showMessage(message = "") {
    formMessage.textContent = message;
  }

  function getRecord(payload) {
    const data = payload?.data || payload;
    return Array.isArray(data) ? data[0] : data;
  }

  function showRecommendation(record) {
    const crops = Array.isArray(record.recommendedCrops)
      ? record.recommendedCrops
      : String(record.recommendedCrops || "")
          .split(",")
          .map((crop) => crop.trim())
          .filter(Boolean);

    cropList.replaceChildren();

    crops.forEach((crop) => {
      const chip = document.createElement("span");
      chip.className = "crop-chip";
      chip.textContent = crop;
      cropList.appendChild(chip);
    });

    reasonText.textContent =
      record.reason || "Suitable crops were selected using your soil type and season.";

    emptyState.classList.add("hidden");
    resultContent.classList.remove("hidden");
    resultCard.classList.add("has-result");
  }

  cropForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    showMessage("");

    const selectedSoil = soilType.value;
    const selectedSeason = season.value;

    if (!selectedSoil || !selectedSeason) {
      showMessage("Please select soil type and season.");
      return;
    }

    recommendButton.disabled = true;
    recommendButton.textContent = "Getting recommendation...";

    try {
      const response = await fetch("/api/crop/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "same-origin",
        body: JSON.stringify({
          soilType: selectedSoil,
          season: selectedSeason
        })
      });

      const payload = await response.json();

      if (!response.ok || payload.success === false) {
        throw new Error(payload.message || "Could not get crop recommendation.");
      }

      const record = getRecord(payload);

      if (!record || !record.recommendedCrops) {
        throw new Error("Recommendation data was not received.");
      }

      showRecommendation(record);
    } catch (error) {
      showMessage(error.message || "Failed to fetch crop recommendation.");
    } finally {
      recommendButton.disabled = false;
      recommendButton.textContent = originalButtonText;
    }
  });
})();