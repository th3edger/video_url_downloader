import logging
logging.basicConfig(level=logging.INFO)
import subprocess

from extract import common as cm
logger = logging.getLogger(__name__)

animes = {
    'uzaki',
    'bokura',
    'grisaia',
    'ft-S2',
    'ft',
    'megami',
    'dal'
}


@cm.tiempo_de_ejecucion
def main():
    _extract()
    _transform()
    _load()


##FUNCIONES
def _extract():
    logger.info('Empezando el proceso de extraccion')
    
    for anime in animes:
        subprocess.run(['python', 'main.py', anime], cwd='./extract')
        subprocess.run(
            [
                'find', '.', '-name', '{}*'.format(anime),
                '-exec', 'mv', '{}', '../transform/{}_.csv'.format(anime), 
                ';'
            ], cwd='./extract'
        )


def _transform():
    logger.info('Empezando el proceso de transformacion')

    for anime in animes:
        dirty_data_filename = f"{anime}_.csv"
        clean_data_filename = f"clean_{dirty_data_filename}"
        subprocess.run(
            [
                'python', 'main.py', dirty_data_filename
            ], cwd='./transform'
        )
        subprocess.run(
            [
                'rm', dirty_data_filename
            ], cwd='./transform'
        )
        subprocess.run(
            [
                'mv', clean_data_filename, '../load/{}.csv'.format(anime)
            ], cwd='./transform'
        )



def _load():
    logger.info('Empezando el proceso de carga')
    
    for anime in animes:
        clean_data_filename = '{}.csv'.format(anime)
        subprocess.run(
            [
                'python', 'main.py', clean_data_filename
            ], cwd='./load'
        )
        subprocess.run(
            [
                'rm', clean_data_filename
            ], cwd='./load'
        )


if __name__ == '__main__':
    main()