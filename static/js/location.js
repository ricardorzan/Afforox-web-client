var headers = new Headers();
headers.append("X-CSCAPI-KEY", "SXZPbTdxNjVnQTBBM3FnSUdhR2lpYk5zVkFiRGtkbmdMOHZKbjkyOA==");

var requestOptions = {
    method: 'GET',
    headers: headers,
    redirect: 'follow'
};


initializeData()

async function initializeData() {
    await fetch("https://api.countrystatecity.in/v1/countries", requestOptions)
        .then(response => response.json())
        .then(async (data) => {
            const campoSelect = document.getElementById('id_domicilio-pais')
            for (var element in data) {
                const nuevaOpcion = document.createElement('option')
                nuevaOpcion.value = data[element].iso2
                nuevaOpcion.innerText = data[element].name
                campoSelect.appendChild(nuevaOpcion);
            }
            campoSelect.disabled = false
            campoSelect.addEventListener("change", filterStates())
        });
}

async function filterStates(e) {
    const paisSeleccionado = document.getElementById('id_domicilio-pais')
    await fetch("https://api.countrystatecity.in/v1/countries/" + paisSeleccionado.value + "/states", requestOptions)
        .then(response => response.json())
        .then(async (data) => {
            console.log(data)
            const campoSelect = document.getElementById('id_domicilio-estado')
            for (let i = campoSelect.options.length; i >= 0; i--) {
                campoSelect.remove(i);
            }

            const campoSegundoSelect = document.getElementById('id_domicilio-ciudad')
            for (let i = campoSegundoSelect.options.length; i >= 0; i--) {
                campoSegundoSelect.remove(i);
            }

            for (var element in data) {
                const nuevaOpcion = document.createElement('option')
                nuevaOpcion.value = data[element].iso2
                nuevaOpcion.innerText = data[element].name
                campoSelect.appendChild(nuevaOpcion);
            }
            campoSelect.disabled = false;
            campoSelect.addEventListener("change", filterCities())
        });
}

async function filterCities(e) {
    const paisSeleccionado = document.getElementById('id_domicilio-pais')
    const ciudadSeleccionada = document.getElementById('id_domicilio-estado')
    await fetch("https://api.countrystatecity.in/v1/countries/" + paisSeleccionado.value + "/states/" + ciudadSeleccionada.value + "/cities", requestOptions)
        .then(response => response.json())
        .then(async (data) => {
            console.log(data)
            const campoSelect = document.getElementById('id_domicilio-ciudad')
            for (let i = campoSelect.options.length; i >= 0; i--) {
                campoSelect.remove(i);
            }
            for (var element in data) {
                const nuevaOpcion = document.createElement('option')
                nuevaOpcion.value = data[element].id
                nuevaOpcion.innerText = data[element].name
                campoSelect.appendChild(nuevaOpcion);
            }
            campoSelect.disabled = false;
        });
}