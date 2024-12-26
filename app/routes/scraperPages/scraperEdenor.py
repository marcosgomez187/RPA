
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc  # Usa esta librería para evitar detección
from bs4 import BeautifulSoup
from time import sleep 

import os

def obtenerHtml():
    
    print('este es metodo obtener HTML')
    url_Edenor= "https://www.edenordigital.com/ingreso"
    
    #se configura el servicio y las opciones de navegaciones
    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument(r"--user-data-dir=C:\Users\usuario\AppData\Local\Google\Chrome\User Data\Default")
    options.add_argument("--profile-directory=Default") 
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')


    # options = webdriver.ChromeOptions()
    # # options.add_argument('--headless')  # Modo sin cabeza
    # options.add_argument('--no-sandbox')  # Opciones adicionales para optimizar la ejecución en distintos entornos
   
    # driver=webdriver.Chrome(options=options)
    driver = uc.Chrome(options=options)

    try:
        driver.get(url_Edenor)   # Navega hasta la página de Edenor
        sleep(10)    # Pausa para permitir la carga de recursos
        
        contenido = driver.page_source  # Obtiene el código HTML
        html = BeautifulSoup(contenido, "html.parser")

        # formulario= html.find('form', {'class':'styles_form__11_YA'})
     
        # print(formulario)  # Imprime el contenido HTML


        #obtengo los elementos del formulario
        email_input= driver.find_element(By.CSS_SELECTOR, "input[type='text']")
    
        password_input=driver.find_element(By.CSS_SELECTOR, "input[type='password']" )

        #cargo las credenciales
        email_input.send_keys('casarosa_999@hotmail.com')
        password_input.send_keys('Cc12345678')

        print("Email ingresado:", email_input.get_attribute("value"))
        print("Password ingresado:", password_input.get_attribute("value"))

        submit_button = driver.find_element(By.CSS_SELECTOR, "button.MuiButtonBase-root.MuiButton-root")
        submit_button.click()

        sleep(30)
    
        #verifico que se haya navegación hacia la pagina del usuario

        usuario_url= driver.current_url
        print(usuario_url)
        if(usuario_url == 'https://www.edenordigital.com/usuario'):
            print('Ingreso a la pagina del usuario')

            contenido_html= driver.page_source

            htmlUser= BeautifulSoup(contenido_html, 'html.parser')

            print(htmlUser)
   
    except Exception as e:
        print(f'error al obtener html: {e}')
    finally:
        driver.close()
    
    



   

 

