import argparse
import re
import logging

import jp_page_object as jp
from common import config
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
enlace_valido = re.compile(r'https?://biblioteca.+\.m[kp]{1,1}[v4]{1,1}')


def _series_scraper(serie_uid):
    host = config()['jp-paw-series'][serie_uid]['url']

    logging.info(f'Empezando el scraper para {host}\n')
    
    jp_pagina_serie = jp.JpSeriePage(serie_uid, host)
    
    links_bien_chiditos = []
    for link in jp_pagina_serie.link_caps:
        link = _fetch_link(link)
        links_bien_chiditos.append(link)
    

    print(f'\n\n{jp_pagina_serie.titulo_serie}\n\n')
    for nom_cap, link_cap in zip(jp_pagina_serie.nom_caps, links_bien_chiditos):
        print(f'{nom_cap}:\t{link_cap}')


def _fetch_link(link_a_revisar):
    link = re.findall(pattern=enlace_valido, string=link_a_revisar)
    string_link = ''.join(link)
    return string_link



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