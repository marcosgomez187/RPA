class MainPage {
    constructor() {
        this.modal = new bootstrap.Modal(document.getElementById('servicioModal'));
        this.modalTitle = document.getElementById('servicioModalLabel');
        this.modalContent = document.getElementById('modalContent');
    }

    async loadModalContent(modalType, servicio) {
        try {
            const response = await fetch(`/load-modal-content?modalType=${modalType}&servicio=${servicio}`);
            const html = await response.text();
            
            // Actualizar título del modal según el tipo
            this.modalTitle.textContent = modalType === 'scrap' 
                ? `Scraping - ${servicio}`
                : `Configuración - ${servicio}`;
            
            // Cargar contenido
            this.modalContent.innerHTML = html;
            
            // Inicializar componentes específicos según el tipo
            switch(modalType) {
                case 'scrap':
                    this.modalTitle.textContent = `Scraping - ${servicio}`;
                    new ScrapManager(servicio);
                    break;
                case 'config':
                    this.modalTitle.textContent = `Configuración - ${servicio}`;
                    new ConfigManager(servicio);
                    break;
                case 'configMail':
                    this.modalTitle.textContent = `Envío de Mail`;
                    new ConfigMail(servicio);
                    break;
                default:
                    console.log('Tipo de modal no reconocido');
                    break;
            }
                        
            // Mostrar modal
            this.modal.show();
        } catch (error) {
            console.error('Error loading modal content:', error);
            alert('Error al cargar el contenido del modal');
        }
    }
}

// Inicializar y hacer global para el onclick
const mainPage = new MainPage();
window.loadModalContent = (modalType, servicio) => mainPage.loadModalContent(modalType, servicio);