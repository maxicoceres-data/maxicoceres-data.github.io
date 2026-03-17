from pathlib import Path

def path_ubicacion():
    # 1. Ubicación de este archivo (path.py)
    current_file = Path(__file__).resolve() 
    
    # 2. Subir a la raíz del proyecto (PORTFOLIO_ANALISIS)
    # path.py está en /function, así que el padre es /function y el abuelo es la raíz.
    BASE_DIR = current_file.parent.parent
    
    # 3. Apuntar a la carpeta data que está en la raíz
    DB_PATH = BASE_DIR / "data" / "proyectos.db"
    
    # Aseguramos que la carpeta exista (por si acaso)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    return DB_PATH