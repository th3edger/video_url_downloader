import logging
import subprocess

import yaml

from extract import common as cm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
confi = None


def config():
    global confi
    if not confi:
        with open(file='./extract/config.yaml',mode='r') as file:
            confi = yaml.safe_load(file)
    
    return confi


animes = list(config()['jp-paw-series'].keys())


##FUNCIONES
def _extract():
    logger.info('Empezando el proceso de extraccion')
    
    for anime in animes:
        subprocess.run(['python', 'main.py', anime], cwd='./extract')
        subprocess.run(
            [
                'find', '.', '-name', '*.csv',
                '-exec', 'mv', '{}', '../animes/', 
                ';'
            ], cwd='./extract'
        )
        subprocess.run(
            [
                'find', '.', '-name', '*.txt',
                '-exec', 'mv', '{}', '../animes/{}', 
                ';'
            ], cwd='./extract'
        )


def _download():
    logger.info('Empezando con la descarga de las series')

    subprocess.run(
        [
            './animes-downloader.sh'
        ], cwd='./animes'
    )



@cm.tiempo_de_ejecucion
def main():
    _extract()
    _download()


if __name__ == '__main__':
    main()
