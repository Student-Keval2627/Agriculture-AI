const irrigationForm = document.getElementById("irrigationForm");
const crop = document.getElementById("crop");
const soilType = document.getElementById("soilType");
const moistureLevel = document.getElementById("moistureLevel");
const adviceButton = document.getElementById("adviceButton");
const formMessage = document.getElementById("formMessage");

const emptyState = document.getElementById("emptyState");
const resultContent = document.getElementById("resultContent");
const statusTitle = document.getElementById("statusTitle");
const priorityBadge = document.getElementById("priorityBadge");
const descriptionText = document.getElementById("descriptionText");
const tipsList = document.getElementById("tipsList");

irrigationForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  formMessage.textContent = "";

  if (!crop.value || !soilType.value || !moistureLevel.value) {
    formMessage.textContent = "Please select all field details.";
    return;
  }

  adviceButton.disabled = true;
  adviceButton.textContent = "Checking water needs...";

  try {
    const response = await fetch("/api/irrigation/advice", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        crop: crop.value,
        soilType: soilType.value,
        moistureLevel: moistureLevel.value
      })
    });

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(result.message || "Could not generate irrigation advice.");
    }

    const data = result.data;

    statusTitle.textContent = data.status;
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
    adviceButton.textContent = "Get irrigation advice";
  }
});