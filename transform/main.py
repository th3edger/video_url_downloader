import argparse
import hashlib
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(archivo):
    logger.info('Empezando la modificacion del archivo')
    
    df = _read_data(archivo)
    df = _generate_uids_for_rows(df)
    df = _drops_rows_with_missing_values(df)
    _save_data(df, archivo)

    return df


##Funciones para Main
def _read_data(archivo):
    logger.info('Leyendo el Archivo CSV')
    return pd.read_csv(archivo)


def _generate_uids_for_rows(df):
    logger.info('Generando uids para cada fila')    
    
    uids = (
        df
        .apply( lambda fila: hashlib.md5(bytes(fila['url'].encode())), axis=1 )
        .apply( lambda hashobejct: hashobejct.hexdigest() )
    )

    df['uid'] = uids
    df.set_index('uid', inplace=True)

    return df


def _drops_rows_with_missing_values(df):
    logger.info('Eliminando las filas en donde no hay valores')
    return df.dropna()

def _save_data(df, filename):
    logger.info(f'Guardando la informacion en {filename}')
    df.to_csv(f'clean_{filename}')



##
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'archivo',
        help='Archivo con insformacion a transformar',
        type=str
    )

    argumento = parser.parse_args()

    df = main(argumento.archivo)
    print(df)