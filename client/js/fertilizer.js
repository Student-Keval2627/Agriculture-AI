const fertilizerForm = document.getElementById("fertilizerForm");
const crop = document.getElementById("crop");
const soilType = document.getElementById("soilType");
const stage = document.getElementById("stage");
const adviceButton = document.getElementById("adviceButton");
const formMessage = document.getElementById("formMessage");

const emptyState = document.getElementById("emptyState");
const resultContent = document.getElementById("resultContent");
const adviceTitle = document.getElementById("adviceTitle");
const priorityBadge = document.getElementById("priorityBadge");
const descriptionText = document.getElementById("descriptionText");
const tipsList = document.getElementById("tipsList");

fertilizerForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  formMessage.textContent = "";

  if (!crop.value || !soilType.value || !stage.value) {
    formMessage.textContent = "Please select crop, soil type, and crop stage.";
    return;
  }

  adviceButton.disabled = true;
  adviceButton.textContent = "Getting field advice...";

  try {
    const response = await fetch("/api/fertilizer/advice", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        crop: crop.value,
        soilType: soilType.value,
        stage: stage.value
      })
    });

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(result.message || "Could not generate advice.");
    }

    const data = result.data;

    adviceTitle.textContent = data.title;
    descriptionText.textContent = data.description;

    priorityBadge.textContent = `${data.priority} Priority`;
    priorityBadge.className = `priority-badge priority-${data.priority.toLowerCase()}`;

    tipsList.innerHTML = "";

    data.tips.forEach((tip) => {
      const item = document.createElement("li");
      item.textContent = tip;
      tipsList.appendChild(item);
    });

    emptyState.classList.add("hidden");
    resultContent.classList.remove("hidden");
  } catch (error) {
    formMessage.textContent = error.message;
  } finally {
    adviceButton.disabled = false;
    adviceButton.textContent = "Get field advice";
  }
});