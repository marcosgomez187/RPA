class ConfigManager {
    constructor(servicio) {
        console.log("constructor config", servicio);
        this.servicio = servicio;
        this.dates = new Set([1]); // Inicialmente el día 1
        this.init();
    }

    init() {
        console.log('Iniciando ConfigManager');
        this.initializeSelects();
        this.setupEventListeners();
        this.loadCurrentConfig();
    }

    initializeSelects() {
        const daySelect = document.getElementById('daySelect');
        // Generar opciones para los 31 días del mes
        for (let i = 1; i <= 31; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            daySelect.appendChild(option);
        }
    }

    setupEventListeners() {
        // Botón para agregar fecha
        document.getElementById('btnAddDate').addEventListener('click', () => {
            const daySelect = document.getElementById('daySelect');
            const selectedDay = parseInt(daySelect.value);
            
            if (selectedDay) {
                this.addDate(selectedDay);
            }
        });

        // Delegación de eventos para botones de eliminar
        document.getElementById('dateTable').addEventListener('click', (e) => {
            if (e.target.matches('button.btn-danger') || e.target.closest('button.btn-danger')) {
                const btn = e.target.closest('button.btn-danger');
                const day = parseInt(btn.dataset.day);
                this.removeDate(day);
            }
        });
    }

    async loadCurrentConfig() {
        try {
            console.log('Cargando configuración actual...');
            this.updateDateTable();
        } catch (error) {
            console.error('Error loading config:', error);
            alert('Error al cargar la configuración');
        }
    }

    addDate(day) {
        if (this.dates.has(day)) {
            alert('Esta fecha ya está configurada');
            return;
        }

        this.dates.add(day);
        this.updateDateTable();
        this.saveConfig();
    }

    removeDate(day) {
        if (this.dates.size <= 1) {
            alert('Debe mantener al menos una fecha configurada');
            return;
        }

        this.dates.delete(day);
        this.updateDateTable();
        this.saveConfig();
    }

    updateDateTable() {
        const tbody = document.querySelector('#dateTable tbody');
        tbody.innerHTML = '';

        // Convertir Set a Array, ordenar y crear filas
        Array.from(this.dates)
            .sort((a, b) => a - b)
            .forEach(day => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${day}</td>
                    <td>
                        <button class="btn btn-danger btn-sm" data-day="${day}">
                            <i class="bi bi-trash"></i> Eliminar
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
    }

    async saveConfig() {
        try {
            // Simulación de llamada al servidor
            console.log('Guardando configuración para servicio:', this.servicio);
            console.log('Fechas configuradas:', Array.from(this.dates));

            await new Promise(resolve => setTimeout(resolve, 500));
            alert('Configuración guardada correctamente');
        } catch (error) {
            console.error('Error saving config:', error);
            alert('Error al guardar la configuración');
        }
    }
}
