document.addEventListener('DOMContentLoaded', function () {
    const formulario = document.getElementById('formularioRegistro');
    const lista = document.getElementById('listaRegistros');
    const total = document.getElementById('totalRegistros');
    const spinner = document.getElementById('spinnerCarga');
    const mensaje = document.getElementById('mensaje');

    let contador = 0;

    if (formulario) {
        formulario.addEventListener('submit', function (e) {
            e.preventDefault();
            spinner.classList.remove('d-none');

            setTimeout(() => {
                spinner.classList.add('d-none');

                const nombre = document.getElementById('nombre').value;
                const descripcion = document.getElementById('descripcion').value;
                const categoria = document.getElementById('categoria').value;

                if (!nombre || !descripcion || !categoria) {
                    mensaje.innerHTML = '<div class="alert alert-danger">Completa todos los campos.</div>';
                    return;
                }

                contador++;
                total.textContent = contador;

                const tarjeta = document.createElement('div');
                tarjeta.className = 'col-md-6 col-lg-4';
                tarjeta.innerHTML = `
                    <div class="card h-100 shadow">
                        <div class="card-body">
                            <h5 class="card-title">${nombre}</h5>
                            <p class="card-text">${descripcion}</p>
                            <span class="badge bg-primary">${categoria}</span>
                        </div>
                    </div>
                `;
                lista.appendChild(tarjeta);

                mensaje.innerHTML = '<div class="alert alert-success">✅ Actividad agregada.</div>';
                formulario.reset();

                setTimeout(() => mensaje.innerHTML = '', 3000);
            }, 1200);
        });
    }
});