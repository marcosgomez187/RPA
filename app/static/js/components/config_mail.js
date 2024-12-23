class ConfigMail {
    constructor() {
        this.emailInput = document.getElementById('emailInput');
        this.sendEmailBtn = document.getElementById('sendEmailBtn');
        this.configMailForm = document.getElementById('configMailForm');

        // Inicializar el evento de envío
        this.init();
    }

    init() {
        this.configMailForm.addEventListener('submit', (event) => {
            event.preventDefault(); // Evitar el comportamiento por defecto de enviar el formulario
            this.enviarCorreo();
        });
    }

    enviarCorreo() {
        const email = this.emailInput.value;

        // Validar que el email no esté vacío y sea un formato válido
        if (this.validarEmail(email)) {
            console.log('Enviando correo a:', email);
            // Aquí puedes implementar la lógica para enviar el correo, por ejemplo, una llamada fetch o Ajax al servidor
            alert(`Correo enviado a ${email}`);
        } else {
            // Si la validación falla, mostrar mensaje de error
            this.emailInput.classList.add('is-invalid');
        }
    }

    // Método de validación de email
    validarEmail(email) {
        const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return regex.test(email);
    }
}

// Inicializar la clase ConfigMail
document.addEventListener('DOMContentLoaded', () => {
    new ConfigMail();
});
