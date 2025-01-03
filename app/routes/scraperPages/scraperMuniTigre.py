from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from time import sleep




def scrapMuniTigre():
    print('metodo para scraper de MuniDeTigre')

    url_Municipalidad="https://ingresospublicos.tigre.gob.ar"    

    options = uc.ChromeOptions()
    options.headless = False  # Ver navegador en tiempo real
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')  # Maximizar ventana
    options.add_argument('--disable-blink-features=AutomationControlled')


    driver = uc.Chrome(options=options)

    
    print('driver inicializado')

    try:
        driver.get(url_Municipalidad)
      
         
        wait = WebDriverWait(driver, 20)  # Espera máxima de 20 segundos

        estado_deuda_link = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[mdata='estado-de-deuda']"))
        )
        print("Se encontró el enlace de 'Estado de Deuda'.")

     

        # Hacer clic usando JavaScript
        driver.execute_script("arguments[0].click();", estado_deuda_link)

        # Cambiar al iframe que contiene la página "Estado de Deuda"
        iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)
        print("Cambiado al contexto del iframe.")

        # Ahora intenta capturar elementos dentro del iframe
        estado_deuda_form = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "Consulta"))
        )
        print("El formulario 'Consulta' está disponible en el iframe.")

    
        user_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
        print('se capturo el input de user')
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        print('se capturo el input del password')

        
        # Ingresar credenciales
        user='32218900'
        password='4184'
        user_input.send_keys(user)
        password_input.send_keys(password)

        print('redenciales ingresadas correctamente')
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "btnConsultar")))
        submit_button.click()
        print("Botón 'Ingresar' presionado. Esperando redirección...")


       

        sleep(10)
    
        # Click en el botón "Ingresar"
        submit_button = driver.find_element((By.CSS_SELECTOR, "button[type='submit']"))
        submit_button.click()
               
        sleep(30)


    except Exception as e:
        print(f"Error al obtener HTML: {e}")
    finally:
        driver.quit()
        print("Driver cerrado.")

