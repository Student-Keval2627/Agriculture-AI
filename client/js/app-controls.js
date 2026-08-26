// ==========================================
// AGRICULTURE AI - GLOBAL APP CONTROLS
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

  setupGlobalLogout();

});


function setupGlobalLogout() {

  let logoutButton =
    document.getElementById("logoutButton");


  // ========================================
  // CREATE LOGOUT BUTTON IF PAGE DOESN'T HAVE
  // ========================================

  if (!logoutButton) {

    logoutButton = document.createElement("button");

    logoutButton.id = "logoutButton";
    logoutButton.type = "button";
    logoutButton.innerHTML = "🚪 Logout";


    const sidebar =
      document.querySelector(".sidebar");


    // If page has sidebar
    if (sidebar) {

      logoutButton.className =
        "global-logout sidebar-logout";

      const nav =
        sidebar.querySelector(".nav-links");

      if (nav) {
        nav.insertAdjacentElement(
          "afterend",
          logoutButton
        );
      } else {
        sidebar.appendChild(logoutButton);
      }

    }

    // If page has no sidebar
    else {

      logoutButton.className =
        "global-logout floating-logout";

      document.body.appendChild(
        logoutButton
      );

    }

  }


  // ========================================
  // LOGOUT CLICK
  // ========================================

  logoutButton.addEventListener(
    "click",
    logoutUser
  );


  // ========================================
  // ADD LOGOUT STYLE
  // ========================================

  addLogoutStyles();

}



async function logoutUser() {

  const logoutButton =
    document.getElementById("logoutButton");


  try {

    if (logoutButton) {

      logoutButton.disabled = true;

      logoutButton.innerHTML =
        "Logging out...";

    }


    const response = await fetch(
      "/api/auth/logout",
      {
        method: "POST",
        credentials: "include"
      }
    );


    const data =
      await response.json();


    if (!response.ok || !data.success) {

      throw new Error(
        data.message || "Logout failed"
      );

    }


    // Redirect after session is cleared
    window.location.href =
      "/login.html";


  } catch (error) {

    console.error(
      "Logout error:",
      error
    );


    alert(
      "Could not logout. Please try again."
    );


    if (logoutButton) {

      logoutButton.disabled = false;

      logoutButton.innerHTML =
        "🚪 Logout";

    }

  }

}



function addLogoutStyles() {

  if (
    document.getElementById(
      "globalLogoutStyles"
    )
  ) {
    return;
  }


  const style =
    document.createElement("style");


  style.id =
    "globalLogoutStyles";


  style.textContent = `

    .global-logout {
      font-family: Arial, sans-serif;
      cursor: pointer;
      transition: 0.2s ease;
    }


    /* SIDEBAR LOGOUT */

    .sidebar-logout {
      width: 100%;

      margin-top: 15px;
      padding: 13px 12px;

      border: none;
      border-radius: 10px;

      background: transparent;

      color: #d2e7d8;

      font-size: 14px;
      text-align: left;
    }


    .sidebar-logout:hover {
      background: #8f3434;
      color: #ffffff;
    }


    /* PAGE WITHOUT SIDEBAR */

    .floating-logout {
      position: fixed;

      top: 22px;
      right: 24px;

      z-index: 9999;

      padding: 10px 15px;

      border: 1px solid #d8e6da;
      border-radius: 10px;

      background: #ffffff;

      color: #9b3939;

      box-shadow:
        0 6px 20px rgba(
          20,
          61,
          34,
          0.08
        );

      font-size: 13px;
      font-weight: 700;
    }


    .floating-logout:hover {
      background: #9b3939;
      color: #ffffff;
      border-color: #9b3939;
    }


    .global-logout:disabled {
      opacity: 0.6;
      cursor: wait;
    }


    @media (max-width: 680px) {

      .floating-logout {
        top: 12px;
        right: 12px;

        padding: 8px 11px;

        font-size: 11px;
      }

    }

  `;


  document.head.appendChild(
    style
  );

}