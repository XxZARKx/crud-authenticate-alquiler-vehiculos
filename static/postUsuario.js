export function getApiUrl() {
  if (window.location.hostname === "localhost") {
    return "http://127.0.0.1:8000";
  } else {
    return `${window.location.origin}`;
  }
}

const path = window.location.pathname;
let tipo = 2; // Por defecto es tipo usuario
if (path.includes(`/employees`)) {
  tipo = 1; // Empleado
  document.getElementById("formTitle").innerText = "Registrar Empleado";
  let navList = document.querySelector("#headerRegister nav ul");
  const listEmpleados = document.createElement("li");
  const registerEmpleados = document.createElement("li");
  const crudDisponibles = document.createElement("li");
  listEmpleados.innerHTML = `<a href="/employees/list">Lista de Empleados</a>`;
  registerEmpleados.innerHTML = `<a href="/employees/register">Registrar Empleado</a>`;
  crudDisponibles.innerHTML = `<a href="/enlaces">Crud Diponibles</a>`;
  navList.appendChild(listEmpleados);
  navList.appendChild(registerEmpleados);
  navList.appendChild(crudDisponibles);
} else if (path.includes(`/clients`)) {
  tipo = 2; // Usuario
  document.getElementById("formTitle").innerText = "Registrar Cliente";
  let navList = document.querySelector("#headerRegister nav ul");
  const listClientes = document.createElement("li");
  const registerClientes = document.createElement("li");
  const crudDisponibles = document.createElement("li");
  listClientes.innerHTML = `<a href="/clients/list">Lista de Clientes</a>`;
  registerClientes.innerHTML = `<a href="/clients/register">Registrar Clientes</a>`;
  crudDisponibles.innerHTML = `<a href="/enlacesClient">Crud Diponibles</a>`;
  navList.appendChild(listClientes);
  navList.appendChild(registerClientes);
  navList.appendChild(crudDisponibles);
} else if (path.startsWith("/register")) {
  document.getElementById("formTitle").innerText = "Registrar Cliente";
  let navList = document.querySelector("#headerRegister nav ul");
  const loginPage = document.createElement("li");
  loginPage.innerHTML = `<a href="/login">Iniciar Sesion</a>`;
  navList.appendChild(loginPage);
}

document
  .getElementById("registerForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const userData = Object.fromEntries(formData.entries());

    userData.tipo = tipo;

    try {
      const response = await fetch(`${getApiUrl()}/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        const result = await response.json();
        Swal.fire(
          tipo === 1 ? "Empleado registrado" : "Usuario registrado",
          `ID: ${result.id}`,
          "success"
        );
        e.target.reset();
      } else {
        Swal.fire("Error", "No se pudo registrar", "error");
      }
    } catch (error) {
      Swal.fire("Error", error.message, "error");
    }
  });
