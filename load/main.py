import argparse
import logging

import pandas as pd

from sqlalchemy import engine
from sqlalchemy.orm import session
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from anime import Anime
from base import Base, engine, Session


def main(archivo):
    Base.metadata.create_all(engine)
    session = Session()
    animes = pd.read_csv(archivo)

    for index, row in animes.iterrows():
        logger.info(f"Cargando el anime de {archivo} dentro de la BD")
        anime = Anime(
            row['uid'],
            row['Titulo de la Serie'],
            row['Nombre del Capitulo'],
            row['url']
        )
        session.add(anime)

    session.commit()
    session.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        'archivo',
        help='El archivo al que deseas cargar en la BD',
        type=str
    )

    argumento = parser.parse_args()

    main(argumento.archivo)