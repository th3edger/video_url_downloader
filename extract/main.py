import argparse
import re
import logging
import pandas as pd

import jp_page_object as jp
from common import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

enlace_valido = re.compile(r'https?://biblioteca.+\.m[kp]{1,1}[v4]{1,1}')
titulo_valido = re.compile(r'(\s?\[[\w\s?-]+[\W]?\]\s?)?(\s?-\sJapan-Paw!)?')



def _series_scraper(serie_uid):
    host = config()['jp-paw-series'][serie_uid]['url']

    logging.info(f'Empezando el scraper para {serie_uid}\nen:{host}\n')
    
    jp_pagina_serie = jp.JpSeriePage(serie_uid, host)
    
    nombres_chiditos = []
    links_bien_chiditos = []
    for nomb_cap, link in zip(jp_pagina_serie.nom_caps, jp_pagina_serie.link_caps):
        nomb_cap = _fetch_chap_name(nomb_cap)
        link = _fetch_link(link)
        nombres_chiditos.append(nomb_cap)
        links_bien_chiditos.append(link)
    
    _save_links(_fetch_title_name(jp_pagina_serie.titulo_serie), nombres_chiditos, links_bien_chiditos)
    logging.info(f'Proceso de extraccion terminado para {_fetch_title_name(jp_pagina_serie.titulo_serie)}')



##FUNCIONES PARA _series_scraper
def _fetch_chap_name(nomb_a_revisar):
    nombre = re.sub(pattern=titulo_valido, repl='', string=nomb_a_revisar)
    string_nombre = ''.join(nombre)
    return string_nombre


def _fetch_link(link_a_revisar):
    link = re.findall(pattern=enlace_valido, string=link_a_revisar)
    string_link = ''.join(link)
    return string_link


def _fetch_title_name(titulo_a_revisar):
    titulo = re.sub(pattern=titulo_valido, repl='', string=titulo_a_revisar)
    string_titulo = ''.join(titulo)
    return string_titulo


def _save_links(titulo_serie, nom_caps, links):
    archivo_salida = f"{titulo_serie}.csv"
    archivo_salida2 = f"{titulo_serie}.txt"

    diccionario = {
        'Titulo de la Serie': titulo_serie,
        'Nombre del Capitulo': nom_caps,
        'url': links
    }

    df = pd.DataFrame(diccionario)
    df2 = pd.DataFrame(diccionario)
    df.to_csv(archivo_salida, index=False)
    df2.to_string(archivo_salida2, index=False)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    opciones_de_series = list(config()['jp-paw-series'].keys())
    parser.add_argument(
        'serie',
        help='la serie que desea analizar',
        type=str,
        choices=opciones_de_series
    )

    argumentos = parser.parse_args()
    _series_scraper(argumentos.serie)