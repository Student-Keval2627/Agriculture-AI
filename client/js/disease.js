const diseaseForm = document.getElementById("diseaseForm");
const crop = document.getElementById("crop");
const symptom = document.getElementById("symptom");
const checkButton = document.getElementById("checkButton");
const formMessage = document.getElementById("formMessage");

const emptyState = document.getElementById("emptyState");
const resultContent = document.getElementById("resultContent");
const diseaseName = document.getElementById("diseaseName");
const riskBadge = document.getElementById("riskBadge");
const descriptionText = document.getElementById("descriptionText");
const adviceList = document.getElementById("adviceList");

diseaseForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  formMessage.textContent = "";

  if (!crop.value || !symptom.value) {
    formMessage.textContent = "Please select both crop and symptom.";
    return;
  }

  checkButton.disabled = true;
  checkButton.textContent = "Checking crop condition...";

  try {
    const response = await fetch("/api/disease/check", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        crop: crop.value,
        symptom: symptom.value
      })
    });

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(result.message || "Could not check the crop condition.");
    }

    const data = result.data;

    diseaseName.textContent = data.disease;
    descriptionText.textContent = data.description;

    riskBadge.textContent = `${data.risk} Risk`;
    riskBadge.className = `risk-badge risk-${data.risk.toLowerCase()}`;

    adviceList.innerHTML = "";

    data.advice.forEach((item) => {
      const listItem = document.createElement("li");
      listItem.textContent = item;
      adviceList.appendChild(listItem);
    });

    emptyState.classList.add("hidden");
    resultContent.classList.remove("hidden");
  } catch (error) {
    formMessage.textContent = error.message;
  } finally {
    checkButton.disabled = false;
    checkButton.textContent = "Check crop condition";
  }
});