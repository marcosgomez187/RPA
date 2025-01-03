from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep
import os


def consultation(driver, facturas, wait, logging):

    mesActual= datetime.now().strftime("%m")
    
     
    servicio='Otros Productos Empresas'

    if(servicio == 'Líneas Moviles'):
        
        ('ejecutnado el scraper de consultation')
        # Click en el botón para descargar "FACTURAS LINEAS MOVILES"
        lineas_moviles = driver.find_element(By.XPATH, "//div[@data-ui-element='card - Facturas de Líneas Móviles']")
        lineas_moviles.click()
        logging.info("Botón 'Facturas Moviles' presionado. Esperando redirección...")

        sleep(10)

        #captura el input y setea el numero de acuerdo
        input_acuerdo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']")))
        input_acuerdo.click()
        input_acuerdo.send_keys('6004003908')
        sleep(5)
        input_acuerdo.send_keys(Keys.ARROW_DOWN)
        input_acuerdo.send_keys(Keys.ENTER)
        input_acuerdo.click()

        print("acuerdo ingresado: ", input_acuerdo.get_attribute("value"))  #muestra por consola el numero de acuerdo insertado

        sleep(15)

        try:
            encuesta= wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog']")))
            print('cuadro de encuesta renderizado')

            botonCerrar= encuesta.find_element(By.CSS_SELECTOR, "button[aria-label='cerrar']")
            botonCerrar.click()

            print('presionado el boton para cerrar la encuesta')
        except Exception:
            print('no se renderizo ningun cuadro de dialog')


        #se obtiene la primera linea de la tabla        
        tbody = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
        
        rows = tbody.find_elements(By.TAG_NAME, "tr") #captura todas la filas

        print(f"Número de filas en el tbody: {len(rows)}") #muestra por consola todas las filas de la tabla
    
        first_row = rows[0] 

        #muestra por consola los elementos de la primera fila
        print("Contenido de la primera fila:", first_row.text)

        button_in_first_row = rows[0].find_element(By.CSS_SELECTOR, "button[data-ui-element='Descarga']")

        button_in_first_row.click()

        print("Botón de descarga en la primera fila clickeado con éxito.")
        # Hacer clic en el botón de descarga
        print("Factura descargada en la carpeta:", facturas)

        sleep(20)

        for file in os.listdir(facturas):
            if file.endswith(".pdf"):  # Filtrar archivos PDF
                old_path = os.path.join(facturas, file)
                print('archivo encontrado', file)
                new_name = f"Consultation S.A Puertos - Lineas Moviles - {file}"
                new_path = os.path.join(facturas, new_name)

            # Renombrar el archivo
            os.rename(old_path, new_path)
            print(f"Archivo descargado y renombrado a: {new_path}")
            break


    elif (servicio == 'Otros Productos Empresas'):
        print('servicio de Otros Productos Empresas')
        lineas_moviles = driver.find_element(By.XPATH, "//div[@data-ui-element='card - Facturas Otros Productos Empresa']")
        lineas_moviles.click()

        sleep(10)
        
        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
        print('inputs capturados:', len(inputs))

        input_cliente= inputs[0]
        input_cliente.click()
        input_cliente.send_keys('0000095735')
        sleep(5)
        input_cliente.send_keys(Keys.ARROW_DOWN)
        input_cliente.send_keys(Keys.ENTER)
        input_cliente.click()
        
        print('informacion seteada')
        print(input_cliente.get_attribute("value"))


        input_acuerdo=inputs[1]
        input_acuerdo.click()    
        input_acuerdo.send_keys('60271')
        sleep(5)
        input_acuerdo.send_keys(Keys.ARROW_DOWN)
        input_acuerdo.send_keys(Keys.ENTER)
        input_acuerdo.click()
        
        print('informacion seteada')
        print(input_acuerdo.get_attribute("value"))

        sleep(10)

        
        try:
            encuesta= wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog']")))
            print('cuadro de encuesta renderizado')

            botonCerrar= encuesta.find_element(By.CSS_SELECTOR, "button[aria-label='cerrar']")
            botonCerrar.click()

            print('presionado el boton para cerrar la encuesta')
        except Exception:
            print('no se renderizo ningun cuadro de dialog')


        #Se captura la tabla
        tabla = driver.find_element(By.CSS_SELECTOR, "table[role='table']")

        #Se captura las filas 

        filas= tabla.find_elements(By.CSS_SELECTOR, "tbody tr")
        print(f"Número de filas en el tbody: {len(filas)}")


        filasMesActual = []

        for fila in filas:
            columnas= fila.find_elements(By.CSS_SELECTOR, "td")

            if mesActual in columnas[2].text:
                filasMesActual.append(fila)


        print(f"filas con el mes actual ({mesActual}): {len(filasMesActual)}") #ESTO SE DEBE ELIMINAR DEL CODIGO

        for fila in filasMesActual:
            print(f"filas con el mes actual: {fila.text}")   #ESTO SE DEBE ELIMNAR DEL CODIGO
            button_descarga = fila.find_element(By.CSS_SELECTOR, "button[data-ui-element='Descarga']")

            button_descarga.click()
            print("Botón de descarga  clickeado con éxito.")
            sleep(10)
            # Hacer clic en el botón de descarga
            print("Factura descargada en la carpeta:", facturas)

            sleep(20)

        for file in os.listdir(facturas):
            if file.endswith(".pdf"):  # Filtrar archivos PDF
                old_path = os.path.join(facturas, file)
                print('archivo encontrado', file)
                new_name = f"Consultation S.A Puertos - Otros Productos Empresa - {file}"
                new_path = os.path.join(facturas, new_name)

                # Renombrar el archivo
                os.rename(old_path, new_path)
                print(f"Archivo descargado y renombrado a: {new_path}")
        

        

        





