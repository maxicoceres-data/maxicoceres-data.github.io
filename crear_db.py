import sqlite3
from pathlib import Path
from function.subir_proyectos import subir_proyecto

#crear ruta para la base de datos

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR /"data" / "proyectos.db"


#conectar o crear base de datos
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


#crear tabla de base de datos

cursor.execute('''
    CREATE TABLE IF NOT EXISTS proyectos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        tecnologia TEXT,
        descripcion TEXT,
        url TEXT,
        github TEXT
    )
''')

conn.commit()
conn.close()

subir_proyecto()
