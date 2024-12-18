export function getApiUrl() {
  // Si el frontend y el backend están en el mismo dominio, usa el dominio actual
  if (window.location.hostname === "localhost") {
    // Para desarrollo local
    return "http://127.0.0.1:8000";
  } else {
    // Para producción, usa el dominio de la página actual
    return `${window.location.origin}`; // Asumimos que la API está en /api
  }
}

// Función para obtener todos los vehículos desde el servidor
async function fetchVehicles() {
  const apiUrl = getApiUrl(); // Obtener la URL de la API
  const response = await fetch(`${apiUrl}/vehicles/`);
  const vehicles = await response.json();
  const tableBody = document.querySelector("#vehiclesTable tbody");

  // Limpiar la tabla antes de agregar nuevos datos
  tableBody.innerHTML = "";

  vehicles.sort((a, b) => a.id - b.id);
  // Agregar los vehículos a la tabla
  vehicles.forEach((vehicle) => {
    const row = document.createElement("tr");

    row.innerHTML = `
		<td>${vehicle.id}</td>
		<td>${vehicle.marca}</td>
		<td>${vehicle.modelo}</td>
		<td>${vehicle.placa}</td>
		<td>${vehicle.matricula}</td>
		<td>${vehicle.estado}</td>
		<td class="buttonActionContainer">
		  <button onclick="editVehicle(${vehicle.id})">Actualizar</button>
		  <button onclick="deleteVehicle(${vehicle.id})">Eliminar</button>
		</td>
	  `;

    tableBody.appendChild(row);
  });
}

// Función para editar un vehículo
function editVehicle(id) {
  const apiUrl = getApiUrl(); // Obtener la URL de la API
  window.location.href = `${apiUrl}/vehicles/update/?id=${id}`;
  Swal.fire({
    title: "Redirigiendo...",
    text: "Serás llevado al formulario de actualización.",
    icon: "info",
    timer: 2000,
    showConfirmButton: false,
  }); // Redirigir al formulario de actualización
}

// Función para eliminar un vehículo
async function deleteVehicle(id) {
  const apiUrl = getApiUrl(); // Obtener la URL de la API
  const result = await Swal.fire({
    title: "¿Estás seguro?",
    text: "No podrás revertir esta acción.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Sí, eliminar",
    cancelButtonText: "Cancelar",
  });

  if (result.isConfirmed) {
    const response = await fetch(`${apiUrl}/vehicles/${id}`, {
      method: "DELETE",
    });

    if (response.ok) {
      Swal.fire("Eliminado", "El vehículo ha sido eliminado.", "success");
      fetchVehicles(); // Recargar los vehículos después de eliminar uno
    } else {
      Swal.fire("Error", "Hubo un problema al eliminar el vehículo.", "error");
    }
  }
}

// Hacer que las funciones sean globales
window.editVehicle = editVehicle;
window.deleteVehicle = deleteVehicle;

// Llamar a la función para obtener los vehículos al cargar la página
fetchVehicles();
