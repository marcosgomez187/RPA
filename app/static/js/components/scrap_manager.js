class ScrapManager {
    constructor(servicio) {
        this.servicio = servicio;
        this.btnIniciar = document.getElementById('btnIniciarScrap');
        this.progressBar = document.querySelector('.progress');
        this.progressBarInner = document.querySelector('.progress-bar');
        this.accionesList = document.getElementById('accionesLista');
        
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
            
            // Simular proceso (aquí irían tus llamadas reales al backend)
            await this.simularProgreso();
            
            // Proceso completado
            this.progressBarInner.style.width = '100%';
            this.progressBarInner.textContent = 'Completado';
            
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
}