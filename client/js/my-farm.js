(() => {
  const form = document.getElementById("farmProfileForm");
  const saveButton = document.getElementById("saveFarmButton");
  const formMessage = document.getElementById("formMessage");

  const farmName = document.getElementById("farmName");
  const location = document.getElementById("location");
  const farmArea = document.getElementById("farmArea");
  const soilType = document.getElementById("soilType");
  const mainCrop = document.getElementById("mainCrop");

  const previewCard = document.getElementById("farmPreviewCard");
  const emptyState = document.getElementById("farmEmptyState");
  const profileContent = document.getElementById("farmProfileContent");

  const profileFarmName = document.getElementById("profileFarmName");
  const profileLocation = document.getElementById("profileLocation");
  const profileFarmArea = document.getElementById("profileFarmArea");
  const profileSoilType = document.getElementById("profileSoilType");
  const profileMainCrop = document.getElementById("profileMainCrop");

  const originalButtonText = saveButton.textContent;

  function showMessage(message = "", isSuccess = false) {
    formMessage.textContent = message;
    formMessage.classList.toggle("success", isSuccess);
  }

  function fillForm(profile) {
    farmName.value = profile.farmName || "";
    location.value = profile.location || "";
    farmArea.value = profile.farmArea || "";
    soilType.value = profile.soilType || "";
    mainCrop.value = profile.mainCrop || "";
  }

  function showProfile(profile) {
    profileFarmName.textContent = profile.farmName;
    profileLocation.textContent = `📍 ${profile.location}`;
    profileFarmArea.textContent = `${profile.farmArea} acres`;
    profileSoilType.textContent = profile.soilType;
    profileMainCrop.textContent = profile.mainCrop;

    emptyState.classList.add("hidden");
    profileContent.classList.remove("hidden");
    previewCard.classList.add("has-profile");
  }

  async function loadProfile() {
    try {
      const response = await fetch("/api/farm/profile", {
        credentials: "same-origin"
      });

      if (response.status === 401) {
        window.location.href = "/login.html";
        return;
      }

      const payload = await response.json();

      if (!response.ok || payload.success === false) {
        throw new Error(payload.message || "Could not load your farm profile.");
      }

      const profile = payload.data || {};
      fillForm(profile);

      if (profile.farmName) {
        showProfile(profile);
      }
    } catch (error) {
      showMessage(error.message || "Could not load your farm profile.");
    }
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    showMessage("");

    const profileData = {
      farmName: farmName.value.trim(),
      location: location.value.trim(),
      farmArea: farmArea.value.trim(),
      soilType: soilType.value,
      mainCrop: mainCrop.value
    };

    saveButton.disabled = true;
    saveButton.textContent = "Saving...";

    try {
      const response = await fetch("/api/farm/profile", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "same-origin",
        body: JSON.stringify(profileData)
      });

      const payload = await response.json();

      if (!response.ok || payload.success === false) {
        throw new Error(payload.message || "Could not save farm profile.");
      }

      fillForm(payload.data);
      showProfile(payload.data);
      showMessage("Farm profile saved successfully.", true);
    } catch (error) {
      showMessage(error.message || "Could not save farm profile.");
    } finally {
      saveButton.disabled = false;
      saveButton.textContent = originalButtonText;
    }
  });

  loadProfile();
})();