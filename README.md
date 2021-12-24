# Video URL Downloader

## Introducción

El siguiente proyecto sirve para descargar series de una manera automática del servidor de Discord de Japan Paws mediante URL's y guardarlas en una Base de Datos de manera estructurada de manera automatizada. 

## Uso del Scraper

Para utilizar el programa utilice la siguiente sintaxis desde la carpeta raíz:

```sh
python3 pipeline.py
```

**Note**: es recomendable el uso de entornos virtuales para la instalación de las múltiples dependencias del proyecto.


## Instalación

> **Note**: Para ejecutar con éxito el programa, se tiene que ejecutar el siguiente comando para instalar las dependencias necesarias de Python que se encuentran en el archivo de requirements.txt:


```sh
pip3 install -r requirements.txt 
```


## Configuración
Para agregar una serie y que ésta se agregue al programa, basta con modificar el archivo de configuración "config.yaml" ubicado en la carpeta "/extract" con la siguiente sintaxis:
```
jp-paw-series:
	<anime>:
		 <url>:
```