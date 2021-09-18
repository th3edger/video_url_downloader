import os, re, requests
import lxml.html as html


XPATH_LINKS_A_DESCARGAR = '//td/a[@class = "enlaces"]/@href'
XPATH_TITULOS_CAPS = '//td/a[@class = "enlaces" and @href]/p/text()'
XPATH_SERIE = '//div[@style]/h1/text()'

PATRON_REGEX = re.compile(r'https?:\/\/[^o].+$')

def make_files(links: list, t_caps: list, nombre_anime: str):

    if not os.path.isdir('anime/'+nombre_anime):
        os.mkdir('anime/'+nombre_anime)

    with open('anime/'+nombre_anime+'/'+nombre_anime+'_zeldas.txt', 'w', encoding='utf-8') as f:
        for iterador in links:
            iterador = "".join(iterador)
            f.write(iterador+"\n")

    diccionario = dict(zip(t_caps, links))


    with open('anime/'+nombre_anime+'/'+nombre_anime+'.txt', 'w', encoding='utf-8') as f:
        nombre_anime = "".join(nombre_anime)
        
        f.write(f"{nombre_anime} \n\n")

        for llave in diccionario:
            f.write( f"{llave} : {diccionario[llave]}\n" )


def regex(lista: list) -> list:
    
    lista_limpia = []

    for line in lista:
        res = re.findall(PATRON_REGEX, line)
        lista_limpia.append(res)
        
    return lista_limpia


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
            
            #se limpia un poco el nombre del anime
            nombre_anime = nombre_anime.replace('\'', '')
            nombre_anime = nombre_anime.replace('[', '')
            nombre_anime = nombre_anime.replace(']', ' -')
            
            links_a_descargar = regex(links_a_descargar)

            make_files(links_a_descargar, titulos_caps, nombre_anime)

        else:
            raise ValueError(f'Error: {respuesta.status_code}')

    except ValueError as ve:
        print(ve)



def run():

    # pagina = input("Ingrese el link de la descarga:  ")
    # print()
    # parse_links(pagina)
    paginas = (
        'https://biblioteca.japan-paw.net/0:/Anime/G/[MKNF]%20Grisaia%20no%20Kajitsu%20[BD%201080p]/[MKNF]%20Grisaia%20no%20Kajitsu%20[BD%201080p].html',
        'https://biblioteca.japan-paw.net/0:/Anime/E/Evangelion:%203.0+1.0%20Thrice%20Upon%20a%20Time/Evangelion%203.0+1.0%20Thrice%20Upon%20a%20Time.html',
        'https://biblioteca.japan-paw.wtf/0:/Anime/B/[Tsubaki]%20Bokura%20wa%20Minna%20Kawai-sou%20[BD%201080p]/[Tsubaki]%20Bokura%20wa%20Minna%20Kawai-sou%20[BD%201080p]mirror.html',
        'https://biblioteca.japanpaw.workers.dev/0:/Anime/F/[PuyaSubs!]%20Fairy%20Tail%20S2%20[1080p]/[PuyaSubs!]%20Fairy%20Tail%20S2%20[1080p].html',
        'https://biblioteca.japanpaw.workers.dev/0:/Anime/F/[BB]%20Fairy%20Tail%20[BD-Tv%20720p]%20+%206%20OVAs/[BB]%20Fairy%20Tail%20[BD-Tv%20720p]%20+%206%20OVAs.html'
    )

    for iterador in paginas:
        parse_links(iterador)

if __name__ == '__main__':
    run()