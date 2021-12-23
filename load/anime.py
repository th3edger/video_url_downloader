from sqlalchemy import Column, String
from base import Base

class Anime(Base):
    __tablename__ = 'animes'

    id = Column(String, primary_key=True)
    titulo_de_la_serie = Column(String)
    nombre_del_capitulo = Column(String)
    url = Column(String, unique=True)

    def __init__(
        self,
        uid,
        titulo,
        nombre_c,
        url
    ):
        self.id = uid,
        self.titulo_de_la_serie = titulo,
        self.nombre_del_capitulo = nombre_c,
        self.url = url