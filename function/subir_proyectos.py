import sqlite3
import streamlit as st
from function.path import path_ubicacion
from pathlib import Path

def subir_proyecto(titulo= None,cant_tecnologia= None,tecnologia= None,descripcion= None,url= None,github= None):
    
    DB_PATH= path_ubicacion()
    
    
    # Validaciones
    if not all([titulo, cant_tecnologia, tecnologia, descripcion, url, github]):
        st.error("Faltan campos obligatorios.")
        return
    
    try:
        cant = int(cant_tecnologia)
    except Exception:
        st.error("Cantidad de tecnologías inválida.")
        return
    
    tecnologias_string = tecnologia if isinstance(tecnologia, str) else ",".join(map(str, tecnologia))
    
    nombre_para_db = str(url.name)
    BASE_DIR = Path(__file__).resolve().parent.parent
    ruta_assets = BASE_DIR / "assets" / nombre_para_db 

    # 2. PROCESO MÁGICO: Copiar de la web a la carpeta 'assets'
    try:
        # Abrimos un archivo nuevo en 'assets' con el nombre del que subiste
        with open(ruta_assets, "wb") as f:
            # Escribimos los bytes que vienen del navegador
            f.write(url.getbuffer())
    except Exception as e:
        st.write(f"Error con la carga de imagen, {e}")

    if not github.lower().startswith("https://github.com/maxicoceres-data/"):
        st.error("La URL de GitHub debe comenzar con https://github.com/maxicoceres-data/")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO proyectos (titulo,tecnologia,descripcion,url,github) VALUES (?,?,?,?,?)", (titulo,tecnologias_string,descripcion,nombre_para_db,github))
        
        conn.commit()
    except Exception as e:
        st.error(f'Error al subir proyecto: {e}')
    finally:
        try:
            conn.close()
        except:
            pass
    