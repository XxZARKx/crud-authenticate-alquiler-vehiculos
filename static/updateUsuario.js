import { getApiUrl } from "./getApiUrl.js";
import { cargarTablaUsuarios } from "./main.js";

const previousUrl = document.referrer;

// Extraer el path de la URL anterior
const previousPath = previousUrl ? new URL(previousUrl).pathname : null;

console.log(previousPath);
let pathTypeUser = "";
if (previousPath.includes(`/employees`)) {
  pathTypeUser = "employees";
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
} else if (previousPath.includes(`/clients`)) {
  pathTypeUser = "clients";
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
}

function getUserIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

async function fetchUser(id) {
  const apiUrl = getApiUrl();

  // Muestra un popup de "Cargando..."
  Swal.fire({
    title: "Cargando...",
    text: "Obteniendo información del usuario",
    icon: "info",
    allowOutsideClick: false,
    allowEscapeKey: false,
  });

  try {
    const response = await fetch(`${apiUrl}/users/${id}`);

    if (!response.ok) {
      console.error("Error al obtener los datos:", response.status);
      Swal.close();
      return;
    }

    const user = await response.json();
    console.log("Datos recibidos del servidor:", user);

    if (user) {
      document.getElementById("userId").value = user.id || "";
      document.getElementById("nombre").value = user.nombre || "";
      document.getElementById("correo").value = user.correo || "";
      document.getElementById("contraseña").value = user.contraseña || "";

      Swal.fire({
        title: "Éxito",
        text: "Datos cargados correctamente",
        icon: "success",
      });
    } else {
      console.error("No se recibieron datos del servidor.");
      Swal.fire({
        title: "Error",
        text: "No se recibieron datos del servidor",
        icon: "error",
      });
    }
  } catch (error) {
    console.error("Error al realizar la solicitud", error);
    Swal.fire({
      title: "Error",
      text: "No se pudo obtener información",
      icon: "error",
    });
  } finally {
    Swal.close();
  }
}

async function updateUser(event) {
  event.preventDefault();
  const id = document.getElementById("userId").value;
  const userData = {
    nombre: document.getElementById("nombre").value,
    correo: document.getElementById("correo").value,
    contraseña: document.getElementById("contraseña").value || undefined,
  };

  const apiUrl = getApiUrl();

  // Realiza el envío con el popup de "Procesando..."
  Swal.fire({
    title: "Actualizando...",
    text: "Por favor, espere",
    icon: "info",
    allowOutsideClick: false,
    allowEscapeKey: false,
  });

  try {
    const response = await fetch(`${apiUrl}/users/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });

    if (response.ok) {
      Swal.fire({
        title: "Éxito",
        text: "Usuario actualizado correctamente",
        icon: "success",
      }).then(() => {
        cargarTablaUsuarios();
        window.location.href = `${apiUrl}/${pathTypeUser}/list`;
      });
    } else {
      Swal.fire({
        title: "Error",
        text: "No se pudo actualizar el usuario",
        icon: "error",
      });
    }
  } catch (error) {
    console.error("Error en la solicitud", error);
    Swal.fire({
      title: "Error",
      text: "Algo salió mal",
      icon: "error",
    });
  } finally {
    Swal.close();
  }
}

document
  .getElementById("updateUserForm")
  .addEventListener("submit", updateUser);

// Inicia la carga de datos
fetchUser(getUserIdFromURL());
