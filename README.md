# Web scraping para el portal inmobiliario Fotocasa.es

## Autor
Daniel Pardo Navarro

## Descripción  
Los portales inmobiliarios constituyen un elemento imprescindible en la actualidad para la compra-venta de propiedades. En este sentido, los usuarios de estos portales son tanto clientes privados como empresas y agencias inmobiliarias. Los compradores pueden hacer búsquedas parametrizando diferentes criterios de acuerdo con sus necesidades por lo que obtiene una visión global del mercado. En este proyecto se implementa un web scraper para recoger todos estos datos relevantes del portal inmobiliario Fotocasa (https://www.fotocasa.es/) debido a su relevancia en el mercado. Este portal es el segundo más importante de España en la actualidad y recibe cerca de casi 16 millones de visitas al mes (https://www.helpmycash.com/cat/vender-piso/portales-inmobiliarios/).

## Ejecución
Se deben indicar 3 parámetros:
- -a Acción sobre la que hacer la búsuqeda ("comprar", "alquiler", "promociones-obra-nueva", "compartir", "alquiler-vacacional")
- -t Tipo de propuedad ("viviendas", "locales", "garajes", "oficinas", "trasteros", "terrenos", "edificios")
- -p Provincia de España
```sh
main.py -a comprar -t viviendas -p barcelona
``
