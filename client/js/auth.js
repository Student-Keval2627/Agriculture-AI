const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

async function sendAuthRequest(url, data) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  const result = await response.json();

  if (!response.ok || !result.success) {
    throw new Error(result.message || "Something went wrong.");
  }

  return result;
}

if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const button = document.getElementById("loginButton");
    const message = document.getElementById("formMessage");

    message.textContent = "";
    button.disabled = true;
    button.textContent = "Logging in...";

    try {
      await sendAuthRequest("/api/auth/login", { email, password });
      window.location.replace("/");
    } catch (error) {
      message.textContent = error.message;
    } finally {
      button.disabled = false;
      button.textContent = "Login";
    }
  });
}

if (registerForm) {
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const button = document.getElementById("registerButton");
    const message = document.getElementById("formMessage");

    message.textContent = "";
    button.disabled = true;
    button.textContent = "Creating account...";

    try {
      await sendAuthRequest("/api/auth/register", { name, email, password });
      window.location.replace("/");
    } catch (error) {
      message.textContent = error.message;
    } finally {
      button.disabled = false;
      button.textContent = "Create account";
    }
  });
}