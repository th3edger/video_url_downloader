import requests
import lxml.html as html

# LINK = 'https://biblioteca.japan-paw.wtf/0:/Anime/B/[Tsubaki]%20Bokura%20wa%20Minna%20Kawai-sou%20[BD%201080p]/[Tsubaki]%20Bokura%20wa%20Minna%20Kawai-sou%20[BD%201080p]mirror.html'

XPATH_LINKS_A_DESCARGAR = '//td/a[@class = "enlaces"]/@href'
XPATH_TITULO = '//td/a[@class = "enlaces" and @href]/p/text()'

def parse_links(link_a_scrapear):
    try:
        # response = requests.get(LINK)
        response = requests.get(link_a_scrapear) 
        
        if response.status_code == 200:
            
            link = response.content.decode('utf-8')
            parseado = html.fromstring(link)

            links_a_descargar = parseado.xpath(XPATH_LINKS_A_DESCARGAR)

            for i in links_a_descargar:
                print(i)

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)


def run():

    pagina = input("Ingrese el link de la descarga:  ")

    parse_links(pagina)


if __name__ == '__main__':
    run()