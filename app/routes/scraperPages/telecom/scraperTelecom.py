from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import logging
from time import sleep
import os
from app.routes.scraperPages.telecom.scraperConsultation import consultation
# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrapTelecom():
    print('metodo para scraper de Telecom')

    # Ruta al escritorio
    #desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Nombre de la carpeta para guardar facturas
    # facturas = os.path.join(desktop_path, "Facturas Lineas Moviles")
    facturas= os.path.abspath("app/data/facturas/telecom-lineasMoviles")

    # Crear la carpeta si no existe
    # if not os.path.exists(facturas):
    #     os.makedirs(facturas)
    #     print(f"Carpeta creada en: {facturas}")
    # else:
    #     print(f"La carpeta ya existe: {facturas}")

    
    empresa= 'consultation'
    servicio= 'telefonia moviles'

    url_Telecom="https://gestiononline.telecom.com.ar"    

    options = uc.ChromeOptions()
    #configuracion para la descarga de facturas
    prefs = {
    "download.default_directory": facturas,         # Ruta de descarga
    "download.prompt_for_download": False,          # No preguntar al descargar
    "download.directory_upgrade": True,             # Actualizar directorio si cambia
    "safebrowsing.enabled": True                    # Evitar bloqueos por seguridad
    }
    options.add_experimental_option("prefs", prefs)


    options.headless = False  # Ver navegador en tiempo real
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')  # Maximizar ventana
    options.add_argument('--disable-blink-features=AutomationControlled')


    driver = uc.Chrome(options=options)

    
    print('driver inicializado')

    try:
        driver.get(url_Telecom)

         # Esperar explícitamente hasta que el campo de email esté presente
        wait = WebDriverWait(driver, 20)  # Espera máxima de 20 segundos

        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))

        
        # Ingresar credenciales
        email = 'proveedores@consultatio.com.ar'
        password = 'Ctio2023*'
        email_input.send_keys(email)
        password_input.send_keys(password)
        logging.info("Credenciales ingresadas.")
    
        # Click en el botón "Ingresar"
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-reflect-preset='loginFormButton']")))
        submit_button.click()
        logging.info("Botón 'Ingresar' presionado. Esperando redirección...")


      
        # Verificar la URL después de iniciar sesión
        wait.until(EC.url_to_be('https://gestiononline.telecom.com.ar/gestionapps/b2bgol-app-002/20241212/#/'))
        logging.info("Ingreso exitoso a la página del usuario.")

        sleep(10)
 
        if (empresa == 'consultation'):
            consultation(driver, facturas, wait, logging)
        
             

      


    except Exception as e:
        logging.error(f"Error al obtener HTML: {e}")
    finally:
        driver.quit()
        logging.info("Driver cerrado.")
