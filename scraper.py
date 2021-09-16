import requests
import lxml.html as html

# LINK = 'https://biblioteca.japan-paw.wtf/0:/Anime/B/[Tsubaki]%20Bokura%20wa%20Minna%20Kawai-sou%20[BD%201080p]/[Tsubaki]%20Bokura%20wa%20Minna%20Kawai-sou%20[BD%201080p]mirror.html'

XPATH_LINKS_A_DESCARGAR = '//td/a[@class = "enlaces"]/@href'
XPATH_TITULOS_CAPS = '//td/a[@class = "enlaces" and @href]/p/text()'
XPATH_SERIE = '//div[@style]/h1/text()'


def make_files(links, t_caps, nombre_anime):
    with open('zeldas.txt', 'w') as f:
        for iterador in links:
            f.write(iterador)

    diccionario = dict(zip(t_caps, links))

    with open('diccionario.txt', 'w') as f:

        f.write(f"{nombre_anime} \n\n")

        for llave in diccionario:
            f.write(f"{llave} : {diccionario[llave]}" )



def parse_links(link_a_scrapear):
    try:
        
        respuesta = requests.get(link_a_scrapear)
        respuesta2 = requests.get(link_a_scrapear)
        respuesta3 = requests.get(link_a_scrapear)
        
        if respuesta.status_code and respuesta2.status_code and respuesta3.status_code == 200:
            
            link = respuesta.content.decode('utf-8')
            link_2 = respuesta2.content.decode('utf-8')
            link_3 = respuesta3.content.decode('utf-8')

            parseado = html.fromstring(link)
            parseado2 = html.fromstring(link_2)
            parseado3 = html.fromstring(link_3)

            links_a_descargar = parseado.xpath(XPATH_LINKS_A_DESCARGAR)
            titulos_caps = parseado2.xpath(XPATH_TITULOS_CAPS)
            nombre_anime = parseado3.xpath(XPATH_SERIE)[0]
            nombre_anime = nombre_anime.replace('\'', '')

            make_files(links_a_descargar, titulos_caps, nombre_anime)

        else:
            raise ValueError(f'Error: {respuesta.status_code}')

    except ValueError as ve:
        print(ve)



def run():

    pagina = input("Ingrese el link de la descarga:  ")
    print()
    parse_links(pagina)


if __name__ == '__main__':
    run()