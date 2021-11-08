import argparse
import datetime
import math
import numpy as np
import random
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.chrome.options import Options
import time
import warnings
warnings.filterwarnings("ignore") #no mostramos los warnings

#funcion para guardar una imagen
def guardarImg(url, identificador):
    r = requests.get(url, stream = True)
    if r.status_code == 200:
        ruta = "./images/"+identificador+".jpg"
        output = open(ruta,"wb")
        for chunk in r:
            output.write(chunk)
        output.close()
        
        
def scrapFotocasa(accion, tipo, provincia):

    #definimos el nombre del archivo de salida
    fecha = datetime.datetime.now().strftime('%d_%m_%Y')
    nombre_archivo = accion + "_" + tipo + "_" + provincia + "_" + fecha
    
    #abrimos el archivo de salida
    salida = open("./"+nombre_archivo+".csv", "w")

    #definimos la url base de la web
    if accion == "promociones-obra-nueva":
        url_base = "https://www.fotocasa.es/es/"+accion+"/comprar/"+tipo+"/"+provincia+"-provincia/todas-las-zonas/l/"
    else:
        url_base = "https://www.fotocasa.es/es/"+accion+"/"+tipo+"/"+provincia+"-provincia/todas-las-zonas/l/"
    
    #añadimos la cabecera con el nombre los campos al archivo de salida
    np.savetxt(salida, [np.concatenate([["Identificador"],["Provincia"], ["Municipio"], ["Zona"], 
                                        ["Tipo"],["Precio"],["Dimensión"],["Habitaciones"], ["Lavabos"],
                                        ["Planta"],["Ascensor"],["Parking"],["Estado"], ["Calefacción"],
                                        ["Agua caliente"],["Antigüedad"],["Orientación"],["Amueblado"],
                                        ["Consumo"],["Emisiones"],["Vendedor"], ["Imagen"]])], fmt="%s", delimiter=',')
    
    #variables para guardar los diferentes campos
    identificador = ""
    ubicacion = ""
    zona = ""
    tipo = ""
    precio = ""
    dimension = ""
    habitaciones = ""
    lavabo = ""
    planta = ""
    ascensor = ""
    parking = ""
    estado = ""
    calefaccion = ""
    agua = ""
    antig = ""
    orientacion = ""
    amueblado = ""
    consumo = ""
    emisiones = ""
    vendedor = ""
    imagen = ""
       
    #definimos el path donde tenemos chromedriver
    DRIVER_PATH = './chromedriver.exe'
    
    #definimos oopciones del webdriver
    options = Options()
    options.headless = True #Si es False se abri el navegador
    options.add_argument("--window-size=1920,1200") #tamaño de la pantalla
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\
37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")
    
    #creamos un objeto
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    #cargamos la url base definida
    driver.get(url_base)
    driver.implicitly_wait(10)
    
    #click para aceptar el aviso de cookies
    try:
        driver.find_element_by_xpath('//*[@id="App"]/div[4]/div/div/div/footer/div/button[2]').click()
    except NoSuchElementException:
        print("Error al aceptar cookies")

    #a partir del número total de propiedades calculamos las páginas que hay, 30 por cada página
    total = math.ceil(int(driver.find_element_by_class_name("re-SearchTitle-count").text.replace(".",""))/30)
    
    #visitamos todas las paginas para cargar todas las propiedades
    for pag in range(total):
        
        #reset de variables en cada iteración para evitar errores
        identificador = ""
        ubicacion = ""
        zona = ""
        tipo = ""
        precio = ""
        dimension = ""
        habitaciones = ""
        lavabo = ""
        planta = ""
        ascensor = ""
        parking = ""
        estado = ""
        calefaccion = ""
        agua = ""
        antig = ""
        orientacion = ""
        amueblado = ""
        consumo = ""
        emisiones = ""
        vendedor = ""
        imagen = ""

        #definimos la nueva url a cargar
        print("Pagina ", pag+1)
        url = url_base + str(pag+1)
        
        #caso de propiedades de obra nueva
        if accion == "promociones-obra-nueva":
            url += "?conservationStatusIds=10"
            
        #cargamos la pagina
        driver.get(url)
        driver.implicitly_wait(10)

        #scroll down de la web para cargar los elementos
        height_web = driver.execute_script("return document.body.scrollHeight")
        pasos = math.floor(height_web/200)
        for i in range(0, pasos*200, 200):
            driver.execute_script("window.scrollTo(0, "+str(i)+");")
            time.sleep(random.uniform(0.1,0.3))
    
        #buscamos todos los elementos de las propiedades
        try:
            elementos = driver.find_elements_by_class_name("re-CardPackMinimal-info-container")
            if elementos == []:
                elementos = driver.find_elements_by_class_name("re-CardPackPremium-info-container")
        except:
            print("Error: Elementos")
        
        
        ubicaciones = []
        urls = []
        
        #de los elementos guardamos la ubicacion y la url detalle de la propiedad
        for i in range(len(elementos)):
    
            #obtenemos ubicacion general
            try:
                ubicacion = elementos[i].find_element_by_class_name('re-CardTitle') #
                ubicacion = ubicacion.text.replace(ubicacion.find_element_by_xpath('./span').text,'')
                
                #quitamos las comas del string
                while ubicacion.find(',') != -1:
                    ubicacion = ubicacion[ubicacion.find(',')+1:]
                
                #guardamos ubicacion 
                ubicaciones.append(ubicacion)
            except:
                ubicaciones.append("")
                print("Error: Ubicación")

            #guardamos urls
            try:
                urls.append(elementos[i].get_attribute('href'))
            except:
                print("Error: URL propiedad")
                
            
        #visitamos todas las url detalle de las propiedades
        for i in range(len(elementos)):
    
            #cargamos la url detalle
            driver.get(urls[i])
            driver.implicitly_wait(10)
    
            #scroll down de la web para cargar los elementos
            height_web = driver.execute_script("return document.body.scrollHeight")
            pasos = math.floor(height_web/200)
            for j in range(0, pasos*200, 200):
                driver.execute_script("window.scrollTo(0, "+str(j)+");")
                time.sleep(random.uniform(0.1,0.3))
            
            #obtenemos los diferentes campos de interes para almacenarlos
            #zona
            try:
                zona = driver.find_element_by_class_name("re-DetailMap-address").text
                while zona.find(',') != -1:
                    zona = zona[zona.find(',')+1:]
            except:
                zona = ""
                print("Error: Zona ", urls[i])
            
            
            #precio
            try:
                precio = driver.find_element_by_class_name("re-DetailHeader-price").text
                precio = precio.replace(".", "") #limpiamos el campo
                precio = precio.replace("€", "")
            except:
                precio = ""
                print("Error: Precio ", urls[i])
                
                
            #vendedor
            try:
                vendedor = driver.find_element_by_class_name("re-ContactDetail-inmoContainer-clientName").text
                while vendedor.find(',') != -1: 
                    vendedor = vendedor[vendedor.find(',')+1:] #limpiamos el campo
            except:
                vendedor = ""
                print("Error: Vendedor ", urls[i])


            #identificador
            try: 
                identificador = driver.find_elements_by_class_name("re-ContactDetail-referenceContainer-reference")[1].text
            except:
                identificador = ""
                print("Error: Identificador ", urls[i])
            
            #recogemos el primer conjunto de caracteristicas para almacenarlas
            caracteristicas1 = []
            try:
                caracteristicas1 = driver.find_elements_by_class_name("re-DetailHeader-featuresItem")
            except:
                print("Error: caracteristicas1 ", urls[i])
                caracteristicas1 = []
            
            #buscamos los componentes que hay en la propiedad
            for caracteristica in caracteristicas1:
                #dimension
                try:
                    if "m²" in caracteristica.find_element_by_xpath('./span[2]').text:
                        dimension = caracteristica.find_element_by_xpath('./span[2]').text.replace("m²", "")
                except:
                    dimension = ""
                    print("Error: Dimensión ", urls[i])
                    
                    
                #numero de habitaciones
                try:
                    if "habs." in caracteristica.find_element_by_xpath('./span[2]').text:
                        habitaciones = caracteristica.find_element_by_xpath('./span[2]').text.replace("habs.", "")
                except:
                    habitaciones = ""
                    print("Error: Habitaciones ", urls[i])
                    
                    
                #numero de plantas
                try:
                    if "planta" in caracteristica.find_element_by_xpath('./span[2]').text:
                        planta = caracteristica.find_element_by_xpath('./span[2]').text.replace("ª Planta", "")
                except:
                    planta = ""
                    print("Error: Plantas ", urls[i])
                
                
                #numero de lavabos
                try:
                    if "baños" in caracteristica.find_element_by_xpath('./span[2]').text:
                        lavabo = caracteristica.find_element_by_xpath('./span[2]').text.replace("baños", "")
                except:                    
                    lavabo = ""
                    print("Error: Baños ", urls[i])
                    
                    
            #recogemos el segundo conjunto de caracteristicas para almacenarlas
            caracteristicas2 = []
            try:
                caracteristicas2 = driver.find_elements_by_class_name("re-DetailFeaturesList-featureContent")
            except:
                print("Error: caracteristicas2 ", urls[i])
                caracteristicas2 = []

            for caracteristica in caracteristicas2:
                #ascensor
                try:
                    if "Ascensor" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                        ascensor = "SI"
                except:
                    ascensor = ""
                    print("Error: Ascensor ", urls[i])
                    
                    
                #consumo
                try:
                    if "Consumo" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                        consumo = caracteristica.find_element_by_xpath('./p[2]/div/div/div[1]').text
                except:
                    try:
                        if "Consumo" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                            consumo = caracteristica.find_element_by_xpath('./p[2]/div/div[1]').text
                    except:
                        consumo = ""
                        print("Error: Consumo ", urls[i])
                        
                        
                #emisiones                        
                try:
                    if "Emisiones" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                        emisiones = caracteristica.find_element_by_xpath('./p[2]/div/div/div[1]').text
                except:
                    try:
                        if "Emisiones" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                            emisiones = caracteristica.find_element_by_xpath('./p[2]/div/div[1]').text
                    except:
                        emisiones = ""
                        print("Error: Emisiones ", urls[i])
                        
                        
                #tipo de propiedad                        
                try:
                    if "Tipo" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                            tipo = caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureValue').text
                except:
                    tipo = ""
                    print("Error: Tipo ", urls[i])
                
                
                #amueblado                        
                try:
                    if "Amueblado" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                        amueblado = caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureValue').text
                except:
                    amueblado = ""
                    print("Error: Amueblado ", urls[i])
                    
                    
                #parking                        
                try:
                    if "Parking" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                        parking = caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureValue').text
                except:
                    parking = ""
                    print("Error: Parking ", urls[i])
                    
                    
                #estado                        
                try:
                    if "Estado" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                        estado = caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureValue').text
                except:
                    estado = ""
                    print("Error: Estado ", urls[i])
                    
                    
                #antigüedad                        
                try:
                    if "Antigüedad" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                        antig = caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureValue').text
                except:
                    antig = ""
                    print("Error: Antigüedad ", urls[i])
                    
                    
                #calefaccion                        
                try:
                    if "Calefacción" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                        calefaccion = caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureValue').text
                except:
                    calefaccion = ""
                    print("Error: Calefacción ", urls[i])
                    
                    
                #agua                        
                try:
                    if "Agua" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                        agua = caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureValue').text
                except:
                    agua = ""
                    print("Error: Agua ", urls[i])
                    
                    
                #orientacion                        
                try:
                    if "Orientación" in caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureLabel').text:
                        orientacion = caracteristica.find_element_by_class_name('re-DetailFeaturesList-featureValue').text
                except:
                    orientacion = ""
                    print("Error: Orientación ", urls[i])
                
            #si no tenemos identificador no guardamos los datos
            if identificador != "":
                
                try: 
                    #buscamos la url de la imagen principal
                    url_foto = driver.find_element_by_class_name('re-DetailMosaicPhoto').get_attribute("src")
                    #guardamos la imagen principal
                    guardarImg(url_foto,identificador)
                    imagen = "SI"

                except:
                    print("Error: Descargar imagen ", urls[i])
                    imagen = "NO"

                    
                #volcamos los datos en el archivo de salida
                np.savetxt(salida, [np.concatenate([[identificador],[provincia], [ubicaciones[i]], [zona], 
                                                    [tipo],[precio],[dimension],[habitaciones],[lavabo],[planta],
                                                    [ascensor],[parking],[estado],[calefaccion],[agua],[antig],
                                                    [orientacion],[amueblado],[consumo],[emisiones],[vendedor],
                                                    [imagen]])],fmt="%s", delimiter=',')
            #volvemos a la url anterior
            driver.back()
    
    #cerramos el archivo y el driver
    salida.close()
    driver.quit()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Web Scraping Fotocasa.es')
    parser.add_argument('-a','--accion', help="Tipo de transaccion", choices=["comprar", "alquiler", "promociones-obra-nueva", "compartir", "alquiler-vacacional"], default="comprar")
    parser.add_argument('-t', '--tipo', help='Tipo de propiedad', choices=["viviendas", "locales", "garajes", "oficinas", "trasteros", "terrenos", "edificios"], default="viviendas")
    parser.add_argument('-p', '--provincia', help='Provincia de la búsqueda', default = "huesca")
    args = parser.parse_args()
    
    lista_provincias=["a-coruna", "araba-alava", "albacete", "alicante", "almeria", "asturias", "avila",
                      "badajoz","illes-balears", "barcelona", "burgos", "caceres", "cadiz", "cantabria",
                      "castellon", "ceuta", "ciudad-real", "cordoba", "cuenca", "girona", "granada", 
                      "guadalajara", "gipuzkoa", "huelva", "huesca","jaen", "la-rioja", "las-palmas", 
                      "leon", "lleida", "lugo", "madrid", "malaga", "melilla", "murcia","navarra", 
                      "ourense", "palencia", "pontevedra", "salamanca", "segovia", "sevilla", "soria", 
                      "tarragona","santa-cruz-de-tenerife", "teruel", "toledo", "valencia", 
                      "valladolid", "bizkaia", "zamora", "zaragoza"]


    if args.accion not in ["comprar", "alquiler", "promociones-obra-nueva", "compartir", "alquiler-vacacional"]:
        raise Exception("ERROR: Introduce una acción correcta")
        exit()

    if args.tipo not in ["viviendas", "locales", "garajes", "oficinas", "trasteros", "terrenos", "edificios"]:
        raise Exception("ERROR: Introduce el tipo de propiedad correcto")
        exit()
    
    if args.accion in ["promociones-obra-nueva", "compartir", "alquiler-vacacional"] and args.tipo != "viviendas":
        raise Exception("ERROR: la acción "+args.tipo+" solo es posible para el tipo viviendas")
        exit()

    if args.provincia not in lista_provincias:
        print("Nombres de provincias aceptados:")
        for i in lista_provincias:
            print(i)
        raise Exception("ERROR: Introduce un nombre de provincia correcto")
        exit()
        
    scrapFotocasa(args.accion, args.tipo, args.provincia)


