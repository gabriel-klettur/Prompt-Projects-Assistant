# modelos_db.py
#* contiene las definciones de los modelos y la configuración de la base de datos.

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Archivo(Base):
    __tablename__ = 'archivos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)

# Configuración de la conexión a la base de datos
engine = create_engine('sqlite:///bd_project_python.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
