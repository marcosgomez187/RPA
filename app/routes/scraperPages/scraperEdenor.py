from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import logging

from app.routes.scraperPages.excelReader import ExcelReader

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def inicializarScrap():
    try:
        logging.info("Iniciando la lectura del Excel...")
        datos = obtenerDatosExcel()
        
        if datos is not None:  # Verifico que los datos no sean nulos
            logging.info("Iniciando el proceso de scraping...")
            ejecutarScraping(datos)

        logging.info("Proceso finalizado con éxito.")
    except Exception as e:
        logging.error(f"Error en el proceso de scraping: {e}")

def obtenerDatosExcel():
    excel_reader = ExcelReader()
    try:
        # Armo un diccionario con los nombres y los tipos de las columnas que necesito
        columnas_y_tipos = {
            "Razón social": str,
            "N° Cuenta": str
        }

        # Nombre de la hoja
        sheet_name = "MEDIDORES"

        datos = excel_reader.read_excel_to_json("Edenor.xlsx", columns=columnas_y_tipos, sheet_name=sheet_name)
        logging.info(datos)
        return datos 
    except Exception as e:
        logging.error(f"Error al leer el Excel: {e}")
        raise

def ejecutarScraping(datos):
    logging.info("Iniciando el scraper de Edenor...")
    url_Edenor = "https://www.edenordigital.com/ingreso"

    options = uc.ChromeOptions()
    options.headless = False  # Ver navegador en tiempo real
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')  # Maximizar ventana
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-save-password-bubble") # Deshabilita la ventana guardar contraseña de google


    driver = uc.Chrome(options=options)

    try:
        logging.info("Accediendo a la URL de Edenor...")
        driver.get(url_Edenor)

        # Esperar explícitamente hasta que el campo de email esté presente
        wait = WebDriverWait(driver, 100)  # Espera máxima de 20 segundos
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))

        # Credenciales EDENOR
        email = 'proveedores@nordelta.com'
        password = 'Edenor2018'
        email_input.send_keys(email)
        password_input.send_keys(password)
        logging.info("Credenciales ingresadas.")

        # Click en el botón "Ingresar"
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='unifiedAuth.submit']")))
        submit_button.click()
        logging.info("Botón 'Ingresar' presionado. Esperando redirección...")

        # Verificar la URL después de iniciar sesión
        wait.until(EC.url_to_be('https://www.edenordigital.com/cuentas'))
        logging.info("Ingreso exitoso a la página del usuario.")

        # Esperar explícitamente hasta que el modal esté visible
        wait = WebDriverWait(driver, 20)  # Espera máxima de 20 segundos
        modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.MuiDialog-root.MuiDialog-root")))
        logging.info("Modal cargado y visible.")

        # Hacer clic en el checkbox "No volver a mostrar"
        checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.styles_container__nU4V6")))
        checkbox.click()
        logging.info("Checkbox 'No volver a mostrar' seleccionado.")

        # Hacer clic en el botón "Entendido"
        button_entendido = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Entendido')]]")))
        button_entendido.click()
        logging.info("Botón 'Entendido' presionado.")


        for cuenta in datos:
            numero_cuenta = cuenta.get("N° Cuenta")
            logging.info(f"Procesando cuenta: {numero_cuenta}")

        # # Capturar HTML
        # contenido_html = driver.page_source
        # logging.info("Contenido de la página del usuario obtenido.")
        # print(contenido_html)

    except Exception as e:
        driver.save_screenshot("screenshot.png") # Capturo la pantalla antes que se cierre para identificar donde estuvo el error
        logging.error(f"Error al obtener HTML: {e}")
    finally:
        driver.quit()
        logging.info("Driver cerrado.")


