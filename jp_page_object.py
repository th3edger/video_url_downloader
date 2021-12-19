from os import link
import bs4
import requests
from common import config

class JpPage:
    def __init__(self, serie_uid, url) -> None:
        self._config = config()['jp-paw-series'][serie_uid]
        self._queries = config()['queries']
        self._html = None

        self._visit(url)
    

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        respuesta = requests.get(url)
        #Metodo que nos permite aventar un errror si la solicitud no fue concluida correctamente
        respuesta.raise_for_status()

        self._html = bs4.BeautifulSoup(respuesta.text, 'html.parser')


    @property
    def link_caps(self):
        lista_links = []
        for link in self._select(self._queries['link_capitulo']):
            if link and link.has_attr('href'):
                lista_links.append(link)

        return [link['href'] for link in lista_links]