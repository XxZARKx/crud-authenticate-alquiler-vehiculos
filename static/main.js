import { fetchUsuarios } from "./getUsuarios.js";
import { deleteUsuario } from "./deleteUsuario.js";

const path = window.location.pathname;
console.log("🚀 ~ path:", path);
if (path.includes(`/employees`)) {
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

export const cargarTablaUsuarios = async () => {
  const usuarios = await fetchUsuarios();
  const tableBody = document.querySelector("#usersTable tbody");

  tableBody.innerHTML = "";

  usuarios.sort((a, b) => a.id - b.id);

  usuarios.forEach((usuario) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${usuario.id}</td>
      <td>${usuario.nombre}</td>
      <td>${usuario.correo}</td>
      <td>${usuario.dni}</td>
      <td>
	    <button onclick="editUser(${usuario.id})">Actualizar</button>
        <button onclick="eliminarUsuario(${usuario.id})">Eliminar</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
};

window.editUser = (id) => {
  window.location.href = `/users/update/?id=${id}`;
};

window.eliminarUsuario = async (id) => {
  const exito = await deleteUsuario(id); // Llamar directamente a la lógica de eliminación.
  if (exito) {
    cargarTablaUsuarios(); // Recargar la tabla después de una eliminación exitosa.
  }
};

// Carga la tabla de usuarios en la página
cargarTablaUsuarios();

export default cargarTablaUsuarios;
