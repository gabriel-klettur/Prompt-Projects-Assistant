# operaciones_db.py
# Contiene funciones para:
#   - guardar_archivo: Guarda un archivo en la base de datos.
#   - obtener_archivos: Obtiene todos los archivos guardados en la base de datos.


from modelos_db import Archivo, Session

session = Session()

def guardar_archivo(nombre_archivo, contenido_archivo):
    archivo = Archivo(nombre=nombre_archivo, contenido=contenido_archivo)
    session.add(archivo)
    session.commit()

def obtener_archivos():
    return session.query(Archivo).all()


