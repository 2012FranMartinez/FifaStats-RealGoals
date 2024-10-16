from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
# import urllib3 # urllib3 es un cliente HTTP potente y fácil de usar para Python.
import re # Expresiones regulares 
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import random
from selenium.webdriver.common.keys import Keys

from datetime import datetime

fecha_actual = datetime.now().strftime("%d_%m_%Y")
fecha_actual = str(fecha_actual)
print(f"==>> fecha_actual: {fecha_actual}")


visualizar = True


fichero_final = f"DatosReales_{fecha_actual}.csv"
print(f"==>> fichero_final: {fichero_final}")

competiciones = ["primera","premier","serie_a","bundesliga","ligue_1","portugal","holanda","championship","segunda","champions","uefa"]
competiciones = ["primera","premier","serie_a","ligue_1"]


def delay_random_wait():
    # time.sleep(random.randint(4,8))
    time.sleep(1)

def waitAndClickElement(elemento):
    delay_random_wait()
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, elemento))
        )
        # Hacer clic en el botón
        button.click()
        print(f"Hiciste clic en el botón {elemento}")
    except TimeoutException:
        print(f"El botón {elemento} no apareció o no es clicable")

def scroll(driver,xpath):
    elemento = driver.find_element("xpath", xpath)
    driver.execute_script("arguments[0].scrollIntoView();", elemento)
   
def scroll_until_element(driver, xpath, max_scrolls=70):
    for scroll_attempt in range(max_scrolls):
        try:
            # Intentar encontrar el elemento
            ele_click = driver.find_element(By.XPATH, xpath)
            # Si se encuentra, salir del bucle y hacer click
            ele_click.click()
            print(f"Elemento encontrado en intento {scroll_attempt + 1}")
            break
        except:
            # Si no se encuentra, hacemos scroll hacia abajo
            body = driver.find_element("tag name", 'body')
            body.send_keys(Keys.PAGE_DOWN)  # Simula el presionar de la tecla "Page Down"
            
            driver.execute_script("window.scrollTo(0, 500);")  # Hacer scroll hacia abajo 500 píxeles

            print(f"Scroll attempt {scroll_attempt + 1} realizado")
    else:
        # Si después de todos los intentos no se encuentra, mostramos un mensaje de error
        print(f"Elemento no encontrado después de {max_scrolls} intentos")

def waitAndGetElement(driver, value, timeout=2):
    delay_random_wait()
    """
    Espera a que un elemento esté presente en la página y devuelve su texto.

    :param driver: WebDriver de Selenium.
    :param by: Estrategia de localización (ej. By.ID, By.XPATH).
    :param value: Valor del selector.
    :param timeout: Tiempo máximo de espera en segundos.
    :return: Texto del elemento o None si no se encuentra.
    """

    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, value))
        )
        return element.text
    except Exception as e:
        print(f"Error: {e}")
        return None

def extraer_stats_jugadores(dict_to_fill,equipo):
    # iterar por los jugadores para sacar las stats reales
    jugadores = driver.find_elements(By.XPATH, "//td[@class='name']")
    cantidad_jugadores = len(jugadores)
    if visualizar:
        print("JUGADORES EN PLANTILLA:",cantidad_jugadores)

    for index, jugador in enumerate(jugadores):
        # Obtener el texto de cada elemento
        if index+1 < cantidad_jugadores+1:
            nombre = driver.find_element(By.XPATH, f"(//td[@class='name'])[{index+1}]").text
            print(f"Elemento {index + 1}: {nombre}")
            dict_to_fill["nombre"].append(nombre) # Añadir en el diccionario            
        else:
            break

        
        dict_to_fill["equipo"].append(equipo)
        
        # Recorrer cada stat de cada jugador
        stats_jugador = driver.find_elements(By.XPATH, f"(//td[@class='name'])[{index+1}]/following-sibling::td[@data-content-tab='team_performance']")
        cantidad = len(stats_jugador)
        
        # Completar la posición del jugador
        posicion = driver.find_element(By.XPATH,f"((//td[@class='name'])[{index+1}]//ancestor::tr//preceding-sibling::tr[@class='row-head'])[last()]").text
        posicion = posicion.split(" ",1)
        posicion = posicion[0]
        print(f"==>> posicion: {posicion}")
        if posicion == "Porteros":
            dict_to_fill["posicion"].append("portero")
        elif posicion == "Defensas":
            dict_to_fill["posicion"].append("defensa")
        elif posicion == "Centrocampistas":
            dict_to_fill["posicion"].append("mediocentro")
        elif posicion == "Delanteros":
            dict_to_fill["posicion"].append("delantero")

        
        if visualizar:
            print("CANTIDAD STATS:",cantidad)

        for i in range(len(stats_jugador)):
            # print(f"(//td[@class='name'])[{index+1}]/following-sibling::td[@data-content-tab='team_performance'][{i+1}]")
            stat = driver.find_element(By.XPATH, f"(//td[@class='name'])[{index+1}]/following-sibling::td[@data-content-tab='team_performance'][{i+1}]").text
            if i == 0:
                if visualizar:
                    print("pj:",stat)
                    
                dict_to_fill["pj"].append(stat)
            elif i == 1:
                if visualizar:
                    print("pt:",stat)

                dict_to_fill["pt"].append(stat)
            elif i == 2:
                if visualizar:
                    print("goles/portería:",stat)
                
                # Diferenciar etntre porteros/resto
                if posicion == "Porteros":
                    dict_to_fill["porteria"].append(stat)
                    dict_to_fill["goles"].append("0")
                else:
                    dict_to_fill["goles"].append(stat)
                    dict_to_fill["porteria"].append("0")      

            elif i == 3:
                if visualizar:
                    print("asistencias:",stat)

                dict_to_fill["asistencias"].append(stat)
            elif i == 4:
                if visualizar:
                    print("tarjetas:",stat)

                dict_to_fill["tarjetas"].append(stat)
    return dict_to_fill


dict_to_fill = {"nombre":[],
                "posicion":[],
                "pj": [],
                "pt": [],
                "goles": [],
                "asistencias": [],
                "tarjetas": [],
                "equipo":[],
                "porteria":[]}


dict_competiciones = {"primera":"Primera División",
                      "premier":"Premier League",
                      "serie_a":"Serie A",
                      "bundesliga":"",
                      "ligue_1":"Ligue 1",
                      "portugal":"",
                      "holanda":"",
                      "championship":"",
                      "segunda":"",
                      "champions":"",
                      "uefa":""
                      }

try: 

    # Lanzar el crhomedriver y preparar el driver
    service = Service(executable_path='./chromedriver.exe')

    # Opciones para el problema de SSL
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    
    # Configurar opciones de Chrome
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless
    chrome_options.add_argument("--window-size=1920x1080")  # Definir el tamaño de la ventana (opcional)

    # chrome_options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(service=service, options=options) # Driver normal
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Entramos en la pagina competiciones
    driver.get("https://es.besoccer.com/competiciones")

    # Aceptar cookies 
    # waitAndClickElement(elemento="//button[./span[text()='ACEPTO']]")
    ele_click = driver.find_element(By.XPATH,"//button[./span[text()='ACEPTO']]")
    ele_click.click()

    # ruta = "https://es.besoccer.com/competicion/clasificacion/"
    # ruta = "https://es.besoccer.com/competicion/clasificacion/real-madrid"

    # bucle for por las competiciones que se han fijado
    for competicion in competiciones:
        ruta_competicion = "https://es.besoccer.com/competicion/clasificacion/" + competicion
        driver.get(ruta_competicion)
        time.sleep(1)
        
        # Cambiar a la temporada 2022
        # waitAndClickElement(elemento="//select[@id='season']")
        # time.sleep(1)
        # waitAndClickElement(elemento="//option[@value='2022']")
        # time.sleep(1)
        ele_click = driver.find_element(By.XPATH,"//select[@id='season']")
        ele_click.click()
        ele_click = driver.find_element(By.XPATH,"//option[@value='2022']")
        ele_click.click()
        time.sleep(3)

        # Lista equipos en liga (sel)
        lista_equipos_xpath = driver.find_elements(By.XPATH,"//a[@data-cy='team']")
        # Crear una lista con los equipos
        lista_estatica_equipos = []
        for equipo in lista_equipos_xpath:
            lista_estatica_equipos.append(equipo.text)
        if visualizar:
            print("*"*50)
            print("Todos los equipos de la lisga son:",lista_estatica_equipos)
            print("Nº de equipos en la liga:", len(lista_estatica_equipos))
            print("*"*50)

        # for i, equipo in enumerate(lista_estatica_equipos):
        #     if visualizar:
        #     equipo = equipo.lower().replace(" ","_")

        # stopper = lista_estatica_equipos.index("Mallorca")
        for i,xpaht_equipo in enumerate(lista_equipos_xpath):
            current_team = lista_estatica_equipos[i].lower().replace(" ","_") # Sacar el equipo formateado para guardar en el csv
            current_url = driver.current_url # Obtener url
            print(current_url,"|",ruta_competicion)
            print(current_url,"|",ruta_competicion+"/2022")

            
            if (current_url == ruta_competicion) or (current_url == (ruta_competicion + "/2022")):
                pass
            else:
                # Cargas pagina competicion
                print(f"==>> Cargas pagina competicion:")
                driver.get(ruta_competicion)
                # Cambiar a la temporada 2022
                print(f"==>> Cambiar a la temporada 2022:")
                # waitAndClickElement(elemento="//select[@id='season']")
                # time.sleep(1)
                # waitAndClickElement(elemento="//option[@value='2022']")
                # time.sleep(1)
                ele_click = driver.find_element(By.XPATH,"//select[@id='season']")
                ele_click.click()
                ele_click = driver.find_element(By.XPATH,"//option[@value='2022']")
                ele_click.click()
                time.sleep(3)

            time.sleep(1)
            # Entra en cada equipo

            # waitAndClickElement(f"(//a[@data-cy='team'])[{i+1}]")   
            # Localiza el elemento
            print(f"Localiza el elemento: (//a[@data-cy='team'])[{i+1}]")
            ele_click = driver.find_element(By.XPATH,f"(//a[@data-cy='team'])[{i+1}]")
            print("+"*50)
            print(f"==>> ele_click: {ele_click}")
            print("+"*50)
            
            # XPath del elemento
            xpath = f"(//a[@data-cy='team'])[{i+1}]"

            # Llamar a la función
            scroll_until_element(driver, xpath)
            
            # driver.execute_script("arguments[0].scrollIntoView();",ele_click)
            # ele_click.click()
            
            current_url = driver.current_url # Obtener url
            print(f"==>> current_url: {current_url}")
            # Extrae la última parte de la URL (después del último '/')
            last_part = current_url.split('/')[-1]
            print(f"==>> last_part: {last_part}")
            if last_part ==  "mallorca":
                print("SIIIU")

            
            # Inserta '/plantilla/' entre la ruta actual y la última parte
            new_url = current_url.replace(last_part, f'plantilla/{last_part}')
            print(f"==>> new_url: {new_url}")
            driver.get(new_url)

            # Comprobar si es la competición que queremos
            # elements = driver.find_elements(By.XPATH, "//option[@value='1' and @selected]") # ***
            elements = driver.find_elements(By.XPATH, f"//option[contains(text(),'{dict_competiciones[competicion]}') and @selected]")
            print(f"//option[contains(text(),'{dict_competiciones[competicion]}') and @selected]")
            # print(f"==>> elements: {elements}")
            if elements:
                print("Si está en primera division")
                
            else:
                print("No está en primera división")
                ele_click = driver.find_element(By.XPATH,"//select[@id='competition']")
                ele_click.click()
                # ele_click = driver.find_element(By.XPATH,"//option[@value='1']")
                print(dict_competiciones[competicion])
                ele_click = driver.find_element(By.XPATH,f"//option[contains(text(),'{dict_competiciones[competicion]}')]")
                print(f"//option[contains(text(),'{dict_competiciones[competicion]}')]")
                ele_click.click()
                time.sleep(3)
                # //select[@id="competition"]


            # Cambiar a la temporada 2022
            print("Cambiar a la temporada 2022")
            ele_click = driver.find_element(By.XPATH,"//select[@id='season']")
            ele_click.click()
            ele_click = driver.find_element(By.XPATH,"//option[@value='2022']")
            ele_click.click()
            time.sleep(5)
            # waitAndClickElement(elemento="//select[@id='season']")
            # time.sleep(1)
            # waitAndClickElement(elemento="//option[@value='2022']")
            # time.sleep(1)

            # Extraer los datos de la plantilla
            dict_to_fill = extraer_stats_jugadores(dict_to_fill,current_team)
            df_stats_reales = pd.DataFrame(dict_to_fill)
            df_stats_reales.to_csv(fichero_final)
            # if visualizar:
            #     print(dict_to_fill)


            
    # Guardar ficheros
    df_stats_reales = pd.DataFrame(dict_to_fill)
    df_stats_reales.to_csv(fichero_final)
    print(df_stats_reales.head())

    print("FIN")
    print("FIN")
except:
    print("algo falló")
finally:
    # Al final, cerrar el navegador
    print("cerrando cdriver")
    driver.quit()






