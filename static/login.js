document.querySelector("form").addEventListener("submit", async function (e) {
  e.preventDefault();
  const errorDiv = document.getElementById("error-message");
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Error en el inicio de sesión");
    }

    // Redirección basada en el tipo de usuario
    switch (data.tipo) {
      case 1:
        window.location.href = "/enlaces"; // O la ruta que prefieras para administradores
        break;
      case 2:
        window.location.href = "/enlacesClient";
        break;
      default:
        throw new Error("Tipo de usuario no válido");
    }
  } catch (error) {
    errorDiv.textContent = error.message;
    errorDiv.style.display = "block";
    console.error("Error:", error);
  }
});
