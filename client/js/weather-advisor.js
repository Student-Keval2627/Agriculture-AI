(() => {
  const weatherForm = document.getElementById("weatherForm");
  const weather = document.getElementById("weather");
  const rainExpected = document.getElementById("rainExpected");
  const weatherButton = document.getElementById("weatherButton");
  const formMessage = document.getElementById("formMessage");

  const weatherResultCard = document.getElementById("weatherResultCard");
  const emptyState = document.getElementById("emptyState");
  const resultContent = document.getElementById("resultContent");
  const adviceTitle = document.getElementById("adviceTitle");
  const priorityBadge = document.getElementById("priorityBadge");
  const adviceList = document.getElementById("adviceList");

  const originalButtonText = weatherButton.textContent;

  function showMessage(message = "") {
    formMessage.textContent = message;
  }

  function showResult(data) {
    adviceTitle.textContent = data.title || "Weather guidance";

    priorityBadge.textContent = `${data.priority || "Low"} Priority`;
    priorityBadge.className = "priority-badge";

    const priority = String(data.priority || "Low").toLowerCase();
    priorityBadge.classList.add(`priority-${priority}`);

    adviceList.replaceChildren();

    (data.advice || []).forEach((advice) => {
      const item = document.createElement("li");
      item.textContent = advice;
      adviceList.appendChild(item);
    });

    emptyState.classList.add("hidden");
    resultContent.classList.remove("hidden");
    weatherResultCard.classList.add("has-result");
  }

  weatherForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    showMessage("");

    weatherButton.disabled = true;
    weatherButton.textContent = "Checking conditions...";

    try {
      const response = await fetch("/api/weather/advice", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "same-origin",
        body: JSON.stringify({
          weather: weather.value,
          rainExpected: rainExpected.value
        })
      });

      const payload = await response.json();

      if (!response.ok || payload.success === false) {
        throw new Error(payload.message || "Could not get weather guidance.");
      }

      showResult(payload.data);
    } catch (error) {
      showMessage(error.message || "Could not get weather guidance.");
    } finally {
      weatherButton.disabled = false;
      weatherButton.textContent = originalButtonText;
    }
  });
})();