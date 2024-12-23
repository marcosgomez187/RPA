class ScrapManager {
    constructor(servicio) {
        console.log("constructor scrap");
        this.servicio = servicio;
        this.btnIniciar = document.getElementById('btnIniciarScrap');
        this.progressBar = document.querySelector('.progress');
        this.progressBarInner = document.querySelector('.progress-bar');
        this.accionesList = document.getElementById('accionesLista');
        this.facturasTableBody = document.querySelector('#facturasTable tbody');
        
        this.init();
    }

    init() {
        this.btnIniciar.addEventListener('click', () => this.iniciarProceso());
    }

    async iniciarProceso() {
        try {
            // Deshabilitar botón
            this.btnIniciar.disabled = true;
            
            // Mostrar barra de progreso
            this.progressBar.classList.remove('d-none');
            this.accionesList.classList.remove('d-none');
            
            // Simular progreso o realizar la llamada real al backend
            await this.simularProgreso();
            
            // Obtener facturas del backend
            await this.obtenerFacturas();

            // Habilitar botón después de completar
            this.btnIniciar.disabled = false;
            
        } catch (error) {
            console.error('Error en el proceso:', error);
            alert('Ocurrió un error durante el proceso');
            this.btnIniciar.disabled = false;
        }
    }

    async simularProgreso() {
        const pasos = [25, 50, 75, 100];
        for (let progreso of pasos) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            this.progressBarInner.style.width = `${progreso}%`;
            this.progressBarInner.textContent = `${progreso}%`;
        }
    }

    async obtenerFacturas() {
        try {
            // Mock de facturas para cada servicio
            const facturasMock = {
                'Arca': [
                    { descripcion: 'Factura 1 Arca', fecha_ejecucion: '2024-12-01', estado_ejecucion: 'Completado', factura_id: '123', monto: '$2000' },
                    { descripcion: 'Factura 2 Arca', fecha_ejecucion: '2024-12-02', estado_ejecucion: 'Pendiente', factura_id: '124', monto: '$3000' }
                ],
                'servicioB': [
                    { descripcion: 'Factura 1 ServicioB', fecha_ejecucion: '2024-12-03', estado_ejecucion: 'Completado', factura_id: '223', monto: '$1500' },
                    { descripcion: 'Factura 2 ServicioB', fecha_ejecucion: '2024-12-04', estado_ejecucion: 'Pendiente', factura_id: '224', monto: '$1200' }
                ]
            };

            // Filtrar las facturas según el servicio
            const facturas = facturasMock[this.servicio] || [];

            // Mostrar las facturas obtenidas
            this.mostrarFacturas(facturas);
        } catch (error) {
            console.error('Error al obtener las facturas:', error);
            alert('No se pudieron obtener las facturas');
        }
    }

    mostrarFacturas(facturas) {
        this.facturasTableBody.innerHTML = ''; // Limpiar la tabla antes de agregar nuevas filas
    
        if (facturas.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = `<td colspan="6" class="text-center">No hay facturas disponibles</td>`;
            this.facturasTableBody.appendChild(row);
            
            // Ocultar el botón de enviar si no hay facturas
            document.getElementById('enviarBtnContainer').style.display = 'none';
            return;
        }
    
        facturas.forEach(factura => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${factura.descripcion}</td>
                <td>${factura.fecha_ejecucion}</td>
                <td>${factura.estado_ejecucion}</td>
                <td>${factura.factura_id}</td>
                <td>${factura.monto}</td>
                <td><button class="btn btn-info">Ver</button></td>
            `;
            this.facturasTableBody.appendChild(row);
        });
    
        // Mostrar el botón de enviar solo si hay facturas
        document.getElementById('enviarBtnContainer').style.display = 'block';
    }
    
}
