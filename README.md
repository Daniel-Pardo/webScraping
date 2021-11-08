# Web scraping para el portal inmobiliario Fotocasa.es

## Autor
Daniel Pardo Navarro

## Descripción  
Los portales inmobiliarios constituyen un elemento imprescindible en la actualidad para la compra-venta de propiedades. En este sentido, los usuarios de estos portales son tanto clientes privados como empresas y agencias inmobiliarias. Los compradores pueden hacer búsquedas parametrizando diferentes criterios de acuerdo con sus necesidades por lo que obtiene una visión global del mercado. En este proyecto se implementa un web scraper para recoger todos estos datos relevantes del portal inmobiliario Fotocasa (https://www.fotocasa.es/) debido a su relevancia en el mercado. Este portal es el segundo más importante de España en la actualidad y recibe cerca de casi 16 millones de visitas al mes (https://www.helpmycash.com/cat/vender-piso/portales-inmobiliarios/).
En el portal web Fotocasa.es se publican anuncios para vender o alquilar una propiedad tanto por parte de los vendedores privados como agentes o inmobiliarias. Estas publicaciones las visualizan posibles compradores en la búsqueda de alguna propiedad. Al recoger la información que contienen estos anuncios se abre la posibilidad de que el dataset generado pueda ser utilizado de múltiples formas como analizar la situación del mercado inmobiliario, hacer estudios de mercado o de la competencia o búsquedas de oportunidades de inversión el mercado.

![Image](https://github.com/Daniel-Pardo/webScraping/blob/main/diagrama.png)

## Ficheros
- PRA_1.pdf: Contiene el documento con la respuesta a las preguntas planteadas en la práctica
- webScraping: Fichero con el proyecto:
  -   main.py: Código para ejecutar el web scrapping
  -   chromedriver.exe: Herramienta para la automatización de Chrome en un servidor remoto, necesario para el funcionamiento de la librería Selenium. 
  -   comprar_viviendas_huesca_04_11_2021.csv: Conjunto de datos de salida para el ejemplo de Comprar Viviendas en la provincia de Huesca.
  -   images: Directorio con las imágenes de salida del dataset de ejemplo anterior. 

## Conjunto de datos

El dataset que genera el script incluye 22 campos diferentes, aunque no todos ellos son obligatorios. A continuación, se describe cada uno de los campos:

-	**Identificador** - Como obligatorio. Este campo contiene un identificador único que permite identificar a las publicaciones de forma unívoca. Se utiliza el mismo identificador que asigna el portal web. 
-	**Provincia** - Campo obligatorio. Nombre de la provincia en la que se ubica la propiedad. 
-	**Municipio** - Campo obligatorio. Municipio donde se encuentra el inmueble. 
-	**Zona** - Campo obligatorio. Zona de la localidad del inmueble. 
-	**Tipo** - Campo obligatorio. Permite identificar el tipo de inmueble concreto. El tipo de inmueble puede ser en general piso, loft, apartamento, ático, dúplex, planta baja, estudio, casa o chalet, casa adosada, finca rústica, garaje, oficina, trastero, terreno, edificio, local o nave industrial dependiendo de las opciones seleccionas. 
-	**Precio** - Campo obligatorio. Precio de venta expresado en euros y sin comas ni puntos decimales.
-	**Dimensión** - Campo obligatorio. Dimensión del inmueble expresada en metros cuadrados.
-	**Habitaciones** - Número de unidades de habitaciones con las que cuenta el inmueble.
-	**Lavabos** - Número de unidades de lavabos de la propiedad.
-	**Planta** - Número de planta en la que se encuentra el inmueble.
-	**Ascensor** - Si la propiedad cuenta con ascensor el campo será “SI”. Para el resto de los casos el campo estará vacío ya que no se puede deducir si realmente no tiene ascensor o falta indicar esta información. 
-	**Parking** - Especifica si la propiedad cuenta con parking.
-	**Estado** - Estado de conservación del inmueble.
-	**Calefacción** - Tipo de energía que utiliza el mecanismo de calefacción.
-	**Agua caliente** - Tipo de energía que se utiliza para calentar el agua. 
-	**Antigüedad** - Años de antigüedad desde la construcción el inmueble.
-	**Orientación** - Orientación respecto de los puntos cardinales.
-	**Amueblado** - Contiene la información sobre si el inmueble está amueblado.
-	**Consumo** - Calificación energética de consumo de energía.
-	**Emisiones** - Calificación sobre las emisiones de CO2. 
-	**Vendedor** - Identifica si es un particular o el nombre de la agencia inmobiliaria que publica el anuncio. 
-	**Imagen** - Campo obligatorio. Se identifica con “SI” en el caso de que se haya descargado la imagen principal del anuncio. En caso de que el anuncio no contenga imagen el campo será “NO”. Las imágenes se guardan en el fichero “images” y tiene como nombre el mismo valor del identificador de la publicación concreta.  

## Ejecución
Se deben indicar 3 parámetros:
- -a: Acción sobre la que hacer la búsuqeda ("comprar", "alquiler", "promociones-obra-nueva", "compartir", "alquiler-vacacional")
- -t: Tipo de propuedad ("viviendas", "locales", "garajes", "oficinas", "trasteros", "terrenos", "edificios")
- -p: Provincia de España
```sh
python main.py -a comprar -t viviendas -p barcelona
```

## Salida
Se obtiene un fichero *.csv* identificado por la acción, el tipo de propiedad, la provincia y la fecha en la que se lanza el script. Además, en el directorio *images* se almacena la imagen principal de cada anuncio con el identificador del anuncio como nombre. 

## DOI de Zenodo del conjunto de datos
- archivo .csv: https://zenodo.org/record/5645835 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5645835.svg)](https://doi.org/10.5281/zenodo.5645835)
- conjunto de imagenes: https://zenodo.org/record/5652229 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5652229.svg)](https://doi.org/10.5281/zenodo.5652229)
