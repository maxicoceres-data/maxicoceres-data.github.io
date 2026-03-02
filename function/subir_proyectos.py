import sqlite3
from pathlib import Path

def subir_proyecto():
    #conectar o crear base de datos
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_FOLDER = BASE_DIR / "data"
    DB_PATH = DATA_FOLDER / "proyectos.db"

    DATA_FOLDER.mkdir(parents=True, exist_ok=True)
    
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    proyectos = []
    
    while True:
        print("\n--- Cargando nuevo proyecto ---")
        titulo = input("Titulo del proyecto: ")
        tecnologia = input("Tecnologia del proyecto: ")
        descripcion = input("Descripción del proyecto: ")
        while True:
            url = input("Url del video o imagen: ")
            if url.lower().endswith((".png",".mp4")):
                break
            else:
                print("El archivo tiene que ser un png o mp4.")
        
        while True:
            github = input("Enlace de Github: ")
            if github.lower().startswith("https://github.com/maxicoceres-data/"):
                break
            else:
                print("Tiene que ser una URL de github.")
        
        proyecto = (titulo,tecnologia,descripcion,url,github)
        proyectos.append(proyecto)
        
        continuar = input("Desea agregar otro proyecto (s/n): ").lower()
        if continuar != "s":
            break
        
    cursor.executemany("INSERT INTO proyectos (titulo,tecnologia,descripcion,url,github) VALUES (?,?,?,?,?)", proyectos)
    
    conn.commit()
    conn.close()
    
    print("Datos subidos correctamente.")