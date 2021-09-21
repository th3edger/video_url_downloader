import os, re, requests, time
import lxml.html as html


XPATH_LINKS_A_DESCARGAR = '//td/a[@class = "enlaces"]/@href'
XPATH_TITULOS_CAPS = '//td/a[@class = "enlaces" and @href]/p/text()'
XPATH_SERIE = '//div[@style]/h1/text()'

PATRON_REGEX_HTML = re.compile(r'https?:\/\/[^o].+$')
PATRON_REGEX_TITULO = re.compile(r'\s?\[[\w\s?-]+[\W]?\]\s?')
PATRON_REGEX_TITULO_2 = re.compile(r'\s')
PATRON_REGEX_NOM_CAP = re.compile(r'\s?\[[\w\s?-]+!?[\w]?\]\s')
PATRON_REGEX_NOM_CAP2 = re.compile(r'\s')
PATRON_REGEX_EXTENSION = re.compile(r'\.m[kp]{1,1}[v4]{1,1}')


def execution_time(func):
    def envoltura(*args, **kwargs):
        tiempo_inicial = time.time()
        func(*args, **kwargs)
        tiempo_final = time.time()
        tiempo_transcurrido = tiempo_final-tiempo_inicial
        tiempo_transcurrido = round(tiempo_transcurrido, 3)
        print(f"Transcurrieron: {tiempo_transcurrido} segundos")

    return envoltura


def regex_html_links(lista: list) -> list:
    lista_limpia = []

    for line in lista:
        line = "".join(line)
        res = re.findall(PATRON_REGEX_HTML, line)
        lista_limpia.append(res)
        
    return lista_limpia


def regex_html_extensions(lista_ext: list) -> list:
    lista_limpia = []

    for line in lista_ext:
        res = "".join(line)
        result = re.findall(PATRON_REGEX_EXTENSION, res)
        lista_limpia.append(result)

    return lista_limpia


def regex_caps(lista: list) -> list:

    lista_limpia = []

    for line in lista:
        res = re.sub(PATRON_REGEX_NOM_CAP, "", line)
        res = re.sub(PATRON_REGEX_NOM_CAP2, "", res)
        lista_limpia.append(res)

    return lista_limpia


def make_files(links: list, t_caps: list, nombre_anime: str):

    if not os.path.isdir('anime/'+nombre_anime):
        os.mkdir('anime/'+nombre_anime)

    with open('anime/'+nombre_anime+'/'+nombre_anime+'_zeldas.txt', 'w', encoding='utf-8') as f:
        for iterador in links:
            f.write(str(iterador)+'\n')


    diccionario = dict(zip(t_caps, links))

    with open('anime/'+nombre_anime+'/'+nombre_anime+'.txt', 'w', encoding='utf-8') as f:
        f.write(f"{nombre_anime}\n\n")

        for llave in diccionario:
            f.write(f"{llave}: {diccionario[llave]}\n")

    
    extensiones = regex_html_extensions(links)
    with open('anime/'+nombre_anime+'/nom_caps_'+nombre_anime+'.txt', 'w', encoding='utf-8') as f:
        for capitulo, ext in list(zip(t_caps, extensiones)):
            ext = "".join(ext)
            capitulo=capitulo+ext+'\n'
            # print(f"{str(capitulo)}{ext}")
            f.write(capitulo)
    

def get_anime(link_a_scrapear):
    try:
        
        respuesta = requests.get(link_a_scrapear)
        
        if respuesta.status_code == 200:

            link_1 = respuesta.content.decode('utf-8')
            link_2 = respuesta.content.decode('utf-8')
            link_3 = respuesta.content.decode('utf-8')

            parseado_1 = html.fromstring(link_1)
            parseado_2 = html.fromstring(link_2)
            parseado_3 = html.fromstring(link_3)

            links_a_descargar = parseado_1.xpath(XPATH_LINKS_A_DESCARGAR)
            titulos_caps = parseado_2.xpath(XPATH_TITULOS_CAPS)
            nombre_anime = parseado_3.xpath(XPATH_SERIE)[0]
            
            #se limpia un poco el nombre del anime
            nombre_anime = re.sub(PATRON_REGEX_TITULO, "", nombre_anime)
            nombre_anime = re.sub(PATRON_REGEX_TITULO_2, "_", nombre_anime)
            
            links_a_descargar = regex_html_links(links_a_descargar)
            titulos_caps = regex_caps(titulos_caps)

            make_files(links_a_descargar, titulos_caps, nombre_anime)

        else:
            raise ValueError(f'Error: {respuesta.status_code}')

    except ValueError as ve:
        print(ve)



@execution_time
def run():

    # pagina = input("Ingrese el link de la descarga:  ")
    # print()
    # get_anime(pagina)
    paginas = (
        'https://biblioteca.japan-paw.net/0:/Anime/G/[MKNF]%20Grisaia%20no%20Kajitsu%20[BD%201080p]/[MKNF]%20Grisaia%20no%20Kajitsu%20[BD%201080p].html',
        'https://biblioteca.japan-paw.net/0:/Anime/E/Evangelion:%203.0+1.0%20Thrice%20Upon%20a%20Time/Evangelion%203.0+1.0%20Thrice%20Upon%20a%20Time.html',
        'https://biblioteca.japan-paw.wtf/0:/Anime/B/[Tsubaki]%20Bokura%20wa%20Minna%20Kawai-sou%20[BD%201080p]/[Tsubaki]%20Bokura%20wa%20Minna%20Kawai-sou%20[BD%201080p]mirror.html',
        'https://biblioteca.japanpaw.workers.dev/0:/Anime/F/[PuyaSubs!]%20Fairy%20Tail%20S2%20[1080p]/[PuyaSubs!]%20Fairy%20Tail%20S2%20[1080p].html',
        'https://biblioteca.japanpaw.workers.dev/0:/Anime/F/[BB]%20Fairy%20Tail%20[BD-Tv%20720p]%20+%206%20OVAs/[BB]%20Fairy%20Tail%20[BD-Tv%20720p]%20+%206%20OVAs.html',
        'https://biblioteca.japan-paw.net/0:/Anime/U/[OTNF]%20Uzaki-chan%20wa%20Asobitai!%20[BD%201080p]/[OTNF]%20Uzaki-chan%20wa%20Asobitai!%20[BD%201080p].html',
        'https://biblioteca.japan-paw.net/0:/Anime/M/[J-Paw%20Mod!]%20Megami-ryou%20no%20Ryoubo-kun%20[Web%201080p]/[J-Paw%20Mod!]%20Megami-ryou%20no%20Ryoubo-kun%20[Web%201080p].html',
        'https://biblioteca.japan-paw.net/0:/Anime/D/[Madness%20Subs]%20Date%20A%20Live%20S3%20[BD%201080p]/[Madness%20Subs]%20Date%20A%20Live%20S3%20[BD%201080p].html'
    )

    for iterador in paginas:
        get_anime(iterador)



if __name__ == '__main__':
    run()