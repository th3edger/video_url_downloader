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
        #En caso de que dejen de funcionar estos Proxies se pueden cambiar en la pagina https://free-proxy-list.net
        proxies = {
            'http': 'http://193.27.78.90:80',
            'http': 'http://80.48.119.28:8080',
            'http': 'http://34.77.73.11:80'
        }
        #En caso de que dejen de funcionar estos Proxies se pueden cambiar en la pagina https://www.socks-proxy.net
        soc_proxies = {
            'http':'socks4://177.68.77.231:4153',
            'http':'socks4://103.254.167.110:5678',
            'http':'socks4://190.186.58.236:40132'
        }
        cabeceras = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
            'User-Agent': 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2',
            'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52',
            'User-Agent': 'Opera/9.80 (X11; Linux x86_64; U; Ubuntu/10.10 (maverick); pl) Presto/2.7.62 Version/11.01',
        }

        respuesta = requests.get(url, headers=cabeceras, proxies=soc_proxies)
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