from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import logging
import time
import os

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
    options.add_argument('--disable-popup-blocking')  # Deshabilita la apertura de nuevas pestañas

    prefs = {
        "download.default_directory": os.path.abspath("app/data/facturas/edenor"),
        "download.prompt_for_download": False,  # No pedir confirmación de descarga
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True  # Habilitar la descarga de archivos
    }
    options.add_experimental_option("prefs", prefs)


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
        modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.MuiDialog-root")))
        logging.info("Modal cargado y visible.")

        # Hacer clic en el botón "Entendido"
        try:
            button_entendido = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//div[contains(@class, 'styles_textContainer__1uzht') and contains(text(), 'Entendido')]]")))
            button_entendido.click()
            logging.info("Botón 'Entendido' presionado.")
        except Exception as e:
            logging.error(f"Error al presionar el botón 'Entendido': {e}")


        try:
            logging.info("Intentando cerrar el tutorial de bienvenida...")

            # Localizar el botón '×' para cerrar el tutorial
            close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='cuentas.resumen.onboarding.close']")))
            
            # Hacer clic en el botón
            close_button.click()
            logging.info("Botón '×' del tutorial presionado con éxito.")
        except Exception as e:
            logging.error(f"Error al intentar cerrar el tutorial: {e}")

        # Iteracion con las cuentas
        # Variable para controlar si es la primera cuenta
        primera_cuenta = True

        for cuenta in datos:
            numero_cuenta = cuenta.get("N° Cuenta")
            logging.info(f"Procesando cuenta: {numero_cuenta}")

            # Si es la primera cuenta, usar el flujo actual para acceder
            if primera_cuenta:
                try:
                    # Localizar el campo de búsqueda y buscar la cuenta
                    input_busqueda = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='accountFilters.searchValue']")))
                    input_busqueda.clear()
                    input_busqueda.send_keys(numero_cuenta)
                    logging.info(f"Cuenta '{numero_cuenta}' ingresada en el campo de búsqueda.")

                    # Espera de 2 segundos (ajustable según el rendimiento de la web)
                    time.sleep(2)

                    # Localizar y hacer clic en la tarjeta correspondiente a la cuenta
                    card = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='button']//div[contains(text(), '{numero_cuenta}')]")))
                    card.click()
                    logging.info(f"Se hizo clic en la tarjeta de la cuenta: {numero_cuenta}")

                    # Esperar a que la página de resumen se cargue
                    wait.until(EC.url_to_be("https://www.edenordigital.com/cuentas/resumen"))
                    logging.info(f"Redirigido a la página de resumen para la cuenta: {numero_cuenta}")

                    # Hacer clic en el botón "Descargar factura"
                    boton_descargar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='cuentas.resumen.billsList.billsListDownloadBill']")))
                    boton_descargar.click()
                    logging.info(f"Factura descargada para la cuenta: {numero_cuenta}")

                    # Cambiar la variable para las siguientes cuentas
                    primera_cuenta = False

                except Exception as e:
                    logging.error(f"No se pudo procesar la cuenta {numero_cuenta}: {e}")

            else:
                try:

                  # Hacer clic en el botón para desplegar el selector de cuentas
                    boton_selector_cuentas = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='cuentas.resumen.accountSelector.open']")))
                    boton_selector_cuentas.click()
                    logging.info("Selector de cuentas desplegado.")

                    # Esperar que el input de búsqueda en el selector sea visible
                    input_selector = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='cuentas.resumen.accountSelector.accountFilter']")))
                    
                    # Limpiar el campo de búsqueda usando Backspace
                    input_selector.send_keys(Keys.CONTROL + "a")  # Selecciona todo el texto
                    input_selector.send_keys(Keys.BACKSPACE)     # Borra el texto seleccionado

                    # Ingresar el número de cuenta
                    input_selector.send_keys(numero_cuenta)
                    logging.info(f"Cuenta '{numero_cuenta}' ingresada en el selector.")

                    # Esperar que la lista de cuentas se actualice y que el elemento esté disponible
                    cuenta_en_lista = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[@data-testid='cuentas.resumen.accountSelector.address.0']/div[contains(text(), '{numero_cuenta}')]")))
                    cuenta_en_lista.click()

                    # Hacer clic en el elemento
                    cuenta_en_lista.click()
                    logging.info(f"Cuenta '{numero_cuenta}' seleccionada del selector.")

                    # Esperar que la página se actualice
                    time.sleep(2)  # Espera para permitir que la página se actualice

                    # Hacer clic en el botón "Descargar factura"
                    boton_descargar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='cuentas.resumen.billsList.billsListDownloadBill']")))
                    boton_descargar.click()
                    logging.info(f"Factura descargada para la cuenta: {numero_cuenta}")

                except Exception as e:
                    logging.error(f"No se pudo procesar la cuenta {numero_cuenta}: {e}")

            # Pausa de 5 segundos para observar la acción
            time.sleep(5)  # Ajusta el tiempo si es necesario


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


