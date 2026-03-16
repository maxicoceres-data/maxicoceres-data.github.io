from pathlib import Path

def path_ubicacion():
    #conectar o crear base de datos
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_FOLDER = BASE_DIR / "data"
    DB_PATH = DATA_FOLDER / "proyectos.db"
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)
    
    return DB_PATH