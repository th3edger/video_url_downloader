import argparse
import logging
import jp_page_object as jp

from common import config
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def _series_scraper(serie_uid):
    host = config()['jp-paw-series'][serie_uid]['url']

    logging.info(f'Empezando el scraper para {host}')
    
    jppagina = jp.JpPage(serie_uid, host)

    for link in jppagina.link_caps:
        print(link)


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