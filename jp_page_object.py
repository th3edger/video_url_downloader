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
    
    def _select_title(self, query_string):
        return self._html.find(query_string).text

    def _visit(self, url):
        respuesta = requests.get(url)
        #Metodo que nos permite aventar un errror si la solicitud no fue concluida correctamente
        respuesta.raise_for_status()

        self._html = bs4.BeautifulSoup(respuesta.text, 'html.parser')



class JpSeriePage(JpPage):
    def __init__(self, serie_uid, url) -> None:
        super().__init__(serie_uid, url)


    @property
    def titulo_serie(self):
        return self._select_title(self._queries['titulo_serie'])
        

    @property
    def nom_caps(self):
        lista_nombres = []
        for nombre in self._select(self._queries['nomb_capitulo']):
            if nombre:
                lista_nombres.append(nombre.text)
        return lista_nombres

    @property
    def link_caps(self):
        lista_links = []
        for link in self._select(self._queries['link_capitulo']):
            if link and link.has_attr('href'):
                lista_links.append(link)

        return [link['href'] for link in lista_links]