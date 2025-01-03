from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def obtenerPages():
    print('metodo para obtener HTML de Natugry')

    url_Natugry="https://ov.naturgy.com.ar/ingreso"

   

    options = uc.ChromeOptions()
    options.headless = False  # Ver navegador en tiempo real
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')  # Maximizar ventana
    options.add_argument('--disable-blink-features=AutomationControlled')


    driver = uc.Chrome(options=options)

    
    print('driver inicializado')

    try:

        driver.get(url_Natugry)
     
            
        # Esperar explícitamente hasta que el campo de email esté presente
        wait = WebDriverWait(driver, 20)  # Espera máxima de 20 segundos
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))


        # Ingresar credenciales
        email = 'casarosa_999@hotmail.com'
        password = 'Cc12345678'
        email_input.send_keys(email)
        password_input.send_keys(password)
        logging.info("Credenciales ingresadas.")


        # Click en el botón "Ingresar"
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='unifiedAuth.submit']")))
        submit_button.click()
        logging.info("Botón 'Ingresar' presionado. Esperando redirección...")


        # Verificar la URL después de iniciar sesión
        wait.until(EC.url_to_be('https://www.edenordigital.com/usuario'))
        logging.info("Ingreso exitoso a la página del usuario.")


        # PAUSA para inspección manual
        input("Script en pausa. Inspecciona la página y presiona Enter para continuar...")


        # # Capturar HTML
        # contenido_html = driver.page_source
        # logging.info("Contenido de la página del usuario obtenido.")
        # print(contenido_html)


    except Exception as e:
        logging.error(f"Error al obtener HTML: {e}")
    finally:
        driver.quit()
        logging.info("Driver cerrado.")



      



